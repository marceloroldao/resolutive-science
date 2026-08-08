"""Small-data tests for the Pantheon+ RCMS runner.

These tests validate the mathematical machinery without downloading the
33 MB production covariance.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "fit_rcms_pantheonplus.py"
spec = importlib.util.spec_from_file_location("fit_rcms_pantheonplus", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def test_intercept_marginalization_is_shift_invariant() -> None:
    zcmb = np.asarray([0.05, 0.1, 0.3, 0.7], dtype=float)
    zhel = zcmb.copy()
    theory = mod.pantheon_lumdists(zcmb, zhel, 0.3, 0.0)
    cov = np.diag([0.01, 0.02, 0.015, 0.012])
    mag = theory + 23.4
    like = mod.MarginalizedSN(mag, zcmb, zhel, cov)
    chi2, intercept = like.chi2(0.3, 0.0)
    assert abs(chi2) < 1e-9
    assert abs(intercept - 23.4) < 1e-9


def test_effective_model_recovers_lcdm_at_zero_amplitude() -> None:
    zcmb = np.asarray([0.02, 0.2, 0.8, 1.5], dtype=float)
    zhel = np.asarray([0.021, 0.201, 0.801, 1.501], dtype=float)
    lcdm = mod.pantheon_lumdists(zcmb, zhel, 0.31, 0.0)
    rcms_zero = mod.pantheon_lumdists(zcmb, zhel, 0.31, 0.0)
    np.testing.assert_allclose(lcdm, rcms_zero, rtol=0.0, atol=1e-12)


def test_distance_prediction_is_independent_of_common_h0_after_intercept_projection() -> None:
    zcmb = np.asarray([0.04, 0.2, 0.6, 1.2], dtype=float)
    zhel = zcmb.copy()
    theory = mod.pantheon_lumdists(zcmb, zhel, 0.3, 0.0)
    cov = np.eye(len(zcmb)) * 0.02
    # Adding any global magnitude offset must be absorbed by the nuisance intercept.
    like_a = mod.MarginalizedSN(theory + 20.0, zcmb, zhel, cov)
    like_b = mod.MarginalizedSN(theory + 24.0, zcmb, zhel, cov)
    chi2_a, _ = like_a.chi2(0.3, 0.0)
    chi2_b, _ = like_b.chi2(0.3, 0.0)
    assert abs(chi2_a - chi2_b) < 1e-9


def test_nonpositive_expansion_is_rejected() -> None:
    zcmb = np.asarray([0.1, 1.0, 2.0], dtype=float)
    try:
        mod.distance_integrals(zcmb, 0.05, -5.0)
    except ValueError:
        return
    raise AssertionError("expected non-positive E(z)^2 to be rejected")
