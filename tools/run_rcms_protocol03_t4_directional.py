#!/usr/bin/env python3
"""RCMS Protocol 03 T4: directional consistency without refitting."""
from __future__ import annotations

import math

# Frozen Protocol 01/02 region.
P01_AR = 0.187021
P01_LO = 0.098671
P01_HI = 0.276779

# Frozen hosted Protocol 03 DES-SN / joint external region.
P03_AR = 0.382099
P03_LO = 0.055322
P03_HI = 0.707729
P03_DELTA_CHI2 = 1.366399
P03_DELTA_AIC = -0.633601


def main() -> None:
    overlap_lo = max(P01_LO, P03_LO)
    overlap_hi = min(P01_HI, P03_HI)
    overlap = max(0.0, overlap_hi - overlap_lo)
    if overlap <= 0.0:
        label = "NO_INTERVAL_OVERLAP"
    elif P01_AR > 0.0 and P03_AR > 0.0:
        label = "POSITIVE_INTERVAL_OVERLAP"
    else:
        label = "MIXED_SIGN_OVERLAP"

    # A descriptive scale check only: approximate each Delta-chi2=1 profile by
    # half its total width. This is not used as a discovery significance.
    s1 = 0.5 * (P01_HI - P01_LO)
    s3 = 0.5 * (P03_HI - P03_LO)
    combined = math.sqrt(s1 * s1 + s3 * s3)
    point_separation_sigma_like = abs(P03_AR - P01_AR) / combined

    print("RCMS Protocol 03 — P03-T4 directional consistency")
    print(f"P01_A_R={P01_AR:.6f} P01_interval=[{P01_LO:.6f},{P01_HI:.6f}]")
    print(f"P03_A_R={P03_AR:.6f} P03_interval=[{P03_LO:.6f},{P03_HI:.6f}]")
    print(f"overlap_interval=[{overlap_lo:.6f},{overlap_hi:.6f}] overlap_width={overlap:.6f}")
    print(f"point_separation_descriptive_sigma_like={point_separation_sigma_like:.6f}")
    print(f"P03_Delta_chi2={P03_DELTA_CHI2:.6f} P03_Delta_AIC={P03_DELTA_AIC:.6f}")
    print("P03_BAO_DIRECTIONAL_INFORMATION=NONE_FREE_SCALE_SINGLE_POINT")
    print(f"P03_T4_DIRECTIONAL_COMPATIBILITY={label}")
    print("note=Directional compatibility is not model-selection evidence or validation of Resolutive Cosmology.")

    if label != "POSITIVE_INTERVAL_OVERLAP":
        raise RuntimeError(f"frozen external region is not positively compatible: {label}")


if __name__ == "__main__":
    main()
