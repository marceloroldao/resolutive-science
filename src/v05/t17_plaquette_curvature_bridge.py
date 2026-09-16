"""T17 — position-dependent plaquette bridge to full connection curvature.

Mathematical consistency test only. It checks whether a small rectangular loop built
from position-dependent near-identity transports recovers derivative + commutator
terms. It is not physical validation of Resolutive curvature.
"""
from __future__ import annotations
import json
import numpy as np


def expm(M: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(M, ord=np.inf)
    s = max(0, int(np.ceil(np.log2(norm))) + 1) if norm > 0 else 0
    X = M / (2**s)
    out = np.eye(M.shape[0]); term = np.eye(M.shape[0])
    for k in range(1, 50):
        term = term @ X / k
        out = out + term
        if np.linalg.norm(term, ord=np.inf) < 1e-18: break
    for _ in range(s): out = out @ out
    return out

P=np.array([[0.,1.],[0.,0.]])
Q=np.array([[0.,0.],[1.,0.]])
R=np.array([[1.,0.],[0.,-1.]])

def A_x(x,y): return (1.0+0.30*y)*P + 0.20*x*R
def A_y(x,y): return (0.70+0.40*x)*Q - 0.10*y*R
def d_x_Ay(): return 0.40*Q
def d_y_Ax(): return 0.30*P
def comm(A,B): return A@B-B@A

# With dU/ds = +A_s U and later transports multiplying on the left, the
# compatible connection convention is F = dA - A wedge A.
def F_expected(x,y): return d_x_Ay()-d_y_Ax()-comm(A_x(x,y),A_y(x,y))

def edge(A,length): return expm(length*A)
def plaquette(x,y,h):
    U1=edge(A_x(x+h/2,y),h)
    U2=edge(A_y(x+h,y+h/2),h)
    U3=edge(A_x(x+h/2,y+h),-h)
    U4=edge(A_y(x,y+h/2),-h)
    return U4@U3@U2@U1

def fro(M): return float(np.linalg.norm(M,ord='fro'))

def run():
    x,y=0.23,-0.17; F=F_expected(x,y); rows=[]
    for h in [1e-1,5e-2,2e-2,1e-2,5e-3,2e-3,1e-3]:
        H=plaquette(x,y,h); scaled=(H-np.eye(2))/(h*h); err=fro(scaled-F)
        rows.append({'h':h,'defect_norm':fro(H-np.eye(2)),
                     'scaled_error_to_F':err,'scaled':scaled.tolist()})
    xs=np.log([r['h'] for r in rows[-5:]])
    ys=np.log([r['scaled_error_to_F'] for r in rows[-5:]])
    slope=float(np.polyfit(xs,ys,1)[0])
    scalar=[]
    for h in [1e-1,1e-2,1e-3]:
        integral=h*(0.3*y)+h*(0.4*(x+h))-h*(0.3*(y+h))-h*(0.4*x)
        scalar.append({'h':h,'scaled_log_holonomy':integral/(h*h)})
    return {'base_point':[x,y],'convention':'dU/ds=+A U => F=dA-A∧A',
            'F_expected':F.tolist(),'rows':rows,'estimated_error_order':slope,
            'abelian_derivative_control':scalar,
            'guard':'full derivative+commutator bridge in chosen representation; not physical validation'}

if __name__=='__main__': print(json.dumps(run(),indent=2))
