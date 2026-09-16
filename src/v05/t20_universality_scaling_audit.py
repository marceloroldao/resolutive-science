"""T20 — universality audit of the T19 scaling exponent.

Compares spectral-gap scaling for relational Laplacians on several graph families.
Theory-only: identifies what controls p*, not a physical validation.
"""
from __future__ import annotations
import json, math
import numpy as np


def laplacian_from_adj(A):
    return A-np.diag(A.sum(axis=1))  # negative-semidefinite convention used in T18/T19


def ring(n):
    A=np.zeros((n,n))
    for i in range(n): A[i,(i-1)%n]=A[i,(i+1)%n]=1
    return laplacian_from_adj(A)


def chain(n):
    A=np.zeros((n,n))
    for i in range(n-1): A[i,i+1]=A[i+1,i]=1
    return laplacian_from_adj(A)


def torus2(L):
    n=L*L; A=np.zeros((n,n))
    def idx(x,y): return (x%L)*L+(y%L)
    for x in range(L):
        for y in range(L):
            i=idx(x,y)
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)): A[i,idx(x+dx,y+dy)]=1
    return laplacian_from_adj(A)


def circulant_regular(n, offsets=(1,3)):
    A=np.zeros((n,n))
    for i in range(n):
        for d in offsets:
            A[i,(i+d)%n]=A[i,(i-d)%n]=1
    return laplacian_from_adj(A)


def gap(L):
    ev=np.sort(np.abs(np.linalg.eigvalsh(L)))
    return float(next(x for x in ev if x>1e-10))


def fit_power(sizes,gaps):
    x=np.log(np.asarray(sizes,float)); y=np.log(np.asarray(gaps,float))
    slope,intercept=np.polyfit(x,y,1)
    return float(-slope),float(math.exp(intercept))


def run():
    families={}
    specs=[('ring',[(n,ring(n)) for n in (16,24,32,48,64,96,128)]),
           ('chain',[(n,chain(n)) for n in (16,24,32,48,64,96,128)]),
           ('circulant_degree4',[(n,circulant_regular(n)) for n in (16,24,32,48,64,96,128)]),
           ('torus2',[(L,torus2(L)) for L in (4,5,6,8,10,12,16)])]
    for name,items in specs:
        linear_sizes=[s for s,_ in items]
        node_counts=[M.shape[0] for _,M in items]
        gs=[gap(M) for _,M in items]
        p_linear,C=fit_power(linear_sizes,gs)
        p_nodes,Cn=fit_power(node_counts,gs)
        families[name]={'linear_sizes':linear_sizes,'node_counts':node_counts,'spectral_gaps':gs,
                        'gap_exponent_vs_linear_size':p_linear,
                        'gap_exponent_vs_node_count':p_nodes,
                        'prefactor_linear':C,'prefactor_nodes':Cn}
    return {'families':families,
            'interpretation':{'rule':'for D13-A two-step low mode, delta_R must scale like the relevant small Laplacian eigenvalue',
                              'expected_1d_local':'gap ~ L^-2 => p*=2 versus linear resolution L',
                              'expected_2d_local':'gap ~ L^-2 but ~ N^-1 because N=L^2',
                              'warning':'an exponent stated against raw node count is dimension/topology dependent'},
            'guard':'T20 tests universality of spectral scaling only; no universal physical time exponent is claimed.'}

if __name__=='__main__': print(json.dumps(run(),indent=2))
