#!/usr/bin/env python3
"""RCMS Protocol 03 T2: DES Y6 no-DESI angular BAO identifiability.

The published cosmology datum is a single transverse BAO dilation alpha at
z_eff=0.851. Protocol 03 leaves the global BAO scale c/(H0*r_d) free and adds
no CMB/SH0ES calibration. Therefore this script demonstrates, rather than
hides, the exact one-point scale degeneracy.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "rcms" / "des_y6_bao_nodesi_alpha_v1.csv"


def load_record():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise RuntimeError(f"expected exactly one compressed BAO datum, found {len(rows)}")
    r = rows[0]
    return float(r["z_eff"]), float(r["alpha"]), float(r["sigma_alpha"]), r


def simpson_integral(om: float, ar: float, z: float, n: int = 400) -> float:
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


def profiled_single_point(om: float, ar: float, z: float, alpha_obs: float, sigma: float):
    shape = simpson_integral(om, ar, z)
    # alpha_th = beta * shape, where beta absorbs the global BAO scale and the
    # fixed fiducial normalization. With one datum beta has an analytic fit.
    beta_hat = alpha_obs / shape
    alpha_th = beta_hat * shape
    chi2 = ((alpha_obs - alpha_th) / sigma) ** 2
    return shape, beta_hat, chi2


def main() -> None:
    z, alpha, sigma, meta = load_record()
    if abs(z - 0.851) > 1e-12 or abs(alpha - 0.9690) > 1e-12 or abs(sigma - 0.0296) > 1e-12:
        raise RuntimeError("frozen DES Y6 no-DESI BAO metadata changed")

    # Representative shapes are declared only to expose the degeneracy; they
    # are not fitted to the datum and are not used to select a preferred model.
    cases = [
        ("LCDM_OM030", 0.30, 0.0),
        ("LCDM_OM040", 0.40, 0.0),
        ("RCMS_P01", 0.30, 0.187021),
        ("RCMS_DES_SN_T1", 0.266117, 0.382099),
        ("RCMS_NEGATIVE_CHECK", 0.30, -0.30),
    ]

    max_chi2 = 0.0
    print("RCMS Protocol 03 — P03-T2 DES Y6 DESI-independent angular BAO")
    print(f"dataset={meta['dataset']} split={meta['split']} z_eff={z:.3f}")
    print(f"alpha_obs={alpha:.4f} sigma_alpha={sigma:.4f} source={meta['source']}")
    print("global_scale_nuisance=free no_CMB_prior=yes no_SH0ES_prior=yes")
    for label, om, ar in cases:
        shape, beta, chi2 = profiled_single_point(om, ar, z, alpha, sigma)
        max_chi2 = max(max_chi2, chi2)
        print(
            f"case={label} Omega_m={om:.6f} A_R={ar:.6f} "
            f"shape_integral={shape:.9f} profiled_beta={beta:.9f} chi2={chi2:.3e}"
        )

    if max_chi2 > 1e-20:
        raise RuntimeError(f"one-point scale degeneracy failed numerically: max chi2={max_chi2:.3e}")

    print("P03_T2_IDENTIFIABILITY=SCALE_DEGENERATE_SINGLE_TRANSVERSE_BAO")
    print("P03_T2_MODEL_SELECTION=NOT_IDENTIFIABLE_WITH_FREE_GLOBAL_SCALE")
    print("note=No early-Universe calibration is introduced to manufacture a BAO-alone A_R constraint.")


if __name__ == "__main__":
    main()
