"""T16 — infinitesimal commutator bridge.

Tests the standard small-loop limit for independently chosen near-identity linear
transformations. This is a mathematical bridge/consistency test, not evidence that
physical Resolutive dynamics is linear or that the resulting object is physical curvature.
"""
from __future__ import annotations
import json
import numpy as np


def expm2(M: np.ndarray) -> np.ndarray:
    """Matrix exponential by eigendecomposition for the fixed real 2x2 test matrices."""
    w, v = np.linalg.eig(M)
    return np.real_if_close(v @ np.diag(np.exp(w)) @ np.linalg.inv(v)).astype(float)


def comm(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    return A @ B - B @ A


def loop(A: np.ndarray, B: np.ndarray, eps: float, delta: float) -> np.ndarray:
    Ae = expm2(eps * A)
    Bd = expm2(delta * B)
    Aei = expm2(-eps * A)
    Bdi = expm2(-delta * B)
    return Ae @ Bd @ Aei @ Bdi


def fro(M: np.ndarray) -> float:
    return float(np.linalg.norm(M, ord="fro"))


def run() -> dict:
    # Noncommuting nilpotent shear generators. No legacy RSMS constants.
    A = np.array([[0.0, 1.0], [0.0, 0.0]])
    B = np.array([[0.0, 0.0], [1.0, 0.0]])
    C = comm(A, B)
    I = np.eye(2)
    rows = []
    for e in [1e-1, 5e-2, 2e-2, 1e-2, 5e-3, 2e-3, 1e-3]:
        H = loop(A, B, e, e)
        scaled = (H - I) / (e * e)
        err = fro(scaled - C)
        rows.append({
            "epsilon": e,
            "loop_defect_norm": fro(H - I),
            "scaled_error_to_commutator": err,
            "scaled": scaled.tolist(),
        })

    # Commuting control.
    D = np.array([[1.0, 0.0], [0.0, -1.0]])
    E = 2.0 * D
    control = []
    for e in [1e-1, 1e-2, 1e-3]:
        H = loop(D, E, e, e)
        control.append({"epsilon": e, "loop_defect_norm": fro(H - I)})

    # Estimate convergence order of scaled error ~ O(epsilon).
    xs = np.log(np.array([r["epsilon"] for r in rows[-5:]]))
    ys = np.log(np.array([r["scaled_error_to_commutator"] for r in rows[-5:]]))
    slope = float(np.polyfit(xs, ys, 1)[0])

    return {
        "A": A.tolist(), "B": B.tolist(), "commutator": C.tolist(),
        "noncommuting_scan": rows,
        "commuting_control": control,
        "estimated_scaled_error_order": slope,
        "expected": "(H-I)/(epsilon*delta) -> [A,B] with first correction O(epsilon+delta)",
        "guard": "mathematical near-identity bridge only; not physical curvature validation",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
