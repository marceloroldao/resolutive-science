# RCMS Observational Protocol 01 — Low-Redshift Pre-registration

**Protocol version:** 0.1  
**Status:** Pre-observational methodological protocol  
**Parent specification:** RCMS-0.1-draft.2  
**Inherited specification:** RSMS-1.0-rc.1  
**Author:** Marcelo Roldão Matos  
**Date frozen:** 2026-08-08

---

## 1. Purpose

This protocol freezes the first observational comparison of the RCMS low-redshift expansion candidate before real-data residuals are inspected for model development.

Its purpose is to reduce researcher degrees of freedom. After this protocol is merged, changes to the tested functional form, probe order, parameter accounting, inclusion rules, nuisance treatment, or primary decision metrics constitute a new protocol version and shall not be presented as the original pre-registered test.

This protocol does not assert that Resolutive Cosmology is validated and does not define a fundamental resolutive law.

## 2. Frozen primary candidate

The primary observational screening model is the one-parameter effective RCMS deformation

\[
H_{\mathrm{eff}}^2(z)=H_{\Lambda\mathrm{CDM}}^2(z)+H_0^2 A_R\ln(1+z).
\tag{RC-PROT01-E001}
\]

The additional RCMS parameter is \(A_R\).

The null/reference model is flat \(\Lambda\)CDM, recovered at

\[
A_R=0.
\tag{RC-PROT01-E002}
\]

### 2.1 Scientific role of the effective model

RC-PROT01-E001 is a **detection surrogate** derived from the low-signal behavior of RC-E020. It is not declared to replace the full RC-E020 physical candidate.

The synthetic program preceding this protocol found that the full two-parameter RC-E020 candidate produced only a small additional reduction in \(\chi^2\) and did not compensate for its second parameter under AIC or BIC in the tested regime. Therefore the first observational screening uses the more identifiable one-parameter surrogate.

A later analysis of the full RC-E020 form shall be labeled a separate model-comparison stage and shall not be substituted post hoc if the primary screening result is unfavorable.

## 3. Frozen parameter accounting

### 3.1 Parameters common to both models

The following cosmological or nuisance quantities shall be treated symmetrically in the reference and RCMS models whenever the corresponding probe is included:

- \(H_0\);
- \(\Omega_m\) under the flat late-time reference background;
- one supernova absolute-calibration/intercept nuisance, or its likelihood-equivalent treatment;
- the BAO sound-horizon scale \(r_d\), unless the selected public likelihood supplies an explicitly different calibrated treatment that is applied identically to both models.

Any additional nuisance parameter required by an adopted public likelihood shall be introduced identically in both models and documented before model comparison.

### 3.2 RCMS-specific parameter

The primary RCMS model has exactly one additional fitted parameter:

\[
A_R.
\]

No redshift-dependent spline, phase function, additional drift coefficient, probe-specific RCMS amplitude, or dataset-specific deformation parameter is allowed in Protocol 01.

## 4. Probe order

Observational analyses shall be executed and retained in the following predeclared order:

1. \(H(z)\) / expansion-history data alone;
2. Type Ia supernovae alone;
3. BAO alone;
4. \(H(z)+\) supernovae;
5. \(H(z)+\) BAO;
6. supernovae + BAO;
7. \(H(z)+\) supernovae + BAO.

The same model definition shall be used in every stage.

The probe-isolated results shall remain in the final record even when the joint analysis is emphasized.

## 5. CMB exclusion from Protocol 01

CMB data are not part of this first low-redshift pre-registration.

Reason: the current RCMS candidate is a late-time background deformation. A full CMB analysis requires explicit early-universe dynamics, radiation content, recombination assumptions, perturbation evolution, and a consistent sound-horizon calculation. Introducing those ingredients only after examining low-redshift results would mix distinct hypothesis stages.

CMB testing shall therefore require a separate pre-registered RCMS protocol.

## 6. Dataset inclusion requirements

Before any likelihood result is interpreted, every observational input shall satisfy the following requirements:

1. public or independently auditable provenance;
2. a stable citation and dataset/version identifier where available;
3. redshift and measured observable values available in machine-readable form;
4. uncertainties and covariance information used when supplied by the source;
5. documented units and conversions;
6. documented treatment of duplicate or overlapping measurements;
7. no point removed because of its residual under either tested model;
8. any quality cut shall be based on source metadata or a criterion fixed before model residuals are inspected;
9. checksums or content hashes shall be stored for ingested files when technically feasible.

If a dataset cannot satisfy the covariance or provenance requirements needed for a claimed statistical interpretation, it may be retained only as an explicitly exploratory secondary check.

## 7. Redshift-domain rule

The analysis shall use the documented valid redshift domain of each selected low-redshift dataset. A new redshift cut shall not be selected by searching for the interval that maximizes RCMS preference.

If an externally motivated redshift restriction is required, its reason and value shall be recorded before fitting both models.

## 8. Likelihood and residual treatment

The preferred analysis shall use the source-provided likelihood or covariance structure when available.

For Gaussian data products, the generic statistic is

\[
\chi^2=(\mathbf d-\mathbf m)^T C^{-1}(\mathbf d-\mathbf m),
\tag{RC-PROT01-E003}
\]

with the same covariance treatment for both models.

Residual diagnostics shall be retained by probe and redshift. An aggregate improvement shall not conceal a coherent degradation in an individual probe.

## 9. Primary model-comparison metrics

The primary reported quantities are:

- maximum-likelihood or minimum-\(\chi^2\) values;
- \(\Delta\chi^2\) relative to flat \(\Lambda\)CDM;
- AIC;
- BIC;
- fitted \(A_R\) with an uncertainty or likelihood/profile interval appropriate to the implemented method;
- fitted common cosmological and nuisance parameters;
- residual summaries by probe.

For

\[
\Delta\chi^2=\chi^2_{\Lambda\mathrm{CDM}}-\chi^2_{\mathrm{RCMS}},
\]

positive values indicate improved raw fit by RCMS before complexity penalty.

AIC and BIC shall count the RCMS model as having one additional parameter relative to the reference model under Protocol 01.

## 10. Decision categories

The first observational result shall be classified conservatively rather than described with discovery language.

### RC-PROT01-D001 — No preference

Use **no preference** when the penalized criteria do not consistently favor RCMS, when the inferred amplitude is compatible with the null within its declared uncertainty, or when improvements are unstable across probes.

### RC-PROT01-D002 — RCMS screening signal

Use **RCMS screening signal** only when all of the following hold:

1. \(A_R\) is consistently displaced from zero under the declared inference procedure;
2. the joint fit improves beyond the one-parameter complexity penalty;
3. the improvement is not produced solely by one visibly pathological subset;
4. common nuisance parameters remain within physically and observationally admissible ranges;
5. leave-one-subset-out or other prespecified robustness diagnostics do not erase the result.

This category is a motivation for independent testing, not validation of Resolutive Physics.

### RC-PROT01-D003 — Reference favored

Use **reference favored** when AIC/BIC or predictive diagnostics consistently favor flat \(\Lambda\)CDM, or when the RCMS amplitude is driven to the null while adding no reproducible predictive value.

### RC-PROT01-D004 — Inconclusive/systematics-limited

Use **inconclusive/systematics-limited** when model preference changes materially under justified covariance, calibration, or dataset-provenance choices that cannot be resolved within the available data.

## 11. Anti-tuning rule

After real-data residuals for Protocol 01 have been inspected, none of the following may be changed and still be called the same pre-registered test:

- the functional dependence \(A_R\ln(1+z)\);
- the number of RCMS-specific parameters;
- the primary probe order;
- the primary AIC/BIC/\(\Delta\chi^2\) reporting requirements;
- inclusion/exclusion rules;
- nuisance symmetry between models;
- parameter bounds for the purpose of selectively improving RCMS, unless the original bounds are demonstrated to be computationally invalid for both models.

Any scientifically justified revision shall create Protocol 02 or a later version. Results from Protocol 01 shall remain archived.

## 12. Parameter-bound policy

Numerical parameter ranges shall be set before production fitting and shall be wide enough that the optimum is not artificially pinned to a boundary.

If an optimum reaches a boundary, the analysis shall report that fact. Expanding a boundary for numerical adequacy is allowed only symmetrically and shall be recorded. Repeated boundary changes selected to improve the RCMS result are nonconforming.

## 13. Robustness checks fixed in advance

At minimum, the production analysis shall include:

1. per-probe fits in the order of Section 4;
2. joint fit;
3. inspection of standardized residuals versus redshift;
4. leave-one-probe-out joint fits;
5. numerical-tolerance stability;
6. parameter-boundary inspection;
7. comparison of fitted nuisance values between reference and RCMS models;
8. a null-recovery test using a synthetic dataset matched approximately to the selected real-data redshift/error structure;
9. an injected-signal recovery test using the same structure.

When covariance matrices are available, synthetic tests should preserve their correlation structure where practical.

## 14. Reporting unfavorable results

All primary Protocol 01 results shall be retained regardless of outcome. In particular:

- a null result shall not be omitted;
- a dataset that disfavors RCMS shall not be removed without an independent quality reason;
- tension between probes shall be reported;
- a post hoc alternative RCMS functional form shall be reported separately from Protocol 01.

## 15. Reproducibility record

The production run shall record:

- repository commit SHA;
- exact input dataset files and hashes;
- data-source citations;
- preprocessing scripts;
- model implementation paths;
- likelihood implementation paths;
- parameter bounds and starting values or grids;
- software and dependency versions;
- numerical tolerances;
- random seeds when randomness is used;
- machine-generated result tables before interpretive editing.

## 16. Pre-observational freeze statement

At the time of this protocol, the RCMS development program has used synthetic data to select and stress-test the one-parameter effective screening model. Those synthetic studies indicated that the full two-parameter RC-E020 form did not earn its additional parameter under the tested AIC/BIC comparisons and that \(H(z)\) carried most of the synthetic discrimination, with supernova data providing useful complementary information.

Protocol 01 freezes the next stage before production observational residuals are used to alter the candidate.

Any future model revision based on real-data behavior shall be explicitly versioned as a subsequent hypothesis and evaluated using an independent or appropriately held-out validation strategy.
