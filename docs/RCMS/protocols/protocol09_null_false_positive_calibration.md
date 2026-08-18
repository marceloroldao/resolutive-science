# RCMS Protocol 09 — Null False-Positive Calibration

**Status:** PREREGISTERED — outcome not inspected  
**Release line:** v0.3-dev  
**RSMS compatibility:** RSMS-1.0-rc.1  
**Parent scientific release:** v0.2.0 — DOI 10.5281/zenodo.22002018

## 1. Purpose

Protocol 09 asks whether the frozen RCMS inference pipeline can generate an apparently positive deformation amplitude when the data-generating process contains no RCMS deformation.

The null hypothesis is fixed as

\[
H_0: A_R = 0.
\]

The RCMS screening surrogate remains unchanged from v0.2.0:

\[
H_{\mathrm{eff}}^2(z)=H_{\Lambda\mathrm{CDM}}^2(z)+H_0^2 A_R\ln(1+z).
\]

No functional change is permitted after synthetic outcomes are inspected.

## 2. Primary scientific question

If observations are generated under Lambda-CDM / the nested null with `A_R = 0`, how frequently does the frozen inference procedure return a positive or apparently significant RCMS amplitude?

P09 is a calibration/falsification protocol. It is not evidence for RCMS even if the pipeline is well calibrated.

## 3. Synthetic-data design

The first P09 implementation must use a deterministic synthetic design with preregistered seeds and must preserve, as closely as practical, the redshift sampling and covariance/noise structure of a frozen release-relevant observational target without using the observed residuals to tune the generator.

Two levels are required:

1. **T0 — controlled diagonal-noise calibration:** synthetic observations generated from the nested null with fixed redshift grid and preregistered Gaussian uncertainties. This validates the statistical machinery in a transparent environment.
2. **T1 — release-relevant covariance calibration:** synthetic observations generated under the nested null using a frozen observational sampling/covariance structure already documented in the repository. No post-outcome covariance modification is allowed.

T1 must not begin until T0 code, metrics, thresholds, and seeds are frozen.

## 4. Frozen Monte Carlo rules for T0

- generator truth: `A_R = 0`;
- number of Monte Carlo realizations: `N = 10000` for the final T0 report;
- development smoke tests may use smaller N but cannot be reported as the scientific outcome;
- master random seed: `20260818`;
- fitting interval for `A_R`: `[-1.0, +1.0]` unless an inherited frozen fitter requires a narrower interval, in which case that inherited bound must be documented before execution;
- all realizations use the same preregistered estimator and nuisance treatment;
- failed numerical fits are counted and reported, not silently discarded.

## 5. Primary metrics

For recovered amplitudes `A_hat` under the null, report:

1. mean bias: `mean(A_hat)`;
2. median recovered amplitude;
3. standard deviation / robust spread;
4. fraction with `A_hat > 0`;
5. one-sided false-positive rate at nominal 95% confidence;
6. two-sided 95% interval coverage for `A_R = 0`;
7. fit-failure rate;
8. empirical quantiles of the test statistic / profile improvement used by the frozen fitter.

Where the estimator is symmetric and correctly calibrated, `P(A_hat > 0)` is expected to be near 0.5. This sign fraction alone is not a discovery false-positive rate; significance thresholds must be evaluated separately.

## 6. Preregistered interpretation bands

These bands are calibration diagnostics, not physical discovery thresholds.

### Sign symmetry

For N=10000:

- `0.485 <= P(A_hat > 0) <= 0.515`: nominally symmetric;
- outside this interval: investigate estimator/generator bias before using the pipeline for v0.3 inference.

### Mean-bias diagnostic

Define

`B = abs(mean(A_hat)) / std(A_hat)`.

- `B <= 0.05`: negligible ensemble bias;
- `0.05 < B <= 0.10`: small bias requiring documentation;
- `B > 0.10`: calibration failure requiring investigation.

### 95% coverage

- `0.94 <= coverage <= 0.96`: nominal calibration band;
- `0.92 <= coverage < 0.94` or `0.96 < coverage <= 0.98`: mild miscalibration requiring documentation;
- coverage outside `[0.92, 0.98]`: calibration failure.

The exact confidence-interval construction must be frozen in the runner before the final N=10000 execution.

## 7. Falsification / stop rules

P09-T0 is considered a pipeline calibration failure if any of the following occurs in the final preregistered run:

- `B > 0.10`;
- 95% null coverage lies outside `[0.92, 0.98]`;
- numerical fit-failure rate exceeds 1%;
- a material sign asymmetry is observed and cannot be explained by a preregistered boundary effect.

If T0 fails, do not tune the RCMS equation. Diagnose the inference implementation or synthetic generator, preserve the failed result, and repeat only under a new explicitly versioned protocol amendment.

Passing P09 does not validate RCMS. It only establishes that the tested pipeline does not obviously manufacture the v0.2 positive direction under a controlled null.

## 8. Required artifacts

The final P09-T0 record must contain:

- runner script;
- fixed seed and configuration;
- machine-readable summary;
- optional full realization table or deterministic regeneration instructions;
- SHA256 hashes for scientific output artifacts;
- frozen Markdown outcome report;
- environment/dependency record;
- automated regression test for deterministic summary quantities where practical.

## 9. Prohibited changes after outcome inspection

After the first final N=10000 outcome is produced, do not silently change:

- the seed;
- N;
- estimator;
- fitting bounds;
- confidence-interval construction;
- interpretation bands;
- failure criteria;
- null generator;
- RCMS logarithmic functional form.

Any scientifically necessary change requires a documented amendment and preservation of the original result.

## 10. Advancement criterion

P10 injection/recovery may proceed after P09-T0 is computationally complete and its outcome is frozen, regardless of whether P09 passes or fails. A P09 failure must remain visible in the v0.3 evidence record and may itself become a central v0.3 result.
