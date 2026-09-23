"""T41 higher-order matched tree null audit.

Degree-preserving constrained random walk in Prüfer-sequence permutation space.
M3/M7 are held out and never used for proposal acceptance.
"""
from __future__ import annotations
import heapq
import json
import random
import numpy as np

from t25_endogenous_dimension_scan import generate
from t38_degree_matched_tree_null import (
    decode_degree_matched_prufer,
    degree_sequence,
    is_connected_tree,
)
from t39_higher_order_topology_source import topology_vector, m3_m7


def tree_to_prufer(adj):
    n = len(adj)
    work = [set(x) for x in adj]
    degree = [len(x) for x in work]
    leaves = [i for i, d in enumerate(degree) if d == 1]
    heapq.heapify(leaves)
    seq = []
    for _ in range(n - 2):
        leaf = heapq.heappop(leaves)
        neighbor = next(iter(work[leaf]))
        seq.append(neighbor)
        work[leaf].remove(neighbor)
        work[neighbor].remove(leaf)
        degree[leaf] -= 1
        degree[neighbor] -= 1
        if degree[neighbor] == 1:
            heapq.heappush(leaves, neighbor)
    return seq


def edge_set(adj):
    return frozenset((u, v) for u in range(len(adj)) for v in adj[u] if u < v)


def baseline_stats(n, parent_seed, degrees):
    H = []
    for replicate in range(99):
        null_seed = 1000003 * n + 1009 * parent_seed + replicate
        null = decode_degree_matched_prufer(degrees, null_seed)
        H.append(topology_vector(null))
    H = np.vstack(H)
    return H.mean(axis=0), H.std(axis=0)


def cag(h, mean, sd):
    z = (h - mean) / sd
    C = -(z[0] + z[1] + z[2]) / 3.0
    A = z[3]
    G = z[7]
    return np.asarray([C, A, G], dtype=float)


def inside_box(value, target):
    return bool(np.all(np.abs(value - target) <= 0.50))


def run_parent(n, parent_seed):
    parent = generate(n, parent_seed)
    degrees = degree_sequence(parent)
    parent_edges = edge_set(parent)
    parent_seq = tree_to_prufer(parent)

    mean, sd = baseline_stats(n, parent_seed, degrees)
    parent_h = topology_vector(parent)
    target = cag(parent_h, mean, sd)

    current_seq = list(parent_seq)
    current = parent
    current_cag = target.copy()

    rng = random.Random(7000003 * n + 7919 * parent_seed)

    accepted = 0
    proposals = 0
    stored = []
    stored_edges = set()

    while proposals < 250000 and len(stored) < 99:
        proposals += 1
        i, j = rng.sample(range(len(current_seq)), 2)
        proposal_seq = list(current_seq)
        proposal_seq[i], proposal_seq[j] = proposal_seq[j], proposal_seq[i]

        # Swapping identical labels is not a new state.
        if proposal_seq == current_seq:
            continue

        proposal = decode_explicit_prufer(proposal_seq, n)
        proposal_h = topology_vector(proposal)
        proposal_cag = cag(proposal_h, mean, sd)

        if not inside_box(proposal_cag, target):
            continue

        current_seq = proposal_seq
        current = proposal
        current_cag = proposal_cag
        accepted += 1

        if accepted <= 500:
            continue
        if (accepted - 500) % 50 != 0:
            continue

        edges = edge_set(current)
        overlap = len(edges & parent_edges) / (n - 1)
        if overlap > 0.90:
            continue
        if edges in stored_edges:
            continue

        stored_edges.add(edges)
        stored.append(
            {
                "adj": current,
                "CAG": current_cag.copy(),
                "parent_edge_overlap": overlap,
            }
        )

    control_degree = all(degree_sequence(x["adj"]) == degrees for x in stored)
    control_tree = all(is_connected_tree(x["adj"]) for x in stored)
    control_match = all(inside_box(x["CAG"], target) for x in stored)
    control_diversity = (
        all(x["parent_edge_overlap"] <= 0.90 for x in stored)
        and len(stored_edges) == len(stored)
    )

    result = {
        "n": n,
        "parent_seed": parent_seed,
        "target_CAG": [float(x) for x in target],
        "proposals": proposals,
        "accepted_moves": accepted,
        "stored_nulls": len(stored),
        "match_feasible": len(stored) == 99,
        "degree_control": control_degree,
        "tree_control": control_tree,
        "match_control": control_match,
        "diversity_control": control_diversity,
    }

    if len(stored) == 99:
        parent_m3, parent_m7 = m3_m7(parent)
        m3s = []
        m7s = []
        overlaps = []
        for item in stored:
            m3, m7 = m3_m7(item["adj"])
            m3s.append(m3)
            m7s.append(m7)
            overlaps.append(item["parent_edge_overlap"])

        result["M3"] = summarize_heldout(parent_m3, m3s)
        result["M7"] = summarize_heldout(parent_m7, m7s)
        result["parent_edge_overlap"] = summarize(overlaps)

    return result


def decode_explicit_prufer(seq, n):
    occurrence = [0] * n
    for label in seq:
        occurrence[label] += 1
    leaves = [i for i, count in enumerate(occurrence) if count == 0]
    heapq.heapify(leaves)
    adj = [set() for _ in range(n)]

    for label in seq:
        leaf = heapq.heappop(leaves)
        adj[leaf].add(label)
        adj[label].add(leaf)
        occurrence[label] -= 1
        if occurrence[label] == 0:
            heapq.heappush(leaves, label)

    a = heapq.heappop(leaves)
    b = heapq.heappop(leaves)
    adj[a].add(b)
    adj[b].add(a)
    return adj


def summarize(values):
    a = np.asarray(values, dtype=float)
    q = np.quantile(a, [0.025, 0.50, 0.975])
    return {
        "mean": float(a.mean()),
        "std": float(a.std()),
        "q025": float(q[0]),
        "median": float(q[1]),
        "q975": float(q[2]),
        "min": float(a.min()),
        "max": float(a.max()),
    }


def summarize_heldout(parent_value, values):
    s = summarize(values)
    s["parent"] = float(parent_value)
    s["parent_percentile"] = float(np.mean(np.asarray(values) <= parent_value))
    s["classification"] = (
        "low" if parent_value < s["q025"]
        else "high" if parent_value > s["q975"]
        else "inside"
    )
    return s


def run():
    rows = [
        run_parent(n, seed)
        for n in (128, 256, 512)
        for seed in (11, 23, 47)
    ]
    all_controls = all(
        x["match_feasible"]
        and x["degree_control"]
        and x["tree_control"]
        and x["match_control"]
        and x["diversity_control"]
        for x in rows
    )
    return {
        "protocol": "T41 frozen",
        "rows": rows,
        "all_controls_pass": all_controls,
        "guard": (
            "M3/M7 held out from sampler; no tolerance relaxation, posthoc "
            "predictor addition, graph dynamics, transition law or physical geometry."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
