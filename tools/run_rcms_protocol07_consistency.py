#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar, brentq
from scipy.stats import chi2

OUT = Path("results/rcms_protocol07_consistency.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

PROFILES = {
    "P01_02_primary": {"a": 0.187021, "lo": 0.098671, "hi": 0.276779},
    "P03_DES_SN5YR": {"a": 0.382099, "lo": 0.055322, "hi": 0.707729},
    "P04_eBOSS_DR16": {"a": 1.662222508, "lo": 0.650565914, "hi": 3.103626193},
    "P06_DESI_DR2": {"a": 0.210244178, "lo": 0.05, "hi": 0.40},
}


def delta_chi2(x, p):
    a, lo, hi = p["a"], p["lo"], p["hi"]
    sigma = a - lo if x <= a else hi - a
    return ((x - a) / sigma) ** 2


def summarize(keys):
    def total(x):
        return float(sum(delta_chi2(x, PROFILES[k]) for k in keys))

    opt = minimize_scalar(total, bounds=(-5.0, 5.0), method="bounded", options={"xatol": 1e-13})
    if not opt.success:
        raise RuntimeError("common-amplitude minimization failed")

    a_common = float(opt.x)
    q = float(opt.fun)
    target = q + 1.0

    def rootfun(x):
        return total(x) - target

    left = brentq(rootfun, -5.0, a_common, xtol=1e-13, rtol=1e-13)
    right = brentq(rootfun, a_common, 5.0, xtol=1e-13, rtol=1e-13)

    df = len(keys) - 1
    p_heterogeneity = float(chi2.sf(q, df)) if df > 0 else float("nan")
    i2 = float(max(0.0, (q - df) / q)) if q > 0 and df > 0 else 0.0
    delta_s_zero = float(total(0.0) - q)

    return {
        "included": list(keys),
        "A_common": a_common,
        "DeltaS_le_1_interval": [float(left), float(right)],
        "zero_in_common_interval": bool(left <= 0.0 <= right),
        "Q_heterogeneity": q,
        "descriptive_df": int(df),
        "heterogeneity_chi2_tail_p_descriptive": p_heterogeneity,
        "I2_descriptive": i2,
        "DeltaS_zero": delta_s_zero,
    }


keys = list(PROFILES)
primary = summarize(keys)
loo = {}
for omitted in keys:
    kept = [k for k in keys if k != omitted]
    loo[omitted] = summarize(kept)

all_loo_positive = all(v["A_common"] > 0 for v in loo.values())
major_loo_inconsistency = any(v["A_common"] <= 0 for v in loo.values())

if primary["A_common"] > 0 and not primary["zero_in_common_interval"]:
    if primary["Q_heterogeneity"] <= 7.815 and all_loo_positive and not major_loo_inconsistency:
        classification = "COMMON_POSITIVE_COMPATIBLE"
    else:
        classification = "COMMON_POSITIVE_HETEROGENEOUS"
elif primary["zero_in_common_interval"]:
    classification = "COMMON_ZERO_COMPATIBLE"
else:
    classification = "COMMON_SIGN_CONFLICT"

result = {
    "protocol": "P07-T1",
    "method": "asymmetric piecewise quadratic synthesis of frozen DeltaChi2<=1 profiles",
    "independence_assumed": False,
    "discovery_sigma_permitted": False,
    "profiles": PROFILES,
    "primary": primary,
    "leave_one_protocol_out": loo,
    "all_leave_one_out_common_best_fits_positive": bool(all_loo_positive),
    "classification": classification,
}

OUT.write_text(json.dumps(result, indent=2) + "\n")

print("RCMS Protocol 07 — Cross-protocol parameter consistency synthesis")
print("INDEPENDENCE_ASSUMED=NO")
print("DISCOVERY_SIGMA_PERMITTED=NO")
print(f"A_common={primary['A_common']:.9f}")
print(
    "COMMON_DeltaS_le_1_interval="
    f"[{primary['DeltaS_le_1_interval'][0]:.9f},{primary['DeltaS_le_1_interval'][1]:.9f}]"
)
print(f"Q_heterogeneity={primary['Q_heterogeneity']:.9f}")
print(f"heterogeneity_descriptive_df={primary['descriptive_df']}")
print(f"heterogeneity_tail_p_descriptive={primary['heterogeneity_chi2_tail_p_descriptive']:.9f}")
print(f"I2_descriptive={primary['I2_descriptive']:.9f}")
print(f"DeltaS_zero={primary['DeltaS_zero']:.9f}")
for omitted, v in loo.items():
    print(
        f"LOO_omit={omitted} A_common={v['A_common']:.9f} "
        f"interval=[{v['DeltaS_le_1_interval'][0]:.9f},{v['DeltaS_le_1_interval'][1]:.9f}] "
        f"Q={v['Q_heterogeneity']:.9f} zero_in_interval={v['zero_in_common_interval']}"
    )
print(f"P07_CLASSIFICATION={classification}")
print(f"machine_readable={OUT}")
print("note=DeltaS_zero is descriptive only and must not be converted to a discovery sigma because cross-protocol covariance is unavailable.")
