# RCMS-0.1

## Resolutive Cosmology Mathematical Specification

**Version:** 0.1-draft.2  
**Status:** Candidate-model normative draft  
**Parent specification:** RSMS-1.0-rc.1  
**Author:** Marcelo Roldão Matos  
**ORCID:** 0009-0003-6075-4680  
**Project:** Resolutive Science

> Specialized cosmological hypotheses shall remain distinguishable from inherited mathematical structure and from empirical validation.

---

## Document status

The **Resolutive Cosmology Mathematical Specification (RCMS)** is the specialized specification for cosmological models developed within Resolutive Science.

RCMS inherits the mathematical language, state-space architecture, registry governance, computational conformance rules, versioning discipline, and scientific-integrity requirements of RSMS-1.0-rc.1. It does not alter RSMS identifiers.

RCMS-0.1-draft.2 establishes the cosmological scope and the first dimensionally explicit falsification candidates. It does not claim that a resolutive cosmology is observationally validated.

## Version history

| Version | Date | Status | Description |
|---|---:|---|---|
| 0.1-draft.1 | 2026-08-07 | Initial normative draft | Established RCMS inheritance, observable architecture, baseline comparison, and validation matrix. |
| 0.1-draft.2 | 2026-08-07 | Candidate-model normative draft | Added bounded background-deformation candidates, dimensional requirements, state-evolution test functions, falsification criteria, and synthetic validation battery. |

## 1. Purpose

RCMS shall provide a reproducible mathematical interface between resolutive hypotheses and cosmological observations, with particular attention to:

- cosmological redshift;
- expansion history;
- Type Ia supernova distance measurements;
- baryon acoustic oscillations (BAO);
- cosmic microwave background (CMB) constraints;
- independent cross-probe consistency.

The specification shall distinguish three layers:

1. inherited RSMS structures;
2. cosmology-specific hypotheses and parameters;
3. observable and statistical comparison procedures.

## 2. Inheritance from RSMS

### RC-D001 — Parent specification

RCMS-0.1 inherits **RSMS-1.0-rc.1**. Any RCMS object that uses an RSMS identifier retains the meaning assigned by that RSMS version unless an explicit, governed extension is declared.

### RC-R001 — No silent redefinition

RCMS shall not silently redefine a canonical RSMS state, field, operator, symbol, unit convention, validation category, or identifier.

### RC-R002 — Scientific-status separation

A mathematically consistent RCMS model, a numerically implemented RCMS model, and an empirically supported RCMS model are distinct statuses. No status shall imply a stronger status without the evidence required by RSMS.

## 3. Cosmological domain

### RC-D002 — Cosmological background

A cosmological specialization shall declare a background spacetime and the assumptions used to obtain its large-scale description, including homogeneity, isotropy, curvature, or departures from them when applicable.

For a homogeneous and isotropic baseline, the reference metric may be written

\[
 ds^2=-c^2dt^2+a^2(t)\left[\frac{dr^2}{1-k r^2}+r^2d\Omega^2\right],
\tag{RC-E001}
\]

where \(a(t)\) is the scale factor and \(k\) is the declared spatial-curvature parameter. Equation RC-E001 is a reference background representation, not a claim that resolutive dynamics must reproduce a specific Friedmann law.

### RC-D003 — Cosmological resolutive state

A cosmological model may associate the inherited resolutive state

\[
R=(\rho_R,\Theta_R,\iota_R,\kappa_R)
\tag{RC-E002}
\]

with cosmological evolution only after declaring the map connecting those components to background or perturbative cosmological quantities.

No component of \(R\) shall be identified with redshift, scale factor, curvature density, dark energy, dark matter, or another conventional cosmological quantity by notation alone.

### RC-R003 — Explicit cosmological map

Every proposed coupling between the resolutive state and cosmological observables shall define its domain, codomain, parameters, units, limiting behavior, and observational consequences.

## 4. Observable architecture

### RC-O001 — Cosmological observable map

A cosmological specialization shall define an observable map

\[
\Pi_{\mathrm{cos}}:\mathcal X_{\mathrm{cos}}\rightarrow\mathcal O_{\mathrm{cos}},
\tag{RC-E003}
\]

where \(\mathcal X_{\mathrm{cos}}\) contains the declared cosmological state and model parameters, and \(\mathcal O_{\mathrm{cos}}\) contains the predicted observables.

The minimum validation program shall treat the following probes separately before any joint fit.

### RC-O002 — Redshift

The model shall state whether the observed redshift relation

\[
1+z=\frac{a(t_0)}{a(t_{\mathrm{em}})}
\tag{RC-E004}
\]

is inherited unchanged, recovered as a limit, or replaced by a declared alternative mapping. Any additional resolutive contribution shall be separately identifiable and testable.

### RC-O003 — Expansion history

The model shall predict a quantity comparable to observational expansion-rate constraints, conventionally represented by

\[
H(z)=\frac{\dot a}{a}.
\tag{RC-E005}
\]

If the resolutive model uses another primary evolution variable, the transformation to the observable \(H(z)\) shall be explicit.

### RC-O004 — Supernova distances

For Type Ia supernova comparison, the model shall produce a luminosity distance \(D_L(z)\) or an explicitly equivalent observable and distance modulus

\[
\mu(z)=5\log_{10}\!\left(\frac{D_L(z)}{10\,\mathrm{pc}}\right).
\tag{RC-E006}
\]

Nuisance calibration shall be handled symmetrically between competing models.

### RC-O005 — BAO

A BAO implementation shall declare the exact observable used, such as transverse, radial, isotropic, or jointly reported distance combinations, together with the treatment of the sound horizon \(r_d\). The model shall not claim BAO agreement from a comparison to a non-equivalent compressed quantity.

### RC-O006 — CMB

A CMB comparison shall declare its level of approximation. Background-distance constraints, shift parameters, acoustic-scale summaries, and full angular power spectra are distinct validation levels and shall not be reported as equivalent.

## 5. Baseline comparison program

### RC-T001 — Reference-model baseline

The first RCMS validation battery shall include a conventional flat \(\Lambda\)CDM baseline evaluated on the same data partitions, likelihood definitions, nuisance treatment, and numerical tolerances used for the resolutive candidate.

### RC-T002 — Probe isolation

Redshift/expansion, supernovae, BAO, and CMB constraints shall first be evaluated independently. A joint likelihood may be reported only after the individual residual structure and tensions have been documented.

### RC-T003 — Symmetric model comparison

Model comparison shall report parameter counts and, where applicable, likelihood-based criteria such as

\[
\mathrm{AIC}=2p-2\ln\hat{\mathcal L},
\tag{RC-E007}
\]

and

\[
\mathrm{BIC}=p\ln n-2\ln\hat{\mathcal L},
\tag{RC-E008}
\]

with \(p\) the declared fitted-parameter count and \(n\) the declared effective number of observations. Bayesian evidence may be added when priors and numerical evidence estimation are fully specified.

### RC-T004 — Out-of-sample testing

Where the data structure permits, candidate cosmologies shall be evaluated with withheld observations, independent datasets, or predictive checks rather than only in-sample optimization.

### RC-T005 — Failure reporting

A probe that disfavors or falsifies a resolutive specialization shall be retained in the validation record. Probe selection shall not be conditioned on favorable performance.

## 6. First resolutive hypothesis slot

### RC-H001 — Resolutive modification of cosmological evolution

The first model-specific hypothesis shall be introduced only as an explicit deformation of a declared reference cosmology. A generic architecture is

\[
H_R^2(z)=H_{\mathrm{ref}}^2(z)+\Delta_R(z;\vartheta_R),
\tag{RC-E009}
\]

where \(\Delta_R\) is a resolutive contribution and \(\vartheta_R\) is its declared parameter set.

RC-E009 is an interface for hypothesis construction, not a physical law. Candidate forms for \(\Delta_R\), their dimensional structure, recovery limits, and synthetic falsification requirements are defined in [Chapter 2 — Resolutive Background Deformations](chapters/02_resolutive_background_deformations.md).

### RC-R004 — Reference recovery

Every candidate \(\Delta_R\) shall specify a parameter limit in which the declared reference model is recovered, when such a nested limit is mathematically intended.

### RC-R005 — Discriminating prediction

A candidate resolutive cosmology should identify at least one observable regime in which its prediction differs from the reference model by more than a tunable reparameterization. Without such a regime, empirical discrimination is not established.

## 7. Planned validation matrix

| Stage | Probe | Primary output | Minimum comparison |
|---|---|---|---|
| C1 | Redshift / expansion | \(H(z)\), residuals | Reference cosmology |
| C2 | Type Ia supernovae | \(\mu(z)\), residuals, likelihood | Reference cosmology |
| C3 | BAO | Declared BAO distance ratios | Reference cosmology |
| C4 | CMB | Declared summary or spectrum-level quantities | Reference cosmology |
| C5 | Joint | Combined likelihood and posterior diagnostics | Same probes and priors |
| C6 | Predictive | Held-out / external predictions | Predeclared candidate models |

## 8. Candidate-model chapter

The first dimensionally explicit candidate family is defined in:

- [Chapter 2 — Resolutive Background Deformations](chapters/02_resolutive_background_deformations.md).

The preferred first falsification target is RC-E020. Synthetic tests RC-T006 through RC-T011 shall precede fitting to real cosmological observations.

## 9. Immediate next implementation stage

The next implementation shall:

1. implement a flat \(\Lambda\)CDM reference background and RC-E020 through the same numerical interface;
2. generate null and injected-signal synthetic datasets;
3. test recovery, discrimination, identifiability, numerical stability, and interval calibration;
4. record seeds, tolerances, parameter bounds, and software versions;
5. reject or revise RC-E020 if it fails the synthetic battery before observational fitting.

Until those tests are completed, RC-E020 remains a dimensionally defined candidate rather than a validated cosmological model.
