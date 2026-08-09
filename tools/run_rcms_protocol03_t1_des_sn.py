#!/usr/bin/env python3
"""RCMS Protocol 03 T1: external replication with DES-SN5YR/Dovekie.

The model is frozen from Protocols 01/02. DES-SN is treated as a relative-
distance probe: the additive SN intercept is analytically marginalized, so
H0 is not inferred from this stage.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import minimize, minimize_scalar, brentq

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "external" / "des_sn5yr"
HD = DATA_DIR / "DES-Dovekie_HD.csv"
PRECISION_NPZ = DATA_DIR / "STAT+SYS.npz"

OM_BOUNDS = (0.05, 0.60)
AR_BOUNDS = (-5.0, 5.0)
C_KM_S = 299792.458
H0_FIXED = 70.0  # arbitrary here; fully absorbed by the marginalized intercept


def read_hd():
    rows = []
    names = None
    for raw in HD.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("VARNAMES:"):
            names = line.split()[1:]
            continue
        if line.startswith("SN:"):
            vals = line.split()[1:]
            if names is None or len(vals) != len(names):
                raise RuntimeError("malformed DES-SN Hubble diagram")
            rows.append(dict(zip(names, vals)))
    if not rows:
        raise RuntimeError("no DES-SN rows loaded")
    zcmb = np.array([float(r["zHD"]) for r in rows])
    zhel = np.array([float(r["zHEL"]) for r in rows])
    mu = np.array([float(r["MU"]) for r in rows])
    mask = zcmb > 0.0
    return zcmb[mask], zhel[mask], mu[mask]


def load_precision(n_expected: int):
    d = np.load(PRECISION_NPZ)
    if len(d.files) < 2:
        raise RuntimeError("unexpected DES precision-matrix npz structure")
    n = int(np.asarray(d[d.files[0]]).ravel()[0])
    if n != n_expected:
        raise RuntimeError(f"precision dimension {n} != Hubble diagram length {n_expected}")
    upper = np.asarray(d[d.files[1]], dtype=float)
    expected_upper = n * (n + 1) // 2
    if upper.size != expected_upper:
        raise RuntimeError(f"upper triangle length {upper.size} != expected {expected_upper}")
    p = np.zeros((n, n), dtype=float)
    iu = np.triu_indices(n)
    p[iu] = upper
    p[(iu[1], iu[0])] = upper
    if not np.allclose(p, p.T, rtol=0.0, atol=1e-12):
        raise RuntimeError("precision matrix is not symmetric")
    eig_min = float(np.linalg.eigvalsh(p)[0])
    if eig_min <= 0.0:
        raise RuntimeError(f"precision matrix not positive definite; lambda_min={eig_min}")
    return p, eig_min


def e_of_z(z, om, ar):
    e2 = om * (1.0 + z) ** 3 + (1.0 - om) + ar * np.log1p(z)
    if np.any(e2 <= 0.0) or not np.all(np.isfinite(e2)):
        raise ValueError("non-positive E^2")
    return np.sqrt(e2)


def mu_theory(zcmb, zhel, om, ar):
    # Dense common integration grid; the arbitrary H0 normalization is removed
    # by analytic intercept marginalization.
    zmax = float(np.max(zcmb))
    grid = np.linspace(0.0, zmax, 5000)
    inv_e = 1.0 / e_of_z(grid, om, ar)
    dc = cumulative_trapezoid(inv_e, grid, initial=0.0) * (C_KM_S / H0_FIXED)
    dc_i = np.interp(zcmb, grid, dc)
    da = dc_i / (1.0 + zcmb)
    arg = (1.0 + zcmb) * (1.0 + zhel) * da
    if np.any(arg <= 0.0):
        raise ValueError("non-positive luminosity-distance argument")
    return 5.0 * np.log10(arg) + 25.0


def marginalized_chi2(mu_model, mu_obs, precision):
    # Exact upstream Eq. A9-A12 implementation. Constants independent of the
    # cosmological model are retained, but cancel in Delta chi2.
    delta = mu_model - mu_obs
    p_delta = precision @ delta
    chit2 = float(delta @ p_delta)
    b = float(np.sum(p_delta))
    c = float(np.sum(precision))
    if c <= 0.0:
        raise RuntimeError("invalid intercept curvature C")
    return chit2 - b * b / c + math.log(c / (2.0 * math.pi))


def objective(x, zcmb, zhel, mu_obs, precision, ar_fixed=None):
    if ar_fixed is None:
        om, ar = float(x[0]), float(x[1])
    else:
        om, ar = float(x[0]), float(ar_fixed)
    if not (OM_BOUNDS[0] <= om <= OM_BOUNDS[1] and AR_BOUNDS[0] <= ar <= AR_BOUNDS[1]):
        return 1e100
    try:
        model = mu_theory(zcmb, zhel, om, ar)
    except ValueError:
        return 1e100
    return marginalized_chi2(model, mu_obs, precision)


def fit_reference(zcmb, zhel, mu_obs, precision):
    res = minimize_scalar(
        lambda om: objective([om], zcmb, zhel, mu_obs, precision, ar_fixed=0.0),
        bounds=OM_BOUNDS,
        method="bounded",
        options={"xatol": 1e-9},
    )
    return float(res.fun), float(res.x)


def fit_rcms(zcmb, zhel, mu_obs, precision):
    best = None
    for start in ((0.30, 0.0), (0.30, 0.2), (0.25, -0.2), (0.40, 0.5)):
        res = minimize(
            objective,
            np.array(start, dtype=float),
            args=(zcmb, zhel, mu_obs, precision),
            method="Nelder-Mead",
            options={"xatol": 1e-8, "fatol": 1e-8, "maxiter": 4000},
        )
        if best is None or res.fun < best.fun:
            best = res
    return float(best.fun), float(best.x[0]), float(best.x[1])


def profile_om(ar, zcmb, zhel, mu_obs, precision):
    res = minimize_scalar(
        lambda om: objective([om], zcmb, zhel, mu_obs, precision, ar_fixed=ar),
        bounds=OM_BOUNDS,
        method="bounded",
        options={"xatol": 2e-8},
    )
    return float(res.fun)


def profile_interval(ar_best, chi_best, zcmb, zhel, mu_obs, precision):
    target = chi_best + 1.0
    def f(a):
        return profile_om(a, zcmb, zhel, mu_obs, precision) - target
    lo = AR_BOUNDS[0]
    hi = AR_BOUNDS[1]
    # bracket on fixed grids, then root-find; boundary means the interval is open.
    left_grid = np.linspace(lo, ar_best, 120)
    right_grid = np.linspace(ar_best, hi, 120)
    left = lo
    for a0, a1 in zip(left_grid[:-1], left_grid[1:]):
        if f(a0) * f(a1) <= 0:
            left = float(brentq(f, a0, a1))
    right = hi
    for a0, a1 in zip(right_grid[:-1], right_grid[1:]):
        if f(a0) * f(a1) <= 0:
            right = float(brentq(f, a0, a1))
            break
    return left, right


def main():
    zcmb, zhel, mu_obs = read_hd()
    precision, eig_min = load_precision(len(mu_obs))

    # Likelihood convention self-check: adding any constant magnitude offset to
    # the theory must not change the analytically marginalized chi-square.
    probe = mu_theory(zcmb, zhel, 0.30, 0.0)
    q0 = marginalized_chi2(probe, mu_obs, precision)
    q1 = marginalized_chi2(probe + 7.123, mu_obs, precision)
    offset_invariance = abs(q1 - q0)
    if offset_invariance > 1e-7:
        raise RuntimeError(f"intercept marginalization check failed: {offset_invariance:.3e}")

    chi0, om0 = fit_reference(zcmb, zhel, mu_obs, precision)
    chi1, om1, ar1 = fit_rcms(zcmb, zhel, mu_obs, precision)
    ar_lo, ar_hi = profile_interval(ar1, chi1, zcmb, zhel, mu_obs, precision)

    n = len(mu_obs)
    # SN-only identifiable cosmological shape parameters: Omega_m; RCMS adds A_R.
    delta = chi0 - chi1
    delta_aic = (chi0 + 2.0 * 1) - (chi1 + 2.0 * 2)
    delta_bic = (chi0 + math.log(n) * 1) - (chi1 + math.log(n) * 2)

    if ar_lo > 0.0 and ar1 > 0.0:
        sign_label = "POSITIVE_EXTERNAL_REGION"
    elif ar_hi < 0.0 and ar1 < 0.0:
        sign_label = "NEGATIVE_EXTERNAL_REGION"
    else:
        sign_label = "ZERO_COMPATIBLE_EXTERNAL_REGION"

    print("RCMS Protocol 03 — P03-T1 DES-SN5YR/Dovekie external replication")
    print(f"N={n} z=[{zcmb.min():.5f},{zcmb.max():.5f}]")
    print(f"precision_lambda_min={eig_min:.6e} offset_invariance_error={offset_invariance:.3e}")
    print(f"LCDM: chi2={chi0:.6f} Omega_m={om0:.6f}")
    print(f"RCMS: chi2={chi1:.6f} Omega_m={om1:.6f} A_R={ar1:.6f}")
    print(f"A_R_profile_delta_chi2_1=[{ar_lo:.6f},{ar_hi:.6f}]")
    print(f"Delta_chi2_LCDM_minus_RCMS={delta:.6f}")
    print(f"Delta_AIC_LCDM_minus_RCMS={delta_aic:.6f}")
    print(f"Delta_BIC_LCDM_minus_RCMS={delta_bic:.6f}")
    print(f"P03_T1_SIGN={sign_label}")
    print("note=External replication stage only; this output does not validate Resolutive Cosmology.")


if __name__ == "__main__":
    main()
