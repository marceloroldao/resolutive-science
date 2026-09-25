"""T47 degree-preserving recursive-order null audit.

Randomizes the T25 parent assignment while preserving:
- exact labeled degree sequence via fixed child quotas;
- recursive birth order parent(v) < v;
- connected rooted-tree class.

M3/M7 are held out until the 99 nulls are frozen.
"""
from __future__ import annotations
import json
import random
import numpy as np

from t25_endogenous_dimension_scan import generate
from t38_degree_matched_tree_null import degree_sequence, is_connected_tree
from t39_higher_order_topology_source import m3_m7
from t41_higher_order_matched_tree_null import edge_set, summarize_heldout, summarize


def extract_parent(adj):
    n = len(adj)
    parent = [-1] * n

    for v in range(1, n):
        older = [u for u in adj[v] if u < v]
        if len(older) != 1:
            raise ValueError(
                f"vertex {v} has {len(older)} older neighbors; expected exactly 1"
            )
        parent[v] = older[0]

    return parent


def build_adj(parent):
    n = len(parent)
    adj = [set() for _ in range(n)]
    for v in range(1, n):
        u = parent[v]
        if not (0 <= u < v):
            raise ValueError(f"invalid recursive parent p[{v}]={u}")
        adj[u].add(v)
        adj[v].add(u)
    return adj


def recursive_order_control(adj):
    return all(
        sum(1 for u in adj[v] if u < v) == 1
        for v in range(1, len(adj))
    )


def sample_recursive_nulls(parent_adj, n, parent_seed):
    original_parent = extract_parent(parent_adj)
    current = list(original_parent)
    parent_edges = edge_set(parent_adj)
    parent_degrees = degree_sequence(parent_adj)

    rng = random.Random(13000019 * n + 13007 * parent_seed)

    accepted = 0
    proposals = 0
    stored = []
    stored_edges = set()

    while proposals < 1_000_000 and len(stored) < 99:
        proposals += 1
        a, b = rng.sample(range(1, n), 2)
        x = current[a]
        y = current[b]

        if x == y:
            continue

        if not (y < a and x < b):
            continue

        current[a], current[b] = y, x
        accepted += 1

        if accepted <= 2000:
            continue
        if (accepted - 2000) % 200 != 0:
            continue

        adj = build_adj(current)
        edges = edge_set(adj)
        overlap = len(edges & parent_edges) / (n - 1)

        if overlap > 0.90:
            continue
        if edges in stored_edges:
            continue

        stored_edges.add(edges)
        stored.append(
            {
                "adj": adj,
                "parent": list(current),
                "parent_edge_overlap": overlap,
            }
        )

    degree_control = all(
        degree_sequence(item["adj"]) == parent_degrees for item in stored
    )
    recursive_control = all(
        recursive_order_control(item["adj"]) for item in stored
    )
    tree_control = all(is_connected_tree(item["adj"]) for item in stored)
    diversity_control = (
        len(stored_edges) == len(stored)
        and all(item["parent_edge_overlap"] <= 0.90 for item in stored)
    )

    return {
        "stored": stored,
        "proposals": proposals,
        "accepted_swaps": accepted,
        "feasible": len(stored) == 99,
        "degree_control": degree_control,
        "recursive_order_control": recursive_control,
        "tree_control": tree_control,
        "diversity_control": diversity_control,
    }


def run_parent(n, parent_seed):
    parent_adj = generate(n, parent_seed)

    try:
        parent = extract_parent(parent_adj)
        parent_recursive = True
    except ValueError:
        parent = None
        parent_recursive = False

    result = {
        "n": n,
        "parent_seed": parent_seed,
        "parent_recursive_order": parent_recursive,
    }

    if not parent_recursive:
        return result

    child_quota = [0] * n
    for v in range(1, n):
        child_quota[parent[v]] += 1

    result["child_quota_degree_identity"] = all(
        len(parent_adj[v]) == (
            child_quota[v] if v == 0 else child_quota[v] + 1
        )
        for v in range(n)
    )

    sample = sample_recursive_nulls(parent_adj, n, parent_seed)
    result.update(
        {
            "proposals": sample["proposals"],
            "accepted_swaps": sample["accepted_swaps"],
            "stored_nulls": len(sample["stored"]),
            "null_feasible": sample["feasible"],
            "degree_control": sample["degree_control"],
            "recursive_order_control": sample["recursive_order_control"],
            "tree_control": sample["tree_control"],
            "diversity_control": sample["diversity_control"],
        }
    )

    if not (
        sample["feasible"]
        and sample["degree_control"]
        and sample["recursive_order_control"]
        and sample["tree_control"]
        and sample["diversity_control"]
    ):
        return result

    parent_m3, parent_m7 = m3_m7(parent_adj)
    null_m3 = []
    null_m7 = []
    overlaps = []

    for item in sample["stored"]:
        m3, m7 = m3_m7(item["adj"])
        null_m3.append(m3)
        null_m7.append(m7)
        overlaps.append(item["parent_edge_overlap"])

    result["M3"] = summarize_heldout(parent_m3, null_m3)
    result["M7"] = summarize_heldout(parent_m7, null_m7)
    result["parent_edge_overlap"] = summarize(overlaps)

    return result


def run():
    rows = [run_parent(2048, seed) for seed in (479, 509, 547)]

    parent_control = all(
        row.get("parent_recursive_order", False)
        and row.get("child_quota_degree_identity", False)
        for row in rows
    )

    controls = all(
        row.get("null_feasible", False)
        and row.get("degree_control", False)
        and row.get("recursive_order_control", False)
        and row.get("tree_control", False)
        and row.get("diversity_control", False)
        for row in rows
    )

    accounting = bool(
        parent_control
        and controls
        and all(
            row["M3"]["classification"] == "inside"
            and row["M7"]["classification"] == "inside"
            for row in rows
        )
    )

    residual = bool(
        parent_control
        and controls
        and all(
            row["M3"]["classification"] == "high"
            and row["M7"]["classification"] == "high"
            for row in rows
        )
    )

    return {
        "protocol": "T47 frozen",
        "N": 2048,
        "seeds": [479, 509, 547],
        "rows": rows,
        "parent_recursive_order_control": parent_control,
        "recursive_null_feasibility": controls,
        "recursive_order_accounting": accounting,
        "residual_after_recursive_order": residual,
        "guard": (
            "Exact labeled degree + parent(v)<v only; no C/A/G/PB matching, "
            "M3/M7 proposal selection, rescue seeds, graph dynamics, transition law, "
            "or physical geometry."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
