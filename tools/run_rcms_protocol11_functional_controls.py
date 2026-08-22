#!/usr/bin/env python3
"""RCMS Protocol 11 — preregistered equal-complexity functional controls."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEAN = ROOT / "data/rcms/desi_dr2_bao_all_mean.txt"
COV = ROOT / "data/rcms/desi_dr2_bao_all_cov.txt"
OUT = ROOT / "results/rcms_protocol11_functional_controls.json"

OMEGA_BOUNDS = (0.05, 0.60)
A_BOUNDS = (-5.0, 5.0)
A_STEP = 0.01
LN2 = math.log(2.0)


def load_data():
    rows = []
    for line in MEAN.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        z, val, kind = line.split()
        rows.append((float(z), float(val), kind))
    cov = [[float(x) for x in line.split()] for line in COV.read_text().splitlines() if line.strip()]
    if len(rows) != 13 or len(cov) != 13 or any(len(r) != 13 for r in cov):
        raise RuntimeError("DESI DR2 BAO frozen dimensions are not 13 / 13x13")
    return rows, cov


def invert(a):
    n = len(a)
    m = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(a)]
    for col in range(n):
        p = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[p][col]) < 1e-15:
            raise RuntimeError("singular covariance")
        m[col], m[p] = m[p], m[col]
        q = m[col][col]
        m[col] = [x / q for x in m[col]]
        for r in range(n):
            if r == col:
                continue
            f = m[r][col]
            if f:
                m[r] = [x - f * y for x, y in zip(m[r], m[col])]
    return [row[n:] for row in m]


def mv(a, x):
    return [sum(v * y for v, y in zip(row, x)) for row in a]


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def simpson(f, b, n=200):
    if n % 2:
        n += 1
    h = b / n
    s = f(0.0) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(i * h)
    return s * h / 3.0


def control(name, z):
    if name == "log":
        return math.log1p(z)
    if name == "linear":
        return LN2 * z
    if name == "saturating":
        return 2.0 * LN2 * z / (1.0 + z)
    if name == "sqrt":
        return LN2 * (math.sqrt(1.0 + z) - 1.0) / (math.sqrt(2.0) - 1.0)
    raise RuntimeError(f"unknown control {name}")


def shapes(rows, omega_m, amp, family):
    def e(z):
        e2 = omega_m * (1.0 + z) ** 3 + 1.0 - omega_m + amp * control(family, z)
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
    return out


def objective(rows, ci, omega_m, amp, family):
    try:
        s = shapes(rows, omega_m, amp, family)
    except ValueError:
        return float("inf"), float("nan")
    d = [r[1] for r in rows]
    cis = mv(ci, s)
    cid = mv(ci, d)
    den = dot(s, cis)
    if den <= 0.0 or not math.isfinite(den):
        return float("inf"), float("nan")
    q = dot(s, cid) / den
    residual = [x - q * y for x, y in zip(d, s)]
    chi2 = dot(residual, mv(ci, residual))
    return chi2, q


def golden_min(fn, lo, hi, tol=1e-8):
    g = (math.sqrt(5.0) - 1.0) / 2.0
    c = hi - g * (hi - lo)
    d = lo + g * (hi - lo)
    fc = fn(c)
    fd = fn(d)
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


def profile_amp(rows, ci, amp, family):
    om, _ = golden_min(lambda x: objective(rows, ci, x, amp, family)[0], *OMEGA_BOUNDS)
    chi, q = objective(rows, ci, om, amp, family)
    return chi, om, q


def evaluate(rows, ci, family, chi0, nobs):
    best = (float("inf"), None, None, None)
    profiles = []
    n = int(round((A_BOUNDS[1] - A_BOUNDS[0]) / A_STEP)) + 1
    for i in range(n):
        amp = A_BOUNDS[0] + i * A_STEP
        chi, om, q = profile_amp(rows, ci, amp, family)
        profiles.append((amp, chi, om, q))
        if chi < best[0]:
            best = (chi, amp, om, q)
    chi1, a1, om1, q1 = best
    target = chi1 + 1.0
    inside = [x for x in profiles if x[1] <= target]
    lo = inside[0][0] if inside else None
    hi = inside[-1][0] if inside else None
    boundary = (
        abs(om1 - OMEGA_BOUNDS[0]) < 1e-4
        or abs(om1 - OMEGA_BOUNDS[1]) < 1e-4
        or abs(a1 - A_BOUNDS[0]) < A_STEP
        or abs(a1 - A_BOUNDS[1]) < A_STEP
    )
    delta_chi2 = chi0 - chi1
    # LCDM has effective k=2 (q,Omega_m); each deformation k=3.
    delta_aic = delta_chi2 - 2.0
    delta_bic = delta_chi2 - math.log(nobs)
    return {
        "family": family,
        "chi2": chi1,
        "Omega_m": om1,
        "A": a1,
        "q": q1,
        "A_profile_delta_chi2_1": [lo, hi],
        "Delta_chi2_vs_LCDM": delta_chi2,
        "Delta_AIC_vs_LCDM": delta_aic,
        "Delta_BIC_vs_LCDM": delta_bic,
        "boundary_contact": boundary,
    }


def main():
    rows, cov = load_data()
    ci = invert(cov)
    if max(abs(cov[i][j] - cov[j][i]) for i in range(13) for j in range(13)) > 1e-12:
        raise RuntimeError("covariance is not symmetric")
    eye = max(
        abs(sum(cov[i][k] * ci[k][j] for k in range(13)) - (1.0 if i == j else 0.0))
        for i in range(13) for j in range(13)
    )
    if eye > 1e-8:
        raise RuntimeError("covariance inverse check failed")

    # A=0 is common to every shape.
    chi0, om0, q0 = profile_amp(rows, ci, 0.0, "log")
    families = ["log", "linear", "saturating", "sqrt"]
    results = [evaluate(rows, ci, f, chi0, len(rows)) for f in families]
    ranked = sorted(results, key=lambda r: r["chi2"])
    logrow = next(r for r in results if r["family"] == "log")
    controls = [r for r in results if r["family"] != "log"]
    best_ctrl = min(controls, key=lambda r: r["chi2"])
    gap = best_ctrl["chi2"] - logrow["chi2"]

    all_no_pref = all(r["Delta_AIC_vs_LCDM"] <= 0.0 for r in results)
    if abs(gap) < 2.0:
        classification = "FUNCTIONALLY_NON_SPECIFIC"
    elif gap >= 2.0 and ranked[0]["family"] == "log" and logrow["Delta_AIC_vs_LCDM"] > 0.0 and not logrow["boundary_contact"]:
        classification = "LOG_DISCRIMINATING"
    elif gap <= -2.0 and best_ctrl["chi2"] < logrow["chi2"] and not best_ctrl["boundary_contact"]:
        classification = "CONTROL_PREFERRED"
    else:
        classification = "FUNCTIONALLY_NON_SPECIFIC"

    payload = {
        "protocol": "P11",
        "status": "FINAL",
        "model_channel": "E2 additive one-parameter deformation",
        "pivot_z": 1.0,
        "normalization": "f(0)=0 and f(1)=ln(2)",
        "LCDM": {"chi2": chi0, "Omega_m": om0, "q": q0},
        "models": results,
        "ranking": [r["family"] for r in ranked],
        "best_nonlog_control": best_ctrl["family"],
        "Delta_chi2_log_minus_control_definition": "chi2_best_control - chi2_log",
        "Delta_chi2_log_ctrl": gap,
        "classification": classification,
        "NO_DEFORMATION_PREFERENCE": all_no_pref,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("RCMS Protocol 11 — Equal-complexity functional controls")
    print(f"LCDM chi2={chi0:.9f} Omega_m={om0:.9f} q={q0:.9f}")
    for r in ranked:
        print(
            f"{r['family']}: chi2={r['chi2']:.9f} A={r['A']:.3f} "
            f"Omega_m={r['Omega_m']:.9f} q={r['q']:.9f} "
            f"profile={r['A_profile_delta_chi2_1']} "
            f"Delta_chi2={r['Delta_chi2_vs_LCDM']:.9f} "
            f"Delta_AIC={r['Delta_AIC_vs_LCDM']:.9f} "
            f"Delta_BIC={r['Delta_BIC_vs_LCDM']:.9f} "
            f"boundary={r['boundary_contact']}"
        )
    print(f"BEST_NONLOG_CONTROL={best_ctrl['family']}")
    print(f"DELTA_CHI2_LOG_CTRL={gap:.9f}")
    print(f"P11_CLASSIFICATION={classification}")
    print(f"NO_DEFORMATION_PREFERENCE={all_no_pref}")
    print(f"machine_readable={OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
