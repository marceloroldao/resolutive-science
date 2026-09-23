"""T44 held-out branch-core clustering audit.

Reuses the exact T41 matcher logic at N=2048 with new seeds. K and M3/M7
are computed only after matched nulls are stored.
"""
from __future__ import annotations
import json
import random
import numpy as np

from t25_endogenous_dimension_scan import generate
from t38_degree_matched_tree_null import degree_sequence, is_connected_tree
from t39_higher_order_topology_source import topology_vector, m3_m7, spearman
from t41_higher_order_matched_tree_null import (
    tree_to_prufer,
    edge_set,
    baseline_stats,
    cag,
    inside_box,
    decode_explicit_prufer,
    summarize,
    summarize_heldout,
)


def branch_core_fraction(adj):
    branch = {v for v in range(len(adj)) if len(adj[v]) >= 3}
    if not branch:
        return 0.0

    seen = set()
    largest = 0

    for root in branch:
        if root in seen:
            continue
        stack = [root]
        seen.add(root)
        size = 0
        while stack:
            u = stack.pop()
            size += 1
            for v in adj[u]:
                if v in branch and v not in seen:
                    seen.add(v)
                    stack.append(v)
        largest = max(largest, size)

    return largest / len(branch)


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

    degree_control = all(degree_sequence(x["adj"]) == degrees for x in stored)
    tree_control = all(is_connected_tree(x["adj"]) for x in stored)
    match_control = all(inside_box(x["CAG"], target) for x in stored)
    diversity_control = (
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
        "degree_control": degree_control,
        "tree_control": tree_control,
        "match_control": match_control,
        "diversity_control": diversity_control,
    }

    if len(stored) != 99:
        return result

    parent_m3, parent_m7 = m3_m7(parent)
    parent_k = branch_core_fraction(parent)

    null_m3 = []
    null_m7 = []
    null_k = []
    overlaps = []

    for item in stored:
        m3, m7 = m3_m7(item["adj"])
        k = branch_core_fraction(item["adj"])
        null_m3.append(m3)
        null_m7.append(m7)
        null_k.append(k)
        overlaps.append(item["parent_edge_overlap"])

    result["M3"] = summarize_heldout(parent_m3, null_m3)
    result["M7"] = summarize_heldout(parent_m7, null_m7)
    result["K"] = summarize_heldout(parent_k, null_k)
    result["rho_K_M3"] = spearman(null_k, null_m3)
    result["rho_K_M7"] = spearman(null_k, null_m7)
    result["parent_edge_overlap"] = summarize(overlaps)
    return result


def run():
    rows = [run_parent(2048, seed) for seed in (211, 239, 269)]

    controls = all(
        row["match_feasible"]
        and row["degree_control"]
        and row["tree_control"]
        and row["match_control"]
        and row["diversity_control"]
        for row in rows
    )

    residual_replication = bool(
        controls
        and all(
            row.get("M3", {}).get("classification") == "high"
            and row.get("M7", {}).get("classification") == "high"
            for row in rows
        )
    )

    parent_departure = bool(
        controls
        and all(row.get("K", {}).get("classification") == "high" for row in rows)
    )

    if controls:
        mins = [min(row["rho_K_M3"], row["rho_K_M7"]) for row in rows]
        association = bool(
            all(row["rho_K_M3"] > 0 and row["rho_K_M7"] > 0 for row in rows)
            and float(np.median(mins)) >= 0.50
        )
        median_min_rho = float(np.median(mins))
    else:
        association = False
        median_min_rho = None

    candidate = bool(
        controls and residual_replication and parent_departure and association
    )

    return {
        "protocol": "T44 frozen",
        "N": 2048,
        "seeds": [211, 239, 269],
        "rows": rows,
        "match_feasibility": controls,
        "residual_replication": residual_replication,
        "branch_core_parent_departure": parent_departure,
        "branch_core_response_association": association,
        "median_min_rho": median_min_rho,
        "branch_core_candidate": candidate,
        "guard": (
            "Exact T41 matcher; K/M3/M7 excluded from sampler; no rescue seeds, "
            "new clustering metrics, graph dynamics, transition law, or physical geometry."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
