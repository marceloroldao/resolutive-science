"""T40 conditional higher-order structure audit.

Uses the frozen T39 predictor family C,A,G and OLS/LOOCV on the exact T38/T39
degree-matched null ensemble. Regression attribution is forbidden outside null
support.
"""
from __future__ import annotations
import json
import numpy as np

from t25_endogenous_dimension_scan import generate
from t38_degree_matched_tree_null import (
    decode_degree_matched_prufer,
    degree_sequence,
)
from t39_higher_order_topology_source import topology_vector, m3_m7


def ols_loocv(X, y):
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    yhat = X @ beta
    resid = y - yhat
    hat = X @ np.linalg.inv(X.T @ X) @ X.T
    leverage = np.diag(hat)
    loo_resid = resid / (1.0 - leverage)
    loo_pred = y - loo_resid
    denom = np.sum((y - y.mean()) ** 2)
    r2 = 1.0 - np.sum((y - loo_pred) ** 2) / denom
    return beta, loo_resid, float(r2)


def compare_parent(n, parent_seed):
    parent = generate(n, parent_seed)
    degrees = degree_sequence(parent)
    parent_h = topology_vector(parent)
    parent_m3, parent_m7 = m3_m7(parent)

    H = []
    m3s = []
    m7s = []

    for replicate in range(99):
        null_seed = 1000003 * n + 1009 * parent_seed + replicate
        null = decode_degree_matched_prufer(degrees, null_seed)
        H.append(topology_vector(null))
        m3, m7 = m3_m7(null)
        m3s.append(m3)
        m7s.append(m7)

    H = np.vstack(H)
    m3s = np.asarray(m3s, dtype=float)
    m7s = np.asarray(m7s, dtype=float)

    h_mean = H.mean(axis=0)
    h_sd = H.std(axis=0)
    Z = (H - h_mean) / h_sd
    parent_z = (parent_h - h_mean) / h_sd

    C = -(Z[:, 0] + Z[:, 1] + Z[:, 2]) / 3.0
    A = Z[:, 3]
    G = Z[:, 7]

    parent_C = -(parent_z[0] + parent_z[1] + parent_z[2]) / 3.0
    parent_A = parent_z[3]
    parent_G = parent_z[7]

    Y3 = (m3s - m3s.mean()) / m3s.std()
    Y7 = (m7s - m7s.mean()) / m7s.std()
    parent_Y3 = (parent_m3 - m3s.mean()) / m3s.std()
    parent_Y7 = (parent_m7 - m7s.mean()) / m7s.std()

    X = np.column_stack([np.ones(99), C, A, G])
    beta3, loo3, r2_3 = ols_loocv(X, Y3)
    beta7, loo7, r2_7 = ols_loocv(X, Y7)

    support = {}
    for name, parent_value, values in (
        ("C", parent_C, C),
        ("A", parent_A, A),
        ("G", parent_G, G),
    ):
        support[name] = {
            "parent": float(parent_value),
            "null_min": float(values.min()),
            "null_max": float(values.max()),
            "q005": float(np.quantile(values, 0.005)),
            "q995": float(np.quantile(values, 0.995)),
            "inside_min_max": bool(values.min() <= parent_value <= values.max()),
        }

    interpolation_safe = all(x["inside_min_max"] for x in support.values())

    parent_design = np.asarray([1.0, parent_C, parent_A, parent_G])
    pred3 = float(parent_design @ beta3)
    pred7 = float(parent_design @ beta7)
    residual3 = float(parent_Y3 - pred3)
    residual7 = float(parent_Y7 - pred7)

    return {
        "n": n,
        "parent_seed": parent_seed,
        "loocv_r2_Y3": r2_3,
        "loocv_r2_Y7": r2_7,
        "support": support,
        "interpolation_safe": interpolation_safe,
        "parent_Y3": float(parent_Y3),
        "parent_Y7": float(parent_Y7),
        "extrapolated_prediction_Y3": pred3,
        "extrapolated_prediction_Y7": pred7,
        "extrapolated_residual_Y3": residual3,
        "extrapolated_residual_Y7": residual7,
        "null_abs_loo_residual_Y3_q95": float(np.quantile(np.abs(loo3), 0.95)),
        "null_abs_loo_residual_Y3_q975": float(np.quantile(np.abs(loo3), 0.975)),
        "null_abs_loo_residual_Y7_q95": float(np.quantile(np.abs(loo7), 0.95)),
        "null_abs_loo_residual_Y7_q975": float(np.quantile(np.abs(loo7), 0.975)),
        "beta_Y3": [float(x) for x in beta3],
        "beta_Y7": [float(x) for x in beta7],
    }


def run():
    rows = [
        compare_parent(n, seed)
        for n in (128, 256, 512)
        for seed in (11, 23, 47)
    ]
    median_r2_y3 = float(np.median([x["loocv_r2_Y3"] for x in rows]))
    median_r2_y7 = float(np.median([x["loocv_r2_Y7"] for x in rows]))
    safe_count = sum(x["interpolation_safe"] for x in rows)

    return {
        "protocol": "T40 frozen",
        "rows": rows,
        "median_loocv_r2_Y3": median_r2_y3,
        "median_loocv_r2_Y7": median_r2_y7,
        "predictive_adequacy_Y3": median_r2_y3 >= 0.50,
        "predictive_adequacy_Y7": median_r2_y7 >= 0.50,
        "interpolation_safe_parents": safe_count,
        "conditional_attribution": (
            "ELIGIBLE_FOR_RESIDUAL_GATE"
            if safe_count == 9
            else "UNDERDETERMINED_OUTSIDE_NULL_SUPPORT"
        ),
        "guard": (
            "No posthoc features, nonlinear rescue, extrapolative attribution, "
            "graph evolution, transition law, or physical geometry."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
