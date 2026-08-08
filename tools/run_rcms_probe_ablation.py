#!/usr/bin/env python3
"""Probe-ablation study for the RCMS synthetic multiobservable benchmark."""
from __future__ import annotations

from math import log
from statistics import mean, median

from tools.run_rcms_multiobservable import (
    build_prediction_grids,
    fit_effective,
    fit_reference,
    probe_layout,
    simulate_joint,
)

PROBE_SETS = (
    ("H",),
    ("SN",),
    ("BAO",),
    ("H", "SN"),
    ("H", "BAO"),
    ("SN", "BAO"),
    ("H", "SN", "BAO"),
)


def subset_layout(probes: tuple[str, ...]):
    return [(probe, z) for probe, z in probe_layout() if probe in probes]


def run_case(probes: tuple[str, ...], injected: bool, seeds=range(20)):
    layout = subset_layout(probes)
    refs, effs = build_prediction_grids(layout)
    dchi2s = []
    a_vals = []
    aic = bic = 0

    full_layout = probe_layout()
    for seed in seeds:
        full_data = simulate_joint(seed, injected, full_layout)
        data = [d for d in full_data if d.probe in probes]
        _, c2_ref = fit_reference(data, refs)
        _, a_r, c2_eff = fit_effective(data, effs)
        dchi2 = c2_ref - c2_eff
        dchi2s.append(dchi2)
        a_vals.append(a_r)
        if dchi2 > 2.0:
            aic += 1
        if dchi2 > log(len(data)):
            bic += 1

    runs = len(dchi2s)
    return {
        "n": len(layout),
        "mean_dchi2": mean(dchi2s),
        "median_dchi2": median(dchi2s),
        "aic": aic / runs,
        "bic": bic / runs,
        "mean_a": mean(a_vals),
    }


def report(injected: bool):
    label = "injected-RC-E020" if injected else "null-LambdaCDM"
    print(f"[{label}-probe-ablation]")
    for probes in PROBE_SETS:
        result = run_case(probes, injected)
        name = "+".join(probes)
        print(
            f"  {name:8s} n={result['n']:2d} "
            f"mean_dchi2={result['mean_dchi2']:.3f} "
            f"median={result['median_dchi2']:.3f} "
            f"AIC={result['aic']:.3f} BIC={result['bic']:.3f} "
            f"A_R={result['mean_a']:.4f}"
        )


if __name__ == "__main__":
    report(False)
    report(True)
