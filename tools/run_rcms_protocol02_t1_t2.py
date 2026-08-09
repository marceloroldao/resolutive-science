#!/usr/bin/env python3
"""Execute preregistered RCMS Protocol 02 tests T1 and T2.

T1: reproduce the Protocol 01 full H(z)+SN+BAO fit with two deterministic
optimization paths: the existing production profile optimizer and an
independent rectangular-grid + coordinate-refinement optimizer.

T2: DESI DR2 jackknife by complete measurement block. Blocks are fixed solely
by the frozen BAO redshift labels before results are inspected. Each omission
removes every observable at that redshift and the matching covariance rows and
columns, then refits the full H(z)+Pantheon+ + remaining-BAO combination.

The frozen Protocol 01 deformation A_R*ln(1+z), parameter bounds, covariances,
and nuisance handling are unchanged.
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
OM_MIN, OM_MAX = 0.05, 0.60
A_MIN, A_MAX = -5.0, 5.0
P01_AR = 0.187021
P01_DCHI2 = 4.559528


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


combo_mod = load_module("rcms_p02_combo", TOOLS / "run_rcms_protocol01_remaining_combos.py")
bao_mod = combo_mod.bao


@dataclass(frozen=True)
class FitResult:
    chi2: float
    omega_m: float
    a_r: float
    parts: dict[str, float]
    nuis: dict[str, float]
    boundary: bool


def full_combo(n_bao: int) -> object:
    return combo_mod.Combo("HZ_SN_BAO", True, True, True, 15 + 1590 + n_bao, 3)


def production_fit(combo, h_like, sn_like, b_like) -> tuple[FitResult, FitResult]:
    ref_chi, ref_om, ref_parts, ref_nuis, ref_bound = combo_mod.profile_omega(
        0.0, combo, h_like, sn_like, b_like
    )
    rc_chi, rc_om, a_r, rc_parts, rc_nuis, rc_bound = combo_mod.fit_rcms(
        combo, h_like, sn_like, b_like
    )
    return (
        FitResult(ref_chi, ref_om, 0.0, ref_parts, ref_nuis, ref_bound),
        FitResult(rc_chi, rc_om, a_r, rc_parts, rc_nuis, rc_bound),
    )


def independent_refine(combo, h_like, sn_like, b_like) -> FitResult:
    """Independent deterministic coarse grid followed by shrinking 2-D grid.

    This intentionally does not call scipy.optimize or the production
    profile_omega/fit_rcms routines. Nuisance profiling remains the frozen
    likelihood definition through combo_mod.evaluate.
    """
    best = (float("inf"), None, None, None, None, True)

    # Full preregistered domain, deliberately coarse first pass.
    om_grid = np.linspace(OM_MIN, OM_MAX, 23)   # spacing 0.025
    a_grid = np.linspace(A_MIN, A_MAX, 101)    # spacing 0.1
    for om in om_grid:
        for ar in a_grid:
            chi, parts, nuis, bound = combo_mod.evaluate(
                float(om), float(ar), combo, h_like, sn_like, b_like
            )
            if chi < best[0]:
                best = (chi, float(om), float(ar), parts, nuis, bound)

    _, om0, ar0, _, _, _ = best
    assert om0 is not None and ar0 is not None

    # Coordinate-independent rectangular refinements around the current best.
    om_half, ar_half = 0.03, 0.12
    for _ in range(5):
        om_lo, om_hi = max(OM_MIN, om0 - om_half), min(OM_MAX, om0 + om_half)
        ar_lo, ar_hi = max(A_MIN, ar0 - ar_half), min(A_MAX, ar0 + ar_half)
        local_best = best
        for om in np.linspace(om_lo, om_hi, 25):
            for ar in np.linspace(ar_lo, ar_hi, 25):
                chi, parts, nuis, bound = combo_mod.evaluate(
                    float(om), float(ar), combo, h_like, sn_like, b_like
                )
                if chi < local_best[0]:
                    local_best = (chi, float(om), float(ar), parts, nuis, bound)
        best = local_best
        _, om0, ar0, _, _, _ = best
        om_half *= 0.25
        ar_half *= 0.25

    chi, om, ar, parts, nuis, bound = best
    assert om is not None and ar is not None and parts is not None and nuis is not None
    boundary = bool(bound or om <= OM_MIN + 1e-3 or om >= OM_MAX - 1e-3 or ar <= A_MIN + 1e-2 or ar >= A_MAX - 1e-2)
    return FitResult(float(chi), float(om), float(ar), parts, nuis, boundary)


def sub_bao(rows, cov, omit_z: float):
    keep = [i for i, row in enumerate(rows) if not math.isclose(float(row[0]), omit_z, rel_tol=0.0, abs_tol=1e-12)]
    removed = [i for i in range(len(rows)) if i not in keep]
    if not removed:
        raise RuntimeError(f"jackknife block z={omit_z} removed no observations")
    sub_rows = [rows[i] for i in keep]
    sub_cov = [[cov[i][j] for j in keep] for i in keep]
    return sub_rows, sub_cov, removed


def metrics(combo, ref: FitResult, rc: FitResult):
    k_ref = combo.common_parameter_count
    k_rc = k_ref + 1
    dchi = ref.chi2 - rc.chi2
    daic = (ref.chi2 + 2 * k_ref) - (rc.chi2 + 2 * k_rc)
    dbic = (ref.chi2 + k_ref * math.log(combo.nobs)) - (rc.chi2 + k_rc * math.log(combo.nobs))
    return dchi, daic, dbic


def print_fit(prefix: str, fit: FitResult) -> None:
    print(
        f"{prefix} chi2={fit.chi2:.6f} Omega_m={fit.omega_m:.6f} A_R={fit.a_r:.6f} "
        + " ".join(f"chi2_{k}={v:.6f}" for k, v in fit.parts.items())
        + " "
        + " ".join(f"{k}={v:.6f}" for k, v in fit.nuis.items())
        + f" boundary={fit.boundary}"
    )


def t1(h_like, sn_like, b_like):
    combo = full_combo(13)
    ref_prod, rc_prod = production_fit(combo, h_like, sn_like, b_like)
    rc_ind = independent_refine(combo, h_like, sn_like, b_like)
    dchi_prod = ref_prod.chi2 - rc_prod.chi2
    dchi_ind = ref_prod.chi2 - rc_ind.chi2

    print("[T1_NUMERICAL_REPRODUCIBILITY]")
    print_fit("PRODUCTION_LCDM", ref_prod)
    print_fit("PRODUCTION_RCMS", rc_prod)
    print_fit("INDEPENDENT_RCMS", rc_ind)
    print(f"difference_A_R={abs(rc_prod.a_r-rc_ind.a_r):.8f}")
    print(f"difference_Omega_m={abs(rc_prod.omega_m-rc_ind.omega_m):.8f}")
    print(f"difference_delta_chi2={abs(dchi_prod-dchi_ind):.8f}")
    print(f"anchor_difference_A_R={abs(rc_prod.a_r-P01_AR):.8f}")
    print(f"anchor_difference_delta_chi2={abs(dchi_prod-P01_DCHI2):.8f}")

    # Declared numerical tolerances, fixed in implementation before execution.
    passed = (
        abs(rc_prod.a_r - rc_ind.a_r) <= 2e-3
        and abs(rc_prod.omega_m - rc_ind.omega_m) <= 2e-3
        and abs(dchi_prod - dchi_ind) <= 2e-3
    )
    print(f"T1_PASS={passed}")
    print()
    return ref_prod, rc_prod, passed


def t2(h_like, sn_like, rows, cov):
    block_redshifts = sorted({float(row[0]) for row in rows})
    if block_redshifts != [0.295, 0.51, 0.706, 0.934, 1.321, 1.484, 2.33]:
        raise RuntimeError(f"unexpected frozen DESI block partition: {block_redshifts}")

    warnings = 0
    print("[T2_DESI_BLOCK_JACKKNIFE]")
    print("block_partition=" + ",".join(f"{z:.3f}" for z in block_redshifts))
    for z in block_redshifts:
        sub_rows, sub_cov, removed = sub_bao(rows, cov, z)
        sub_inv = bao_mod.invert(sub_cov)
        b_like = (sub_rows, sub_inv)
        combo = full_combo(len(sub_rows))
        ref, rc = production_fit(combo, h_like, sn_like, b_like)
        lo, hi = combo_mod.profile_interval(combo, h_like, sn_like, b_like, rc.chi2, rc.a_r)
        dchi, daic, dbic = metrics(combo, ref, rc)
        warn = (
            rc.a_r <= 0.0
            or rc.boundary
            or dchi < 1.0
        )
        warnings += int(warn)
        print(
            f"omit_z={z:.3f} removed={len(removed)} kept={len(sub_rows)} "
            f"A_R={rc.a_r:.6f} interval=[{lo:.6f},{hi:.6f}] "
            f"Omega_m={rc.omega_m:.6f} delta_chi2={dchi:.6f} "
            f"delta_AIC={daic:.6f} delta_BIC={dbic:.6f} "
            f"boundary={rc.boundary} warning={warn}"
        )
    print(f"T2_warning_count={warnings}")
    print(f"T2_MULTIPLE_COLLAPSE_WARNING={warnings >= 2}")
    print()


def main() -> None:
    h_like, sn_like, b_like, hdiag = combo_mod.load_likelihoods()
    rows, cov = bao_mod.load_data()
    det, det_rel, inv_err = hdiag
    print("RCMS Protocol 02 — T1 numerical reproduction + T2 DESI jackknife")
    print(f"Hz_cov_det={det:.6e} rel_reference_error={det_rel:.3e} inverse_residual={inv_err:.3e}")
    print("Frozen model: A_R*ln(1+z); no new RCMS parameter")
    print()
    _, _, t1_pass = t1(h_like, sn_like, b_like)
    if not t1_pass:
        raise SystemExit("T1 numerical reproducibility failed; T2 results are not accepted")
    t2(h_like, sn_like, rows, cov)


if __name__ == "__main__":
    main()
