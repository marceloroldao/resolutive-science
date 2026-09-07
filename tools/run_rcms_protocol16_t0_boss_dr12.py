#!/usr/bin/env python3
"""RCMS P16-T0 — BOSS DR12 held-out intake and LCDM identifiability gate.

This runner MUST NOT evaluate the RCMS amplitude A_R.
"""
from __future__ import annotations

import hashlib
import json
import math
import urllib.request
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/rcms_protocol16_t0_boss_dr12.json"
UPSTREAM = "bb0c1c9009dc76d1391300e169e8df38fd1096db"
BASE = f"https://raw.githubusercontent.com/CobayaSampler/bao_data/{UPSTREAM}"
FILES = {
    "sdss_DR12Consensus_bao.dat": "fc43f1cd9c815bb58b09f4d8d1d272d2c4ec57e05e4893e2121c20dc08f4f862",
    "BAO_consensus_covtot_dM_Hz.txt": "05c04829c8edc117870efe809494593a23de6c35547f8b66760a5250804b65cf",
}
RD_FID = 147.78
C_KMS = 299792.458
OMEGA_BOUNDS = (0.05, 0.60)
Q_BOUNDS = (10.0, 60.0)


def download(name: str) -> bytes:
    with urllib.request.urlopen(f"{BASE}/{name}", timeout=30) as r:
        b = r.read()
    got = hashlib.sha256(b).hexdigest()
    if got != FILES[name]:
        raise RuntimeError(f"hash mismatch for {name}: {got}")
    return b


def parse_data(b: bytes):
    rows = []
    for line in b.decode().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        z, value, kind = line.split()
        rows.append((float(z), float(value), kind))
    if len(rows) != 6:
        raise RuntimeError("expected six BOSS DR12 consensus measurements")
    zs = sorted(set(r[0] for r in rows))
    if zs != [0.38, 0.51, 0.61]:
        raise RuntimeError(f"unexpected redshifts: {zs}")
    kinds = [r[2] for r in rows]
    if kinds != ["DM_over_rs", "bao_Hz_rs"] * 3:
        raise RuntimeError(f"unexpected observable ordering: {kinds}")
    return rows


def simpson_inv_e(z: float, om: float, n: int = 600) -> float:
    if n % 2:
        n += 1
    h = z / n
    def inv_e(x):
        return 1.0 / math.sqrt(om * (1.0 + x) ** 3 + 1.0 - om)
    s = inv_e(0.0) + inv_e(z)
    for i in range(1, n):
        s += (4.0 if i % 2 else 2.0) * inv_e(i * h)
    return s * h / 3.0


def model(rows, om: float, q: float):
    integ = {}
    vals = []
    for z, _, kind in rows:
        if z not in integ:
            integ[z] = simpson_inv_e(z, om)
        e = math.sqrt(om * (1.0 + z) ** 3 + 1.0 - om)
        if kind == "DM_over_rs":
            vals.append(q * RD_FID * integ[z])
        elif kind == "bao_Hz_rs":
            vals.append(C_KMS * e / (q * RD_FID))
        else:
            raise RuntimeError(kind)
    return np.asarray(vals)


def chi2(rows, data, ci, om: float, q: float) -> float:
    r = data - model(rows, om, q)
    return float(r @ ci @ r)


def golden(fn, lo, hi, tol=1e-10):
    g = (math.sqrt(5.0) - 1.0) / 2.0
    c, d = hi - g * (hi - lo), lo + g * (hi - lo)
    fc, fd = fn(c), fn(d)
    while hi - lo > tol:
        if fc < fd:
            hi, d, fd = d, c, fc
            c = hi - g * (hi - lo); fc = fn(c)
        else:
            lo, c, fc = c, d, fd
            d = lo + g * (hi - lo); fd = fn(d)
    x = (lo + hi) / 2.0
    return x, fn(x)


def profile_q(rows, data, ci, om):
    # Optimize log(q), keeping the scale nuisance strictly positive.
    lq, val = golden(lambda x: chi2(rows, data, ci, om, math.exp(x)), math.log(Q_BOUNDS[0]), math.log(Q_BOUNDS[1]))
    return math.exp(lq), val


def main():
    raw_data = download("sdss_DR12Consensus_bao.dat")
    raw_cov = download("BAO_consensus_covtot_dM_Hz.txt")
    rows = parse_data(raw_data)
    cov = np.loadtxt(raw_cov.decode().splitlines())
    if cov.shape != (6, 6):
        raise RuntimeError(f"unexpected covariance shape {cov.shape}")
    symmetry = float(np.max(np.abs(cov - cov.T)))
    eig = np.linalg.eigvalsh(cov)
    if symmetry > 1e-10 or float(eig.min()) <= 0.0:
        raise RuntimeError("covariance symmetry/positive-definiteness gate failed")
    ci = np.linalg.inv(cov)
    data = np.asarray([r[1] for r in rows])

    om_best, chi_best = golden(lambda om: profile_q(rows, data, ci, om)[1], *OMEGA_BOUNDS)
    q_best, chi_best = profile_q(rows, data, ci, om_best)

    grid = np.linspace(OMEGA_BOUNDS[0], OMEGA_BOUNDS[1], 57)
    prof = [profile_q(rows, data, ci, float(om))[1] for om in grid]
    shape_span = float(max(prof) - min(prof))
    interior = (om_best > OMEGA_BOUNDS[0] + 1e-4 and om_best < OMEGA_BOUNDS[1] - 1e-4 and q_best > Q_BOUNDS[0] + 1e-4 and q_best < Q_BOUNDS[1] - 1e-4)
    identifiable = shape_span > 1.0 and interior

    payload = {
        "protocol": "P16-T0",
        "status": "FINAL",
        "target": "SDSS-III BOSS DR12 BAO-only consensus",
        "upstream_revision": UPSTREAM,
        "file_sha256": FILES,
        "rd_fid_Mpc": RD_FID,
        "covariance_max_asymmetry": symmetry,
        "covariance_min_eigenvalue": float(eig.min()),
        "LCDM": {"Omega_m": om_best, "q": q_best, "chi2": chi_best},
        "profiled_Omega_m_chi2_span": shape_span,
        "shape_identifiable": identifiable,
        "interior_optimum": interior,
        "RCMS_PARAMETER_EVALUATED": False,
        "classification": "READY_FOR_BLIND_RCMS_REVEAL" if identifiable else "T0_GATE_FAILED",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("RCMS P16-T0 — BOSS DR12 held-out intake")
    print(f"LCDM Omega_m={om_best:.9f} q={q_best:.9f} chi2={chi_best:.9f}")
    print(f"COV_MIN_EIG={eig.min():.9f} COV_MAX_ASYM={symmetry:.3e}")
    print(f"PROFILED_OMEGA_M_CHI2_SPAN={shape_span:.9f}")
    print(f"P16_T0_SHAPE_IDENTIFIABILITY={'PASS' if identifiable else 'FAIL'}")
    print("RCMS_PARAMETER_EVALUATED=NO")
    print(f"P16_T0_STATUS={payload['classification']}")
    if not identifiable:
        raise SystemExit(2)

if __name__ == "__main__":
    main()
