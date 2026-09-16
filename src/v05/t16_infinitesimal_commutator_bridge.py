"""T16 — infinitesimal commutator bridge.

Pure mathematical consistency test. The chosen generators are nilpotent, so their
exponentials are exact: exp(tA)=I+tA. No physical-curvature claim is made.
"""
from __future__ import annotations
import json
import numpy as np


def comm(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    return A @ B - B @ A


def nilpotent_exp(M: np.ndarray, t: float) -> np.ndarray:
    I = np.eye(M.shape[0])
    if not np.allclose(M @ M, 0.0):
        raise ValueError("T16 exact exponential helper requires M^2=0")
    return I + t * M


def loop(A: np.ndarray, B: np.ndarray, eps: float, delta: float) -> np.ndarray:
    return (nilpotent_exp(A, eps) @ nilpotent_exp(B, delta) @
            nilpotent_exp(A, -eps) @ nilpotent_exp(B, -delta))


def fro(M: np.ndarray) -> float:
    return float(np.linalg.norm(M, ord="fro"))


def run() -> dict:
    A = np.array([[0.0, 1.0], [0.0, 0.0]])
    B = np.array([[0.0, 0.0], [1.0, 0.0]])
    C = comm(A, B)
    I = np.eye(2)
    rows = []
    for e in [1e-1, 5e-2, 2e-2, 1e-2, 5e-3, 2e-3, 1e-3]:
        H = loop(A, B, e, e)
        scaled = (H - I) / (e * e)
        rows.append({"epsilon": e, "loop_defect_norm": fro(H-I),
                     "scaled_error_to_commutator": fro(scaled-C),
                     "scaled": scaled.tolist()})
    xs = np.log(np.array([r["epsilon"] for r in rows[-5:]]))
    ys = np.log(np.array([r["scaled_error_to_commutator"] for r in rows[-5:]]))
    slope = float(np.polyfit(xs, ys, 1)[0])
    # commuting nilpotent control: A with itself
    control = [{"epsilon": e, "loop_defect_norm": fro(loop(A,A,e,e)-I)}
               for e in [1e-1,1e-2,1e-3]]
    return {"A":A.tolist(),"B":B.tolist(),"commutator":C.tolist(),
            "noncommuting_scan":rows,"commuting_control":control,
            "estimated_scaled_error_order":slope,
            "expected":"(H-I)/(epsilon*delta) -> [A,B]",
            "guard":"mathematical near-identity bridge only; not physical curvature validation"}

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
