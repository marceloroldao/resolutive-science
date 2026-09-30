"""T72 exhaustive local feasible-cone audit.

Enumerates all structurally valid T47 one-swap moves from the exact T25 parent,
under the frozen T70 bands. M3/M7 are intentionally absent.
"""
from __future__ import annotations

import json

from t25_endogenous_dimension_scan import generate
from t47_degree_preserving_recursive_order_null import extract_parent
from t69_joint_moment_covariance_intervention import (
    moments,
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
    target_m = moments(parent)
    c0 = covariance_stats(parent)
    target_c = c0["C_KR"]
    ek = c0["E_K"]
    events = c0["events"]
    children = c0["children"]
    base_contrib = [contrib_for_parent(u, children[u]) for u in range(N)]
    bands = BANDS[seed]

    valid = 0
    feasible = 0
    a1_up = 0
    a1_down = 0
    c_down = 0
    c_up = 0
    joint_outward = 0

    mins = [float("inf")] * 4
    maxs = [float("-inf")] * 4

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
            deltas = (dm[0], dm[1], dm[2], dc)

            if any(abs(deltas[i]) > bands[i] + 1e-18 for i in range(4)):
                continue

            feasible += 1
            for i, value in enumerate(deltas):
                mins[i] = min(mins[i], value)
                maxs[i] = max(maxs[i], value)

            if dm[0] > EPS:
                a1_up += 1
            elif dm[0] < -EPS:
                a1_down += 1

            if dc < -EPS:
                c_down += 1
            elif dc > EPS:
                c_up += 1

            if dm[0] > EPS and dc < -EPS:
                joint_outward += 1

    if feasible == 0:
        mins = [None] * 4
        maxs = [None] * 4

    return {
        "seed": seed,
        "parent_A1": target_m[0],
        "parent_A2": target_m[1],
        "parent_A3": target_m[2],
        "parent_C_KR": target_c,
        "bands": {
            "A1": bands[0], "A2": bands[1], "A3": bands[2], "C_KR": bands[3]
        },
        "structurally_valid_swaps": valid,
        "four_band_feasible_swaps": feasible,
        "delta_min": {"A1": mins[0], "A2": mins[1], "A3": mins[2], "C_KR": mins[3]},
        "delta_max": {"A1": maxs[0], "A2": maxs[1], "A3": maxs[2], "C_KR": maxs[3]},
        "A1_positive_count": a1_up,
        "A1_negative_count": a1_down,
        "C_more_negative_count": c_down,
        "C_less_negative_count": c_up,
        "joint_A1_up_C_more_negative_count": joint_outward,
        "local_boundary_A1": a1_up == 0,
        "local_boundary_C": c_down == 0,
        "joint_outward_reachable": joint_outward > 0,
    }


def run():
    rows = [run_parent(seed) for seed in SEEDS]
    return {
        "protocol": "T72 frozen",
        "status": "LOCAL_FEASIBLE_CONE_AUDIT",
        "N": N,
        "seeds": list(SEEDS),
        "rows": rows,
        "T72_A1_LOCAL_BOUNDARY_ALL3": all(r["local_boundary_A1"] for r in rows),
        "T72_C_LOCAL_BOUNDARY_ALL3": all(r["local_boundary_C"] for r in rows),
        "T72_JOINT_OUTWARD_REACHABLE_ANY": any(r["joint_outward_reachable"] for r in rows),
        "M3_M7_computed": False,
        "global_extremality": "NOT_CLAIMED",
        "physical_mapping": "NONE",
        "new_physics": "NOT_ESTABLISHED",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
