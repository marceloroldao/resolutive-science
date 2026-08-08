#!/usr/bin/env python3
"""Run the preregistered Pantheon+ SN-alone comparison for RCMS Protocol 01.

Run ``tools/fetch_rcms_pantheonplus.py`` first. That acquisition tool pins and
verifies the exact upstream Git blobs; this runner never substitutes a diagonal
or reconstructed covariance.

Likelihood semantics reproduce the frozen Cobaya PantheonPlus likelihood
(without SH0ES): zCMB > 0.01, the full masked covariance, no Cepheid-host
override, and one additive supernova intercept marginalized in both models.
"""
from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

try:
    import numpy as np
    from scipy.integrate import cumulative_simpson
    from scipy.linalg import cho_factor, cho_solve
    from scipy.optimize import minimize_scalar
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Pantheon+ production fitting requires numpy and scipy in the "
        "observational-analysis environment."
    ) from exc

C_KM_S = 299792.458
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = ROOT / "data" / "external" / "pantheonplus_v1"

OMEGA_MIN = 0.05
OMEGA_MAX = 0.60
A_MIN = -5.0
A_MAX = 5.0
FIXED_H0 = 70.0  # exactly degenerate with the marginalized SN intercept
DISTANCE_GRID_POINTS = 8193


@dataclass(frozen=True)
class FitResult:
    chi2: float
    omega_m: float
    a_r: float
    intercept: float


def read_pantheon_table(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    lines = path.read_text().splitlines()
    if not lines:
        raise RuntimeError("empty Pantheon+ data file")
    header = lines[0].lstrip("#").split()
    idx = {name: header.index(name) for name in ("m_b_corr", "zHD", "zHEL")}
    rows = [line.split() for line in lines[1:] if line.strip()]
    mag = np.asarray([float(row[idx["m_b_corr"]]) for row in rows], dtype=float)
    zcmb = np.asarray([float(row[idx["zHD"]]) for row in rows], dtype=float)
    zhel = np.asarray([float(row[idx["zHEL"]]) for row in rows], dtype=float)
    if len(mag) != 1701:
        raise RuntimeError(f"expected 1701 Pantheon+ rows, found {len(mag)}")
    return mag, zcmb, zhel


def read_covariance(path: Path) -> np.ndarray:
    raw = np.loadtxt(path)
    n = int(raw[0])
    if n != 1701 or len(raw) != n * n + 1:
        raise RuntimeError(
            f"invalid Pantheon+ covariance structure: n={n}, entries={len(raw)-1}"
        )
    cov = raw[1:].reshape((n, n))
    if not np.all(np.isfinite(cov)):
        raise RuntimeError("Pantheon+ covariance contains non-finite values")
    return cov


def distance_integrals(zcmb: np.ndarray, omega_m: float, a_r: float) -> np.ndarray:
    """Return integral_0^z dx/E(x) on a deterministic dense Simpson grid."""
    zmax = float(np.max(zcmb))
    grid = np.linspace(0.0, zmax, DISTANCE_GRID_POINTS)
    e2 = omega_m * (1.0 + grid) ** 3 + (1.0 - omega_m) + a_r * np.log1p(grid)
    if np.any(e2 <= 0.0) or not np.all(np.isfinite(e2)):
        raise ValueError("non-positive or non-finite E(z)^2")
    cumulative = cumulative_simpson(1.0 / np.sqrt(e2), x=grid, initial=0.0)
    return np.interp(zcmb, grid, cumulative)


def pantheon_lumdists(
    zcmb: np.ndarray, zhel: np.ndarray, omega_m: float, a_r: float
) -> np.ndarray:
    """Cobaya-compatible uncalibrated SN distance quantity.

    Cobaya evaluates
      5 log10[(1+zhel)(1+zcmb) D_A(zcmb)].
    In the flat background D_A=D_M/(1+zcmb), hence this is
      5 log10[(1+zhel) D_M].
    The H0-dependent common scale is removed by intercept marginalization.
    """
    integrals = distance_integrals(zcmb, omega_m, a_r)
    dm = (C_KM_S / FIXED_H0) * integrals
    argument = (1.0 + zhel) * dm
    if np.any(argument <= 0.0):
        raise ValueError("non-positive luminosity-distance argument")
    return 5.0 * np.log10(argument)


class MarginalizedSN:
    def __init__(
        self, mag: np.ndarray, zcmb: np.ndarray, zhel: np.ndarray, cov: np.ndarray
    ) -> None:
        if cov.shape != (len(mag), len(mag)):
            raise RuntimeError("masked covariance shape does not match masked data")
        if not np.allclose(cov, cov.T, rtol=0.0, atol=1e-10):
            raise RuntimeError("masked covariance is not symmetric")
        self.mag = mag
        self.zcmb = zcmb
        self.zhel = zhel
        self.factor = cho_factor(cov, lower=True, check_finite=True)
        self.ones = np.ones(len(mag), dtype=float)
        self.cinv_ones = cho_solve(self.factor, self.ones, check_finite=False)
        self.ones_cinv_ones = float(self.ones @ self.cinv_ones)
        if self.ones_cinv_ones <= 0.0:
            raise RuntimeError("invalid intercept Fisher information")

    def chi2(self, omega_m: float, a_r: float) -> tuple[float, float]:
        theory = pantheon_lumdists(self.zcmb, self.zhel, omega_m, a_r)
        residual = self.mag - theory
        cinv_r = cho_solve(self.factor, residual, check_finite=False)
        intercept = float(self.ones @ cinv_r / self.ones_cinv_ones)
        # Algebraically identical to projecting C^-1 orthogonally to the
        # constant-intercept direction, as done by frozen Cobaya PantheonPlus.
        chi2 = float(
            residual @ cinv_r
            - (self.ones @ cinv_r) ** 2 / self.ones_cinv_ones
        )
        return chi2, intercept


def bounded_minimize(
    fn: Callable[[float], float], low: float, high: float
) -> tuple[float, float]:
    result = minimize_scalar(
        fn, bounds=(low, high), method="bounded", options={"xatol": 2e-5}
    )
    if not result.success:
        raise RuntimeError(f"bounded minimization failed: {result.message}")
    return float(result.x), float(result.fun)


def fit_lcdm(like: MarginalizedSN) -> FitResult:
    omega, _ = bounded_minimize(
        lambda om: like.chi2(om, 0.0)[0], OMEGA_MIN, OMEGA_MAX
    )
    chi2, intercept = like.chi2(omega, 0.0)
    return FitResult(chi2, omega, 0.0, intercept)


def profile_omega(like: MarginalizedSN, a_r: float) -> tuple[float, float]:
    try:
        return bounded_minimize(
            lambda om: like.chi2(om, a_r)[0], OMEGA_MIN, OMEGA_MAX
        )
    except ValueError:
        return float("nan"), float("inf")


def fit_rcms(like: MarginalizedSN) -> FitResult:
    def profile(a_r: float) -> float:
        return profile_omega(like, a_r)[1]

    # Coarse deterministic scan guards against silently assuming a globally
    # unimodal A_R profile; bounded refinement is restricted around its best bin.
    scan = np.linspace(A_MIN, A_MAX, 101)
    values = np.asarray([profile(float(a)) for a in scan])
    i = int(np.argmin(values))
    left = float(scan[max(0, i - 1)])
    right = float(scan[min(len(scan) - 1, i + 1)])
    if left == right:
        a_best = left
    else:
        a_best, _ = bounded_minimize(profile, left, right)
    omega_best, _ = profile_omega(like, a_best)
    chi2, intercept = like.chi2(omega_best, a_best)
    return FitResult(chi2, omega_best, a_best, intercept)


def profile_interval(
    like: MarginalizedSN, best: FitResult, delta: float = 1.0
) -> tuple[float, float]:
    target = best.chi2 + delta

    def prof(a: float) -> float:
        return profile_omega(like, a)[1]

    def crossing(lo: float, hi: float) -> float:
        flo = prof(lo) - target
        fhi = prof(hi) - target
        if flo * fhi > 0:
            return lo if abs(flo) < abs(fhi) else hi
        for _ in range(35):
            mid = 0.5 * (lo + hi)
            fm = prof(mid) - target
            if flo * fm <= 0:
                hi, fhi = mid, fm
            else:
                lo, flo = mid, fm
        return 0.5 * (lo + hi)

    lower = A_MIN if prof(A_MIN) <= target else crossing(A_MIN, best.a_r)
    upper = A_MAX if prof(A_MAX) <= target else crossing(best.a_r, A_MAX)
    return lower, upper


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    args = parser.parse_args()

    dat_path = args.data_dir / "Pantheon+SH0ES.dat"
    cov_path = args.data_dir / "Pantheon+SH0ES_STAT+SYS.cov"
    if not dat_path.exists() or not cov_path.exists():
        raise SystemExit(
            "Pantheon+ frozen files not found. Run tools/fetch_rcms_pantheonplus.py first."
        )

    mag, zcmb, zhel = read_pantheon_table(dat_path)
    cov = read_covariance(cov_path)
    mask = zcmb > 0.01
    mag_m = mag[mask]
    zcmb_m = zcmb[mask]
    zhel_m = zhel[mask]
    cov_m = cov[np.ix_(mask, mask)]

    like = MarginalizedSN(mag_m, zcmb_m, zhel_m, cov_m)
    lcdm = fit_lcdm(like)
    rcms = fit_rcms(like)
    lo, hi = profile_interval(like, rcms)

    n = len(mag_m)
    # Only identifiable shape parameters are counted: the intercept is common
    # and analytically marginalized in both models.
    k_lcdm = 1
    k_rcms = 2
    aic_lcdm = lcdm.chi2 + 2 * k_lcdm
    aic_rcms = rcms.chi2 + 2 * k_rcms
    bic_lcdm = lcdm.chi2 + k_lcdm * math.log(n)
    bic_rcms = rcms.chi2 + k_rcms * math.log(n)

    boundary = (
        rcms.omega_m <= OMEGA_MIN + 1e-3
        or rcms.omega_m >= OMEGA_MAX - 1e-3
        or rcms.a_r <= A_MIN + 1e-2
        or rcms.a_r >= A_MAX - 1e-2
    )

    print("RCMS Protocol 01 — Pantheon+ SN-alone")
    print(f"masked_supernovae={n}")
    print(f"LCDM: chi2={lcdm.chi2:.6f} omega_m={lcdm.omega_m:.6f}")
    print(
        f"RCMS: chi2={rcms.chi2:.6f} omega_m={rcms.omega_m:.6f} "
        f"A_R={rcms.a_r:.6f}"
    )
    print(f"A_R_profile_delta_chi2_1=[{lo:.6f}, {hi:.6f}]")
    print(f"delta_chi2_LCDM_minus_RCMS={lcdm.chi2 - rcms.chi2:.6f}")
    print(f"delta_AIC_LCDM_minus_RCMS={aic_lcdm - aic_rcms:.6f}")
    print(f"delta_BIC_LCDM_minus_RCMS={bic_lcdm - bic_rcms:.6f}")
    print(f"boundary_contact={boundary}")


if __name__ == "__main__":
    main()
