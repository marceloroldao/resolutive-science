#!/usr/bin/env python3
"""Multi-seed synthetic calibration for RC-E020 versus flat Lambda-CDM."""
from __future__ import annotations

from math import log
from statistics import mean, median

from rcms.background import LCDMParams, RCMSParams
from rcms.synthetic import chi2, grid_fit_e020, make_grid, simulate, symmetric_grid


def summarize(label: str, deltas: list[float], eps: list[float], s1: list[float], n: int) -> None:
    aic_adv = [d - 4.0 for d in deltas]  # RCMS adds two fitted parameters.
    bic_adv = [d - 2.0 * log(n) for d in deltas]
    print(f"[{label}]")
    print(f"  runs={len(deltas)} n_per_run={n}")
    print(f"  delta_chi2 mean={mean(deltas):.6f} median={median(deltas):.6f} max={max(deltas):.6f}")
    print(f"  AIC-favor fraction={sum(x > 0 for x in aic_adv)/len(aic_adv):.3f}")
    print(f"  BIC-favor fraction={sum(x > 0 for x in bic_adv)/len(bic_adv):.3f}")
    print(f"  best epsilon_R mean={mean(eps):.6f} median={median(eps):.6f}")
    print(f"  best s1 mean={mean(s1):.6f} median={median(s1):.6f}")


def evaluate(injected: RCMSParams | None, seeds: range, fractional_sigma: float):
    lcdm = LCDMParams(h0=70.0, omega_m=0.3)
    z = make_grid(z_max=2.0, n=24)
    eps_grid = symmetric_grid(-0.20, 0.20, 0.02)
    s1_grid = symmetric_grid(0.0, 2.0, 0.1)
    deltas: list[float] = []
    eps: list[float] = []
    s1: list[float] = []
    for seed in seeds:
        data = simulate(z, lcdm, rcms=injected, fractional_sigma=fractional_sigma, seed=seed)
        best, fit_chi2 = grid_fit_e020(data, lcdm, eps_grid, s1_grid)
        ref_chi2 = chi2(data, lcdm, None)
        deltas.append(ref_chi2 - fit_chi2)
        eps.append(best.epsilon_r)
        s1.append(best.s1)
    return deltas, eps, s1, len(z)


def main() -> None:
    null = evaluate(None, range(100, 150), fractional_sigma=0.03)
    summarize("null-LambdaCDM", *null)
    injected_model = RCMSParams(epsilon_r=0.16, s1=1.2)
    injected = evaluate(injected_model, range(200, 250), fractional_sigma=0.02)
    summarize("injected-RC-E020", *injected)


if __name__ == "__main__":
    main()
