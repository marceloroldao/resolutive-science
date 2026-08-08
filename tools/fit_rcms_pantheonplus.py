#!/usr/bin/env python3
"""Run the preregistered Pantheon+ SN-alone comparison for RCMS Protocol 01.

The runner intentionally does not bundle Pantheon+ data. Run
``tools/fetch_rcms_pantheonplus.py`` first. The acquisition tool pins and
verifies the exact upstream Git blobs.

Likelihood semantics reproduce Cobaya's frozen PantheonPlus (without SH0ES):
- zCMB > 0.01 fixed mask;
- full masked covariance;
- no Cepheid-host distance override;
- one additive SN intercept analytically marginalized for both models.

The marginalized quadratic form is evaluated through a Cholesky solve rather
than explicitly forming the projected inverse covariance. This is algebraically
equivalent to Cobaya's projection and is numerically better conditioned.
"""
from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

try:
    import numpy as np
    from scipy.linalg import cho_factor, cho_solve
    from scipy.optimize import minimize_scalar
except ImportError as exc:  # pragma: no cover - dependency guard
    raise SystemExit(
        "Pantheon+ production fitting requires numpy and scipy. "
        "Install them in the observational-analysis environment."
    ) from exc

C_KM_S = 299792.458
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = ROOT / "data" / "external" / "pantheonplus_v1"

OMEGA_MIN = 0.05
OMEGA_MAX = 0.60
A_MIN = -5.0
A_MAX = 5.0
FIXED_H0 = 70.0  # exactly absorbed by the marginalized SN intercept


@dataclass(frozen=True)
class FitResult:
    chi2: float
    omega_m: float
    a_r: float
    intercept: float


def read_pantheon_table(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter=None, skipinitialspace=True)
        # csv cannot auto-split arbitrary whitespace with delimiter=None.
    # Re-read explicitly because Pantheon+ is a whitespace table.
    lines = path.read_text().splitlines()
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
    return raw[1:].reshape((n, n))


def e2(z: float, omega_m: float, a_r: float) -> float:
    value = omega_m * (1.0 + z) ** 3 + (1.0 - omega_m) + a_r * math.log1p(z)
    if value <= 0.0:
        raise ValueError("non-positive E(z)^2")
    return value


def adaptive_simpson_integral(z: float, omega_m: float, a_r: float, n: int = 160) -> float:
    if z == 0.0:
        return 0.0
    # Fixed even Simpson grid is deterministic and more than sufficient for
    # Pantheon+ precision; n=160 is retained as a conservative production value.
    n = n if n % 2 == 0 else n + 1
    h = z / n
    total = 0.0
    for j in range(n + 1):
        x = j * h
        weight = 1.0 if j in (0, n) else (4.0 if j % 2 else 2.0)
        total += weight / math.sqrt(e2(x, omega_m, a_r))
    return total * h / 3.0


def pantheon_lumdists(zcmb: np.ndarray, zhel: np.ndarray, omega_m: float, a_r: float) -> np.ndarray:
    # Cobaya uses 5 log10[(1+zhel)(1+zcmb) D_A(zcmb)].
    # In a flat background D_A = D_M/(1+zcmb), so this is
    # 5 log10[(1+zhel) D_M], with D_M in Mpc.
    scale = C_KM_S / FIXED_H0
    out = np.empty_like(zcmb)
    cache: dict[float, float] = {}
    for i, (zc, zh) in enumerate(zip(zcmb, zhel)):
        key = float(zc)
        integral = cache.get(key)
        if integral is None:
            integral = adaptive_simpson_integral(key, omega_m, a_r)
            cache[key] = integral
        dm = scale * integral
        out[i] = 5.0 * math.log10((1.0 + float(zh)) * dm)
    return out


class MarginalizedSN:
    def __init__(self, mag: np.ndarray, zcmb: np.ndarray, zhel: np.ndarray, cov: np.ndarray):
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
        # Best additive intercept for residual = data - theory - M.
        intercept = float(self.ones @ cinv_r / self.ones_cinv_ones)
        centered = residual - intercept
        cinv_centered = cho_solve(self.factor, centered, check_finite=False)
        chi2 = float(centered @ cinv_centered)
        return chi2, intercept


def bounded_minimize(fn: Callable[[float], float], low: float, high: float) -> tuple[float, float]:
    result = minimize_scalar(fn, bounds=(low, high), method="bounded", options={"xatol": 2e-5})
    if not result.success:
        raise RuntimeError(f"bounded minimization failed: {result.message}")
    return float(result.x), float(result.fun)


def fit_lcdm(like: MarginalizedSN) -> FitResult:
    omega, chi2 = bounded_minimize(lambda om: like.chi2(om, 0.0)[0], OMEGA_MIN, OMEGA_MAX)
    final_chi2, intercept = like.chi2(omega, 0.0)
    return FitResult(final_chi2, omega, 0.0, intercept)


def fit_rcms(like: MarginalizedSN) -> FitResult:
    # Profile omega_m analytically/numerically for each A_R, then minimize A_R.
    def profile(a_r: float) -> float:
        try:
            _, chi2 = bounded_minimize(
                lambda om: like.chi2(om, a_r)[0], OMEGA_MIN, OMEGA_MAX
            )
            return chi2
        except ValueError:
            return float("inf")

    a_best, _ = bounded_minimize(profile, A_MIN, A_MAX)
    omega_best, _ = bounded_minimize(
        lambda om: like.chi2(om, a_best)[0], OMEGA_MIN, OMEGA_MAX
    )
    chi2, intercept = like.chi2(omega_best, a_best)
    return FitResult(chi2, omega_best, a_best, intercept)


def profile_interval(like: MarginalizedSN, best: FitResult, delta: float = 1.0) -> tuple[float, float]:
    target = best.chi2 + delta

    def prof(a: float) -> float:
        try:
            _, val = bounded_minimize(lambda om: like.chi2(om, a)[0], OMEGA_MIN, OMEGA_MAX)
            return val
        except ValueError:
            return float("inf")

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
    # Identifiable shape parameters only; intercept is common and marginalized.
    k_lcdm = 1
    k_rcms = 2
    aic_lcdm = lcdm.chi2 + 2 * k_lcdm
    aic_rcms = rcms.chi2 + 2 * k_rcms
    bic_lcdm = lcdm.chi2 + k_lcdm * math.log(n)
    bic_rcms = rcms.chi2 + k_rcms * math.log(n)

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
    print(
        "boundary_contact="
        f"{rcms.omega_m <= OMEGA_MIN + 1e-3 or rcms.omega_m >= OMEGA_MAX - 1e-3 or rcms.a_r <= A_MIN + 1e-2 or rcms.a_r >= A_MAX - 1e-2}"
    )


if __name__ == "__main__":
    main()
