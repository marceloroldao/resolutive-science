#!/usr/bin/env python3
"""RCMS Protocol 20 — exact-redshift cross-survey concordance diagnostic."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import run_rcms_protocol17_residual_topology as p17
import run_rcms_protocol19_redshift_locality as p19

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/rcms_protocol20_cross_survey_concordance.json"
TARGET_Z = 0.51
WINDOW = (0.38, 0.61)


def exact_indices(rows, z):
    idx = [i for i, r in enumerate(rows) if abs(float(r[0]) - z) < 1e-12]
    if len(idx) != 2:
        raise RuntimeError(f"expected exactly two observables at z={z}, found {len(idx)}")
    return idx


def window_indices(rows, lo, hi):
    idx = [i for i, r in enumerate(rows) if lo - 1e-12 <= float(r[0]) <= hi + 1e-12]
    if len(idx) < 2:
        raise RuntimeError("window has too few observables")
    return idx


def profile_payload(rows, cov, full_fit, pred_builder, idx):
    data = np.asarray([r[1] for r in rows], dtype=float)
    avals, pred_grid = pred_builder(rows, float(full_fit["Omega_m"]), float(full_fit["q"]))
    prof = p19.observed_local_profile(data, cov, pred_grid, avals, idx)
    prof["nobs"] = len(idx)
    prof["zero_in_profile"] = bool(prof["profile_delta_chi2_1"][0] <= 0.0 <= prof["profile_delta_chi2_1"][1])
    prof["indices"] = list(idx)
    prof["kinds"] = [rows[i][2] for i in idx]
    prof["redshifts"] = [float(rows[i][0]) for i in idx]
    return prof


def cross_summary(a, b):
    alo, ahi = a["profile_delta_chi2_1"]
    blo, bhi = b["profile_delta_chi2_1"]
    overlap = max(alo, blo) <= min(ahi, bhi)
    gap = 0.0 if overlap else max(blo - ahi, alo - bhi)
    opposite = bool(a["A_R"] * b["A_R"] < 0.0)
    return {
        "opposite_best_fit_signs": opposite,
        "sign_agreement": not opposite,
        "profile_interval_overlap": bool(overlap),
        "profile_interval_gap": float(gap),
        "best_amplitude_separation": float(abs(a["A_R"] - b["A_R"])),
        "boundary_limited": bool(a["boundary_contact"] or b["boundary_contact"]),
    }


def classify(summary):
    if summary["opposite_best_fit_signs"] and not summary["profile_interval_overlap"]:
        return "EXACT_Z_SURVEY_DISCORDANCE"
    if summary["opposite_best_fit_signs"] and summary["profile_interval_overlap"]:
        return "EXACT_Z_SURVEY_DIRECTIONAL_TENSION"
    if (not summary["opposite_best_fit_signs"]) and (not summary["profile_interval_overlap"]):
        return "EXACT_Z_AMPLITUDE_TENSION"
    return "EXACT_Z_CONCORDANT_WITHIN_DIAGNOSTIC"


def main():
    desi_rows, desi_cov = p17.load_desi()
    boss_rows, boss_cov = p17.load_boss()

    desi_full = p17.fit_desi(desi_rows, desi_cov)["RCMS"]
    boss_full = p17.fit_boss(boss_rows, boss_cov)["RCMS"]

    # Frozen exact-z primary comparison.
    di = exact_indices(desi_rows, TARGET_Z)
    bi = exact_indices(boss_rows, TARGET_Z)
    d_primary = profile_payload(desi_rows, desi_cov, desi_full, p19.prediction_grid_desi, di)
    b_primary = profile_payload(boss_rows, boss_cov, boss_full, p19.prediction_grid_boss, bi)
    primary_summary = cross_summary(d_primary, b_primary)
    classification = classify(primary_summary)

    # Frozen secondary BOSS-span sensitivity window.
    dwi = window_indices(desi_rows, *WINDOW)
    bwi = window_indices(boss_rows, *WINDOW)
    d_window = profile_payload(desi_rows, desi_cov, desi_full, p19.prediction_grid_desi, dwi)
    b_window = profile_payload(boss_rows, boss_cov, boss_full, p19.prediction_grid_boss, bwi)
    window_summary = cross_summary(d_window, b_window)

    payload = {
        "protocol": "P20",
        "status": "FINAL",
        "target_redshift": TARGET_Z,
        "secondary_window": list(WINDOW),
        "frozen_full_vector_states": {
            "DESI_DR2": {k: float(v) for k, v in desi_full.items() if k != "pred"},
            "BOSS_DR12": {k: float(v) for k, v in boss_full.items() if k != "pred"},
        },
        "primary_exact_z": {
            "DESI_DR2": d_primary,
            "BOSS_DR12": b_primary,
            "summary": primary_summary,
        },
        "secondary_window_diagnostic": {
            "DESI_DR2": d_window,
            "BOSS_DR12": b_window,
            "summary": window_summary,
        },
        "classification": classification,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("RCMS P20 — Exact-redshift cross-survey concordance")
    print(
        f"z={TARGET_Z:.2f} DESI A_R={d_primary['A_R']:.3f} profile={d_primary['profile_delta_chi2_1']} "
        f"boundary={d_primary['boundary_contact']}"
    )
    print(
        f"z={TARGET_Z:.2f} BOSS A_R={b_primary['A_R']:.3f} profile={b_primary['profile_delta_chi2_1']} "
        f"boundary={b_primary['boundary_contact']}"
    )
    print(f"primary_summary={primary_summary}")
    print(
        f"window DESI A_R={d_window['A_R']:.3f} profile={d_window['profile_delta_chi2_1']} | "
        f"BOSS A_R={b_window['A_R']:.3f} profile={b_window['profile_delta_chi2_1']}"
    )
    print(f"window_summary={window_summary}")
    print(f"P20_CLASSIFICATION={classification}")
    print(f"machine_readable={OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
