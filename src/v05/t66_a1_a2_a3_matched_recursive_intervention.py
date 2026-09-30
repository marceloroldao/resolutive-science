"""T66 final A1+A2+A3 matched recursive-order intervention."""
from __future__ import annotations
import hashlib,json,math,random,statistics
from t25_endogenous_dimension_scan import generate
from t47_degree_preserving_recursive_order_null import extract_parent,build_adj
from t39_higher_order_topology_source import m3_m7

N=2048; SEEDS=(1301,1327,1361); NULLS=99; BURN_IN=2000; THIN=200
STAGE_A_CEILING=1_000_000; STAGE_B_CEILING=7_500_000; OVERLAP_MAX=0.90

def moments(parent):
    n=len(parent); rs=[(parent[v]+1.0)/(v+1.0) for v in range(1,n)]
    return tuple(math.fsum(r**p for r in rs)/(n-1) for p in (1,2,3))

def child_quota(parent):
    q=[0]*len(parent)
    for v in range(1,len(parent)): q[parent[v]]+=1
    return q

def digest_parent(parent):
    return hashlib.blake2b(",".join(map(str,parent[1:])).encode("ascii"),digest_size=16).hexdigest()

def overlap(parent,original):
    return sum(parent[v]==original[v] for v in range(1,len(parent)))/(len(parent)-1)

def quantile(values,q):
    s=sorted(values); x=(len(s)-1)*q; lo=int(math.floor(x)); hi=int(math.ceil(x))
    if lo==hi:return s[lo]
    w=x-lo; return s[lo]*(1-w)+s[hi]*w

def summary(values):
    return {"mean":statistics.fmean(values),"sd":statistics.pstdev(values),
            "q025":quantile(values,.025),"median":quantile(values,.5),
            "q975":quantile(values,.975),"min":min(values),"max":max(values)}

def classify(parent_value,null_values):
    s=summary(null_values)
    c="low" if parent_value<s["q025"] else ("high" if parent_value>s["q975"] else "inside")
    return {"parent":parent_value,**{f"null_{k}":v for k,v in s.items()},
            "classification":c,
            "parent_minus_null_sd":((parent_value-s["mean"])/s["sd"] if s["sd"]>0 else None)}

def propose(current,rng):
    a,b=rng.sample(range(1,len(current)),2); x,y=current[a],current[b]
    if x==y or not (y<a and x<b): return None
    return a,b,x,y

def delta_moments(n,a,b,x,y):
    ro=((x+1.0)/(a+1.0),(y+1.0)/(b+1.0))
    rn=((y+1.0)/(a+1.0),(x+1.0)/(b+1.0))
    return tuple((sum(r**p for r in rn)-sum(r**p for r in ro))/(n-1) for p in (1,2,3))

def stage_a(original,seed):
    current=list(original); quota=child_quota(original); rng=random.Random(25000009*N+25013*seed)
    accepted=proposals=0; vals=[[],[],[]]; ovs=[]; seen=set()
    while proposals<STAGE_A_CEILING and len(vals[0])<NULLS:
        proposals+=1; mv=propose(current,rng)
        if mv is None: continue
        a,b,x,y=mv; current[a],current[b]=y,x; accepted+=1
        if accepted<=BURN_IN or (accepted-BURN_IN)%THIN: continue
        ov=overlap(current,original)
        if ov>OVERLAP_MAX: continue
        d=digest_parent(current)
        if d in seen: continue
        if child_quota(current)!=quota or not all(0<=current[v]<v for v in range(1,N)):
            raise RuntimeError("Stage A invariant failure")
        mm=moments(current); seen.add(d)
        for i,val in enumerate(mm): vals[i].append(val)
        ovs.append(ov)
    return {"feasible":len(vals[0])==NULLS,"proposals":proposals,"accepted":accepted,"vals":vals,"overlaps":ovs}

def stage_b(original,seed,limits):
    current=list(original); quota=child_quota(original); target=moments(original); cur=list(target)
    rng=random.Random(27000059*N+27011*seed)
    accepted=proposals=0; stored=[]; vals=[[],[],[]]; ovs=[]; seen=set()
    while proposals<STAGE_B_CEILING and len(stored)<NULLS:
        proposals+=1; mv=propose(current,rng)
        if mv is None: continue
        a,b,x,y=mv; dm=delta_moments(N,a,b,x,y); cand=[cur[i]+dm[i] for i in range(3)]
        if any(abs(cand[i]-target[i])>limits[i] for i in range(3)): continue
        current[a],current[b]=y,x; cur=cand; accepted+=1
        if accepted<=BURN_IN or (accepted-BURN_IN)%THIN: continue
        ov=overlap(current,original)
        if ov>OVERLAP_MAX: continue
        d=digest_parent(current)
        if d in seen: continue
        if child_quota(current)!=quota or not all(0<=current[v]<v for v in range(1,N)):
            raise RuntimeError("Stage B invariant failure")
        exact=moments(current)
        if any(abs(exact[i]-target[i])>limits[i]+1e-12 for i in range(3)):
            raise RuntimeError("Stage B moment accounting failure")
        seen.add(d); stored.append(list(current)); ovs.append(ov)
        for i,val in enumerate(exact): vals[i].append(val)
    match=bool(len(stored)==NULLS and all(
        all(abs(x-target[i])<=limits[i]+1e-12 for x in vals[i]) and min(vals[i])<=target[i]<=max(vals[i])
        for i in range(3)
    )) if stored else False
    return {"feasible":len(stored)==NULLS,"match":match,"proposals":proposals,"accepted":accepted,
            "stored":stored,"vals":vals,"overlaps":ovs}

def run_parent(seed):
    parent_adj=generate(N,seed); original=extract_parent(parent_adj); target=moments(original)
    sa=stage_a(original,seed)
    row={"seed":seed,"n":N,"parent_A1":target[0],"parent_A2":target[1],"parent_A3":target[2],
         "stage_a_proposals":sa["proposals"],"stage_a_accepted":sa["accepted"],
         "stage_a_stored":len(sa["vals"][0]),"stage_a_feasible":sa["feasible"]}
    if not sa["feasible"]: return row
    sums=[summary(sa["vals"][i]) for i in range(3)]; limits=[.25*s["sd"] for s in sums]
    row.update({"stage_a_A1":sums[0],"stage_a_A2":sums[1],"stage_a_A3":sums[2],
                "delta_A1":limits[0],"delta_A2":limits[1],"delta_A3":limits[2]})
    if not all(x>0 for x in limits):
        row["stage_b_feasible"]=False; return row
    sb=stage_b(original,seed,limits)
    row.update({"stage_b_proposals":sb["proposals"],"stage_b_accepted":sb["accepted"],
                "stage_b_stored":len(sb["stored"]),"stage_b_feasible":sb["feasible"],
                "stage_b_joint_match":sb["match"],
                "stage_b_A1":summary(sb["vals"][0]) if sb["vals"][0] else None,
                "stage_b_A2":summary(sb["vals"][1]) if sb["vals"][1] else None,
                "stage_b_A3":summary(sb["vals"][2]) if sb["vals"][2] else None,
                "stage_b_overlap":summary(sb["overlaps"]) if sb["overlaps"] else None})
    if not (sb["feasible"] and sb["match"]):
        row["heldout_evaluated"]=False; return row
    pm3,pm7=m3_m7(parent_adj); nm3=[]; nm7=[]
    for ps in sb["stored"]:
        m3,m7=m3_m7(build_adj(ps)); nm3.append(m3); nm7.append(m7)
    row["heldout_evaluated"]=True; row["M3"]=classify(pm3,nm3); row["M7"]=classify(pm7,nm7)
    return row

def run():
    rows=[run_parent(seed) for seed in SEEDS]
    feasible=all(r.get("stage_a_feasible",False) and r.get("stage_b_feasible",False) and r.get("stage_b_joint_match",False) for r in rows)
    accounting=feasible and all(r["M3"]["classification"]=="inside" and r["M7"]["classification"]=="inside" for r in rows)
    residual=feasible and all(r["M3"]["classification"]=="low" and r["M7"]["classification"]=="low" for r in rows)
    outcome="A1_A2_A3_ACCOUNTING_IDENTIFIED" if accounting else ("LOW_LOW_RESIDUAL_AFTER_A1_A2_A3" if residual else ("MIXED" if feasible else "INFEASIBLE"))
    return {"protocol":"T66 frozen","status":"FINAL_MOMENT_HIERARCHY_INTERVENTION","N":N,"seeds":list(SEEDS),
            "rows":rows,"T66_FEASIBILITY":feasible,"T66_ACCOUNTING":accounting,"T66_RESIDUAL":residual,
            "T66_OUTCOME":outcome,"T66_MOMENT_HIERARCHY_STOP":True,
            "physical_mapping":"NONE","new_physics":"NOT_ESTABLISHED"}

if __name__=="__main__":
    result=run(); print(json.dumps(result,indent=2))
    if not result["T66_FEASIBILITY"]: raise SystemExit(1)
