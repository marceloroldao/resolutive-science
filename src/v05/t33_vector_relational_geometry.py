"""T33 vector relational geometry diagnostics. No graph dynamics."""
from __future__ import annotations
import json
import numpy as np
from t25_endogenous_dimension_scan import generate, distances
from t30_relational_compatibility import profile_from_dist

def profiles(adj,R):
    n=len(adj); ds=[distances(adj,u) for u in range(n)]
    return [profile_from_dist(ds[u],R,n) for u in range(n)]

def local_matrix(adj,ps,v):
    return np.asarray([ps[w]-ps[v] for w in adj[v]],float)

def rank_stats(X):
    if X.size==0:return 0,0.0,[]
    s=np.linalg.svd(X,compute_uv=False)
    rank=int(np.linalg.matrix_rank(X))
    q=s*s
    pr=float(q.sum()**2/(q*q).sum()) if np.any(q) else 0.0
    return rank,pr,[float(x) for x in s]

def span_residual(X,t):
    nt=np.linalg.norm(t)
    if nt==0:return 0.0
    if X.size==0:return 1.0
    coef=np.linalg.lstsq(X.T,t,rcond=None)[0]
    return float(np.linalg.norm(t-X.T@coef)/nt)

def nnls_projected_gradient(X,t,iters=400):
    # deterministic nonnegative least squares, diagnostic only
    if X.size==0:return np.zeros(0)
    A=X.T
    alpha=np.zeros(X.shape[0])
    L=float(np.linalg.norm(A,2)**2)
    if L==0:return alpha
    for _ in range(iters):
        alpha=np.maximum(0.0,alpha-(A.T@(A@alpha-t))/L)
    return alpha

def cone_residual(X,t):
    nt=np.linalg.norm(t)
    if nt==0:return 0.0
    if X.size==0:return 1.0
    a=nnls_projected_gradient(X,t)
    return float(np.linalg.norm(t-X.T@a)/nt)

def audit(n,seed,R):
    adj=generate(n,seed); ps=profiles(adj,R)
    ranks=[];prs=[]; span=[];cone=[]
    traps=aligned=0; trap_span=[];trap_cone=[]
    for v in range(n):
        X=local_matrix(adj,ps,v);r,pr,_=rank_stats(X);ranks.append(r);prs.append(pr)
    for a in range(n):
      for v in range(n):
        if v==a:continue
        t=ps[a]-ps[v]; X=local_matrix(adj,ps,v)
        sr=span_residual(X,t);cr=cone_residual(X,t);span.append(sr);cone.append(cr)
        phi_v=float(np.linalg.norm(t))
        phin=[float(np.linalg.norm(ps[a]-ps[w])) for w in adj[v]]
        strict=all(phi_v < x for x in phin)
        if strict:
            traps+=1;trap_span.append(sr);trap_cone.append(cr)
            if any(float(np.dot(ps[w]-ps[v],t))>0 for w in adj[v]):aligned+=1
    return {"n":n,"seed":seed,"R":R,
      "mean_local_rank":float(np.mean(ranks)),"max_local_rank":max(ranks),
      "mean_participation_rank":float(np.mean(prs)),
      "mean_span_residual":float(np.mean(span)),"median_span_residual":float(np.median(span)),
      "mean_cone_residual":float(np.mean(cone)),"median_cone_residual":float(np.median(cone)),
      "scalar_traps":traps,
      "trap_positive_alignment_fraction":aligned/traps if traps else None,
      "trap_median_span_residual":float(np.median(trap_span)) if trap_span else None,
      "trap_median_cone_residual":float(np.median(trap_cone)) if trap_cone else None}

def run():
    rows=[audit(n,s,R) for n in (128,256,512) for s in (11,23,47) for R in (1,2,4,8)]
    return {"protocol":"T33 frozen","rows":rows,
      "guard":"Profile-space vectors are relational diagnostics, not physical tangent vectors or dynamics."}

if __name__=="__main__":print(json.dumps(run(),indent=2))
