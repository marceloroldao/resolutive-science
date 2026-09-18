"""T30 continuous coordinate-free relational compatibility audit."""
from __future__ import annotations
import json, math
import numpy as np
from t25_endogenous_dimension_scan import generate, distances

def profile_from_dist(d,R,n):
    counts=[0]*(R+1)
    for x in d:
        if 0 <= x <= R: counts[x]+=1
    cum=[]; s=0
    for x in counts:
        s+=x; cum.append(s/n)
    return np.asarray(cum,dtype=float)

def summaries(vals):
    a=np.asarray(vals,dtype=float)
    if len(a)==0:return {"count":0}
    q=np.quantile(a,[.05,.25,.5,.75,.95])
    mean=float(a.mean()); sd=float(a.std())
    return {"count":len(a),"min":float(a.min()),"q05":float(q[0]),
      "q25":float(q[1]),"median":float(q[2]),"q75":float(q[3]),
      "q95":float(q[4]),"max":float(a.max()),"mean":mean,"std":sd,
      "cv":sd/mean if mean else None,"zero_fraction":float(np.mean(a==0.0))}

def audit_graph(n,seed,R):
    adj=generate(n,seed)
    ds=[distances(adj,u) for u in range(n)]
    ps=[profile_from_dist(ds[u],R,n) for u in range(n)]
    band=[]; allpairs=[]
    for u in range(n):
      for v in range(u+1,n):
        D=float(np.sqrt(np.mean((ps[u]-ps[v])**2)))
        allpairs.append(D)
        if v not in adj[u] and R < ds[u][v] <= 2*R: band.append(D)
    def pack(vals):
        d=summaries(vals)
        c=summaries([1/(1+x) for x in vals])
        return {"D":d,"C":c}
    return {"n":n,"seed":seed,"R":R,"band":pack(band),"all_pairs":pack(allpairs)}

def run():
    rows=[]
    for n in (128,256,512):
      for seed in (11,23,47):
        for R in (1,2,4,8,16): rows.append(audit_graph(n,seed,R))
    return {"protocol":"T30 frozen","rows":rows,
      "guard":"Diagnostic only: no compatibility threshold and no edge addition."}

if __name__=="__main__":print(json.dumps(run(),indent=2))
