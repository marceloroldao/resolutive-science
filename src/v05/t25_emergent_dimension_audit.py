"""T25 — emergent dimension audit for relational networks.

Computes graph-ball growth and spectral/random-walk diagnostics on known control graphs.
The purpose is to validate dimension estimators before applying them to endogenous
Resolutive networks. Theory-only; no physical spatial dimension is claimed.
"""
from __future__ import annotations
import json, math
from collections import deque
import numpy as np


def ring_adj(n:int):
    A=np.zeros((n,n),dtype=float)
    for i in range(n): A[i,(i-1)%n]=A[i,(i+1)%n]=1
    return A


def torus_adj(L:int,d:int):
    shape=(L,)*d; n=L**d; A=np.zeros((n,n),dtype=float)
    def idx(coord):
        z=0
        for c in coord: z=z*L+(c%L)
        return z
    for flat in range(n):
        coord=[]; q=flat
        for _ in range(d): coord.append(q%L); q//=L
        coord=coord[::-1]
        for ax in range(d):
            for s in (-1,1):
                c=coord.copy(); c[ax]=(c[ax]+s)%L
                A[flat,idx(c)]=1
    return A


def ball_volumes(A,root=0,max_r=None):
    n=len(A); dist=[None]*n; dist[root]=0; dq=deque([root])
    while dq:
        u=dq.popleft()
        for v in np.flatnonzero(A[u]):
            if dist[v] is None: dist[v]=dist[u]+1; dq.append(int(v))
    diam=max(x for x in dist if x is not None)
    if max_r is None: max_r=max(1,diam//3)
    rs=list(range(1,min(max_r,diam)+1))
    vs=[sum(x is not None and x<=r for x in dist) for r in rs]
    return rs,vs,diam


def local_log_slopes(rs,vs):
    out=[]
    for i in range(1,len(rs)):
        out.append((rs[i], math.log(vs[i]/vs[i-1])/math.log(rs[i]/rs[i-1])))
    return out


def growth_fit(rs,vs):
    if len(rs)<3:return None
    # Exclude r=1 and late finite-size saturation where possible.
    x=np.log(np.array(rs[1:],float)); y=np.log(np.array(vs[1:],float))
    return float(np.polyfit(x,y,1)[0])


def spectral_dimension(A,times):
    deg=A.sum(axis=1); P=A/deg[:,None]
    eig=np.linalg.eigvals(P)
    eig=np.real_if_close(eig).real
    ret=[]
    for t in times:
        # Average return probability = trace(P^t)/N.
        p=float(np.sum(eig**t)/len(eig)); ret.append(max(p,1e-300))
    # For diffusion P_return ~ t^{-d_s/2}; fit only positive even times supplied.
    x=np.log(np.array(times,float)); y=np.log(np.array(ret,float))
    slope=float(np.polyfit(x,y,1)[0]); ds=-2*slope
    return ret,ds


def audit(name,A):
    rs,vs,diam=ball_volumes(A)
    # choose early/intermediate radii before torus saturation
    cut=max(3,min(len(rs),6))
    dg=growth_fit(rs[:cut],vs[:cut])
    times=[2,4,6,8,10,12]
    ret,ds=spectral_dimension(A,times)
    return {'name':name,'nodes':len(A),'diameter':diam,'radii':rs,'ball_volumes':vs,
            'growth_dimension_fit':dg,'local_growth_slopes':local_log_slopes(rs[:cut],vs[:cut]),
            'return_times':times,'return_probabilities':ret,'spectral_dimension_fit':ds}


def run():
    controls=[('ring_128',ring_adj(128)),('torus2_L16',torus_adj(16,2)),('torus3_L8',torus_adj(8,3))]
    return {'controls':[audit(n,A) for n,A in controls],
            'definitions':{
                'growth_dimension':'V(r) ~ r^d_g on a scaling window',
                'spectral_dimension':'P_return(t) ~ t^(-d_s/2) on a diffusion scaling window',
                'walk_dimension':'<r^2> ~ t^(2/d_w); not estimated in this first harness'},
            'decision_rule':'dimension is emergent only if a stable scaling window survives graph size/root/coarse-graining checks; disagreement among d_g,d_s,d_w is reported, not averaged away',
            'guard':'control graphs have known construction dimension; this validates estimators only, not a physical Resolutive dimension.'}

if __name__=='__main__': print(json.dumps(run(),indent=2))
