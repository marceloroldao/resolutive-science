"""T14 reference simulator for the v0.5 Resolutive transition-law candidates.

Theory-only computational consistency harness. It does not validate a physical theory.
No legacy Resolutive constants are inserted.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product, permutations
import math
import random
from typing import Iterable, Sequence

State = tuple[int, ...]
PairState = tuple[State, State]


def ring_neighbors(n: int) -> tuple[tuple[int, int], ...]:
    if n < 3:
        raise ValueError("n must be >= 3")
    return tuple(((i - 1) % n, (i + 1) % n) for i in range(n))


def local_force(x: State, i: int, neighbors: Sequence[Sequence[int]], m: int) -> int:
    """Permutation-covariant example force using only relational-neighbor states."""
    return sum((x[j] - x[i]) for j in neighbors[i]) % m


def step_a(prev: State, cur: State, neighbors: Sequence[Sequence[int]], m: int) -> State:
    return tuple((prev[i] + local_force(cur, i, neighbors, m)) % m for i in range(len(cur)))


def inverse_a(cur: State, nxt: State, neighbors: Sequence[Sequence[int]], m: int) -> State:
    return tuple((nxt[i] - local_force(cur, i, neighbors, m)) % m for i in range(len(cur)))


def evolve_pair_a(z: PairState, neighbors: Sequence[Sequence[int]], m: int) -> PairState:
    prev, cur = z
    return cur, step_a(prev, cur, neighbors, m)


def orbit_period_a(z0: PairState, neighbors: Sequence[Sequence[int]], m: int, max_steps: int = 100000) -> int | None:
    z = z0
    for k in range(1, max_steps + 1):
        z = evolve_pair_a(z, neighbors, m)
        if z == z0:
            return k
    return None


@dataclass(frozen=True)
class BState:
    x: State
    h: State


def step_b(s: BState, neighbors: Sequence[Sequence[int]], m: int, hmod: int) -> BState:
    # History accumulates a bounded local transition surrogate.
    h2 = tuple((s.h[i] + local_force(s.x, i, neighbors, m)) % hmod for i in range(len(s.x)))
    # Present evolution is explicitly history-sensitive.
    x2 = tuple((s.x[i] + local_force(s.x, i, neighbors, m) + h2[i]) % m for i in range(len(s.x)))
    return BState(x2, h2)


def history_ablation_pair(x: State, h1: State, h2: State, neighbors: Sequence[Sequence[int]], m: int, hmod: int) -> tuple[State, State]:
    return step_b(BState(x, h1), neighbors, m, hmod).x, step_b(BState(x, h2), neighbors, m, hmod).x


def softmax(scores: Sequence[float]) -> tuple[float, ...]:
    mx = max(scores)
    e = [math.exp(s - mx) for s in scores]
    z = sum(e)
    return tuple(v / z for v in e)


def kernel_c(x: State, i: int, neighbors: Sequence[Sequence[int]], m: int, beta: float = 1.0) -> tuple[float, ...]:
    # beta is a computational model parameter, not inverse temperature.
    target = sum(x[j] for j in neighbors[i]) / len(neighbors[i])
    scores = [-beta * abs(a - target) for a in range(m)]
    return softmax(scores)


def sample_c(x: State, neighbors: Sequence[Sequence[int]], m: int, rng: random.Random, beta: float = 1.0) -> State:
    out = []
    for i in range(len(x)):
        p = kernel_c(x, i, neighbors, m, beta)
        r = rng.random()
        acc = 0.0
        chosen = m - 1
        for a, pa in enumerate(p):
            acc += pa
            if r <= acc:
                chosen = a
                break
        out.append(chosen)
    return tuple(out)


def relabel_state(x: State, pi: Sequence[int]) -> State:
    y = [0] * len(x)
    for old, new in enumerate(pi):
        y[new] = x[old]
    return tuple(y)


def relabel_neighbors(neighbors: Sequence[Sequence[int]], pi: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    out: list[list[int]] = [[] for _ in pi]
    for old, new in enumerate(pi):
        out[new] = [pi[j] for j in neighbors[old]]
    return tuple(tuple(v) for v in out)


def test_a_reversibility(samples: int = 500, n: int = 7, m: int = 5, seed: int = 13) -> dict:
    rng = random.Random(seed)
    nb = ring_neighbors(n)
    failures = 0
    for _ in range(samples):
        prev = tuple(rng.randrange(m) for _ in range(n))
        cur = tuple(rng.randrange(m) for _ in range(n))
        nxt = step_a(prev, cur, nb, m)
        if inverse_a(cur, nxt, nb, m) != prev:
            failures += 1
    return {"samples": samples, "failures": failures, "pass": failures == 0}


def test_permutation_covariance(samples: int = 250, n: int = 7, m: int = 5, seed: int = 14) -> dict:
    rng = random.Random(seed)
    nb = ring_neighbors(n)
    failures = 0
    for _ in range(samples):
        prev = tuple(rng.randrange(m) for _ in range(n))
        cur = tuple(rng.randrange(m) for _ in range(n))
        pi = list(range(n))
        rng.shuffle(pi)
        nb2 = relabel_neighbors(nb, pi)
        lhs = step_a(relabel_state(prev, pi), relabel_state(cur, pi), nb2, m)
        rhs = relabel_state(step_a(prev, cur, nb, m), pi)
        failures += lhs != rhs
    return {"samples": samples, "failures": failures, "pass": failures == 0}


def test_b_history_effect(n: int = 7, m: int = 5, hmod: int = 7) -> dict:
    nb = ring_neighbors(n)
    x = tuple((i * 2 + 1) % m for i in range(n))
    h0 = tuple(0 for _ in range(n))
    h1 = tuple((i + 1) % hmod for i in range(n))
    a, b = history_ablation_pair(x, h0, h1, nb, m, hmod)
    differing_sites = sum(u != v for u, v in zip(a, b))
    return {"differing_sites": differing_sites, "pass": differing_sites > 0, "next_without_history_label": a, "next_with_history_label": b}


def test_c_normalization(samples: int = 250, n: int = 7, m: int = 5, seed: int = 15) -> dict:
    rng = random.Random(seed)
    nb = ring_neighbors(n)
    max_error = 0.0
    for _ in range(samples):
        x = tuple(rng.randrange(m) for _ in range(n))
        i = rng.randrange(n)
        p = kernel_c(x, i, nb, m)
        max_error = max(max_error, abs(sum(p) - 1.0))
    return {"samples": samples, "max_normalization_error": max_error, "pass": max_error < 1e-12}


def exact_small_orbit_scan(n: int = 3, m: int = 2) -> dict:
    nb = ring_neighbors(n)
    states = list(product(range(m), repeat=n))
    periods: dict[int, int] = {}
    missing = 0
    max_bound = len(states) ** 2
    for prev in states:
        for cur in states:
            p = orbit_period_a((prev, cur), nb, m, max_bound)
            if p is None:
                missing += 1
            else:
                periods[p] = periods.get(p, 0) + 1
    return {"n": n, "m": m, "pair_states": len(states) ** 2, "period_histogram": dict(sorted(periods.items())), "missing": missing, "pass": missing == 0}


def run_reference_suite() -> dict:
    return {
        "A_reversibility": test_a_reversibility(),
        "A_permutation_covariance": test_permutation_covariance(),
        "A_exact_small_orbits": exact_small_orbit_scan(),
        "B_history_ablation": test_b_history_effect(),
        "C_normalization": test_c_normalization(),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_reference_suite(), indent=2, sort_keys=True))
