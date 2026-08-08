#!/usr/bin/env python3
"""Compare Lambda-CDM, effective RCMS, and full RC-E020 with common nuisances."""
from __future__ import annotations

from math import log
from statistics import mean, median

from rcms.background import LCDMParams, RCMSParams, h_rcms_e020
from rcms.observables import mu_e020, dv_e020
from tools.run_rcms_calibration_nuisance import (
    A_GRID,
    H0_GRID,
    OM_GRID,
    build_grids,
    layout,
    profiled_chi2,
    simulate,
)

EPS_GRID = (-0.04, 0.0, 0.04, 0.08, 0.12, 0.16, 0.20, 0.24)
S1_GRID = (0.4, 0.8, 1.2, 1.6, 2.0)


def full_predictions(pts, lcdm: LCDMParams, rc: RCMSParams):
    vals = []
    for probe, z in pts:
        if probe == "H":
            vals.append(h_rcms_e020(z, lcdm, rc))
        elif probe == "SN":
            vals.append(mu_e020(z, lcdm, rc))
        elif probe == "BAO":
            vals.append(dv_e020(z, lcdm, rc))
        else:
            raise ValueError(probe)
    return tuple(vals)


def build_full_grid(pts):
    grid = []
    for h0 in H0_GRID:
        for om in OM_GRID:
            p = LCDMParams(h0, om)
            for eps in EPS_GRID:
                for s1 in S1_GRID:
                    rc = RCMSParams(eps, s1)
                    try:
                        grid.append((p, eps, s1, full_predictions(pts, p, rc)))
                    except ValueError:
                        pass
    return grid


def fit_reference(data, refs):
    candidates = []
    for p, pred in refs:
        c2, sn_off, rd = profiled_chi2(data, pred)
        candidates.append((c2, p, sn_off, rd))
    return min(candidates, key=lambda x: x[0])


def fit_effective(data, effs):
    candidates = []
    for p, a_r, pred in effs:
        c2, sn_off, rd = profiled_chi2(data, pred)
        candidates.append((c2, p, a_r, sn_off, rd))
    return min(candidates, key=lambda x: x[0])


def fit_full(data, fulls):
    candidates = []
    for p, eps, s1, pred in fulls:
        c2, sn_off, rd = profiled_chi2(data, pred)
        candidates.append((c2, p, eps, s1, sn_off, rd))
    return min(candidates, key=lambda x: x[0])


def run(injected: bool, seeds=range(20)):
    pts = layout()
    refs, effs = build_grids(pts)
    fulls = build_full_grid(pts)
    nobs = len(pts)
    ln_n = log(nobs)

    d_eff, d_full = [], []
    eff_a, full_eps, full_s1 = [], [], []
    aic_wins = {"ref": 0, "effective": 0, "full": 0}
    bic_wins = {"ref": 0, "effective": 0, "full": 0}

    for seed in seeds:
        data = simulate(seed, injected, pts)
        ref = fit_reference(data, refs)
        eff = fit_effective(data, effs)
        full = fit_full(data, fulls)
        c_ref, c_eff, c_full = ref[0], eff[0], full[0]

        d_eff.append(c_ref - c_eff)
        d_full.append(c_ref - c_full)
        eff_a.append(eff[2])
        full_eps.append(full[2])
        full_s1.append(full[3])

        # Common parameters/nuisances cancel. Extras: effective=1, full=2.
        aic_scores = {"ref": c_ref, "effective": c_eff + 2.0, "full": c_full + 4.0}
        bic_scores = {"ref": c_ref, "effective": c_eff + ln_n, "full": c_full + 2.0 * ln_n}
        aic_wins[min(aic_scores, key=aic_scores.get)] += 1
        bic_wins[min(bic_scores, key=bic_scores.get)] += 1

    runs = len(d_eff)
    label = "injected-RC-E020" if injected else "null-LambdaCDM"
    print(f"[{label}-full-vs-effective]")
    print(f"  runs={runs} n_total={nobs}")
    print(f"  effective delta_chi2 mean={mean(d_eff):.3f} median={median(d_eff):.3f}")
    print(f"  full      delta_chi2 mean={mean(d_full):.3f} median={median(d_full):.3f}")
    print(f"  effective A_R mean={mean(eff_a):.4f}")
    print(f"  full epsilon_R mean={mean(full_eps):.4f} s1 mean={mean(full_s1):.4f}")
    print("  AIC winner fractions=" + ", ".join(f"{k}:{v/runs:.3f}" for k, v in aic_wins.items()))
    print("  BIC winner fractions=" + ", ".join(f"{k}:{v/runs:.3f}" for k, v in bic_wins.items()))


if __name__ == "__main__":
    run(False)
    run(True)
