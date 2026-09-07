#!/usr/bin/env python3
"""RCMS Protocol 13 — preregistered systematics/nuisance sensitivity map."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MEAN = ROOT / "data/rcms/desi_dr2_bao_all_mean.txt"
COV = ROOT / "data/rcms/desi_dr2_bao_all_cov.txt"
OUT = ROOT / "results/rcms_protocol13_systematics.json"

OMEGA_BOUNDS = (0.05, 0.60)
AR_BOUNDS = (-1.0, 1.0)
AR_STEP = 0.01


def load_data():
    rows = []
    for line in MEAN.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        z, val, kind = line.split()
        rows.append((float(z), float(val), kind))
    cov = np.loadtxt(COV, dtype=float)
    if len(rows) != 13 or cov.shape != (13, 13):
        raise RuntimeError("DESI DR2 BAO frozen dimensions are not 13 / 13x13")
    if not np.allclose(cov, cov.T, rtol=0.0, atol=1e-12):
        raise RuntimeError("baseline covariance is not symmetric")
    np.linalg.cholesky(cov)
    return rows, cov


def simpson(f, b, n=200):
    if n % 2:
        n += 1
    h = b / n
    s = f(0.0) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(i * h)
    return s * h / 3.0


def shapes(rows, omega_m, a_r):
    def e(z):
        e2 = omega_m * (1.0 + z) ** 3 + 1.0 - omega_m + a_r * math.log1p(z)
        if e2 <= 0.0 or not math.isfinite(e2):
            raise ValueError
        return math.sqrt(e2)

    cache = {}
    out = []
    for z, _, kind in rows:
        if z not in cache:
            cache[z] = simpson(lambda x: 1.0 / e(x), z)
        dm = cache[z]
        dh = 1.0 / e(z)
        if kind == "DM_over_rs":
            out.append(dm)
        elif kind == "DH_over_rs":
            out.append(dh)
        elif kind == "DV_over_rs":
            out.append((z * dm * dm * dh) ** (1.0 / 3.0))
        else:
            raise RuntimeError(f"unknown BAO observable {kind}")
    return np.asarray(out, dtype=float)


def objective(rows, ci, omega_m, a_r):
    try:
        s = shapes(rows, omega_m, a_r)
    except ValueError:
        return float("inf"), float("nan")
    d = np.asarray([r[1] for r in rows], dtype=float)
    den = float(s @ ci @ s)
    if den <= 0.0 or not math.isfinite(den):
        return float("inf"), float("nan")
    q = float((s @ ci @ d) / den)
    residual = d - q * s
    return float(residual @ ci @ residual), q


def golden_min(fn, lo, hi, tol=1e-8):
    g = (math.sqrt(5.0) - 1.0) / 2.0
    c = hi - g * (hi - lo)
    d = lo + g * (hi - lo)
    fc, fd = fn(c), fn(d)
    while hi - lo > tol:
        if fc < fd:
            hi, d, fd = d, c, fc
            c = hi - g * (hi - lo)
            fc = fn(c)
        else:
            lo, c, fc = c, d, fd
            d = lo + g * (hi - lo)
            fd = fn(d)
    x = (lo + hi) / 2.0
    return x, fn(x)


def profile_ar(rows, ci, a_r):
    om, _ = golden_min(lambda x: objective(rows, ci, x, a_r)[0], *OMEGA_BOUNDS)
    chi, q = objective(rows, ci, om, a_r)
    return chi, om, q


def evaluate_branch(name, rows, cov):
    eig = np.linalg.eigvalsh(cov)
    min_eig = float(np.min(eig))
    if min_eig <= 0.0:
        return {"branch": name, "valid": False, "reason": "non_positive_definite", "min_cov_eigenvalue": min_eig}
    ci = np.linalg.inv(cov)
    chi0, om0, q0 = profile_ar(rows, ci, 0.0)
    profiles = []
    best = (float("inf"), None, None, None)
    n = int(round((AR_BOUNDS[1] - AR_BOUNDS[0]) / AR_STEP)) + 1
    for i in range(n):
        ar = AR_BOUNDS[0] + i * AR_STEP
        chi, om, q = profile_ar(rows, ci, ar)
        profiles.append((ar, chi, om, q))
        if chi < best[0]:
            best = (chi, ar, om, q)
    chi1, ar1, om1, q1 = best
    inside = [p for p in profiles if p[1] <= chi1 + 1.0]
    lo = inside[0][0] if inside else None
    hi = inside[-1][0] if inside else None
    zero_in = bool(lo is not None and hi is not None and lo <= 0.0 <= hi)
    boundary = bool(
        abs(om1 - OMEGA_BOUNDS[0]) < 1e-4
        or abs(om1 - OMEGA_BOUNDS[1]) < 1e-4
        or abs(ar1 - AR_BOUNDS[0]) < AR_STEP
        or abs(ar1 - AR_BOUNDS[1]) < AR_STEP
    )
    dchi = chi0 - chi1
    return {
        "branch": name,
        "valid": True,
        "nobs": len(rows),
        "min_cov_eigenvalue": min_eig,
        "LCDM": {"chi2": chi0, "Omega_m": om0, "q": q0},
        "RCMS": {"chi2": chi1, "Omega_m": om1, "A_R": ar1, "q": q1},
        "A_R_profile_delta_chi2_1": [lo, hi],
        "zero_in_profile": zero_in,
        "Delta_chi2": dchi,
        "Delta_AIC": dchi - 2.0,
        "boundary_contact": boundary,
    }


def subset(rows, cov, keep):
    idx = np.asarray(keep, dtype=int)
    return [rows[i] for i in idx], cov[np.ix_(idx, idx)]


def main():
    rows, cov = load_data()
    zs = [r[0] for r in rows]
    zmin, zmax = min(zs), max(zs)

    branches = []
    branches.append(("B0_full_covariance", rows, cov.copy()))
    branches.append(("B1_diagonal_only", rows, np.diag(np.diag(cov))))
    half = cov.copy()
    for i in range(len(rows)):
        for j in range(len(rows)):
            if i != j:
                half[i, j] *= 0.5
    branches.append(("B2_half_correlations", rows, half))

    keep_b3 = [i for i, r in enumerate(rows) if not math.isclose(r[0], zmin, rel_tol=0.0, abs_tol=1e-12)]
    keep_b4 = [i for i, r in enumerate(rows) if not math.isclose(r[0], zmax, rel_tol=0.0, abs_tol=1e-12)]
    keep_b5 = [i for i, r in enumerate(rows) if r[2] == "DH_over_rs"]
    keep_b6 = [i for i, r in enumerate(rows) if r[2] != "DH_over_rs"]
    branches.append(("B3_drop_min_redshift", *subset(rows, cov, keep_b3)))
    branches.append(("B4_drop_max_redshift", *subset(rows, cov, keep_b4)))
    branches.append(("B5_radial_only", *subset(rows, cov, keep_b5)))
    branches.append(("B6_transverse_volume_only", *subset(rows, cov, keep_b6)))

    results = [evaluate_branch(name, r, c) for name, r, c in branches]
    baseline = results[0]
    valid_nonbase = [r for r in results[1:] if r.get("valid")]
    invalid_count = sum(not r.get("valid", False) for r in results)

    if invalid_count > 1:
        classification = "SYSTEMATICS_INDETERMINATE"
    else:
        neg_majority = sum(r["RCMS"]["A_R"] < 0.0 for r in valid_nonbase) >= 4
        if neg_majority:
            classification = "SYSTEMATICS_SIGN_REVERSAL"
        else:
            positive_count = sum(r["RCMS"]["A_R"] > 0.0 for r in valid_nonbase)
            bad_negative = any(r["nobs"] >= 5 and r["RCMS"]["A_R"] < -0.05 for r in valid_nonbase)
            stable = baseline.get("valid") and baseline["RCMS"]["A_R"] > 0.0 and positive_count >= 5 and not bad_negative
            classification = "SYSTEMATICS_STABLE_POSITIVE" if stable else "SYSTEMATICS_SENSITIVE"

    payload = {
        "protocol": "P13",
        "status": "FINAL",
        "frozen_surrogate": "H_eff^2=H_LCDM^2+H0^2*A_R*ln(1+z)",
        "A_R_bounds": list(AR_BOUNDS),
        "A_R_step": AR_STEP,
        "Omega_m_bounds": list(OMEGA_BOUNDS),
        "zmin": zmin,
        "zmax": zmax,
        "branches": results,
        "classification": classification,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("RCMS Protocol 13 — Systematics and nuisance sensitivity")
    for r in results:
        if not r.get("valid"):
            print(f"{r['branch']}: INVALID reason={r['reason']}")
            continue
        print(
            f"{r['branch']}: N={r['nobs']} A_R={r['RCMS']['A_R']:.3f} "
            f"profile={r['A_R_profile_delta_chi2_1']} Delta_chi2={r['Delta_chi2']:.9f} "
            f"Delta_AIC={r['Delta_AIC']:.9f} zero_in={r['zero_in_profile']} boundary={r['boundary_contact']}"
        )
    print(f"P13_CLASSIFICATION={classification}")
    print(f"machine_readable={OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
