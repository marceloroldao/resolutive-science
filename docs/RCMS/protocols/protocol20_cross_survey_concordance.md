# RCMS Protocol 20 — Cross-Survey Concordance at Matched Redshift

**Status:** PREREGISTERED / DIAGNOSTIC  
**Release line:** v0.4-dev  
**Parent evidence:** P17–P19; v0.3.0 DOI `10.5281/zenodo.22643804`

## 1. Purpose

P20 is the final diagnosis-before-extension gate. It asks whether independent DESI DR2 and BOSS DR12 BAO measurements at the same cosmic epoch prefer compatible local directions under the unchanged RCMS surrogate.

Both surveys contain radial and transverse measurements at exactly

\[
z=0.51.
\]

This exact redshift match is frozen as the primary comparison before execution. No redshift interpolation is used.

## 2. Model boundary

The physical surrogate remains

\[
E^2(z)=\Omega_m(1+z)^3+(1-\Omega_m)+A_R\ln(1+z).
\]

P20 introduces no new parameter, survey offset, channel correction, or redshift law.

## 3. Primary matched-redshift subsets

### DESI DR2 at z=0.51

Use exactly the two measurements:

- `DM_over_rs`;
- `DH_over_rs`.

Use the corresponding 2x2 covariance submatrix from the frozen DESI DR2 covariance.

### BOSS DR12 at z=0.51

Use exactly the two measurements:

- `DM_over_rs`;
- `bao_Hz_rs`.

Use the corresponding 2x2 covariance submatrix from the frozen BOSS DR12 covariance.

The BOSS likelihood retains its native published convention; no approximate conversion of the measured vector is introduced.

## 4. Frozen nuisance state

For each survey first reproduce the full-vector RCMS fit from P17/P19.

Then freeze, separately for each survey:

- `Omega_m` to the full-vector RCMS best fit;
- the global BAO scale nuisance to the full-vector RCMS best fit.

At z=0.51 only `A_R` is scanned over the already frozen primary domain:

- DESI: `[-1,+1]`, step `0.01`;
- BOSS: `[-1,+1]`, step `0.005`.

No nuisance is reprofiled in the two-point local subset.

## 5. Primary outputs

For each survey report at z=0.51:

- best local diagnostic `A_R`;
- minimum local chi-square;
- `Delta chi2 <= 1` amplitude interval;
- whether zero lies in the interval;
- boundary contact.

Then report:

- sign agreement between DESI and BOSS local best amplitudes;
- one-sigma profile overlap;
- profile interval gap if disjoint;
- absolute best-amplitude separation.

## 6. Secondary window diagnostic

As a sensitivity check, also evaluate the fixed BOSS redshift span

`0.38 <= z <= 0.61`.

This includes all six BOSS DR12 observables and, for DESI, only the exact z=0.51 pair. The same frozen nuisance state is retained.

This secondary diagnostic cannot override the primary exact-z classification.

## 7. Preregistered classification

### `EXACT_Z_SURVEY_DISCORDANCE`

At z=0.51 the DESI and BOSS best local amplitudes have opposite signs **and** their `Delta chi2 <= 1` intervals do not overlap.

### `EXACT_Z_SURVEY_DIRECTIONAL_TENSION`

The best local amplitudes have opposite signs, but the one-sigma intervals overlap.

### `EXACT_Z_AMPLITUDE_TENSION`

The best amplitudes have the same sign but their one-sigma intervals do not overlap.

### `EXACT_Z_CONCORDANT_WITHIN_DIAGNOSTIC`

The best amplitudes do not have opposite signs and their one-sigma intervals overlap.

### `P20_INVALID`

Full-fit closure, covariance extraction, prediction evaluation, or profile construction fails.

Boundary contact must be reported but does not by itself change the primary label; it limits amplitude interpretation.

## 8. Interpretation boundary

A cross-survey discrepancy at the same redshift would indicate that cosmic epoch alone cannot explain the disagreement. It would not identify whether the cause is model inadequacy, survey systematics, BAO compression, calibration convention, or another survey-specific effect.

Conversely, broad profile overlap would mean the exact-z data are too weak to establish cross-survey discordance.

P20 is the final diagnostic gate before P21. No new RCMS functional form may be generated until this outcome is frozen.
