"""T28 D28-A multiscale relational consolidation.

Frozen protocol implementation. Coordinate-free; node IDs are not used to break
structural symmetry. Theory-only.
"""
from __future__ import annotations
import json, random
from collections import Counter, deque
from t25_endogenous_dimension_scan import generate, distances

def signature(adj,u,R):
    d=distances(adj,u)
    shells=[]
    for r in range(R+1):
        nodes=[v for v,x in enumerate(d) if x==r]
        shells.append((len(nodes),tuple(sorted(Counter(len(adj[v]) for v in nodes).items()))))
    return tuple(shells)

def candidates(adj,R):
    sig=[signature(adj,u,R) for u in range(len(adj))]
    out=[]
    for u in range(len(adj)):
        du=distances(adj,u)
        for v in range(u+1,len(adj)):
            if v in adj[u]: continue
            if R < du[v] <= 2*R and sig[u]==sig[v]:
                key=(sig[u],tuple(sorted((len(adj[u]),len(adj[v])))))
                out.append((key,u,v))
    return out

def select_symmetry_safe(adj,R):
    cs=candidates(adj,R)
    # A structural key that names more than one possible pair is unresolved.
    # No ID-based choice is allowed. Only a uniquely characterized pair is accepted.
    by={}
    for key,u,v in cs: by.setdefault(key,[]).append((u,v))
    return [pairs[0] for key,pairs in by.items() if len(pairs)==1], {
        "candidate_pairs":len(cs),"structural_classes":len(by),
        "unresolved_pairs":sum(len(p) for p in by.values() if len(p)>1),
        "unique_structural_pairs":sum(1 for p in by.values() if len(p)==1)}

def step(adj,R):
    chosen,diag=select_symmetry_safe(adj,R)
    out=[set(x) for x in adj]
    for u,v in chosen: out[u].add(v);out[v].add(u)
    return out,chosen,diag

def edges(adj):return sum(map(len,adj))//2
def beta1(adj):return edges(adj)-len(adj)+1

def run(rounds=5):
    rows=[]
    for n in (128,256,512):
      for seed in (11,23,47):
        adj=generate(n,seed); initial_e=edges(adj)
        hist=[]
        for s in range(rounds):
            R=2**s; adj,added,diag=step(adj,R)
            hist.append({"round":s,"R":R,"added":len(added),"edges":edges(adj),
                         "beta1":beta1(adj),**diag})
        rows.append({"n":n,"seed":seed,"initial_edges":initial_e,"rounds":hist,
                     "final_edges":edges(adj),"final_beta1":beta1(adj)})
    return {"protocol":"D28-A frozen","rounds":rounds,"rows":rows,
            "guard":"zero activity caused by unresolved structural symmetry is a valid result."}

if __name__=="__main__":print(json.dumps(run(),indent=2))
