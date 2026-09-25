"""T48 same-candidate selection-operator counterfactual.

Records the exact T25 candidate/tie schedule, proves edge-exact MIN replay,
then replaces only the parent-selection operator with RANDOM-AVAILABLE.
"""
from __future__ import annotations
import json
import random
import numpy as np

from t25_endogenous_dimension_scan import generate
from t38_degree_matched_tree_null import is_connected_tree
from t39_higher_order_topology_source import m3_m7
from t41_higher_order_matched_tree_null import summarize, summarize_heldout, edge_set
from t47_degree_preserving_recursive_order_null import recursive_order_control


MAX_DEGREE = 6
SAMPLE_SIZE = 5


def edge(adj, a, b):
    if (
        a != b
        and len(adj[a]) < MAX_DEGREE
        and len(adj[b]) < MAX_DEGREE
    ):
        adj[a].add(b)
        adj[b].add(a)
        return True
    return False


def record_baseline_trace(n, seed):
    rng = random.Random(seed)
    adj = [set() for _ in range(n)]
    edge(adj, 0, 1)

    trace = []

    for v in range(2, n):
        candidates = rng.sample(range(v), min(SAMPLE_SIZE, v))
        tie_values = [rng.random() for _ in candidates]

        ordered = sorted(
            zip(candidates, tie_values),
            key=lambda item: (len(adj[item[0]]), item[1]),
        )

        chosen = None
        for u, _tie in ordered:
            if edge(adj, v, u):
                chosen = u
                break

        fallback_parent = None
        if chosen is None:
            avail = [u for u in range(v) if len(adj[u]) < MAX_DEGREE]
            if avail:
                fallback_parent = rng.choice(avail)
                if not edge(adj, v, fallback_parent):
                    raise RuntimeError("baseline fallback edge failed")
                chosen = fallback_parent

        if chosen is None:
            raise RuntimeError(f"baseline failed to attach vertex {v}")

        trace.append(
            {
                "v": v,
                "candidates": list(candidates),
                "tie_values": list(tie_values),
                "fallback_parent": fallback_parent,
                "chosen_parent": chosen,
            }
        )

    return adj, trace


def replay_min(n, trace):
    adj = [set() for _ in range(n)]
    edge(adj, 0, 1)

    for row in trace:
        v = row["v"]
        ordered = sorted(
            zip(row["candidates"], row["tie_values"]),
            key=lambda item: (len(adj[item[0]]), item[1]),
        )

        chosen = None
        for u, _tie in ordered:
            if edge(adj, v, u):
                chosen = u
                break

        if chosen is None:
            u = row["fallback_parent"]
            if u is None:
                raise RuntimeError(
                    f"MIN replay needs fallback at v={v}, but trace has none"
                )
            if not edge(adj, v, u):
                raise RuntimeError(f"MIN replay fallback failed at v={v}")
            chosen = u

        if chosen != row["chosen_parent"]:
            raise RuntimeError(
                f"MIN replay parent mismatch at v={v}: "
                f"{chosen} != {row['chosen_parent']}"
            )

    return adj


def random_available_counterfactual(n, parent_seed, replicate, trace):
    rng = random.Random(
        17000023 * n + 65537 * parent_seed + 1009 * replicate
    )
    adj = [set() for _ in range(n)]
    edge(adj, 0, 1)

    for row in trace:
        v = row["v"]
        available = [
            u for u in row["candidates"]
            if len(adj[u]) < MAX_DEGREE
        ]

        if available:
            u = rng.choice(available)
        else:
            avail_all = [
                u for u in range(v)
                if len(adj[u]) < MAX_DEGREE
            ]
            if not avail_all:
                raise RuntimeError(
                    f"counterfactual has no available parent at v={v}"
                )
            u = rng.choice(avail_all)

        if not edge(adj, v, u):
            raise RuntimeError(
                f"counterfactual edge failed at v={v}, parent={u}"
            )

    return adj


def degree_histogram(adj):
    n = len(adj)
    return np.asarray(
        [
            sum(1 for ns in adj if len(ns) == d) / n
            for d in range(1, MAX_DEGREE + 1)
        ],
        dtype=float,
    )


def run_parent(n, seed):
    frozen = generate(n, seed)
    traced, trace = record_baseline_trace(n, seed)
    replay = replay_min(n, trace)

    frozen_edges = edge_set(frozen)
    trace_edges = edge_set(traced)
    replay_edges = edge_set(replay)

    trace_matches_generate = trace_edges == frozen_edges
    replay_matches_generate = replay_edges == frozen_edges

    result = {
        "n": n,
        "parent_seed": seed,
        "trace_matches_generate": trace_matches_generate,
        "replay_matches_generate": replay_matches_generate,
        "baseline_edges": len(frozen_edges),
        "trace_rows": len(trace),
    }

    if not (trace_matches_generate and replay_matches_generate):
        return result

    min_m3, min_m7 = m3_m7(replay)
    min_hist = degree_histogram(replay)

    random_m3 = []
    random_m7 = []
    tv_deg = []
    controls = True

    for replicate in range(99):
        adj = random_available_counterfactual(
            n, seed, replicate, trace
        )

        controls = controls and is_connected_tree(adj)
        controls = controls and max(map(len, adj)) <= MAX_DEGREE
        controls = controls and recursive_order_control(adj)
        controls = controls and (sum(map(len, adj)) // 2 == n - 1)

        m3, m7 = m3_m7(adj)
        random_m3.append(m3)
        random_m7.append(m7)

        hist = degree_histogram(adj)
        tv_deg.append(float(0.5 * np.abs(hist - min_hist).sum()))

    result["counterfactual_control"] = bool(controls)
    result["MIN_M3"] = float(min_m3)
    result["MIN_M7"] = float(min_m7)
    result["RANDOM_M3"] = summarize_heldout(min_m3, random_m3)
    result["RANDOM_M7"] = summarize_heldout(min_m7, random_m7)
    result["MIN_degree_histogram_d1_to_d6"] = [
        float(x) for x in min_hist
    ]
    result["degree_histogram_TV"] = summarize(tv_deg)

    return result


def run():
    rows = [run_parent(2048, seed) for seed in (577, 607, 641)]

    replay_pass = all(
        row.get("trace_matches_generate", False)
        and row.get("replay_matches_generate", False)
        for row in rows
    )

    counterfactual_control = all(
        row.get("counterfactual_control", False)
        for row in rows
    )

    regulatory = bool(
        replay_pass
        and counterfactual_control
        and all(
            row["RANDOM_M3"]["classification"] == "low"
            and row["RANDOM_M7"]["classification"] == "low"
            for row in rows
        )
    )

    return {
        "protocol": "T48 frozen",
        "N": 2048,
        "seeds": [577, 607, 641],
        "rows": rows,
        "trace_replay": replay_pass,
        "counterfactual_control": counterfactual_control,
        "selection_regulatory_direction": regulatory,
        "guard": (
            "Exact baseline candidate sets and birth order; only MIN-DEGREE is "
            "replaced by RANDOM-AVAILABLE; no degree matching, rescue variants, "
            "target fitting, or physical-geometry claim."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
