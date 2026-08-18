#!/usr/bin/env python3
"""RCMS Protocol 04 P04-T4: preregistered LRG component ablation."""
from __future__ import annotations

import importlib.util
import json
import math
import pathlib
import sys

import numpy as np
from scipy.optimize import brentq, minimize

ROOT = pathlib.Path(__file__).resolve().parents[1]
T0_PATH = ROOT / "tools" / "run_rcms_protocol04_t0_eboss.py"
OUT = ROOT / "results" / "rcms_protocol04_t4_lrg_component_ablation.json"
OM_BOUNDS = (0.10, 0.50)
Q_BOUNDS = (20.0, 45.0)
AR_BOUNDS = (-5.0, 5.0)


def load_t0():
    spec = importlib.util.spec_from_file_location("rcms_p04_t0", T0_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load P04-T0 implementation")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


t0 = load_t0()
LRG_COV = np.linalg.inv(t0.LRG_INV)


def e_rcms(z: float, om: float, ar: float) -> float:
    e2 = om * (1.0 + z) ** 3 + 1.0 - om + ar * math.log1p(z)
    if not math.isfinite(e2) or e2 <= 0.0:
        raise ValueError("non-positive RCMS E^2")
    return math.sqrt(e2)


def dm_shape(z: float, om: float, ar: float) -> float:
    value, _ = t0.quad(lambda zz: 1.0 / e_rcms(zz, om, ar), 0.0, z, epsabs=2e-11, epsrel=2e-11)
    return float(value)


def prediction(z: float, om: float, q: float, ar: float) -> np.ndarray:
    return np.array([q * dm_shape(z, om, ar), q / e_rcms(z, om, ar)], dtype=float)


def lrg_component_chi2(mode: str, pred: np.ndarray) -> float:
    if mode == "FULL":
        return t0.gaussian_chi2(pred, t0.LRG_MEAN, t0.LRG_INV)
    if mode == "NONE":
        return 0.0
    idx = 0 if mode == "DM" else 1
    var = float(LRG_COV[idx, idx])
    d = float(pred[idx] - t0.LRG_MEAN[idx])
    return d * d / var


def total_chi2(mode: str, om: float, q: float, ar: float) -> float:
    if not (OM_BOUNDS[0] <= om <= OM_BOUNDS[1] and Q_BOUNDS[0] <= q <= Q_BOUNDS[1] and AR_BOUNDS[0] <= ar <= AR_BOUNDS[1]):
        return 1e12
    try:
        lrg = lrg_component_chi2(mode, prediction(t0.LRG_Z, om, q, ar))
        qso = t0.gaussian_chi2(prediction(t0.QSO_Z, om, q, ar), t0.QSO_MEAN, t0.QSO_INV)
        lya = t0.lya_chi2(prediction(t0.LYA_Z, om, q, ar))
    except (ValueError, OverflowError):
        return 1e12
    val = float(lrg + qso + lya)
    return val if math.isfinite(val) else 1e12


def fit(mode: str, ar_fixed: float | None):
    if ar_fixed is None:
        starts = [(0.304,30.0,0.0),(0.30,30.0,0.5),(0.35,32.0,1.5),(0.25,28.0,-0.5),(0.45,36.0,2.0)]
        bounds = [OM_BOUNDS,Q_BOUNDS,AR_BOUNDS]
        fun = lambda x: total_chi2(mode,float(x[0]),float(x[1]),float(x[2]))
    else:
        starts = [(0.304,30.0),(0.25,28.0),(0.35,32.0),(0.45,36.0)]
        bounds = [OM_BOUNDS,Q_BOUNDS]
        fun = lambda x: total_chi2(mode,float(x[0]),float(x[1]),float(ar_fixed))
    best = None
    for start in starts:
        res = minimize(fun,np.asarray(start,dtype=float),method="Nelder-Mead",options={"xatol":1e-9,"fatol":1e-9,"maxiter":6000})
        x = np.asarray(res.x,dtype=float)
        if any(x[i] < bounds[i][0] or x[i] > bounds[i][1] for i in range(len(bounds))):
            continue
        cand = (float(fun(x)),x)
        if best is None or cand[0] < best[0]:
            best = cand
    if best is None:
        raise RuntimeError(f"no admissible fit mode={mode} A_R={ar_fixed}")
    return best


def profile_interval(mode: str, ar_best: float, chi_best: float):
    target = chi_best + 1.0
    def f(a: float) -> float:
        return fit(mode,float(a))[0] - target
    def roots(grid):
        out=[]; pa=float(grid[0]); pf=f(pa)
        for aa in grid[1:]:
            a=float(aa); cf=f(a)
            if pf*cf <= 0.0:
                out.append(float(brentq(f,pa,a,xtol=2e-8)))
            pa,pf=a,cf
        return out
    left=roots(np.linspace(AR_BOUNDS[0],ar_best,101))
    right=roots(np.linspace(ar_best,AR_BOUNDS[1],101))
    return (left[-1] if left else None, right[0] if right else None)


def evaluate(name: str, mode: str) -> dict:
    null_chi,null_x=fit(mode,0.0)
    rc_chi,rc_x=fit(mode,None)
    om,q,ar=map(float,rc_x)
    lo,hi=profile_interval(mode,ar,rc_chi)
    margin=min(om-OM_BOUNDS[0],OM_BOUNDS[1]-om,q-Q_BOUNDS[0],Q_BOUNDS[1]-q,ar-AR_BOUNDS[0],AR_BOUNDS[1]-ar)
    ident=(lo is not None and hi is not None and margin > 1e-3)
    return {"name":name,"mode":mode,"lcdm":{"chi2_relative":null_chi,"Omega_m":float(null_x[0]),"q":float(null_x[1])},"rcms":{"chi2_relative":rc_chi,"Omega_m":om,"q":q,"A_R":ar,"A_R_profile_delta_chi2_1":[lo,hi],"identifiable":ident},"Delta_chi2":float(null_chi-rc_chi),"Delta_AIC":float(null_chi-rc_chi-2.0)}


def main() -> None:
    configs=[("FULL_LRG","FULL"),("LRG_DM_ONLY","DM"),("LRG_DH_ONLY","DH"),("NO_LRG","NONE")]
    rows=[evaluate(n,m) for n,m in configs]
    payload={"protocol":"RCMS Protocol 04 P04-T4","model_form":"A_R*ln(1+z)","lrg_covariance":LRG_COV.tolist(),"results":rows}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("RCMS Protocol 04 — P04-T4 LRG component ablation")
    print("MODEL_FORM_FROZEN=A_R*ln(1+z)")
    for row in rows:
        r=row["rcms"]; lo,hi=r["A_R_profile_delta_chi2_1"]
        print(f"{row['name']}: A_R={r['A_R']:.9f} profile=[{lo},{hi}] Delta_chi2={row['Delta_chi2']:.9f} Delta_AIC={row['Delta_AIC']:.9f} identifiable={r['identifiable']}")
    print(f"machine_readable={OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
