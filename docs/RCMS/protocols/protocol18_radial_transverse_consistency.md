# RCMS Protocol 18 — Radial/Transverse Consistency Audit

**Status:** PREREGISTERED / DIAGNOSTIC  
**Release line:** v0.4-dev  
**Parent evidence:** P13, P14, P17-A; v0.3.0 DOI `10.5281/zenodo.22643804`

## 1. Purpose

P18 tests whether the radial-versus-transverse amplitude incompatibility observed inside DESI DR2 in P13 recurs in an independent BAO survey under matched frozen conventions.

P18 is a parameter-consistency audit. It does not introduce a new model, channel correction, redshift switch, or survey-dependent term.

The frozen surrogate remains

\[
E^2(z)=\Omega_m(1+z)^3+(1-\Omega_m)+A_R\ln(1+z).
\]

## 2. Datasets

Use the same two complete-covariance BAO datasets validated in P17-A:

- DESI DR2 13-observable vector;
- SDSS-III BOSS DR12 six-observable consensus vector from frozen upstream revision `bb0c1c9009dc76d1391300e169e8df38fd1096db`.

No additional dataset may be added after observing the P18 result.

## 3. Frozen channel decomposition

### DESI DR2

- radial: `DH_over_rs` only;
- transverse/volume: `DM_over_rs` and `DV_over_rs` only.

### BOSS DR12

- radial: `bao_Hz_rs` only;
- transverse: `DM_over_rs` only.

Each subset uses the corresponding covariance submatrix from the original full covariance.

## 4. Likelihood and nuisance policy

For every subset:

- preserve the exact survey-specific likelihood convention used in P13/P16;
- preserve `Omega_m in [0.05,0.60]`;
- preserve `A_R in [-1,+1]`;
- profile the same global BAO scale nuisance used in the parent protocol;
- use no external CMB, SH0ES, `r_d`, BBN, or calibration prior.

The amplitude grid is frozen to:

- DESI: step `0.01`;
- BOSS: step `0.005`.

## 5. Required closure gates

Before accepting channel results, the runner must reproduce:

- the P13 DESI full-vector baseline;
- the P13 DESI radial-only best amplitude `A_R=-0.58` within one grid step;
- the P13 DESI transverse/volume-only best amplitude `A_R=+0.86` within one grid step;
- the P16 BOSS full-vector Lambda-CDM and RCMS fits.

If these fail, classify `P18_INVALID`.

## 6. Outputs per survey/channel

For radial and transverse subsets report:

- number of observables;
- best `A_R`, `Omega_m`, nuisance scale, chi-square;
- `Delta chi2` against `A_R=0`;
- `Delta AIC` for the added amplitude;
- `Delta chi2 <= 1` profile interval in the frozen domain;
- whether zero lies in the interval;
- whether any primary parameter touches a frozen boundary.

## 7. Cross-channel diagnostics

For each survey report:

- sign agreement between radial and transverse best amplitudes;
- profile-interval overlap;
- interval gap when disjoint;
- absolute best-amplitude separation `|A_radial-A_transverse|`.

## 8. Preregistered classification

### `CROSS_SURVEY_CHANNEL_SIGN_REVERSAL`

Both DESI and BOSS have valid radial and transverse subset fits, and in **both** surveys the radial and transverse best-fit amplitudes have opposite signs.

Boundary contact does not erase the sign observation, but any survey with a boundary-limited subset must also carry the qualifier `boundary_limited=true` and prevents a stronger amplitude-separation claim.

### `SURVEY_SPECIFIC_CHANNEL_TENSION`

Exactly one of the two surveys has opposite radial/transverse best-fit signs, or both surveys show non-overlapping one-sigma profile intervals but only one has opposite signs.

### `CHANNEL_AMPLITUDE_HETEROGENEITY`

Neither sign-reversal label applies, but at least one survey has disjoint radial/transverse `Delta chi2 <= 1` intervals.

### `CHANNEL_CONSISTENT_WITHIN_DIAGNOSTIC`

Neither survey has opposite best-fit signs and the radial/transverse one-sigma profile intervals overlap in both surveys.

### `P18_INVALID`

A closure, covariance, or numerical-identifiability gate fails so that the required comparison cannot be made.

## 9. Interpretation boundary

P18 cannot identify the physical cause of a channel discrepancy. A recurrent sign reversal could reflect model inadequacy, survey conventions, residual systematics, BAO compression choices, or other structure. It only determines whether the P13 channel sensitivity is isolated or recurrent.

No channel-dependent RCMS term may be proposed until P19 and P20 are also completed.
