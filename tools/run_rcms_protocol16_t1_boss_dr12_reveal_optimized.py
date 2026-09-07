#!/usr/bin/env python3
"""RCMS P16-T1 optimized executor.

Scientifically identical to the frozen P16-T1 runner; only caches the expansion
shape for fixed (Omega_m, A_R) while profiling q.
"""
from __future__ import annotations

import hashlib
import json
import math
import urllib.request
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/rcms_protocol16_t1_boss_dr12_reveal.json"
UPSTREAM = "bb0c1c9009dc76d1391300e169e8df38fd1096db"
BASE = f"https://raw.githubusercontent.com/CobayaSampler/bao_data/{UPSTREAM}"
FILES = {
    "sdss_DR12Consensus_bao.dat": "fc43f1cd9c815bb58b09f4d8d1d272d2c4ec57e05e4893e2121c20dc08f4f862",
    "BAO_consensus_covtot_dM_Hz.txt": "05c04829c8edc117870efe809494593a23de6c35547f8b66760a5250804b65cf",
}
RD_FID = 147.78
C_KMS = 299792.458
OMEGA_BOUNDS = (0.05, 0.60)
A_BOUNDS = (-1.0, 1.0)
Q_BOUNDS = (10.0, 60.0)
A_STEP = 0.005
PRED = (0.121971100, 0.407494649)
T0 = {"Omega_m": 0.364867611, "q": 30.509014587, "chi2": 2.061158601}


def download(name):
    with urllib.request.urlopen(f"{BASE}/{name}", timeout=30) as r:
        b = r.read()
    if hashlib.sha256(b).hexdigest() != FILES[name]:
        raise RuntimeError(f"hash mismatch: {name}")
    return b


def load():
    rows=[]
    for line in download("sdss_DR12Consensus_bao.dat").decode().splitlines():
        if line.strip() and not line.lstrip().startswith('#'):
            z,v,k=line.split(); rows.append((float(z),float(v),k))
    cov=np.loadtxt(download("BAO_consensus_covtot_dM_Hz.txt").decode().splitlines())
    return rows, np.asarray([r[1] for r in rows]), cov, np.linalg.inv(cov)


def simpson_inv_e(z, om, a, n=600):
    if n % 2: n += 1
    h=z/n
    def inv_e(x):
        e2=om*(1+x)**3 + 1-om + a*math.log1p(x)
        if e2 <= 0: raise ValueError
        return 1/math.sqrt(e2)
    s=inv_e(0)+inv_e(z)
    for i in range(1,n): s+=(4 if i%2 else 2)*inv_e(i*h)
    return s*h/3


def shape_components(rows, om, a):
    # pred(q) = q*dm_component + hz_component/q
    ints={}; dm=[]; hz=[]
    for z,_,kind in rows:
        e2=om*(1+z)**3 + 1-om + a*math.log1p(z)
        if e2 <= 0: raise ValueError
        e=math.sqrt(e2)
        if z not in ints:
            ints[z]=simpson_inv_e(z,om,a)
        if kind=="DM_over_rs":
            dm.append(RD_FID*ints[z]); hz.append(0.0)
        elif kind=="bao_Hz_rs":
            dm.append(0.0); hz.append(C_KMS*e/RD_FID)
        else: raise RuntimeError(kind)
    return np.asarray(dm), np.asarray(hz)


def golden(fn,lo,hi,tol=1e-9):
    g=(math.sqrt(5)-1)/2
    c,d=hi-g*(hi-lo),lo+g*(hi-lo); fc,fd=fn(c),fn(d)
    while hi-lo>tol:
        if fc<fd:
            hi,d,fd=d,c,fc; c=hi-g*(hi-lo); fc=fn(c)
        else:
            lo,c,fc=c,d,fd; d=lo+g*(hi-lo); fd=fn(d)
    x=(lo+hi)/2; return x,fn(x)


def profile_q_from_components(data,ci,dm,hz):
    def f(logq):
        q=math.exp(logq)
        r=data-(q*dm+hz/q)
        return float(r@ci@r)
    lq,val=golden(f,math.log(Q_BOUNDS[0]),math.log(Q_BOUNDS[1]))
    return math.exp(lq),val


def profile_om(rows,data,ci,a):
    def f(om):
        try: dm,hz=shape_components(rows,om,a)
        except ValueError: return float('inf')
        return profile_q_from_components(data,ci,dm,hz)[1]
    om,val=golden(f,*OMEGA_BOUNDS)
    dm,hz=shape_components(rows,om,a)
    q,val=profile_q_from_components(data,ci,dm,hz)
    return val,om,q


def main():
    rows,data,cov,ci=load()
    eig=np.linalg.eigvalsh(cov)
    if cov.shape!=(6,6) or np.max(np.abs(cov-cov.T))>1e-10 or eig.min()<=0:
        raise RuntimeError('covariance gate failed')

    chi0,om0,q0=profile_om(rows,data,ci,0.0)
    if abs(chi0-T0['chi2'])>2e-6 or abs(om0-T0['Omega_m'])>2e-6 or abs(q0-T0['q'])>2e-6:
        raise RuntimeError(f"optimized executor failed T0 closure: {(chi0,om0,q0)}")

    grid=[]; best=(float('inf'),None,None,None)
    n=int(round((A_BOUNDS[1]-A_BOUNDS[0])/A_STEP))+1
    for i in range(n):
        a=A_BOUNDS[0]+i*A_STEP
        chi,om,q=profile_om(rows,data,ci,a)
        grid.append((a,chi,om,q))
        if chi<best[0]: best=(chi,a,om,q)
    chi1,a1,om1,q1=best
    target=chi1+1.0
    inside=[x for x in grid if x[1]<=target]
    plo,phi=inside[0][0],inside[-1][0]
    zero_in=plo<=0<=phi
    boundary=(abs(a1-A_BOUNDS[0])<A_STEP or abs(a1-A_BOUNDS[1])<A_STEP or om1<OMEGA_BOUNDS[0]+1e-4 or om1>OMEGA_BOUNDS[1]-1e-4)
    quantitative=PRED[0]<=a1<=PRED[1]
    directional=a1>0
    dchi=chi0-chi1; daic=dchi-2.0; dbic=dchi-math.log(6.0)

    if boundary: classification='OUT_OF_SAMPLE_INVALID'
    elif quantitative and directional: classification='OUT_OF_SAMPLE_QUANTITATIVE_HIT'
    elif a1<0: classification='OUT_OF_SAMPLE_SIGN_FAILURE'
    elif a1>=0 and zero_in and not quantitative: classification='OUT_OF_SAMPLE_NULL_COMPATIBLE'
    else: classification='OUT_OF_SAMPLE_DIRECTIONAL_ONLY'

    payload={
        'protocol':'P16-T1','status':'FINAL','executor':'optimized_shape_cache_equivalent',
        'target':'SDSS-III BOSS DR12 BAO-only consensus','prediction_interval':list(PRED),
        'A_R_bounds':list(A_BOUNDS),'A_R_step':A_STEP,'T0_closure_pass':True,
        'LCDM':{'chi2':chi0,'Omega_m':om0,'q':q0},
        'RCMS':{'chi2':chi1,'Omega_m':om1,'q':q1,'A_R':a1,'A_profile_delta_chi2_1':[plo,phi]},
        'Delta_chi2':dchi,'Delta_AIC':daic,'Delta_BIC':dbic,'zero_in_profile':zero_in,
        'quantitative_prediction_hit':quantitative,'directional_prediction_hit':directional,
        'boundary_contact':boundary,'classification':classification,
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print('RCMS P16-T1 — optimized BOSS DR12 blind reveal')
    print(f'T0_CLOSURE=PASS chi2={chi0:.9f} Omega_m={om0:.9f} q={q0:.9f}')
    print(f'RCMS chi2={chi1:.9f} A_R={a1:.6f} Omega_m={om1:.9f} q={q1:.9f}')
    print(f'PROFILE=[{plo:.6f},{phi:.6f}] ZERO_IN={zero_in}')
    print(f'DELTA_CHI2={dchi:.9f} DELTA_AIC={daic:.9f} DELTA_BIC={dbic:.9f}')
    print(f'QUANTITATIVE_PREDICTION_HIT={quantitative}')
    print(f'DIRECTIONAL_PREDICTION_HIT={directional}')
    print(f'BOUNDARY_CONTACT={boundary}')
    print(f'P16_CLASSIFICATION={classification}')

if __name__=='__main__': main()
