#!/usr/bin/env python3
"""RCMS Protocol 04 P04-T0: eBOSS DR16 Lambda-CDM and identifiability gate.

This program intentionally contains no RCMS A_R model. It validates the frozen
multi-redshift BAO likelihood and establishes that a free global BAO scale does
not erase all late-time shape information.
"""

from __future__ import annotations

import math
import pathlib

import numpy as np
from scipy.integrate import quad
from scipy.interpolate import RectBivariateSpline
from scipy.optimize import minimize_scalar

DATA = pathlib.Path("data/external/eboss_dr16")
OM_BOUNDS = (0.10, 0.50)
Q_BOUNDS = (20.0, 45.0)
PROFILE_GRID = np.linspace(0.12, 0.48, 19)
PROFILE_SPAN_MIN = 1.0e-3


def e_lcdm(z: float, omega_m: float) -> float:
    return math.sqrt(omega_m * (1.0 + z) ** 3 + 1.0 - omega_m)


def dm_shape(z: float, omega_m: float) -> float:
    value, _ = quad(lambda zz: 1.0 / e_lcdm(zz, omega_m), 0.0, z, epsabs=2e-11, epsrel=2e-11)
    return value


def prediction(z: float, omega_m: float, q: float) -> np.ndarray:
    return np.array([q * dm_shape(z, omega_m), q / e_lcdm(z, omega_m)])


def load_gaussian(measurement: str, covariance: str):
    rows = []
    for raw in (DATA / measurement).read_text().splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        parts = raw.split()
        rows.append((float(parts[0]), float(parts[1]), parts[2]))
    if len(rows) != 2 or rows[0][0] != rows[1][0]:
        raise RuntimeError(f"unexpected measurement layout in {measurement}")
    obs = [r[2] for r in rows]
    if obs != ["DM_over_rs", "DH_over_rs"]:
        raise RuntimeError(f"unexpected observable order in {measurement}: {obs}")
    z = rows[0][0]
    mean = np.array([r[1] for r in rows], dtype=float)
    cov = np.loadtxt(DATA / covariance)
    if cov.shape != (2, 2) or not np.allclose(cov, cov.T, rtol=0, atol=1e-12):
        raise RuntimeError(f"invalid covariance in {covariance}")
    eig = np.linalg.eigvalsh(cov)
    if eig.min() <= 0:
        raise RuntimeError(f"non-positive covariance in {covariance}")
    return z, mean, np.linalg.inv(cov), eig


def load_lya_grid():
    grid = np.loadtxt(DATA / "sdss_DR16_LYAUTO_BAO_DMDHgrid.txt")
    if grid.ndim != 2 or grid.shape[1] != 3 or np.any(grid[:, 2] <= 0):
        raise RuntimeError("invalid Lyman-alpha grid")
    x = np.unique(grid[:, 0])
    y = np.unique(grid[:, 1])
    if x.size * y.size != grid.shape[0]:
        raise RuntimeError("Lyman-alpha grid is not rectangular")
    logp = np.log(grid[:, 2]).reshape(x.size, y.size)
    interp = RectBivariateSpline(x, y, logp, kx=3, ky=3)
    return x, y, logp, interp


LRG_Z, LRG_MEAN, LRG_INV, LRG_EIG = load_gaussian(
    "sdss_DR16_LRG_BAO_DMDH.dat", "sdss_DR16_LRG_BAO_DMDH_covtot.txt"
)
QSO_Z, QSO_MEAN, QSO_INV, QSO_EIG = load_gaussian(
    "sdss_DR16_QSO_BAO_DMDH.txt", "sdss_DR16_QSO_BAO_DMDH_covtot.txt"
)
LYA_X, LYA_Y, LYA_LOGP, LYA_INTERP = load_lya_grid()
LYA_Z = 2.334
LYA_LOGP_MAX = float(np.max(LYA_LOGP))


def gaussian_chi2(pred: np.ndarray, mean: np.ndarray, inv: np.ndarray) -> float:
    d = pred - mean
    return float(d @ inv @ d)


def lya_chi2(pred: np.ndarray) -> float:
    dm, dh = map(float, pred)
    if not (LYA_X[0] <= dm <= LYA_X[-1] and LYA_Y[0] <= dh <= LYA_Y[-1]):
        return 1.0e9
    logp = float(LYA_INTERP(dm, dh)[0, 0])
    return -2.0 * (logp - LYA_LOGP_MAX)


def total_chi2(omega_m: float, q: float) -> float:
    if not (OM_BOUNDS[0] <= omega_m <= OM_BOUNDS[1] and Q_BOUNDS[0] <= q <= Q_BOUNDS[1]):
        return 1.0e12
    return (
        gaussian_chi2(prediction(LRG_Z, omega_m, q), LRG_MEAN, LRG_INV)
        + gaussian_chi2(prediction(QSO_Z, omega_m, q), QSO_MEAN, QSO_INV)
        + lya_chi2(prediction(LYA_Z, omega_m, q))
    )


def profile_q(omega_m: float):
    result = minimize_scalar(
        lambda q: total_chi2(omega_m, float(q)),
        bounds=Q_BOUNDS,
        method="bounded",
        options={"xatol": 2e-10, "maxiter": 500},
    )
    if not result.success:
        raise RuntimeError(f"q profiling failed at Omega_m={omega_m}: {result.message}")
    return float(result.fun), float(result.x)


def main() -> None:
    lrg_zero = gaussian_chi2(LRG_MEAN, LRG_MEAN, LRG_INV)
    qso_zero = gaussian_chi2(QSO_MEAN, QSO_MEAN, QSO_INV)
    lya_grid_min = float(np.min(-2.0 * (LYA_LOGP - LYA_LOGP_MAX)))
    if abs(lrg_zero) > 1e-12 or abs(qso_zero) > 1e-12 or abs(lya_grid_min) > 1e-12:
        raise SystemExit("upstream likelihood convention gate failed")

    result = minimize_scalar(
        lambda om: profile_q(float(om))[0],
        bounds=OM_BOUNDS,
        method="bounded",
        options={"xatol": 2e-8, "maxiter": 300},
    )
    if not result.success:
        raise SystemExit(f"Lambda-CDM shape optimization failed: {result.message}")
    omega_best = float(result.x)
    chi2_best, q_best = profile_q(omega_best)

    margin_om = min(omega_best - OM_BOUNDS[0], OM_BOUNDS[1] - omega_best)
    margin_q = min(q_best - Q_BOUNDS[0], Q_BOUNDS[1] - q_best)
    if margin_om < 1e-3 or margin_q < 1e-3:
        raise SystemExit("Lambda-CDM optimum is boundary-limited")

    profile = []
    for om in PROFILE_GRID:
        chi2, q = profile_q(float(om))
        profile.append((float(om), chi2, q))
    profile_chi2 = np.array([row[1] for row in profile])
    profile_span = float(np.max(profile_chi2) - np.min(profile_chi2))
    if not np.isfinite(profile_span) or profile_span <= PROFILE_SPAN_MIN:
        raise SystemExit(f"shape identifiability gate failed: profile_span={profile_span:.8g}")

    print("RCMS Protocol 04 — P04-T0 eBOSS DR16 baseline gate")
    print("RCMS_PARAMETER_EVALUATED=NO")
    print(f"LRG_z={LRG_Z:.3f} covariance_lambda_min={LRG_EIG.min():.9g}")
    print(f"QSO_z={QSO_Z:.3f} covariance_lambda_min={QSO_EIG.min():.9g}")
    print(
        f"LYA_z={LYA_Z:.3f} grid_shape={LYA_X.size}x{LYA_Y.size} "
        f"DM_range=[{LYA_X[0]:.6f},{LYA_X[-1]:.6f}] "
        f"DH_range=[{LYA_Y[0]:.6f},{LYA_Y[-1]:.6f}]"
    )
    print("UPSTREAM_LIKELIHOOD_CONVENTION=PASS")
    print(f"LCDM_Omega_m={omega_best:.9f}")
    print(f"LCDM_q_c_over_H0rd={q_best:.9f}")
    print(f"LCDM_chi2_relative={chi2_best:.9f}")
    print(f"PROFILE_OMEGA_M_SPAN_DELTA_CHI2={profile_span:.9f}")
    print("P04_T0_SHAPE_IDENTIFIABILITY=PASS")
    print("P04_T0_STATUS=READY_FOR_PREREGISTERED_RCMS_REVEAL")


if __name__ == "__main__":
    main()
