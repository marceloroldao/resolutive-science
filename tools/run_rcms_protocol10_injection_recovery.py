#!/usr/bin/env python3
"""RCMS Protocol 10 — preregistered DESI covariance injection/recovery calibration."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MEAN = ROOT / "data/rcms/desi_dr2_bao_all_mean.txt"
COV = ROOT / "data/rcms/desi_dr2_bao_all_cov.txt"
DEFAULT_JSON = ROOT / "results/rcms_protocol10_summary.json"
DEFAULT_CSV = ROOT / "results/rcms_protocol10_realizations.csv"

AR_TRUTHS = np.asarray([-0.40, -0.20, 0.00, 0.20, 0.40], dtype=float)
AR_GRID = np.round(np.arange(-1.0, 1.0 + 0.0001, 0.01), 12)
OM_GRID = np.round(np.arange(0.05, 0.60 + 0.0001, 0.005), 12)
OMEGA_GEN = 0.295
Q_GEN = 29.468025096
DELTA95 = 3.841458820694124
FINAL_N_PER = 2000
FINAL_SEED = 20260821


def load_data():
    rows = []
    for line in MEAN.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        z, val, kind = line.split()
        rows.append((float(z), float(val), kind))
    cov = np.loadtxt(COV, dtype=float)
    if len(rows) != 13 or cov.shape != (13, 13):
        raise RuntimeError("DESI DR2 frozen dimensions are not 13 / 13x13")
    if not np.allclose(cov, cov.T, rtol=0.0, atol=1e-12):
        raise RuntimeError("DESI covariance is not symmetric")
    np.linalg.cholesky(cov)
    return rows, cov


def template_shapes(rows):
    om_mesh, ar_mesh = np.meshgrid(OM_GRID, AR_GRID, indexing="ij")
    oms = om_mesh.ravel()
    ars = ar_mesh.ravel()
    nt = len(oms)
    shapes = np.empty((nt, len(rows)), dtype=float)
    nodes, weights = np.polynomial.legendre.leggauss(64)
    unique_z = sorted({z for z, _, _ in rows})
    dm_cache = {}
    dh_cache = {}
    valid = np.ones(nt, dtype=bool)

    for z in unique_z:
        x = 0.5 * z * (nodes + 1.0)
        w = 0.5 * z * weights
        e2 = (
            oms[:, None] * (1.0 + x[None, :]) ** 3
            + (1.0 - oms[:, None])
            + ars[:, None] * np.log1p(x[None, :])
        )
        good = np.all(e2 > 0.0, axis=1)
        valid &= good
        safe = np.where(e2 > 0.0, e2, np.nan)
        dm_cache[z] = np.nansum(w[None, :] / np.sqrt(safe), axis=1)
        ez2 = oms * (1.0 + z) ** 3 + (1.0 - oms) + ars * np.log1p(z)
        good_z = ez2 > 0.0
        valid &= good_z
        dh_cache[z] = np.where(good_z, 1.0 / np.sqrt(np.where(good_z, ez2, np.nan)), np.nan)

    for j, (z, _, kind) in enumerate(rows):
        dm = dm_cache[z]
        dh = dh_cache[z]
        if kind == "DM_over_rs":
            shapes[:, j] = dm
        elif kind == "DH_over_rs":
            shapes[:, j] = dh
        elif kind == "DV_over_rs":
            shapes[:, j] = (z * dm * dm * dh) ** (1.0 / 3.0)
        else:
            raise RuntimeError(f"unknown BAO observable: {kind}")

    valid &= np.all(np.isfinite(shapes), axis=1)
    shapes[~valid, :] = 0.0
    return shapes, oms, ars, valid


def profiled_chi2_batch(data, ci, shapes, denom, valid):
    dci = data @ ci
    dcid = np.einsum("bi,bi->b", dci, data)
    cross = dci @ shapes.T
    chi = dcid[:, None] - (cross * cross) / denom[None, :]
    chi[:, ~valid] = np.inf
    return chi


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def classify_point(truth, bias_ratio, coverage, sign_recovery, boundary_rate, failure_rate):
    fail = False
    warn = False
    if bias_ratio > 0.20:
        fail = True
    elif bias_ratio > 0.10:
        warn = True
    if not (0.90 <= coverage <= 0.99):
        fail = True
    elif not (0.92 <= coverage <= 0.98):
        warn = True
    if abs(truth) == 0.20:
        if sign_recovery < 0.65:
            fail = True
        elif sign_recovery < 0.75:
            warn = True
    elif abs(truth) == 0.40:
        if sign_recovery < 0.90:
            fail = True
        elif sign_recovery < 0.95:
            warn = True
    if boundary_rate > 0.01 or failure_rate > 0.01:
        fail = True
    return "FAIL" if fail else ("WARNING" if warn else "PASS")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-per", type=int, default=FINAL_N_PER)
    parser.add_argument("--seed", type=int, default=FINAL_SEED)
    parser.add_argument("--batch", type=int, default=100)
    parser.add_argument("--out-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--out-csv", type=Path, default=DEFAULT_CSV)
    args = parser.parse_args()

    rows, cov = load_data()
    ci = np.linalg.inv(cov)
    chol = np.linalg.cholesky(cov)
    shapes, oms, ars, valid0 = template_shapes(rows)
    cis = shapes @ ci
    denom = np.einsum("ti,ti->t", cis, shapes)
    valid = valid0 & np.isfinite(denom) & (denom > 0.0)

    gen_indices = {}
    for truth in AR_TRUTHS:
        mask = np.isclose(oms, OMEGA_GEN, atol=1e-12, rtol=0.0) & np.isclose(ars, truth, atol=1e-12, rtol=0.0) & valid
        idxs = np.flatnonzero(mask)
        if len(idxs) != 1:
            raise RuntimeError(f"generator template not uniquely found for A_R={truth}")
        gen_indices[float(truth)] = int(idxs[0])

    records = []
    point_summaries = []

    for inj_idx, truth in enumerate(AR_TRUTHS):
        rng = np.random.default_rng(args.seed + inj_idx)
        mu = Q_GEN * shapes[gen_indices[float(truth)]]
        synth = mu[None, :] + rng.standard_normal((args.n_per, 13)) @ chol.T

        a_hat = np.empty(args.n_per, dtype=float)
        delta_truth = np.empty(args.n_per, dtype=float)
        fit_fail = np.zeros(args.n_per, dtype=bool)

        truth_mask = np.isclose(ars, truth, atol=1e-12, rtol=0.0) & valid
        for start in range(0, args.n_per, args.batch):
            stop = min(args.n_per, start + args.batch)
            chi = profiled_chi2_batch(synth[start:stop], ci, shapes, denom, valid)
            best_idx = np.argmin(chi, axis=1)
            best_chi = chi[np.arange(stop - start), best_idx]
            truth_chi = np.min(chi[:, truth_mask], axis=1)
            local_fail = ~np.isfinite(best_chi) | ~np.isfinite(truth_chi)
            fit_fail[start:stop] = local_fail
            a_hat[start:stop] = ars[best_idx]
            delta_truth[start:stop] = truth_chi - best_chi

        good = ~fit_fail
        ga = a_hat[good]
        gd = delta_truth[good]
        mean_a = float(np.mean(ga))
        median_a = float(np.median(ga))
        std_a = float(np.std(ga, ddof=1))
        raw_bias = mean_a - float(truth)
        bias_ratio = float(abs(raw_bias) / std_a) if std_a > 0 else float("inf")
        coverage = float(np.mean(gd <= DELTA95))
        if truth > 0:
            sign_recovery = float(np.mean(ga > 0.0))
        elif truth < 0:
            sign_recovery = float(np.mean(ga < 0.0))
        else:
            sign_recovery = float("nan")
        boundary_rate = float(np.mean(np.isclose(np.abs(ga), 1.0, atol=1e-12, rtol=0.0)))
        failure_rate = float(np.mean(fit_fail))
        point_class = classify_point(float(truth), bias_ratio, coverage, sign_recovery, boundary_rate, failure_rate)

        point_summaries.append({
            "A_true": float(truth),
            "child_seed": args.seed + inj_idx,
            "mean_A_hat": mean_a,
            "median_A_hat": median_a,
            "std_A_hat": std_a,
            "raw_bias": raw_bias,
            "bias_ratio_Binj": bias_ratio,
            "coverage95": coverage,
            "sign_recovery": None if truth == 0 else sign_recovery,
            "boundary_hit_rate": boundary_rate,
            "failure_rate": failure_rate,
            "point_classification": point_class,
        })

        for i in range(args.n_per):
            records.append((float(truth), args.seed + inj_idx, i, a_hat[i], delta_truth[i], bool(fit_fail[i])))

    truths = np.asarray([p["A_true"] for p in point_summaries], dtype=float)
    means = np.asarray([p["mean_A_hat"] for p in point_summaries], dtype=float)
    beta, alpha = np.polyfit(truths, means, 1)
    linearity_pass = abs(alpha) <= 0.03 and 0.90 <= beta <= 1.10

    point_classes = [p["point_classification"] for p in point_summaries]
    if (not linearity_pass) or "FAIL" in point_classes:
        overall = "RECOVERY_FAIL"
    elif "WARNING" in point_classes:
        overall = "RECOVERY_WARNING"
    else:
        overall = "RECOVERY_PASS"

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["A_true", "child_seed", "realization", "A_hat", "DeltaChi2_truth", "covered95", "fit_failure"])
        for truth, seed, i, ah, dt, fail in records:
            w.writerow([truth, seed, i, f"{ah:.12g}", f"{dt:.12g}", bool((not fail) and dt <= DELTA95), fail])

    final_identity = args.n_per == FINAL_N_PER and args.seed == FINAL_SEED
    result = {
        "protocol": "P10",
        "status": "FINAL" if final_identity else "SMOKE",
        "preregistered_scientific_run": bool(final_identity),
        "configuration": {
            "A_R_truths": AR_TRUTHS.tolist(),
            "N_per_truth": args.n_per,
            "master_seed": args.seed,
            "Omega_m_generator": OMEGA_GEN,
            "q_generator": Q_GEN,
            "A_R_bounds": [-1.0, 1.0],
            "A_R_step": 0.01,
            "Omega_m_bounds": [0.05, 0.60],
            "Omega_m_step": 0.005,
            "confidence_delta_chi2_95": DELTA95,
            "covariance": "data/rcms/desi_dr2_bao_all_cov.txt",
        },
        "points": point_summaries,
        "linearity": {"alpha": float(alpha), "beta": float(beta), "pass": bool(linearity_pass)},
        "classification": overall,
    }
    result["csv_sha256"] = sha256(args.out_csv)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("RCMS Protocol 10 — Injection/recovery calibration")
    print(f"RUN_STATUS={result['status']}")
    print(f"N_PER_TRUTH={args.n_per}")
    print(f"MASTER_SEED={args.seed}")
    for p in point_summaries:
        print(
            f"A_true={p['A_true']:+.2f} mean={p['mean_A_hat']:+.6f} std={p['std_A_hat']:.6f} "
            f"B={p['bias_ratio_Binj']:.6f} coverage95={p['coverage95']:.6f} "
            f"sign_recovery={p['sign_recovery']} class={p['point_classification']}"
        )
    print(f"linearity_alpha={alpha:.9f}")
    print(f"linearity_beta={beta:.9f}")
    print(f"P10_CLASSIFICATION={overall}")
    print(f"csv_sha256={result['csv_sha256']}")
    print(f"machine_readable={args.out_json}")


if __name__ == "__main__":
    main()
