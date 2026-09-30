"""T62 derived parent-age kernel for the frozen T25 choice dynamics.

Mathematical causal-order statistic only; birth labels are not physical time.
"""
from __future__ import annotations

import json
import math
import random

from t61_mean_field_degree_law import K, M, solve_fixed_point

N = 500_000
SEEDS = (941, 977, 1013)


def theoretical_moments():
    fixed = solve_fixed_point()
    if not fixed["fixed_point_gate"]:
        raise RuntimeError("T61 fixed point did not converge under frozen gates")

    p = fixed["p"]
    s = fixed["parent_selection_s"]
    rates = [s[k] / p[k] for k in range(K - 1)]

    def moment(r):
        total = 0.0
        prefix = 1.0
        for k, ak in enumerate(rates):
            if k > 0:
                prefix *= rates[k - 1]
            denom = 1.0
            for j in range(k + 1):
                denom *= r + 1.0 + rates[j]
            total += ak * prefix / denom
        return total

    def log_moment():
        total = 0.0
        prefix = 1.0
        r = 0.0
        for k, ak in enumerate(rates):
            if k > 0:
                prefix *= rates[k - 1]
            denom = 1.0
            for j in range(k + 1):
                denom *= r + 1.0 + rates[j]
            term = ak * prefix / denom
            total += term * sum(
                1.0 / (r + 1.0 + rates[j])
                for j in range(k + 1)
            )
        return total

    return {
        "degree_fraction_p": p,
        "parent_class_probability_s": s,
        "class_selection_rate_a": rates,
        "M0": moment(0.0),
        "M1": moment(1.0),
        "M2": moment(2.0),
        "M3": moment(3.0),
        "L_log_age": log_moment(),
    }


def simulate(n, seed):
    rng = random.Random(seed)
    degrees = [0] * n
    degrees[0] = 1
    degrees[1] = 1

    # Include the initial frozen edge 0 -> 1 using the finite-label convention.
    r0 = (0 + 1) / (1 + 1)
    sums = [r0, r0 * r0, r0 ** 3, -math.log(r0)]
    edge_count = 1
    fallback_count = 0

    for v in range(2, n):
        candidates = rng.sample(range(v), min(M, v))
        candidates = sorted(
            candidates,
            key=lambda u: (degrees[u], rng.random()),
        )

        parent = None
        for u in candidates:
            if degrees[u] < K:
                parent = u
                break

        if parent is None:
            fallback_count += 1
            available = [u for u in range(v) if degrees[u] < K]
            if not available:
                raise RuntimeError("no unsaturated parent")
            parent = rng.choice(available)

        r = (parent + 1) / (v + 1)
        sums[0] += r
        sums[1] += r * r
        sums[2] += r ** 3
        sums[3] += -math.log(r)
        edge_count += 1

        degrees[parent] += 1
        degrees[v] = 1

    return {
        "seed": seed,
        "n": n,
        "edge_count": edge_count,
        "M1_empirical": sums[0] / edge_count,
        "M2_empirical": sums[1] / edge_count,
        "M3_empirical": sums[2] / edge_count,
        "L_log_age_empirical": sums[3] / edge_count,
        "fallback_count": fallback_count,
    }


def run():
    theory = theoretical_moments()
    normalization_gate = abs(theory["M0"] - 1.0) <= 1e-9
    rows = []

    for seed in SEEDS:
        row = simulate(N, seed)
        errors = {
            "M1": row["M1_empirical"] - theory["M1"],
            "M2": row["M2_empirical"] - theory["M2"],
            "M3": row["M3_empirical"] - theory["M3"],
            "L_log_age": row["L_log_age_empirical"] - theory["L_log_age"],
        }
        row["errors"] = errors
        row["moment_gate"] = all(
            abs(errors[key]) <= 0.002 for key in ("M1", "M2", "M3")
        )
        row["log_age_gate"] = abs(errors["L_log_age"]) <= 0.003
        rows.append(row)

    moment_gate = all(row["moment_gate"] for row in rows)
    log_gate = all(row["log_age_gate"] for row in rows)

    return {
        "protocol": "T62 frozen",
        "status": "MATHEMATICAL_CAUSAL_ORDER_TEST",
        "theory": theory,
        "uniform_recursive_tree_comparator": {
            "M1": 0.5,
            "M2": 1.0 / 3.0,
            "M3": 0.25,
            "L_log_age": 1.0,
        },
        "heldout": rows,
        "T62_NORMALIZATION": normalization_gate,
        "T62_MOMENT_LAW": moment_gate,
        "T62_LOG_AGE": log_gate,
        "T62_OVERALL": bool(normalization_gate and moment_gate and log_gate),
        "physical_time": "NOT_DERIVED",
        "new_physics": "NOT_ESTABLISHED",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))
    if not result["T62_OVERALL"]:
        raise SystemExit(1)
