"""T63 parent-child age-alignment null test.

Tests only A1 = mean[(parent+1)/(child+1)] under exact child-quota
and recursive-order parent swaps. M3/M7 are intentionally absent.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import statistics

from t25_endogenous_dimension_scan import generate
from t47_degree_preserving_recursive_order_null import extract_parent

N = 4096
SEEDS = (1031, 1063, 1097)
NULLS = 999
BURN_IN = 5000
THIN = 500
PROPOSAL_CEILING = 5_000_000
OVERLAP_MAX = 0.25


def a1(parent):
    n = len(parent)
    return math.fsum(
        (parent[v] + 1.0) / (v + 1.0)
        for v in range(1, n)
    ) / (n - 1)


def log_age(parent):
    n = len(parent)
    # Algebraically split the log ratio into separate sums to make the
    # child-quota invariance numerically explicit and stable.
    parent_term = math.fsum(
        math.log(parent[v] + 1.0)
        for v in range(1, n)
    )
    child_term = math.fsum(
        math.log(v + 1.0)
        for v in range(1, n)
    )
    return (child_term - parent_term) / (n - 1)


def child_quota(parent):
    out = [0] * len(parent)
    for v in range(1, len(parent)):
        out[parent[v]] += 1
    return out


def assignment_digest(parent):
    # Stable compact identity for duplicate-state rejection.
    raw = ",".join(map(str, parent[1:])).encode("ascii")
    return hashlib.blake2b(raw, digest_size=16).hexdigest()


def summarize(values):
    ordered = sorted(values)
    n = len(ordered)

    def quantile(q):
        if n == 1:
            return ordered[0]
        x = (n - 1) * q
        lo = int(math.floor(x))
        hi = int(math.ceil(x))
        if lo == hi:
            return ordered[lo]
        w = x - lo
        return ordered[lo] * (1.0 - w) + ordered[hi] * w

    mean = statistics.fmean(values)
    sd = statistics.pstdev(values)
    return {
        "mean": mean,
        "sd": sd,
        "q005": quantile(0.005),
        "median": quantile(0.5),
        "q995": quantile(0.995),
        "min": ordered[0],
        "max": ordered[-1],
    }


def run_parent(seed):
    parent_adj = generate(N, seed)
    original = extract_parent(parent_adj)
    current = list(original)
    original_quota = child_quota(original)
    original_a1 = a1(original)
    original_L = log_age(original)

    rng = random.Random(17000023 * N + 17011 * seed)
    accepted = 0
    proposals = 0
    stored_a1 = []
    stored_L_error = []
    overlaps = []
    digests = set()

    while proposals < PROPOSAL_CEILING and len(stored_a1) < NULLS:
        proposals += 1
        a, b = rng.sample(range(1, N), 2)
        x = current[a]
        y = current[b]

        if x == y:
            continue
        if not (y < a and x < b):
            continue

        current[a], current[b] = y, x
        accepted += 1

        if accepted <= BURN_IN:
            continue
        if (accepted - BURN_IN) % THIN != 0:
            continue

        overlap = sum(
            1 for v in range(1, N)
            if current[v] == original[v]
        ) / (N - 1)
        if overlap > OVERLAP_MAX:
            continue

        digest = assignment_digest(current)
        if digest in digests:
            continue

        # Explicitly verify the frozen structural invariants at storage time.
        quota_ok = child_quota(current) == original_quota
        recursive_ok = all(0 <= current[v] < v for v in range(1, N))
        if not (quota_ok and recursive_ok):
            raise RuntimeError("parent-swap invariant failure")

        value = a1(current)
        L_error = log_age(current) - original_L

        digests.add(digest)
        stored_a1.append(value)
        stored_L_error.append(L_error)
        overlaps.append(overlap)

    feasible = len(stored_a1) == NULLS
    null_summary = summarize(stored_a1) if stored_a1 else None
    overlap_summary = summarize(overlaps) if overlaps else None
    max_L_error = max((abs(x) for x in stored_L_error), default=float("inf"))

    identified = bool(
        feasible
        and null_summary is not None
        and original_a1 > null_summary["q995"]
        and max_L_error <= 1e-12
    )

    if null_summary and null_summary["sd"] > 0:
        z = (original_a1 - null_summary["mean"]) / null_summary["sd"]
    else:
        z = None

    return {
        "seed": seed,
        "n": N,
        "parent_A1": original_a1,
        "parent_L": original_L,
        "proposals": proposals,
        "accepted_swaps": accepted,
        "stored_nulls": len(stored_a1),
        "null_feasible": feasible,
        "null_A1": null_summary,
        "parent_minus_null_sd": z,
        "overlap": overlap_summary,
        "max_abs_L_invariant_error": max_L_error,
        "L_invariant_gate": max_L_error <= 1e-12,
        "directional_A1_gate": bool(
            null_summary is not None
            and original_a1 > null_summary["q995"]
        ),
        "identified_seed": identified,
    }


def run():
    rows = [run_parent(seed) for seed in SEEDS]
    feasibility = all(row["null_feasible"] for row in rows)
    invariant = all(row["L_invariant_gate"] for row in rows)
    identified = all(row["directional_A1_gate"] for row in rows)

    return {
        "protocol": "T63 frozen",
        "status": "MATHEMATICAL_PARENT_CHILD_PAIRING_TEST",
        "N": N,
        "seeds": list(SEEDS),
        "nulls_per_parent": NULLS,
        "primary_statistic": "A1=mean((parent+1)/(child+1))",
        "frozen_direction": "HIGH",
        "rows": rows,
        "T63_STRUCTURAL_FEASIBILITY": feasibility,
        "T63_LOG_AGE_INVARIANT": invariant,
        "T63_AGE_ALIGNMENT": bool(feasibility and invariant and identified),
        "M3_M7_computed": False,
        "physical_time": "NOT_DERIVED",
        "new_physics": "NOT_ESTABLISHED",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))
    if not (
        result["T63_STRUCTURAL_FEASIBILITY"]
        and result["T63_LOG_AGE_INVARIANT"]
    ):
        raise SystemExit(1)
