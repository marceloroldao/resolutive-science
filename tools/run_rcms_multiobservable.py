#!/usr/bin/env python3
"""Joint H(z)+SN+BAO synthetic RCMS discrimination benchmark."""
from __future__ import annotations

from dataclasses import dataclass
from math import log
from random import Random
from statistics import mean, median

from rcms.background import LCDMParams, RCMSParams, RCMSEffectiveParams, h_lcdm, h_rcms_e020, h_rcms_effective
from rcms.observables import mu_lcdm, mu_effective, dv_lcdm, dv_effective


@dataclass(frozen=True)
class Datum:
    probe: str
    z: float
    value: float
    sigma: float


def simulate_joint(seed: int, injected: bool) -> list[Datum]:
    rng = Random(seed)
    lcdm = LCDMParams(h0=70.0, omega_m=0.30)
    rc = RCMSParams(epsilon_r=0.16, s1=1.2)
    out: list[Datum] = []

    # H(z): 24 points, 2% fractional uncertainty.
    for i in range(24):
        z = 2.0 * i / 23.0
        truth = h_rcms_e020(z, lcdm, rc) if injected else h_lcdm(z, lcdm)
        sigma = 0.02 * truth
        out.append(Datum("H", z, rng.gauss(truth, sigma), sigma))

    # Supernova-like distance moduli: 36 points, 0.10 mag uncertainty.
    for i in range(1, 37):
        z = 0.02 + 1.58 * i / 36.0
        if injected:
            # Generate through the effective low-signal approximation using injected A_R.
            truth = mu_effective(z, lcdm, RCMSEffectiveParams(a_r=0.16 * 1.2))
        else:
            truth = mu_lcdm(z, lcdm)
        sigma = 0.10
        out.append(Datum("SN", z, rng.gauss(truth, sigma), sigma))

    # Isotropic BAO-like D_V: 6 redshifts, 1.5% fractional uncertainty.
    for z in (0.20, 0.35, 0.50, 0.70, 1.00, 1.30):
        if injected:
            truth = dv_effective(z, lcdm, RCMSEffectiveParams(a_r=0.16 * 1.2))
        else:
            truth = dv_lcdm(z, lcdm)
        sigma = 0.015 * truth
        out.append(Datum("BAO", z, rng.gauss(truth, sigma), sigma))

    return out


def chi2_joint(data: list[Datum], lcdm: LCDMParams, a_r: float | None) -> float:
    rc = RCMSEffectiveParams(a_r=0.0 if a_r is None else a_r)
    total = 0.0
    for d in data:
        if d.probe == "H":
            pred = h_lcdm(d.z, lcdm) if a_r is None else h_rcms_effective(d.z, lcdm, rc)
        elif d.probe == "SN":
            pred = mu_lcdm(d.z, lcdm) if a_r is None else mu_effective(d.z, lcdm, rc)
        elif d.probe == "BAO":
            pred = dv_lcdm(d.z, lcdm) if a_r is None else dv_effective(d.z, lcdm, rc)
        else:
            raise ValueError(d.probe)
        total += ((d.value - pred) / d.sigma) ** 2
    return total


def fit_reference(data: list[Datum]) -> tuple[LCDMParams, float]:
    best = None
    best_chi2 = float("inf")
    for h0 in (68.0, 69.0, 70.0, 71.0, 72.0):
        for om in (0.26, 0.28, 0.30, 0.32, 0.34):
            p = LCDMParams(h0=h0, omega_m=om)
            c2 = chi2_joint(data, p, None)
            if c2 < best_chi2:
                best, best_chi2 = p, c2
    assert best is not None
    return best, best_chi2


def fit_effective(data: list[Datum]) -> tuple[LCDMParams, float, float]:
    best = None
    best_a = 0.0
    best_chi2 = float("inf")
    a_grid = [round(-0.10 + 0.02 * i, 10) for i in range(21)]  # -0.10 .. 0.30
    for h0 in (68.0, 69.0, 70.0, 71.0, 72.0):
        for om in (0.26, 0.28, 0.30, 0.32, 0.34):
            p = LCDMParams(h0=h0, omega_m=om)
            for a_r in a_grid:
                try:
                    c2 = chi2_joint(data, p, a_r)
                except ValueError:
                    continue
                if c2 < best_chi2:
                    best, best_a, best_chi2 = p, a_r, c2
    assert best is not None
    return best, best_a, best_chi2


def run_ensemble(injected: bool, seeds=range(20)) -> None:
    dchi2s = []
    aic_favor = 0
    bic_favor = 0
    a_vals = []
    h0_vals = []
    om_vals = []
    for seed in seeds:
        data = simulate_joint(seed, injected)
        ref_p, c2_ref = fit_reference(data)
        eff_p, a_r, c2_eff = fit_effective(data)
        dchi2 = c2_ref - c2_eff
        dchi2s.append(dchi2)
        a_vals.append(a_r)
        h0_vals.append(eff_p.h0)
        om_vals.append(eff_p.omega_m)
        n = len(data)
        # Effective model has one additional parameter relative to reference.
        if dchi2 > 2.0:
            aic_favor += 1
        if dchi2 > log(n):
            bic_favor += 1

    label = "injected-RC-E020-joint" if injected else "null-LambdaCDM-joint"
    runs = len(dchi2s)
    print(f"[{label}]")
    print(f"  runs={runs} n_total=66")
    print(f"  delta_chi2 mean={mean(dchi2s):.3f} median={median(dchi2s):.3f} max={max(dchi2s):.3f}")
    print(f"  AIC-favor fraction={aic_favor/runs:.3f}")
    print(f"  BIC-favor fraction={bic_favor/runs:.3f}")
    print(f"  A_R mean={mean(a_vals):.4f} median={median(a_vals):.4f}")
    print(f"  H0 mean={mean(h0_vals):.3f} Omega_m mean={mean(om_vals):.4f}")


if __name__ == "__main__":
    run_ensemble(False)
    run_ensemble(True)
