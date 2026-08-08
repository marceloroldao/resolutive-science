#!/usr/bin/env python3
"""Evaluate the remaining preregistered RCMS Protocol 01 probe combinations.

This file freezes, in one implementation before execution, the three remaining
real-data combinations after H(z)+Pantheon+:

1. H(z) + DESI DR2 BAO;
2. Pantheon+ + DESI DR2 BAO;
3. H(z) + Pantheon+ + DESI DR2 BAO.

All probes share Omega_m and, in RCMS, the single frozen effective deformation
A_R. Probe-specific scale nuisances are handled exactly as in their already
formalized single-probe likelihoods:
- H(z): H0 is profiled with the Moresco covariance;
- Pantheon+: the additive SN intercept is analytically marginalized;
- BAO: q=c/(H0*r_d) is profiled, equivalent to a free r_d in BAO without CMB.

No SH0ES, CMB, RSD, sound-horizon prior, or post-hoc RCMS term is introduced.
"""
from __future__ import annotations

import importlib.util
import math
import sys
from dataclasses import dataclass
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
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


hz = load_module("rcms_real_hz_combo", TOOLS / "run_rcms_real_hz.py")
sn = load_module("rcms_pantheon_combo", TOOLS / "fit_rcms_pantheonplus.py")
bao = load_module("rcms_desi_combo", TOOLS / "run_rcms_desi_dr2_bao.py")


@dataclass(frozen=True)
class Combo:
    name: str
    use_hz: bool
    use_sn: bool
    use_bao: bool
    nobs: int
    common_parameter_count: int


COMBOS = (
    Combo("HZ_BAO", True, False, True, 15 + 13, 3),
    Combo("SN_BAO", False, True, True, 1590 + 13, 2),
    Combo("HZ_SN_BAO", True, True, True, 15 + 1590 + 13, 3),
)


def bounded_minimize(fn: Callable[[float], float], low: float, high: float) -> tuple[float, float]:
    result = minimize_scalar(fn, bounds=(low, high), method="bounded", options={"xatol": 2e-5})
    if not result.success:
        raise RuntimeError(f"bounded minimization failed: {result.message}")
    return float(result.x), float(result.fun)


def load_likelihoods():
    z_h, h_obs, _, h_cov = hz.build_covariance()
    h_inv, h_det, h_det_rel, h_inv_err = hz.covariance_checks(h_cov)

    dat_path = PANTHEON_DIR / "Pantheon+SH0ES.dat"
    cov_path = PANTHEON_DIR / "Pantheon+SH0ES_STAT+SYS.cov"
    if not dat_path.exists() or not cov_path.exists():
        raise SystemExit("Pantheon+ frozen bytes missing; run tools/fetch_rcms_pantheonplus.py first")
    mag, zcmb, zhel = sn.read_pantheon_table(dat_path)
    sn_cov = sn.read_covariance(cov_path)
    mask = zcmb > 0.01
    sn_like = sn.MarginalizedSN(
        mag[mask], zcmb[mask], zhel[mask], sn_cov[np.ix_(mask, mask)]
    )
    if int(mask.sum()) != 1590:
        raise RuntimeError(f"expected 1590 masked Pantheon+ rows, got {int(mask.sum())}")

    bao_rows, bao_cov = bao.load_data()
    bao_inv = bao.invert(bao_cov)
    if len(bao_rows) != 13:
        raise RuntimeError(f"expected 13 DESI DR2 BAO observables, got {len(bao_rows)}")

    return (
        (z_h, h_obs, h_inv),
        sn_like,
        (bao_rows, bao_inv),
        (h_det, h_det_rel, h_inv_err),
    )


def evaluate(omega_m: float, a_r: float, combo: Combo, h_like, sn_like, b_like):
    total = 0.0
    parts: dict[str, float] = {}
    nuis: dict[str, float] = {}
    boundary = False

    if combo.use_hz:
        z_h, h_obs, h_inv = h_like
        hchi, h0, hbound = hz.objective_om(omega_m, a_r, z_h, h_obs, h_inv)
        if not math.isfinite(hchi) or h0 is None:
            return float("inf"), {}, {}, True
        total += hchi
        parts["Hz"] = hchi
        nuis["H0"] = h0
        boundary = boundary or hbound

    if combo.use_sn:
        try:
            schi, _ = sn_like.chi2(omega_m, a_r)
        except ValueError:
            return float("inf"), {}, {}, True
        total += schi
        parts["SN"] = schi

    if combo.use_bao:
        rows, inv = b_like
        bchi, q = bao.objective(rows, inv, omega_m, a_r)
        if not math.isfinite(bchi) or not math.isfinite(q):
            return float("inf"), {}, {}, True
        total += bchi
        parts["BAO"] = bchi
        nuis["q"] = q

    return total, parts, nuis, boundary


def profile_omega(a_r: float, combo: Combo, h_like, sn_like, b_like):
    def fn(om: float) -> float:
        return evaluate(om, a_r, combo, h_like, sn_like, b_like)[0]

    om, _ = bounded_minimize(fn, OM_MIN, OM_MAX)
    total, parts, nuis, boundary = evaluate(om, a_r, combo, h_like, sn_like, b_like)
    boundary = boundary or om <= OM_MIN + 1e-3 or om >= OM_MAX - 1e-3
    return total, om, parts, nuis, boundary


def fit_rcms(combo: Combo, h_like, sn_like, b_like):
    def prof(a: float) -> float:
        return profile_omega(a, combo, h_like, sn_like, b_like)[0]

    # Fixed coarse scan before local refinement avoids assuming global unimodality.
    scan = np.linspace(A_MIN, A_MAX, 101)
    values = np.asarray([prof(float(a)) for a in scan])
    idx = int(np.argmin(values))
    left = float(scan[max(0, idx - 1)])
    right = float(scan[min(len(scan) - 1, idx + 1)])
    if left == right:
        a_best = left
    else:
        a_best, _ = bounded_minimize(prof, left, right)
    total, om, parts, nuis, boundary = profile_omega(a_best, combo, h_like, sn_like, b_like)
    boundary = boundary or a_best <= A_MIN + 1e-2 or a_best >= A_MAX - 1e-2
    return total, om, a_best, parts, nuis, boundary


def profile_interval(combo: Combo, h_like, sn_like, b_like, best_chi2: float, best_a: float):
    target = best_chi2 + 1.0

    def prof(a: float) -> float:
        return profile_omega(a, combo, h_like, sn_like, b_like)[0]

    def root(lo: float, hi: float) -> float:
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


def run_combo(combo: Combo, h_like, sn_like, b_like):
    ref_chi, ref_om, ref_parts, ref_nuis, ref_bound = profile_omega(
        0.0, combo, h_like, sn_like, b_like
    )
    rc_chi, rc_om, a_r, rc_parts, rc_nuis, rc_bound = fit_rcms(
        combo, h_like, sn_like, b_like
    )
    lo, hi = profile_interval(combo, h_like, sn_like, b_like, rc_chi, a_r)

    k_ref = combo.common_parameter_count
    k_rc = k_ref + 1
    delta_chi = ref_chi - rc_chi
    delta_aic = (ref_chi + 2 * k_ref) - (rc_chi + 2 * k_rc)
    delta_bic = (ref_chi + k_ref * math.log(combo.nobs)) - (
        rc_chi + k_rc * math.log(combo.nobs)
    )

    if lo <= 0.0 <= hi:
        decision = "NO_PREFERENCE"
    elif delta_aic > 0.0 and delta_bic > 0.0:
        decision = f"RCMS_SCREENING_CANDIDATE_{combo.name}"
    elif delta_aic < 0.0 and delta_bic < 0.0:
        decision = f"REFERENCE_FAVORED_{combo.name}"
    else:
        decision = "NO_PREFERENCE"

    print(f"[{combo.name}]")
    print(
        f"LCDM chi2={ref_chi:.6f} Omega_m={ref_om:.6f} "
        + " ".join(f"chi2_{k}={v:.6f}" for k, v in ref_parts.items())
        + " "
        + " ".join(f"{k}={v:.6f}" for k, v in ref_nuis.items())
        + f" boundary={ref_bound}"
    )
    print(
        f"RCMS chi2={rc_chi:.6f} Omega_m={rc_om:.6f} A_R={a_r:.6f} "
        + " ".join(f"chi2_{k}={v:.6f}" for k, v in rc_parts.items())
        + " "
        + " ".join(f"{k}={v:.6f}" for k, v in rc_nuis.items())
        + f" boundary={rc_bound}"
    )
    print(f"A_R_profile_delta_chi2_1=[{lo:.6f}, {hi:.6f}]")
    print(f"delta_chi2_LCDM_minus_RCMS={delta_chi:.6f}")
    print(f"delta_AIC_LCDM_minus_RCMS={delta_aic:.6f}")
    print(f"delta_BIC_LCDM_minus_RCMS={delta_bic:.6f}")
    print(f"DECISION={decision}")
    print()


def main() -> None:
    h_like, sn_like, b_like, hdiag = load_likelihoods()
    det, det_rel, inv_err = hdiag
    print("RCMS Protocol 01 — remaining combinations frozen before joint execution")
    print(f"Hz_cov_det={det:.6e} rel_reference_error={det_rel:.3e} inverse_residual={inv_err:.3e}")
    print("Pantheon+ masked N=1590; DESI DR2 BAO N=13; H(z) N=15")
    print()
    for combo in COMBOS:
        run_combo(combo, h_like, sn_like, b_like)


if __name__ == "__main__":
    main()
