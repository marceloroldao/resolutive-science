"""T61 mean-field degree law for the frozen T25 generator.

Mathematical graph-process test only. No physical mapping is asserted.
"""
from __future__ import annotations

import json
import math
import random

M = 5
K = 6
N = 500_000
SEEDS = (811, 857, 907)
ETA = 0.1
MAX_ITERS = 100_000


def parent_probabilities(p):
    tails = [sum(p[i:]) for i in range(K)]
    pK = p[-1]
    fallback = pK ** M
    s = [0.0] * K
    for i in range(K - 1):
        denom = 1.0 - pK
        if denom <= 0.0:
            raise RuntimeError("invalid all-saturated fixed-point state")
        s[i] = tails[i] ** M - tails[i + 1] ** M + fallback * p[i] / denom
    s[-1] = 0.0
    return s


def flow_map(p):
    s = parent_probabilities(p)
    f = [0.0] * K
    f[0] = 1.0 - s[0]
    for i in range(1, K - 1):
        f[i] = s[i - 1] - s[i]
    f[-1] = s[-2]
    return f, s


def solve_fixed_point():
    p = [0.5, 0.25, 0.125, 0.0625, 0.03125, 0.03125]
    total = sum(p)
    p = [x / total for x in p]
    converged = False
    for iteration in range(1, MAX_ITERS + 1):
        f, _ = flow_map(p)
        updated = [(1.0 - ETA) * x + ETA * y for x, y in zip(p, f)]
        p = updated
        f2, s2 = flow_map(p)
        residual = max(abs(x - y) for x, y in zip(p, f2))
        if residual <= 1e-13:
            converged = True
            break
    else:
        iteration = MAX_ITERS
        f2, s2 = flow_map(p)
        residual = max(abs(x - y) for x, y in zip(p, f2))

    normalization_error = abs(sum(p) - 1.0)
    mean_degree = sum((i + 1) * p[i] for i in range(K))
    mean_degree_error = abs(mean_degree - 2.0)
    wedge_density = sum(math.comb(i + 1, 2) * p[i] for i in range(K))
    parent_sum_error = abs(sum(s2) - 1.0)

    gate = (
        converged
        and residual <= 1e-13
        and normalization_error <= 1e-13
        and mean_degree_error <= 1e-10
        and parent_sum_error <= 1e-13
        and all(x >= -1e-14 for x in p)
    )
    return {
        "p": p,
        "parent_selection_s": s2,
        "iterations": iteration,
        "stationarity_residual_max_abs": residual,
        "normalization_error": normalization_error,
        "mean_degree": mean_degree,
        "mean_degree_error": mean_degree_error,
        "parent_probability_sum_error": parent_sum_error,
        "wedge_density_predicted": wedge_density,
        "fixed_point_gate": gate,
    }


def simulate_exact_t25_degrees(n, seed):
    rng = random.Random(seed)
    degrees = [0] * n
    degrees[0] = 1
    degrees[1] = 1
    counts = [0] * (K + 1)
    counts[1] = 2
    fallback_count = 0

    for v in range(2, n):
        candidates = rng.sample(range(v), min(M, v))
        candidates = sorted(candidates, key=lambda u: (degrees[u], rng.random()))

        chosen = None
        for u in candidates:
            if degrees[u] < K:
                chosen = u
                break

        if chosen is None:
            fallback_count += 1
            available = [u for u in range(v) if degrees[u] < K]
            if not available:
                raise RuntimeError("no unsaturated parent available")
            chosen = rng.choice(available)

        old = degrees[chosen]
        counts[old] -= 1
        degrees[chosen] = old + 1
        counts[old + 1] += 1

        degrees[v] = 1
        counts[1] += 1

    p = [counts[k] / n for k in range(1, K + 1)]
    mean_degree = sum(k * counts[k] for k in range(1, K + 1)) / n
    wedge_density = sum(math.comb(k, 2) * counts[k] for k in range(1, K + 1)) / n
    return {
        "seed": seed,
        "n": n,
        "counts": counts[1:],
        "p_empirical": p,
        "mean_degree": mean_degree,
        "wedge_density_empirical": wedge_density,
        "fallback_count": fallback_count,
    }


def run():
    fixed = solve_fixed_point()
    if not fixed["fixed_point_gate"]:
        return {
            "protocol": "T61 frozen",
            "status": "FIXED_POINT_FAIL",
            "fixed_point": fixed,
            "new_physics": "NOT_ESTABLISHED",
        }

    expected = fixed["p"]
    wedge_expected = fixed["wedge_density_predicted"]
    rows = []
    for seed in SEEDS:
        row = simulate_exact_t25_degrees(N, seed)
        errors = [row["p_empirical"][i] - expected[i] for i in range(K)]
        tv = 0.5 * sum(abs(x) for x in errors)
        max_abs = max(abs(x) for x in errors)
        wedge_error = row["wedge_density_empirical"] - wedge_expected
        row.update({
            "degree_class_errors": errors,
            "degree_total_variation": tv,
            "degree_max_abs_error": max_abs,
            "wedge_density_error": wedge_error,
            "degree_law_seed_gate": tv <= 0.005 and max_abs <= 0.005,
            "wedge_seed_gate": abs(wedge_error) <= 0.02,
        })
        rows.append(row)

    degree_gate = all(row["degree_law_seed_gate"] for row in rows)
    wedge_gate = all(row["wedge_seed_gate"] for row in rows)

    return {
        "protocol": "T61 frozen",
        "status": "MATHEMATICAL_GRAPH_PROCESS_TEST",
        "generator": {
            "m": M,
            "max_degree": K,
            "n": N,
            "seeds": list(SEEDS),
            "sampling": "without replacement",
            "tie_break": "one RNG random per sampled candidate in sorting key",
            "fallback": "uniform among unsaturated vertices only if sampled candidates all saturated",
        },
        "fixed_point": fixed,
        "heldout": rows,
        "T61_FIXED_POINT": fixed["fixed_point_gate"],
        "T61_DEGREE_LAW": degree_gate,
        "T61_WEDGE_DENSITY": wedge_gate,
        "T61_OVERALL": bool(fixed["fixed_point_gate"] and degree_gate and wedge_gate),
        "physical_mapping": "NONE",
        "new_physics": "NOT_ESTABLISHED",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))
    if not result.get("T61_OVERALL", False):
        raise SystemExit(1)
