#!/usr/bin/env python3
"""RCMS Protocol 09 T1 — DESI DR2 covariance null calibration.

This runner implements the preregistered P09-T1 estimator exactly:
- DESI DR2 13-point BAO sampling and frozen covariance;
- null truth A_R=0;
- N=5000, seed=20260820 for the final scientific run;
- A_R grid [-1,1] step 0.01;
- Omega_m grid [0.05,0.60] step 0.005;
- analytic profiling of q=c/(H0*r_d);
- Delta-chi2 confidence and false-positive gates frozen in the protocol.
"""
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
DEFAULT_JSON = ROOT / "results/rcms_protocol09_t1_summary.json"
DEFAULT_CSV = ROOT / "results/rcms_protocol09_t1_realizations.csv"

AR_GRID = np.round(np.arange(-1.0, 1.0 + 0.0001, 0.01), 12)
OM_GRID = np.round(np.arange(0.05, 0.60 + 0.0001, 0.005), 12)
DELTA95 = 3.841458820694124
DELTA_ONE_SIDED95 = 2.705543454095404


def load_data() -> tuple[list[tuple[float, float, str]], np.ndarray]:
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


def template_shapes(rows: list[tuple[float, float, str]]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Precompute all (Omega_m,A_R) BAO shape templates using 64-point GL quadrature."""
    om_mesh, ar_mesh = np.meshgrid(OM_GRID, AR_GRID, indexing="ij")
    oms = om_mesh.ravel()
    ars = ar_mesh.ravel()
    nt = len(oms)
    shapes = np.empty((nt, len(rows)), dtype=float)

    nodes, weights = np.polynomial.legendre.leggauss(64)
    unique_z = sorted({z for z, _, _ in rows})
    dm_cache: dict[float, np.ndarray] = {}
    dh_cache: dict[float, np.ndarray] = {}
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
    return shapes, oms, ars


def profiled_chi2_batch(
    data: np.ndarray,
    ci: np.ndarray,
    shapes: np.ndarray,
    denom: np.ndarray,
    valid: np.ndarray,
) -> np.ndarray:
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260820)
    parser.add_argument("--batch", type=int, default=100)
    parser.add_argument("--out-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--out-csv", type=Path, default=DEFAULT_CSV)
    args = parser.parse_args()

    rows, cov = load_data()
    ci = np.linalg.inv(cov)
    chol = np.linalg.cholesky(cov)
    shapes, oms, ars = template_shapes(rows)
    cis = shapes @ ci
    denom = np.einsum("ti,ti->t", cis, shapes)
    valid = np.isfinite(denom) & (denom > 0.0) & np.all(np.isfinite(shapes), axis=1)

    observed = np.asarray([v for _, v, _ in rows], dtype=float)[None, :]
    zero_mask = np.isclose(ars, 0.0, rtol=0.0, atol=1e-12) & valid
    chi_obs = profiled_chi2_batch(observed, ci, shapes, denom, valid)[0]
    zero_indices = np.flatnonzero(zero_mask)
    iz = zero_indices[int(np.argmin(chi_obs[zero_indices]))]
    om0 = float(oms[iz])
    shape0 = shapes[iz]
    q0 = float((shape0 @ ci @ observed[0]) / (shape0 @ ci @ shape0))
    mu0 = q0 * shape0

    rng = np.random.default_rng(args.seed)
    noise = rng.standard_normal((args.n, 13)) @ chol.T
    synth = mu0[None, :] + noise

    a_hat = np.empty(args.n, dtype=float)
    delta0 = np.empty(args.n, dtype=float)
    fit_fail = np.zeros(args.n, dtype=bool)

    for start in range(0, args.n, args.batch):
        stop = min(args.n, start + args.batch)
        chi = profiled_chi2_batch(synth[start:stop], ci, shapes, denom, valid)
        best_idx = np.argmin(chi, axis=1)
        best_chi = chi[np.arange(stop - start), best_idx]
        zero_chi = np.min(chi[:, zero_mask], axis=1)
        local_fail = ~np.isfinite(best_chi) | ~np.isfinite(zero_chi)
        fit_fail[start:stop] = local_fail
        a_hat[start:stop] = ars[best_idx]
        delta0[start:stop] = zero_chi - best_chi

    good = ~fit_fail
    good_a = a_hat[good]
    good_delta = delta0[good]
    mean_a = float(np.mean(good_a)) if len(good_a) else float("nan")
    median_a = float(np.median(good_a)) if len(good_a) else float("nan")
    std_a = float(np.std(good_a, ddof=1)) if len(good_a) > 1 else float("nan")
    B = float(abs(mean_a) / std_a) if std_a > 0 else float("inf")
    sign_fraction = float(np.mean(good_a > 0.0)) if len(good_a) else float("nan")
    one_sided = (good_a > 0.0) & (good_delta >= DELTA_ONE_SIDED95)
    fpr95 = float(np.mean(one_sided)) if len(good_a) else float("nan")
    coverage95 = float(np.mean(good_delta <= DELTA95)) if len(good_a) else float("nan")
    boundary = np.isclose(np.abs(good_a), 1.0, rtol=0.0, atol=1e-12)
    boundary_rate = float(np.mean(boundary)) if len(good_a) else float("nan")
    failure_rate = float(np.mean(fit_fail))

    fail = (
        B > 0.10
        or not (0.92 <= coverage95 <= 0.98)
        or boundary_rate > 0.01
        or failure_rate > 0.01
    )
    warning = (
        not fail
        and (
            not (0.47 <= sign_fraction <= 0.53)
            or not (0.035 <= fpr95 <= 0.065)
        )
    )
    classification = "CALIBRATION_FAIL" if fail else ("CALIBRATION_WARNING" if warning else "CALIBRATION_PASS")

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["realization", "A_hat", "DeltaChi2_A0", "covered95", "one_sided_fp95", "boundary_hit", "fit_failure"])
        for i in range(args.n):
            w.writerow([
                i,
                f"{a_hat[i]:.12g}",
                f"{delta0[i]:.12g}",
                bool((not fit_fail[i]) and delta0[i] <= DELTA95),
                bool((not fit_fail[i]) and a_hat[i] > 0.0 and delta0[i] >= DELTA_ONE_SIDED95),
                bool((not fit_fail[i]) and abs(a_hat[i]) == 1.0),
                bool(fit_fail[i]),
            ])

    quantiles = {str(q): float(np.quantile(good_delta, q)) for q in (0.5, 0.9, 0.95, 0.99)} if len(good_delta) else {}
    final_identity = args.n == 5000 and args.seed == 20260820
    result = {
        "protocol": "P09-T1",
        "status": "FINAL" if final_identity else "SMOKE",
        "preregistered_scientific_run": bool(final_identity),
        "null_truth_A_R": 0.0,
        "configuration": {
            "N": args.n,
            "seed": args.seed,
            "A_R_bounds": [-1.0, 1.0],
            "A_R_step": 0.01,
            "Omega_m_bounds": [0.05, 0.60],
            "Omega_m_step": 0.005,
            "covariance": "data/rcms/desi_dr2_bao_all_cov.txt",
            "sampling": "data/rcms/desi_dr2_bao_all_mean.txt",
            "confidence_delta_chi2_95": DELTA95,
            "one_sided_delta_chi2_95": DELTA_ONE_SIDED95,
        },
        "null_reference": {"Omega_m": om0, "q": q0},
        "metrics": {
            "mean_A_hat": mean_a,
            "median_A_hat": median_a,
            "std_A_hat": std_a,
            "bias_ratio_B": B,
            "fraction_A_hat_gt_0": sign_fraction,
            "one_sided_fpr95": fpr95,
            "coverage95": coverage95,
            "boundary_hit_rate": boundary_rate,
            "failure_rate": failure_rate,
            "DeltaChi2_A0_quantiles": quantiles,
        },
        "classification": classification,
    }
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    result["csv_sha256"] = sha256(args.out_csv)
    args.out_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("RCMS Protocol 09 T1 — DESI covariance null calibration")
    print(f"RUN_STATUS={result['status']}")
    print(f"N={args.n}")
    print(f"seed={args.seed}")
    print(f"null_Omega_m={om0:.6f}")
    print(f"null_q={q0:.9f}")
    print(f"mean_A_hat={mean_a:.12g}")
    print(f"std_A_hat={std_a:.12g}")
    print(f"bias_ratio_B={B:.12g}")
    print(f"fraction_A_hat_gt_0={sign_fraction:.9f}")
    print(f"one_sided_fpr95={fpr95:.9f}")
    print(f"coverage95={coverage95:.9f}")
    print(f"boundary_hit_rate={boundary_rate:.9f}")
    print(f"failure_rate={failure_rate:.9f}")
    print(f"P09_T1_CLASSIFICATION={classification}")
    print(f"csv_sha256={result['csv_sha256']}")
    print(f"machine_readable={args.out_json}")


if __name__ == "__main__":
    main()
