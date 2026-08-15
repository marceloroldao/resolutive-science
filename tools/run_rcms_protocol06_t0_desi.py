#!/usr/bin/env python3
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize, minimize_scalar

DATA = Path("data/rcms/protocol06/desi_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt")
COV = Path("data/rcms/protocol06/desi_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt")

rows = []
for line in DATA.read_text().splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    z, value, obs = line.split()
    rows.append((float(z), float(value), obs))

if len(rows) != 13:
    raise SystemExit(f"expected 13 measurements, got {len(rows)}")

cov = np.loadtxt(COV)
if cov.shape != (13, 13) or not np.all(np.isfinite(cov)):
    raise SystemExit("invalid covariance shape/content")
eigs = np.linalg.eigvalsh(cov)
if np.min(eigs) <= 0:
    raise SystemExit(f"covariance not positive definite: min_eig={np.min(eigs)}")
inv = np.linalg.inv(cov)
y = np.array([r[1] for r in rows])


def E(z, om):
    return np.sqrt(om * (1.0 + z) ** 3 + (1.0 - om))


def dc(z, om):
    return quad(lambda x: 1.0 / E(x, om), 0.0, z, epsabs=1e-10, epsrel=1e-10, limit=200)[0]


def theory(om, q):
    out = []
    for z, _, obs in rows:
        d = dc(z, om)
        if obs == "DM_over_rs":
            v = q * d
        elif obs == "DH_over_rs":
            v = q / E(z, om)
        elif obs == "DV_over_rs":
            v = q * (z * d * d / E(z, om)) ** (1.0 / 3.0)
        else:
            raise SystemExit(f"unsupported observable {obs}")
        out.append(v)
    return np.array(out)


def chi2(params):
    om, q = params
    if not (0.10 <= om <= 0.50 and 20.0 <= q <= 45.0):
        return 1e100
    r = theory(om, q) - y
    return float(r @ inv @ r)

res = minimize(chi2, x0=[0.30, 30.0], method="Nelder-Mead", options={"xatol":1e-10,"fatol":1e-10,"maxiter":10000})
om_best, q_best = res.x
cmin = res.fun
boundary = (abs(om_best-0.10)<1e-4 or abs(om_best-0.50)<1e-4 or abs(q_best-20.0)<1e-4 or abs(q_best-45.0)<1e-4)

oms = np.linspace(0.10, 0.50, 41)
profile = []
for om in oms:
    qr = minimize_scalar(lambda q: chi2((om, q)), bounds=(20.0, 45.0), method="bounded", options={"xatol":1e-10})
    profile.append(qr.fun)
profile = np.array(profile)
span = float(np.max(profile) - np.min(profile))
identifiable = span >= 4.0

print("RCMS Protocol 06 — P06-T0 DESI DR2 baseline gate")
print("RCMS_PARAMETER_EVALUATED=NO")
print(f"N_MEASUREMENTS={len(rows)}")
print(f"Z_RANGE=[{min(r[0] for r in rows):.3f},{max(r[0] for r in rows):.3f}]")
print(f"COV_MIN_EIG={np.min(eigs):.12g}")
print(f"LCDM_Omega_m={om_best:.9f}")
print(f"LCDM_q_c_over_H0rd={q_best:.9f}")
print(f"LCDM_chi2={cmin:.9f}")
print(f"LCDM_boundary={boundary}")
print(f"PROFILE_OMEGA_M_SPAN_DELTA_CHI2={span:.9f}")
print(f"P06_T0_SHAPE_IDENTIFIABILITY={'PASS' if identifiable else 'FAIL'}")

if (not res.success) or boundary or (not identifiable):
    raise SystemExit("P06_T0_STATUS=STOP_BEFORE_RCMS_REVEAL")
print("P06_T0_STATUS=READY_FOR_PREREGISTERED_RCMS_REVEAL")
