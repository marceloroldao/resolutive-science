#!/usr/bin/env python3
"""RCMS Protocol 17 — residual topology and sign map.

Diagnostic only. No new cosmological parameter or functional form is introduced.
"""
from __future__ import annotations

import hashlib
import json
import math
import urllib.request
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/rcms_protocol17_residual_topology.json"

# DESI DR2 frozen local inputs used in P13.
DESI_MEAN = ROOT / "data/rcms/desi_dr2_bao_all_mean.txt"
DESI_COV = ROOT / "data/rcms/desi_dr2_bao_all_cov.txt"

# BOSS DR12 frozen upstream inputs used in P16.
BOSS_REV = "bb0c1c9009dc76d1391300e169e8df38fd1096db"
BOSS_BASE = f"https://raw.githubusercontent.com/CobayaSampler/bao_data/{BOSS_REV}"
BOSS_FILES = {
    "sdss_DR12Consensus_bao.dat": "fc43f1cd9c815bb58b09f4d8d1d272d2c4ec57e05e4893e2121c20dc08f4f862",
    "BAO_consensus_covtot_dM_Hz.txt": "05c04829c8edc117870efe809494593a23de6c35547f8b66760a5250804b65cf",
}
RD_FID = 147.78
C_KMS = 299792.458

OMEGA_BOUNDS = (0.05, 0.60)
DESI_A_BOUNDS = (-1.0, 1.0)
DESI_A_STEP = 0.01
BOSS_A_BOUNDS = (-1.0, 1.0)
BOSS_A_STEP = 0.005
Q_BOUNDS = (10.0, 60.0)

P13_EXPECTED = {"chi_lcdm": 10.271042637, "chi_rcms": 8.965255791, "A_R": 0.21}
P16_EXPECTED = {
    "chi_lcdm": 2.061158601,
    "chi_rcms": 1.019163004,
    "A_R": -1.0,
    "Omega_m_lcdm": 0.364867611,
    "q_lcdm": 30.509014587,
}


def simpson_inv_e(z, om, a, n=400):
    if n % 2:
        n += 1
    h = z / n
    def inv_e(x):
        e2 = om * (1 + x) ** 3 + 1 - om + a * math.log1p(x)
        if e2 <= 0 or not math.isfinite(e2):
            raise ValueError
        return 1.0 / math.sqrt(e2)
    s = inv_e(0.0) + inv_e(z)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * inv_e(i * h)
    return s * h / 3.0


def golden(fn, lo, hi, tol=1e-8):
    g = (math.sqrt(5.0) - 1.0) / 2.0
    c, d = hi - g * (hi - lo), lo + g * (hi - lo)
    fc, fd = fn(c), fn(d)
    while hi - lo > tol:
        if fc < fd:
            hi, d, fd = d, c, fc
            c = hi - g * (hi - lo)
            fc = fn(c)
        else:
            lo, c, fc = c, d, fd
            d = lo + g * (hi - lo)
            fd = fn(d)
    x = (lo + hi) / 2.0
    return x, fn(x)


def load_desi():
    rows = []
    for line in DESI_MEAN.read_text().splitlines():
        if line.strip() and not line.lstrip().startswith("#"):
            z, v, kind = line.split()
            rows.append((float(z), float(v), kind))
    cov = np.loadtxt(DESI_COV, dtype=float)
    if len(rows) != 13 or cov.shape != (13, 13):
        raise RuntimeError("DESI dimensions failed")
    np.linalg.cholesky(cov)
    return rows, cov


def desi_shape(rows, om, a):
    cache = {}
    out = []
    for z, _, kind in rows:
        e2 = om * (1 + z) ** 3 + 1 - om + a * math.log1p(z)
        if e2 <= 0:
            raise ValueError
        e = math.sqrt(e2)
        if z not in cache:
            cache[z] = simpson_inv_e(z, om, a, n=200)
        dm = cache[z]
        dh = 1.0 / e
        if kind == "DM_over_rs":
            out.append(dm)
        elif kind == "DH_over_rs":
            out.append(dh)
        elif kind == "DV_over_rs":
            out.append((z * dm * dm * dh) ** (1.0 / 3.0))
        else:
            raise RuntimeError(kind)
    return np.asarray(out)


def desi_objective(rows, ci, om, a):
    try:
        s = desi_shape(rows, om, a)
    except ValueError:
        return float("inf"), float("nan"), None
    data = np.asarray([r[1] for r in rows])
    q = float((s @ ci @ data) / (s @ ci @ s))
    pred = q * s
    r = data - pred
    return float(r @ ci @ r), q, pred


def desi_profile(rows, ci, a):
    om, _ = golden(lambda x: desi_objective(rows, ci, x, a)[0], *OMEGA_BOUNDS)
    chi, q, pred = desi_objective(rows, ci, om, a)
    return chi, om, q, pred


def fit_desi(rows, cov):
    ci = np.linalg.inv(cov)
    chi0, om0, q0, pred0 = desi_profile(rows, ci, 0.0)
    best = (float("inf"), None, None, None, None)
    n = int(round((DESI_A_BOUNDS[1] - DESI_A_BOUNDS[0]) / DESI_A_STEP)) + 1
    for i in range(n):
        a = DESI_A_BOUNDS[0] + i * DESI_A_STEP
        chi, om, q, pred = desi_profile(rows, ci, a)
        if chi < best[0]:
            best = (chi, a, om, q, pred)
    chi1, a1, om1, q1, pred1 = best
    if abs(chi0 - P13_EXPECTED["chi_lcdm"]) > 2e-5 or abs(chi1 - P13_EXPECTED["chi_rcms"]) > 2e-5 or abs(a1 - P13_EXPECTED["A_R"]) > 1e-12:
        raise RuntimeError(f"P13 closure failed: {(chi0, chi1, a1)}")
    return {
        "LCDM": {"chi2": chi0, "Omega_m": om0, "q": q0, "pred": pred0},
        "RCMS": {"chi2": chi1, "Omega_m": om1, "q": q1, "A_R": a1, "pred": pred1},
    }


def boss_download(name):
    with urllib.request.urlopen(f"{BOSS_BASE}/{name}", timeout=30) as r:
        b = r.read()
    if hashlib.sha256(b).hexdigest() != BOSS_FILES[name]:
        raise RuntimeError(f"BOSS hash mismatch: {name}")
    return b


def load_boss():
    rows = []
    for line in boss_download("sdss_DR12Consensus_bao.dat").decode().splitlines():
        if line.strip() and not line.lstrip().startswith("#"):
            z, v, kind = line.split()
            rows.append((float(z), float(v), kind))
    cov = np.loadtxt(boss_download("BAO_consensus_covtot_dM_Hz.txt").decode().splitlines())
    if len(rows) != 6 or cov.shape != (6, 6):
        raise RuntimeError("BOSS dimensions failed")
    np.linalg.cholesky(cov)
    return rows, cov


def boss_components(rows, om, a):
    ints, dm, hz = {}, [], []
    for z, _, kind in rows:
        e2 = om * (1 + z) ** 3 + 1 - om + a * math.log1p(z)
        if e2 <= 0:
            raise ValueError
        e = math.sqrt(e2)
        if z not in ints:
            ints[z] = simpson_inv_e(z, om, a, n=600)
        if kind == "DM_over_rs":
            dm.append(RD_FID * ints[z]); hz.append(0.0)
        elif kind == "bao_Hz_rs":
            dm.append(0.0); hz.append(C_KMS * e / RD_FID)
        else:
            raise RuntimeError(kind)
    return np.asarray(dm), np.asarray(hz)


def boss_profile_q(data, ci, dm, hz):
    def f(logq):
        q = math.exp(logq)
        r = data - (q * dm + hz / q)
        return float(r @ ci @ r)
    lq, val = golden(f, math.log(Q_BOUNDS[0]), math.log(Q_BOUNDS[1]), tol=1e-9)
    q = math.exp(lq)
    return q, val, q * dm + hz / q


def boss_profile(rows, data, ci, a):
    def f(om):
        try:
            dm, hz = boss_components(rows, om, a)
        except ValueError:
            return float("inf")
        return boss_profile_q(data, ci, dm, hz)[1]
    om, _ = golden(f, *OMEGA_BOUNDS)
    dm, hz = boss_components(rows, om, a)
    q, chi, pred = boss_profile_q(data, ci, dm, hz)
    return chi, om, q, pred


def fit_boss(rows, cov):
    data = np.asarray([r[1] for r in rows])
    ci = np.linalg.inv(cov)
    chi0, om0, q0, pred0 = boss_profile(rows, data, ci, 0.0)
    best = (float("inf"), None, None, None, None)
    n = int(round((BOSS_A_BOUNDS[1] - BOSS_A_BOUNDS[0]) / BOSS_A_STEP)) + 1
    for i in range(n):
        a = BOSS_A_BOUNDS[0] + i * BOSS_A_STEP
        chi, om, q, pred = boss_profile(rows, data, ci, a)
        if chi < best[0]:
            best = (chi, a, om, q, pred)
    chi1, a1, om1, q1, pred1 = best
    if abs(chi0 - P16_EXPECTED["chi_lcdm"]) > 2e-6 or abs(om0 - P16_EXPECTED["Omega_m_lcdm"]) > 2e-6 or abs(q0 - P16_EXPECTED["q_lcdm"]) > 2e-6:
        raise RuntimeError(f"P16 T0 closure failed: {(chi0, om0, q0)}")
    if abs(chi1 - P16_EXPECTED["chi_rcms"]) > 2e-6 or abs(a1 - P16_EXPECTED["A_R"]) > 1e-12:
        raise RuntimeError(f"P16 T1 closure failed: {(chi1, a1)}")
    return {
        "LCDM": {"chi2": chi0, "Omega_m": om0, "q": q0, "pred": pred0},
        "RCMS": {"chi2": chi1, "Omega_m": om1, "q": q1, "A_R": a1, "pred": pred1},
    }


def channel(kind):
    return "radial" if kind in ("DH_over_rs", "bao_Hz_rs") else "transverse_volume"


def canonical_sign(kind, standardized):
    return -standardized if kind == "bao_Hz_rs" else standardized


def residual_map(survey, rows, cov, fits):
    data = np.asarray([r[1] for r in rows])
    sig = np.sqrt(np.diag(cov))
    L = np.linalg.cholesky(cov)
    unique_z = sorted(set(r[0] for r in rows))
    median_z = float(np.median(unique_z))
    out_models = {}

    for model_name in ("LCDM", "RCMS"):
        fit = fits[model_name]
        pred = np.asarray(fit["pred"])
        resid = data - pred
        standardized = resid / sig
        whitened = np.linalg.solve(L, resid)
        if abs(float(whitened @ whitened) - float(fit["chi2"])) > 5e-7:
            raise RuntimeError(f"{survey} {model_name} whitened chi2 reconstruction failed")

        rows_out = []
        for i, ((z, obs, kind), p, r, s, w) in enumerate(zip(rows, pred, resid, standardized, whitened)):
            rows_out.append({
                "index": i,
                "survey": survey,
                "z": z,
                "kind": kind,
                "channel": channel(kind),
                "data": obs,
                "prediction": float(p),
                "residual": float(r),
                "marginal_sigma": float(sig[i]),
                "standardized_residual": float(s),
                "canonical_standardized_residual": float(canonical_sign(kind, s)),
                "whitened_residual": float(w),
            })

        radial = [x["canonical_standardized_residual"] for x in rows_out if x["channel"] == "radial"]
        trans = [x["canonical_standardized_residual"] for x in rows_out if x["channel"] == "transverse_volume"]
        low = [x["canonical_standardized_residual"] for x in rows_out if x["z"] <= median_z]
        high = [x["canonical_standardized_residual"] for x in rows_out if x["z"] > median_z]
        radial_mean = float(np.mean(radial)) if radial else None
        trans_mean = float(np.mean(trans)) if trans else None
        low_mean = float(np.mean(low)) if low else None
        high_mean = float(np.mean(high)) if high else None

        out_models[model_name] = {
            "fit": {k: v for k, v in fit.items() if k != "pred"},
            "median_unique_redshift": median_z,
            "radial_canonical_mean": radial_mean,
            "transverse_volume_canonical_mean": trans_mean,
            "radial_minus_transverse_gap": None if radial_mean is None or trans_mean is None else radial_mean - trans_mean,
            "low_z_canonical_mean": low_mean,
            "high_z_canonical_mean": high_mean,
            "low_minus_high_gap": None if low_mean is None or high_mean is None else low_mean - high_mean,
            "max_abs_standardized_residual": float(np.max(np.abs(standardized))),
            "max_abs_whitened_residual": float(np.max(np.abs(whitened))),
            "rows": rows_out,
        }

    for i in range(len(rows)):
        a0 = abs(out_models["LCDM"]["rows"][i]["standardized_residual"])
        a1 = abs(out_models["RCMS"]["rows"][i]["standardized_residual"])
        out_models["RCMS"]["rows"][i]["delta_abs_standardized_vs_LCDM"] = a1 - a0

    return out_models


def classify(surveys):
    for payload in surveys.values():
        m = payload["RCMS"]
        r, t = m["radial_canonical_mean"], m["transverse_volume_canonical_mean"]
        gap = m["radial_minus_transverse_gap"]
        if r is not None and t is not None and gap is not None and abs(gap) >= 0.50 and r * t < 0:
            return "CHANNEL_ORGANIZED_TENSION"
    for payload in surveys.values():
        m = payload["RCMS"]
        lo, hi = m["low_z_canonical_mean"], m["high_z_canonical_mean"]
        gap = m["low_minus_high_gap"]
        if lo is not None and hi is not None and gap is not None and abs(gap) >= 0.50 and lo * hi < 0:
            return "REDSHIFT_ORGANIZED_TENSION"
    return "DIFFUSE_RESIDUAL_STRUCTURE"


def main():
    desi_rows, desi_cov = load_desi()
    boss_rows, boss_cov = load_boss()

    desi_fits = fit_desi(desi_rows, desi_cov)
    boss_fits = fit_boss(boss_rows, boss_cov)

    surveys = {
        "DESI_DR2": residual_map("DESI_DR2", desi_rows, desi_cov, desi_fits),
        "BOSS_DR12": residual_map("BOSS_DR12", boss_rows, boss_cov, boss_fits),
    }
    classification = classify(surveys)

    payload = {
        "protocol": "P17-A",
        "status": "FINAL",
        "scope": "BAO residual topology only; no new model",
        "frozen_surrogate": "E2=Omega_m*(1+z)^3+(1-Omega_m)+A_R*ln(1+z)",
        "boss_upstream_revision": BOSS_REV,
        "surveys": surveys,
        "classification": classification,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("RCMS P17-A — Residual topology and sign map")
    for survey, p in surveys.items():
        for model in ("LCDM", "RCMS"):
            m = p[model]
            print(
                f"{survey} {model}: chi2={m['fit']['chi2']:.9f} "
                f"radial_mean={m['radial_canonical_mean']:.6f} "
                f"transverse_mean={m['transverse_volume_canonical_mean']:.6f} "
                f"channel_gap={m['radial_minus_transverse_gap']:.6f} "
                f"low_mean={m['low_z_canonical_mean']:.6f} high_mean={m['high_z_canonical_mean']:.6f} "
                f"z_gap={m['low_minus_high_gap']:.6f}"
            )
    print(f"P17_CLASSIFICATION={classification}")
    print(f"machine_readable={OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
