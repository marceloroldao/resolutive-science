"""T80 weighted larger-N M3/M7 structural accounting replication.

Regenerates the exact deterministic T79 297-state candidate ensembles and
control-only entropy weights. M3/M7 are computed only after all T79 gates
pass. Weighted empirical quantiles use first cumulative crossing.
"""
from __future__ import annotations

import json
import math
import statistics

import numpy as np

from t25_endogenous_dimension_scan import generate
from t47_degree_preserving_recursive_order_null import extract_parent, build_adj
from t39_higher_order_topology_source import m3_m7
from t69_joint_moment_covariance_intervention import moments, covariance_stats, summary
from t77_full4d_entropy_corrected_sampler import (
    N,
    SEEDS,
    PINV_RCOND,
    stage_a,
    local_full4d_law,
)
from t78_entropy_balanced_reweighting import (
    calibrate,
    TOL,
    ESS_MIN,
    MAX_WEIGHT_MAX,
)
from t79_expanded_pool_entropy_balancing import (
    expanded_candidates,
    TOTAL_CANDIDATES,
)


def weighted_response_summary(values, weights):
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    weights = weights / np.sum(weights)

    order = np.argsort(values, kind="mergesort")
    v = values[order]
    w = weights[order]
    cum = np.cumsum(w)

    def wq(p):
        idx = int(np.searchsorted(cum, p, side="left"))
        if idx >= len(v):
            idx = len(v) - 1
        return float(v[idx])

    mean = float(np.dot(weights, values))
    var = float(np.dot(weights, (values - mean) ** 2))

    return {
        "weighted_mean": mean,
        "weighted_sd": math.sqrt(max(0.0, var)),
        "q025": wq(0.025),
        "median": wq(0.5),
        "q975": wq(0.975),
        "min": float(np.min(values)),
        "max": float(np.max(values)),
    }


def classify(parent_value, response_summary):
    q025 = response_summary["q025"]
    q975 = response_summary["q975"]
    if parent_value < q025:
        return "low"
    if parent_value > q975:
        return "high"
    return "inside"


def prepare_frozen_parent(seed):
    parent_adj = generate(N, seed)
    parent = extract_parent(parent_adj)
    targets = np.asarray(
        list(moments(parent)) + [covariance_stats(parent)["C_KR"]],
        dtype=float,
    )

    sa = stage_a(parent, seed)
    if not sa["feasible"]:
        return {
            "seed": seed,
            "feasible": False,
            "failure_stage": "stage_a",
        }

    sums = [summary(sa["vals"][i]) for i in range(4)]
    limits = np.asarray([0.25 * s["sd"] for s in sums], dtype=float)

    local = local_full4d_law(parent, limits.tolist())
    pool = expanded_candidates(
        parent,
        seed,
        limits.tolist(),
        local["lambda_y"],
    )

    row = {
        "seed": seed,
        "stage_a_feasible": bool(sa["feasible"]),
        "candidate_feasible": bool(pool["feasible"]),
        "candidate_stored": len(pool["stored"]),
        "bands": {
            "A1": float(limits[0]),
            "A2": float(limits[1]),
            "A3": float(limits[2]),
            "C_KR": float(limits[3]),
        },
    }

    if not pool["feasible"] or len(pool["stored"]) != TOTAL_CANDIDATES:
        row["feasible"] = False
        row["failure_stage"] = "candidate_generation"
        return row

    values = np.column_stack([
        np.asarray(pool["vals"][i], dtype=float)
        for i in range(4)
    ])

    y = (values - targets[None, :]) / limits[None, :]
    inside = bool(np.all(np.abs(y) <= 1.0 + 1e-12))
    bracket = [
        bool(float(np.min(values[:, i])) <= float(targets[i]) <= float(np.max(values[:, i])))
        for i in range(4)
    ]

    row["all_candidates_inside_hard_box"] = inside
    row["parent_bracketing"] = {
        "A1": bracket[0],
        "A2": bracket[1],
        "A3": bracket[2],
        "C_KR": bracket[3],
    }

    if not (inside and all(bracket)):
        row["feasible"] = False
        row["failure_stage"] = "candidate_control_gate"
        return row

    cal = calibrate(y)
    weights = np.asarray(cal.pop("weights"), dtype=float)
    weights = weights / np.sum(weights)

    gates = {
        "convergence": bool(cal["converged"] and cal["max_abs_weighted_mean_y"] <= TOL),
        "ess": bool(cal["ess"] >= ESS_MIN),
        "max_weight": bool(cal["max_weight"] <= MAX_WEIGHT_MAX),
        "positive_support": bool(cal["positive_support"] and np.all(weights > 0.0)),
    }

    weighted_control_mean_y = weights.dot(y)
    row["calibration"] = {
        "theta": cal["theta"],
        "max_abs_weighted_mean_y": cal["max_abs_weighted_mean_y"],
        "ess": cal["ess"],
        "max_weight": cal["max_weight"],
        "min_weight": cal["min_weight"],
        "gates": gates,
    }

    if not all(gates.values()):
        row["feasible"] = False
        row["failure_stage"] = "weight_quality_gate"
        return row

    row["feasible"] = True
    row["weighted_control_mean_y"] = weighted_control_mean_y.tolist()

    return {
        **row,
        "_parent_adj": parent_adj,
        "_candidate_states": pool["stored"],
        "_weights": weights,
    }


def evaluate_heldout(prepared):
    seed = prepared["seed"]
    parent_adj = prepared["_parent_adj"]
    states = prepared["_candidate_states"]
    weights = prepared["_weights"]

    # Held out until graph states and control-only weights are fully frozen.
    parent_m3, parent_m7 = m3_m7(parent_adj)

    null_m3 = []
    null_m7 = []
    for parent_state in states:
        m3, m7 = m3_m7(build_adj(parent_state))
        null_m3.append(m3)
        null_m7.append(m7)

    wm3 = weighted_response_summary(null_m3, weights)
    wm7 = weighted_response_summary(null_m7, weights)

    u3 = summary(null_m3)
    u7 = summary(null_m7)

    return {
        "seed": seed,
        "M3": {
            "parent": parent_m3,
            "weighted": wm3,
            "classification": classify(parent_m3, wm3),
            "unweighted_descriptive": u3,
            "parent_minus_weighted_mean_sd": (
                (parent_m3 - wm3["weighted_mean"]) / wm3["weighted_sd"]
                if wm3["weighted_sd"] > 0 else None
            ),
        },
        "M7": {
            "parent": parent_m7,
            "weighted": wm7,
            "classification": classify(parent_m7, wm7),
            "unweighted_descriptive": u7,
            "parent_minus_weighted_mean_sd": (
                (parent_m7 - wm7["weighted_mean"]) / wm7["weighted_sd"]
                if wm7["weighted_sd"] > 0 else None
            ),
        },
    }


def public_control_row(prepared):
    return {
        k: v
        for k, v in prepared.items()
        if not k.startswith("_")
    }


def run():
    prepared_rows = [prepare_frozen_parent(seed) for seed in SEEDS]

    feasible = all(row.get("feasible", False) for row in prepared_rows)
    if not feasible:
        return {
            "protocol": "T80 frozen",
            "status": "WEIGHTED_LARGER_N_ACCOUNTING_REPLICATION",
            "N": N,
            "seeds": list(SEEDS),
            "control_rows": [public_control_row(r) for r in prepared_rows],
            "heldout_rows": [],
            "T80_FEASIBILITY": False,
            "T80_ACCOUNTING_REPLICATED": False,
            "T80_RESIDUAL": False,
            "T80_OUTCOME": "INFEASIBLE",
            "M3_M7_computed": False,
            "physical_mapping": "NONE",
            "new_physics": "NOT_ESTABLISHED",
        }

    heldout_rows = [evaluate_heldout(row) for row in prepared_rows]

    accounting = all(
        row["M3"]["classification"] == "inside"
        and row["M7"]["classification"] == "inside"
        for row in heldout_rows
    )
    residual = all(
        row["M3"]["classification"] == "low"
        and row["M7"]["classification"] == "low"
        for row in heldout_rows
    )

    if accounting:
        outcome = "LARGER_N_ACCOUNTING_REPLICATED"
    elif residual:
        outcome = "LOW_LOW_RESIDUAL"
    else:
        outcome = "MIXED"

    return {
        "protocol": "T80 frozen",
        "status": "WEIGHTED_LARGER_N_ACCOUNTING_REPLICATION",
        "N": N,
        "seeds": list(SEEDS),
        "candidate_states_per_parent": TOTAL_CANDIDATES,
        "weighted_quantile_rule": "FIRST_CUMULATIVE_CROSSING_NO_INTERPOLATION",
        "control_rows": [public_control_row(r) for r in prepared_rows],
        "heldout_rows": heldout_rows,
        "T80_FEASIBILITY": True,
        "T80_ACCOUNTING_REPLICATED": accounting,
        "T80_RESIDUAL": residual,
        "T80_OUTCOME": outcome,
        "M3_M7_computed": True,
        "physical_mapping": "NONE",
        "new_physics": "NOT_ESTABLISHED",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))
    if not result["T80_FEASIBILITY"]:
        raise SystemExit(1)
