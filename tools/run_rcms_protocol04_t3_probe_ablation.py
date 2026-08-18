#!/usr/bin/env python3
"""RCMS Protocol 04 P04-T3: preregistered eBOSS DR16 leave-one-probe-out ablation."""
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
OUT = ROOT / "results" / "rcms_protocol04_t3_probe_ablation.json"

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


def contributions(om: float, q: float, ar: float) -> dict[str, float]:
    return {
        "LRG": t0.gaussian_chi2(prediction(t0.LRG_Z, om, q, ar), t0.LRG_MEAN, t0.LRG_INV),
        "QSO": t0.gaussian_chi2(prediction(t0.QSO_Z, om, q, ar), t0.QSO_MEAN, t0.QSO_INV),
        "LYA": t0.lya_chi2(prediction(t0.LYA_Z, om, q, ar)),
    }


def total_chi2(probes: tuple[str, ...], om: float, q: float, ar: float) -> float:
    if not (OM_BOUNDS[0] <= om <= OM_BOUNDS[1]):
        return 1e12
    if not (Q_BOUNDS[0] <= q <= Q_BOUNDS[1]):
        return 1e12
    if not (AR_BOUNDS[0] <= ar <= AR_BOUNDS[1]):
        return 1e12
    try:
        c = contributions(om, q, ar)
    except (ValueError, OverflowError):
        return 1e12
    value = float(sum(c[p] for p in probes))
    return value if math.isfinite(value) else 1e12


def fit(probes: tuple[str, ...], ar_fixed: float | None):
    if ar_fixed is None:
        starts = [(0.304, 30.0, 0.0), (0.30, 30.0, 0.5), (0.35, 32.0, 1.5), (0.25, 28.0, -0.5), (0.45, 36.0, 2.0)]
        bounds = [OM_BOUNDS, Q_BOUNDS, AR_BOUNDS]
        fun = lambda x: total_chi2(probes, float(x[0]), float(x[1]), float(x[2]))
    else:
        starts = [(0.304, 30.0), (0.25, 28.0), (0.35, 32.0), (0.45, 36.0)]
        bounds = [OM_BOUNDS, Q_BOUNDS]
        fun = lambda x: total_chi2(probes, float(x[0]), float(x[1]), float(ar_fixed))

    best = None
    for start in starts:
        res = minimize(fun, np.asarray(start, dtype=float), method="Nelder-Mead",
                       options={"xatol": 1e-9, "fatol": 1e-9, "maxiter": 6000})
        x = np.asarray(res.x, dtype=float)
        if any(x[i] < bounds[i][0] or x[i] > bounds[i][1] for i in range(len(bounds))):
            continue
        candidate = (float(fun(x)), x, bool(res.success), str(res.message))
        if best is None or candidate[0] < best[0]:
            best = candidate
    if best is None:
        raise RuntimeError(f"no admissible optimizer result for probes={probes}, A_R={ar_fixed}")
    return best


def profile_interval(probes: tuple[str, ...], ar_best: float, chi_best: float):
    target = chi_best + 1.0

    def f(a: float) -> float:
        return fit(probes, float(a))[0] - target

    def root_on_grid(grid):
        prev_a = float(grid[0]); prev_f = f(prev_a)
        roots = []
        for aa in grid[1:]:
            a = float(aa); cur_f = f(a)
            if prev_f * cur_f <= 0.0:
                roots.append(float(brentq(f, prev_a, a, xtol=2e-8)))
            prev_a, prev_f = a, cur_f
        return roots

    left = root_on_grid(np.linspace(AR_BOUNDS[0], ar_best, 101))
    right = root_on_grid(np.linspace(ar_best, AR_BOUNDS[1], 101))
    lo = left[-1] if left else None
    hi = right[0] if right else None
    return lo, hi


def evaluate(name: str, probes: tuple[str, ...]) -> dict:
    null_chi, null_x, _, _ = fit(probes, 0.0)
    rc_chi, rc_x, _, _ = fit(probes, None)
    om, q, ar = map(float, rc_x)
    lo, hi = profile_interval(probes, ar, rc_chi)
    margin = min(om-OM_BOUNDS[0], OM_BOUNDS[1]-om, q-Q_BOUNDS[0], Q_BOUNDS[1]-q, ar-AR_BOUNDS[0], AR_BOUNDS[1]-ar)
    identifiable = (lo is not None and hi is not None and margin > 1e-3)
    return {
        "name": name,
        "probes": list(probes),
        "lcdm": {"chi2_relative": null_chi, "Omega_m": float(null_x[0]), "q": float(null_x[1])},
        "rcms": {"chi2_relative": rc_chi, "Omega_m": om, "q": q, "A_R": ar,
                 "A_R_profile_delta_chi2_1": [lo, hi], "identifiable": identifiable},
        "Delta_chi2": float(null_chi - rc_chi),
        "Delta_AIC": float(null_chi - rc_chi - 2.0),
    }


def main() -> None:
    configs = [
        ("FULL", ("LRG", "QSO", "LYA")),
        ("NO_LRG", ("QSO", "LYA")),
        ("NO_QSO", ("LRG", "LYA")),
        ("NO_LYA", ("LRG", "QSO")),
    ]
    rows = [evaluate(name, probes) for name, probes in configs]
    payload = {"protocol": "RCMS Protocol 04 P04-T3", "model_form": "A_R*ln(1+z)", "results": rows}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("RCMS Protocol 04 — P04-T3 eBOSS probe ablation")
    print("MODEL_FORM_FROZEN=A_R*ln(1+z)")
    for row in rows:
        r = row["rcms"]
        lo, hi = r["A_R_profile_delta_chi2_1"]
        print(f"{row['name']}: probes={'+'.join(row['probes'])} A_R={r['A_R']:.9f} "
              f"profile=[{lo},{hi}] Delta_chi2={row['Delta_chi2']:.9f} "
              f"Delta_AIC={row['Delta_AIC']:.9f} identifiable={r['identifiable']}")
    print(f"machine_readable={OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
