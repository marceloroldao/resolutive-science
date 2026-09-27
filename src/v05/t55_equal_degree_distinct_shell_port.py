"""T55 exact-degree / distinct-second-shell ordinary circuit feasibility.

This script checks only graph structure and Kirchhoff's conventional law.
It makes no new-physics or physical hazard claim.
"""
from __future__ import annotations
from collections import deque
import json
import math
import numpy as np

VERTICES = ("r", "A", "B", "C", "U", "V", "W", "B1", "C1", "C2")
EDGES = (
    ("r", "A"), ("r", "B"), ("r", "C"),
    ("A", "U"),
    ("B", "V"), ("B", "B1"),
    ("C", "W"), ("C", "C1"), ("C", "C2"),
)
R_OHM = 1000.0
SOURCE_VOLT = 3.0
TARGETS = ("U", "V", "W")
EXPECTED_Q = {"U": 1, "V": 2, "W": 3}


def adjacency():
    result = {v: set() for v in VERTICES}
    for a, b in EDGES:
        if a == b or b in result[a]:
            raise AssertionError("invalid edge")
        result[a].add(b)
        result[b].add(a)
    return result


def distances(adj, source):
    out = {source: 0}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in out:
                out[v] = out[u] + 1
                queue.append(v)
    return out


def path_edges(adj, start, finish):
    predecessor = {start: None}
    queue = deque([start])
    while queue and finish not in predecessor:
        u = queue.popleft()
        for v in adj[u]:
            if v not in predecessor:
                predecessor[v] = u
                queue.append(v)
    if finish not in predecessor:
        raise AssertionError("disconnected graph")
    edges = set()
    cur = finish
    while cur != start:
        prev = predecessor[cur]
        edges.add(frozenset((cur, prev)))
        cur = prev
    return edges


def laplacian():
    idx = {name: i for i, name in enumerate(VERTICES)}
    L = np.zeros((len(VERTICES), len(VERTICES)), dtype=float)
    g = 1.0 / R_OHM
    for a, b in EDGES:
        i, j = idx[a], idx[b]
        L[i, i] += g
        L[j, j] += g
        L[i, j] -= g
        L[j, i] -= g
    return L, idx


def port_solution(adj, L, idx, target):
    fixed = {"r": SOURCE_VOLT, target: 0.0}
    free = [v for v in VERTICES if v not in fixed]
    Fi = [idx[v] for v in fixed]
    Ui = [idx[v] for v in free]
    fixed_values = np.array(list(fixed.values()), dtype=float)

    V = np.zeros(len(VERTICES), dtype=float)
    V[Fi] = fixed_values
    V[Ui] = np.linalg.solve(
        L[np.ix_(Ui, Ui)],
        -L[np.ix_(Ui, Fi)] @ fixed_values,
    )
    current = float((L @ V)[idx["r"]])
    power = sum(
        float((V[idx[a]] - V[idx[b]]) ** 2 / R_OHM)
        for a, b in EDGES
    )
    kcl_error = float(np.max(np.abs((L @ V)[Ui])))
    path = path_edges(adj, "r", target)
    nonpath_current = max(
        (
            abs(float((V[idx[a]] - V[idx[b]]) / R_OHM))
            for a, b in EDGES
            if frozenset((a, b)) not in path
        ),
        default=0.0,
    )
    resistance = SOURCE_VOLT / current
    return {
        "target": target,
        "q": sum(d == 2 for d in distances(adj, target).values()),
        "degree": len(adj[target]),
        "path_edges": len(path),
        "R_eff_ohm": resistance,
        "I_source_ampere": current,
        "P_total_watt": power,
        "max_floating_KCL_ampere": kcl_error,
        "max_off_path_current_ampere": nonpath_current,
        "numerical_control": (
            math.isclose(resistance, 2000.0, rel_tol=1e-9)
            and math.isclose(current, 0.0015, rel_tol=1e-9)
            and math.isclose(power, 0.0045, rel_tol=1e-9)
            and kcl_error <= 1e-12
            and nonpath_current <= 1e-12
        ),
    }


def run():
    adj = adjacency()
    structural_control = (
        len(VERTICES) == 10
        and len(EDGES) == 9
        and len(distances(adj, "r")) == 10
        and all(len(adj[v]) == 1 for v in TARGETS)
    )
    q = {v: sum(d == 2 for d in distances(adj, v).values()) for v in TARGETS}
    contrast_control = q == EXPECTED_Q and q["V"] - q["U"] == 1 and q["W"] - q["U"] == 2
    L, idx = laplacian()
    ports = [port_solution(adj, L, idx, target) for target in TARGETS]
    circuit_control = all(p["numerical_control"] for p in ports)
    return {
        "protocol": "T55 frozen",
        "status": "conventional analytical / numerical feasibility only",
        "structural_control": structural_control,
        "q": q,
        "contrast_control": contrast_control,
        "ports": ports,
        "circuit_control": circuit_control,
        "T55_FEASIBILITY": bool(structural_control and contrast_control and circuit_control),
        "physical_hazard_comparator": "NOT_CALIBRATED",
        "physical_measurement": "NOT_EXECUTED",
        "new_physics": "NOT_ESTABLISHED",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))
    if not result["T55_FEASIBILITY"]:
        raise SystemExit(1)
