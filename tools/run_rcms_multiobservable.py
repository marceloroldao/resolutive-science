#!/usr/bin/env python3
"""Joint H(z)+SN+BAO synthetic RCMS discrimination benchmark."""
from __future__ import annotations

from dataclasses import dataclass
from math import log
from random import Random
from statistics import mean, median

from rcms.background import LCDMParams, RCMSParams, RCMSEffectiveParams, h_lcdm, h_rcms_e020, h_rcms_effective
from rcms.observables import mu_lcdm, mu_effective, dv_lcdm, dv_effective

H0_GRID = (68.0, 69.0, 70.0, 71.0, 72.0)
OM_GRID = (0.26, 0.28, 0.30, 0.32, 0.34)
A_GRID = tuple(round(-0.10 + 0.02 * i, 10) for i in range(21))


@dataclass(frozen=True)
class Datum:
    probe: str
    z: float
    value: float
    sigma: float


def probe_layout() -> list[tuple[str, float]]:
    layout = [("H", 2.0 * i / 23.0) for i in range(24)]
    layout += [("SN", 0.02 + 1.58 * i / 36.0) for i in range(1, 37)]
    layout += [("BAO", z) for z in (0.20, 0.35, 0.50, 0.70, 1.00, 1.30)]
    return layout


def predict(layout: list[tuple[str, float]], lcdm: LCDMParams, a_r: float | None) -> tuple[float, ...]:
    rc = RCMSEffectiveParams(a_r=0.0 if a_r is None else a_r)
    out = []
    for probe, z in layout:
        if probe == "H":
            value = h_lcdm(z, lcdm) if a_r is None else h_rcms_effective(z, lcdm, rc)
        elif probe == "SN":
            value = mu_lcdm(z, lcdm) if a_r is None else mu_effective(z, lcdm, rc)
        elif probe == "BAO":
            value = dv_lcdm(z, lcdm) if a_r is None else dv_effective(z, lcdm, rc)
        else:
            raise ValueError(probe)
        out.append(value)
    return tuple(out)


def build_prediction_grids(layout: list[tuple[str, float]]):
    refs = []
    effs = []
    for h0 in H0_GRID:
        for om in OM_GRID:
            p = LCDMParams(h0=h0, omega_m=om)
            refs.append((p, predict(layout, p, None)))
            for a_r in A_GRID:
                try:
                    effs.append((p, a_r, predict(layout, p, a_r)))
                except ValueError:
                    continue
    return refs, effs


def simulate_joint(seed: int, injected: bool, layout: list[tuple[str, float]]) -> list[Datum]:
    rng = Random(seed)
    lcdm = LCDMParams(h0=70.0, omega_m=0.30)
    rc = RCMSParams(epsilon_r=0.16, s1=1.2)
    eff = RCMSEffectiveParams(a_r=0.16 * 1.2)
    out: list[Datum] = []
    for probe, z in layout:
        if probe == "H":
            truth = h_rcms_e020(z, lcdm, rc) if injected else h_lcdm(z, lcdm)
            sigma = 0.02 * truth
        elif probe == "SN":
            truth = mu_effective(z, lcdm, eff) if injected else mu_lcdm(z, lcdm)
            sigma = 0.10
        elif probe == "BAO":
            truth = dv_effective(z, lcdm, eff) if injected else dv_lcdm(z, lcdm)
            sigma = 0.015 * truth
        else:
            raise ValueError(probe)
        out.append(Datum(probe, z, rng.gauss(truth, sigma), sigma))
    return out


def chi2_cached(data: list[Datum], predictions: tuple[float, ...]) -> float:
    return sum(((d.value - p) / d.sigma) ** 2 for d, p in zip(data, predictions))


def fit_reference(data: list[Datum], refs):
    candidates = [(p, chi2_cached(data, pred)) for p, pred in refs]
    p, c2 = min(candidates, key=lambda item: item[1])
    return p, c2


def fit_effective(data: list[Datum], effs):
    candidates = [(p, a, chi2_cached(data, pred)) for p, a, pred in effs]
    p, a_r, c2 = min(candidates, key=lambda item: item[2])
    return p, a_r, c2


def run_ensemble(injected: bool, layout, refs, effs, seeds=range(20)) -> None:
    dchi2s = []
    aic_favor = bic_favor = 0
    a_vals = []
    h0_vals = []
    om_vals = []
    for seed in seeds:
        data = simulate_joint(seed, injected, layout)
        _, c2_ref = fit_reference(data, refs)
        eff_p, a_r, c2_eff = fit_effective(data, effs)
        dchi2 = c2_ref - c2_eff
        dchi2s.append(dchi2)
        a_vals.append(a_r)
        h0_vals.append(eff_p.h0)
        om_vals.append(eff_p.omega_m)
        if dchi2 > 2.0:
            aic_favor += 1
        if dchi2 > log(len(data)):
            bic_favor += 1

    label = "injected-RC-E020-joint" if injected else "null-LambdaCDM-joint"
    runs = len(dchi2s)
    print(f"[{label}]")
    print(f"  runs={runs} n_total={len(layout)}")
    print(f"  delta_chi2 mean={mean(dchi2s):.3f} median={median(dchi2s):.3f} max={max(dchi2s):.3f}")
    print(f"  AIC-favor fraction={aic_favor/runs:.3f}")
    print(f"  BIC-favor fraction={bic_favor/runs:.3f}")
    print(f"  A_R mean={mean(a_vals):.4f} median={median(a_vals):.4f}")
    print(f"  H0 mean={mean(h0_vals):.3f} Omega_m mean={mean(om_vals):.4f}")


if __name__ == "__main__":
    layout = probe_layout()
    refs, effs = build_prediction_grids(layout)
    run_ensemble(False, layout, refs, effs)
    run_ensemble(True, layout, refs, effs)
