"""Synthetic RCMS comparison with H0 and omega_m re-fitted in both models."""
from __future__ import annotations

from math import log
from statistics import mean, median

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


def fit_ref(data: list[Observation], h0_grid: list[float], om_grid: list[float]):
    best = None
    best_chi2 = float('inf')
    for h0 in h0_grid:
        for om in om_grid:
            p = LCDMParams(h0=h0, omega_m=om)
            value = chi2_ref(data, p)
            if value < best_chi2:
                best, best_chi2 = p, value
    return best, best_chi2


def fit_eff(data: list[Observation], h0_grid: list[float], om_grid: list[float], a_grid: list[float]):
    best = None
    best_chi2 = float('inf')
    for h0 in h0_grid:
        for om in om_grid:
            lcdm = LCDMParams(h0=h0, omega_m=om)
            for a_r in a_grid:
                value = chi2_eff(data, lcdm, a_r)
                if value < best_chi2:
                    best, best_chi2 = (lcdm, a_r), value
    return best, best_chi2


def run_case(label: str, injected: RCMSParams | None, sigma_frac: float, seeds=range(30)) -> None:
    truth_lcdm = LCDMParams(h0=70.0, omega_m=0.3)
    z = make_grid(2.0, 24)
    h0_grid = symmetric_grid(67.0, 73.0, 1.0)
    om_grid = symmetric_grid(0.26, 0.34, 0.02)
    a_grid = symmetric_grid(-0.30, 0.30, 0.02)

    deltas = []
    daics = []
    dbics = []
    h0_ref = []
    om_ref = []
    h0_eff = []
    om_eff = []
    a_eff = []

    for seed in seeds:
        data = simulate(z, truth_lcdm, injected, fractional_sigma=sigma_frac, seed=seed)
        pref, c_ref = fit_ref(data, h0_grid, om_grid)
        peff, c_eff = fit_eff(data, h0_grid, om_grid, a_grid)
        lcdm_eff, a_r = peff
        dchi2 = c_ref - c_eff
        deltas.append(dchi2)
        daics.append(dchi2 - 2.0)  # one additional parameter
        dbics.append(dchi2 - log(len(data)))
        h0_ref.append(pref.h0); om_ref.append(pref.omega_m)
        h0_eff.append(lcdm_eff.h0); om_eff.append(lcdm_eff.omega_m); a_eff.append(a_r)

    print(f"[{label}]")
    print(f"  delta_chi2 mean={mean(deltas):.6f} median={median(deltas):.6f} max={max(deltas):.6f}")
    print(f"  AIC-favor fraction={sum(x > 0 for x in daics)/len(daics):.3f}")
    print(f"  BIC-favor fraction={sum(x > 0 for x in dbics)/len(dbics):.3f}")
    print(f"  ref H0 mean={mean(h0_ref):.3f} Omega_m mean={mean(om_ref):.4f}")
    print(f"  eff H0 mean={mean(h0_eff):.3f} Omega_m mean={mean(om_eff):.4f}")
    print(f"  eff A_R mean={mean(a_eff):.6f} median={median(a_eff):.6f}")


if __name__ == '__main__':
    run_case('null-LambdaCDM-nuisance-refit', None, 0.03)
    run_case('injected-RC-E020-nuisance-refit', RCMSParams(epsilon_r=0.16, s1=1.2), 0.02)
