#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np

DEFAULT_N = 10_000
MASTER_SEED = 20260818
A_MIN = -1.0
A_MAX = 1.0
Z_MIN = 0.05
Z_MAX = 2.00
N_Z = 64
Z95_TWO_SIDED = 1.959963984540054
Z95_ONE_SIDED = 1.6448536269514722

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "results" / "rcms_protocol09_t0_summary.json"
DEFAULT_CSV = ROOT / "results" / "rcms_protocol09_t0_realizations.csv"


def design() -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    z = np.linspace(Z_MIN, Z_MAX, N_Z, dtype=float)
    x = np.log1p(z)
    sigma = 0.06 + 0.02 * z
    w = 1.0 / sigma**2
    fisher = float(np.sum(w * x**2))
    sigma_a = fisher ** -0.5
    return z, x, sigma, sigma_a


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def run(n: int, seed: int, out_csv: Path, out_json: Path) -> dict:
    if n <= 0:
        raise ValueError("N must be positive")
    z, x, sigma, sigma_a = design()
    w = 1.0 / sigma**2
    denom = float(np.sum(w * x**2))

    rng = np.random.default_rng(seed)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    ahat = np.empty(n, dtype=float)
    bounded = np.empty(n, dtype=float)
    zscore = np.empty(n, dtype=float)
    dchi2 = np.empty(n, dtype=float)
    cover = np.empty(n, dtype=bool)
    one_sided_fp = np.empty(n, dtype=bool)
    boundary = np.empty(n, dtype=bool)
    failed = np.empty(n, dtype=bool)

    for i in range(n):
        eps = rng.normal(loc=0.0, scale=sigma, size=N_Z)
        y = eps  # null truth A_R = 0
        a = float(np.sum(w * x * y) / denom)
        bad = not np.isfinite(a)
        if bad:
            a = float("nan")
            b = float("nan")
            zs = float("nan")
            dc = float("nan")
            cv = False
            fp = False
            bh = False
        else:
            b = float(np.clip(a, A_MIN, A_MAX))
            zs = a / sigma_a
            dc = zs * zs
            lo = a - Z95_TWO_SIDED * sigma_a
            hi = a + Z95_TWO_SIDED * sigma_a
            cv = bool(lo <= 0.0 <= hi)
            fp = bool(zs > Z95_ONE_SIDED)
            bh = bool(a < A_MIN or a > A_MAX)

        ahat[i] = a
        bounded[i] = b
        zscore[i] = zs
        dchi2[i] = dc
        cover[i] = cv
        one_sided_fp[i] = fp
        boundary[i] = bh
        failed[i] = bad

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "realization",
            "A_hat_unbounded",
            "A_hat_bounded",
            "z_score",
            "DeltaChi2_0",
            "coverage95",
            "one_sided_fp95",
            "boundary_hit",
            "failed",
        ])
        for i in range(n):
            writer.writerow([
                i,
                f"{ahat[i]:.17g}" if np.isfinite(ahat[i]) else "nan",
                f"{bounded[i]:.17g}" if np.isfinite(bounded[i]) else "nan",
                f"{zscore[i]:.17g}" if np.isfinite(zscore[i]) else "nan",
                f"{dchi2[i]:.17g}" if np.isfinite(dchi2[i]) else "nan",
                int(cover[i]),
                int(one_sided_fp[i]),
                int(boundary[i]),
                int(failed[i]),
            ])

    good = ~failed & np.isfinite(ahat)
    n_good = int(np.sum(good))
    if n_good == 0:
        raise RuntimeError("all realizations failed")

    a_good = ahat[good]
    d_good = dchi2[good]
    mean_a = float(np.mean(a_good))
    std_a = float(np.std(a_good, ddof=1))
    bias_ratio = float(abs(mean_a) / std_a) if std_a > 0 else float("inf")
    sign_fraction = float(np.mean(a_good > 0.0))
    coverage = float(np.mean(cover[good]))
    fpr = float(np.mean(one_sided_fp[good]))
    boundary_rate = float(np.mean(boundary[good]))
    failure_rate = float(np.mean(failed))

    sign_pass = 0.485 <= sign_fraction <= 0.515
    bias_pass = bias_ratio <= 0.10
    coverage_pass = 0.92 <= coverage <= 0.98
    fpr_pass = 0.03 <= fpr <= 0.07
    failure_pass = failure_rate <= 0.01
    overall_pass = bool(sign_pass and bias_pass and coverage_pass and fpr_pass and failure_pass)

    summary = {
        "protocol": "P09-T0",
        "status": "FINAL" if n == DEFAULT_N and seed == MASTER_SEED else "SMOKE",
        "preregistered_scientific_run": bool(n == DEFAULT_N and seed == MASTER_SEED),
        "null_truth_A_R": 0.0,
        "configuration": {
            "N": int(n),
            "seed": int(seed),
            "rng": "numpy.default_rng/PCG64",
            "z_grid": {"count": N_Z, "min": Z_MIN, "max": Z_MAX, "spacing": "linear"},
            "design": "x=ln(1+z)",
            "sigma_law": "0.06 + 0.02*z",
            "A_bounds": [A_MIN, A_MAX],
            "estimator": "one-parameter weighted least squares",
            "ci95_z": Z95_TWO_SIDED,
            "one_sided95_z": Z95_ONE_SIDED,
            "sigma_A_analytic": sigma_a,
        },
        "metrics": {
            "n_good": n_good,
            "mean_A_hat": mean_a,
            "median_A_hat": float(np.median(a_good)),
            "std_A_hat": std_a,
            "bias_ratio_B": bias_ratio,
            "fraction_A_hat_gt_0": sign_fraction,
            "one_sided_false_positive_rate_95": fpr,
            "two_sided_coverage_95": coverage,
            "boundary_hit_rate": boundary_rate,
            "failure_rate": failure_rate,
            "DeltaChi2_0_quantiles": {
                "q50": float(np.quantile(d_good, 0.50)),
                "q90": float(np.quantile(d_good, 0.90)),
                "q95": float(np.quantile(d_good, 0.95)),
                "q99": float(np.quantile(d_good, 0.99)),
            },
        },
        "gates": {
            "sign_symmetry": sign_pass,
            "bias": bias_pass,
            "coverage95": coverage_pass,
            "one_sided_fpr95": fpr_pass,
            "failure_rate": failure_pass,
            "overall": overall_pass,
        },
        "interpretation": (
            "CALIBRATION_PASS" if overall_pass else "CALIBRATION_FAIL"
        ),
        "csv_sha256": sha256_file(out_csv),
        "notes": [
            "P09-T0 validates only the controlled one-parameter statistical core.",
            "Passing T0 is not evidence for RCMS and does not replace release-relevant T1 covariance calibration.",
        ],
    }

    out_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=DEFAULT_N)
    parser.add_argument("--seed", type=int, default=MASTER_SEED)
    parser.add_argument("--out-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--out-csv", type=Path, default=DEFAULT_CSV)
    args = parser.parse_args()

    summary = run(args.n, args.seed, args.out_csv, args.out_json)
    m = summary["metrics"]
    g = summary["gates"]
    print("RCMS Protocol 09 T0 — Null false-positive calibration")
    print(f"RUN_STATUS={summary['status']}")
    print(f"N={summary['configuration']['N']}")
    print(f"seed={summary['configuration']['seed']}")
    print(f"sigma_A={summary['configuration']['sigma_A_analytic']:.12g}")
    print(f"mean_A_hat={m['mean_A_hat']:.12g}")
    print(f"std_A_hat={m['std_A_hat']:.12g}")
    print(f"bias_ratio_B={m['bias_ratio_B']:.12g}")
    print(f"fraction_A_hat_gt_0={m['fraction_A_hat_gt_0']:.9f}")
    print(f"one_sided_fpr95={m['one_sided_false_positive_rate_95']:.9f}")
    print(f"coverage95={m['two_sided_coverage_95']:.9f}")
    print(f"boundary_hit_rate={m['boundary_hit_rate']:.9f}")
    print(f"failure_rate={m['failure_rate']:.9f}")
    print(f"P09_T0_CLASSIFICATION={summary['interpretation']}")
    print(f"P09_T0_OVERALL_PASS={g['overall']}")
    print(f"csv_sha256={summary['csv_sha256']}")
    print(f"machine_readable={args.out_json}")


if __name__ == "__main__":
    main()
