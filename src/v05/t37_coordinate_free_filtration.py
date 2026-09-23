"""T37 coordinate-free neighborhood filtration audit.

Uses only graph-distance neighborhood sets and set cardinalities/intersections.
No profile coordinates, Euclidean profile metric, dynamics, or physical dimension.
"""
from __future__ import annotations
import json
from collections import defaultdict
import numpy as np

from t25_endogenous_dimension_scan import generate, distances


def summarize(values):
    a = np.asarray(values, dtype=float)
    if len(a) == 0:
        return {"count": 0}
    q = np.quantile(a, [0.05, 0.25, 0.50, 0.75, 0.95])
    return {
        "count": int(len(a)),
        "mean": float(a.mean()),
        "std": float(a.std()),
        "min": float(a.min()),
        "q05": float(q[0]),
        "q25": float(q[1]),
        "median": float(q[2]),
        "q75": float(q[3]),
        "q95": float(q[4]),
        "max": float(a.max()),
    }


def neighborhoods(ds, radius):
    return [
        {u for u, distance in enumerate(row) if 0 <= distance <= radius}
        for row in ds
    ]


def run_graph(n, seed):
    adj = generate(n, seed)
    ds = [distances(adj, u) for u in range(n)]
    balls = {r: neighborhoods(ds, r) for r in (1, 2, 4, 8)}

    scale_rows = []
    nesting_pass = True

    for radius in (1, 2, 4):
        rows = []
        by_degree = defaultdict(list)
        for v in range(n):
            low = balls[radius][v]
            high = balls[2 * radius][v]
            nesting_pass = nesting_pass and low.issubset(high)

            nu = len(high - low) / len(high)
            xi = len(high) / len(low)
            sigma = len(low) / n

            row = {
                "degree": len(adj[v]),
                "nu": float(nu),
                "xi": float(xi),
                "sigma": float(sigma),
            }
            rows.append(row)
            by_degree[row["degree"]].append(row)

        scale_rows.append(
            {
                "transition": f"{radius}->{2 * radius}",
                "nu": summarize([x["nu"] for x in rows]),
                "xi": summarize([x["xi"] for x in rows]),
                "sigma_R": summarize([x["sigma"] for x in rows]),
                "degree_conditioned": {
                    str(degree): {
                        "count": len(group),
                        "nu": summarize([x["nu"] for x in group]),
                        "xi": summarize([x["xi"] for x in group]),
                    }
                    for degree, group in sorted(by_degree.items())
                },
            }
        )

    edges = [(u, v) for u in range(n) for v in adj[u] if u < v]
    edge_rows = []
    for radius in (1, 2, 4, 8):
        rows = []
        by_degree_pair = defaultdict(list)
        for u, v in edges:
            a = balls[radius][u]
            b = balls[radius][v]
            union = a | b
            jaccard = len(a & b) / len(union) if union else 1.0
            contrast = 1.0 - jaccard
            pair = tuple(sorted((len(adj[u]), len(adj[v]))))
            rows.append(float(contrast))
            by_degree_pair[pair].append(float(contrast))

        edge_rows.append(
            {
                "R": radius,
                "jaccard_contrast": summarize(rows),
                "degree_pair_conditioned": {
                    f"{a}-{b}": summarize(values)
                    for (a, b), values in sorted(by_degree_pair.items())
                },
            }
        )

    return {
        "n": n,
        "seed": seed,
        "nesting_pass": nesting_pass,
        "scale_extension": scale_rows,
        "edge_contrast": edge_rows,
    }


def run():
    return {
        "protocol": "T37 frozen",
        "runs": [
            run_graph(n, seed)
            for n in (128, 256, 512)
            for seed in (11, 23, 47)
        ],
        "guard": (
            "No profile coordinates, Euclidean profile metric, target dimension, "
            "physical distance, graph evolution, transition law, or dynamics."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
