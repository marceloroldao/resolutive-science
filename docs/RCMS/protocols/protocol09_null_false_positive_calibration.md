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

Two levels are required:

1. **T0 — controlled diagonal-noise calibration:** transparent one-parameter null calibration in the normalized additive deformation channel. This tests sign symmetry, interval coverage, false-positive calibration, deterministic seeding, and boundary handling. It does **not** claim to reproduce the full Pantheon+/BAO likelihood or nuisance structure.
2. **T1 — release-relevant covariance calibration:** synthetic observations generated under the nested null using a frozen observational sampling/covariance structure already documented in the repository. This is the first test intended to exercise a release-relevant covariance/likelihood structure.

T1 must not begin until T0 code, metrics, thresholds, seeds, and outcome are frozen.

## 4. Exact frozen T0 design

The T0 observable is the normalized residual in the additive deformation channel,

\[
y_i = A_R\,x_i + \epsilon_i,
\qquad
x_i=\ln(1+z_i),
\]

with null truth `A_R = 0`.

The exact design is frozen as follows before the final outcome is executed:

- redshift grid: 64 equally spaced points on `z in [0.05, 2.00]` including both endpoints;
- design vector: `x_i = ln(1 + z_i)`;
- Gaussian independent errors: `epsilon_i ~ Normal(0, sigma_i^2)`;
- uncertainty law: `sigma_i = 0.06 + 0.02 z_i`;
- generator truth: `A_R = 0`;
- Monte Carlo realizations: `N = 10000` for the scientific run;
- master seed: `20260818` using NumPy `default_rng` / PCG64;
- fitting interval: `A_R in [-1.0, +1.0]`;
- no nuisance parameters in T0;
- estimator: weighted least squares in the one-parameter channel;
- unconstrained estimator:

\[
\hat A_R = \frac{\sum_i w_i x_i y_i}{\sum_i w_i x_i^2},
\qquad
w_i=\sigma_i^{-2};
\]

- reported bounded estimate: unconstrained estimate clipped to `[-1,+1]`; boundary-hit frequency is reported;
- nominal standard error before clipping:

\[
\sigma_{\hat A}=\left(\sum_iw_ix_i^2\right)^{-1/2};
\]

- two-sided 95% interval: `A_hat_unbounded +/- 1.959963984540054 * sigma_A`;
- one-sided positive 95% false positive: `A_hat_unbounded / sigma_A > 1.6448536269514722`;
- profile-improvement statistic under this Gaussian T0:

\[
\Delta\chi^2_0=(\hat A_R/\sigma_{\hat A})^2.
\]

The final scientific run must use exactly this configuration unless a protocol amendment is committed **before** its output is inspected.

## 5. Monte Carlo execution rules

- `N = 10000` is the only scientific T0 outcome;
- smaller runs are implementation smoke tests only;
- all 10000 realizations use the same fixed grid and uncertainty law;
- failed/non-finite realizations are counted and reported, not silently discarded;
- the scientific JSON summary must include the exact configuration and deterministic SHA256 of the realization-level CSV output;
- the full realization table may be regenerated deterministically from the frozen runner, but the workflow should preserve it as an artifact when practical.

## 6. Primary metrics

For recovered amplitudes under the null, report:

1. mean of the unbounded recovered amplitude;
2. median recovered amplitude;
3. standard deviation;
4. fraction with `A_hat_unbounded > 0`;
5. one-sided false-positive rate at nominal 95% confidence;
6. two-sided 95% interval coverage for `A_R = 0`;
7. boundary-hit frequency for the reported bounded estimator;
8. numerical/non-finite failure rate;
9. empirical quantiles of `DeltaChi2_0` at 50%, 90%, 95%, 99%;
10. mean-bias diagnostic `B = abs(mean(A_hat))/std(A_hat)`.

Where the estimator is symmetric and correctly calibrated, `P(A_hat > 0)` is expected to be near 0.5. This sign fraction alone is not a discovery false-positive rate.

## 7. Preregistered interpretation bands

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

### One-sided 95% false-positive rate

- `0.04 <= FPR <= 0.06`: nominal calibration band;
- `0.03 <= FPR < 0.04` or `0.06 < FPR <= 0.07`: mild miscalibration requiring documentation;
- outside `[0.03, 0.07]`: calibration failure.

## 8. Falsification / stop rules

P09-T0 is considered a pipeline calibration failure if any of the following occurs in the final preregistered run:

- `B > 0.10`;
- 95% null coverage lies outside `[0.92, 0.98]`;
- one-sided nominal-95% false-positive rate lies outside `[0.03, 0.07]`;
- numerical/non-finite failure rate exceeds 1%;
- a material sign asymmetry is observed and cannot be explained by a preregistered boundary effect.

If T0 fails, do not tune the RCMS equation. Diagnose the inference implementation or synthetic generator, preserve the failed result, and repeat only under a new explicitly versioned protocol amendment.

Passing P09-T0 does not validate RCMS. It only establishes that this controlled statistical core does not obviously manufacture a positive direction under the null. Release-relevant inference calibration is deferred to P09-T1.

## 9. Required artifacts

The final P09-T0 record must contain:

- runner script;
- fixed seed and configuration;
- machine-readable JSON summary;
- realization-level CSV or deterministic regeneration instructions;
- SHA256 of the CSV output;
- frozen Markdown outcome report;
- environment/dependency record;
- automated smoke/regression test where practical.

## 10. Prohibited changes after outcome inspection

After the first final N=10000 outcome is produced, do not silently change:

- the seed;
- N;
- redshift grid;
- uncertainty law;
- estimator;
- fitting bounds;
- confidence-interval construction;
- significance threshold;
- interpretation bands;
- failure criteria;
- null generator;
- RCMS logarithmic functional form.

Any scientifically necessary change requires a documented amendment and preservation of the original result.

## 11. Advancement criterion

P10 injection/recovery may proceed after P09-T0 is computationally complete and its outcome is frozen, regardless of whether P09 passes or fails. A P09 failure must remain visible in the v0.3 evidence record and may itself become a central v0.3 result.
