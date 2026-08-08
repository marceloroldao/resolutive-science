#!/usr/bin/env python3
"""Joint RCMS synthetic benchmark with profiled SN and BAO calibration nuisances."""
from __future__ import annotations

from dataclasses import dataclass
from math import log
from random import Random
from statistics import mean, median

from rcms.background import LCDMParams, RCMSParams, RCMSEffectiveParams, h_lcdm, h_rcms_e020, h_rcms_effective
from rcms.observables import mu_lcdm, mu_e020, mu_effective, dv_lcdm, dv_e020, dv_effective

H0_GRID = (68.0, 69.0, 70.0, 71.0, 72.0)
OM_GRID = (0.26, 0.28, 0.30, 0.32, 0.34)
A_GRID = tuple(round(-0.10 + 0.02 * i, 10) for i in range(21))
RD_TRUE = 147.0
SN_OFFSET_TRUE = 0.08


@dataclass(frozen=True)
class Datum:
    probe: str
    z: float
    value: float
    sigma: float


def layout() -> list[tuple[str, float]]:
    pts = [("H", 2.0 * i / 23.0) for i in range(24)]
    pts += [("SN", 0.02 + 1.58 * i / 36.0) for i in range(1, 37)]
    pts += [("BAO", z) for z in (0.20, 0.35, 0.50, 0.70, 1.00, 1.30)]
    return pts


def simulate(seed: int, injected: bool, pts: list[tuple[str, float]]) -> list[Datum]:
    rng = Random(seed)
    lcdm = LCDMParams(70.0, 0.30)
    rc = RCMSParams(0.16, 1.2)
    out = []
    for probe, z in pts:
        if probe == "H":
            truth = h_rcms_e020(z, lcdm, rc) if injected else h_lcdm(z, lcdm)
            sigma = 0.02 * truth
        elif probe == "SN":
            base = mu_e020(z, lcdm, rc) if injected else mu_lcdm(z, lcdm)
            truth = base + SN_OFFSET_TRUE
            sigma = 0.10
        elif probe == "BAO":
            dv = dv_e020(z, lcdm, rc) if injected else dv_lcdm(z, lcdm)
            truth = dv / RD_TRUE
            sigma = 0.015 * truth
        else:
            raise ValueError(probe)
        out.append(Datum(probe, z, rng.gauss(truth, sigma), sigma))
    return out


def predictions(pts, lcdm: LCDMParams, a_r: float | None):
    rc = RCMSEffectiveParams(0.0 if a_r is None else a_r)
    vals = []
    for probe, z in pts:
        if probe == "H":
            vals.append(h_lcdm(z, lcdm) if a_r is None else h_rcms_effective(z, lcdm, rc))
        elif probe == "SN":
            vals.append(mu_lcdm(z, lcdm) if a_r is None else mu_effective(z, lcdm, rc))
        elif probe == "BAO":
            # Cache raw D_V. The nuisance alpha=1/r_d is profiled analytically.
            vals.append(dv_lcdm(z, lcdm) if a_r is None else dv_effective(z, lcdm, rc))
    return tuple(vals)


def build_grids(pts):
    refs, effs = [], []
    for h0 in H0_GRID:
        for om in OM_GRID:
            p = LCDMParams(h0, om)
            refs.append((p, predictions(pts, p, None)))
            for a_r in A_GRID:
                try:
                    effs.append((p, a_r, predictions(pts, p, a_r)))
                except ValueError:
                    pass
    return refs, effs


def profiled_chi2(data: list[Datum], pred: tuple[float, ...]):
    h_idx = [i for i, d in enumerate(data) if d.probe == "H"]
    sn_idx = [i for i, d in enumerate(data) if d.probe == "SN"]
    bao_idx = [i for i, d in enumerate(data) if d.probe == "BAO"]

    chi2 = sum(((data[i].value - pred[i]) / data[i].sigma) ** 2 for i in h_idx)

    # Profile additive SN calibration/absolute-magnitude offset.
    wsum = sum(1.0 / data[i].sigma**2 for i in sn_idx)
    sn_offset = sum((data[i].value - pred[i]) / data[i].sigma**2 for i in sn_idx) / wsum
    chi2 += sum(((data[i].value - (pred[i] + sn_offset)) / data[i].sigma) ** 2 for i in sn_idx)

    # Profile alpha=1/r_d for BAO observable D_V/r_d.
    num = sum(pred[i] * data[i].value / data[i].sigma**2 for i in bao_idx)
    den = sum(pred[i] ** 2 / data[i].sigma**2 for i in bao_idx)
    alpha = num / den
    if alpha <= 0:
        return float("inf"), sn_offset, float("nan")
    rd = 1.0 / alpha
    chi2 += sum(((data[i].value - alpha * pred[i]) / data[i].sigma) ** 2 for i in bao_idx)
    return chi2, sn_offset, rd


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


def run(injected: bool, seeds=range(20)):
    pts = layout()
    refs, effs = build_grids(pts)
    dchi2s = []
    a_vals, sn_vals, rd_vals = [], [], []
    aic = bic = 0
    for seed in seeds:
        data = simulate(seed, injected, pts)
        c2_ref, _, _, _ = fit_reference(data, refs)
        c2_eff, _, a_r, sn_off, rd = fit_effective(data, effs)
        dchi2 = c2_ref - c2_eff
        dchi2s.append(dchi2)
        a_vals.append(a_r)
        sn_vals.append(sn_off)
        rd_vals.append(rd)
        if dchi2 > 2.0:
            aic += 1
        if dchi2 > log(len(data)):
            bic += 1

    label = "injected-RC-E020-calibration-nuisance" if injected else "null-LambdaCDM-calibration-nuisance"
    n = len(dchi2s)
    print(f"[{label}]")
    print(f"  runs={n} n_total={len(pts)}")
    print(f"  delta_chi2 mean={mean(dchi2s):.3f} median={median(dchi2s):.3f} max={max(dchi2s):.3f}")
    print(f"  AIC-favor fraction={aic/n:.3f}")
    print(f"  BIC-favor fraction={bic/n:.3f}")
    print(f"  A_R mean={mean(a_vals):.4f} median={median(a_vals):.4f}")
    print(f"  SN_offset mean={mean(sn_vals):.4f} true={SN_OFFSET_TRUE:.4f}")
    print(f"  r_d mean={mean(rd_vals):.3f} true={RD_TRUE:.3f}")


if __name__ == "__main__":
    run(False)
    run(True)
