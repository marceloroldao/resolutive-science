"""Background-distance observables for RCMS synthetic multi-probe tests."""
from __future__ import annotations

from math import log10
from typing import Callable

from .background import LCDMParams, RCMSEffectiveParams, h_lcdm, h_rcms_effective

C_KM_S = 299792.458


def _simpson_integral(fn: Callable[[float], float], a: float, b: float, n: int = 400) -> float:
    if b < a:
        raise ValueError("integration upper bound must be >= lower bound")
    if n < 2:
        raise ValueError("n must be >= 2")
    if n % 2:
        n += 1
    if a == b:
        return 0.0
    h = (b - a) / n
    total = fn(a) + fn(b)
    for i in range(1, n):
        x = a + i * h
        total += (4.0 if i % 2 else 2.0) * fn(x)
    return total * h / 3.0


def comoving_distance_lcdm(z: float, params: LCDMParams) -> float:
    if z < 0:
        raise ValueError("z must be non-negative")
    return C_KM_S * _simpson_integral(lambda zz: 1.0 / h_lcdm(zz, params), 0.0, z)


def comoving_distance_effective(z: float, params: LCDMParams, rcms: RCMSEffectiveParams) -> float:
    if z < 0:
        raise ValueError("z must be non-negative")
    return C_KM_S * _simpson_integral(lambda zz: 1.0 / h_rcms_effective(zz, params, rcms), 0.0, z)


def luminosity_distance_lcdm(z: float, params: LCDMParams) -> float:
    return (1.0 + z) * comoving_distance_lcdm(z, params)


def luminosity_distance_effective(z: float, params: LCDMParams, rcms: RCMSEffectiveParams) -> float:
    return (1.0 + z) * comoving_distance_effective(z, params, rcms)


def distance_modulus_from_mpc(dl_mpc: float) -> float:
    if dl_mpc <= 0:
        raise ValueError("luminosity distance must be positive")
    return 5.0 * log10(dl_mpc) + 25.0


def mu_lcdm(z: float, params: LCDMParams) -> float:
    return distance_modulus_from_mpc(luminosity_distance_lcdm(z, params))


def mu_effective(z: float, params: LCDMParams, rcms: RCMSEffectiveParams) -> float:
    return distance_modulus_from_mpc(luminosity_distance_effective(z, params, rcms))


def dv_lcdm(z: float, params: LCDMParams) -> float:
    """Isotropic BAO volume distance D_V in Mpc."""
    if z <= 0:
        raise ValueError("BAO z must be positive")
    dm = comoving_distance_lcdm(z, params)
    return (dm * dm * C_KM_S * z / h_lcdm(z, params)) ** (1.0 / 3.0)


def dv_effective(z: float, params: LCDMParams, rcms: RCMSEffectiveParams) -> float:
    if z <= 0:
        raise ValueError("BAO z must be positive")
    dm = comoving_distance_effective(z, params, rcms)
    return (dm * dm * C_KM_S * z / h_rcms_effective(z, params, rcms)) ** (1.0 / 3.0)
