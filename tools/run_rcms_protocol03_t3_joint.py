#!/usr/bin/env python3
"""RCMS Protocol 03 T3: external DES-SN + DES Y6 no-DESI BAO joint fit.

The DES Y6 compressed external BAO likelihood contains one transverse datum.
With the preregistered free global scale nuisance it is exactly saturated for
any admissible late-time shape. Consequently the external joint fit must
reproduce P03-T1 DES-SN. This script treats that fact as a numerical closure
test rather than introducing a post-hoc sound-horizon calibration.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

from run_rcms_protocol03_t1_des_sn import (
    fit_rcms,
    fit_reference,
    load_precision,
    profile_interval,
    read_hd,
)

ROOT = Path(__file__).resolve().parents[1]
BAO_DATA = ROOT / "data" / "rcms" / "des_y6_bao_nodesi_alpha_v1.csv"

# Frozen hosted P03-T1 anchors. They are used only as closure targets.
T1_LCDM_CHI2 = 1640.273214
T1_LCDM_OM = 0.330317
T1_RCMS_CHI2 = 1638.906815
T1_RCMS_OM = 0.266117
T1_RCMS_AR = 0.382099
T1_DELTA_CHI2 = 1.366399

# Fixed numerical tolerances declared before this P03-T3 run.
CHI2_TOL = 5.0e-5
PARAM_TOL = 5.0e-5
BAO_CHI2_TOL = 1.0e-20


def load_bao():
    with BAO_DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise RuntimeError("expected one frozen DES Y6 no-DESI BAO datum")
    r = rows[0]
    return float(r["z_eff"]), float(r["alpha"]), float(r["sigma_alpha"])


def shape_integral(om: float, ar: float, z: float, n: int = 800) -> float:
    if n % 2:
        n += 1
    h = z / n

    def inv_e(x: float) -> float:
        e2 = om * (1.0 + x) ** 3 + (1.0 - om) + ar * math.log1p(x)
        if e2 <= 0.0 or not math.isfinite(e2):
            raise ValueError("non-positive E^2")
        return 1.0 / math.sqrt(e2)

    s = inv_e(0.0) + inv_e(z)
    for i in range(1, n):
        s += (4.0 if i % 2 else 2.0) * inv_e(i * h)
    return s * h / 3.0


def profile_bao_scale(om: float, ar: float, z: float, alpha: float, sigma: float):
    shape = shape_integral(om, ar, z)
    beta = alpha / shape
    pred = beta * shape
    chi2 = ((alpha - pred) / sigma) ** 2
    return chi2, beta, shape


def assert_close(name: str, got: float, expected: float, tol: float) -> None:
    err = abs(got - expected)
    print(f"closure {name}: got={got:.9f} expected={expected:.9f} abs_error={err:.3e} tol={tol:.1e}")
    if err > tol:
        raise RuntimeError(f"P03-T3 closure failed for {name}: {err} > {tol}")


def main() -> None:
    zcmb, zhel, mu_obs = read_hd()
    precision, eig_min = load_precision(len(mu_obs))
    z_bao, alpha_bao, sigma_bao = load_bao()

    sn_chi0, om0 = fit_reference(zcmb, zhel, mu_obs, precision)
    sn_chi1, om1, ar1 = fit_rcms(zcmb, zhel, mu_obs, precision)
    ar_lo, ar_hi = profile_interval(ar1, sn_chi1, zcmb, zhel, mu_obs, precision)

    bao_chi0, beta0, shape0 = profile_bao_scale(om0, 0.0, z_bao, alpha_bao, sigma_bao)
    bao_chi1, beta1, shape1 = profile_bao_scale(om1, ar1, z_bao, alpha_bao, sigma_bao)
    if max(bao_chi0, bao_chi1) > BAO_CHI2_TOL:
        raise RuntimeError("free-scale BAO contribution is not numerically saturated")

    joint_chi0 = sn_chi0 + bao_chi0
    joint_chi1 = sn_chi1 + bao_chi1
    delta = joint_chi0 - joint_chi1

    # Closure against the previously hosted and frozen external SN stage.
    assert_close("LCDM_chi2", joint_chi0, T1_LCDM_CHI2, CHI2_TOL)
    assert_close("LCDM_Omega_m", om0, T1_LCDM_OM, PARAM_TOL)
    assert_close("RCMS_chi2", joint_chi1, T1_RCMS_CHI2, CHI2_TOL)
    assert_close("RCMS_Omega_m", om1, T1_RCMS_OM, PARAM_TOL)
    assert_close("RCMS_A_R", ar1, T1_RCMS_AR, PARAM_TOL)
    assert_close("Delta_chi2", delta, T1_DELTA_CHI2, CHI2_TOL)

    n_sn = len(mu_obs)
    # The one BAO datum is exactly accompanied by one freely profiled scale
    # nuisance. It adds no shape information. Delta AIC remains the T1 value.
    delta_aic = delta - 2.0
    # For transparency we do not promote a joint BIC: adding one saturated
    # datum+nuisance does not create an independent shape constraint.

    print("RCMS Protocol 03 — P03-T3 external joint replication")
    print(f"DES_SN_N={n_sn} DES_BAO_N=1 precision_lambda_min={eig_min:.6e}")
    print(f"LCDM: joint_chi2={joint_chi0:.6f} Omega_m={om0:.6f} BAO_beta={beta0:.9f} BAO_shape={shape0:.9f}")
    print(f"RCMS: joint_chi2={joint_chi1:.6f} Omega_m={om1:.6f} A_R={ar1:.6f} BAO_beta={beta1:.9f} BAO_shape={shape1:.9f}")
    print(f"A_R_profile_delta_chi2_1=[{ar_lo:.6f},{ar_hi:.6f}]")
    print(f"Delta_chi2_LCDM_minus_RCMS={delta:.6f}")
    print(f"Delta_AIC_LCDM_minus_RCMS={delta_aic:.6f}")
    print("Delta_BIC_joint=NOT_PROMOTED_SINGLE_SATURATED_BAO_POINT")
    print(f"BAO_chi2_LCDM={bao_chi0:.3e} BAO_chi2_RCMS={bao_chi1:.3e}")
    print("P03_T3_INFORMATION_GAIN_FROM_BAO=ZERO_WITH_PREREGISTERED_FREE_SCALE")
    print("P03_T3_DIRECTION=POSITIVE_A_R_FROM_DES_SN_ONLY")
    print("note=The joint result is externally positive in direction but statistically equivalent to P03-T1; BAO adds no independent A_R information under the frozen nuisance policy.")


if __name__ == "__main__":
    main()
