"""Background cosmology functions for RCMS synthetic falsification tests."""
from __future__ import annotations

from dataclasses import dataclass
from math import log1p, sqrt, tanh


@dataclass(frozen=True)
class LCDMParams:
    """Flat Lambda-CDM background parameters used as the reference model."""

    h0: float = 70.0
    omega_m: float = 0.3

    def validate(self) -> None:
        if self.h0 <= 0:
            raise ValueError("h0 must be positive")
        if not 0.0 < self.omega_m < 1.0:
            raise ValueError("omega_m must lie strictly between 0 and 1")


@dataclass(frozen=True)
class RCMSParams:
    """RC-E020 deformation parameters."""

    epsilon_r: float = 0.0
    s1: float = 0.0


@dataclass(frozen=True)
class RCMSEffectiveParams:
    """One-parameter low-signal effective deformation amplitude."""

    a_r: float = 0.0


def e2_lcdm(z: float, params: LCDMParams) -> float:
    """Dimensionless squared expansion rate E(z)^2 for flat Lambda-CDM."""
    params.validate()
    if z < 0:
        raise ValueError("z must be non-negative")
    return params.omega_m * (1.0 + z) ** 3 + (1.0 - params.omega_m)


def h_lcdm(z: float, params: LCDMParams) -> float:
    """Reference H(z) in the same units as h0."""
    return params.h0 * sqrt(e2_lcdm(z, params))


def deformation_e020(z: float, params: RCMSParams) -> float:
    """Dimensionless RC-E020 deformation F_R(z)."""
    if z < 0:
        raise ValueError("z must be non-negative")
    return params.epsilon_r * tanh(params.s1 * log1p(z))


def deformation_effective(z: float, params: RCMSEffectiveParams) -> float:
    """Low-signal RC-E020 approximation F_eff=A_R ln(1+z).

    RC-E020 gives tanh(x)~x for |x| << 1, so
    epsilon_R*tanh[s1 ln(1+z)] ~ (epsilon_R*s1) ln(1+z).
    The effective parameter is A_R=epsilon_R*s1.
    """
    if z < 0:
        raise ValueError("z must be non-negative")
    return params.a_r * log1p(z)


def h_rcms_e020(z: float, lcdm: LCDMParams, rcms: RCMSParams) -> float:
    """RC-E020 expansion rate.

    Implements
        H_A^2 = H_ref^2 + H0^2 epsilon_R tanh[s1 ln(1+z)].
    """
    base_e2 = e2_lcdm(z, lcdm)
    total_e2 = base_e2 + deformation_e020(z, rcms)
    if total_e2 <= 0:
        raise ValueError("RC-E020 violates positive expansion-square requirement RC-R006")
    return lcdm.h0 * sqrt(total_e2)


def h_rcms_effective(z: float, lcdm: LCDMParams, rcms: RCMSEffectiveParams) -> float:
    """One-parameter low-signal effective RCMS expansion rate."""
    base_e2 = e2_lcdm(z, lcdm)
    total_e2 = base_e2 + deformation_effective(z, rcms)
    if total_e2 <= 0:
        raise ValueError("effective RCMS model violates positive expansion-square requirement")
    return lcdm.h0 * sqrt(total_e2)
