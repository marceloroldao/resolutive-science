# RCMS-0.1

## Resolutive Cosmology Mathematical Specification

**Version:** 0.1-draft.1  
**Status:** Initial specialized draft  
**Parent specification:** RSMS-1.0-rc.1  
**Author:** Marcelo Roldão Matos  
**ORCID:** 0009-0003-6075-4680  
**Project:** Resolutive Science

> Specialized cosmological hypotheses shall inherit RSMS definitions and remain distinguishable from empirical validation claims.

---

## 1. Purpose and scientific boundary

RCMS specializes the universal RSMS architecture for cosmology. Its purpose is to define a reproducible mathematical framework in which resolutive cosmological hypotheses can be compared with standard cosmological descriptions using equivalent observational information and declared statistical criteria.

RCMS does not assume that Resolutive Cosmology is empirically correct. A resolutive construction remains a hypothesis until its predictions are confronted with data under the validation rules inherited from RSMS Chapters 7 and 10.

### RC-A001 — Parent-specification inheritance

RCMS shall inherit the active definitions, notation, identifier governance, reproducibility requirements, and scientific-status boundaries of RSMS-1.0-rc.1 unless an explicit controlled specialization is declared.

### RC-A002 — Symmetric cosmological comparison

Comparisons with ΛCDM or other cosmological models shall use equivalent datasets, nuisance treatment, calibration assumptions, parameter accounting, priors, likelihood definitions, and statistical criteria unless a difference is explicitly documented and justified.

### RC-A003 — No validation by construction

Recovery of a known cosmological relation, successful numerical integration, or agreement with a selected observable shall not by itself be described as empirical validation of the full resolutive cosmological model.

---

## 2. Cosmological observable domain

The first RCMS validation program targets five observational sectors:

1. cosmological redshift;
2. expansion history;
3. baryon acoustic oscillations (BAO);
4. cosmic microwave background (CMB) compressed observables and, in later versions, full likelihoods;
5. Type Ia supernova distance measurements.

### RC-D001 — Cosmological background

A cosmological specialization shall declare a background state

\[
\mathcal B_C = \{M,g,\mathcal R_f,\mathcal P_C\},
\tag{RC-E001}
\]

where `M`, `g`, and `\mathcal R_f` inherit their RSMS roles and `\mathcal P_C` is the declared set of cosmological parameters and nuisance quantities.

### RC-D002 — Scale factor

The dimensionless scale factor is denoted by

\[
a(t), \qquad a(t_0)=1.
\tag{RC-E002}
\]

### RC-D003 — Cosmological redshift

The operational redshift variable is

\[
1+z \equiv a^{-1}
\tag{RC-E003}
\]

for the homogeneous background convention. Any resolutive correction to the mapping between emitted and observed frequency shall be introduced as a separate testable specialization rather than silently absorbed into this definition.

### RC-D004 — Expansion rate

The background expansion rate is

\[
H(t) \equiv \frac{\dot a}{a},
\qquad H(z)=H[a(z)].
\tag{RC-E004}
\]

RCMS does not yet prescribe a universal resolutive Friedmann equation. Competing dynamical closures shall be separately identified and compared.

---

## 3. Resolutive cosmological state

### RC-D005 — Cosmological resolutive state

At background level, the cosmological resolutive state is represented by a specialization of the RSMS state,

\[
R_C(t)=\bigl(\rho_R(t),\Theta_R(t),\iota_R(t),\kappa_R(t)\bigr).
\tag{RC-E005}
\]

This equation defines state bookkeeping only. It does not assert that all four components are independently observable or dynamically necessary.

### RC-D006 — Observable projection

Cosmological observables are generated through a declared specialization of the RSMS projection operator,

\[
\Pi_C:\{\mathcal B_C,R_C\}\longrightarrow \mathcal O_C,
\tag{RC-E006}
\]

with

\[
\mathcal O_C \supseteq
\{z,H(z),D_M(z),D_H(z),D_L(z),D_A(z),r_d,\mu(z)\}.
\tag{RC-E007}
\]

Every implemented projection shall declare its domain, parameters, units, numerical procedure, and limiting behavior.

---

## 4. Baseline geometric observables

The following relations define the initial background-observable layer and are not unique predictions of Resolutive Cosmology.

### RC-D007 — Hubble distance

\[
D_H(z)=\frac{c}{H(z)}.
\tag{RC-E008}
\]

### RC-D008 — Line-of-sight comoving distance

For a declared background expansion function,

\[
D_C(z)=c\int_0^z\frac{dz'}{H(z')}.
\tag{RC-E009}
\]

### RC-D009 — Transverse comoving distance

The transverse distance `D_M` shall be obtained from `D_C` using the declared spatial-curvature convention. Flat-background tests use

\[
D_M(z)=D_C(z).
\tag{RC-E010}
\]

### RC-D010 — Angular-diameter distance

\[
D_A(z)=\frac{D_M(z)}{1+z}.
\tag{RC-E011}
\]

### RC-D011 — Luminosity distance

Under metric distance duality,

\[
D_L(z)=(1+z)D_M(z)=(1+z)^2D_A(z).
\tag{RC-E012}
\]

A resolutive model predicting violation of this relation shall expose that violation as an explicit falsifiable hypothesis.

### RC-D012 — Supernova distance modulus

\[
\mu(z)=5\log_{10}\!\left(\frac{D_L(z)}{\mathrm{Mpc}}\right)+25.
\tag{RC-E013}
\]

Absolute-magnitude/calibration degeneracies shall be treated explicitly in likelihood comparisons.

---

## 5. BAO interface

### RC-D013 — Sound horizon at drag epoch

The drag-epoch sound horizon is denoted `r_d`. RCMS implementations shall state whether `r_d` is calculated from an early-universe model, externally calibrated, or treated as a fitted/nuisance parameter.

### RC-D014 — BAO observables

The initial BAO interface shall support at least

\[
\frac{D_M(z)}{r_d},
\qquad
\frac{D_H(z)}{r_d},
\qquad
\frac{D_V(z)}{r_d},
\tag{RC-E014}
\]

where

\[
D_V(z)=\left[zD_H(z)D_M^2(z)\right]^{1/3}.
\tag{RC-E015}
\]

Covariance matrices shall be used when supplied by the dataset.

---

## 6. CMB interface

### RC-D015 — CMB validation levels

CMB comparison shall be divided into explicit levels:

- **Level C1:** background/derived compressed quantities;
- **Level C2:** distance-prior or acoustic-scale likelihoods;
- **Level C3:** full angular-power-spectrum calculation and likelihood.

A model passing C1 shall not be described as having passed C2 or C3.

### RC-D016 — Acoustic-scale interface

Where physically defined by the specialization, the acoustic angular scale may be represented by

\[
\theta_* = \frac{r_s(z_*)}{D_M(z_*)},
\tag{RC-E016}
\]

with all recombination and sound-horizon assumptions declared. This is an interface definition, not yet a complete resolutive perturbation theory.

---

## 7. First resolutive dynamical hypothesis slot

The initial RCMS deliberately separates kinematics from dynamics.

### RC-H001 — Resolutive expansion closure

A candidate resolutive cosmological dynamics shall define

\[
H_R^2(z)=H_0^2\,\mathcal E_R^2
\bigl(z;R_C,\mathcal P_C\bigr),
\tag{RC-E017}
\]

where `\mathcal E_R` is dimensionless and shall be specified by each candidate closure.

This equation is a schema, not a validated law.

### RC-R001 — ΛCDM recovery test

A candidate closure intended as an extension of standard background cosmology shall state whether a parameter limit exists such that

\[
\mathcal E_R^2(z)\longrightarrow
\Omega_r(1+z)^4+\Omega_m(1+z)^3+\Omega_k(1+z)^2+\Omega_\Lambda.
\tag{RC-E018}
\]

If no such limit exists, the model shall be classified as an alternative rather than a continuous extension.

### RC-R002 — Dimensional consistency

Every term entering `H_R^2` shall have dimensions of inverse time squared before normalization, and every exponent or logarithm shall have a dimensionless argument.

---

## 8. Validation matrix

The first computational battery shall report sectors independently before any joint score.

| Sector | Primary quantities | Initial comparison |
|---|---|---|
| Redshift | `z`, frequency/scale-factor mapping | standard background mapping vs explicit resolutive alternative |
| Expansion | `H(z)`, distances | cosmic chronometers and declared expansion datasets |
| BAO | `D_M/r_d`, `D_H/r_d`, `D_V/r_d` | covariance-aware likelihood |
| CMB | `\theta_*`, distance/acoustic quantities | C1 first; C2/C3 only when physically implemented |
| Supernovae | `\mu(z)` | covariance-aware SN Ia likelihood with calibration treatment |

### RC-T001 — Sector isolation

A candidate model shall first be tested separately in each observational sector. Failure in one sector shall not be hidden by aggregate improvement in another.

### RC-T002 — Joint likelihood

A joint cosmological fit may be reported only after dataset overlap, covariance, nuisance parameters, calibration assumptions, and shared parameters are documented.

### RC-T003 — Baseline models

At minimum, the same computational pipeline shall support a flat ΛCDM baseline. Additional comparisons may include curved ΛCDM, wCDM, CPL, or other declared alternatives where scientifically appropriate.

### RC-T004 — Model complexity

Comparisons shall report goodness of fit together with model complexity using declared criteria such as AIC and BIC; Bayesian evidence shall be reported only when priors and evidence computation are explicitly documented.

### RC-T005 — Out-of-sample robustness

Where dataset structure permits, sensitivity to calibration choices, subsets, redshift ranges, and alternative data compilations shall be reported.

---

## 9. Computational traceability

Every RCMS result intended for publication shall record:

- exact RCMS and RSMS versions;
- code commit;
- dataset identifiers and source versions;
- preprocessing steps;
- parameter definitions and priors/bounds;
- random seeds where applicable;
- optimizer/sampler configuration;
- covariance treatment;
- convergence diagnostics;
- numerical tolerances;
- generated tables/figures;
- failed as well as successful validation sectors.

### RC-C001 — Reproducible cosmology run

A quantitative cosmology claim is computationally conforming only when the inputs and execution metadata are sufficient for an independent implementation to reproduce the reported numerical result within declared tolerances.

---

## 10. Open scientific questions for draft.2

The next RCMS revision shall not assume answers to the following questions:

1. What explicit evolution equations govern `R_C(t)`?
2. Does the resolutive phase `\Theta_R` affect homogeneous expansion, perturbations, or only a deeper state description?
3. Is the proposed `4\pi` phase periodicity cosmologically observable, and if so through which discriminating observable?
4. Does `\rho_R` behave as a new degree of freedom, an effective geometric quantity, or a reparameterization of known components?
5. How are early-universe perturbations, recombination, and the CMB power spectra derived rather than phenomenologically fitted?
6. Can a single resolutive parameterization fit SN + BAO + expansion + CMB constraints without dataset-specific retuning?

These are research questions, not established properties.

---

## 11. Planned RCMS progression

- `0.1-draft.1`: scope, inheritance, observables, baseline distances, BAO/CMB interfaces, validation rules;
- `0.1-draft.2`: explicit candidate resolutive background dynamics and limiting cases;
- `0.1-draft.3`: likelihood/data interfaces and reproducible benchmark implementation;
- `0.2`: perturbation architecture and CMB consistency requirements;
- `1.0`: only after cross-dataset validation, audit, compatibility review, and release hardening.
