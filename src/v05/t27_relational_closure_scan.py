"""T27 coordinate-free relational closure scan."""
from __future__ import annotations
import json, random
import numpy as np
from t25_endogenous_dimension_scan import generate, distances, growth_dim, spectral_dim, walk_dim, relabel

def closure_once(adj):
    base=[set(x) for x in adj]; n=len(base); add=[]
    for u in range(n):
        for v in range(u+1,n):
            if v in base[u]: continue
            if base[u].intersection(base[v]): add.append((u,v))
    out=[set(x) for x in base]
    for u,v in add: out[u].add(v); out[v].add(u)
    return out,add

def edges(adj): return sum(map(len,adj))//2

def cycle_rank(adj): return edges(adj)-len(adj)+1

def triangles(adj):
    s=0
    for u in range(len(adj)):
        for v in adj[u]:
            if v>u:s+=len(adj[u].intersection(adj[v]))
    return s//3

def clustering(adj):
    vals=[]
    for u,ns in enumerate(adj):
        k=len(ns)
        if k<2: vals.append(0.0); continue
        links=sum(1 for a in ns for b in ns if a<b and b in adj[a])
        vals.append(2*links/(k*(k-1)))
    return float(np.mean(vals))

def sampled_diameter(adj,roots):
    ecc=[max(distances(adj,r)) for r in roots]
    return max(ecc),float(np.mean(ecc))

def audit():
    rows=[]
    for n in (128,256,512):
      for seed in (11,23,47):
        base=generate(n,seed); adj,added=closure_once(base)
        roots=random.Random(seed+100).sample(range(n),8)
        dg=growth_dim(adj,roots); ds,ret=spectral_dim(adj); dw,msd=walk_dim(adj,roots,seed=seed+200)
        diam,me=sampled_diameter(adj,roots)
        # exact relabeling covariance: close after relabel vs relabel after close, compare invariant summary
        rb=relabel(base,seed+300); rc,_=closure_once(rb)
        inv=lambda g:(edges(g),sorted(map(len,g)),cycle_rank(g),triangles(g))
        rows.append({"n":n,"seed":seed,"base_edges":edges(base),"closure_edges_added":len(added),
          "edges":edges(adj),"mean_degree":2*edges(adj)/n,"cycle_rank":cycle_rank(adj),
          "cycle_rank_per_node":cycle_rank(adj)/n,"triangles":triangles(adj),
          "mean_clustering":clustering(adj),"sample_diameter":diam,"mean_eccentricity":me,
          "growth_dimension_mean":float(np.mean(dg)) if dg else None,
          "growth_dimension_roots":dg,"spectral_dimension":ds,"walk_dimension":dw,
          "return_probabilities":ret,"msd":msd,"relabel_covariant":inv(adj)==inv(rc)})
    return {"protocol":{"common_neighbors_threshold":1,"closure_rounds":1,
      "coordinates":False,"target_dimension":None},"rows":rows,
      "guard":"T27 tests a frozen local closure rule; it does not identify physical space."}

if __name__=="__main__": print(json.dumps(audit(),indent=2))
