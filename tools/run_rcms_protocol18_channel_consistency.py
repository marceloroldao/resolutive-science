#!/usr/bin/env python3
"""RCMS Protocol 18 — radial/transverse parameter-consistency audit."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import run_rcms_protocol17_residual_topology as p17

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/rcms_protocol18_channel_consistency.json"


def subset(rows, cov, keep):
    idx = np.asarray(keep, dtype=int)
    return [rows[i] for i in idx], cov[np.ix_(idx, idx)]


def profile_desi_subset(rows, cov):
    ci = np.linalg.inv(cov)
    chi0, om0, q0, _ = p17.desi_profile(rows, ci, 0.0)
    grid = []
    best = (float("inf"), None, None, None)
    n = int(round((p17.DESI_A_BOUNDS[1] - p17.DESI_A_BOUNDS[0]) / p17.DESI_A_STEP)) + 1
    for i in range(n):
        a = p17.DESI_A_BOUNDS[0] + i * p17.DESI_A_STEP
        chi, om, q, _ = p17.desi_profile(rows, ci, a)
        grid.append((a, chi, om, q))
        if chi < best[0]:
            best = (chi, a, om, q)
    chi1, a1, om1, q1 = best
    inside = [x for x in grid if x[1] <= chi1 + 1.0]
    lo, hi = inside[0][0], inside[-1][0]
    dchi = chi0 - chi1
    boundary = bool(
        abs(a1 - p17.DESI_A_BOUNDS[0]) < p17.DESI_A_STEP
        or abs(a1 - p17.DESI_A_BOUNDS[1]) < p17.DESI_A_STEP
        or om1 <= p17.OMEGA_BOUNDS[0] + 1e-4
        or om1 >= p17.OMEGA_BOUNDS[1] - 1e-4
    )
    return {
        "nobs": len(rows),
        "LCDM": {"chi2": chi0, "Omega_m": om0, "q": q0},
        "RCMS": {"chi2": chi1, "Omega_m": om1, "q": q1, "A_R": a1},
        "A_R_profile_delta_chi2_1": [lo, hi],
        "zero_in_profile": bool(lo <= 0.0 <= hi),
        "Delta_chi2": dchi,
        "Delta_AIC": dchi - 2.0,
        "boundary_contact": boundary,
    }


def profile_boss_subset(rows, cov):
    data = np.asarray([r[1] for r in rows], dtype=float)
    ci = np.linalg.inv(cov)
    chi0, om0, q0, _ = p17.boss_profile(rows, data, ci, 0.0)
    grid = []
    best = (float("inf"), None, None, None)
    n = int(round((p17.BOSS_A_BOUNDS[1] - p17.BOSS_A_BOUNDS[0]) / p17.BOSS_A_STEP)) + 1
    for i in range(n):
        a = p17.BOSS_A_BOUNDS[0] + i * p17.BOSS_A_STEP
        chi, om, q, _ = p17.boss_profile(rows, data, ci, a)
        grid.append((a, chi, om, q))
        if chi < best[0]:
            best = (chi, a, om, q)
    chi1, a1, om1, q1 = best
    inside = [x for x in grid if x[1] <= chi1 + 1.0]
    lo, hi = inside[0][0], inside[-1][0]
    dchi = chi0 - chi1
    boundary = bool(
        abs(a1 - p17.BOSS_A_BOUNDS[0]) < p17.BOSS_A_STEP
        or abs(a1 - p17.BOSS_A_BOUNDS[1]) < p17.BOSS_A_STEP
        or om1 <= p17.OMEGA_BOUNDS[0] + 1e-4
        or om1 >= p17.OMEGA_BOUNDS[1] - 1e-4
        or q1 <= p17.Q_BOUNDS[0] + 1e-3
        or q1 >= p17.Q_BOUNDS[1] - 1e-3
    )
    return {
        "nobs": len(rows),
        "LCDM": {"chi2": chi0, "Omega_m": om0, "q": q0},
        "RCMS": {"chi2": chi1, "Omega_m": om1, "q": q1, "A_R": a1},
        "A_R_profile_delta_chi2_1": [lo, hi],
        "zero_in_profile": bool(lo <= 0.0 <= hi),
        "Delta_chi2": dchi,
        "Delta_AIC": dchi - 2.0,
        "boundary_contact": boundary,
    }


def survey_summary(radial, transverse):
    ar_r = radial["RCMS"]["A_R"]
    ar_t = transverse["RCMS"]["A_R"]
    rlo, rhi = radial["A_R_profile_delta_chi2_1"]
    tlo, thi = transverse["A_R_profile_delta_chi2_1"]
    overlap = max(rlo, tlo) <= min(rhi, thi)
    gap = 0.0 if overlap else max(tlo - rhi, rlo - thi)
    return {
        "sign_agreement": bool(ar_r == 0.0 or ar_t == 0.0 or ar_r * ar_t > 0.0),
        "opposite_best_fit_signs": bool(ar_r * ar_t < 0.0),
        "profile_interval_overlap": bool(overlap),
        "profile_interval_gap": float(gap),
        "best_amplitude_separation": float(abs(ar_r - ar_t)),
        "boundary_limited": bool(radial["boundary_contact"] or transverse["boundary_contact"]),
    }


def classify(summaries):
    opposite = [s["opposite_best_fit_signs"] for s in summaries.values()]
    disjoint = [not s["profile_interval_overlap"] for s in summaries.values()]
    if all(opposite):
        return "CROSS_SURVEY_CHANNEL_SIGN_REVERSAL"
    if sum(opposite) == 1 or (all(disjoint) and sum(opposite) == 1):
        return "SURVEY_SPECIFIC_CHANNEL_TENSION"
    if any(disjoint):
        return "CHANNEL_AMPLITUDE_HETEROGENEITY"
    return "CHANNEL_CONSISTENT_WITHIN_DIAGNOSTIC"


def main():
    desi_rows, desi_cov = p17.load_desi()
    boss_rows, boss_cov = p17.load_boss()

    # Full-vector closure gates inherited from P17/P13/P16.
    desi_full = p17.fit_desi(desi_rows, desi_cov)
    boss_full = p17.fit_boss(boss_rows, boss_cov)

    d_rad_idx = [i for i, r in enumerate(desi_rows) if r[2] == "DH_over_rs"]
    d_tr_idx = [i for i, r in enumerate(desi_rows) if r[2] != "DH_over_rs"]
    b_rad_idx = [i for i, r in enumerate(boss_rows) if r[2] == "bao_Hz_rs"]
    b_tr_idx = [i for i, r in enumerate(boss_rows) if r[2] == "DM_over_rs"]

    d_rad = profile_desi_subset(*subset(desi_rows, desi_cov, d_rad_idx))
    d_tr = profile_desi_subset(*subset(desi_rows, desi_cov, d_tr_idx))
    b_rad = profile_boss_subset(*subset(boss_rows, boss_cov, b_rad_idx))
    b_tr = profile_boss_subset(*subset(boss_rows, boss_cov, b_tr_idx))

    if abs(d_rad["RCMS"]["A_R"] + 0.58) > p17.DESI_A_STEP + 1e-12:
        raise RuntimeError(f"P13 radial closure failed: {d_rad['RCMS']['A_R']}")
    if abs(d_tr["RCMS"]["A_R"] - 0.86) > p17.DESI_A_STEP + 1e-12:
        raise RuntimeError(f"P13 transverse closure failed: {d_tr['RCMS']['A_R']}")

    surveys = {
        "DESI_DR2": {"radial": d_rad, "transverse_volume": d_tr},
        "BOSS_DR12": {"radial": b_rad, "transverse": b_tr},
    }
    summaries = {
        "DESI_DR2": survey_summary(d_rad, d_tr),
        "BOSS_DR12": survey_summary(b_rad, b_tr),
    }
    classification = classify(summaries)

    payload = {
        "protocol": "P18",
        "status": "FINAL",
        "scope": "matched radial/transverse BAO parameter-consistency audit",
        "full_vector_closure": {
            "DESI_DR2": {
                "LCDM_chi2": desi_full["LCDM"]["chi2"],
                "RCMS_chi2": desi_full["RCMS"]["chi2"],
                "RCMS_A_R": desi_full["RCMS"]["A_R"],
            },
            "BOSS_DR12": {
                "LCDM_chi2": boss_full["LCDM"]["chi2"],
                "RCMS_chi2": boss_full["RCMS"]["chi2"],
                "RCMS_A_R": boss_full["RCMS"]["A_R"],
            },
        },
        "surveys": surveys,
        "summaries": summaries,
        "classification": classification,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("RCMS P18 — Radial/transverse consistency audit")
    for survey, channels in surveys.items():
        for name, r in channels.items():
            print(
                f"{survey} {name}: N={r['nobs']} A_R={r['RCMS']['A_R']:.3f} "
                f"profile={r['A_R_profile_delta_chi2_1']} Delta_chi2={r['Delta_chi2']:.9f} "
                f"Delta_AIC={r['Delta_AIC']:.9f} boundary={r['boundary_contact']}"
            )
        print(f"{survey} summary={summaries[survey]}")
    print(f"P18_CLASSIFICATION={classification}")
    print(f"machine_readable={OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
