"""T78 entropy-balanced reweighting of the exact T77 candidate ensembles.

Regenerates the deterministic 99-state T77 ensemble for each parent and
calibrates strictly positive exponential-tilting weights so the weighted
mean of normalized controls (A1,A2,A3,C_KR) is zero. M3/M7 are absent.
"""
from __future__ import annotations

import json
import math

import numpy as np

from t25_endogenous_dimension_scan import generate
from t47_degree_preserving_recursive_order_null import extract_parent
from t69_joint_moment_covariance_intervention import moments, covariance_stats, summary
from t77_full4d_entropy_corrected_sampler import (
    N,
    SEEDS,
    NULLS,
    PINV_RCOND,
    stage_a,
    local_full4d_law,
    stage_b_corrected,
)

MAX_ITER = 100
TOL = 1e-10
ESS_MIN = 50.0
MAX_WEIGHT_MAX = 0.05
MAX_BACKTRACK = 80


def softmax_weights(y, theta):
    logits = y.dot(theta)
    shift = float(np.max(logits))
    ex = np.exp(logits - shift)
    total = float(np.sum(ex))
    if not math.isfinite(total) or total <= 0.0:
        raise RuntimeError("nonfinite softmax normalizer")
    return ex / total


def weighted_moments(y, weights):
    mean = weights.dot(y)
    centered = y - mean
    cov = (centered * weights[:, None]).T.dot(centered)
    cov = 0.5 * (cov + cov.T)
    return mean, cov


def calibrate(y):
    theta = np.zeros(y.shape[1], dtype=float)
    converged = False
    history = []
    weights = np.full(y.shape[0], 1.0 / y.shape[0], dtype=float)

    for iteration in range(MAX_ITER + 1):
        weights = softmax_weights(y, theta)
        mean, cov = weighted_moments(y, weights)
        norm_inf = float(np.max(np.abs(mean)))
        history.append(norm_inf)

        if norm_inf <= TOL:
            converged = True
            break

        if iteration == MAX_ITER:
            break

        step = np.linalg.pinv(cov, rcond=PINV_RCOND).dot(mean)
        accepted = False
        alpha = 1.0

        for _ in range(MAX_BACKTRACK):
            candidate_theta = theta - alpha * step
            candidate_w = softmax_weights(y, candidate_theta)
            candidate_mean, _ = weighted_moments(y, candidate_w)
            candidate_norm = float(np.max(np.abs(candidate_mean)))

            if candidate_norm < norm_inf:
                theta = candidate_theta
                accepted = True
                break

            alpha *= 0.5

        if not accepted:
            break

    weights = softmax_weights(y, theta)
    mean, cov = weighted_moments(y, weights)
    residual = float(np.max(np.abs(mean)))
    ess = float(1.0 / np.sum(weights * weights))
    max_weight = float(np.max(weights))
    min_weight = float(np.min(weights))
    positive = bool(np.all(weights > 0.0))

    eigvals = np.linalg.eigvalsh(cov)
    maxeig = float(np.max(np.abs(eigvals))) if len(eigvals) else 0.0
    rank_tol = PINV_RCOND * maxeig
    rank = int(np.sum(np.abs(eigvals) > rank_tol))

    return {
        "converged": bool(converged and residual <= TOL),
        "iterations": len(history) - 1,
        "theta": theta.tolist(),
        "weighted_mean_y": mean.tolist(),
        "max_abs_weighted_mean_y": residual,
        "ess": ess,
        "max_weight": max_weight,
        "min_weight": min_weight,
        "positive_support": positive,
        "weighted_covariance_eigenvalues": eigvals.tolist(),
        "weighted_covariance_rank": rank,
        "gradient_norm_history": history,
        "weights": weights,
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
        "stage_a_feasible": sa["feasible"],
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
    sb = stage_b_corrected(parent, seed, limits.tolist(), local["lambda_y"])

    row["candidate_feasible"] = sb["feasible"]
    row["candidate_stored"] = len(sb["stored"])
    if not sb["feasible"]:
        return row

    values = np.column_stack([
        np.asarray(sb["vals"][i], dtype=float)
        for i in range(4)
    ])

    if values.shape != (NULLS, 4):
        raise RuntimeError("unexpected T77 candidate matrix shape")

    y = (values - targets[None, :]) / limits[None, :]
    inside_box = bool(np.all(np.abs(y) <= 1.0 + 1e-12))
    bracket = [
        float(np.min(values[:, i])) <= targets[i] <= float(np.max(values[:, i]))
        for i in range(4)
    ]

    row["all_candidates_inside_hard_box"] = inside_box
    row["parent_bracketing"] = {
        "A1": bracket[0],
        "A2": bracket[1],
        "A3": bracket[2],
        "C_KR": bracket[3],
    }
    row["candidate_mean_y"] = np.mean(y, axis=0).tolist()

    if not (inside_box and all(bracket)):
        row["candidate_reconstruction_gate"] = False
        return row

    row["candidate_reconstruction_gate"] = True

    cal = calibrate(y)
    weights = cal.pop("weights")

    weighted_raw = weights.dot(values)
    raw_offset = weighted_raw - targets

    row["calibration"] = cal
    row["weighted_raw_mean"] = {
        "A1": float(weighted_raw[0]),
        "A2": float(weighted_raw[1]),
        "A3": float(weighted_raw[2]),
        "C_KR": float(weighted_raw[3]),
    }
    row["weighted_raw_offset"] = {
        "A1": float(raw_offset[0]),
        "A2": float(raw_offset[1]),
        "A3": float(raw_offset[2]),
        "C_KR": float(raw_offset[3]),
    }

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
        "protocol": "T78 frozen",
        "status": "ENTROPY_BALANCED_REWEIGHTING_VALIDATION",
        "N": N,
        "seeds": list(SEEDS),
        "candidate_states_per_parent": NULLS,
        "newton_tolerance": TOL,
        "pinv_rcond": PINV_RCOND,
        "ess_min": ESS_MIN,
        "max_weight_max": MAX_WEIGHT_MAX,
        "rows": rows,
        "T78_CANDIDATE_RECONSTRUCTION": candidate_gate,
        "T78_ENTROPY_BALANCING_VALIDATED": validated,
        "M3_M7_computed": False,
        "physical_entropy": "NOT_CLAIMED",
        "physical_mapping": "NONE",
        "new_physics": "NOT_ESTABLISHED",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))
    if not result["T78_CANDIDATE_RECONSTRUCTION"]:
        raise SystemExit(1)
