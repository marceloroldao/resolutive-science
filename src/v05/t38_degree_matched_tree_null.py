"""T38 degree-matched tree null specificity audit.

Builds 99 degree-sequence-matched labeled-tree nulls per frozen T25 parent
using randomized Prüfer multisets. No dynamics or physical geometry.
"""
from __future__ import annotations
import heapq
import json
import random
from collections import deque

import numpy as np

from t25_endogenous_dimension_scan import generate


METRICS = (
    "median_nu_1_2",
    "median_nu_2_4",
    "median_nu_4_8",
    "mean_DJ_R1",
    "mean_DJ_R2",
    "mean_DJ_R4",
    "mean_DJ_R8",
)


def degree_sequence(adj):
    return [len(neighbors) for neighbors in adj]


def decode_degree_matched_prufer(degrees, seed):
    seq = []
    for label, degree in enumerate(degrees):
        seq.extend([label] * (degree - 1))

    rng = random.Random(seed)
    rng.shuffle(seq)

    remaining = [degree - 1 for degree in degrees]
    leaves = [i for i, count in enumerate(remaining) if count == 0]
    heapq.heapify(leaves)

    adj = [set() for _ in degrees]

    for label in seq:
        leaf = heapq.heappop(leaves)
        adj[leaf].add(label)
        adj[label].add(leaf)
        remaining[label] -= 1
        if remaining[label] == 0:
            heapq.heappush(leaves, label)

    a = heapq.heappop(leaves)
    b = heapq.heappop(leaves)
    adj[a].add(b)
    adj[b].add(a)
    return adj


def is_connected_tree(adj):
    n = len(adj)
    if sum(map(len, adj)) // 2 != n - 1:
        return False

    seen = {0}
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    return len(seen) == n


def balls_to_radius_8(adj):
    n = len(adj)
    radii = (1, 2, 4, 8)
    balls = {r: [None] * n for r in radii}

    for root in range(n):
        dist = {root: 0}
        queue = deque([root])
        while queue:
            u = queue.popleft()
            if dist[u] >= 8:
                continue
            for v in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    queue.append(v)

        for radius in radii:
            balls[radius][root] = {
                node for node, d in dist.items() if d <= radius
            }
    return balls


def t37_summary_vector(adj):
    n = len(adj)
    balls = balls_to_radius_8(adj)
    out = []

    for radius in (1, 2, 4):
        nu = [
            1.0 - len(balls[radius][v]) / len(balls[2 * radius][v])
            for v in range(n)
        ]
        out.append(float(np.median(nu)))

    edges = [(u, v) for u in range(n) for v in adj[u] if u < v]

    for radius in (1, 2, 4, 8):
        contrast = []
        for u, v in edges:
            a = balls[radius][u]
            b = balls[radius][v]
            contrast.append(1.0 - len(a & b) / len(a | b))
        out.append(float(np.mean(contrast)))

    return np.asarray(out, dtype=float)


def compare_parent(n, parent_seed):
    parent = generate(n, parent_seed)
    degrees = degree_sequence(parent)
    parent_metrics = t37_summary_vector(parent)

    null_vectors = []
    controls_pass = True

    for replicate in range(99):
        null_seed = 1000003 * n + 1009 * parent_seed + replicate
        null = decode_degree_matched_prufer(degrees, null_seed)

        controls_pass = controls_pass and degree_sequence(null) == degrees
        controls_pass = controls_pass and is_connected_tree(null)

        null_vectors.append(t37_summary_vector(null))

    matrix = np.vstack(null_vectors)
    comparisons = []

    for j, metric in enumerate(METRICS):
        values = matrix[:, j]
        q025, q50, q975 = np.quantile(values, [0.025, 0.50, 0.975])
        parent_value = float(parent_metrics[j])

        if parent_value < q025:
            direction = "low"
        elif parent_value > q975:
            direction = "high"
        else:
            direction = "inside"

        comparisons.append(
            {
                "metric": metric,
                "parent": parent_value,
                "null_mean": float(values.mean()),
                "null_std": float(values.std()),
                "q025": float(q025),
                "null_median": float(q50),
                "q975": float(q975),
                "parent_percentile": float(np.mean(values <= parent_value)),
                "extreme_direction": direction,
            }
        )

    return {
        "n": n,
        "parent_seed": parent_seed,
        "controls_pass": controls_pass,
        "comparisons": comparisons,
    }


def run():
    parents = [
        compare_parent(n, seed)
        for n in (128, 256, 512)
        for seed in (11, 23, 47)
    ]

    stable = {}
    for metric in METRICS:
        directions = [
            next(
                row["extreme_direction"]
                for row in parent["comparisons"]
                if row["metric"] == metric
            )
            for parent in parents
        ]
        stable[metric] = (
            "high" if all(d == "high" for d in directions)
            else "low" if all(d == "low" for d in directions)
            else None
        )

    return {
        "protocol": "T38 frozen",
        "nulls_per_parent": 99,
        "parents": parents,
        "degree_sequence_control": all(p["controls_pass"] for p in parents),
        "stable_same_direction_extremes": stable,
        "guard": (
            "No target dimension, profile metric, graph evolution, transition law, "
            "target-domain fitting, or physical-geometry claim."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
