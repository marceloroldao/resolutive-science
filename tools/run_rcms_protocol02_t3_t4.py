#!/usr/bin/env python3
"""Execute preregistered RCMS Protocol 02 T3 and T4.

T3: fixed Pantheon+ split at z_CMB=0.3, with covariance consistently subset.
T4: diagonal-covariance diagnostics for Pantheon+, DESI BAO, and both.

The frozen RCMS deformation, parameter bounds, datasets, and likelihood
semantics are inherited unchanged from Protocol 01 production runners.
"""
from __future__ import annotations

import importlib.util
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
PANTHEON_DIR = ROOT / "data" / "external" / "pantheonplus_v1"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


combo = load_module("rcms_combo_t34", TOOLS / "run_rcms_protocol01_remaining_combos.py")
sn = load_module("rcms_sn_t34", TOOLS / "fit_rcms_pantheonplus.py")
bao = load_module("rcms_bao_t34", TOOLS / "run_rcms_desi_dr2_bao.py")
hz = load_module("rcms_hz_t34", TOOLS / "run_rcms_real_hz.py")


@dataclass(frozen=True)
class Case:
    name: str
    use_hz: bool
    use_bao: bool
    nobs: int
    common_parameter_count: int


def make_sn_likes():
    dat_path = PANTHEON_DIR / "Pantheon+SH0ES.dat"
    cov_path = PANTHEON_DIR / "Pantheon+SH0ES_STAT+SYS.cov"
    if not dat_path.exists() or not cov_path.exists():
        raise SystemExit("Pantheon+ frozen bytes missing; run tools/fetch_rcms_pantheonplus.py first")

    mag, zcmb, zhel = sn.read_pantheon_table(dat_path)
    cov = sn.read_covariance(cov_path)
    base = zcmb > 0.01
    low = base & (zcmb < 0.3)
    high = base & (zcmb >= 0.3)

    def mk(mask: np.ndarray, diagonal: bool = False):
        c = cov[np.ix_(mask, mask)]
        if diagonal:
            c = np.diag(np.diag(c))
        return sn.MarginalizedSN(mag[mask], zcmb[mask], zhel[mask], c)

    return {
        "full": mk(base),
        "low": mk(low),
        "high": mk(high),
        "full_diag": mk(base, diagonal=True),
        "n_full": int(base.sum()),
        "n_low": int(low.sum()),
        "n_high": int(high.sum()),
    }


def make_h_like():
    z_h, h_obs, _, h_cov = hz.build_covariance()
    h_inv, _, _, _ = hz.covariance_checks(h_cov)
    return (z_h, h_obs, h_inv)


def make_b_likes():
    rows, cov = bao.load_data()
    inv_full = bao.invert(cov)
    diag = [[0.0 for _ in range(len(cov))] for __ in range(len(cov))]
    for i in range(len(cov)):
        diag[i][i] = cov[i][i]
    inv_diag = bao.invert(diag)
    return (rows, inv_full), (rows, inv_diag)


def fit_case(case: Case, sn_like, h_like, b_like):
    c = combo.Combo(case.name, case.use_hz, True, case.use_bao, case.nobs, case.common_parameter_count)
    ref_chi, ref_om, ref_parts, ref_nuis, ref_bound = combo.profile_omega(
        0.0, c, h_like, sn_like, b_like
    )
    rc_chi, rc_om, a_r, rc_parts, rc_nuis, rc_bound = combo.fit_rcms(
        c, h_like, sn_like, b_like
    )
    lo, hi = combo.profile_interval(c, h_like, sn_like, b_like, rc_chi, a_r)
    delta_chi = ref_chi - rc_chi
    k0 = case.common_parameter_count
    k1 = k0 + 1
    delta_aic = (ref_chi + 2 * k0) - (rc_chi + 2 * k1)
    delta_bic = (ref_chi + k0 * math.log(case.nobs)) - (rc_chi + k1 * math.log(case.nobs))
    return {
        "name": case.name,
        "ref_chi": ref_chi,
        "ref_om": ref_om,
        "ref_parts": ref_parts,
        "ref_nuis": ref_nuis,
        "rc_chi": rc_chi,
        "rc_om": rc_om,
        "a_r": a_r,
        "lo": lo,
        "hi": hi,
        "delta_chi": delta_chi,
        "delta_aic": delta_aic,
        "delta_bic": delta_bic,
        "boundary": bool(ref_bound or rc_bound),
    }


def show(result):
    print(
        f"{result['name']} A_R={result['a_r']:.6f} "
        f"interval=[{result['lo']:.6f},{result['hi']:.6f}] "
        f"Omega_m={result['rc_om']:.6f} delta_chi2={result['delta_chi']:.6f} "
        f"delta_AIC={result['delta_aic']:.6f} delta_BIC={result['delta_bic']:.6f} "
        f"boundary={result['boundary']}"
    )


def main():
    sns = make_sn_likes()
    h_like = make_h_like()
    b_full, b_diag = make_b_likes()
    print("RCMS Protocol 02 — T3 SN split + T4 covariance ablation")
    print(f"Pantheon counts full={sns['n_full']} low_z={sns['n_low']} high_z={sns['n_high']} split=0.3")
    print()

    print("[T3_SUPERNOVA_REDSHIFT_SPLIT]")
    t3_cases = (
        Case("LOW_SN_BAO", False, True, sns["n_low"] + 13, 2),
        Case("HIGH_SN_BAO", False, True, sns["n_high"] + 13, 2),
        Case("HZ_LOW_SN_BAO", True, True, 15 + sns["n_low"] + 13, 3),
        Case("HZ_HIGH_SN_BAO", True, True, 15 + sns["n_high"] + 13, 3),
    )
    t3_results = []
    for case in t3_cases:
        like = sns["low"] if "LOW" in case.name else sns["high"]
        r = fit_case(case, like, h_like, b_full)
        t3_results.append(r)
        show(r)
    signs = [math.copysign(1.0, r["a_r"]) if r["a_r"] != 0 else 0.0 for r in t3_results]
    print(f"T3_SIGN_REVERSAL={len(set(signs)) > 1}")
    print()

    print("[T4_COVARIANCE_ABLATION]")
    full_case = Case("FULL_BASELINE", True, True, 15 + sns["n_full"] + 13, 3)
    base = fit_case(full_case, sns["full"], h_like, b_full)
    show(base)
    variants = (
        ("SN_DIAGONAL_ONLY", sns["full_diag"], b_full),
        ("BAO_DIAGONAL_ONLY", sns["full"], b_diag),
        ("SN_BAO_DIAGONAL_ONLY", sns["full_diag"], b_diag),
    )
    for name, slike, blike in variants:
        case = Case(name, True, True, 15 + sns["n_full"] + 13, 3)
        r = fit_case(case, slike, h_like, blike)
        show(r)
        print(f"movement_A_R_vs_full={r['a_r'] - base['a_r']:.6f}")


if __name__ == "__main__":
    main()
