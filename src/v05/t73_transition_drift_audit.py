"""T73 exact one-step transition-drift audit.

Exhaustively enumerates every unordered child-pair proposal from the exact
T25 parent. M3/M7 are intentionally absent.
"""
from __future__ import annotations

import json
import math

from t25_endogenous_dimension_scan import generate
from t47_degree_preserving_recursive_order_null import extract_parent
from t69_joint_moment_covariance_intervention import (
    covariance_stats,
    delta_moments,
    contrib_for_parent,
    replace_sorted,
)

N = 4096
SEEDS = (1571, 1601, 1627)
BANDS = {
    1571: (0.0004944836316886312, 0.0009186559308883041, 0.0011213160862183868, 0.0004111725745889904),
    1601: (0.00042495772627906657, 0.0007304893212312395, 0.0008568639442333685, 0.0004673920464498475),
    1627: (0.0003892352154036993, 0.0007408779933725684, 0.0009407445205092983, 0.0004918636938616715),
}
EPS = 1e-15


def run_parent(seed):
    adj = generate(N, seed)
    parent = extract_parent(adj)
    c0 = covariance_stats(parent)
    ek = c0["E_K"]
    events = c0["events"]
    children = c0["children"]
    base_contrib = [contrib_for_parent(u, children[u]) for u in range(N)]
    bands = BANDS[seed]

    total_pairs = (N - 1) * (N - 2) // 2
    valid = 0
    band_feasible = 0

    sums = [0.0] * 4
    sums2 = [0.0] * 4
    min_d = [float("inf")] * 4
    max_d = [float("-inf")] * 4

    sum_a1_c = 0.0

    a1_pos = a1_neg = 0
    c_neg = c_pos = 0
    joint_outward = 0

    for a in range(1, N - 1):
        x = parent[a]
        for b in range(a + 1, N):
            y = parent[b]
            if x == y:
                continue
            if not (y < a and x < b):
                continue

            valid += 1
            dm = delta_moments(N, a, b, x, y)

            old_x_r, old_x_kr, _ = base_contrib[x]
            old_y_r, old_y_kr, _ = base_contrib[y]
            new_x = replace_sorted(children[x], a, b)
            new_y = replace_sorted(children[y], b, a)
            new_x_r, new_x_kr, _ = contrib_for_parent(x, new_x)
            new_y_r, new_y_kr, _ = contrib_for_parent(y, new_y)

            delta_sr = new_x_r + new_y_r - old_x_r - old_y_r
            delta_skr = new_x_kr + new_y_kr - old_x_kr - old_y_kr
            dc = (delta_skr / events) - ek * (delta_sr / events)

            d = (dm[0], dm[1], dm[2], dc)

            if all(abs(d[i]) <= bands[i] + 1e-18 for i in range(4)):
                band_feasible += 1

            for i, value in enumerate(d):
                sums[i] += value
                sums2[i] += value * value
                min_d[i] = min(min_d[i], value)
                max_d[i] = max(max_d[i], value)

            sum_a1_c += d[0] * d[3]

            if d[0] > EPS:
                a1_pos += 1
            elif d[0] < -EPS:
                a1_neg += 1

            if d[3] < -EPS:
                c_neg += 1
            elif d[3] > EPS:
                c_pos += 1

            if d[0] > EPS and d[3] < -EPS:
                joint_outward += 1

    if valid == 0:
        raise RuntimeError("no structurally valid swaps")

    means = [x / valid for x in sums]
    variances = [
        max(0.0, sums2[i] / valid - means[i] * means[i])
        for i in range(4)
    ]
    sds = [math.sqrt(v) for v in variances]

    cov_a1_c = sum_a1_c / valid - means[0] * means[3]
    corr_a1_c = (
        cov_a1_c / (sds[0] * sds[3])
        if sds[0] > 0 and sds[3] > 0
        else None
    )

    unconditional = [x / total_pairs for x in sums]

    return {
        "seed": seed,
        "total_unordered_pair_proposals": total_pairs,
        "structurally_valid_swaps": valid,
        "valid_fraction": valid / total_pairs,
        "four_band_feasible_swaps": band_feasible,
        "all_valid_inside_frozen_bands": band_feasible == valid,
        "conditional_mean_delta": {
            "A1": means[0],
            "A2": means[1],
            "A3": means[2],
            "C_KR": means[3],
        },
        "conditional_sd_delta": {
            "A1": sds[0],
            "A2": sds[1],
            "A3": sds[2],
            "C_KR": sds[3],
        },
        "unconditional_proposal_mean_delta": {
            "A1": unconditional[0],
            "A2": unconditional[1],
            "A3": unconditional[2],
            "C_KR": unconditional[3],
        },
        "delta_min": {
            "A1": min_d[0], "A2": min_d[1], "A3": min_d[2], "C_KR": min_d[3]
        },
        "delta_max": {
            "A1": max_d[0], "A2": max_d[1], "A3": max_d[2], "C_KR": max_d[3]
        },
        "cov_delta_A1_C_KR": cov_a1_c,
        "corr_delta_A1_C_KR": corr_a1_c,
        "sign_counts": {
            "A1_positive": a1_pos,
            "A1_negative": a1_neg,
            "C_more_negative": c_neg,
            "C_less_negative": c_pos,
            "joint_A1_up_C_more_negative": joint_outward,
        },
        "sign_fractions_valid": {
            "A1_positive": a1_pos / valid,
            "A1_negative": a1_neg / valid,
            "C_more_negative": c_neg / valid,
            "C_less_negative": c_pos / valid,
            "joint_A1_up_C_more_negative": joint_outward / valid,
        },
        "drift_A1_negative": means[0] < 0,
        "drift_C_less_negative": means[3] > 0,
        "drift_gate": means[0] < 0 and means[3] > 0,
    }


def run():
    rows = [run_parent(seed) for seed in SEEDS]
    return {
        "protocol": "T73 frozen",
        "status": "EXACT_ONE_STEP_TRANSITION_DRIFT_AUDIT",
        "N": N,
        "seeds": list(SEEDS),
        "rows": rows,
        "T73_ALL_VALID_INSIDE_BANDS": all(r["all_valid_inside_frozen_bands"] for r in rows),
        "T73_DRIFT_MATCHES_T70_T71": all(r["drift_gate"] for r in rows),
        "M3_M7_computed": False,
        "stationary_distribution": "NOT_DERIVED",
        "physical_mapping": "NONE",
        "new_physics": "NOT_ESTABLISHED",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
