"""T35 canonical scale transport audit.

Physics diagnostic only. No target dimension, fitted alignment, graph evolution,
or transition law.
"""
from __future__ import annotations
import json
from collections import defaultdict
import numpy as np

from t25_endogenous_dimension_scan import generate, distances
from t30_relational_compatibility import profile_from_dist


def profiles(adj, radius):
    n = len(adj)
    ds = [distances(adj, u) for u in range(n)]
    return [profile_from_dist(ds[u], radius, n) for u in range(n)]


def edge_displacements(adj, ps, v):
    return np.asarray([ps[w] - ps[v] for w in adj[v]], dtype=float)


def row_basis(x):
    if x.size == 0:
        return np.empty((0, x.shape[1] if x.ndim == 2 else 0))
    _, _, vh = np.linalg.svd(x, full_matrices=False)
    rank = int(np.linalg.matrix_rank(x))
    return vh[:rank]


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


def audit_transition(adj, p_low, p_high, radius):
    rows = []
    for v in range(len(adj)):
        x_low = edge_displacements(adj, p_low, v)
        x_high = edge_displacements(adj, p_high, v)

        # Canonical inclusion R^(R+1) -> R^(2R+1), no fitted alignment.
        x_up = np.pad(x_low, ((0, 0), (0, radius)), mode="constant")

        q_low = row_basis(x_up)
        q_high = row_basis(x_high)

        if len(q_low) and len(q_high):
            sv = np.linalg.svd(q_low @ q_high.T, compute_uv=False)
            common_rank = min(len(q_low), len(q_high))
            mean_cos = float(np.mean(sv[:common_rank]))
            min_cos = float(np.min(sv[:common_rank]))
        else:
            common_rank = 0
            mean_cos = None
            min_cos = None

        outer = x_high[:, radius + 1 :]
        power = float(np.sum(x_high * x_high))
        eta_outer = (
            float(np.sum(outer * outer) / power) if power > 0.0 else None
        )

        if power > 0.0 and len(q_low):
            projection = x_high @ q_low.T @ q_low
            residual = float(
                np.linalg.norm(x_high - projection, "fro")
                / np.linalg.norm(x_high, "fro")
            )
        elif power > 0.0:
            residual = 1.0
        else:
            residual = None

        rows.append(
            {
                "degree": len(adj[v]),
                "rank_low": int(np.linalg.matrix_rank(x_low)),
                "rank_high": int(np.linalg.matrix_rank(x_high)),
                "common_rank": common_rank,
                "mean_principal_cosine": mean_cos,
                "min_principal_cosine": min_cos,
                "eta_outer": eta_outer,
                "projection_residual": residual,
            }
        )
    return rows


def pack(rows):
    def vals(key):
        return [r[key] for r in rows if r[key] is not None]

    by_degree = defaultdict(list)
    for row in rows:
        by_degree[row["degree"]].append(row)

    return {
        "mean_principal_cosine": summarize(vals("mean_principal_cosine")),
        "min_principal_cosine": summarize(vals("min_principal_cosine")),
        "eta_outer": summarize(vals("eta_outer")),
        "projection_residual": summarize(vals("projection_residual")),
        "degree_conditioned": {
            str(degree): {
                "count": len(group),
                "mean_principal_cosine": summarize(
                    [r["mean_principal_cosine"] for r in group
                     if r["mean_principal_cosine"] is not None]
                ),
                "eta_outer": summarize(
                    [r["eta_outer"] for r in group if r["eta_outer"] is not None]
                ),
                "projection_residual": summarize(
                    [r["projection_residual"] for r in group
                     if r["projection_residual"] is not None]
                ),
            }
            for degree, group in sorted(by_degree.items())
        },
    }


def run():
    runs = []
    for n in (128, 256, 512):
        for seed in (11, 23, 47):
            adj = generate(n, seed)
            profile_cache = {r: profiles(adj, r) for r in (1, 2, 4, 8)}
            for radius in (1, 2, 4):
                rows = audit_transition(
                    adj,
                    profile_cache[radius],
                    profile_cache[2 * radius],
                    radius,
                )
                runs.append(
                    {
                        "n": n,
                        "seed": seed,
                        "transition": f"{radius}->{2 * radius}",
                        "summary": pack(rows),
                    }
                )

    return {
        "protocol": "T35 frozen",
        "embedding": "canonical_zero_padding",
        "runs": runs,
        "guard": (
            "No target dimension, fitted alignment, selected cosine/residual "
            "threshold, graph evolution, transition law, or physical tangent-space claim."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
