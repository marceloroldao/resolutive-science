# RCMS Protocol 19 — Redshift Locality Diagnostic

**Status:** PREREGISTERED / DIAGNOSTIC  
**Release line:** v0.4-dev  
**Parent evidence:** P17-A, P18; v0.3.0 DOI `10.5281/zenodo.22643804`

## 1. Purpose

P19 asks whether the fitted RCMS deformation pull is organized by redshift after P17 found diffuse post-fit residual topology and P18 found a survey-specific, rather than cross-survey, channel tension.

P19 does **not** introduce a redshift-dependent physical parameter into RCMS. It computes redshift-local diagnostic amplitude pulls around each survey's already frozen full-vector RCMS nuisance state.

The physical surrogate remains unchanged:

\[
E^2(z)=\Omega_m(1+z)^3+(1-\Omega_m)+A_R\ln(1+z).
\]

## 2. Datasets

Use exactly the P17/P18 complete-covariance BAO datasets:

- DESI DR2 13-observable vector;
- BOSS DR12 six-observable consensus vector at `z=0.38,0.51,0.61`.

No additional survey is admitted after P19 outcome inspection.

## 3. Frozen nuisance state

For each survey first reproduce the full-vector RCMS fit under the parent likelihood.

Then freeze:

- `Omega_m` to that survey's full-vector RCMS best fit;
- the survey's global BAO scale nuisance to that full-vector RCMS best fit.

For all locality diagnostics, only `A_R` is scanned. The scale nuisance and `Omega_m` are **not** reprofiled separately in low/high-redshift subsets.

This prevents subset-specific nuisance freedom from masquerading as redshift evolution.

## 4. Candidate redshift splits

Candidate split points are the midpoints between adjacent unique survey redshifts, subject to both sides containing at least two observables.

For each split `z_s`:

- low subset: observables with `z < z_s`;
- high subset: observables with `z > z_s`;
- use the corresponding covariance submatrix for each subset;
- scan `A_R in [-1,+1]` with the parent survey step (`0.01` DESI, `0.005` BOSS), holding the frozen nuisance state fixed.

For each side report best `A_R` and `Delta chi2 <= 1` profile interval.

## 5. Primary locality statistic

For each candidate split define

\[
D(z_s)=|A_{\rm low}-A_{\rm high}|.
\]

The primary observed statistic is

\[
D_{\max}=\max_{z_s} D(z_s).
\]

The split that maximizes `D` is diagnostic only; it is not a fitted physical transition redshift.

## 6. Look-elsewhere calibration

Because multiple split points are scanned, the raw maximum separation cannot be interpreted without calibration.

P19 uses a parametric null generated from the survey's frozen **constant-amplitude full RCMS best fit** and full covariance.

Frozen Monte Carlo design:

- deterministic NumPy RNG seed: `190019`;
- `N = 2000` realizations per survey;
- synthetic vector sampled from the full best-fit RCMS prediction with the full survey covariance;
- for each synthetic realization repeat the identical split scan and compute `D_max`;
- empirical p-value with plus-one correction:

\[
p = \frac{1 + \#\{D_{\max}^{\rm sim}\ge D_{\max}^{\rm obs}\}}{N+1}.
\]

The simulation is a diagnostic calibration under the frozen Gaussian likelihood; it is not a discovery significance for new physics.

## 7. Additional diagnostics

Report per survey:

- all candidate splits;
- low/high best amplitudes and one-sigma profile intervals;
- `D_max` and maximizing split;
- empirical look-elsewhere p-value;
- whether low/high best amplitudes have opposite signs at the maximizing split;
- whether their one-sigma intervals overlap;
- boundary contact for either local best amplitude.

## 8. Preregistered classification

### `REDSHIFT_LOCALITY_RECURRENT`

Both surveys have look-elsewhere `p <= 0.05`, with non-overlapping low/high one-sigma amplitude intervals at their maximizing splits.

### `REDSHIFT_LOCALITY_SURVEY_SPECIFIC`

Exactly one survey has look-elsewhere `p <= 0.05` and non-overlapping low/high one-sigma intervals.

### `REDSHIFT_LOCALITY_WEAK`

Neither stronger label applies, but at least one survey has raw `D_max >= 0.50` and opposite-sign local best amplitudes.

### `NO_REDSHIFT_LOCALITY_EVIDENCE`

None of the above criteria are met and all numerical/calibration gates pass.

### `P19_INVALID`

Full-fit closure, covariance generation, local profile evaluation, or Monte Carlo calibration fails.

Boundary contact does not automatically invalidate the diagnostic but must be reported and prevents interpretation of the numerical amplitude separation as a well-localized transition.

## 9. Non-negotiable interpretation boundary

- No fitted change-point is promoted to cosmological physics.
- No piecewise `A_R(z)` model is introduced by P19.
- No split may be selected manually after seeing the outcome.
- No external prior may be added after inspection.
- P19 cannot justify a new redshift-dependent RCMS form by itself; P20 cross-survey concordance must be completed first.
