# RCMS Protocol 06 — DESI DR2 External Multi-Redshift Replication

**Status:** Preregistered before any Protocol 06 RCMS fit  
**RSMS compatibility:** RSMS-1.0  
**Parent evidence:** Protocols 01–05  

## 1. Purpose

Protocol 06 tests whether the frozen RCMS background surrogate is recovered in an external multi-redshift BAO dataset from DESI DR2, rather than by rearranging eBOSS DR16 tracer blocks.

The scientific question is intentionally narrow:

> Does DESI DR2 BAO shape information independently prefer the same positive RCMS direction when the same one-parameter surrogate and symmetric global BAO-scale nuisance treatment are used?

## 2. Frozen model

The tested RCMS surrogate remains

\[
E_{\rm RCMS}^2(z)=\Omega_m(1+z)^3+(1-\Omega_m)+A_R\ln(1+z).
\]

The null model is exactly

\[
A_R=0.
\]

No new exponent, transition redshift, spline, tracer-dependent coefficient, or dataset-specific RCMS parameter may be introduced.

## 3. Dataset frozen for the primary statistic

Primary dataset: the public DESI DR2 combined BAO likelihood for all tracers as distributed by the Cobaya BAO data package.

Frozen upstream representation:

- measurements: `desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt`;
- covariance: `desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt`;
- measurement blob SHA: `8aff444fdb42c0946342aa0011ab287eda097c4c`;
- covariance blob SHA: `fd8e5697ab61379b07b52efb781ea6713417a4d9`;
- observables: `DV_over_rs`, `DM_over_rs`, and `DH_over_rs` over multiple redshifts;
- no eBOSS DR16 observation is included in the Protocol 06 primary statistic.

The upstream combined vector contains 13 measurements spanning approximately `z=0.295` to `z=2.33`.

## 4. Frozen nuisance policy

A single global dimensionless BAO scale nuisance is used symmetrically under Lambda-CDM and RCMS:

\[
q \equiv \frac{c}{H_0 r_d}.
\]

For a flat background,

\[
D_M/r_d=q\int_0^z\frac{dz'}{E(z')},
\]

\[
D_H/r_d=\frac{q}{E(z)},
\]

and

\[
D_V/r_d=q\left[\frac{z}{E(z)}\left(\int_0^z\frac{dz'}{E(z')}\right)^2\right]^{1/3}.
\]

No external CMB, BBN, SH0ES, sound-horizon, or absolute calibration is introduced.

## 5. Frozen parameter domains

For continuity with Protocols 04–05:

- `Omega_m in [0.10, 0.50]`;
- `q in [20, 45]`;
- `A_R in [-5, 5]` only after P06-T0 passes.

## 6. P06-T0 — acquisition, upstream-likelihood, and identifiability gate

P06-T0 must be executed without evaluating `A_R` and must print `RCMS_PARAMETER_EVALUATED=NO`.

Required checks:

1. download the exact frozen measurement and covariance blobs;
2. verify their Git blob SHAs;
3. verify 13 measurements and a finite positive-definite 13x13 covariance matrix;
4. fit flat Lambda-CDM in `(Omega_m,q)`;
5. require the best fit not to lie on a frozen parameter boundary;
6. profile `q` over a fixed `Omega_m` scan and require a profile span of at least `Delta chi2 = 4` across the full frozen `Omega_m` domain.

If any gate fails, Protocol 06 stops before exposing `A_R`.

## 7. P06-T1 — external RCMS reveal

Only after P06-T0 passes, fit the exact same data with `A_R` free.

Record:

- null and RCMS minimum chi-square;
- best-fit `Omega_m`, `q`, and `A_R`;
- `Delta chi2 = chi2_null - chi2_RCMS`;
- `Delta AIC = AIC_null - AIC_RCMS`;
- profile interval in `A_R` at `Delta chi2 <= 1`;
- optimizer convergence and boundary diagnostics.

## 8. Frozen directional classification

The Protocol 06 reveal is classified as one of:

- `DESI_DR2_POSITIVE_SUPPORTED`: best-fit `A_R>0`, profile excludes zero at `Delta chi2<=1`, and `Delta AIC>2`;
- `DESI_DR2_POSITIVE_DIRECTIONAL`: best-fit `A_R>0`, but zero remains in the profile or complexity-penalized support is not strong enough;
- `DESI_DR2_NULL_COMPATIBLE`: best fit is near zero and the profile is compatible with zero without meaningful positive preference;
- `DESI_DR2_SIGN_REVERSAL`: best-fit `A_R<0` and the profile excludes zero;
- `DESI_DR2_NOT_IDENTIFIABLE`: the fit cannot identify `A_R` after nuisance profiling;
- `INCONCLUSIVE_PROTOCOL06`: technical/statistical limitations prevent a defensible classification.

## 9. Anti-tuning rule

After this preregistration is merged, no change to the RCMS functional form, parameter domains, DESI DR2 primary data vector, covariance, nuisance asymmetry, or calibration policy may be made in response to the observed P06 result.

Any later alternative model belongs to a new protocol/version and must preserve Protocol 06 unchanged.

## 10. Interpretation boundary

Protocol 06 is a cosmological surrogate test. Even a positive result would not by itself validate the full Resolutive Physics ontology.

Mathematical consistency, numerical reproducibility, observational fit, independent replication, model selection, and physical validation remain distinct stages.
