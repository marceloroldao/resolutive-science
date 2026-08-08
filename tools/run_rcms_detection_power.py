"""Map effective RCMS detection power after refitting H0 and Omega_m."""
from __future__ import annotations

from math import log

from rcms.background import LCDMParams, RCMSParams, RCMSEffectiveParams, h_lcdm, h_rcms_effective
from rcms.synthetic import Observation, make_grid, simulate, symmetric_grid


def chi2_ref(data: list[Observation], lcdm: LCDMParams) -> float:
    return sum(((o.h - h_lcdm(o.z, lcdm)) / o.sigma) ** 2 for o in data)


def chi2_eff(data: list[Observation], lcdm: LCDMParams, a_r: float) -> float:
    p = RCMSEffectiveParams(a_r=a_r)
    total = 0.0
    for o in data:
        try:
            pred = h_rcms_effective(o.z, lcdm, p)
        except ValueError:
            return float('inf')
        total += ((o.h - pred) / o.sigma) ** 2
    return total


def best_scores(data: list[Observation]):
    h0_grid = symmetric_grid(67.0, 73.0, 1.0)
    om_grid = symmetric_grid(0.26, 0.34, 0.02)
    a_grid = symmetric_grid(-0.30, 0.30, 0.02)
    best_ref = float('inf')
    best_eff = float('inf')
    for h0 in h0_grid:
        for om in om_grid:
            lcdm = LCDMParams(h0=h0, omega_m=om)
            best_ref = min(best_ref, chi2_ref(data, lcdm))
            for a_r in a_grid:
                best_eff = min(best_eff, chi2_eff(data, lcdm, a_r))
    dchi2 = best_ref - best_eff
    return dchi2, dchi2 - 2.0, dchi2 - log(len(data))


def evaluate(n: int, sigma_frac: float, seeds=range(20)) -> None:
    truth = LCDMParams(h0=70.0, omega_m=0.3)
    injected = RCMSParams(epsilon_r=0.16, s1=1.2)
    z = make_grid(2.0, n)
    aic_hits = bic_hits = 0
    dsum = 0.0
    for seed in seeds:
        data = simulate(z, truth, injected, fractional_sigma=sigma_frac, seed=seed)
        dchi2, daic, dbic = best_scores(data)
        dsum += dchi2
        aic_hits += daic > 0
        bic_hits += dbic > 0
    runs = len(list(seeds))
    print(
        f"n={n:02d} sigma={sigma_frac:.3f} "
        f"mean_dchi2={dsum/runs:.3f} "
        f"AIC_power={aic_hits/runs:.3f} BIC_power={bic_hits/runs:.3f}"
    )


if __name__ == '__main__':
    for n in (24, 48):
        for sigma in (0.01, 0.02, 0.03, 0.05):
            evaluate(n, sigma)
