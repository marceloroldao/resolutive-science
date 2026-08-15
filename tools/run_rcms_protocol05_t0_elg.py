#!/usr/bin/env python3
"""RCMS Protocol 05 P05-T0: ELG replacement Lambda-CDM and identifiability gate.

This program intentionally evaluates no RCMS A_R parameter. It validates the
frozen eBOSS DR16 ELG BAO-only likelihood and constructs the preregistered
ELG+QSO+LYA-auto Lambda-CDM challenge statistic.
"""
from __future__ import annotations

import importlib.util
import math
import pathlib
import sys

import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.optimize import minimize_scalar

ROOT = pathlib.Path(__file__).resolve().parents[1]
P04_T0 = ROOT / "tools" / "run_rcms_protocol04_t0_eboss.py"
DATA = ROOT / "data" / "external" / "eboss_dr16"
ELG_FILE = DATA / "sdss_DR16_ELG_BAO_DVtable.txt"
ELG_Z = 0.845
OM_BOUNDS = (0.10, 0.50)
Q_BOUNDS = (20.0, 45.0)
PROFILE_GRID = np.linspace(0.12, 0.48, 19)
PROFILE_SPAN_MIN = 1.0e-3


def load_p04():
    spec = importlib.util.spec_from_file_location("p04_t0", P04_T0)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load P04-T0 implementation")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


p04 = load_p04()


def load_elg():
    grid = np.loadtxt(ELG_FILE)
    if grid.ndim != 2 or grid.shape[1] != 2:
        raise RuntimeError("unexpected ELG grid layout")
    x = np.asarray(grid[:, 0], dtype=float)
    prob = np.asarray(grid[:, 1], dtype=float)
    if np.any(~np.isfinite(x)) or np.any(~np.isfinite(prob)) or np.any(prob <= 0.0):
        raise RuntimeError("invalid ELG probability grid")
    if np.any(np.diff(x) <= 0.0):
        raise RuntimeError("ELG DV grid is not strictly increasing")
    logp = np.log(prob)
    interp = UnivariateSpline(x, logp, s=0, ext=2)
    return x, logp, interp


ELG_X, ELG_LOGP, ELG_INTERP = load_elg()
ELG_LOGP_MAX = float(np.max(ELG_LOGP))


def e_lcdm(z: float, om: float) -> float:
    return math.sqrt(om * (1.0 + z) ** 3 + 1.0 - om)


def dm_shape(z: float, om: float) -> float:
    value, _ = p04.quad(lambda zz: 1.0 / e_lcdm(zz, om), 0.0, z, epsabs=2e-11, epsrel=2e-11)
    return float(value)


def dm_over_rs(z: float, om: float, q: float) -> float:
    return q * dm_shape(z, om)


def dh_over_rs(z: float, om: float, q: float) -> float:
    return q / e_lcdm(z, om)


def dv_over_rs(z: float, om: float, q: float) -> float:
    dm = dm_over_rs(z, om, q)
    dh = dh_over_rs(z, om, q)
    return float((z * dm * dm * dh) ** (1.0 / 3.0))


def elg_chi2(om: float, q: float) -> float:
    dv = dv_over_rs(ELG_Z, om, q)
    if not (ELG_X[0] <= dv <= ELG_X[-1]):
        return 1.0e9
    logp = float(ELG_INTERP(dv))
    return -2.0 * (logp - ELG_LOGP_MAX)


def total_chi2(om: float, q: float) -> float:
    if not (OM_BOUNDS[0] <= om <= OM_BOUNDS[1] and Q_BOUNDS[0] <= q <= Q_BOUNDS[1]):
        return 1.0e12
    qso_pred = np.array([
        dm_over_rs(p04.QSO_Z, om, q),
        dh_over_rs(p04.QSO_Z, om, q),
    ])
    lya_pred = np.array([
        dm_over_rs(p04.LYA_Z, om, q),
        dh_over_rs(p04.LYA_Z, om, q),
    ])
    return float(
        elg_chi2(om, q)
        + p04.gaussian_chi2(qso_pred, p04.QSO_MEAN, p04.QSO_INV)
        + p04.lya_chi2(lya_pred)
    )


def profile_q(om: float):
    res = minimize_scalar(
        lambda q: total_chi2(float(om), float(q)),
        bounds=Q_BOUNDS,
        method="bounded",
        options={"xatol": 2e-10, "maxiter": 500},
    )
    if not res.success:
        raise RuntimeError(f"q profiling failed at Omega_m={om}: {res.message}")
    return float(res.fun), float(res.x)


def main() -> None:
    # Cobaya's 1D grid convention is log(probability), so its maximum must map
    # to zero relative chi-square before any cosmological fit is interpreted.
    elg_grid_min = float(np.min(-2.0 * (ELG_LOGP - ELG_LOGP_MAX)))
    if abs(elg_grid_min) > 1e-12:
        raise SystemExit("ELG upstream likelihood convention gate failed")

    res = minimize_scalar(
        lambda om: profile_q(float(om))[0],
        bounds=OM_BOUNDS,
        method="bounded",
        options={"xatol": 2e-8, "maxiter": 300},
    )
    if not res.success:
        raise SystemExit(f"Lambda-CDM shape optimization failed: {res.message}")
    om_best = float(res.x)
    chi_best, q_best = profile_q(om_best)

    margin_om = min(om_best - OM_BOUNDS[0], OM_BOUNDS[1] - om_best)
    margin_q = min(q_best - Q_BOUNDS[0], Q_BOUNDS[1] - q_best)
    if margin_om < 1e-3 or margin_q < 1e-3:
        raise SystemExit("P05 Lambda-CDM optimum is boundary-limited")

    profile = [profile_q(float(om))[0] for om in PROFILE_GRID]
    finite = np.asarray([x for x in profile if np.isfinite(x) and x < 1.0e8])
    if finite.size < 3:
        raise SystemExit("insufficient finite Omega_m profile points")
    profile_span = float(np.max(finite) - np.min(finite))
    if profile_span <= PROFILE_SPAN_MIN:
        raise SystemExit(f"P05 shape identifiability gate failed: span={profile_span:.8g}")

    print("RCMS Protocol 05 — P05-T0 ELG replacement baseline gate")
    print("RCMS_PARAMETER_EVALUATED=NO")
    print(f"ELG_z={ELG_Z:.3f} observable=DV_over_rs grid_points={ELG_X.size}")
    print(f"ELG_DV_range=[{ELG_X[0]:.9f},{ELG_X[-1]:.9f}]")
    print("ELG_UPSTREAM_LIKELIHOOD_CONVENTION=PASS")
    print(f"LCDM_Omega_m={om_best:.9f}")
    print(f"LCDM_q_c_over_H0rd={q_best:.9f}")
    print(f"LCDM_chi2_relative={chi_best:.9f}")
    print(f"PROFILE_OMEGA_M_SPAN_DELTA_CHI2={profile_span:.9f}")
    print("P05_T0_SHAPE_IDENTIFIABILITY=PASS")
    print("P05_T0_STATUS=READY_FOR_PREREGISTERED_RCMS_CHALLENGE")


if __name__ == "__main__":
    main()
