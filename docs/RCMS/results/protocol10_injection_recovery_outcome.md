# RCMS Protocol 10 — Frozen Injection/Recovery Outcome

**Release line:** v0.3-dev  
**Parent release:** v0.2.0 — DOI `10.5281/zenodo.22002018`  
**Status:** FINAL / FROZEN  
**Classification:** `RECOVERY_PASS`

## Scientific run identity

- realizations per injected truth: `N_per_truth = 2000`
- master seed: `20260821`
- injected truths: `A_R = [-0.4, -0.2, 0.0, +0.2, +0.4]`
- runner: `tools/run_rcms_protocol10_injection_recovery.py`
- GitHub Actions run: `32587458321`
- scientific CSV SHA256: `f042891dda3e05c0bbb9d1b78269f3560aa50005e39834608fc2e4cc925b328d`
- archived workflow artifact: `rcms-protocol10`, artifact ID `9479421198`

## Frozen recovery table

| Injected `A_R` | Mean recovered | Std | Bias ratio `B` | Coverage95 | Sign recovery | Class |
|---:|---:|---:|---:|---:|---:|---|
| -0.40 | -0.392210 | 0.144973 | 0.053734 | 0.9550 | 0.9945 | PASS |
| -0.20 | -0.192935 | 0.162238 | 0.043547 | 0.9525 | 0.8750 | PASS |
| 0.00 | +0.002555 | 0.174883 | 0.014610 | 0.9560 | n/a | PASS |
| +0.20 | +0.205175 | 0.195062 | 0.026530 | 0.9485 | 0.8495 | PASS |
| +0.40 | +0.397530 | 0.208200 | 0.011864 | 0.9530 | 0.9750 | PASS |

## Linearity

The preregistered linear recovery fit is

`A_recovered_mean = alpha + beta * A_injected`

with

- `alpha = 0.004023000`
- `beta = 0.988795000`

The recovery is therefore close to unbiased and close to unit slope across both signs.

## Interpretation

P10 shows that the frozen calibration pipeline can recover negative, null, and positive injected RCMS amplitudes without a material one-sided pull toward positive values in this synthetic DESI-like structure. This supports estimator calibration only. It does not validate the physical RCMS interpretation and does not establish that the positive observational direction is new physics.
