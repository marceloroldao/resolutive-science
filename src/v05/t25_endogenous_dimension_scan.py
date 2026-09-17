"""T25 endogenous dimension scan.

Generates graphs without Euclidean coordinates or target dimension, then estimates
growth, spectral and walk scaling. Theory-only; no physical spatial dimension claim.
"""
from __future__ import annotations
import json, math, random
from collections import deque
import numpy as np

def generate(n:int, seed:int, max_degree:int=6, sample_size:int=5):
    rng=random.Random(seed)
    adj=[set() for _ in range(n)]
    def edge(a,b):
        if a!=b and len(adj[a])<max_degree and len(adj[b])<max_degree:
            adj[a].add(b); adj[b].add(a); return True
        return False
    edge(0,1)
    for v in range(2,n):
        candidates=rng.sample(range(v), min(sample_size,v))
        candidates=sorted(candidates,key=lambda u:(len(adj[u]),rng.random()))
        if not any(edge(v,u) for u in candidates):
            avail=[u for u in range(v) if len(adj[u])<max_degree]
            if avail: edge(v,rng.choice(avail))
    # repair disconnected components coordinate-free
    seen={0}; q=deque([0])
    while q:
        u=q.popleft()
        for w in adj[u]:
            if w not in seen: seen.add(w); q.append(w)
    for v in range(n):
        if v not in seen:
            edge(v,rng.choice(tuple(seen))); seen.add(v)
    return adj

def distances(adj,root):
    d=[-1]*len(adj); d[root]=0; q=deque([root])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if d[v]<0:d[v]=d[u]+1;q.append(v)
    return d

def growth_dim(adj,roots):
    estimates=[]
    for root in roots:
        d=distances(adj,root); diam=max(d)
        rs=list(range(1,max(2,diam//2)+1))
        vs=[sum(x<=r for x in d) for r in rs]
        usable=[(r,v) for r,v in zip(rs,vs) if r>=2 and v < .75*len(adj)]
        if len(usable)>=3:
            x=np.log([a for a,b in usable]); y=np.log([b for a,b in usable])
            estimates.append(float(np.polyfit(x,y,1)[0]))
    return estimates

def spectral_dim(adj,times=(2,4,6,8,10,12)):
    n=len(adj); A=np.zeros((n,n))
    for i,ns in enumerate(adj):
        for j in ns:A[i,j]=1
    deg=A.sum(1); P=A/deg[:,None]
    ev=np.real_if_close(np.linalg.eigvals(P)).real
    ret=[max(float(np.sum(ev**t)/n),1e-300) for t in times]
    slope=float(np.polyfit(np.log(times),np.log(ret),1)[0])
    return -2*slope,ret

def walk_dim(adj,roots,times=range(2,13,2),walks=1500,seed=0):
    rng=random.Random(seed); rows=[]
    for t in times:
        vals=[]
        for root in roots:
            d=distances(adj,root); s=0.0
            for _ in range(walks):
                u=root
                for __ in range(t):u=rng.choice(tuple(adj[u]))
                s+=d[u]**2
            vals.append(s/walks)
        rows.append((t,sum(vals)/len(vals)))
    good=[x for x in rows if x[1]>0]
    slope=float(np.polyfit(np.log([x[0] for x in good]),np.log([x[1] for x in good]),1)[0])
    return 2/slope,rows

def relabel(adj,seed):
    rng=random.Random(seed); n=len(adj); p=list(range(n));rng.shuffle(p)
    out=[set() for _ in range(n)]
    for u in range(n):
        for v in adj[u]:out[p[u]].add(p[v])
    return out

def run():
    results=[]
    for n in (128,256,512):
      for seed in (11,23,47):
        adj=generate(n,seed)
        roots=random.Random(seed+100).sample(range(n),min(8,n))
        dg=growth_dim(adj,roots)
        ds,ret=spectral_dim(adj)
        dw,msd=walk_dim(adj,roots,seed=seed+200)
        adj2=relabel(adj,seed+300)
        # graph invariants used as relabeling check
        inv=(sorted(map(len,adj)),sum(map(len,adj))//2)
        inv2=(sorted(map(len,adj2)),sum(map(len,adj2))//2)
        results.append({"n":n,"seed":seed,"mean_degree":sum(map(len,adj))/n,
          "growth_dimension_mean":sum(dg)/len(dg) if dg else None,
          "growth_dimension_roots":dg,"spectral_dimension":ds,"walk_dimension":dw,
          "return_probabilities":ret,"msd":msd,"relabel_invariants_equal":inv==inv2})
    return {"generator":{"coordinates":False,"target_dimension":False,"max_degree":6,"sample_size":5},
      "results":results,
      "guard":"Any exponent is a property of this preregistered graph generator and estimator window, not physical space."}

if __name__=="__main__": print(json.dumps(run(),indent=2))
