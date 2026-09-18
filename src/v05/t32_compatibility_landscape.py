"""T32 diagnostics for T30/T31 landscape. No new dynamics."""
from __future__ import annotations
import json
from collections import Counter
import numpy as np
from t25_endogenous_dimension_scan import generate, distances
from t30_relational_compatibility import profile_from_dist

def rankdata(a):
    order=np.argsort(a); ranks=np.empty(len(a),float); i=0
    while i<len(a):
        j=i
        while j+1<len(a) and a[order[j+1]]==a[order[i]]:j+=1
        r=(i+j)/2+1
        for k in range(i,j+1):ranks[order[k]]=r
        i=j+1
    return ranks

def corr(x,y):
    x=np.asarray(x,float);y=np.asarray(y,float)
    p=float(np.corrcoef(x,y)[0,1]) if np.std(x)>0 and np.std(y)>0 else None
    rx,ry=rankdata(x),rankdata(y)
    s=float(np.corrcoef(rx,ry)[0,1]) if np.std(rx)>0 and np.std(ry)>0 else None
    return p,s

def audit(n,seed,R):
    adj=generate(n,seed); ds=[distances(adj,u) for u in range(n)]
    counts=[]
    for u in range(n):
        shell=[0]*(R+1)
        for d in ds[u]:
            if 0<=d<=R:shell[d]+=1
        c=[];z=0
        for x in shell:z+=x;c.append(z)
        counts.append(tuple(c))
    mult=Counter(counts)
    alias_nodes=sum(v for v in mult.values() if v>1)
    collision_pairs=sum(v*(v-1)//2 for v in mult.values() if v>1)
    total_pairs=n*(n-1)//2
    ps=[profile_from_dist(ds[u],R,n) for u in range(n)]
    gd=[];pd=[]
    for u in range(n):
      for v in range(u+1,n):
        gd.append(ds[u][v]);pd.append(float(np.sqrt(np.mean((ps[u]-ps[v])**2))))
    pear,spear=corr(gd,pd)
    ref_alias=0; minima=[]; barriers=[]; unique_traps=0; failed=0
    for a in range(n):
        phi=[float(np.sqrt(np.mean((ps[a]-p)**2))) for p in ps]
        if any(v!=a and counts[v]==counts[a] for v in range(n)):ref_alias+=1
        mins=[v for v in range(n) if v!=a and all(phi[v]<phi[w] for w in adj[v])]
        minima.append(len(mins))
        for v in mins:
            failed+=1
            if mult[counts[v]]==1: unique_traps+=1
            barriers.append(min(max(0.0,phi[w]-phi[v]) for w in adj[v]))
    return {"n":n,"seed":seed,"R":R,"unique_profiles":len(mult),
      "max_profile_multiplicity":max(mult.values()),"aliased_node_fraction":alias_nodes/n,
      "exact_collision_pair_fraction":collision_pairs/total_pairs,
      "reference_alias_fraction":ref_alias/n,"pearson_graphD_profileD":pear,
      "spearman_graphD_profileD":spear,"mean_strict_minima":float(np.mean(minima)),
      "mean_strict_minima_density":float(np.mean(minima))/n,
      "strict_minima_unique_profile_fraction":unique_traps/failed if failed else None,
      "positive_barrier_fraction":float(np.mean(np.asarray(barriers)>0)) if barriers else None,
      "mean_barrier":float(np.mean(barriers)) if barriers else None}

def run():
    rows=[audit(n,s,R) for n in (128,256,512) for s in (11,23,47) for R in (1,2,4,8)]
    return {"protocol":"T32 frozen","rows":rows,
      "guard":"Landscape diagnosis only; no smoothing, threshold, energy or dynamics."}

if __name__=="__main__":print(json.dumps(run(),indent=2))
