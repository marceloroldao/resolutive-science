"""T65 joint A1+A2 matched recursive-order intervention.

A1 and A2 were derived in T62 before this intervention. M3/M7 are held out
until each Stage-B ensemble is frozen.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import statistics

from t25_endogenous_dimension_scan import generate
from t47_degree_preserving_recursive_order_null import extract_parent, build_adj
from t39_higher_order_topology_source import m3_m7

N=2048
SEEDS=(1213,1237,1277)
NULLS=99
BURN_IN=2000
THIN=200
STAGE_A_CEILING=1_000_000
STAGE_B_CEILING=5_000_000
OVERLAP_MAX=0.90


def moments(parent):
    n=len(parent)
    a1=math.fsum((parent[v]+1.0)/(v+1.0) for v in range(1,n))/(n-1)
    a2=math.fsum(((parent[v]+1.0)/(v+1.0))**2 for v in range(1,n))/(n-1)
    return a1,a2


def child_quota(parent):
    q=[0]*len(parent)
    for v in range(1,len(parent)):
        q[parent[v]]+=1
    return q


def digest_parent(parent):
    raw=",".join(map(str,parent[1:])).encode("ascii")
    return hashlib.blake2b(raw,digest_size=16).hexdigest()


def edge_overlap(parent,original):
    return sum(1 for v in range(1,len(parent)) if parent[v]==original[v])/(len(parent)-1)


def quantile(values,q):
    s=sorted(values)
    x=(len(s)-1)*q
    lo=int(math.floor(x)); hi=int(math.ceil(x))
    if lo==hi:return s[lo]
    w=x-lo
    return s[lo]*(1-w)+s[hi]*w


def summary(values):
    return {
        "mean":statistics.fmean(values),
        "sd":statistics.pstdev(values),
        "q025":quantile(values,0.025),
        "median":quantile(values,0.5),
        "q975":quantile(values,0.975),
        "min":min(values),
        "max":max(values),
    }


def classify(parent_value,null_values):
    s=summary(null_values)
    if parent_value<s["q025"]: c="low"
    elif parent_value>s["q975"]: c="high"
    else: c="inside"
    return {
        "parent":parent_value,
        **{f"null_{k}":v for k,v in s.items()},
        "classification":c,
        "parent_minus_null_sd":((parent_value-s["mean"])/s["sd"] if s["sd"]>0 else None),
    }


def propose(current,rng):
    a,b=rng.sample(range(1,len(current)),2)
    x,y=current[a],current[b]
    if x==y:return None
    if not (y<a and x<b):return None
    return a,b,x,y


def delta_moments(n,a,b,x,y):
    ra_old=(x+1.0)/(a+1.0); rb_old=(y+1.0)/(b+1.0)
    ra_new=(y+1.0)/(a+1.0); rb_new=(x+1.0)/(b+1.0)
    d1=(ra_new+rb_new-ra_old-rb_old)/(n-1)
    d2=(ra_new*ra_new+rb_new*rb_new-ra_old*ra_old-rb_old*rb_old)/(n-1)
    return d1,d2


def stage_a(original,seed):
    current=list(original)
    quota=child_quota(original)
    rng=random.Random(21000011*N+21013*seed)
    accepted=proposals=0
    vals1=[]; vals2=[]; overlaps=[]; seen=set()
    while proposals<STAGE_A_CEILING and len(vals1)<NULLS:
        proposals+=1
        mv=propose(current,rng)
        if mv is None: continue
        a,b,x,y=mv
        current[a],current[b]=y,x
        accepted+=1
        if accepted<=BURN_IN or (accepted-BURN_IN)%THIN!=0: continue
        ov=edge_overlap(current,original)
        if ov>OVERLAP_MAX: continue
        d=digest_parent(current)
        if d in seen: continue
        if child_quota(current)!=quota or not all(0<=current[v]<v for v in range(1,N)):
            raise RuntimeError("Stage A invariant failure")
        m1,m2=moments(current)
        seen.add(d); vals1.append(m1); vals2.append(m2); overlaps.append(ov)
    return {
        "feasible":len(vals1)==NULLS,
        "proposals":proposals,
        "accepted":accepted,
        "A1":vals1,
        "A2":vals2,
        "overlaps":overlaps,
    }


def stage_b(original,seed,d1_lim,d2_lim):
    current=list(original)
    quota=child_quota(original)
    target1,target2=moments(original)
    current1,current2=target1,target2
    rng=random.Random(23000033*N+23003*seed)
    accepted=proposals=0
    stored=[]; vals1=[]; vals2=[]; overlaps=[]; seen=set()

    while proposals<STAGE_B_CEILING and len(stored)<NULLS:
        proposals+=1
        mv=propose(current,rng)
        if mv is None: continue
        a,b,x,y=mv
        dm1,dm2=delta_moments(N,a,b,x,y)
        cand1=current1+dm1; cand2=current2+dm2
        if abs(cand1-target1)>d1_lim or abs(cand2-target2)>d2_lim:
            continue

        current[a],current[b]=y,x
        current1,current2=cand1,cand2
        accepted+=1

        if accepted<=BURN_IN or (accepted-BURN_IN)%THIN!=0: continue
        ov=edge_overlap(current,original)
        if ov>OVERLAP_MAX: continue
        d=digest_parent(current)
        if d in seen: continue
        if child_quota(current)!=quota or not all(0<=current[v]<v for v in range(1,N)):
            raise RuntimeError("Stage B invariant failure")

        exact1,exact2=moments(current)
        if abs(exact1-target1)>d1_lim+1e-12 or abs(exact2-target2)>d2_lim+1e-12:
            raise RuntimeError("Stage B moment accounting failure")

        seen.add(d)
        stored.append(list(current))
        vals1.append(exact1); vals2.append(exact2); overlaps.append(ov)

    joint_match=bool(
        len(stored)==NULLS
        and all(abs(x-target1)<=d1_lim+1e-12 for x in vals1)
        and all(abs(x-target2)<=d2_lim+1e-12 for x in vals2)
        and min(vals1)<=target1<=max(vals1)
        and min(vals2)<=target2<=max(vals2)
    ) if stored else False

    return {
        "feasible":len(stored)==NULLS,
        "joint_match":joint_match,
        "proposals":proposals,
        "accepted":accepted,
        "stored":stored,
        "A1":vals1,
        "A2":vals2,
        "overlaps":overlaps,
    }


def run_parent(seed):
    parent_adj=generate(N,seed)
    original=extract_parent(parent_adj)
    p1,p2=moments(original)

    sa=stage_a(original,seed)
    row={
        "seed":seed,"n":N,
        "parent_A1":p1,"parent_A2":p2,
        "stage_a_proposals":sa["proposals"],
        "stage_a_accepted":sa["accepted"],
        "stage_a_stored":len(sa["A1"]),
        "stage_a_feasible":sa["feasible"],
    }
    if not sa["feasible"]: return row

    s1=summary(sa["A1"]); s2=summary(sa["A2"])
    d1=0.25*s1["sd"]; d2=0.25*s2["sd"]
    row.update({"stage_a_A1":s1,"stage_a_A2":s2,"delta_A1":d1,"delta_A2":d2})
    if not (d1>0 and d2>0):
        row["stage_b_feasible"]=False
        return row

    sb=stage_b(original,seed,d1,d2)
    row.update({
        "stage_b_proposals":sb["proposals"],
        "stage_b_accepted":sb["accepted"],
        "stage_b_stored":len(sb["stored"]),
        "stage_b_feasible":sb["feasible"],
        "stage_b_joint_match":sb["joint_match"],
        "stage_b_A1":summary(sb["A1"]) if sb["A1"] else None,
        "stage_b_A2":summary(sb["A2"]) if sb["A2"] else None,
        "stage_b_overlap":summary(sb["overlaps"]) if sb["overlaps"] else None,
    })
    if not (sb["feasible"] and sb["joint_match"]):
        row["heldout_evaluated"]=False
        return row

    parent_m3,parent_m7=m3_m7(parent_adj)
    null_m3=[]; null_m7=[]
    for ps in sb["stored"]:
        adj=build_adj(ps)
        m3,m7=m3_m7(adj)
        null_m3.append(m3); null_m7.append(m7)

    row["heldout_evaluated"]=True
    row["M3"]=classify(parent_m3,null_m3)
    row["M7"]=classify(parent_m7,null_m7)
    return row


def run():
    rows=[run_parent(seed) for seed in SEEDS]
    feasible=all(r.get("stage_a_feasible",False) and r.get("stage_b_feasible",False) and r.get("stage_b_joint_match",False) for r in rows)
    accounting=feasible and all(r["M3"]["classification"]=="inside" and r["M7"]["classification"]=="inside" for r in rows)
    residual=feasible and all(r["M3"]["classification"]=="low" and r["M7"]["classification"]=="low" for r in rows)
    outcome="A1_A2_ACCOUNTING_IDENTIFIED" if accounting else ("LOW_LOW_RESIDUAL_AFTER_A1_A2" if residual else ("MIXED" if feasible else "INFEASIBLE"))
    return {
        "protocol":"T65 frozen",
        "status":"A1_A2_MATCHED_RECURSIVE_INTERVENTION",
        "N":N,
        "seeds":list(SEEDS),
        "rows":rows,
        "T65_FEASIBILITY":feasible,
        "T65_ACCOUNTING":accounting,
        "T65_RESIDUAL":residual,
        "T65_OUTCOME":outcome,
        "physical_mapping":"NONE",
        "new_physics":"NOT_ESTABLISHED",
    }


if __name__=="__main__":
    result=run()
    print(json.dumps(result,indent=2))
    if not result["T65_FEASIBILITY"]:
        raise SystemExit(1)
