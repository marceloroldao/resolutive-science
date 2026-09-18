"""T31 reference-relative flow diagnostics on frozen T30 distance."""
from __future__ import annotations
import json, math
import numpy as np
from t25_endogenous_dimension_scan import generate, distances
from t30_relational_compatibility import profile_from_dist

def profiles(adj,R):
    n=len(adj)
    ds=[distances(adj,u) for u in range(n)]
    return [profile_from_dist(ds[u],R,n) for u in range(n)]

def D(p,q): return float(np.sqrt(np.mean((p-q)**2)))

def audit_reference(adj,ps,a,tol=1e-15):
    phi=[D(ps[a],p) for p in ps]
    es=[(u,v) for u in range(len(adj)) for v in adj[u] if u<v]
    diffs=[phi[v]-phi[u] for u,v in es]
    G=float(np.mean(np.square(diffs))) if diffs else 0.0
    Z=float(np.mean([abs(x)<=tol for x in diffs])) if diffs else 1.0
    strict_min=0; reached=trapped=ambiguous=0; lens=[]
    for start in range(len(adj)):
        if start==a: reached+=1;lens.append(0);continue
        u=start; seen={u}; steps=0
        while True:
            lower=[v for v in adj[u] if phi[v] < phi[u]-tol]
            if not lower:
                trapped+=1
                if u!=a and all(phi[u] < phi[w]-tol for w in adj[u]): strict_min+=1
                break
            m=min(phi[v] for v in lower)
            best=[v for v in lower if abs(phi[v]-m)<=tol]
            if len(best)!=1:
                ambiguous+=1;break
            u=best[0];steps+=1
            if u==a:
                reached+=1;lens.append(steps);break
            if u in seen:
                trapped+=1;break
            seen.add(u)
    n=len(adj)
    return {"reference":a,"degree":len(adj[a]),"G":G,"neutral_fraction":Z,
      "reach_fraction":reached/n,"trap_fraction":trapped/n,
      "ambiguity_fraction":ambiguous/n,"mean_reach_steps":float(np.mean(lens)) if lens else None,
      "strict_local_min_events":strict_min}

def run():
    rows=[]
    for n in (128,256,512):
      for seed in (11,23,47):
        adj=generate(n,seed)
        for R in (1,2,4,8):
            ps=profiles(adj,R)
            refs=[audit_reference(adj,ps,a) for a in range(n)]
            rows.append({"n":n,"seed":seed,"R":R,
              "mean_G":float(np.mean([x["G"] for x in refs])),
              "mean_neutral_fraction":float(np.mean([x["neutral_fraction"] for x in refs])),
              "mean_reach_fraction":float(np.mean([x["reach_fraction"] for x in refs])),
              "mean_trap_fraction":float(np.mean([x["trap_fraction"] for x in refs])),
              "mean_ambiguity_fraction":float(np.mean([x["ambiguity_fraction"] for x in refs])),
              "references":refs})
    return {"protocol":"T31 frozen","rows":rows,
      "guard":"Reference-relative diagnostic only; no absolute direction or transition law."}

if __name__=="__main__": print(json.dumps(run(),indent=2))
