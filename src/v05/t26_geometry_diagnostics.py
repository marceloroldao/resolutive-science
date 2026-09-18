"""T26 diagnostics for the frozen T25 endogenous generator.

No retuning. Audits topology/finite-size behavior before any second generator.
"""
from __future__ import annotations
import json, math, random
from collections import deque, Counter
import numpy as np
from t25_endogenous_dimension_scan import generate, distances

def edges(adj): return sum(map(len,adj))//2

def components(adj):
    unseen=set(range(len(adj))); c=0
    while unseen:
        c+=1; root=next(iter(unseen)); q=[root]; unseen.remove(root)
        while q:
            u=q.pop()
            for v in adj[u]:
                if v in unseen: unseen.remove(v); q.append(v)
    return c

def cycle_rank(adj):
    # first Betti number for undirected graph
    return edges(adj)-len(adj)+components(adj)

def degree_hist(adj): return dict(sorted(Counter(map(len,adj)).items()))

def diameter_sample(adj,roots):
    ecc=[max(distances(adj,r)) for r in roots]
    return max(ecc), float(np.mean(ecc))

def ball_curve(adj,root):
    d=distances(adj,root); D=max(d)
    return [(r,sum(x<=r for x in d)) for r in range(1,D+1)]

def local_growth(adj,roots):
    out=[]
    for root in roots:
        curve=ball_curve(adj,root); slopes=[]
        for (r0,v0),(r1,v1) in zip(curve,curve[1:]):
            if r0>=1 and v1 < .8*len(adj):
                slopes.append((r1,math.log(v1/v0)/math.log(r1/r0)))
        out.append({"root":root,"slopes":slopes})
    return out

def triangle_count(adj):
    s=0
    for u in range(len(adj)):
        for v in adj[u]:
            if v>u:s+=len(adj[u].intersection(adj[v]))
    return s//3

def spectral_return_lazy(adj,times=(2,4,8,16,32,64)):
    n=len(adj); A=np.zeros((n,n))
    for i,ns in enumerate(adj):
        for j in ns:A[i,j]=1
    deg=A.sum(1)
    P=.5*np.eye(n)+.5*(A/deg[:,None])
    ev=np.real_if_close(np.linalg.eigvals(P)).real
    ret=[float(np.sum(ev**t)/n) for t in times]
    local=[]
    for i in range(1,len(times)):
        slope=math.log(ret[i]/ret[i-1])/math.log(times[i]/times[i-1])
        local.append((times[i],-2*slope))
    return ret,local

def audit():
    rows=[]
    for n in (128,256,512):
      for seed in (11,23,47):
        adj=generate(n,seed); roots=random.Random(seed+100).sample(range(n),8)
        diam,mean_ecc=diameter_sample(adj,roots)
        ret,ds_local=spectral_return_lazy(adj)
        rows.append({"n":n,"seed":seed,"edges":edges(adj),"components":components(adj),
          "cycle_rank":cycle_rank(adj),"cycle_rank_per_node":cycle_rank(adj)/n,
          "triangles":triangle_count(adj),"degree_histogram":degree_hist(adj),
          "sample_diameter":diam,"mean_eccentricity":mean_ecc,
          "local_growth":local_growth(adj,roots),
          "lazy_return_probability":ret,"lazy_local_spectral_dimension":ds_local})
    return {"status":"diagnostic only; frozen T25 generator unchanged","rows":rows}

if __name__=="__main__": print(json.dumps(audit(),indent=2))
