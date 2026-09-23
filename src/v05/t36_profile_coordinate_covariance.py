"""T36 profile-coordinate covariance audit.

Compares cumulative-ball and exact-shell coordinates carrying exactly the same
finite-radius graph information. No dynamics or physical metric is introduced.
"""
from __future__ import annotations
import json
import numpy as np

from t25_endogenous_dimension_scan import generate, distances
from t30_relational_compatibility import profile_from_dist
from t35_canonical_scale_transport import audit_transition, pack


def shell_profile_from_dist(d, radius, n):
    counts = [0] * (radius + 1)
    for x in d:
        if 0 <= x <= radius:
            counts[x] += 1
    return np.asarray(counts, dtype=float) / n


def make_profiles(ds, radius, n, representation):
    if representation == "cumulative_ball":
        return [profile_from_dist(d, radius, n) for d in ds]
    if representation == "exact_shell":
        return [shell_profile_from_dist(d, radius, n) for d in ds]
    raise ValueError(representation)


def roundtrip_error(ball, shell):
    ball2 = np.cumsum(shell)
    shell2 = np.concatenate(([ball[0]], np.diff(ball)))
    return max(
        float(np.max(np.abs(ball - ball2))),
        float(np.max(np.abs(shell - shell2))),
    )


def run():
    runs = []
    max_roundtrip_error = 0.0

    for n in (128, 256, 512):
        for seed in (11, 23, 47):
            adj = generate(n, seed)
            ds = [distances(adj, u) for u in range(n)]

            for radius in (1, 2, 4, 8):
                balls = make_profiles(ds, radius, n, "cumulative_ball")
                shells = make_profiles(ds, radius, n, "exact_shell")
                for b, s in zip(balls, shells):
                    max_roundtrip_error = max(
                        max_roundtrip_error, roundtrip_error(b, s)
                    )

            for radius in (1, 2, 4):
                for representation in ("cumulative_ball", "exact_shell"):
                    p_low = make_profiles(ds, radius, n, representation)
                    p_high = make_profiles(ds, 2 * radius, n, representation)
                    rows = audit_transition(adj, p_low, p_high, radius)
                    runs.append(
                        {
                            "n": n,
                            "seed": seed,
                            "transition": f"{radius}->{2 * radius}",
                            "representation": representation,
                            "summary": pack(rows),
                        }
                    )

    return {
        "protocol": "T36 frozen",
        "max_information_roundtrip_error": max_roundtrip_error,
        "runs": runs,
        "guard": (
            "Same graph information only; no preferred profile metric, dynamics, "
            "graph evolution, target dimension, or physical tangent-space claim."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
