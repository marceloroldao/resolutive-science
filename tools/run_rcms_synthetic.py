#!/usr/bin/env python3
"""Run a compact reproducible synthetic benchmark for RC-E020."""
from __future__ import annotations

from rcms.background import LCDMParams, RCMSParams
from rcms.synthetic import chi2, grid_fit_e020, make_grid, simulate, symmetric_grid


def run_case(name: str, injected: RCMSParams | None, seed: int, fractional_sigma: float) -> None:
    lcdm = LCDMParams(h0=70.0, omega_m=0.3)
    z = make_grid(z_max=2.0, n=24)
    epsilon_grid = symmetric_grid(-0.20, 0.20, 0.02)
    s1_grid = symmetric_grid(0.0, 2.0, 0.1)
    data = simulate(z, lcdm, rcms=injected, fractional_sigma=fractional_sigma, seed=seed)
    best, best_chi2 = grid_fit_e020(data, lcdm, epsilon_grid, s1_grid)
    ref_chi2 = chi2(data, lcdm, None)
    delta_chi2 = ref_chi2 - best_chi2
    print(f"[{name}]")
    print(f"  seed={seed} n={len(data)} sigma_frac={fractional_sigma:.3f}")
    if injected is None:
        print("  injected=LambdaCDM null")
    else:
        print(f"  injected epsilon_R={injected.epsilon_r:.3f} s1={injected.s1:.3f}")
    print(f"  best epsilon_R={best.epsilon_r:.3f} s1={best.s1:.3f}")
    print(f"  chi2_ref={ref_chi2:.6f}")
    print(f"  chi2_rcms={best_chi2:.6f}")
    print(f"  delta_chi2={delta_chi2:.6f}")


def main() -> None:
    run_case("null", injected=None, seed=17, fractional_sigma=0.03)
    run_case(
        "injected",
        injected=RCMSParams(epsilon_r=0.16, s1=1.2),
        seed=23,
        fractional_sigma=0.02,
    )


if __name__ == "__main__":
    main()
