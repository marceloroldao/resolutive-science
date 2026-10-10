"""T76 entropy-corrected matched null sampler validation.

Derives a local 2D diffusion tilt in (A1, C_KR), applies the inverse tilt as
a Metropolis-Hastings importance weight inside the unchanged hard
A1/A2/A3/C_KR matching box, and validates centering/bracketing without M3/M7.
"""
from __future__ import annotations

import json
import math
import random
import statistics

from t25_endogenous_dimension_scan import generate
from t47_degree_preserving_recursive_order_null import extract_parent
from t69_joint_moment_covariance_intervention import (
    moments,
    child_quota,
    covariance_stats,
    summary,
    digest_parent,
    overlap,
    propose,
    delta_moments,
    contrib_for_parent,
    replace_sorted,
)

N = 4096
SEEDS = (1753, 1789, 1811)
NULLS = 99
CHAINS = 9
STATES_PER_CHAIN = 11
BURN_IN = 2000
THIN = 200
STAGE_A_CEILING = 10_000_000
CHAIN_CEILING = 2_000_000
OVERLAP_MAX = 0.90
CENTER_FRACTION = 0.20


def stage_a(original, seed):
    current = list(original)
    quota = child_quota(original)
    rng = random.Random(49000049 * N + 49003 * seed)
    accepted = proposals = 0
    vals = [[], [], [], []]
    ovs = []
    seen = set()

    while proposals < STAGE_A_CEILING and len(vals[0]) < NULLS:
        proposals += 1
        mv = propose(current, rng)
        if mv is None:
            continue
        a, b, x, y = mv
        current[a], current[b] = y, x
        accepted += 1

        if accepted <= BURN_IN or (accepted - BURN_IN) % THIN:
            continue

        ov = overlap(current, original)
        if ov > OVERLAP_MAX:
            continue

        d = digest_parent(current)
        if d in seen:
            continue

        if child_quota(current) != quota:
            raise RuntimeError("Stage A quota invariant failure")
        if not all(0 <= current[v] < v for v in range(1, N)):
            raise RuntimeError("Stage A recursive-order failure")

        mm = moments(current)
        cc = covariance_stats(current)["C_KR"]
        seen.add(d)
        for i, value in enumerate(mm):
            vals[i].append(value)
        vals[3].append(cc)
        ovs.append(ov)

    return {
        "feasible": len(vals[0]) == NULLS,
        "proposals": proposals,
        "accepted": accepted,
        "vals": vals,
        "overlaps": ovs,
    }


def local_two_dimensional_law(original, limits):
    c0 = covariance_stats(original)
    ek = c0["E_K"]
    events = c0["events"]
    children = c0["children"]
    base_contrib = [contrib_for_parent(u, children[u]) for u in range(N)]

    structurally_valid = 0
    locally_accepted = 0

    sa = sc = saa = scc = sac = 0.0

    for a in range(1, N - 1):
        x = original[a]
        for b in range(a + 1, N):
            y = original[b]
            if x == y:
                continue
            if not (y < a and x < b):
                continue

            structurally_valid += 1
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

            if not (
                abs(dm[0]) <= limits[0] + 1e-18
                and abs(dm[1]) <= limits[1] + 1e-18
                and abs(dm[2]) <= limits[2] + 1e-18
                and abs(dc) <= limits[3] + 1e-18
            ):
                continue

            locally_accepted += 1
            da = dm[0]
            sa += da
            sc += dc
            saa += da * da
            scc += dc * dc
            sac += da * dc

    if locally_accepted == 0:
        raise RuntimeError("no locally accepted moves")

    mu_a = sa / locally_accepted
    mu_c = sc / locally_accepted
    var_a = max(0.0, saa / locally_accepted - mu_a * mu_a)
    var_c = max(0.0, scc / locally_accepted - mu_c * mu_c)
    cov_ac = sac / locally_accepted - mu_a * mu_c

    det = var_a * var_c - cov_ac * cov_ac
    if not (det > 0.0):
        raise RuntimeError("singular local covariance")

    lambda_a = 2.0 * (var_c * mu_a - cov_ac * mu_c) / det
    lambda_c = 2.0 * (-cov_ac * mu_a + var_a * mu_c) / det

    return {
        "structurally_valid": structurally_valid,
        "locally_accepted": locally_accepted,
        "mu": {"A1": mu_a, "C_KR": mu_c},
        "covariance": {
            "A1_A1": var_a,
            "A1_C_KR": cov_ac,
            "C_KR_C_KR": var_c,
            "det": det,
        },
        "lambda": {"A1": lambda_a, "C_KR": lambda_c},
        "reconstructed_mu": {
            "A1": 0.5 * (var_a * lambda_a + cov_ac * lambda_c),
            "C_KR": 0.5 * (cov_ac * lambda_a + var_c * lambda_c),
        },
    }


def run_one_corrected_chain(
    original, seed, chain_index, limits, lambda_a, lambda_c, global_seen
):
    current = list(original)
    quota = child_quota(original)
    target_m = list(moments(original))
    cov0 = covariance_stats(original)
    target_c = cov0["C_KR"]

    cur_m = list(target_m)
    cur_sr = cov0["sum_R"]
    cur_skr = cov0["sum_KR"]
    ek = cov0["E_K"]
    events = cov0["events"]
    children = [list(x) for x in cov0["children"]]

    rng = random.Random(
        53000047 * N + 53017 * seed + 1000003 * chain_index
    )

    proposals = 0
    band_valid = 0
    mh_accepted = 0
    stored = []
    vals = [[], [], [], []]
    ovs = []

    while proposals < CHAIN_CEILING and len(stored) < STATES_PER_CHAIN:
        proposals += 1
        mv = propose(current, rng)
        if mv is None:
            continue

        a, b, x, y = mv
        dm = delta_moments(N, a, b, x, y)
        cand_m = [cur_m[i] + dm[i] for i in range(3)]
        if any(abs(cand_m[i] - target_m[i]) > limits[i] for i in range(3)):
            continue

        old_x_r, old_x_kr, _ = contrib_for_parent(x, children[x])
        old_y_r, old_y_kr, _ = contrib_for_parent(y, children[y])
        new_x = replace_sorted(children[x], a, b)
        new_y = replace_sorted(children[y], b, a)
        new_x_r, new_x_kr, _ = contrib_for_parent(x, new_x)
        new_y_r, new_y_kr, _ = contrib_for_parent(y, new_y)

        cand_sr = cur_sr + (new_x_r + new_y_r - old_x_r - old_y_r)
        cand_skr = cur_skr + (new_x_kr + new_y_kr - old_x_kr - old_y_kr)
        cand_c = (cand_skr / events) - ek * (cand_sr / events)

        if abs(cand_c - target_c) > limits[3]:
            continue

        band_valid += 1

        log_alpha = -(lambda_a * dm[0] + lambda_c * (cand_c - (cur_skr / events - ek * (cur_sr / events))))
        if log_alpha < 0.0 and math.log(rng.random()) >= log_alpha:
            continue

        current[a], current[b] = y, x
        children[x] = new_x
        children[y] = new_y
        cur_m = cand_m
        cur_sr = cand_sr
        cur_skr = cand_skr
        mh_accepted += 1

        if mh_accepted <= BURN_IN or (mh_accepted - BURN_IN) % THIN:
            continue

        ov = overlap(current, original)
        if ov > OVERLAP_MAX:
            continue

        d = digest_parent(current)
        if d in global_seen:
            continue

        if child_quota(current) != quota:
            raise RuntimeError("corrected Stage B quota invariant failure")
        if not all(0 <= current[v] < v for v in range(1, N)):
            raise RuntimeError("corrected Stage B recursive-order failure")

        exact_m = moments(current)
        exact_c = covariance_stats(current)["C_KR"]

        if any(abs(exact_m[i] - target_m[i]) > limits[i] + 1e-12 for i in range(3)):
            raise RuntimeError("corrected Stage B moment box failure")
        if abs(exact_c - target_c) > limits[3] + 1e-12:
            raise RuntimeError("corrected Stage B covariance box failure")

        global_seen.add(d)
        stored.append(list(current))
        for i, value in enumerate(exact_m):
            vals[i].append(value)
        vals[3].append(exact_c)
        ovs.append(ov)

    return {
        "chain_index": chain_index,
        "feasible": len(stored) == STATES_PER_CHAIN,
        "proposals": proposals,
        "band_valid_proposals": band_valid,
        "mh_accepted": mh_accepted,
        "stored": stored,
        "vals": vals,
        "overlaps": ovs,
    }


def stage_b_corrected(original, seed, limits, lambdas):
    pooled = []
    vals = [[], [], [], []]
    ovs = []
    global_seen = set()
    chain_rows = []

    for chain_index in range(CHAINS):
        row = run_one_corrected_chain(
            original,
            seed,
            chain_index,
            limits,
            lambdas["A1"],
            lambdas["C_KR"],
            global_seen,
        )

        chain_rows.append({
            "chain_index": chain_index,
            "feasible": row["feasible"],
            "proposals": row["proposals"],
            "band_valid_proposals": row["band_valid_proposals"],
            "mh_accepted": row["mh_accepted"],
            "stored": len(row["stored"]),
        })

        if not row["feasible"]:
            return {
                "feasible": False,
                "stored": pooled,
                "vals": vals,
                "overlaps": ovs,
                "chains": chain_rows,
            }

        pooled.extend(row["stored"])
        for i in range(4):
            vals[i].extend(row["vals"][i])
        ovs.extend(row["overlaps"])

    return {
        "feasible": len(pooled) == NULLS,
        "stored": pooled,
        "vals": vals,
        "overlaps": ovs,
        "chains": chain_rows,
    }


def run_parent(seed):
    parent = extract_parent(generate(N, seed))
    targets = list(moments(parent)) + [covariance_stats(parent)["C_KR"]]

    sa = stage_a(parent, seed)
    row = {
        "seed": seed,
        "targets": {
            "A1": targets[0],
            "A2": targets[1],
            "A3": targets[2],
            "C_KR": targets[3],
        },
        "stage_a_feasible": sa["feasible"],
        "stage_a_stored": len(sa["vals"][0]),
    }
    if not sa["feasible"]:
        return row

    sums = [summary(sa["vals"][i]) for i in range(4)]
    limits = [0.25 * s["sd"] for s in sums]
    row["bands"] = {
        "A1": limits[0],
        "A2": limits[1],
        "A3": limits[2],
        "C_KR": limits[3],
    }

    local = local_two_dimensional_law(parent, limits)
    row["local_law"] = local

    sb = stage_b_corrected(parent, seed, limits, local["lambda"])
    row["stage_b_feasible"] = sb["feasible"]
    row["stage_b_stored"] = len(sb["stored"])
    row["stage_b_chains"] = sb["chains"]

    if not sb["feasible"]:
        return row

    coordinate_summaries = [summary(sb["vals"][i]) for i in range(4)]
    row["stage_b_summary"] = {
        "A1": coordinate_summaries[0],
        "A2": coordinate_summaries[1],
        "A3": coordinate_summaries[2],
        "C_KR": coordinate_summaries[3],
    }
    row["overlap"] = summary(sb["overlaps"])

    bracket = [
        min(sb["vals"][i]) <= targets[i] <= max(sb["vals"][i])
        for i in range(4)
    ]

    mean_offsets = [
        statistics.fmean(sb["vals"][i]) - targets[i]
        for i in range(4)
    ]
    center_a = abs(mean_offsets[0]) <= CENTER_FRACTION * limits[0]
    center_c = abs(mean_offsets[3]) <= CENTER_FRACTION * limits[3]

    row["mean_offset"] = {
        "A1": mean_offsets[0],
        "A2": mean_offsets[1],
        "A3": mean_offsets[2],
        "C_KR": mean_offsets[3],
    }
    row["parent_bracketing"] = {
        "A1": bracket[0],
        "A2": bracket[1],
        "A3": bracket[2],
        "C_KR": bracket[3],
    }
    row["centering_gate"] = {
        "A1": center_a,
        "C_KR": center_c,
    }
    row["seed_gate"] = all(bracket) and center_a and center_c
    return row


def run():
    rows = [run_parent(seed) for seed in SEEDS]
    feasible = all(
        r.get("stage_a_feasible", False)
        and r.get("stage_b_feasible", False)
        for r in rows
    )
    validated = feasible and all(r.get("seed_gate", False) for r in rows)

    return {
        "protocol": "T76 frozen",
        "status": "ENTROPY_CORRECTED_SAMPLER_VALIDATION",
        "N": N,
        "seeds": list(SEEDS),
        "rows": rows,
        "T76_FEASIBILITY": feasible,
        "T76_CORRECTED_SAMPLER_VALIDATED": validated,
        "M3_M7_computed": False,
        "physical_entropy": "NOT_CLAIMED",
        "physical_mapping": "NONE",
        "new_physics": "NOT_ESTABLISHED",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))
    if not result["T76_FEASIBILITY"]:
        raise SystemExit(1)
