# RCMS Protocol 02 — Low-Redshift Robustness and Independent Replication

**Status:** Pre-registered before Protocol 02 execution  
**Relationship to Protocol 01:** Follow-up robustness protocol; no modification of the Protocol 01 deformation  
**Primary objective:** Attempt to falsify or de-stabilize the positive \(A_R\approx0.19\) region observed in the Protocol 01 SN+BAO and full low-redshift fits

---

## 1. Frozen model under test

Protocol 02 retains exactly the Protocol 01 effective screening deformation:

\[
H_{\mathrm{eff}}^2(z)=H_{\Lambda\mathrm{CDM}}^2(z)+H_0^2 A_R\ln(1+z).
\]

No new redshift dependence, probe-specific term, extra RCMS coefficient, or post-hoc correction is permitted in this protocol.

The null/reference model is flat \(\Lambda\)CDM, recovered at \(A_R=0\).

## 2. Frozen parameter bounds

Unless a test is explicitly a likelihood-only re-evaluation with an existing optimizer, all fits retain the Protocol 01 parameter domain:

- \(40\le H_0\le100\) km s\(^{-1}\) Mpc\(^{-1}\);
- \(0.05\le\Omega_m\le0.60\);
- \(-5\le A_R\le5\).

BAO retains a free common scale \(q=c/(H_0r_d)\), with no CMB or external sound-horizon prior.

Pantheon+ remains no-SH0ES and analytically marginalizes the additive intercept direction.

## 3. Tests frozen before execution

### T1 — Numerical reproducibility

Run the full Protocol 01 combination with two independent deterministic optimization paths:

1. the existing production optimizer;
2. an independent coarse-grid + local-refinement implementation.

Pass condition: best-fit \(A_R\), \(\Omega_m\), and \(\Delta\chi^2\) agree within declared numerical tolerances.

### T2 — DESI jackknife by measurement block

For each BAO measurement block declared from the frozen DESI DR2 vector, remove one complete block at a time and refit the full \(H(z)+\)SN+BAO combination.

The block partition must be derived only from the fixed BAO observable/redshift labels before any jackknife result is inspected.

Report for every omission:

- best-fit \(A_R\);
- profile interval;
- \(\Delta\chi^2\);
- \(\Delta\mathrm{AIC}\);
- \(\Delta\mathrm{BIC}\).

Robustness warning condition: sign reversal of best-fit \(A_R\), contact with parameter bounds, or collapse of the likelihood improvement to \(\Delta\chi^2<1\) in multiple single-block omissions.

### T3 — Supernova redshift split

Use a fixed split at \(z_{\rm CMB}=0.3\), chosen before execution to create a simple low/high-redshift diagnostic rather than optimize significance.

Evaluate:

- low-z Pantheon+ subset + BAO;
- high-z Pantheon+ subset + BAO;
- full H(z)+ each SN subset + BAO.

The Pantheon+ covariance must be subset consistently from the frozen full covariance.

Report whether the fitted \(A_R\) sign and magnitude are mutually compatible.

### T4 — Covariance ablation diagnostic

Repeat the full combination with diagonal-only covariance separately for:

1. Pantheon+;
2. DESI BAO;
3. both simultaneously.

These are diagnostics only and are not substitutes for the production full-covariance result.

Large movement of \(A_R\) relative to the full-covariance profile is evidence of covariance sensitivity.

### T5 — Null Monte Carlo calibration

Generate synthetic observations under the best-fit flat \(\Lambda\)CDM null using the frozen covariance models for H(z), Pantheon+, and BAO.

For each realization, fit both nested models with the same Protocol 02 pipeline and record:

\[
\Delta\chi^2=\chi^2_{\Lambda\mathrm{CDM}}-\chi^2_{\mathrm{RCMS}}.
\]

Initial production target: 500 deterministic Monte Carlo realizations with a frozen RNG seed sequence.

Primary calibration statistic:

\[
p_{\rm MC}=\frac{1+N(\Delta\chi^2_{\rm sim}\ge4.559528)}{1+N_{\rm sim}}.
\]

The observed threshold 4.559528 is frozen from the Protocol 01 full combination and must not be changed after simulations begin.

### T6 — Residual localization

At the full-combination best fits for both models, report per-probe and redshift-binned residual contributions without changing the likelihood.

Purpose: determine whether the RCMS likelihood gain is broad or concentrated in a small observational region.

No bin discovered after looking at residuals may be promoted to a new fit in Protocol 02.

## 4. Decision framework

Protocol 02 does **not** redefine model selection. Protocol 01 remains inconclusive.

The robustness label will be one of:

- **ROBUST_SIGNAL_REGION:** positive \(A_R\) remains stable across T1–T4, null calibration is uncommon under \(\Lambda\)CDM, and no single residual block dominates the improvement;
- **FRAGILE_SIGNAL_REGION:** positive \(A_R\) depends strongly on one subset, covariance treatment, or numerical path;
- **NULL_COMPATIBLE:** Monte Carlo calibration shows the observed improvement is common under the null and/or the signal collapses across predeclared ablations;
- **INCONCLUSIVE_ROBUSTNESS:** mixed diagnostics without a stable classification.

These labels are robustness statements about the frozen one-parameter surrogate, not empirical validation of Resolutive Cosmology.

## 5. Anti-overfitting guardrails

During Protocol 02:

- no change to \(A_R\ln(1+z)\);
- no new RCMS parameter;
- no tuning of the redshift split;
- no removal of an observation because it weakens RCMS;
- no change to the Monte Carlo observed threshold;
- no replacement of AIC/BIC conventions after seeing results;
- no incorporation of CMB, SH0ES, RSD, or an external \(r_d\) prior.

Any model revision must occur only in a separately named and pre-registered later protocol.

## 6. Execution order

The implementation should be committed before any Protocol 02 observational output is inspected. Execution order is frozen as:

1. T1 numerical reproducibility;
2. T2 DESI block jackknife;
3. T3 SN redshift split;
4. T4 covariance ablation;
5. T5 null Monte Carlo calibration;
6. T6 residual localization;
7. consolidated Protocol 02 report.

## 7. Protocol 01 anchor values

The following values are carried forward only as frozen reference targets, not as tunable goals:

\[
A_R^{\rm P01}=0.187021,
\qquad
\Delta\chi^2_{\rm P01}=4.559528,
\]

with profile interval

\[
0.098671\le A_R\le0.276779.
\]

Protocol 02 is explicitly designed to challenge these values.