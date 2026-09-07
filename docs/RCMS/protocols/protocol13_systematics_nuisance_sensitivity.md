# RCMS Protocol 13 — Systematics and Nuisance Sensitivity

**Status:** PREREGISTERED / FROZEN BEFORE EXECUTION  
**Release line:** v0.3-dev  
**Parent release:** v0.2.0 — DOI `10.5281/zenodo.22002018`  
**Frozen surrogate:**

\[
H_{\mathrm{eff}}^2(z)=H_{\Lambda\mathrm{CDM}}^2(z)+H_0^2 A_R\ln(1+z).
\]

## 1. Purpose

Protocol 13 tests whether the positive RCMS screening direction is fragile to a small, preregistered set of scientifically defensible covariance and nuisance choices already represented by frozen release-relevant datasets.

This protocol is not an optimization exercise. All branches below are frozen before outcome inspection and all outcomes, including branches that weaken, null, or reverse the RCMS direction, must be reported.

## 2. Primary test bed

The primary P13 test bed is the frozen DESI DR2 13-observable BAO vector and covariance used by Protocols 06, 09-T1, 10, and 11.

The baseline likelihood is the same Gaussian likelihood with:

- full 13x13 covariance;
- profiled global BAO scale `q = c/(H0*r_d)`;
- fitted `Omega_m` in `[0.05,0.60]`;
- fitted `A_R` in `[-1,+1]` for sensitivity-map comparison;
- no CMB, SH0ES, external sound-horizon calibration, or additional physical parameter.

## 3. Frozen sensitivity branches

Exactly the following branches shall be evaluated.

### B0 — Full covariance baseline

Use the frozen 13x13 DESI DR2 covariance unchanged.

### B1 — Diagonal-only covariance diagnostic

Set all off-diagonal covariance terms to zero while preserving the published diagonal variances.

This branch is explicitly a diagnostic and is not promoted as the preferred physical likelihood.

### B2 — Correlation-strength half diagnostic

Preserve all variances and replace each off-diagonal term by 0.5 times its baseline value:

\[
C^{(1/2)}_{ij}=\begin{cases}
C_{ii}, & i=j,\\
0.5 C_{ij}, & i\ne j.
\end{cases}
\]

Positive definiteness must be checked before fitting.

### B3 — Leave-lowest-redshift-observable-pair-out

Remove every DESI DR2 BAO observable at the minimum redshift present in the frozen vector, preserving the corresponding covariance submatrix.

### B4 — Leave-highest-redshift-observable-pair-out

Remove every DESI DR2 BAO observable at the maximum redshift present in the frozen vector, preserving the corresponding covariance submatrix.

### B5 — Radial-only subset

Use only observables labeled `DH_over_rs`, with the corresponding covariance submatrix.

### B6 — Transverse/volume subset

Use all non-`DH_over_rs` observables (`DM_over_rs` and `DV_over_rs`) with the corresponding covariance submatrix.

No other cuts, rescalings, priors, covariance manipulations, or nuisance changes may be added after execution begins.

## 4. Quantities to report for every branch

For each branch report:

- number of retained observables;
- best-fit `A_R`;
- best-fit `Omega_m`;
- profiled `q`;
- RCMS minimum chi-square;
- Lambda-CDM minimum chi-square at `A_R=0`;
- `Delta chi2 = chi2_LCDM - chi2_RCMS`;
- `Delta AIC = AIC_LCDM - AIC_RCMS` using one additional RCMS parameter;
- profile `Delta chi2 <= 1` interval for `A_R`;
- whether zero lies in that interval;
- boundary contact flag;
- covariance positive-definiteness diagnostics where applicable.

## 5. Preregistered classification

Let `B0` denote the baseline full-covariance best-fit sign.

### `SYSTEMATICS_STABLE_POSITIVE`

All conditions must hold:

1. baseline `A_R > 0`;
2. at least 5 of the 6 non-baseline branches have `A_R > 0`;
3. no branch with at least 5 retained observables has a best fit `A_R < -0.05`;
4. no numerical/covariance failure invalidates more than one branch.

### `SYSTEMATICS_SENSITIVE`

Assigned if the baseline is positive but the stable-positive criteria fail without a coherent sign reversal across a majority of branches.

### `SYSTEMATICS_SIGN_REVERSAL`

Assigned if at least 4 of the 6 non-baseline branches have `A_R < 0`.

### `SYSTEMATICS_INDETERMINATE`

Assigned if more than one branch is invalid because of numerical or covariance failure.

These labels describe robustness only. They do not establish model preference or physical validation.

## 6. Scientific boundaries

- P13 shall not alter the logarithmic functional form.
- P13 shall not introduce CMB, SH0ES, or an external `r_d` prior.
- Diagonal or half-correlation covariance branches are stress diagnostics, not replacements for the official full covariance.
- A branch with `A_R>0` is not counted as independent evidence.
- The full sensitivity map must be preserved, not just the most favorable branch.

## 7. Advancement rule

After the complete P13 sensitivity map is frozen, proceed to P14 amplitude stability regardless of whether P13 passes or fails. A P13 failure is a publishable falsification outcome and must not trigger retuning of the surrogate.
