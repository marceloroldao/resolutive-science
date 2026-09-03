# RCMS Protocol 16 — Preregistered Out-of-Sample Prediction

**Status:** PREREGISTERED / TARGET FROZEN BEFORE RCMS OUTCOME INSPECTION  
**Release line:** v0.3-dev  
**Highest-value final gate of v0.3**

## 1. Purpose

Protocol 16 performs a genuine held-out observational test of the unchanged one-parameter logarithmic RCMS screening surrogate. The target dataset, upstream revision, quantitative prediction, parameter bounds, nuisance policy, and decision criteria are frozen before any RCMS fit to the target is executed.

The frozen surrogate remains

\[
E_{\rm RCMS}^2(z)=\Omega_m(1+z)^3+(1-\Omega_m)+A_R\ln(1+z).
\]

No response-dependent modification is permitted.

## 2. Held-out target

Target: **SDSS-III BOSS DR12 BAO-only consensus** at

\[
z=0.38,\ 0.51,\ 0.61.
\]

The target has not previously been used in the RCMS protocol line of this repository.

Frozen upstream repository:

- repository: `CobayaSampler/bao_data`;
- revision: `bb0c1c9009dc76d1391300e169e8df38fd1096db`;
- data file: `sdss_DR12Consensus_bao.dat`;
- covariance: `BAO_consensus_covtot_dM_Hz.txt`.

The six target measurements contain transverse distance and radial expansion information at three redshifts. The published BOSS fiducial sound horizon is `r_d,fid = 147.78 Mpc`.

The target vector and covariance may be downloaded/verified after this freeze, but no RCMS target fit may be inspected until the intake and Lambda-CDM reproduction gates pass.

## 3. Nuisance and model policy

Both Lambda-CDM and RCMS shall use the same single global BAO scale nuisance. A convenient parameterization is

\[
q=\frac{c}{H_0 r_d}.
\]

For the BOSS DR12 consensus convention,

\[
D_M\frac{r_{d,\rm fid}}{r_d}=q\,r_{d,\rm fid}\int_0^z\frac{dz'}{E(z')},
\]

and

\[
H(z)\frac{r_d}{r_{d,\rm fid}}=\frac{c\,E(z)}{q\,r_{d,\rm fid}}.
\]

The nuisance `q` is profiled symmetrically in both models.

Frozen parameter domains:

- `Omega_m in [0.05, 0.60]`;
- `A_R in [-1.0, +1.0]` for the primary P16 target fit;
- no CMB, SH0ES, external `r_d`, BBN, or other calibration prior.

If the best RCMS fit contacts `A_R=+/-1`, the primary result is classified boundary-limited and no stronger interpretation is allowed without a separately preregistered extension.

## 4. Pre-target quantitative prediction

The prediction is frozen from the pre-target v0.3 evidence record, not from BOSS DR12.

P14's pre-target descriptive common profile gives

\[
A_{\rm pred}=0.264079766
\]

with descriptive `Delta S <= 1` interval

\[
0.121971100\le A_R\le0.407494649.
\]

Therefore P16 freezes the following prediction hierarchy:

### Primary quantitative prediction

The BOSS DR12 best-fit amplitude will lie inside

`0.121971100 <= A_R <= 0.407494649`.

### Directional prediction

The BOSS DR12 best-fit amplitude will be positive.

### Model-selection boundary

No prediction is made that RCMS will beat Lambda-CDM by AIC or BIC. P15 explicitly found `NO_MODEL_SELECTION_PREFERENCE`; P16 must preserve that prior scientific state.

## 5. Intake gate — P16-T0

Before revealing the RCMS target outcome, P16-T0 must:

1. verify the frozen upstream revision/files;
2. verify the 6x6 covariance is symmetric and positive definite;
3. reproduce the declared BOSS data convention and `r_d,fid=147.78 Mpc`;
4. fit flat Lambda-CDM with the global scale nuisance profiled;
5. demonstrate shape identifiability after profiling the global scale;
6. confirm no target RCMS amplitude has been reported by the runner.

Only after T0 passes may T1 reveal `A_R`.

## 6. P16-T1 outputs

Report:

- Lambda-CDM best `Omega_m`, `q`, and chi-square;
- RCMS best `Omega_m`, `q`, `A_R`, and chi-square;
- `Delta chi2`;
- `Delta AIC`;
- BIC only if the 6-observable Gaussian convention is used consistently and explicitly;
- `Delta chi2 <= 1` profile interval for `A_R`;
- boundary contact;
- whether the best fit is inside the frozen quantitative prediction interval;
- whether the sign prediction succeeds.

## 7. Preregistered classification

### `OUT_OF_SAMPLE_QUANTITATIVE_HIT`

Requires:

1. T0 passes;
2. best-fit `A_R` is inside `[0.121971100, 0.407494649]`;
3. best-fit `A_R > 0`;
4. no parameter-boundary contact.

### `OUT_OF_SAMPLE_DIRECTIONAL_ONLY`

T0 passes and best-fit `A_R > 0`, but the quantitative interval is missed or a nonfatal uncertainty limitation prevents the stronger label.

### `OUT_OF_SAMPLE_NULL_COMPATIBLE`

Best fit is non-negative but the profile is centered sufficiently near zero that no directional replication is supported; operationally this label applies when best-fit `A_R >= 0` but `A_R=0` lies inside the `Delta chi2 <= 1` interval and the quantitative interval is missed.

### `OUT_OF_SAMPLE_SIGN_FAILURE`

Best-fit `A_R < 0`.

### `OUT_OF_SAMPLE_INVALID`

Intake/likelihood reproduction fails or the fit is boundary-limited in a way that invalidates the primary classification.

## 8. Non-negotiable rules

- No model modification after target inspection.
- No widened prediction interval after target inspection.
- No added prior/calibration after target inspection.
- No deletion of an unfavorable target result.
- BOSS DR12 is a held-out target for P16 and must remain identified as such in the v0.3 publication record.

## 9. Publication meaning

P16 is an out-of-sample test of a phenomenological late-time surrogate, not a direct test of the full Resolutive Physics ontology. A successful P16 would improve evidence for predictive recurrence of the screening pattern; a failure would be a substantive falsification result and would still complete the v0.3 scientific objective.
