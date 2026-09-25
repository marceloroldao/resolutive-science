"""T49 selection-pressure dose-response audit.

Uses exact T25 candidate traces and paired random schedules across alpha.
Only the probability of applying the MIN-current-degree operator changes.
"""
from __future__ import annotations
import json
import random
import numpy as np

from t25_endogenous_dimension_scan import generate
from t38_degree_matched_tree_null import is_connected_tree
from t39_higher_order_topology_source import m3_m7
from t41_higher_order_matched_tree_null import edge_set, summarize
from t47_degree_preserving_recursive_order_null import recursive_order_control
from t48_same_candidate_selection_operator_counterfactual import (
    MAX_DEGREE,
    edge,
    record_baseline_trace,
    replay_min,
    degree_histogram,
)


ALPHAS = (0.00, 0.25, 0.50, 0.75, 1.00)


def make_schedule(n, parent_seed, replicate, trace):
    rng = random.Random(
        19000069 * n + 131071 * parent_seed + 4099 * replicate
    )
    return [
        (rng.random(), rng.random(), rng.random())
        for _ in trace
    ]


def choose_from_uniform(items, u):
    if not items:
        raise ValueError("cannot choose from empty list")
    idx = min(int(u * len(items)), len(items) - 1)
    return items[idx]


def alpha_counterfactual(n, trace, schedule, alpha):
    if alpha == 1.0:
        return replay_min(n, trace)

    adj = [set() for _ in range(n)]
    edge(adj, 0, 1)

    for row, (u_mode, u_choice, u_fallback) in zip(trace, schedule):
        v = row["v"]
        available = [
            u for u in row["candidates"]
            if len(adj[u]) < MAX_DEGREE
        ]

        if available:
            if u_mode < alpha:
                tie = dict(zip(row["candidates"], row["tie_values"]))
                u = min(
                    available,
                    key=lambda x: (len(adj[x]), tie[x]),
                )
            else:
                u = choose_from_uniform(available, u_choice)
        else:
            avail_all = [
                u for u in range(v)
                if len(adj[u]) < MAX_DEGREE
            ]
            if not avail_all:
                raise RuntimeError(
                    f"no available fallback parent at v={v}"
                )
            u = choose_from_uniform(avail_all, u_fallback)

        if not edge(adj, v, u):
            raise RuntimeError(
                f"edge failed at v={v}, parent={u}, alpha={alpha}"
            )

    return adj


def summarize_values(values):
    a = np.asarray(values, dtype=float)
    q025, q50, q975 = np.quantile(a, [0.025, 0.50, 0.975])
    return {
        "count": int(len(a)),
        "mean": float(a.mean()),
        "std": float(a.std()),
        "q025": float(q025),
        "median": float(q50),
        "q975": float(q975),
        "min": float(a.min()),
        "max": float(a.max()),
    }


def run_parent(n, seed):
    frozen = generate(n, seed)
    traced, trace = record_baseline_trace(n, seed)
    min_adj = replay_min(n, trace)

    frozen_edges = edge_set(frozen)
    replay_edges = edge_set(min_adj)

    replay_pass = (
        edge_set(traced) == frozen_edges
        and replay_edges == frozen_edges
    )

    result = {
        "n": n,
        "parent_seed": seed,
        "trace_replay": replay_pass,
    }
    if not replay_pass:
        return result

    min_m3, min_m7 = m3_m7(min_adj)
    min_hist = degree_histogram(min_adj)

    rows = {}
    controls = True

    for alpha in ALPHAS:
        if alpha == 1.0:
            rows[str(alpha)] = {
                "M3": {
                    "count": 1,
                    "mean": float(min_m3),
                    "std": 0.0,
                    "q025": float(min_m3),
                    "median": float(min_m3),
                    "q975": float(min_m3),
                    "min": float(min_m3),
                    "max": float(min_m3),
                },
                "M7": {
                    "count": 1,
                    "mean": float(min_m7),
                    "std": 0.0,
                    "q025": float(min_m7),
                    "median": float(min_m7),
                    "q975": float(min_m7),
                    "min": float(min_m7),
                    "max": float(min_m7),
                },
                "degree_histogram_TV": {
                    "count": 1,
                    "mean": 0.0,
                    "std": 0.0,
                    "q025": 0.0,
                    "median": 0.0,
                    "q975": 0.0,
                    "min": 0.0,
                    "max": 0.0,
                },
            }
            continue

        m3s = []
        m7s = []
        tvs = []

        for replicate in range(99):
            schedule = make_schedule(n, seed, replicate, trace)
            adj = alpha_counterfactual(n, trace, schedule, alpha)

            controls = controls and is_connected_tree(adj)
            controls = controls and max(map(len, adj)) <= MAX_DEGREE
            controls = controls and recursive_order_control(adj)
            controls = controls and (sum(map(len, adj)) // 2 == n - 1)

            m3, m7 = m3_m7(adj)
            m3s.append(m3)
            m7s.append(m7)

            hist = degree_histogram(adj)
            tvs.append(float(0.5 * np.abs(hist - min_hist).sum()))

        rows[str(alpha)] = {
            "M3": summarize_values(m3s),
            "M7": summarize_values(m7s),
            "degree_histogram_TV": summarize_values(tvs),
        }

    m3_means = [rows[str(a)]["M3"]["mean"] for a in ALPHAS]
    m7_means = [rows[str(a)]["M7"]["mean"] for a in ALPHAS]

    m3_strict = all(
        m3_means[i] > m3_means[i + 1]
        for i in range(len(m3_means) - 1)
    )
    m7_strict = all(
        m7_means[i] > m7_means[i + 1]
        for i in range(len(m7_means) - 1)
    )

    result.update(
        {
            "counterfactual_control": bool(controls),
            "dose_rows": rows,
            "M3_means_by_alpha": [
                {"alpha": a, "mean": float(v)}
                for a, v in zip(ALPHAS, m3_means)
            ],
            "M7_means_by_alpha": [
                {"alpha": a, "mean": float(v)}
                for a, v in zip(ALPHAS, m7_means)
            ],
            "M3_strictly_decreasing": m3_strict,
            "M7_strictly_decreasing": m7_strict,
        }
    )
    return result


def run():
    rows = [run_parent(2048, seed) for seed in (673, 701, 733)]

    replay_pass = all(row.get("trace_replay", False) for row in rows)
    controls = all(
        row.get("counterfactual_control", False) for row in rows
    )
    m3_gate = all(
        row.get("M3_strictly_decreasing", False) for row in rows
    )
    m7_gate = all(
        row.get("M7_strictly_decreasing", False) for row in rows
    )

    return {
        "protocol": "T49 frozen",
        "N": 2048,
        "seeds": [673, 701, 733],
        "alphas": list(ALPHAS),
        "rows": rows,
        "trace_replay": replay_pass,
        "counterfactual_control": controls,
        "M3_dose_response": m3_gate,
        "M7_dose_response": m7_gate,
        "selection_pressure_regulator": bool(
            replay_pass and controls and m3_gate and m7_gate
        ),
        "guard": (
            "Exact T25 candidate traces and paired random schedules across alpha; "
            "no new operators, degree matching, rescue seeds, target fitting, "
            "or physical-geometry claim."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
