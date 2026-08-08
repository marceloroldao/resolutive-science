"""Small dependency-free synthetic test utilities for RC-E020."""
from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Iterable, Sequence

from .background import (
    LCDMParams,
    RCMSParams,
    RCMSEffectiveParams,
    h_lcdm,
    h_rcms_e020,
    h_rcms_effective,
)


@dataclass(frozen=True)
class Observation:
    z: float
    h: float
    sigma: float


def make_grid(z_max: float = 2.0, n: int = 24) -> list[float]:
    if z_max <= 0 or n < 3:
        raise ValueError("z_max must be positive and n >= 3")
    return [z_max * i / (n - 1) for i in range(n)]


def simulate(
    z_values: Sequence[float],
    lcdm: LCDMParams,
    rcms: RCMSParams | None = None,
    fractional_sigma: float = 0.03,
    seed: int = 0,
) -> list[Observation]:
    if fractional_sigma <= 0:
        raise ValueError("fractional_sigma must be positive")
    rng = Random(seed)
    out: list[Observation] = []
    for z in z_values:
        truth = h_lcdm(z, lcdm) if rcms is None else h_rcms_e020(z, lcdm, rcms)
        sigma = fractional_sigma * truth
        out.append(Observation(z=z, h=rng.gauss(truth, sigma), sigma=sigma))
    return out


def chi2(data: Iterable[Observation], lcdm: LCDMParams, rcms: RCMSParams | None = None) -> float:
    total = 0.0
    for obs in data:
        pred = h_lcdm(obs.z, lcdm) if rcms is None else h_rcms_e020(obs.z, lcdm, rcms)
        total += ((obs.h - pred) / obs.sigma) ** 2
    return total


def chi2_effective(data: Iterable[Observation], lcdm: LCDMParams, rcms: RCMSEffectiveParams) -> float:
    total = 0.0
    for obs in data:
        pred = h_rcms_effective(obs.z, lcdm, rcms)
        total += ((obs.h - pred) / obs.sigma) ** 2
    return total


def grid_fit_e020(
    data: Sequence[Observation],
    lcdm: LCDMParams,
    epsilon_grid: Sequence[float],
    s1_grid: Sequence[float],
) -> tuple[RCMSParams, float]:
    best: RCMSParams | None = None
    best_chi2 = float("inf")
    for epsilon_r in epsilon_grid:
        for s1 in s1_grid:
            candidate = RCMSParams(epsilon_r=epsilon_r, s1=s1)
            try:
                value = chi2(data, lcdm, candidate)
            except ValueError:
                continue
            if value < best_chi2:
                best = candidate
                best_chi2 = value
    if best is None:
        raise ValueError("no admissible RC-E020 candidate on supplied grid")
    return best, best_chi2


def grid_fit_effective(
    data: Sequence[Observation],
    lcdm: LCDMParams,
    a_grid: Sequence[float],
) -> tuple[RCMSEffectiveParams, float]:
    best: RCMSEffectiveParams | None = None
    best_chi2 = float("inf")
    for a_r in a_grid:
        candidate = RCMSEffectiveParams(a_r=a_r)
        try:
            value = chi2_effective(data, lcdm, candidate)
        except ValueError:
            continue
        if value < best_chi2:
            best = candidate
            best_chi2 = value
    if best is None:
        raise ValueError("no admissible effective RCMS candidate on supplied grid")
    return best, best_chi2


def symmetric_grid(lo: float, hi: float, step: float) -> list[float]:
    if step <= 0 or hi < lo:
        raise ValueError("invalid grid bounds")
    values: list[float] = []
    x = lo
    while x <= hi + step * 1e-9:
        values.append(round(x, 12))
        x += step
    return values
