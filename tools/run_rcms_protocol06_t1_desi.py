#!/usr/bin/env python3
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize

DATA = Path("data/rcms/protocol06/desi_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt")
COV = Path("data/rcms/protocol06/desi_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt")
OUT = Path("results/rcms_protocol06_t1.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

rows = []
for line in DATA.read_text().splitlines():
    s = line.strip()
    if not s or s.startswith("#"):
        continue
    z, value, obs = s.split()
    rows.append((float(z), float(value), obs))
y = np.array([r[1] for r in rows])
cov = np.loadtxt(COV)
inv = np.linalg.inv(cov)


def e2(z, om, ar):
    return om * (1.0 + z) ** 3 + (1.0 - om) + ar * np.log1p(z)


def E(z, om, ar):
    v = e2(z, om, ar)
    if v <= 0:
        raise ValueError("non-positive E^2")
    return np.sqrt(v)


def dc(z, om, ar):
    return quad(lambda x: 1.0 / E(x, om, ar), 0.0, z, epsabs=2e-9, epsrel=2e-9, limit=200)[0]


def theory(om, q, ar):
    out = []
    for z, _, obs in rows:
        d = dc(z, om, ar)
        ez = E(z, om, ar)
        if obs == "DM_over_rs":
            v = q * d
        elif obs == "DH_over_rs":
            v = q / ez
        elif obs == "DV_over_rs":
            v = q * (z * d * d / ez) ** (1.0 / 3.0)
        else:
            raise ValueError(obs)
        out.append(v)
    return np.array(out)


def chi2_3(p):
    om, q, ar = p
    if not (0.10 <= om <= 0.50 and 20.0 <= q <= 45.0 and -5.0 <= ar <= 5.0):
        return 1e80
    try:
        t = theory(om, q, ar)
    except (ValueError, FloatingPointError):
        return 1e80
    r = t - y
    return float(r @ inv @ r)


def chi2_2(p):
    return chi2_3((p[0], p[1], 0.0))

null = minimize(chi2_2, x0=[0.30, 29.5], method="Nelder-Mead", options={"maxiter":12000,"xatol":1e-10,"fatol":1e-10})
alt = minimize(chi2_3, x0=[null.x[0], null.x[1], 0.2], method="Nelder-Mead", options={"maxiter":20000,"xatol":1e-9,"fatol":1e-9})

om0, q0 = null.x
om1, q1, ar1 = alt.x
chi0 = float(null.fun)
chi1 = float(alt.fun)
dchi = float(chi0 - chi1)
daic = float(dchi - 2.0)

ars = np.linspace(-5.0, 5.0, 201)
prof = []
start = np.array([om1, q1])
for ar in ars:
    def f2(p):
        return chi2_3((p[0], p[1], ar))
    rr = minimize(f2, x0=start, method="Nelder-Mead", options={"maxiter":7000,"xatol":2e-8,"fatol":2e-8})
    prof.append(float(rr.fun))
    if rr.success and np.isfinite(rr.fun):
        start = rr.x
prof = np.array(prof)
threshold = chi1 + 1.0
mask = prof <= threshold + 1e-8
if np.any(mask):
    inside = ars[mask]
    lo, hi = float(inside.min()), float(inside.max())
else:
    lo = hi = float("nan")
zero_in_profile = bool(lo <= 0.0 <= hi) if np.isfinite(lo) else False

boundary = bool(
    min(abs(om1-0.10), abs(om1-0.50)) < 1e-4 or
    min(abs(q1-20.0), abs(q1-45.0)) < 1e-4 or
    min(abs(ar1+5.0), abs(ar1-5.0)) < 1e-4
)

if ar1 > 0 and (not zero_in_profile) and daic > 2.0:
    classification = "DESI_DR2_POSITIVE_SUPPORTED"
elif ar1 > 0:
    classification = "DESI_DR2_POSITIVE_DIRECTIONAL"
elif ar1 < 0 and (not zero_in_profile):
    classification = "DESI_DR2_SIGN_REVERSAL"
else:
    classification = "DESI_DR2_NULL_COMPATIBLE"

result = {
    "protocol": "P06-T1",
    "dataset": "DESI DR2 combined BAO all tracers",
    "model_form": "A_R*ln(1+z)",
    "null": {"chi2": float(chi0), "Omega_m": float(om0), "q": float(q0)},
    "rcms": {"chi2": float(chi1), "Omega_m": float(om1), "q": float(q1), "A_R": float(ar1)},
    "A_R_profile_delta_chi2_1": [float(lo), float(hi)],
    "zero_in_profile": bool(zero_in_profile),
    "Delta_chi2_LCDM_minus_RCMS": float(dchi),
    "Delta_AIC_LCDM_minus_RCMS": float(daic),
    "boundary": bool(boundary),
    "null_converged": bool(null.success),
    "rcms_converged": bool(alt.success),
    "classification": str(classification),
}
OUT.write_text(json.dumps(result, indent=2) + "\n")

print("RCMS Protocol 06 — P06-T1 DESI DR2 external reveal")
print("MODEL_FORM_FROZEN=A_R*ln(1+z)")
print(f"LCDM_chi2={chi0:.9f}")
print(f"LCDM_Omega_m={om0:.9f}")
print(f"LCDM_q={q0:.9f}")
print(f"RCMS_chi2={chi1:.9f}")
print(f"RCMS_Omega_m={om1:.9f}")
print(f"RCMS_q={q1:.9f}")
print(f"RCMS_A_R={ar1:.9f}")
print(f"A_R_profile_delta_chi2_1=[{lo:.9f},{hi:.9f}]")
print(f"Delta_chi2_LCDM_minus_RCMS={dchi:.9f}")
print(f"Delta_AIC_LCDM_minus_RCMS={daic:.9f}")
print(f"RCMS_boundary={boundary}")
print(f"P06_CLASSIFICATION={classification}")
print(f"machine_readable={OUT}")
print("note=Protocol 06 tests the frozen cosmological surrogate; it does not validate the full Resolutive Physics ontology.")

if not (null.success and alt.success) or boundary:
    raise SystemExit("P06 numerical convergence/boundary gate failed")
