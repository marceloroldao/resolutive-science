"""T29 diagnostics for frozen D28-A. No model changes."""
from __future__ import annotations
import json
from collections import Counter
from t25_endogenous_dimension_scan import generate, distances
from t28_multiscale_relational_dynamics import signature, step, edges

def exact_diameter(adj):
    return max(max(distances(adj,u)) for u in range(len(adj)))

def counters(adj,R):
    n=len(adj); sig=[signature(adj,u,R) for u in range(n)]
    nonedges=band=eq_global=eq_band=0
    classes={}
    ecc=[]
    for u in range(n):
        du=distances(adj,u); ecc.append(max(du))
        for v in range(u+1,n):
            if v in adj[u]: continue
            nonedges+=1
            same=sig[u]==sig[v]
            if same: eq_global+=1
            inband=R < du[v] <= 2*R
            if inband:
                band+=1
                if same:
                    eq_band+=1
                    key=(sig[u],tuple(sorted((len(adj[u]),len(adj[v])))))
                    classes.setdefault(key,0);classes[key]+=1
    unique=sum(1 for x in classes.values() if x==1)
    unresolved=sum(x for x in classes.values() if x>1)
    return {"diameter":max(ecc),"vertices_ecc_le_2R":sum(x<=2*R for x in ecc),
            "nonedge_pairs":nonedges,"distance_band_pairs":band,
            "equal_signature_pairs_global":eq_global,
            "equal_signature_pairs_in_band":eq_band,
            "structural_classes":len(classes),"unique_structural_classes":unique,
            "unresolved_candidate_pairs":unresolved}

def run(rounds=5):
    rows=[]
    for n in (128,256,512):
      for seed in (11,23,47):
        parent=generate(n,seed); seq=[set(x) for x in parent]; rr=[]
        for s in range(rounds):
            R=2**s
            before=counters(seq,R)
            new,added,_=step(seq,R)
            parent_c=counters(parent,R)
            _,parent_added,_=step(parent,R)
            rr.append({"round":s,"R":R,"sequential":before,
                       "sequential_accepted":len(added),
                       "parent_counterfactual":parent_c,
                       "parent_counterfactual_accepted":len(parent_added),
                       "feedback_suppression":len(parent_added)>0 and len(added)==0})
            seq=new
        rows.append({"n":n,"seed":seed,"rounds":rr})
    return {"protocol":"T29 frozen diagnostic","rows":rows,
            "guard":"counterfactual is diagnostic only; D28-A is unchanged."}

if __name__=="__main__":print(json.dumps(run(),indent=2))
