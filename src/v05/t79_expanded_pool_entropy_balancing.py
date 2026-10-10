"""T79 expanded-pool entropy-balancing validation.

Regenerates the T77 full-4D corrected candidate mechanism but uses
27 independent chains (297 unique states) per retained parent, then applies
the unchanged T78 maximum-entropy control calibration. M3/M7 are absent.
"""
from __future__ import annotations

import json
import statistics

import numpy as np

from t25_endogenous_dimension_scan import generate
from t47_degree_preserving_recursive_order_null import extract_parent
from t69_joint_moment_covariance_intervention import moments, covariance_stats, summary
from t77_full4d_entropy_corrected_sampler import (
    N,
    SEEDS,
    PINV_RCOND,
    OVERLAP_MAX,
    stage_a,
    local_full4d_law,
    run_one_corrected_chain,
)
from t78_entropy_balanced_reweighting import (
    calibrate,
    TOL,
    ESS_MIN,
    MAX_WEIGHT_MAX,
)

CHAINS = 27
STATES_PER_CHAIN = 11
TOTAL_CANDIDATES = CHAINS * STATES_PER_CHAIN


def expanded_candidates(original, seed, limits, lambda_y):
    pooled = []
    vals = [[], [], [], []]
    overlaps = []
    chain_rows = []
    global_seen = set()

    for chain_index in range(CHAINS):
        row = run_one_corrected_chain(
            original,
            seed,
            chain_index,
            limits,
            lambda_y,
            global_seen,
        )
        chain_rows.append({
            "chain_index": chain_index,
            "feasible": bool(row["feasible"]),
            "proposals": int(row["proposals"]),
            "box_valid_proposals": int(row["box_valid_proposals"]),
            "mh_accepted": int(row["mh_accepted"]),
            "stored": len(row["stored"]),
        })

        if not row["feasible"]:
            return {
                "feasible": False,
                "stored": pooled,
                "vals": vals,
                "overlaps": overlaps,
                "chains": chain_rows,
            }

        pooled.extend(row["stored"])
        for i in range(4):
            vals[i].extend(row["vals"][i])
        overlaps.extend(row["overlaps"])

    return {
        "feasible": len(pooled) == TOTAL_CANDIDATES,
        "stored": pooled,
        "vals": vals,
        "overlaps": overlaps,
        "chains": chain_rows,
    }


def concentration_counts(weights):
    ordered = np.sort(np.asarray(weights, dtype=float))[::-1]
    cumulative = np.cumsum(ordered)

    def first_count(level):
        return int(np.searchsorted(cumulative, level, side="left") + 1)

    return {
        "states_for_50pct_weight": first_count(0.50),
        "states_for_80pct_weight": first_count(0.80),
        "states_for_95pct_weight": first_count(0.95),
    }


def run_parent(seed):
    parent = extract_parent(generate(N, seed))
    targets = np.asarray(
        list(moments(parent)) + [covariance_stats(parent)["C_KR"]],
        dtype=float,
    )

    sa = stage_a(parent, seed)
    row = {
        "seed": seed,
        "stage_a_feasible": bool(sa["feasible"]),
        "stage_a_stored": len(sa["vals"][0]),
    }
    if not sa["feasible"]:
        return row

    sums = [summary(sa["vals"][i]) for i in range(4)]
    limits = np.asarray([0.25 * s["sd"] for s in sums], dtype=float)
    row["bands"] = {
        "A1": float(limits[0]),
        "A2": float(limits[1]),
        "A3": float(limits[2]),
        "C_KR": float(limits[3]),
    }

    local = local_full4d_law(parent, limits.tolist())
    row["local_rank"] = int(local["rank"])
    row["local_reconstruction_residual"] = float(
        local["reconstruction_residual_norm"]
    )

    pool = expanded_candidates(
        parent, seed, limits.tolist(), local["lambda_y"]
    )
    row["candidate_feasible"] = bool(pool["feasible"])
    row["candidate_stored"] = len(pool["stored"])
    row["chains"] = pool["chains"]

    if not pool["feasible"]:
        return row

    values = np.column_stack([
        np.asarray(pool["vals"][i], dtype=float)
        for i in range(4)
    ])
    if values.shape != (TOTAL_CANDIDATES, 4):
        raise RuntimeError("unexpected T79 candidate matrix shape")

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
    row["candidate_mean_y"] = np.mean(y, axis=0).tolist()
    row["candidate_reconstruction_gate"] = bool(inside and all(bracket))

    if not row["candidate_reconstruction_gate"]:
        return row

    cal = calibrate(y)
    weights = cal.pop("weights")
    weighted_raw = weights.dot(values)
    raw_offset = weighted_raw - targets

    concentration = concentration_counts(weights)
    cal["ess_fraction"] = float(cal["ess"] / TOTAL_CANDIDATES)
    cal["max_weight_over_uniform"] = float(
        cal["max_weight"] / (1.0 / TOTAL_CANDIDATES)
    )
    cal["concentration"] = concentration

    row["calibration"] = cal
    row["weighted_raw_offset"] = {
        "A1": float(raw_offset[0]),
        "A2": float(raw_offset[1]),
        "A3": float(raw_offset[2]),
        "C_KR": float(raw_offset[3]),
    }
    row["candidate_overlap"] = summary(pool["overlaps"])

    gates = {
        "convergence": bool(cal["converged"]),
        "ess": bool(cal["ess"] >= ESS_MIN),
        "max_weight": bool(cal["max_weight"] <= MAX_WEIGHT_MAX),
        "positive_support": bool(cal["positive_support"]),
    }
    row["gates"] = gates
    row["seed_gate"] = bool(all(gates.values()))
    return row


def run():
    rows = [run_parent(seed) for seed in SEEDS]
    candidate_gate = all(
        row.get("candidate_reconstruction_gate", False)
        for row in rows
    )
    validated = candidate_gate and all(
        row.get("seed_gate", False)
        for row in rows
    )

    return {
        "protocol": "T79 frozen",
        "status": "EXPANDED_POOL_ENTROPY_BALANCING_VALIDATION",
        "N": N,
        "seeds": list(SEEDS),
        "candidate_chains": CHAINS,
        "states_per_chain": STATES_PER_CHAIN,
        "total_candidates": TOTAL_CANDIDATES,
        "newton_tolerance": TOL,
        "pinv_rcond": PINV_RCOND,
        "ess_min_unchanged": ESS_MIN,
        "max_weight_max_unchanged": MAX_WEIGHT_MAX,
        "rows": rows,
        "T79_CANDIDATE_RECONSTRUCTION": candidate_gate,
        "T79_EXPANDED_BALANCING_VALIDATED": validated,
        "M3_M7_computed": False,
        "physical_entropy": "NOT_CLAIMED",
        "physical_mapping": "NONE",
        "new_physics": "NOT_ESTABLISHED",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))
    if not result["T79_CANDIDATE_RECONSTRUCTION"]:
        raise SystemExit(1)
