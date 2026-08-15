#!/usr/bin/env python3
import json
import math
from pathlib import Path

OUT = Path("results/rcms_protocol08_log_provenance.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

# P08-T0/T1: numerical regression of the exact logarithmic homomorphism.
s1_values = [-2.0, -0.5, 0.0, 0.25, 1.0, 3.0]
lambdas = [0.125, 0.25, 0.5, 0.8, 1.0, 1.25, 2.0, 4.0, 10.0]
max_comp_residual = 0.0
max_identity_residual = 0.0
for s1 in s1_values:
    S = lambda lam: s1 * math.log(lam)
    max_identity_residual = max(max_identity_residual, abs(S(1.0)))
    for l1 in lambdas:
        for l2 in lambdas:
            residual = abs(S(l1 * l2) - S(l1) - S(l2))
            max_comp_residual = max(max_comp_residual, residual)

composition_pass = max_comp_residual < 1e-12 and max_identity_residual < 1e-15

# P08-T2: solve the largest positive |x| satisfying a relative tanh-linearization error threshold.
def relative_error(x: float) -> float:
    tx = math.tanh(x)
    return abs(tx - x) / max(abs(tx), 1e-15)


def threshold_x(target: float) -> float:
    lo, hi = 0.0, 5.0
    for _ in range(120):
        mid = (lo + hi) / 2.0
        if relative_error(mid) <= target:
            lo = mid
        else:
            hi = mid
    return lo

thresholds = {"0.1pct": 0.001, "1pct": 0.01, "5pct": 0.05}
x_limits = {name: threshold_x(val) for name, val in thresholds.items()}

# Validate the expected local cubic behavior at very small x.
small_x = 1e-3
cubic_ratio = abs((math.tanh(small_x) - small_x) / (-(small_x ** 3) / 3.0))
taylor_pass = abs(cubic_ratio - 1.0) < 1e-5

# P08-T3: descriptive domain diagnostic after T0/T2 are fixed.
A_COMMON = 0.211141330
z_ranges = [1.0, 2.33, 3.0]
domain = {}
for label, xmax in x_limits.items():
    domain[label] = {}
    for zmax in z_ranges:
        logspan = math.log1p(zmax)
        s1_max = xmax / logspan
        epsilon_min_for_product = A_COMMON / s1_max if s1_max > 0 else math.inf
        domain[label][f"z<={zmax:g}"] = {
            "x_max": xmax,
            "ln_1_plus_zmax": logspan,
            "abs_s1_max": s1_max,
            "abs_epsilon_min_if_epsilon_times_s1_equals_A_common": epsilon_min_for_product,
        }

# Nonempty domain is a mathematical statement here: finite positive s1_max exists for every frozen range/threshold.
domain_nonempty = all(
    entry["abs_s1_max"] > 0 and math.isfinite(entry["abs_epsilon_min_if_epsilon_times_s1_equals_A_common"])
    for block in domain.values() for entry in block.values()
)

if composition_pass and taylor_pass and domain_nonempty:
    classification = "LOG_FORM_CONDITIONALLY_DERIVED"
else:
    classification = "LOG_FORM_PROVENANCE_FAILED"

result = {
    "protocol": "P08",
    "hypothesis": "continuous additive drift under multiplicative positive scale composition",
    "derived_form": "S(lambda)=s1*ln(lambda)",
    "redshift_map": "lambda=1+z",
    "T0_dimensionless_log_argument": True,
    "T1_max_composition_residual": max_comp_residual,
    "T1_max_identity_residual": max_identity_residual,
    "T1_pass": composition_pass,
    "T2_relative_error_x_limits": x_limits,
    "T2_small_x_cubic_ratio": cubic_ratio,
    "T2_taylor_pass": taylor_pass,
    "T3_A_common_descriptive": A_COMMON,
    "T3_domain_diagnostics": domain,
    "T3_domain_nonempty": domain_nonempty,
    "classification": classification,
    "scientific_boundary": "conditional mathematical provenance only; P08-H001 is not derived from a fundamental Resolutive Master Equation",
}
OUT.write_text(json.dumps(result, indent=2) + "\n")

print("RCMS Protocol 08 — logarithmic provenance")
print("PHYSICAL_LAW_CLAIM=NO")
print("MASTER_EQUATION_DERIVATION=NO")
print("CONDITIONAL_SCALE_COMPOSITION_DERIVATION=YES")
print(f"T1_max_composition_residual={max_comp_residual:.3e}")
print(f"T1_max_identity_residual={max_identity_residual:.3e}")
print(f"T1_PASS={composition_pass}")
for label, xmax in x_limits.items():
    print(f"T2_x_limit_{label}={xmax:.12f}")
print(f"T2_small_x_cubic_ratio={cubic_ratio:.12f}")
print(f"T2_PASS={taylor_pass}")
for label, block in domain.items():
    for zr, vals in block.items():
        print(
            f"T3_{label}_{zr}: abs_s1_max={vals['abs_s1_max']:.12f} "
            f"epsilon_min_for_Acommon={vals['abs_epsilon_min_if_epsilon_times_s1_equals_A_common']:.12f}"
        )
print(f"P08_CLASSIFICATION={classification}")
print(f"machine_readable={OUT}")

if classification == "LOG_FORM_PROVENANCE_FAILED":
    raise SystemExit(1)
