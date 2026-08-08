#!/usr/bin/env python3
"""Preregistered RCMS Protocol 01 H(z)-only production fit.

This script uses the exact 15-point Moresco BC03 table and reproduces the
public Moresco et al. (2020) covariance prescription before evaluating the
flat-LambdaCDM and one-parameter effective RCMS models.

No third-party dependencies are required.
"""
from __future__ import annotations

import csv
from math import exp, isfinite, log, log1p, sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "rcms" / "cc_hz_moresco_bc03_v1.csv"
SYS = ROOT / "data" / "rcms" / "cc_systematics_moresco2020_v1.csv"

H0_MIN, H0_MAX = 40.0, 100.0
OM_MIN, OM_MAX = 0.05, 0.60
A_MIN, A_MAX = -5.0, 5.0
A_STEP = 0.01
GOLDEN_TOL = 2.0e-7
PUBLISHED_DET = 4.560e33
DET_REL_TOL = 5.0e-4


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def interp_const(x, xs, ys):
    if x <= xs[0]:
        return ys[0]
    if x >= xs[-1]:
        return ys[-1]
    lo, hi = 0, len(xs) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if xs[mid] <= x:
            lo = mid
        else:
            hi = mid
    t = (x - xs[lo]) / (xs[hi] - xs[lo])
    return ys[lo] + t * (ys[hi] - ys[lo])


def cholesky(a):
    n = len(a)
    l = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(l[i][k] * l[j][k] for k in range(j))
            if i == j:
                v = a[i][i] - s
                if v <= 0.0:
                    raise RuntimeError("covariance is not positive definite")
                l[i][j] = sqrt(v)
            else:
                l[i][j] = (a[i][j] - s) / l[j][j]
    return l


def solve_cholesky(l, b):
    n = len(l)
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(l[i][k] * y[k] for k in range(i))) / l[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(l[k][i] * x[k] for k in range(i + 1, n))) / l[i][i]
    return x


def inverse_from_cholesky(l):
    n = len(l)
    inv = [[0.0] * n for _ in range(n)]
    for j in range(n):
        e = [0.0] * n
        e[j] = 1.0
        col = solve_cholesky(l, e)
        for i in range(n):
            inv[i][j] = col[i]
    return inv


def matvec(a, x):
    return [sum(row[j] * x[j] for j in range(len(x))) for row in a]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def build_covariance():
    obs = read_csv(DATA)
    syst = read_csv(SYS)
    z = [float(r["z"]) for r in obs]
    h = [float(r["H_km_s_Mpc"]) for r in obs]
    sig = [float(r["sigma_km_s_Mpc"]) for r in obs]
    zs = [float(r["z"]) for r in syst]
    imf = [float(r["imf_percent"]) / 100.0 for r in syst]
    spsooo = [float(r["spsooo_percent"]) / 100.0 for r in syst]

    u = [h[i] * interp_const(z[i], zs, imf) for i in range(len(z))]
    v = [h[i] * interp_const(z[i], zs, spsooo) for i in range(len(z))]
    n = len(z)
    cov = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cov[i][j] = u[i] * u[j] + v[i] * v[j]
            if i == j:
                cov[i][j] += sig[i] ** 2
    return z, h, sig, cov


def covariance_checks(cov):
    n = len(cov)
    max_asym = max(abs(cov[i][j] - cov[j][i]) for i in range(n) for j in range(n))
    if max_asym > 1.0e-10:
        raise RuntimeError(f"covariance asymmetry too large: {max_asym}")
    l = cholesky(cov)
    logdet = 2.0 * sum(log(l[i][i]) for i in range(n))
    det = exp(logdet)
    rel = abs(det - PUBLISHED_DET) / PUBLISHED_DET
    if rel > DET_REL_TOL:
        raise RuntimeError(f"determinant mismatch: got {det:.6e}, reference {PUBLISHED_DET:.6e}")
    inv = inverse_from_cholesky(l)
    max_identity_err = 0.0
    for i in range(n):
        for j in range(n):
            val = sum(cov[i][k] * inv[k][j] for k in range(n))
            target = 1.0 if i == j else 0.0
            max_identity_err = max(max_identity_err, abs(val - target))
    if max_identity_err > 1.0e-9:
        raise RuntimeError(f"inverse residual too large: {max_identity_err:.3e}")
    return inv, det, rel, max_identity_err


def model_shape(z, om, a_r):
    out = []
    for zz in z:
        e2 = om * (1.0 + zz) ** 3 + (1.0 - om) + a_r * log1p(zz)
        if e2 <= 0.0 or not isfinite(e2):
            return None
        out.append(sqrt(e2))
    return out


def profile_h0(shape, h, inv):
    wh = matvec(inv, h)
    wf = matvec(inv, shape)
    denom = dot(shape, wf)
    if denom <= 0.0:
        return float("inf"), None, True
    h0 = dot(shape, wh) / denom
    boundary = False
    if h0 < H0_MIN:
        h0, boundary = H0_MIN, True
    elif h0 > H0_MAX:
        h0, boundary = H0_MAX, True
    r = [h[i] - h0 * shape[i] for i in range(len(h))]
    chi2 = dot(r, matvec(inv, r))
    return chi2, h0, boundary


def objective_om(om, a_r, z, h, inv):
    if not (OM_MIN <= om <= OM_MAX):
        return float("inf"), None, True
    shape = model_shape(z, om, a_r)
    if shape is None:
        return float("inf"), None, True
    return profile_h0(shape, h, inv)


def minimize_om(a_r, z, h, inv):
    # Deterministic bounded golden-section search. Endpoint values are retained
    # so a genuine boundary optimum cannot be hidden by the interior search.
    phi = (sqrt(5.0) - 1.0) / 2.0
    lo, hi = OM_MIN, OM_MAX
    c = hi - phi * (hi - lo)
    d = lo + phi * (hi - lo)
    fc = objective_om(c, a_r, z, h, inv)[0]
    fd = objective_om(d, a_r, z, h, inv)[0]
    for _ in range(120):
        if hi - lo <= GOLDEN_TOL:
            break
        if fc <= fd:
            hi, d, fd = d, c, fc
            c = hi - phi * (hi - lo)
            fc = objective_om(c, a_r, z, h, inv)[0]
        else:
            lo, c, fc = c, d, fd
            d = lo + phi * (hi - lo)
            fd = objective_om(d, a_r, z, h, inv)[0]
    candidates = [OM_MIN, OM_MAX, (lo + hi) / 2.0]
    best = (float("inf"), None, None, True)
    for om in candidates:
        chi2, h0, h0_bound = objective_om(om, a_r, z, h, inv)
        om_bound = abs(om - OM_MIN) < 1e-8 or abs(om - OM_MAX) < 1e-8
        candidate = (chi2, om, h0, h0_bound or om_bound)
        if candidate[0] < best[0]:
            best = candidate
    return best


def profile_grid(z, h, inv):
    n_steps = int(round((A_MAX - A_MIN) / A_STEP))
    rows = []
    best = (float("inf"), None, None, None, True)
    for k in range(n_steps + 1):
        a_r = A_MIN + k * A_STEP
        chi2, om, h0, boundary = minimize_om(a_r, z, h, inv)
        rows.append((a_r, chi2, om, h0, boundary))
        if chi2 < best[0]:
            best = (chi2, a_r, om, h0, boundary)
    return rows, best


def profile_interval(rows, minimum, delta=1.0):
    accepted = [r for r in rows if r[1] <= minimum + delta]
    if not accepted:
        return None, None
    return accepted[0][0], accepted[-1][0]


def main():
    z, h, sig, cov = build_covariance()
    if len(z) != 15:
        raise RuntimeError(f"expected 15 covariance-compatible points, found {len(z)}")
    inv, det, det_rel, inv_err = covariance_checks(cov)

    ref_chi2, ref_om, ref_h0, ref_boundary = minimize_om(0.0, z, h, inv)
    rows, best = profile_grid(z, h, inv)
    rc_chi2, a_r, rc_om, rc_h0, rc_boundary = best
    a_lo, a_hi = profile_interval(rows, rc_chi2, 1.0)

    n = len(z)
    delta_chi2 = ref_chi2 - rc_chi2
    aic_ref = ref_chi2 + 2.0 * 2
    aic_rc = rc_chi2 + 2.0 * 3
    bic_ref = ref_chi2 + 2.0 * log(n)
    bic_rc = rc_chi2 + 3.0 * log(n)
    delta_aic = aic_ref - aic_rc
    delta_bic = bic_ref - bic_rc

    if a_lo is not None and a_lo <= 0.0 <= a_hi:
        stage_decision = "NO_PREFERENCE"
    elif delta_aic > 0.0 and delta_bic > 0.0:
        stage_decision = "RCMS_SCREENING_CANDIDATE_HZ_ONLY"
    elif delta_aic < 0.0 and delta_bic < 0.0:
        stage_decision = "REFERENCE_FAVORED_HZ_ONLY"
    else:
        stage_decision = "NO_PREFERENCE"

    print("[RCMS Protocol 01: real H(z)-only production]")
    print(f"  dataset=RCMS-DATA-CC-MORESCO-BC03-v1 n={n} z=[{min(z):.4f},{max(z):.3f}]")
    print(f"  covariance determinant={det:.6e} reference={PUBLISHED_DET:.6e} rel_error={det_rel:.3e}")
    print(f"  covariance inverse_max_residual={inv_err:.3e} positive_definite=yes")
    print(f"  frozen_bounds H0=[{H0_MIN:.1f},{H0_MAX:.1f}] Omega_m=[{OM_MIN:.2f},{OM_MAX:.2f}] A_R=[{A_MIN:.1f},{A_MAX:.1f}]")
    print("  [flat-LambdaCDM]")
    print(f"    chi2={ref_chi2:.6f} H0={ref_h0:.6f} Omega_m={ref_om:.6f} boundary={str(ref_boundary).lower()}")
    print("  [RCMS-effective]")
    print(f"    chi2={rc_chi2:.6f} H0={rc_h0:.6f} Omega_m={rc_om:.6f} A_R={a_r:.4f} boundary={str(rc_boundary).lower()}")
    print(f"    A_R_profile_delta_chi2_1=[{a_lo:.2f},{a_hi:.2f}]")
    print(f"  delta_chi2={delta_chi2:.6f}")
    print(f"  AIC_ref={aic_ref:.6f} AIC_rcms={aic_rc:.6f} delta_AIC_ref_minus_rcms={delta_aic:.6f}")
    print(f"  BIC_ref={bic_ref:.6f} BIC_rcms={bic_rc:.6f} delta_BIC_ref_minus_rcms={delta_bic:.6f}")
    print(f"  HZ_STAGE_DECISION={stage_decision}")
    print("  note=This is the first H(z)-only stage, not the final multi-probe Protocol 01 decision.")


if __name__ == "__main__":
    main()
