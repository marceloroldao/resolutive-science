"""T64 direct A1-matched recursive-order intervention.

Stage A calibrates only A1 dispersion under ordinary quota-preserving recursive
nulls. Stage B matches A1 directly. M3/M7 are evaluated only after Stage-B
states are frozen.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import statistics

from t25_endogenous_dimension_scan import generate
from t47_degree_preserving_recursive_order_null import extract_parent, build_adj
from t39_higher_order_topology_source import m3_m7

N = 2048
SEEDS = (1129, 1151, 1187)
NULLS = 99
BURN_IN = 2000
THIN = 200
STAGE_A_CEILING = 1_000_000
STAGE_B_CEILING = 5_000_000
OVERLAP_MAX = 0.90


def a1(parent):
    return math.fsum(
        (parent[v] + 1.0) / (v + 1.0)
        for v in range(1, len(parent))
    ) / (len(parent) - 1)


def child_quota(parent):
    out = [0] * len(parent)
    for v in range(1, len(parent)):
        out[parent[v]] += 1
    return out


def digest_parent(parent):
    raw = ",".join(map(str, parent[1:])).encode("ascii")
    return hashlib.blake2b(raw, digest_size=16).hexdigest()


def edge_overlap(parent, original):
    return sum(
        1 for v in range(1, len(parent))
        if parent[v] == original[v]
    ) / (len(parent) - 1)


def quantile(values, q):
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    x = (len(ordered) - 1) * q
    lo = int(math.floor(x))
    hi = int(math.ceil(x))
    if lo == hi:
        return ordered[lo]
    w = x - lo
    return ordered[lo] * (1.0 - w) + ordered[hi] * w


def summary(values):
    return {
        "mean": statistics.fmean(values),
        "sd": statistics.pstdev(values),
        "q025": quantile(values, 0.025),
        "median": quantile(values, 0.5),
        "q975": quantile(values, 0.975),
        "min": min(values),
        "max": max(values),
    }


def classify(parent_value, null_values):
    q025 = quantile(null_values, 0.025)
    q975 = quantile(null_values, 0.975)
    if parent_value < q025:
        c = "low"
    elif parent_value > q975:
        c = "high"
    else:
        c = "inside"
    s = summary(null_values)
    return {
        "parent": parent_value,
        **{f"null_{k}": v for k, v in s.items()},
        "classification": c,
        "parent_minus_null_sd": (
            (parent_value - s["mean"]) / s["sd"]
            if s["sd"] > 0 else None
        ),
    }


def propose_swap(current, rng):
    a, b = rng.sample(range(1, len(current)), 2)
    x, y = current[a], current[b]
    if x == y:
        return None
    if not (y < a and x < b):
        return None
    return a, b, x, y


def swap_delta_a1(n, a, b, x, y):
    old = (x + 1.0) / (a + 1.0) + (y + 1.0) / (b + 1.0)
    new = (y + 1.0) / (a + 1.0) + (x + 1.0) / (b + 1.0)
    return (new - old) / (n - 1)


def sample_stage_a(original, seed):
    current = list(original)
    original_quota = child_quota(original)
    rng = random.Random(13000019 * N + 13007 * seed)
    accepted = 0
    proposals = 0
    values = []
    overlaps = []
    states = set()

    while proposals < STAGE_A_CEILING and len(values) < NULLS:
        proposals += 1
        move = propose_swap(current, rng)
        if move is None:
            continue
        a, b, x, y = move
        current[a], current[b] = y, x
        accepted += 1

        if accepted <= BURN_IN or (accepted - BURN_IN) % THIN != 0:
            continue

        overlap = edge_overlap(current, original)
        if overlap > OVERLAP_MAX:
            continue
        d = digest_parent(current)
        if d in states:
            continue
        if child_quota(current) != original_quota:
            raise RuntimeError("Stage A quota invariant failure")
        if not all(0 <= current[v] < v for v in range(1, N)):
            raise RuntimeError("Stage A recursive-order failure")

        states.add(d)
        values.append(a1(current))
        overlaps.append(overlap)

    return {
        "feasible": len(values) == NULLS,
        "proposals": proposals,
        "accepted": accepted,
        "values": values,
        "overlaps": overlaps,
    }


def sample_stage_b(original, seed, delta):
    current = list(original)
    original_quota = child_quota(original)
    target = a1(original)
    current_a1 = target
    rng = random.Random(19000081 * N + 19013 * seed)
    accepted = 0
    proposals = 0
    stored = []
    values = []
    overlaps = []
    states = set()

    while proposals < STAGE_B_CEILING and len(stored) < NULLS:
        proposals += 1
        move = propose_swap(current, rng)
        if move is None:
            continue
        a, b, x, y = move
        candidate_a1 = current_a1 + swap_delta_a1(N, a, b, x, y)
        if abs(candidate_a1 - target) > delta:
            continue

        current[a], current[b] = y, x
        current_a1 = candidate_a1
        accepted += 1

        if accepted <= BURN_IN or (accepted - BURN_IN) % THIN != 0:
            continue

        overlap = edge_overlap(current, original)
        if overlap > OVERLAP_MAX:
            continue
        d = digest_parent(current)
        if d in states:
            continue
        if child_quota(current) != original_quota:
            raise RuntimeError("Stage B quota invariant failure")
        if not all(0 <= current[v] < v for v in range(1, N)):
            raise RuntimeError("Stage B recursive-order failure")

        exact_a1 = a1(current)
        if abs(exact_a1 - target) > delta + 1e-12:
            raise RuntimeError("Stage B A1 incremental accounting failure")

        states.add(d)
        stored.append(list(current))
        values.append(exact_a1)
        overlaps.append(overlap)

    realized_match = bool(
        len(values) == NULLS
        and all(abs(x - target) <= delta + 1e-12 for x in values)
        and min(values) <= target <= max(values)
    ) if values else False

    return {
        "feasible": len(stored) == NULLS,
        "proposals": proposals,
        "accepted": accepted,
        "stored": stored,
        "values": values,
        "overlaps": overlaps,
        "realized_match": realized_match,
    }


def run_parent(seed):
    parent_adj = generate(N, seed)
    original = extract_parent(parent_adj)
    parent_a1 = a1(original)

    stage_a = sample_stage_a(original, seed)
    row = {
        "seed": seed,
        "n": N,
        "parent_A1": parent_a1,
        "stage_a_proposals": stage_a["proposals"],
        "stage_a_accepted": stage_a["accepted"],
        "stage_a_stored": len(stage_a["values"]),
        "stage_a_feasible": stage_a["feasible"],
    }
    if not stage_a["feasible"]:
        return row

    stage_a_summary = summary(stage_a["values"])
    sigma = stage_a_summary["sd"]
    delta = 0.25 * sigma
    row["stage_a_A1"] = stage_a_summary
    row["delta_A1"] = delta

    if not (sigma > 0 and delta > 0):
        row["stage_b_feasible"] = False
        return row

    stage_b = sample_stage_b(original, seed, delta)
    row.update({
        "stage_b_proposals": stage_b["proposals"],
        "stage_b_accepted": stage_b["accepted"],
        "stage_b_stored": len(stage_b["stored"]),
        "stage_b_feasible": stage_b["feasible"],
        "stage_b_match_control": stage_b["realized_match"],
        "stage_b_A1": summary(stage_b["values"]) if stage_b["values"] else None,
        "stage_b_overlap": summary(stage_b["overlaps"]) if stage_b["overlaps"] else None,
    })

    if not (stage_b["feasible"] and stage_b["realized_match"]):
        row["heldout_evaluated"] = False
        return row

    # Held out until the full Stage-B ensemble for this parent is frozen.
    parent_m3, parent_m7 = m3_m7(parent_adj)
    null_m3 = []
    null_m7 = []
    for parent_state in stage_b["stored"]:
        adj = build_adj(parent_state)
        m3, m7 = m3_m7(adj)
        null_m3.append(m3)
        null_m7.append(m7)

    row["heldout_evaluated"] = True
    row["M3"] = classify(parent_m3, null_m3)
    row["M7"] = classify(parent_m7, null_m7)
    return row


def run():
    rows = [run_parent(seed) for seed in SEEDS]
    feasibility = all(
        row.get("stage_a_feasible", False)
        and row.get("stage_b_feasible", False)
        and row.get("stage_b_match_control", False)
        for row in rows
    )

    if feasibility:
        accounting = all(
            row["M3"]["classification"] == "inside"
            and row["M7"]["classification"] == "inside"
            for row in rows
        )
        residual_low = all(
            row["M3"]["classification"] == "low"
            and row["M7"]["classification"] == "low"
            for row in rows
        )
    else:
        accounting = False
        residual_low = False

    if accounting:
        outcome = "A1_ACCOUNTING_IDENTIFIED"
    elif residual_low:
        outcome = "LOW_LOW_RESIDUAL_AFTER_A1"
    elif feasibility:
        outcome = "MIXED"
    else:
        outcome = "INFEASIBLE"

    return {
        "protocol": "T64 frozen",
        "status": "DIRECT_A1_MATCHED_RECURSIVE_INTERVENTION",
        "N": N,
        "seeds": list(SEEDS),
        "rows": rows,
        "T64_FEASIBILITY": feasibility,
        "T64_A1_ACCOUNTING": bool(feasibility and accounting),
        "T64_RESIDUAL_AFTER_A1": bool(feasibility and residual_low),
        "T64_OUTCOME": outcome,
        "physical_mapping": "NONE",
        "new_physics": "NOT_ESTABLISHED",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))
    if not result["T64_FEASIBILITY"]:
        raise SystemExit(1)
