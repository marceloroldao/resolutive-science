#!/usr/bin/env python3
"""Preregistered RCMS Protocol 02 T6 residual-localization diagnostic."""
from __future__ import annotations
import importlib.util, sys
from pathlib import Path
import numpy as np
from scipy.linalg import cho_solve

ROOT=Path(__file__).resolve().parents[1]; TOOLS=ROOT/'tools'
BINS=((0.0,0.3),(0.3,0.6),(0.6,1.0),(1.0,1.5),(1.5,float('inf')))

def load(name,path):
    s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m
combo=load('p02t6_combo',TOOLS/'run_rcms_protocol01_remaining_combos.py'); hz=combo.hz; sn=combo.sn; bao=combo.bao

def bin_label(lo,hi): return f"[{lo:.1f},{'inf' if not np.isfinite(hi) else f'{hi:.1f}'})"
def summarize(name,z,delta):
    print(f"[{name}_REDSHIFT_BINS]")
    pos=sum(max(0.0,float(x)) for x in delta)
    rows=[]
    for lo,hi in BINS:
        mask=(z>=lo)&(z<hi); val=float(np.sum(delta[mask])); rows.append((lo,hi,int(mask.sum()),val))
        print(f"bin={bin_label(lo,hi)} n={int(mask.sum())} delta_chi2={val:.6f}")
    best=max(rows,key=lambda r:r[3])
    frac=(best[3]/pos) if pos>0 else 0.0
    print(f"largest_positive_bin={bin_label(best[0],best[1])} gain={best[3]:.6f} fraction_of_positive_gain={frac:.6f}")
    print(); return rows

def h_contrib(h_like,om,ar,h0):
    z,h,inv=h_like; shape=hz.model_shape(z,om,ar); r=np.asarray(h)-h0*np.asarray(shape); w=np.asarray(inv)@r; return np.asarray(z),r*w

def sn_contrib(like,om,ar):
    th=sn.pantheon_lumdists(like.zcmb,like.zhel,om,ar); raw=like.mag-th
    cinv=cho_solve(like.factor,raw,check_finite=False); b=float(like.ones@cinv/like.ones_cinv_ones)
    r=raw-b; w=cho_solve(like.factor,r,check_finite=False); return np.asarray(like.zcmb),r*w

def bao_contrib(b_like,om,ar,q):
    rows,inv=b_like; s=np.asarray(bao.shapes(rows,om,ar)); d=np.asarray([r[1] for r in rows]); r=d-q*s; w=np.asarray(inv)@r
    return np.asarray([r0[0] for r0 in rows]),r*w

def main():
    h_like,s_like,b_like,_=combo.load_likelihoods(); C=combo.Combo('HZ_SN_BAO',True,True,True,1618,3)
    ref_chi,ref_om,ref_parts,ref_nuis,_=combo.profile_omega(0.0,C,h_like,s_like,b_like)
    rc_chi,rc_om,ar,rc_parts,rc_nuis,_=combo.fit_rcms(C,h_like,s_like,b_like)
    print('RCMS Protocol 02 — T6 residual localization')
    print(f"LCDM chi2={ref_chi:.6f} Omega_m={ref_om:.6f} H0={ref_nuis['H0']:.6f} q={ref_nuis['q']:.6f}")
    print(f"RCMS chi2={rc_chi:.6f} Omega_m={rc_om:.6f} A_R={ar:.6f} H0={rc_nuis['H0']:.6f} q={rc_nuis['q']:.6f}")
    print(f"total_delta_chi2={ref_chi-rc_chi:.6f}\n")
    all_delta=[]
    for name,fn in (
        ('HZ',lambda om,a,n:h_contrib(h_like,om,a,n['H0'])),
        ('SN',lambda om,a,n:sn_contrib(s_like,om,a)),
        ('BAO',lambda om,a,n:bao_contrib(b_like,om,a,n['q'])),):
        z0,c0=fn(ref_om,0.0,ref_nuis); z1,c1=fn(rc_om,ar,rc_nuis)
        if not np.allclose(z0,z1): raise RuntimeError('redshift mismatch')
        d=c0-c1; all_delta.extend(d.tolist())
        print(f"[{name}_PROBE] chi2_LCDM={float(c0.sum()):.6f} chi2_RCMS={float(c1.sum()):.6f} delta_chi2={float(d.sum()):.6f}")
        summarize(name,z0,d)
    recovered=float(np.sum(all_delta)); target=ref_chi-rc_chi
    print(f"additive_recovered_delta_chi2={recovered:.6f}")
    print(f"closure_error={abs(recovered-target):.3e}")
    if abs(recovered-target)>2e-5: raise SystemExit('T6 additive decomposition failed closure')

if __name__=='__main__': main()
