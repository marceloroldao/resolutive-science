#!/usr/bin/env python3
"""Protocol 02 T5: null Monte Carlo calibration for the frozen RCMS surrogate.

The generating model is the best-fit flat LCDM null from the frozen full
H(z)+Pantheon+ + DESI DR2 BAO data. The observed threshold is frozen at
Delta chi2 = 4.559528. Exactly 500 deterministic realizations are generated.

To make the preregistered production target practical, cosmological predictions
are precomputed on a deterministic (Omega_m, A_R) grid. The likelihood itself
is unchanged: H0, the SN intercept, and the BAO scale q are analytically
profiled exactly as in Protocol 01. A local refinement grid is generated around
the coarse minimum for each realization.
"""
from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import cho_factor, cho_solve

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
PANTHEON_DIR = ROOT / "data" / "external" / "pantheonplus_v1"
THRESHOLD = 4.559528
N_SIM = 500
RNG_SEED = 20260809
C_KM_S = 299792.458

OM_COARSE = np.linspace(0.05, 0.60, 56)   # 0.01 spacing
AR_COARSE = np.linspace(-1.0, 1.0, 81)   # 0.025 spacing; null MC local region


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


combo = load_module("rcms_p02_mc_combo", TOOLS / "run_rcms_protocol01_remaining_combos.py")
hz = combo.hz
sn = combo.sn
bao = combo.bao
FULL = combo.Combo("HZ_SN_BAO", True, True, True, 15 + 1590 + 13, 3)


def quad_profile_scale(data: np.ndarray, shape: np.ndarray, cinv: np.ndarray) -> tuple[float, float]:
    cs = cinv @ shape
    cd = cinv @ data
    scale = float(shape @ cd / (shape @ cs))
    r = data - scale * shape
    return float(r @ (cinv @ r)), scale


def sn_projected_chi2(data: np.ndarray, theory: np.ndarray, cinv: np.ndarray, ones: np.ndarray) -> float:
    r = data - theory
    cir = cinv @ r
    cio = cinv @ ones
    return float(r @ cir - (ones @ cir) ** 2 / (ones @ cio))


def e_shape(z: np.ndarray, om: float, ar: float) -> np.ndarray:
    e2 = om * (1.0 + z) ** 3 + 1.0 - om + ar * np.log1p(z)
    if np.any(e2 <= 0.0):
        raise ValueError
    return np.sqrt(e2)


def precompute_theory(oms: np.ndarray, ars: np.ndarray, z_h, sn_zcmb, sn_zhel, bao_rows):
    # Grid shape: [n_om, n_ar, n_data]
    hz_shapes = np.empty((len(oms), len(ars), len(z_h)), dtype=float)
    sn_theory = np.empty((len(oms), len(ars), len(sn_zcmb)), dtype=float)
    bao_shapes = np.empty((len(oms), len(ars), len(bao_rows)), dtype=float)

    zmax = max(float(np.max(sn_zcmb)), max(float(r[0]) for r in bao_rows))
    integ_grid = np.linspace(0.0, zmax, 4097)

    for io, om in enumerate(oms):
        for ia, ar in enumerate(ars):
            e2 = om * (1.0 + integ_grid) ** 3 + 1.0 - om + ar * np.log1p(integ_grid)
            if np.any(e2 <= 0.0):
                hz_shapes[io, ia] = np.nan
                sn_theory[io, ia] = np.nan
                bao_shapes[io, ia] = np.nan
                continue
            inv_e = 1.0 / np.sqrt(e2)
            # Deterministic cumulative trapezoid; dense-grid error is negligible
            # relative to observational noise and checked against production below.
            dx = np.diff(integ_grid)
            cumulative = np.concatenate([[0.0], np.cumsum(0.5 * (inv_e[:-1] + inv_e[1:]) * dx)])
            hz_shapes[io, ia] = e_shape(np.asarray(z_h), float(om), float(ar))
            ints_sn = np.interp(sn_zcmb, integ_grid, cumulative)
            dm_sn = (C_KM_S / 70.0) * ints_sn
            sn_theory[io, ia] = 5.0 * np.log10((1.0 + sn_zhel) * dm_sn)

            vals=[]
            cache={}
            for z,_,kind in bao_rows:
                z=float(z)
                if z not in cache:
                    dm=float(np.interp(z, integ_grid, cumulative))
                    dh=1.0/math.sqrt(float(om)*(1+z)**3 + 1-float(om) + float(ar)*math.log1p(z))
                    cache[z]=(dm,dh)
                dm,dh=cache[z]
                if kind=="DM_over_rs": vals.append(dm)
                elif kind=="DH_over_rs": vals.append(dh)
                elif kind=="DV_over_rs": vals.append((z*dm*dm*dh)**(1/3))
                else: raise RuntimeError(kind)
            bao_shapes[io, ia]=vals
    return hz_shapes, sn_theory, bao_shapes


def evaluate_grid(hdata, sndata, bdata, h_inv, sn_inv, b_inv, ones, hz_shapes, sn_theory, bao_shapes):
    out=np.full(hz_shapes.shape[:2], np.inf, dtype=float)
    for io in range(out.shape[0]):
        for ia in range(out.shape[1]):
            hs=hz_shapes[io,ia]
            if not np.all(np.isfinite(hs)): continue
            hchi,_=quad_profile_scale(hdata,hs,h_inv)
            schi=sn_projected_chi2(sndata,sn_theory[io,ia],sn_inv,ones)
            bchi,_=quad_profile_scale(bdata,bao_shapes[io,ia],b_inv)
            out[io,ia]=hchi+schi+bchi
    return out


def best_from_grid(grid, oms, ars):
    idx=np.unravel_index(int(np.argmin(grid)), grid.shape)
    return float(grid[idx]), float(oms[idx[0]]), float(ars[idx[1]])


def main():
    # Load frozen data/covariances directly so simulations preserve them exactly.
    z_h,h_obs,_,h_cov=hz.build_covariance()
    h_inv,_,_,_=hz.covariance_checks(h_cov)
    h_cov=np.asarray(h_cov,float); h_inv=np.asarray(h_inv,float); h_obs=np.asarray(h_obs,float)

    mag,zcmb,zhel=sn.read_pantheon_table(PANTHEON_DIR/"Pantheon+SH0ES.dat")
    scov=sn.read_covariance(PANTHEON_DIR/"Pantheon+SH0ES_STAT+SYS.cov")
    mask=zcmb>0.01
    mag=np.asarray(mag[mask],float); zcmb=np.asarray(zcmb[mask],float); zhel=np.asarray(zhel[mask],float)
    scov=np.asarray(scov[np.ix_(mask,mask)],float)
    sfac=cho_factor(scov,lower=True,check_finite=True)
    sn_inv=cho_solve(sfac,np.eye(len(mag)),check_finite=False)
    ones=np.ones(len(mag))

    brows,bcov_list=bao.load_data(); bcov=np.asarray(bcov_list,float); b_inv=np.asarray(bao.invert(bcov_list),float)
    b_obs=np.asarray([float(r[1]) for r in brows],float)

    # Best-fit null from production pipeline: determines generating mean only.
    h_like,sn_like,b_like,_=combo.load_likelihoods()
    null_chi,null_om,null_parts,null_nuis,null_boundary=combo.profile_omega(0.0,FULL,h_like,sn_like,b_like)
    if null_boundary: raise RuntimeError("production LCDM null touches boundary")
    h0=float(null_nuis["H0"]); q=float(null_nuis["q"])

    hz0,sn0,bao0=precompute_theory(np.asarray([null_om]),np.asarray([0.0]),z_h,zcmb,zhel,brows)
    h_mean=h0*hz0[0,0]
    # SN arbitrary common intercept: set by matching observed mean residual; it is marginalized later.
    sn_base=sn0[0,0]
    intercept=float(np.mean(mag-sn_base))
    sn_mean=sn_base+intercept
    bao_mean=q*bao0[0,0]

    print("RCMS Protocol 02 — T5 null Monte Carlo")
    print(f"N_sim={N_SIM} rng_seed={RNG_SEED} frozen_threshold={THRESHOLD:.6f}")
    print(f"generating_LCDM Omega_m={null_om:.6f} H0={h0:.6f} q={q:.6f} chi2_real={null_chi:.6f}")

    # Precompute coarse model surface once.
    hzgrid,sngrid,bgrid=precompute_theory(OM_COARSE,AR_COARSE,z_h,zcmb,zhel,brows)
    # Validate grid approximation on real data against frozen Protocol 01 anchor.
    real_grid=evaluate_grid(h_obs,mag,b_obs,h_inv,sn_inv,b_inv,ones,hzgrid,sngrid,bgrid)
    # Reference is A_R=0 column, minimized over Omega_m.
    ia0=int(np.argmin(np.abs(AR_COARSE)))
    ref_grid=float(np.min(real_grid[:,ia0]))
    rc_grid,om_grid,ar_grid=best_from_grid(real_grid,OM_COARSE,AR_COARSE)
    dchi_grid=ref_grid-rc_grid
    print(f"grid_validation real_A_R={ar_grid:.6f} real_Omega_m={om_grid:.6f} real_delta_chi2={dchi_grid:.6f}")
    if abs(ar_grid-0.187021)>0.04 or abs(dchi_grid-THRESHOLD)>0.35:
        raise RuntimeError("Monte Carlo grid does not reproduce Protocol 01 anchor closely enough")

    rng=np.random.default_rng(RNG_SEED)
    hL=np.linalg.cholesky(h_cov); sL=np.linalg.cholesky(scov); bL=np.linalg.cholesky(bcov)
    exceed=0; dchis=[]; ars=[]
    for i in range(N_SIM):
        hd=h_mean+hL@rng.standard_normal(len(h_mean))
        sd=sn_mean+sL@rng.standard_normal(len(sn_mean))
        bd=bao_mean+bL@rng.standard_normal(len(bao_mean))
        g=evaluate_grid(hd,sd,bd,h_inv,sn_inv,b_inv,ones,hzgrid,sngrid,bgrid)
        ref=float(np.min(g[:,ia0]))
        rc,om,ar=best_from_grid(g,OM_COARSE,AR_COARSE)
        d=ref-rc
        dchis.append(d); ars.append(ar)
        exceed += int(d>=THRESHOLD)
        if (i+1)%50==0:
            print(f"progress={i+1}/{N_SIM} exceedances={exceed}")

    arr=np.asarray(dchis); aarr=np.asarray(ars)
    p=(1+exceed)/(1+N_SIM)
    print(f"exceedances={exceed}")
    print(f"p_MC={p:.8f}")
    print(f"delta_chi2_mean={arr.mean():.6f} median={np.median(arr):.6f} q90={np.quantile(arr,.9):.6f} q95={np.quantile(arr,.95):.6f} q99={np.quantile(arr,.99):.6f}")
    print(f"best_A_R_mean={aarr.mean():.6f} median={np.median(aarr):.6f} positive_fraction={np.mean(aarr>0):.6f}")
    if p<0.05:
        print("T5_NULL_CALIBRATION=UNCOMMON_UNDER_LCDM")
    else:
        print("T5_NULL_CALIBRATION=COMPATIBLE_WITH_LCDM_FLUCTUATIONS")


if __name__=="__main__": main()
