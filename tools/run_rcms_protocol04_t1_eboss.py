#!/usr/bin/env python3
"""RCMS Protocol 04 P04-T1: blind eBOSS DR16 independent-shape RCMS reveal.

Execution settings are frozen in docs/RCMS/protocols/protocol04_t1_execution_freeze.md.
The likelihood/data implementation is imported from the passed P04-T0 code.
"""
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
OUT = ROOT / "results" / "rcms_protocol04_t1.json"

OM_BOUNDS = (0.10, 0.50)
Q_BOUNDS = (20.0, 45.0)
AR_BOUNDS = (-5.0, 5.0)
PRIMARY_INTERVAL = (0.098671, 0.276779)
DES_SN_INTERVAL = (0.055322, 0.707729)


def load_t0():
    spec = importlib.util.spec_from_file_location("rcms_p04_t0", T0_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load P04-T0 implementation")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


t0 = load_t0()


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


def total_chi2(om: float, q: float, ar: float) -> float:
    if not (OM_BOUNDS[0] <= om <= OM_BOUNDS[1]):
        return 1.0e12
    if not (Q_BOUNDS[0] <= q <= Q_BOUNDS[1]):
        return 1.0e12
    if not (AR_BOUNDS[0] <= ar <= AR_BOUNDS[1]):
        return 1.0e12
    try:
        lrg = t0.gaussian_chi2(prediction(t0.LRG_Z, om, q, ar), t0.LRG_MEAN, t0.LRG_INV)
        qso = t0.gaussian_chi2(prediction(t0.QSO_Z, om, q, ar), t0.QSO_MEAN, t0.QSO_INV)
        lya = t0.lya_chi2(prediction(t0.LYA_Z, om, q, ar))
    except (ValueError, OverflowError):
        return 1.0e12
    value = float(lrg + qso + lya)
    return value if math.isfinite(value) else 1.0e12


def bounded_multistart(ar_fixed: float | None = None):
    if ar_fixed is None:
        starts = [
            (0.304383014, 30.016136523, 0.0),
            (0.30, 30.0, 0.2),
            (0.25, 30.0, -0.2),
            (0.40, 30.0, 0.5),
            (0.30, 32.0, -0.5),
        ]
        bounds = [OM_BOUNDS, Q_BOUNDS, AR_BOUNDS]

        def fun(x):
            return total_chi2(float(x[0]), float(x[1]), float(x[2]))
    else:
        starts = [
            (0.304383014, 30.016136523),
            (0.25, 30.0),
            (0.40, 30.0),
            (0.30, 25.0),
            (0.30, 35.0),
        ]
        bounds = [OM_BOUNDS, Q_BOUNDS]

        def fun(x):
            return total_chi2(float(x[0]), float(x[1]), float(ar_fixed))

    best = None
    for start in starts:
        res = minimize(
            fun,
            np.asarray(start, dtype=float),
            method="Nelder-Mead",
            options={"xatol": 1e-9, "fatol": 1e-9, "maxiter": 6000},
        )
        x = np.asarray(res.x, dtype=float)
        # Nelder-Mead has no bounds in older scipy APIs, so reject outside-domain points.
        if any(x[i] < bounds[i][0] or x[i] > bounds[i][1] for i in range(len(bounds))):
            continue
        value = float(fun(x))
        candidate = (value, x, bool(res.success), str(res.message))
        if best is None or candidate[0] < best[0]:
            best = candidate
    if best is None:
        raise RuntimeError(f"no admissible optimizer result for A_R={ar_fixed}")
    return best


def profile_ar(ar: float):
    value, x, success, message = bounded_multistart(float(ar))
    return float(value), float(x[0]), float(x[1]), success, message


def profile_interval(ar_best: float, chi_best: float):
    target = chi_best + 1.0

    def f(a: float) -> float:
        return profile_ar(float(a))[0] - target

    left_grid = np.linspace(AR_BOUNDS[0], ar_best, 121)
    right_grid = np.linspace(ar_best, AR_BOUNDS[1], 121)
    left = None
    right = None

    prev_a = float(left_grid[0])
    prev_f = f(prev_a)
    for a in left_grid[1:]:
        a = float(a)
        cur_f = f(a)
        if prev_f * cur_f <= 0.0:
            left = float(brentq(f, prev_a, a, xtol=2e-8))
        prev_a, prev_f = a, cur_f

    prev_a = float(right_grid[0])
    prev_f = f(prev_a)
    for a in right_grid[1:]:
        a = float(a)
        cur_f = f(a)
        if prev_f * cur_f <= 0.0:
            right = float(brentq(f, prev_a, a, xtol=2e-8))
            break
        prev_a, prev_f = a, cur_f

    return left, right


def overlap(a, b) -> bool:
    return max(a[0], b[0]) <= min(a[1], b[1])


def classify(ar_best: float, lo: float | None, hi: float | None, boundary: bool) -> str:
    if boundary or lo is None or hi is None:
        return "NOT_IDENTIFIABLE"
    if ar_best < 0.0 and hi < 0.0:
        return "SIGN_REVERSAL"
    if lo <= 0.0 <= hi:
        return "NULL_COMPATIBLE"
    if ar_best > 0.0 and lo > 0.0:
        p04 = (lo, hi)
        if overlap(p04, PRIMARY_INTERVAL) or overlap(p04, DES_SN_INTERVAL):
            return "POSITIVE_COMPATIBLE"
        return "POSITIVE_TENSION"
    return "NULL_COMPATIBLE"


def main() -> None:
    # Null is explicitly re-fit here using the same likelihood and domains.
    null_chi, null_x, null_success, null_msg = bounded_multistart(0.0)
    null_om, null_q = map(float, null_x)

    rc_chi, rc_x, rc_success, rc_msg = bounded_multistart(None)
    rc_om, rc_q, ar_best = map(float, rc_x)

    lo, hi = profile_interval(ar_best, rc_chi)
    margin = min(
        rc_om - OM_BOUNDS[0], OM_BOUNDS[1] - rc_om,
        rc_q - Q_BOUNDS[0], Q_BOUNDS[1] - rc_q,
        ar_best - AR_BOUNDS[0], AR_BOUNDS[1] - ar_best,
    )
    boundary = margin <= 1e-3
    label = classify(ar_best, lo, hi, boundary)

    delta_chi2 = float(null_chi - rc_chi)
    delta_aic = float(delta_chi2 - 2.0)

    payload = {
        "protocol": "RCMS Protocol 04 P04-T1",
        "dataset": "eBOSS DR16 LRG+QSO+LYA-auto",
        "bounds": {"Omega_m": OM_BOUNDS, "q": Q_BOUNDS, "A_R": AR_BOUNDS},
        "null": {
            "chi2_relative": null_chi,
            "Omega_m": null_om,
            "q": null_q,
            "optimizer_success": null_success,
            "optimizer_message": null_msg,
        },
        "rcms": {
            "chi2_relative": rc_chi,
            "Omega_m": rc_om,
            "q": rc_q,
            "A_R": ar_best,
            "A_R_profile_delta_chi2_1": [lo, hi],
            "optimizer_success": rc_success,
            "optimizer_message": rc_msg,
            "boundary": boundary,
        },
        "Delta_chi2_LCDM_minus_RCMS": delta_chi2,
        "Delta_AIC_LCDM_minus_RCMS": delta_aic,
        "BIC_status": "NOT_APPLICABLE_NONIID_COMPRESSED_LIKELIHOOD",
        "P04_T2_DIRECTION": label,
        "carried_forward": {
            "primary_interval": PRIMARY_INTERVAL,
            "DES_SN_interval": DES_SN_INTERVAL,
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lo_text = "OPEN" if lo is None else f"{lo:.9f}"
    hi_text = "OPEN" if hi is None else f"{hi:.9f}"
    print("RCMS Protocol 04 — P04-T1 blind eBOSS DR16 independent-shape reveal")
    print("MODEL_FORM_FROZEN=A_R*ln(1+z)")
    print(f"LCDM_chi2_relative={null_chi:.9f}")
    print(f"LCDM_Omega_m={null_om:.9f}")
    print(f"LCDM_q={null_q:.9f}")
    print(f"RCMS_chi2_relative={rc_chi:.9f}")
    print(f"RCMS_Omega_m={rc_om:.9f}")
    print(f"RCMS_q={rc_q:.9f}")
    print(f"RCMS_A_R={ar_best:.9f}")
    print(f"A_R_profile_delta_chi2_1=[{lo_text},{hi_text}]")
    print(f"Delta_chi2_LCDM_minus_RCMS={delta_chi2:.9f}")
    print(f"Delta_AIC_LCDM_minus_RCMS={delta_aic:.9f}")
    print("BIC_STATUS=NOT_APPLICABLE_NONIID_COMPRESSED_LIKELIHOOD")
    print(f"RCMS_boundary={boundary}")
    print(f"P04_T2_DIRECTION={label}")
    print(f"machine_readable={OUT.relative_to(ROOT)}")
    print("note=P04-T1/T2 is an independent-shape screening result, not validation of Resolutive Physics.")


if __name__ == "__main__":
    main()
