"""T15: finite reversible relational maps and commutator-loop defects.

Pure mathematical consistency/emergence experiment. A nonidentity commutator here is
NOT physical curvature; it is a discrete algebraic precursor only.
"""
from __future__ import annotations
from itertools import product

State = tuple[int, ...]


def add_at(x: State, i: int, amount: int, m: int) -> State:
    y = list(x); y[i] = (y[i] + amount) % m; return tuple(y)


def shear_a(x: State, m: int) -> State:
    """Reversible relational shear: x0 <- x0 + x1."""
    return add_at(x, 0, x[1], m)


def shear_a_inv(x: State, m: int) -> State:
    return add_at(x, 0, -x[1], m)


def shear_b(x: State, m: int) -> State:
    """Reversible relational shear: x1 <- x1 + x0."""
    return add_at(x, 1, x[0], m)


def shear_b_inv(x: State, m: int) -> State:
    return add_at(x, 1, -x[0], m)


def shift0(x: State, m: int) -> State:
    return add_at(x, 0, 1, m)


def shift0_inv(x: State, m: int) -> State:
    return add_at(x, 0, -1, m)


def shift1(x: State, m: int) -> State:
    return add_at(x, 1, 1, m)


def shift1_inv(x: State, m: int) -> State:
    return add_at(x, 1, -1, m)


def compose(x: State, ops, m: int) -> State:
    for op in ops:
        x = op(x, m)
    return x


def commutator_loop(x: State, a, b, ainv, binv, m: int) -> State:
    # Apply A, B, A^-1, B^-1 in traversal order.
    return compose(x, (a, b, ainv, binv), m)


def exhaustive_scan(n: int, m: int, a, b, ainv, binv) -> dict:
    total = m ** n
    nonidentity = 0
    changed_sites = 0
    examples = []
    for x in product(range(m), repeat=n):
        y = commutator_loop(x, a, b, ainv, binv, m)
        if y != x:
            nonidentity += 1
            changed_sites += sum(u != v for u, v in zip(x, y))
            if len(examples) < 8:
                examples.append({"in": x, "out": y})
    return {
        "n": n, "m": m, "states": total,
        "nonidentity": nonidentity,
        "fraction_nonidentity": nonidentity / total,
        "mean_changed_sites_given_defect": (changed_sites / nonidentity if nonidentity else 0.0),
        "examples": examples,
    }


def inverse_check(n: int, m: int, op, inv) -> bool:
    return all(inv(op(x, m), m) == x and op(inv(x, m), m) == x
               for x in product(range(m), repeat=n))


def run_suite() -> dict:
    rows = {}
    for m in (2, 3, 4, 5, 7):
        rows[f"commuting_control_m{m}"] = exhaustive_scan(2, m, shift0, shift1, shift0_inv, shift1_inv)
        rows[f"noncommuting_shears_m{m}"] = exhaustive_scan(2, m, shear_a, shear_b, shear_a_inv, shear_b_inv)
    return {
        "inverse_checks": {
            "shift0": inverse_check(2, 7, shift0, shift0_inv),
            "shift1": inverse_check(2, 7, shift1, shift1_inv),
            "shear_a": inverse_check(2, 7, shear_a, shear_a_inv),
            "shear_b": inverse_check(2, 7, shear_b, shear_b_inv),
        },
        "scans": rows,
        "interpretation_guard": "nonidentity commutator = discrete algebraic loop defect only; not physical curvature",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_suite(), indent=2))
