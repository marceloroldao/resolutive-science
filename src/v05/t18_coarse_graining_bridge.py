"""T18 — coarse-graining audit starting directly from D13-A.

Tests whether the discrete reversible rule admits a stable low-dimensional linear
coarse representation. This is a theory-only mathematical audit, not physical validation.
"""
from __future__ import annotations
import json
import numpy as np


def ring_laplacian(n: int) -> np.ndarray:
    L = -2.0*np.eye(n)
    for i in range(n):
        L[i,(i-1)%n] += 1.0
        L[i,(i+1)%n] += 1.0
    return L


def d13a_linear_operator(n: int, coupling: float) -> np.ndarray:
    """Lift (prev,cur)->(cur,prev+coupling*L cur), before modular reduction."""
    I=np.eye(n); Z=np.zeros((n,n)); L=ring_laplacian(n)
    return np.block([[Z,I],[I,coupling*L]])


def fourier_basis(n: int, modes: int) -> np.ndarray:
    """Real orthonormal low-frequency block/coarse basis."""
    cols=[np.ones(n)/np.sqrt(n)]
    k=1
    while len(cols)<modes and k <= n//2:
        c=np.cos(2*np.pi*k*np.arange(n)/n); c=c/np.linalg.norm(c); cols.append(c)
        if len(cols)<modes:
            s=np.sin(2*np.pi*k*np.arange(n)/n)
            if np.linalg.norm(s)>1e-12: cols.append(s/np.linalg.norm(s))
        k+=1
    return np.column_stack(cols[:modes])


def coarse_operator(M: np.ndarray, B: np.ndarray) -> tuple[np.ndarray,float]:
    """Galerkin projection onto same coarse basis for prev and cur."""
    Z=np.zeros_like(B)
    Q=np.block([[B,Z],[Z,B]])
    Me=Q.T@M@Q
    residual=np.linalg.norm(M@Q-Q@Me,'fro')/max(np.linalg.norm(M@Q,'fro'),1e-15)
    return Me,float(residual)


def generator_diagnostic(Me: np.ndarray, steps: int) -> dict:
    """Finite-step effective operator; report closeness to identity before any log."""
    U=np.linalg.matrix_power(Me,steps)
    defect=float(np.linalg.norm(U-np.eye(U.shape[0]),'fro'))
    return {'steps':steps,'identity_defect':defect,'generator_linearization_valid':defect<0.25,
            'G_linear':((U-np.eye(U.shape[0]))/steps).tolist()}


def run() -> dict:
    rows=[]
    for n in [16,32,64,128]:
        for coupling in [0.01,0.02,0.05]:
            M=d13a_linear_operator(n,coupling)
            for modes in [1,3,5]:
                B=fourier_basis(n,modes)
                Me,res=coarse_operator(M,B)
                eig=np.linalg.eigvals(Me)
                rows.append({'n':n,'coupling':coupling,'modes':modes,
                             'projection_residual':res,
                             'spectral_radius':float(max(abs(eig))),
                             'one_step_identity_defect':float(np.linalg.norm(Me-np.eye(Me.shape[0]),'fro')),
                             'two_step':generator_diagnostic(Me,2)})
    return {'source':'direct linear lift of D13-A local-force rule; no prescribed connection/curvature',
            'rows':rows,
            'decision_rule':{'stable_projection':'residual decreases/remains small across n',
                             'near_identity_generator':'requires a coarse evolution operator approaching I under an explicit scaling'},
            'guard':'A stable coarse linear representation is not automatically a continuum physical law.'}

if __name__=='__main__': print(json.dumps(run(),indent=2))
