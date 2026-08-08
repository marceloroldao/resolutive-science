#!/usr/bin/env python3
"""RCMS Protocol 01 preregistered H(z) + Pantheon+ joint comparison.

The two probes share only the late-time expansion-shape parameters Omega_m and
A_R. Cosmic chronometers identify/profile H0; Pantheon+ has its additive
absolute-magnitude/intercept analytically marginalized and therefore contributes
no absolute H0 information. No SH0ES or CMB prior is introduced.
"""
from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path
from typing import Callable

import numpy as np
from scipy.optimize import minimize_scalar

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
PANTHEON_DIR = ROOT / "data" / "external" / "pantheonplus_v1"
OM_MIN, OM_MAX = 0.05, 0.60
A_MIN, A_MAX = -5.0, 5.0


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


hz = load_module("rcms_real_hz", TOOLS / "run_rcms_real_hz.py")
sn = load_module("rcms_pantheonplus", TOOLS / "fit_rcms_pantheonplus.py")


def bounded_minimize(fn: Callable[[float], float], low: float, high: float) -> tuple[float, float]:
    result = minimize_scalar(fn, bounds=(low, high), method="bounded", options={"xatol": 2e-5})
    if not result.success:
        raise RuntimeError(f"bounded minimization failed: {result.message}")
    return float(result.x), float(result.fun)


def build_likelihoods():
    z_h, h_obs, _, cov_h = hz.build_covariance()
    inv_h, det, det_rel, inv_err = hz.covariance_checks(cov_h)

    dat_path = PANTHEON_DIR / "Pantheon+SH0ES.dat"
    cov_path = PANTHEON_DIR / "Pantheon+SH0ES_STAT+SYS.cov"
    if not dat_path.exists() or not cov_path.exists():
        raise SystemExit("Pantheon+ frozen bytes missing; run tools/fetch_rcms_pantheonplus.py first")
    mag, zcmb, zhel = sn.read_pantheon_table(dat_path)
    cov = sn.read_covariance(cov_path)
    mask = zcmb > 0.01
    sn_like = sn.MarginalizedSN(
        mag[mask], zcmb[mask], zhel[mask], cov[np.ix_(mask, mask)]
    )
    return (z_h, h_obs, inv_h), sn_like, (det, det_rel, inv_err, int(mask.sum()))


def joint_at(omega_m: float, a_r: float, hz_like, sn_like):
    z_h, h_obs, inv_h = hz_like
    hz_chi2, h0, hz_boundary = hz.objective_om(omega_m, a_r, z_h, h_obs, inv_h)
    if not math.isfinite(hz_chi2) or h0 is None:
        return float("inf"), None, True, float("inf"), float("inf")
    try:
        sn_chi2, _ = sn_like.chi2(omega_m, a_r)
    except ValueError:
        return float("inf"), None, True, float("inf"), float("inf")
    return hz_chi2 + sn_chi2, h0, hz_boundary, hz_chi2, sn_chi2


def profile_omega(a_r: float, hz_like, sn_like):
    def fn(om: float) -> float:
        return joint_at(om, a_r, hz_like, sn_like)[0]

    om, _ = bounded_minimize(fn, OM_MIN, OM_MAX)
    total, h0, h0_bound, hchi, schi = joint_at(om, a_r, hz_like, sn_like)
    boundary = h0_bound or om <= OM_MIN + 1e-3 or om >= OM_MAX - 1e-3
    return total, om, h0, boundary, hchi, schi


def fit_rcms(hz_like, sn_like):
    def prof(a: float) -> float:
        return profile_omega(a, hz_like, sn_like)[0]

    scan = np.linspace(A_MIN, A_MAX, 101)
    vals = np.asarray([prof(float(a)) for a in scan])
    idx = int(np.argmin(vals))
    left = float(scan[max(0, idx - 1)])
    right = float(scan[min(len(scan) - 1, idx + 1)])
    if left == right:
        a_best = left
    else:
        a_best, _ = bounded_minimize(prof, left, right)
    total, om, h0, boundary, hchi, schi = profile_omega(a_best, hz_like, sn_like)
    boundary = boundary or a_best <= A_MIN + 1e-2 or a_best >= A_MAX - 1e-2
    return total, om, h0, a_best, boundary, hchi, schi


def profile_interval(hz_like, sn_like, best_chi2: float, best_a: float, delta: float = 1.0):
    target = best_chi2 + delta

    def prof(a: float) -> float:
        return profile_omega(a, hz_like, sn_like)[0]

    def root(lo: float, hi: float):
        flo, fhi = prof(lo) - target, prof(hi) - target
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

    lower = A_MIN if prof(A_MIN) <= target else root(A_MIN, best_a)
    upper = A_MAX if prof(A_MAX) <= target else root(best_a, A_MAX)
    return lower, upper


def main() -> None:
    hz_like, sn_like, diagnostics = build_likelihoods()
    det, det_rel, inv_err, n_sn = diagnostics

    ref_total, ref_om, ref_h0, ref_bound, ref_hchi, ref_schi = profile_omega(0.0, hz_like, sn_like)
    rc_total, rc_om, rc_h0, a_r, rc_bound, rc_hchi, rc_schi = fit_rcms(hz_like, sn_like)
    lo, hi = profile_interval(hz_like, sn_like, rc_total, a_r)

    n_h = len(hz_like[0])
    n = n_h + n_sn
    # Identifiable parameters: H0 and Omega_m; RCMS adds A_R.
    k_ref, k_rc = 2, 3
    delta_chi2 = ref_total - rc_total
    delta_aic = (ref_total + 2 * k_ref) - (rc_total + 2 * k_rc)
    delta_bic = (ref_total + k_ref * math.log(n)) - (rc_total + k_rc * math.log(n))

    zero_in_profile = lo <= 0.0 <= hi
    if zero_in_profile:
        decision = "NO_PREFERENCE"
    elif delta_aic > 0.0 and delta_bic > 0.0:
        decision = "RCMS_SCREENING_CANDIDATE_HZ_SN"
    elif delta_aic < 0.0 and delta_bic < 0.0:
        decision = "REFERENCE_FAVORED_HZ_SN"
    else:
        decision = "NO_PREFERENCE"

    print("RCMS Protocol 01 — joint H(z) + Pantheon+ SN")
    print(f"N_Hz={n_h} N_SN={n_sn} N_total={n}")
    print(f"Hz_cov_det={det:.6e} rel_reference_error={det_rel:.3e} inverse_residual={inv_err:.3e}")
    print(
        f"LCDM: chi2={ref_total:.6f} H0={ref_h0:.6f} Omega_m={ref_om:.6f} "
        f"chi2_Hz={ref_hchi:.6f} chi2_SN={ref_schi:.6f} boundary={ref_bound}"
    )
    print(
        f"RCMS: chi2={rc_total:.6f} H0={rc_h0:.6f} Omega_m={rc_om:.6f} A_R={a_r:.6f} "
        f"chi2_Hz={rc_hchi:.6f} chi2_SN={rc_schi:.6f} boundary={rc_bound}"
    )
    print(f"A_R_profile_delta_chi2_1=[{lo:.6f}, {hi:.6f}]")
    print(f"delta_chi2_LCDM_minus_RCMS={delta_chi2:.6f}")
    print(f"delta_AIC_LCDM_minus_RCMS={delta_aic:.6f}")
    print(f"delta_BIC_LCDM_minus_RCMS={delta_bic:.6f}")
    print(f"JOINT_HZ_SN_DECISION={decision}")


if __name__ == "__main__":
    main()
