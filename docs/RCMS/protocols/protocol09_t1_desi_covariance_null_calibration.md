# RCMS Protocol 09 T1 — DESI DR2 Covariance Null Calibration

**Status:** PREREGISTERED — outcome not inspected  
**Release line:** v0.3-dev  
**RSMS compatibility:** RSMS-1.0-rc.1  
**Parent:** P09-T0 `CALIBRATION_PASS`

## 1. Purpose

P09-T1 tests whether the frozen RCMS inference procedure remains statistically calibrated when synthetic null data are generated with the frozen correlated DESI DR2 BAO covariance structure used by the v0.2 evidence line.

The physical deformation remains frozen:

\[
H_{\mathrm{eff}}^2(z)=H_{\Lambda\mathrm{CDM}}^2(z)+H_0^2A_R\ln(1+z),
\]

with null truth

\[
A_R=0.
\]

Passing T1 does not validate RCMS; it only tests whether correlated observational covariance causes the pipeline to manufacture a positive deformation direction.

## 2. Frozen observational structure

Use exactly:

- `data/rcms/desi_dr2_bao_all_mean.txt` for the 13-point redshift/observable layout;
- `data/rcms/desi_dr2_bao_all_cov.txt` for the frozen 13x13 covariance;
- observable kinds `DV_over_rs`, `DM_over_rs`, and `DH_over_rs` exactly as recorded;
- the same BAO scale nuisance `q=c/(H0*r_d)` profiled analytically;
- the same matter-density range `0.05 <= Omega_m <= 0.60`.

The observed DESI residual vector must not be injected into the null generator.

## 3. Null generator

First determine the deterministic LCDM reference mean by fitting the frozen DESI DR2 sampling structure with `A_R=0`, profiling `Omega_m` and `q` exactly as in the frozen BAO runner.

Each synthetic realization is then

\[
d_i = \mu_i^{\Lambda\mathrm{CDM}} + \epsilon_i,
\qquad
\epsilon\sim\mathcal N(0,C_{\rm DESI}).
\]

Only the sampling structure and covariance are inherited from DESI DR2. The empirical residuals of the real dataset are not reused.

## 4. Frozen Monte Carlo configuration

- final scientific realizations: `N = 5000`;
- master seed: `20260820`;
- development smoke test: `N = 500`, same seed, not a scientific outcome;
- `A_R` search interval: `[-1.0,+1.0]`;
- `A_R` grid spacing: `0.01`;
- `Omega_m` search interval: `[0.05,0.60]`;
- `Omega_m` grid spacing: `0.005`;
- `q` is profiled analytically for every `(Omega_m,A_R)` template and every realization;
- no fitted realization may be silently discarded.

The finite grid is part of the preregistered estimator. It must not be refined after outcome inspection to improve calibration statistics.

## 5. Confidence and false-positive construction

For each realization, profile over `Omega_m` and `q` and retain the minimum chi-square as a function of `A_R`.

Define:

- best-fit `A_hat` as the grid value with minimum profiled chi-square;
- two-sided 95% confidence set by `Delta chi2 <= 3.841458820694124`;
- one-sided positive 95% false positive when `A_hat > 0` and `Delta chi2(A_R=0) >= 2.705543454095404`;
- boundary hit when `A_hat` equals either frozen A_R search endpoint.

## 6. Primary metrics

Report:

1. mean and median `A_hat`;
2. standard deviation of `A_hat`;
3. `B = abs(mean(A_hat))/std(A_hat)`;
4. fraction `A_hat > 0`;
5. one-sided 95% false-positive rate;
6. 95% null coverage;
7. `A_R` boundary-hit rate;
8. fit-failure rate;
9. empirical quantiles of `Delta chi2(A_R=0)`;
10. fitted-null reference values of `Omega_m` and `q` used by the generator.

## 7. Preregistered gates

### Calibration pass

T1 passes if all hold:

- `B <= 0.10`;
- `0.47 <= fraction(A_hat > 0) <= 0.53`;
- `0.035 <= one-sided FPR95 <= 0.065`;
- `0.92 <= coverage95 <= 0.98`;
- boundary-hit rate `<= 0.01`;
- fit-failure rate `<= 0.01`.

### Calibration warning

If `B <= 0.10`, coverage and failure gates pass, but either sign fraction or one-sided FPR lies outside its nominal band, classify `CALIBRATION_WARNING` and preserve the result before any methodological follow-up.

### Calibration fail

Classify `CALIBRATION_FAIL` if any of the following holds:

- `B > 0.10`;
- coverage outside `[0.92,0.98]`;
- boundary-hit rate `> 0.01`;
- fit-failure rate `> 0.01`.

## 8. Interpretation rule

A T1 pass means the tested correlated-covariance pipeline does not obviously manufacture the positive v0.2 direction under a DESI-like null ensemble. It does not establish that the real-data positive direction is physical.

A warning or failure must not trigger a change to the RCMS logarithmic equation. The failed calibration remains part of the v0.3 evidence record.

## 9. Required artifacts

- deterministic runner;
- machine-readable summary JSON;
- realization table or deterministic regeneration procedure;
- hashes of scientific outputs;
- frozen outcome report;
- GitHub Actions workflow;
- explicit record of N, seed, grids, covariance source, and classification.
