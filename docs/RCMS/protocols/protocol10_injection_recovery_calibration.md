# RCMS Protocol 10 — Injection/Recovery Calibration

**Status:** PREREGISTERED — outcomes not inspected  
**Release line:** v0.3-dev  
**RSMS compatibility:** RSMS-1.0-rc.1  
**Parent evidence:** P09-T0 `CALIBRATION_PASS`, P09-T1 `CALIBRATION_PASS`

## 1. Purpose

Protocol 10 tests whether the frozen RCMS DESI-BAO inference machinery can recover known injected deformation amplitudes without material bias, sign inversion, or severe uncertainty miscalibration.

The surrogate remains frozen:

\[
H_{\mathrm{eff}}^2(z)=H_{\Lambda\mathrm{CDM}}^2(z)+H_0^2 A_R\ln(1+z).
\]

P10 is a measurement-calibration protocol, not observational evidence for RCMS.

## 2. Frozen observational structure

Use the same DESI DR2 BAO sampling and 13x13 covariance frozen for P09-T1:

- `data/rcms/desi_dr2_bao_all_mean.txt`
- `data/rcms/desi_dr2_bao_all_cov.txt`

Synthetic means are generated from the RCMS template itself, not from observed residuals.

The nuisance reference is fixed at the P09-T1 null-reference values:

- `Omega_m = 0.295`
- `q = 29.468025096`

Only `A_R` is varied as injection truth.

## 3. Injection grid and Monte Carlo freeze

Final scientific injections:

`A_R,true = [-0.40, -0.20, 0.00, +0.20, +0.40]`

For each truth value:

- `N = 2000` realizations;
- master seed = `20260821`;
- deterministic child seed = `master_seed + injection_index` in the listed order;
- total final ensemble size = `10000` realizations.

Development smoke tests may use smaller N but are not scientific outcomes.

## 4. Frozen estimator

Use the same estimator family as P09-T1:

- `A_R` fit grid: `[-1.0,+1.0]`, step `0.01`;
- `Omega_m` nuisance grid: `[0.05,0.60]`, step `0.005`;
- BAO scale `q` profiled analytically;
- same DESI covariance inverse for generator and fitter;
- no post-outcome retuning of grids, bounds, nuisance treatment, or confidence thresholds.

## 5. Primary metrics per injected amplitude

For each truth value report:

1. `mean(A_hat)`;
2. median `A_hat`;
3. standard deviation;
4. raw bias `mean(A_hat)-A_true`;
5. standardized ensemble bias
   `B_inj = abs(mean(A_hat)-A_true)/std(A_hat)`;
6. 95% profile-likelihood coverage of the injected truth using `DeltaChi2 <= 3.841458820694124`;
7. sign-recovery probability for nonzero injections;
8. boundary-hit rate;
9. fit-failure rate.

Also fit the descriptive calibration relation

\[
\langle \hat A_R\rangle = \alpha + \beta A_{R,\mathrm{true}}
\]

across the five injection points.

## 6. Preregistered calibration gates

### Per-injection bias

- `B_inj <= 0.10`: pass;
- `0.10 < B_inj <= 0.20`: warning;
- `B_inj > 0.20`: fail.

### Per-injection 95% coverage

- `[0.92,0.98]`: pass;
- `[0.90,0.92)` or `(0.98,0.99]`: warning;
- outside `[0.90,0.99]`: fail.

### Sign recovery

For `|A_true| = 0.20`:

- `>= 0.75`: pass;
- `[0.65,0.75)`: warning;
- `< 0.65`: fail.

For `|A_true| = 0.40`:

- `>= 0.95`: pass;
- `[0.90,0.95)`: warning;
- `< 0.90`: fail.

The zero injection has no sign-recovery gate; its sign symmetry remains descriptive because P09 already calibrates the null.

### Global linearity

For the five-point calibration relation:

- `abs(alpha) <= 0.03`;
- `0.90 <= beta <= 1.10`.

Violation of either global linearity bound is a calibration failure.

### Numerical integrity

At every injection:

- boundary-hit rate must be `<= 0.01`;
- fit-failure rate must be `<= 0.01`.

Exceeding either bound is a failure.

## 7. Overall classification

- `RECOVERY_PASS`: all hard gates pass and no warning band is entered;
- `RECOVERY_WARNING`: no hard failure, but at least one warning band is entered;
- `RECOVERY_FAIL`: any hard failure occurs.

A failed P10 result must be preserved. The RCMS equation must not be changed to rescue recovery.

## 8. Prohibited changes after final outcome inspection

Do not silently change:

- injection amplitudes;
- N;
- seeds;
- covariance;
- nuisance reference;
- fitting grids/bounds;
- confidence construction;
- sign-recovery thresholds;
- bias/coverage thresholds;
- RCMS logarithmic functional form.

Any necessary change requires an explicit versioned amendment preserving the original outcome.

## 9. Advancement criterion

P11 equal-complexity functional controls may proceed after P10 is frozen whether P10 passes, warns, or fails. A failure changes the interpretation of later protocols and must remain visible in the v0.3 evidence record.
