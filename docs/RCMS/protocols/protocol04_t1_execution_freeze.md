# RCMS Protocol 04 — P04-T1 execution freeze

**Status:** Frozen before P04-T1 RCMS output is inspected  
**Parent protocol:** `protocol04_independent_shape_replication.md`  
**P04-T0 gate:** PASS on GitHub Actions run `31855944476`  
**RSMS compatibility:** RSMS-1.0

## Purpose

This document freezes the numerical execution settings for the first permitted Protocol 04 RCMS reveal after P04-T0 passed.

## Dataset and likelihood

The primary statistic remains exactly the eBOSS DR16 set frozen for P04-T0:

- LRG at `z_eff=0.698`, `DM_over_rs` and `DH_over_rs`, published covariance;
- QSO at `z_eff=1.48`, `DM_over_rs` and `DH_over_rs`, published covariance;
- Lyman-alpha auto-correlation at `z_eff=2.334`, published 2D probability grid.

No DESI, Pantheon+, DES-SN, CMB, SH0ES, BBN, sound-horizon calibration, or other likelihood is added.

The common scale nuisance remains

`q = c / (H0 r_d)`

and is fitted symmetrically under Lambda-CDM and RCMS.

## Frozen model

Lambda-CDM null:

`E(z)^2 = Omega_m (1+z)^3 + 1 - Omega_m`

RCMS surrogate:

`E(z)^2 = Omega_m (1+z)^3 + 1 - Omega_m + A_R ln(1+z)`

No additional RCMS parameter is permitted.

## Parameter domains

The P04-T0 domains are retained:

- `Omega_m in [0.10, 0.50]`
- `q in [20.0, 45.0]`

The inherited RCMS screening domain used in the preceding RCMS protocols is retained without change:

- `A_R in [-5.0, 5.0]`

The carried-forward positive regions are comparison targets only and are not used as priors or optimizer restrictions.

## Numerical procedure

1. Re-run P04-T0 in the same workflow as a gate.
2. Fit the Lambda-CDM null with `A_R=0`.
3. Fit RCMS in `(Omega_m, q, A_R)` using deterministic fixed multi-start bounded minimization.
4. Profile `(Omega_m, q)` at fixed `A_R` and determine the `Delta chi2 <= 1` interval by deterministic bracketing/root finding.
5. Record parameter-boundary diagnostics and convergence state.
6. Compute `Delta chi2 = chi2_null - chi2_RCMS`.
7. Compute `Delta AIC = Delta chi2 - 2`, because RCMS adds exactly one fitted parameter.
8. Do not report BIC as a formal selection statistic for this hybrid compressed likelihood; the Lyman-alpha contribution is a non-Gaussian 2D likelihood grid and a defensible asymptotic independent-observation count is not frozen.
9. Apply the directional labels exactly as defined in Protocol 04 Section 9.

## Directional classification rule

- `SIGN_REVERSAL` if the best fit is negative and the `Delta chi2<=1` interval excludes zero on the negative side.
- `NULL_COMPATIBLE` if the profile interval contains zero.
- `POSITIVE_COMPATIBLE` if the best fit is positive, the profile excludes zero, and the profile overlaps either carried-forward positive interval.
- `POSITIVE_TENSION` if the best fit is positive, the profile excludes zero, and it overlaps neither carried-forward positive interval.
- `NOT_IDENTIFIABLE` if a finite two-sided profile interval cannot be established within the frozen `A_R` domain or the solution is boundary-limited.

## Anti-tuning statement

These choices are frozen before the P04-T1 RCMS output is inspected. If the result is null, negative, boundary-limited, or in tension with earlier RCMS results, it is retained unchanged. No response-dependent alteration of model form, bounds, dataset membership, covariance, or nuisance treatment is permitted inside Protocol 04.
