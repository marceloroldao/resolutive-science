#!/usr/bin/env python3
"""RCMS Protocol 05 P05-T1: ELG replacement challenge reveal."""
from __future__ import annotations

import importlib.util
import json
import math
import pathlib
import sys

import numpy as np
from scipy.optimize import brentq, minimize

ROOT = pathlib.Path(__file__).resolve().parents[1]
T0_PATH = ROOT / "tools" / "run_rcms_protocol05_t0_elg.py"
OUT = ROOT / "results" / "rcms_protocol05_t1.json"

OM_BOUNDS = (0.10, 0.50)
Q_BOUNDS = (20.0, 45.0)
AR_BOUNDS = (-5.0, 5.0)


def load_t0():
    spec = importlib.util.spec_from_file_location("rcms_p05_t0", T0_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load P05-T0 implementation")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


t0 = load_t0()


def e_rcms(z: float, om: float, ar: float) -> float:
    e2 = om * (1.0 + z) ** 3 + 1.0 - om + ar * math.log1p(z)
    if not math.isfinite(e2) or e2 <= 0.0:
        raise ValueError("non-positive RCMS E^2")
    return math.sqrt(e2)


def dm_shape(z: float, om: float, ar: float) -> float:
    value, _ = t0.p04.quad(lambda zz: 1.0 / e_rcms(zz, om, ar), 0.0, z, epsabs=2e-11, epsrel=2e-11)
    return float(value)


def dm_over_rs(z: float, om: float, q: float, ar: float) -> float:
    return q * dm_shape(z, om, ar)


def dh_over_rs(z: float, om: float, q: float, ar: float) -> float:
    return q / e_rcms(z, om, ar)


def dv_over_rs(z: float, om: float, q: float, ar: float) -> float:
    dm = dm_over_rs(z, om, q, ar)
    dh = dh_over_rs(z, om, q, ar)
    return float((z * dm * dm * dh) ** (1.0 / 3.0))


def elg_chi2(om: float, q: float, ar: float) -> float:
    dv = dv_over_rs(t0.ELG_Z, om, q, ar)
    if not (t0.ELG_X[0] <= dv <= t0.ELG_X[-1]):
        return 1.0e9
    logp = float(t0.ELG_INTERP(dv))
    return -2.0 * (logp - t0.ELG_LOGP_MAX)


def total_chi2(om: float, q: float, ar: float) -> float:
    if not (OM_BOUNDS[0] <= om <= OM_BOUNDS[1]):
        return 1.0e12
    if not (Q_BOUNDS[0] <= q <= Q_BOUNDS[1]):
        return 1.0e12
    if not (AR_BOUNDS[0] <= ar <= AR_BOUNDS[1]):
        return 1.0e12
    try:
        qso_pred = np.array([
            dm_over_rs(t0.p04.QSO_Z, om, q, ar),
            dh_over_rs(t0.p04.QSO_Z, om, q, ar),
        ])
        lya_pred = np.array([
            dm_over_rs(t0.p04.LYA_Z, om, q, ar),
            dh_over_rs(t0.p04.LYA_Z, om, q, ar),
        ])
        value = (
            elg_chi2(om, q, ar)
            + t0.p04.gaussian_chi2(qso_pred, t0.p04.QSO_MEAN, t0.p04.QSO_INV)
            + t0.p04.lya_chi2(lya_pred)
        )
    except (ValueError, OverflowError):
        return 1.0e12
    return float(value) if math.isfinite(value) else 1.0e12


def fit(ar_fixed: float | None = None):
    if ar_fixed is None:
        starts = [
            (0.282, 29.35, 0.0),
            (0.30, 30.0, 0.2),
            (0.25, 30.0, -0.2),
            (0.40, 32.0, 0.8),
            (0.30, 35.0, -0.8),
        ]
        bounds = [OM_BOUNDS, Q_BOUNDS, AR_BOUNDS]
        fun = lambda x: total_chi2(float(x[0]), float(x[1]), float(x[2]))
    else:
        starts = [
            (0.282, 29.35),
            (0.22, 28.0),
            (0.35, 31.0),
            (0.45, 35.0),
        ]
        bounds = [OM_BOUNDS, Q_BOUNDS]
        fun = lambda x: total_chi2(float(x[0]), float(x[1]), float(ar_fixed))

    best = None
    for start in starts:
        res = minimize(fun, np.asarray(start, dtype=float), method="Nelder-Mead",
                       options={"xatol": 1e-9, "fatol": 1e-9, "maxiter": 6000})
        x = np.asarray(res.x, dtype=float)
        if any(x[i] < bounds[i][0] or x[i] > bounds[i][1] for i in range(len(bounds))):
            continue
        value = float(fun(x))
        cand = (value, x, bool(res.success), str(res.message))
        if best is None or cand[0] < best[0]:
            best = cand
    if best is None:
        raise RuntimeError(f"no admissible optimizer result for A_R={ar_fixed}")
    return best


def profile_ar(ar: float):
    value, x, success, msg = fit(float(ar))
    return float(value), float(x[0]), float(x[1]), success, msg


def profile_interval(ar_best: float, chi_best: float):
    target = chi_best + 1.0
    def f(a: float) -> float:
        return profile_ar(float(a))[0] - target

    left_grid = np.linspace(AR_BOUNDS[0], ar_best, 121)
    right_grid = np.linspace(ar_best, AR_BOUNDS[1], 121)
    left = None
    right = None

    prev_a, prev_f = float(left_grid[0]), f(float(left_grid[0]))
    for a in left_grid[1:]:
        a = float(a); cur = f(a)
        if prev_f * cur <= 0.0:
            left = float(brentq(f, prev_a, a, xtol=2e-8))
        prev_a, prev_f = a, cur

    prev_a, prev_f = float(right_grid[0]), f(float(right_grid[0]))
    for a in right_grid[1:]:
        a = float(a); cur = f(a)
        if prev_f * cur <= 0.0:
            right = float(brentq(f, prev_a, a, xtol=2e-8))
            break
        prev_a, prev_f = a, cur
    return left, right


def classify(ar: float, lo: float | None, hi: float | None, delta_chi2: float, boundary: bool) -> str:
    if boundary or lo is None or hi is None:
        return "NOT_IDENTIFIABLE"
    if ar < 0.0 and hi < 0.0:
        return "SIGN_REVERSAL"
    if ar > 0.0 and lo > 0.0:
        return "LOWZ_SHAPE_PERSISTENCE"
    if ar > 0.0:
        return "POSITIVE_BUT_WEAK"
    if lo <= 0.0 <= hi and delta_chi2 < 1.0:
        return "LRG_SPECIFIC_SUPPORTED"
    return "INCONCLUSIVE_PROTOCOL05"


def main() -> None:
    null_chi, null_x, null_success, null_msg = fit(0.0)
    null_om, null_q = map(float, null_x)

    rc_chi, rc_x, rc_success, rc_msg = fit(None)
    rc_om, rc_q, ar = map(float, rc_x)
    lo, hi = profile_interval(ar, rc_chi)

    margin = min(
        rc_om - OM_BOUNDS[0], OM_BOUNDS[1] - rc_om,
        rc_q - Q_BOUNDS[0], Q_BOUNDS[1] - rc_q,
        ar - AR_BOUNDS[0], AR_BOUNDS[1] - ar,
    )
    boundary = margin <= 1e-3
    delta_chi2 = float(null_chi - rc_chi)
    delta_aic = float(delta_chi2 - 2.0)
    label = classify(ar, lo, hi, delta_chi2, boundary)

    payload = {
        "protocol": "RCMS Protocol 05 P05-T1",
        "dataset": "eBOSS DR16 ELG+QSO+LYA-auto (LRG replaced)",
        "null": {"chi2_relative": null_chi, "Omega_m": null_om, "q": null_q,
                 "optimizer_success": null_success, "optimizer_message": null_msg},
        "rcms": {"chi2_relative": rc_chi, "Omega_m": rc_om, "q": rc_q, "A_R": ar,
                 "A_R_profile_delta_chi2_1": [lo, hi], "boundary": boundary,
                 "optimizer_success": rc_success, "optimizer_message": rc_msg},
        "Delta_chi2_LCDM_minus_RCMS": delta_chi2,
        "Delta_AIC_LCDM_minus_RCMS": delta_aic,
        "P05_T2_CLASSIFICATION": label,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lo_text = "OPEN" if lo is None else f"{lo:.9f}"
    hi_text = "OPEN" if hi is None else f"{hi:.9f}"
    print("RCMS Protocol 05 — P05-T1 ELG replacement challenge reveal")
    print("MODEL_FORM_FROZEN=A_R*ln(1+z)")
    print(f"LCDM_chi2_relative={null_chi:.9f}")
    print(f"LCDM_Omega_m={null_om:.9f}")
    print(f"LCDM_q={null_q:.9f}")
    print(f"RCMS_chi2_relative={rc_chi:.9f}")
    print(f"RCMS_Omega_m={rc_om:.9f}")
    print(f"RCMS_q={rc_q:.9f}")
    print(f"RCMS_A_R={ar:.9f}")
    print(f"A_R_profile_delta_chi2_1=[{lo_text},{hi_text}]")
    print(f"Delta_chi2_LCDM_minus_RCMS={delta_chi2:.9f}")
    print(f"Delta_AIC_LCDM_minus_RCMS={delta_aic:.9f}")
    print("BIC_STATUS=NOT_APPLICABLE_NONIID_COMPRESSED_LIKELIHOOD")
    print(f"RCMS_boundary={boundary}")
    print(f"P05_T2_CLASSIFICATION={label}")
    print(f"machine_readable={OUT.relative_to(ROOT)}")
    print("note=Protocol 05 is a tracer/block-dependence diagnostic, not validation of Resolutive Physics.")


if __name__ == "__main__":
    main()
