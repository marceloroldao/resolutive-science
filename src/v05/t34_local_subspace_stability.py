"""T34 local subspace stability audit. No target rank/dimension."""
from __future__ import annotations
import json
from collections import defaultdict
import numpy as np
from t25_endogenous_dimension_scan import generate, distances
from t30_relational_compatibility import profile_from_dist

def profiles(adj,R):
    n=len(adj);ds=[distances(adj,u) for u in range(n)]
    return [profile_from_dist(ds[u],R,n) for u in range(n)]

def X(adj,ps,v): return np.asarray([ps[w]-ps[v] for w in adj[v]],float)

def metrics(x):
    if x.size==0:return 0,0.0,[]
    s=np.linalg.svd(x,compute_uv=False);lam=s*s
    rank=int(np.linalg.matrix_rank(x))
    part=float(lam.sum()**2/(lam*lam).sum()) if np.any(lam) else 0.0
    c=(np.cumsum(lam)/lam.sum()).tolist() if lam.sum()>0 else []
    return rank,part,[float(z) for z in c]

def row_basis(x):
    if x.size==0:return np.empty((0,x.shape[1] if x.ndim==2 else 0))
    _,s,vh=np.linalg.svd(x,full_matrices=False)
    r=int(np.linalg.matrix_rank(x))
    return vh[:r]

def overlap(x1,x2restricted):
    q1=row_basis(x1);q2=row_basis(x2restricted)
    if len(q1)==0 or len(q2)==0:return None
    sv=np.linalg.svd(q1@q2.T,compute_uv=False)
    return {"common_rank":min(len(q1),len(q2)),
      "mean_principal_cosine":float(np.mean(sv)),
      "min_principal_cosine":float(np.min(sv))}

def audit(n,seed):
    adj=generate(n,seed)
    P={R:profiles(adj,R) for R in (1,2,4,8)}
    out=[]
    for R in (1,2,4,8):
      rows=[];bydeg=defaultdict(list)
      for v in range(n):
        r,p,c=metrics(X(adj,P[R],v))
        rec={"degree":len(adj[v]),"rank":r,"participation_rank":p,"concentration":c}
        rows.append(rec);bydeg[len(adj[v])].append(rec)
      out.append({"R":R,
        "mean_rank":float(np.mean([z["rank"] for z in rows])),
        "mean_participation_rank":float(np.mean([z["participation_rank"] for z in rows])),
        "degree_conditioned":{str(d):{"count":len(z),
          "mean_rank":float(np.mean([q["rank"] for q in z])),
          "mean_participation_rank":float(np.mean([q["participation_rank"] for q in z]))}
          for d,z in sorted(bydeg.items())}})
    overlaps=[]
    for R,R2 in ((1,2),(2,4),(4,8)):
      vals=[]
      for v in range(n):
        a=X(adj,P[R],v)
        b=X(adj,P[R2],v)[:,:R+1]
        o=overlap(a,b)
        if o:vals.append(o)
      overlaps.append({"transition":f"{R}->{R2}",
        "mean_of_mean_cosine":float(np.mean([z["mean_principal_cosine"] for z in vals])),
        "mean_of_min_cosine":float(np.mean([z["min_principal_cosine"] for z in vals]))})
    return {"n":n,"seed":seed,"scales":out,"overlaps":overlaps}

def run():
    return {"protocol":"T34 frozen",
      "runs":[audit(n,s) for n in (128,256,512) for s in (11,23,47)],
      "guard":"No target rank, target dimension, graph dynamics or physical tangent-space claim."}

if __name__=="__main__":print(json.dumps(run(),indent=2))
