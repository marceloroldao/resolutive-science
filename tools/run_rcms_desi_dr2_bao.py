#!/usr/bin/env python3
"""Protocol 01 DESI DR2 BAO-only comparison using only the Python stdlib.

The BAO scale q=c/(H0*r_d) is profiled analytically. The reference model
fits Omega_m; RCMS fits Omega_m and the single extra A_R shape parameter.
"""
from __future__ import annotations

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEAN = ROOT / "data/rcms/desi_dr2_bao_all_mean.txt"
COV = ROOT / "data/rcms/desi_dr2_bao_all_cov.txt"
OMEGA_BOUNDS = (0.05, 0.60)
AR_BOUNDS = (-5.0, 5.0)
AR_STEP = 0.01


def load_data():
    rows=[]
    for line in MEAN.read_text().splitlines():
        if not line or line.startswith('#'): continue
        z,val,kind=line.split()
        rows.append((float(z),float(val),kind))
    cov=[[float(x) for x in line.split()] for line in COV.read_text().splitlines() if line.strip()]
    if len(rows)!=13 or len(cov)!=13 or any(len(r)!=13 for r in cov):
        raise RuntimeError("DESI DR2 BAO frozen dimensions are not 13 / 13x13")
    return rows,cov


def invert(a):
    n=len(a); m=[row[:] + [1.0 if i==j else 0.0 for j in range(n)] for i,row in enumerate(a)]
    for col in range(n):
        p=max(range(col,n), key=lambda r: abs(m[r][col]))
        if abs(m[p][col])<1e-15: raise RuntimeError("singular covariance")
        m[col],m[p]=m[p],m[col]
        q=m[col][col]; m[col]=[x/q for x in m[col]]
        for r in range(n):
            if r==col: continue
            f=m[r][col]
            if f: m[r]=[x-f*y for x,y in zip(m[r],m[col])]
    return [row[n:] for row in m]


def mv(a,x): return [sum(v*y for v,y in zip(row,x)) for row in a]
def dot(x,y): return sum(a*b for a,b in zip(x,y))


def simpson(f,b,n=200):
    if n%2: n+=1
    h=b/n; s=f(0.0)+f(b)
    for i in range(1,n): s+=(4 if i%2 else 2)*f(i*h)
    return s*h/3.0


def shapes(rows,omega_m,a_r):
    def e(z):
        e2=omega_m*(1+z)**3 + 1-omega_m + a_r*math.log1p(z)
        if e2<=0: raise ValueError
        return math.sqrt(e2)
    cache={}
    out=[]
    for z,_,kind in rows:
        if z not in cache: cache[z]=simpson(lambda x:1/e(x),z)
        dm=cache[z]; dh=1/e(z)
        if kind=="DM_over_rs": out.append(dm)
        elif kind=="DH_over_rs": out.append(dh)
        elif kind=="DV_over_rs": out.append((z*dm*dm*dh)**(1/3))
        else: raise RuntimeError(f"unknown BAO observable {kind}")
    return out


def objective(rows,ci,omega_m,a_r):
    try: s=shapes(rows,omega_m,a_r)
    except ValueError: return float('inf'), float('nan')
    d=[r[1] for r in rows]
    cis=mv(ci,s); cid=mv(ci,d)
    q=dot(s,cid)/dot(s,cis)
    residual=[x-q*y for x,y in zip(d,s)]
    chi2=dot(residual,mv(ci,residual))
    return chi2,q


def golden_min(fn,lo,hi,tol=1e-8):
    g=(math.sqrt(5)-1)/2
    c=hi-g*(hi-lo); d=lo+g*(hi-lo); fc=fn(c); fd=fn(d)
    while hi-lo>tol:
        if fc<fd: hi,d,fd=d,c,fc; c=hi-g*(hi-lo); fc=fn(c)
        else: lo,c,fc=c,d,fd; d=lo+g*(hi-lo); fd=fn(d)
    x=(lo+hi)/2
    return x,fn(x)


def profile_ar(rows,ci,a_r):
    om,chi=golden_min(lambda x:objective(rows,ci,x,a_r)[0],*OMEGA_BOUNDS)
    chi,q=objective(rows,ci,om,a_r)
    return chi,om,q


def main():
    rows,cov=load_data(); ci=invert(cov)
    # symmetry / inverse checks
    if max(abs(cov[i][j]-cov[j][i]) for i in range(13) for j in range(13))>1e-12:
        raise RuntimeError("covariance is not symmetric")
    eye=max(abs(sum(cov[i][k]*ci[k][j] for k in range(13))-(1.0 if i==j else 0.0)) for i in range(13) for j in range(13))
    if eye>1e-8: raise RuntimeError("covariance inverse check failed")

    chi0,om0,q0=profile_ar(rows,ci,0.0)
    best=(float('inf'),None,None,None)
    profiles=[]
    n=int(round((AR_BOUNDS[1]-AR_BOUNDS[0])/AR_STEP))+1
    for i in range(n):
        ar=AR_BOUNDS[0]+i*AR_STEP
        chi,om,q=profile_ar(rows,ci,ar)
        profiles.append((ar,chi,om,q))
        if chi<best[0]: best=(chi,ar,om,q)
    chi1,ar1,om1,q1=best
    target=chi1+1.0
    inside=[x for x in profiles if x[1]<=target]
    ar_lo,ar_hi=inside[0][0],inside[-1][0]
    nobs=len(rows)
    # effective identifiable parameters: q, Omega_m; RCMS adds A_R
    aic0=chi0+2*2; aic1=chi1+2*3
    bic0=chi0+2*math.log(nobs); bic1=chi1+3*math.log(nobs)

    print("RCMS Protocol 01 — DESI DR2 BAO-only")
    print(f"N = {nobs}")
    print(f"LCDM: chi2={chi0:.6f}, Omega_m={om0:.6f}, q=c/(H0*r_d)={q0:.6f}")
    print(f"RCMS: chi2={chi1:.6f}, Omega_m={om1:.6f}, A_R={ar1:.3f}, q={q1:.6f}")
    print(f"A_R profile Delta-chi2<=1 interval: [{ar_lo:.3f}, {ar_hi:.3f}]")
    print(f"Delta chi2 (LCDM-RCMS) = {chi0-chi1:.6f}")
    print(f"Delta AIC (LCDM-RCMS) = {aic0-aic1:.6f}")
    print(f"Delta BIC (LCDM-RCMS) = {bic0-bic1:.6f}")
    boundary=(abs(om1-OMEGA_BOUNDS[0])<1e-4 or abs(om1-OMEGA_BOUNDS[1])<1e-4 or abs(ar1-AR_BOUNDS[0])<AR_STEP or abs(ar1-AR_BOUNDS[1])<AR_STEP)
    print(f"Boundary contact: {boundary}")
    if aic0-aic1>0 and bic0-bic1>0 and not (ar_lo<=0<=ar_hi):
        print("Classification: RCMS SCREENING SIGNAL (BAO-only stage; not validation)")
    elif aic0-aic1<0 and bic0-bic1<0:
        print("Classification: NO PREFERENCE / reference penalized criteria favored")
    else:
        print("Classification: NO PREFERENCE / mixed criteria")

if __name__=="__main__": main()
