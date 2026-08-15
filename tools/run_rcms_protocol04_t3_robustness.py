#!/usr/bin/env python3
"""RCMS Protocol 04 P04-T3: eBOSS leave-one-redshift-block-out robustness."""
from __future__ import annotations

import importlib.util
import json
import math
import pathlib
import sys

import numpy as np
from scipy.optimize import minimize

ROOT = pathlib.Path(__file__).resolve().parents[1]
T1_PATH = ROOT / "tools" / "run_rcms_protocol04_t1_eboss.py"
OUT = ROOT / "results" / "rcms_protocol04_t3.json"

OM_BOUNDS = (0.10, 0.50)
Q_BOUNDS = (20.0, 45.0)
AR_BOUNDS = (-5.0, 5.0)
BLOCKS = ("LRG", "QSO", "LYA_AUTO")


def load_t1():
    spec = importlib.util.spec_from_file_location("rcms_p04_t1", T1_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load P04-T1 implementation")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


t1 = load_t1()
t0 = t1.t0


def subset_chi2(om: float, q: float, ar: float, omit: str) -> float:
    if not (OM_BOUNDS[0] <= om <= OM_BOUNDS[1]):
        return 1.0e12
    if not (Q_BOUNDS[0] <= q <= Q_BOUNDS[1]):
        return 1.0e12
    if not (AR_BOUNDS[0] <= ar <= AR_BOUNDS[1]):
        return 1.0e12
    try:
        terms = []
        if omit != "LRG":
            terms.append(
                t0.gaussian_chi2(
                    t1.prediction(t0.LRG_Z, om, q, ar), t0.LRG_MEAN, t0.LRG_INV
                )
            )
        if omit != "QSO":
            terms.append(
                t0.gaussian_chi2(
                    t1.prediction(t0.QSO_Z, om, q, ar), t0.QSO_MEAN, t0.QSO_INV
                )
            )
        if omit != "LYA_AUTO":
            terms.append(t0.lya_chi2(t1.prediction(t0.LYA_Z, om, q, ar)))
    except (ValueError, OverflowError):
        return 1.0e12
    value = float(sum(terms))
    return value if math.isfinite(value) else 1.0e12


def fit_subset(omit: str, ar_fixed: float | None):
    if ar_fixed is None:
        starts = [
            (0.35, 35.0, 1.66),
            (0.30, 30.0, 0.0),
            (0.30, 32.0, 0.5),
            (0.25, 30.0, -0.5),
            (0.40, 35.0, 2.0),
        ]
        bounds = [OM_BOUNDS, Q_BOUNDS, AR_BOUNDS]

        def fun(x):
            return subset_chi2(float(x[0]), float(x[1]), float(x[2]), omit)
    else:
        starts = [
            (0.304, 30.0),
            (0.25, 30.0),
            (0.40, 30.0),
            (0.30, 25.0),
            (0.30, 35.0),
        ]
        bounds = [OM_BOUNDS, Q_BOUNDS]

        def fun(x):
            return subset_chi2(float(x[0]), float(x[1]), float(ar_fixed), omit)

    best = None
    for start in starts:
        res = minimize(
            fun,
            np.asarray(start, dtype=float),
            method="Nelder-Mead",
            options={"xatol": 1e-9, "fatol": 1e-9, "maxiter": 6000},
        )
        x = np.asarray(res.x, dtype=float)
        if any(x[i] < bounds[i][0] or x[i] > bounds[i][1] for i in range(len(bounds))):
            continue
        value = float(fun(x))
        cand = (value, x, bool(res.success), str(res.message))
        if best is None or cand[0] < best[0]:
            best = cand
    if best is None:
        raise RuntimeError(f"no admissible fit for omit={omit}, A_R={ar_fixed}")
    return best


def main() -> None:
    rows = []
    for omit in BLOCKS:
        null_chi, null_x, null_success, null_msg = fit_subset(omit, 0.0)
        rc_chi, rc_x, rc_success, rc_msg = fit_subset(omit, None)
        null_om, null_q = map(float, null_x)
        rc_om, rc_q, ar = map(float, rc_x)
        margin = min(
            rc_om - OM_BOUNDS[0], OM_BOUNDS[1] - rc_om,
            rc_q - Q_BOUNDS[0], Q_BOUNDS[1] - rc_q,
            ar - AR_BOUNDS[0], AR_BOUNDS[1] - ar,
        )
        boundary = margin <= 1e-3
        dchi2 = float(null_chi - rc_chi)
        sign_reversal = ar < 0.0
        row = {
            "omit": omit,
            "null": {
                "chi2_relative": float(null_chi),
                "Omega_m": null_om,
                "q": null_q,
                "optimizer_success": null_success,
                "optimizer_message": null_msg,
            },
            "rcms": {
                "chi2_relative": float(rc_chi),
                "Omega_m": rc_om,
                "q": rc_q,
                "A_R": ar,
                "boundary": boundary,
                "optimizer_success": rc_success,
                "optimizer_message": rc_msg,
            },
            "Delta_chi2_LCDM_minus_RCMS": dchi2,
            "sign_reversal": sign_reversal,
        }
        rows.append(row)

    payload = {
        "protocol": "RCMS Protocol 04 P04-T3",
        "dataset": "eBOSS DR16 LRG+QSO+LYA-auto",
        "primary_A_R": 1.662222508,
        "runs": rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("RCMS Protocol 04 — P04-T3 leave-one-redshift-block-out robustness")
    print("PRIMARY_A_R=1.662222508")
    for row in rows:
        rc = row["rcms"]
        print(
            f"omit={row['omit']} A_R={rc['A_R']:.9f} "
            f"Omega_m={rc['Omega_m']:.9f} q={rc['q']:.9f} "
            f"Delta_chi2={row['Delta_chi2_LCDM_minus_RCMS']:.9f} "
            f"boundary={rc['boundary']} sign_reversal={row['sign_reversal']}"
        )
    print(f"machine_readable={OUT.relative_to(ROOT)}")
    print("note=P04-T3 is a frozen robustness diagnostic; primary P04-T1/T2 remains unchanged.")


if __name__ == "__main__":
    main()
