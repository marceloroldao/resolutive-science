"""T68 joint pre-attachment degree / parent-age covariance null test.

M3/M7 are intentionally absent.
"""
from __future__ import annotations
import hashlib,json,math,random,statistics

from t25_endogenous_dimension_scan import generate
from t47_degree_preserving_recursive_order_null import extract_parent

N=4096
SEEDS=(1409,1427,1451)
NULLS=999
BURN_IN=5000
THIN=500
PROPOSAL_CEILING=5_000_000
OVERLAP_MAX=0.25
THEORY=-0.060540682885
THEORY_TOL=0.006


def child_quota(parent):
    q=[0]*len(parent)
    for v in range(1,len(parent)): q[parent[v]]+=1
    return q


def digest_parent(parent):
    return hashlib.blake2b(",".join(map(str,parent[1:])).encode("ascii"),digest_size=16).hexdigest()


def overlap(parent,original):
    return sum(parent[v]==original[v] for v in range(1,len(parent)))/(len(parent)-1)


def joint_stats(parent):
    n=len(parent)
    deg=[0]*n
    deg[0]=1; deg[1]=1
    sum_k=sum_r=sum_kr=0.0
    counts={}
    sum_r_by_k={}
    events=0
    for v in range(2,n):
        u=parent[v]
        if not (0<=u<v):
            raise RuntimeError("nonrecursive parent")
        k=deg[u]
        if k<=0:
            raise RuntimeError("parent has invalid current degree")
        r=(u+1.0)/(v+1.0)
        sum_k+=k; sum_r+=r; sum_kr+=k*r; events+=1
        counts[k]=counts.get(k,0)+1
        sum_r_by_k[k]=sum_r_by_k.get(k,0.0)+r
        deg[u]+=1
        deg[v]=1
    ek=sum_k/events
    er=sum_r/events
    ekr=sum_kr/events
    cov=ekr-ek*er
    conditional={str(k):sum_r_by_k[k]/counts[k] for k in sorted(counts)}
    histogram={str(k):counts[k] for k in sorted(counts)}
    return {
        "events":events,
        "E_K":ek,
        "E_R":er,
        "E_KR":ekr,
        "C_KR":cov,
        "conditional_E_R_given_K":conditional,
        "attachment_degree_counts":histogram,
        "reconstructed_final_degrees":deg,
    }


def quantile(values,q):
    s=sorted(values)
    x=(len(s)-1)*q; lo=int(math.floor(x)); hi=int(math.ceil(x))
    if lo==hi:return s[lo]
    w=x-lo
    return s[lo]*(1-w)+s[hi]*w


def summary(values):
    return {"mean":statistics.fmean(values),"sd":statistics.pstdev(values),
            "q005":quantile(values,.005),"median":quantile(values,.5),
            "q995":quantile(values,.995),"min":min(values),"max":max(values)}


def run_parent(seed):
    adj=generate(N,seed)
    original=extract_parent(adj)
    original_quota=child_quota(original)
    parent_stats=joint_stats(original)
    final_degrees=[len(ns) for ns in adj]
    if parent_stats["reconstructed_final_degrees"]!=final_degrees:
        raise RuntimeError("parent degree reconstruction mismatch")

    current=list(original)
    rng=random.Random(29000027*N+29009*seed)
    accepted=proposals=0
    covs=[]; ovs=[]; seen=set()
    histogram_ref=parent_stats["attachment_degree_counts"]

    while proposals<PROPOSAL_CEILING and len(covs)<NULLS:
        proposals+=1
        a,b=rng.sample(range(1,N),2)
        x,y=current[a],current[b]
        if x==y or not (y<a and x<b):
            continue
        current[a],current[b]=y,x
        accepted+=1

        if accepted<=BURN_IN or (accepted-BURN_IN)%THIN:
            continue
        ov=overlap(current,original)
        if ov>OVERLAP_MAX:
            continue
        d=digest_parent(current)
        if d in seen:
            continue
        if child_quota(current)!=original_quota:
            raise RuntimeError("quota invariant failure")

        st=joint_stats(current)
        if st["reconstructed_final_degrees"]!=final_degrees:
            raise RuntimeError("null final-degree mismatch")
        if st["attachment_degree_counts"]!=histogram_ref:
            raise RuntimeError("T67 attachment-degree invariant failure")

        seen.add(d)
        covs.append(st["C_KR"])
        ovs.append(ov)

    feasible=len(covs)==NULLS
    s=summary(covs) if covs else None
    theory_gate=abs(parent_stats["C_KR"]-THEORY)<=THEORY_TOL
    directional=bool(s and parent_stats["C_KR"]<s["q005"])
    return {
        "seed":seed,
        "n":N,
        "parent_stats":parent_stats,
        "parent_theory_error":parent_stats["C_KR"]-THEORY,
        "theory_gate":theory_gate,
        "proposals":proposals,
        "accepted_swaps":accepted,
        "stored_nulls":len(covs),
        "null_feasible":feasible,
        "null_C_KR":s,
        "parent_minus_null_sd":(
            (parent_stats["C_KR"]-s["mean"])/s["sd"] if s and s["sd"]>0 else None
        ),
        "overlap":summary(ovs) if ovs else None,
        "directional_gate":directional,
    }


def run():
    rows=[run_parent(seed) for seed in SEEDS]
    feasible=all(r["null_feasible"] for r in rows)
    theory=all(r["theory_gate"] for r in rows)
    identified=all(r["directional_gate"] for r in rows)
    return {
        "protocol":"T68 frozen",
        "status":"JOINT_ATTACHMENT_STATE_PARENT_AGE_TEST",
        "N":N,
        "seeds":list(SEEDS),
        "theoretical_C_KR":THEORY,
        "rows":rows,
        "T68_FEASIBILITY":feasible,
        "T68_ANALYTIC_COVARIANCE":theory,
        "T68_JOINT_ALIGNMENT":bool(feasible and theory and identified),
        "M3_M7_computed":False,
        "physical_mapping":"NONE",
        "new_physics":"NOT_ESTABLISHED",
    }


if __name__=="__main__":
    result=run()
    print(json.dumps(result,indent=2))
    if not result["T68_FEASIBILITY"]:
        raise SystemExit(1)
