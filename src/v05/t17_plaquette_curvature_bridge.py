"""T17 — position-dependent plaquette bridge to full connection curvature.

Mathematical consistency test only. It checks whether a small rectangular loop built
from position-dependent near-identity transports recovers derivative + commutator
terms. It is not physical validation of Resolutive curvature.
"""
from __future__ import annotations
import json
import numpy as np


def expm(M: np.ndarray) -> np.ndarray:
    # Stable enough for the fixed small real 2x2 matrices used here.
    vals, vecs = np.linalg.eig(M)
    if abs(np.linalg.det(vecs)) < 1e-12:
        # Scaling/squaring Taylor fallback.
        norm = np.linalg.norm(M, ord=np.inf)
        s = max(0, int(np.ceil(np.log2(norm))) + 1) if norm > 0 else 0
        X = M / (2**s)
        R = np.eye(M.shape[0]); term = np.eye(M.shape[0])
        for k in range(1, 40):
            term = term @ X / k
            R = R + term
        for _ in range(s): R = R @ R
        return R
    R = vecs @ np.diag(np.exp(vals)) @ np.linalg.inv(vecs)
    return np.real_if_close(R).astype(float)


P = np.array([[0., 1.], [0., 0.]])
Q = np.array([[0., 0.], [1., 0.]])
R = np.array([[1., 0.], [0., -1.]])


def A_x(x: float, y: float) -> np.ndarray:
    return (1.0 + 0.30*y) * P + 0.20*x * R


def A_y(x: float, y: float) -> np.ndarray:
    return (0.70 + 0.40*x) * Q - 0.10*y * R


def d_x_Ay() -> np.ndarray:
    return 0.40 * Q


def d_y_Ax() -> np.ndarray:
    return 0.30 * P


def comm(A, B): return A @ B - B @ A


def F_expected(x: float, y: float) -> np.ndarray:
    return d_x_Ay() - d_y_Ax() + comm(A_x(x,y), A_y(x,y))


def edge(A, length: float) -> np.ndarray:
    return expm(length * A)


def plaquette(x: float, y: float, h: float) -> np.ndarray:
    # Counterclockwise: +x, +y, -x, -y. Edge generators sampled at edge midpoints.
    U1 = edge(A_x(x+h/2, y), h)
    U2 = edge(A_y(x+h, y+h/2), h)
    U3 = edge(A_x(x+h/2, y+h), -h)
    U4 = edge(A_y(x, y+h/2), -h)
    # Column-vector convention: later transport multiplies on the left.
    return U4 @ U3 @ U2 @ U1


def fro(M): return float(np.linalg.norm(M, ord='fro'))


def run():
    x, y = 0.23, -0.17
    F = F_expected(x,y)
    rows=[]
    for h in [1e-1,5e-2,2e-2,1e-2,5e-3,2e-3,1e-3]:
        H=plaquette(x,y,h)
        scaled=(H-np.eye(2))/(h*h)
        # Depending on traversal/operator convention the loop returns +/- F.
        err_plus=fro(scaled-F); err_minus=fro(scaled+F)
        sign=1 if err_plus <= err_minus else -1
        err=min(err_plus,err_minus)
        rows.append({'h':h,'defect_norm':fro(H-np.eye(2)),
                     'scaled_error_to_oriented_F':err,'orientation_sign':sign,
                     'scaled':scaled.tolist()})
    xs=np.log([r['h'] for r in rows[-5:]])
    ys=np.log([r['scaled_error_to_oriented_F'] for r in rows[-5:]])
    slope=float(np.polyfit(xs,ys,1)[0])

    # Abelian/scalar control: commutator vanishes but derivative curl remains.
    # ax=0.3*y, ay=0.4*x => d_x ay-d_y ax = 0.1.
    scalar=[]
    for h in [1e-1,1e-2,1e-3]:
        # Exact scalar loop integral with midpoint-linear fields.
        integral = h*(0.3*y) + h*(0.4*(x+h)) - h*(0.3*(y+h)) - h*(0.4*x)
        scaled=integral/(h*h)
        scalar.append({'h':h,'scaled_log_holonomy':scaled})
    return {'base_point':[x,y], 'F_expected':F.tolist(), 'rows':rows,
            'estimated_error_order':slope,
            'abelian_derivative_control':scalar,
            'guard':'full derivative+commutator bridge in chosen representation; not physical validation'}

if __name__=='__main__': print(json.dumps(run(),indent=2))
