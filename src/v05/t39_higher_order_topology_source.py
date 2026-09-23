"""T39 higher-order topology source audit.

Reuses the exact T38 degree-matched tree null ensemble and tests eight
preregistered coordinate-free topology diagnostics against the joint M3/M7
high-radius departure. No dynamics or physical geometry.
"""
from __future__ import annotations
import heapq
import json
import math
import random
from collections import deque

import numpy as np

from t25_endogenous_dimension_scan import generate
from t38_degree_matched_tree_null import (
    decode_degree_matched_prufer,
    degree_sequence,
)


H_NAMES = (
    "H1_diameter",
    "H2_mean_pairwise_distance",
    "H3_mean_eccentricity",
    "H4_degree_assortativity",
    "H5_mean_branch_segment_length",
    "H6_max_branch_segment_length",
    "H7_max_normalized_betweenness",
    "H8_betweenness_gini",
)


def bfs_dist(adj, root):
    d = [-1] * len(adj)
    d[root] = 0
    q = deque([root])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if d[v] < 0:
                d[v] = d[u] + 1
                q.append(v)
    return d


def rooted_tree_data(adj, root=0):
    n = len(adj)
    parent = [-1] * n
    order = [root]
    for u in order:
        for v in adj[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            order.append(v)

    subtree = [1] * n
    for u in reversed(order[1:]):
        subtree[parent[u]] += subtree[u]
    return parent, order, subtree


def tree_distance_summaries(adj):
    n = len(adj)
    d0 = bfs_dist(adj, 0)
    a = int(np.argmax(d0))
    da = bfs_dist(adj, a)
    b = int(np.argmax(da))
    db = bfs_dist(adj, b)

    diameter = max(da)
    mean_ecc = float(np.mean([max(x, y) for x, y in zip(da, db)]))

    parent, _, subtree = rooted_tree_data(adj, 0)
    pair_sum = 0
    for v in range(1, n):
        s = subtree[v]
        pair_sum += s * (n - s)
    mean_pair = pair_sum / (n * (n - 1) / 2)

    return float(diameter), float(mean_pair), mean_ecc, parent, subtree


def assortativity(adj):
    x = []
    y = []
    degrees = degree_sequence(adj)
    for u in range(len(adj)):
        for v in adj[u]:
            x.append(degrees[u])
            y.append(degrees[v])
    ax = np.asarray(x, dtype=float)
    ay = np.asarray(y, dtype=float)
    sx = float(ax.std())
    sy = float(ay.std())
    if sx == 0.0 or sy == 0.0:
        return 0.0
    return float(np.corrcoef(ax, ay)[0, 1])


def branch_segments(adj):
    degrees = degree_sequence(adj)
    endpoints = [v for v, d in enumerate(degrees) if d != 2]
    visited = set()
    lengths = []

    for start in endpoints:
        for nxt in adj[start]:
            edge = tuple(sorted((start, nxt)))
            if edge in visited:
                continue
            visited.add(edge)
            length = 1
            prev, cur = start, nxt

            while degrees[cur] == 2:
                a, b = tuple(adj[cur])
                nxt2 = b if a == prev else a
                edge2 = tuple(sorted((cur, nxt2)))
                visited.add(edge2)
                prev, cur = cur, nxt2
                length += 1

            lengths.append(length)

    if not lengths:
        return 0.0, 0.0
    return float(np.mean(lengths)), float(max(lengths))


def normalized_betweenness(adj, parent, subtree):
    n = len(adj)
    denom = (n - 1) * (n - 2) / 2
    if denom <= 0:
        return np.zeros(n, dtype=float)

    values = []
    for v in range(n):
        comps = []
        for w in adj[v]:
            if parent[w] == v:
                comps.append(subtree[w])
            elif parent[v] == w:
                comps.append(n - subtree[v])
            else:
                raise RuntimeError("tree parent relation inconsistent")

        total = 0
        prefix = 0
        for s in comps:
            total += prefix * s
            prefix += s
        values.append(total / denom)

    return np.asarray(values, dtype=float)


def gini(values):
    a = np.asarray(values, dtype=float)
    if len(a) == 0 or np.all(a == 0):
        return 0.0
    a = np.sort(a)
    n = len(a)
    return float(
        (2.0 * np.dot(np.arange(1, n + 1), a) / (n * a.sum()))
        - (n + 1) / n
    )


def topology_vector(adj):
    diameter, mean_pair, mean_ecc, parent, subtree = tree_distance_summaries(adj)
    mean_branch, max_branch = branch_segments(adj)
    b = normalized_betweenness(adj, parent, subtree)
    return np.asarray(
        [
            diameter,
            mean_pair,
            mean_ecc,
            assortativity(adj),
            mean_branch,
            max_branch,
            float(b.max()),
            gini(b),
        ],
        dtype=float,
    )


def balls_to_radius_8(adj):
    n = len(adj)
    balls = {4: [None] * n, 8: [None] * n}
    for root in range(n):
        dist = {root: 0}
        q = deque([root])
        while q:
            u = q.popleft()
            if dist[u] >= 8:
                continue
            for v in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)
        balls[4][root] = {u for u, d in dist.items() if d <= 4}
        balls[8][root] = set(dist)
    return balls


def m3_m7(adj):
    n = len(adj)
    balls = balls_to_radius_8(adj)

    nu4 = [
        1.0 - len(balls[4][v]) / len(balls[8][v])
        for v in range(n)
    ]
    m3 = float(np.median(nu4))

    contrasts = []
    for u in range(n):
        for v in adj[u]:
            if u < v:
                a = balls[8][u]
                b = balls[8][v]
                contrasts.append(1.0 - len(a & b) / len(a | b))
    m7 = float(np.mean(contrasts))
    return m3, m7


def rank_average(a):
    a = np.asarray(a, dtype=float)
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), dtype=float)
    i = 0
    while i < len(a):
        j = i + 1
        while j < len(a) and a[order[j]] == a[order[i]]:
            j += 1
        rank = (i + 1 + j) / 2.0
        ranks[order[i:j]] = rank
        i = j
    return ranks


def spearman(x, y):
    rx = rank_average(x)
    ry = rank_average(y)
    if rx.std() == 0.0 or ry.std() == 0.0:
        return 0.0
    return float(np.corrcoef(rx, ry)[0, 1])


def compare_parent(n, parent_seed):
    parent = generate(n, parent_seed)
    degrees = degree_sequence(parent)
    parent_h = topology_vector(parent)
    parent_m3, parent_m7 = m3_m7(parent)

    null_h = []
    null_m3 = []
    null_m7 = []

    for replicate in range(99):
        null_seed = 1000003 * n + 1009 * parent_seed + replicate
        null = decode_degree_matched_prufer(degrees, null_seed)
        null_h.append(topology_vector(null))
        m3, m7 = m3_m7(null)
        null_m3.append(m3)
        null_m7.append(m7)

    H = np.vstack(null_h)
    m3s = np.asarray(null_m3)
    m7s = np.asarray(null_m7)

    z3 = (m3s - m3s.mean()) / m3s.std()
    z7 = (m7s - m7s.mean()) / m7s.std()
    joint = (z3 + z7) / 2.0

    rows = []
    for j, name in enumerate(H_NAMES):
        vals = H[:, j]
        q025, q50, q975 = np.quantile(vals, [0.025, 0.50, 0.975])
        pval = float(parent_h[j])
        direction = (
            "low" if pval < q025
            else "high" if pval > q975
            else "inside"
        )
        rows.append(
            {
                "metric": name,
                "parent": pval,
                "null_mean": float(vals.mean()),
                "null_std": float(vals.std()),
                "q025": float(q025),
                "null_median": float(q50),
                "q975": float(q975),
                "parent_percentile": float(np.mean(vals <= pval)),
                "parent_extreme_direction": direction,
                "rho_M3": spearman(vals, m3s),
                "rho_M7": spearman(vals, m7s),
                "rho_Z37": spearman(vals, joint),
            }
        )

    return {
        "n": n,
        "parent_seed": parent_seed,
        "parent_M3": parent_m3,
        "parent_M7": parent_m7,
        "rows": rows,
    }


def gate(parents):
    out = {}
    for name in H_NAMES:
        rows = [
            next(row for row in p["rows"] if row["metric"] == name)
            for p in parents
        ]
        dirs = [r["parent_extreme_direction"] for r in rows]
        if all(d == "high" for d in dirs):
            extreme_direction = "high"
        elif all(d == "low" for d in dirs):
            extreme_direction = "low"
        else:
            extreme_direction = None

        rhos_joint = [r["rho_Z37"] for r in rows]
        nonzero = [x for x in rhos_joint if x != 0.0]
        same_sign_joint = (
            len(nonzero) == 9
            and (all(x > 0 for x in nonzero) or all(x < 0 for x in nonzero))
        )
        if same_sign_joint:
            sign = 1 if rhos_joint[0] > 0 else -1
        else:
            sign = 0

        median_abs = float(np.median(np.abs(rhos_joint)))
        m3_match = sum(
            1 for r in rows if sign and np.sign(r["rho_M3"]) == sign
        )
        m7_match = sum(
            1 for r in rows if sign and np.sign(r["rho_M7"]) == sign
        )

        passed = (
            extreme_direction is not None
            and same_sign_joint
            and median_abs >= 0.50
            and m3_match >= 8
            and m7_match >= 8
        )

        out[name] = {
            "parent_extreme_direction_all9": extreme_direction,
            "rho_Z37_same_nonzero_sign_all9": same_sign_joint,
            "median_abs_rho_Z37": median_abs,
            "rho_M3_sign_matches": m3_match,
            "rho_M7_sign_matches": m7_match,
            "passes": passed,
        }
    return out


def run():
    parents = [
        compare_parent(n, seed)
        for n in (128, 256, 512)
        for seed in (11, 23, 47)
    ]
    gates = gate(parents)
    return {
        "protocol": "T39 frozen",
        "parents": parents,
        "gates": gates,
        "passing_candidates": [
            name for name, result in gates.items() if result["passes"]
        ],
        "guard": (
            "No posthoc topology metric, multivariate model selection, target "
            "dimension, graph evolution, transition law, or physical geometry."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
