"""T75 confirmatory reflected-diffusion sampler-bias test.

New held-out N=4096 parents. Predictions from exact local accepted-step
drift/diffusion are computed before constrained multi-chain sampling.
M3/M7 are intentionally absent.
"""
from __future__ import annotations

import hashlib
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
SEEDS = (1663, 1693, 1721)
NULLS = 99
CHAINS = 9
STATES_PER_CHAIN = 11
BURN_IN = 2000
THIN = 200
STAGE_A_CEILING = 10_000_000
CHAIN_CEILING = 1_000_000
OVERLAP_MAX = 0.90


def stage_a(original, seed):
    current = list(original)
    quota = child_quota(original)
    rng = random.Random(43000019 * N + 43003 * seed)
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


def local_accepted_law(original, limits):
    c0 = covariance_stats(original)
    ek = c0["E_K"]
    events = c0["events"]
    children = c0["children"]
    base_contrib = [contrib_for_parent(u, children[u]) for u in range(N)]

    structurally_valid = 0
    accepted = 0

    sum_a = sum_a2 = 0.0
    sum_c = sum_c2 = 0.0

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

            accepted += 1
            da = dm[0]
            sum_a += da
            sum_a2 += da * da
            sum_c += dc
            sum_c2 += dc * dc

    if accepted == 0:
        raise RuntimeError("no locally accepted moves")

    mu_a = sum_a / accepted
    mu_c = sum_c / accepted
    var_a = max(0.0, sum_a2 / accepted - mu_a * mu_a)
    var_c = max(0.0, sum_c2 / accepted - mu_c * mu_c)
    sd_a = math.sqrt(var_a)
    sd_c = math.sqrt(var_c)

    return {
        "structurally_valid": structurally_valid,
        "locally_accepted": accepted,
        "mu_A1": mu_a,
        "sd_A1": sd_a,
        "mu_C_KR": mu_c,
        "sd_C_KR": sd_c,
    }


def reflected_mean_offset(mu, sd, delta):
    if sd <= 0:
        raise RuntimeError("nonpositive diffusion scale")
    variance = sd * sd
    kappa = 2.0 * mu / variance
    z = kappa * delta
    if abs(z) < 1e-8:
        return 0.0, kappa, z
    mean = delta / math.tanh(z) - 1.0 / kappa
    return mean, kappa, z


def run_one_chain(original, seed, chain_index, limits, global_seen):
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
        47000027 * N + 47017 * seed + 1000003 * chain_index
    )
    accepted = proposals = 0
    stored = []
    vals = [[], [], [], []]

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

        current[a], current[b] = y, x
        children[x] = new_x
        children[y] = new_y
        cur_m = cand_m
        cur_sr = cand_sr
        cur_skr = cand_skr
        accepted += 1

        if accepted <= BURN_IN or (accepted - BURN_IN) % THIN:
            continue

        ov = overlap(current, original)
        if ov > OVERLAP_MAX:
            continue

        d = digest_parent(current)
        if d in global_seen:
            continue

        if child_quota(current) != quota:
            raise RuntimeError("Stage B quota invariant failure")
        if not all(0 <= current[v] < v for v in range(1, N)):
            raise RuntimeError("Stage B recursive-order failure")

        exact_m = moments(current)
        exact_c = covariance_stats(current)["C_KR"]
        if any(abs(exact_m[i] - target_m[i]) > limits[i] + 1e-12 for i in range(3)):
            raise RuntimeError("Stage B moment accounting failure")
        if abs(exact_c - target_c) > limits[3] + 1e-12:
            raise RuntimeError("Stage B covariance accounting failure")

        global_seen.add(d)
        stored.append(list(current))
        for i, value in enumerate(exact_m):
            vals[i].append(value)
        vals[3].append(exact_c)

    return {
        "chain_index": chain_index,
        "feasible": len(stored) == STATES_PER_CHAIN,
        "proposals": proposals,
        "accepted": accepted,
        "stored": stored,
        "vals": vals,
    }


def stage_b_multichain(original, seed, limits):
    pooled = []
    vals = [[], [], [], []]
    global_seen = set()
    chain_rows = []

    for chain_index in range(CHAINS):
        row = run_one_chain(
            original, seed, chain_index, limits, global_seen
        )
        chain_rows.append({
            "chain_index": chain_index,
            "feasible": row["feasible"],
            "proposals": row["proposals"],
            "accepted": row["accepted"],
            "stored": len(row["stored"]),
        })

        if not row["feasible"]:
            return {
                "feasible": False,
                "stored": pooled,
                "vals": vals,
                "chains": chain_rows,
            }

        pooled.extend(row["stored"])
        for i in range(4):
            vals[i].extend(row["vals"][i])

    return {
        "feasible": len(pooled) == NULLS,
        "stored": pooled,
        "vals": vals,
        "chains": chain_rows,
    }


def ratio_gate(predicted, observed):
    if predicted == 0.0:
        return False, None, False
    sign_match = predicted * observed > 0.0
    ratio = abs(observed / predicted)
    pass_gate = sign_match and 0.80 <= ratio <= 1.20
    return sign_match, ratio, pass_gate


def run_parent(seed):
    parent = extract_parent(generate(N, seed))
    parent_m = list(moments(parent))
    parent_c = covariance_stats(parent)["C_KR"]

    sa = stage_a(parent, seed)
    row = {
        "seed": seed,
        "parent_A1": parent_m[0],
        "parent_A2": parent_m[1],
        "parent_A3": parent_m[2],
        "parent_C_KR": parent_c,
        "stage_a_feasible": sa["feasible"],
        "stage_a_stored": len(sa["vals"][0]),
    }
    if not sa["feasible"]:
        return row

    sums = [summary(sa["vals"][i]) for i in range(4)]
    limits = [0.25 * s["sd"] for s in sums]
    row["stage_a_summary"] = {
        "A1": sums[0],
        "A2": sums[1],
        "A3": sums[2],
        "C_KR": sums[3],
    }
    row["bands"] = {
        "A1": limits[0],
        "A2": limits[1],
        "A3": limits[2],
        "C_KR": limits[3],
    }

    local = local_accepted_law(parent, limits)
    pred_a, k_a, z_a = reflected_mean_offset(
        local["mu_A1"], local["sd_A1"], limits[0]
    )
    pred_c, k_c, z_c = reflected_mean_offset(
        local["mu_C_KR"], local["sd_C_KR"], limits[3]
    )

    # Predictions are fixed before Stage B starts.
    row["local_law"] = local
    row["predicted_offset"] = {
        "A1": pred_a,
        "C_KR": pred_c,
    }
    row["diffusion_parameters"] = {
        "A1": {"kappa": k_a, "z": z_a},
        "C_KR": {"kappa": k_c, "z": z_c},
    }

    sb = stage_b_multichain(parent, seed, limits)
    row["stage_b_feasible"] = sb["feasible"]
    row["stage_b_stored"] = len(sb["stored"])
    row["stage_b_chains"] = sb["chains"]

    if not sb["feasible"]:
        return row

    obs_a = statistics.fmean(sb["vals"][0]) - parent_m[0]
    obs_c = statistics.fmean(sb["vals"][3]) - parent_c

    sign_a, ratio_a, gate_a = ratio_gate(pred_a, obs_a)
    sign_c, ratio_c, gate_c = ratio_gate(pred_c, obs_c)

    row["observed_offset"] = {
        "A1": obs_a,
        "C_KR": obs_c,
    }
    row["comparison"] = {
        "A1": {
            "sign_match": sign_a,
            "magnitude_ratio_observed_over_predicted": ratio_a,
            "gate": gate_a,
        },
        "C_KR": {
            "sign_match": sign_c,
            "magnitude_ratio_observed_over_predicted": ratio_c,
            "gate": gate_c,
        },
    }
    row["seed_gate"] = gate_a and gate_c
    return row


def run():
    rows = [run_parent(seed) for seed in SEEDS]
    feasible = all(
        r.get("stage_a_feasible", False)
        and r.get("stage_b_feasible", False)
        for r in rows
    )
    confirmed = feasible and all(r.get("seed_gate", False) for r in rows)

    return {
        "protocol": "T75 frozen",
        "status": "CONFIRMATORY_REFLECTED_DIFFUSION_TEST",
        "N": N,
        "seeds": list(SEEDS),
        "rows": rows,
        "T75_FEASIBILITY": feasible,
        "T75_REFLECTED_DIFFUSION_CONFIRMED": confirmed,
        "M3_M7_computed": False,
        "physical_diffusion": "NOT_CLAIMED",
        "physical_mapping": "NONE",
        "new_physics": "NOT_ESTABLISHED",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))
    if not result["T75_FEASIBILITY"]:
        raise SystemExit(1)
