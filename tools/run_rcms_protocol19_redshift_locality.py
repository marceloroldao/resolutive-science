#!/usr/bin/env python3
"""RCMS Protocol 19 — redshift-locality diagnostic with look-elsewhere calibration."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import run_rcms_protocol17_residual_topology as p17

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/rcms_protocol19_redshift_locality.json"
SEED = 190019
NSIM = 2000


def candidate_splits(rows):
    zvals = sorted(set(float(r[0]) for r in rows))
    out = []
    for a, b in zip(zvals[:-1], zvals[1:]):
        s = 0.5 * (a + b)
        low = [i for i, r in enumerate(rows) if r[0] < s]
        high = [i for i, r in enumerate(rows) if r[0] > s]
        if len(low) >= 2 and len(high) >= 2:
            out.append((s, low, high))
    if not out:
        raise RuntimeError("no admissible redshift split")
    return out


def prediction_grid_desi(rows, om, q):
    avals = np.arange(p17.DESI_A_BOUNDS[0], p17.DESI_A_BOUNDS[1] + 0.5 * p17.DESI_A_STEP, p17.DESI_A_STEP)
    preds = []
    for a in avals:
        preds.append(q * p17.desi_shape(rows, om, float(a)))
    return avals, np.asarray(preds, dtype=float)


def prediction_grid_boss(rows, om, q):
    avals = np.arange(p17.BOSS_A_BOUNDS[0], p17.BOSS_A_BOUNDS[1] + 0.5 * p17.BOSS_A_STEP, p17.BOSS_A_STEP)
    preds = []
    for a in avals:
        dm, hz = p17.boss_components(rows, om, float(a))
        preds.append(q * dm + hz / q)
    return avals, np.asarray(preds, dtype=float)


def chi2_grid(data, cov, pred_grid, idx):
    ix = np.asarray(idx, dtype=int)
    y = np.asarray(data, dtype=float)[ix]
    m = pred_grid[:, ix]
    ci = np.linalg.inv(cov[np.ix_(ix, ix)])
    r = y[None, :] - m
    return np.einsum("ai,ij,aj->a", r, ci, r, optimize=True)


def observed_local_profile(data, cov, pred_grid, avals, idx):
    c = chi2_grid(data, cov, pred_grid, idx)
    j = int(np.argmin(c))
    m = float(c[j])
    inside = np.flatnonzero(c <= m + 1.0 + 1e-12)
    lo = float(avals[int(inside[0])])
    hi = float(avals[int(inside[-1])])
    a = float(avals[j])
    step = float(avals[1] - avals[0])
    boundary = bool(abs(a - avals[0]) < 0.51 * step or abs(a - avals[-1]) < 0.51 * step)
    return {"A_R": a, "chi2": m, "profile_delta_chi2_1": [lo, hi], "boundary_contact": boundary}


def sim_best_indices(Y, cov, pred_grid, idx):
    ix = np.asarray(idx, dtype=int)
    y = Y[:, ix]
    m = pred_grid[:, ix]
    ci = np.linalg.inv(cov[np.ix_(ix, ix)])
    yci = y @ ci
    ycy = np.einsum("bi,bi->b", yci, y, optimize=True)
    cross = yci @ m.T
    mcm = np.einsum("ai,ij,aj->a", m, ci, m, optimize=True)
    chi = ycy[:, None] - 2.0 * cross + mcm[None, :]
    return np.argmin(chi, axis=1)


def analyze_survey(name, rows, cov, full_fit, pred_builder, rng):
    data = np.asarray([r[1] for r in rows], dtype=float)
    om = float(full_fit["Omega_m"])
    q = float(full_fit["q"])
    a_full = float(full_fit["A_R"])
    avals, pred_grid = pred_builder(rows, om, q)
    full_idx = int(np.argmin(np.abs(avals - a_full)))
    if abs(float(avals[full_idx]) - a_full) > 0.51 * float(avals[1] - avals[0]):
        raise RuntimeError(f"{name}: full amplitude missing from grid")
    mu = pred_grid[full_idx]

    # Full-covariance constant-amplitude null simulations.
    L = np.linalg.cholesky(cov)
    Y = mu[None, :] + rng.standard_normal((NSIM, len(rows))) @ L.T

    splits = []
    sim_d_by_split = []
    for split_z, low_idx, high_idx in candidate_splits(rows):
        low = observed_local_profile(data, cov, pred_grid, avals, low_idx)
        high = observed_local_profile(data, cov, pred_grid, avals, high_idx)
        d = abs(low["A_R"] - high["A_R"])

        low_best = sim_best_indices(Y, cov, pred_grid, low_idx)
        high_best = sim_best_indices(Y, cov, pred_grid, high_idx)
        sim_d = np.abs(avals[low_best] - avals[high_best])
        sim_d_by_split.append(sim_d)

        overlap = max(low["profile_delta_chi2_1"][0], high["profile_delta_chi2_1"][0]) <= min(
            low["profile_delta_chi2_1"][1], high["profile_delta_chi2_1"][1]
        )
        splits.append({
            "split_z": float(split_z),
            "n_low": len(low_idx),
            "n_high": len(high_idx),
            "low": low,
            "high": high,
            "D": float(d),
            "opposite_signs": bool(low["A_R"] * high["A_R"] < 0.0),
            "profile_overlap": bool(overlap),
        })

    obs_d = np.asarray([s["D"] for s in splits])
    j = int(np.argmax(obs_d))
    sim_dmax = np.max(np.vstack(sim_d_by_split), axis=0)
    dmax = float(obs_d[j])
    exceed = int(np.count_nonzero(sim_dmax >= dmax - 1e-12))
    p_emp = float((1 + exceed) / (NSIM + 1))
    winner = splits[j]

    return {
        "frozen_full_fit": {"Omega_m": om, "q": q, "A_R": a_full, "chi2": float(full_fit["chi2"])},
        "candidate_splits": splits,
        "D_max": dmax,
        "maximizing_split_z": float(winner["split_z"]),
        "max_split_low_A_R": float(winner["low"]["A_R"]),
        "max_split_high_A_R": float(winner["high"]["A_R"]),
        "max_split_opposite_signs": bool(winner["opposite_signs"]),
        "max_split_profile_overlap": bool(winner["profile_overlap"]),
        "max_split_boundary_contact": bool(winner["low"]["boundary_contact"] or winner["high"]["boundary_contact"]),
        "look_elsewhere_N": NSIM,
        "look_elsewhere_exceedances": exceed,
        "look_elsewhere_p": p_emp,
    }


def classify(surveys):
    strong = []
    raw_weak = []
    for s in surveys.values():
        strong.append(s["look_elsewhere_p"] <= 0.05 and not s["max_split_profile_overlap"])
        raw_weak.append(s["D_max"] >= 0.50 and s["max_split_opposite_signs"])
    if all(strong):
        return "REDSHIFT_LOCALITY_RECURRENT"
    if sum(strong) == 1:
        return "REDSHIFT_LOCALITY_SURVEY_SPECIFIC"
    if any(raw_weak):
        return "REDSHIFT_LOCALITY_WEAK"
    return "NO_REDSHIFT_LOCALITY_EVIDENCE"


def main():
    desi_rows, desi_cov = p17.load_desi()
    boss_rows, boss_cov = p17.load_boss()
    desi = p17.fit_desi(desi_rows, desi_cov)["RCMS"]
    boss = p17.fit_boss(boss_rows, boss_cov)["RCMS"]

    # Independent deterministic streams under one preregistered seed.
    root_rng = np.random.default_rng(SEED)
    desi_rng = np.random.default_rng(root_rng.integers(0, 2**63 - 1))
    boss_rng = np.random.default_rng(root_rng.integers(0, 2**63 - 1))

    surveys = {
        "DESI_DR2": analyze_survey("DESI_DR2", desi_rows, desi_cov, desi, prediction_grid_desi, desi_rng),
        "BOSS_DR12": analyze_survey("BOSS_DR12", boss_rows, boss_cov, boss, prediction_grid_boss, boss_rng),
    }
    classification = classify(surveys)
    payload = {
        "protocol": "P19",
        "status": "FINAL",
        "seed": SEED,
        "N_simulations_per_survey": NSIM,
        "scope": "redshift-local diagnostic amplitude pulls with frozen full-fit Omega_m and BAO scale",
        "surveys": surveys,
        "classification": classification,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("RCMS P19 — Redshift locality diagnostic")
    for name, s in surveys.items():
        print(
            f"{name}: D_max={s['D_max']:.3f} split={s['maximizing_split_z']:.6f} "
            f"A_low={s['max_split_low_A_R']:.3f} A_high={s['max_split_high_A_R']:.3f} "
            f"opposite={s['max_split_opposite_signs']} overlap={s['max_split_profile_overlap']} "
            f"boundary={s['max_split_boundary_contact']} p_LEE={s['look_elsewhere_p']:.6f}"
        )
    print(f"P19_CLASSIFICATION={classification}")
    print(f"machine_readable={OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
