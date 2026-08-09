# RCMS Protocol 03 — External Replication and Prospective Prediction

**Status:** Pre-registered before Protocol 03 execution  
**Relationship to Protocol 02:** External replication follow-up; no modification of the frozen Protocol 01/02 deformation  
**Primary objective:** Test whether the positive low-redshift RCMS screening region replicates in observational datasets that were not used as the primary discovery set in Protocols 01–02.

---

## 1. Frozen model

Protocol 03 retains exactly

\[
H_{\mathrm{eff}}^2(z)=H_{\Lambda\mathrm{CDM}}^2(z)+H_0^2 A_R\ln(1+z).
\]

No new redshift dependence, probe-specific RCMS coefficient, additional RCMS parameter, or post-hoc correction is permitted.

The reference model remains flat \(\Lambda\)CDM, recovered at \(A_R=0\).

## 2. Frozen Protocol 02 context

Protocol 02 closed with the label `INCONCLUSIVE_ROBUSTNESS`.

The carried-forward anchors are descriptive only:

\[
A_R^{\rm P01}=0.187021,
\qquad
\Delta\chi^2_{\rm P01}=4.559528,
\qquad
p_{\rm MC}^{\rm P02}=0.03592814.
\]

Protocol 03 shall not optimize new dataset choices, cuts, or likelihood details to reproduce these anchors.

## 3. External replication datasets

### P03-DATA-SN — DES supernova sample

The primary external supernova replication target is the public Dark Energy Survey supernova release associated with the DES-SN five-year / Dovekie cosmology analysis.

Requirements:

- use the public cosmology data product and released covariance/likelihood information;
- do not combine Pantheon+ observations into the primary replication statistic;
- marginalize or profile the absolute supernova calibration symmetrically between models;
- preserve all published quality selections unless the upstream likelihood itself requires an explicitly documented transformation.

### P03-DATA-BAO — DESI-independent DES Y6 angular BAO

The preferred external BAO replication target is the DES Year 6 angular BAO measurement constructed from sky area excluding overlap with DESI.

Requirements:

- use the public measurement and covariance/likelihood released with that analysis;
- retain the same angular-BAO observable definition used by the upstream analysis;
- do not import DESI DR2 BAO measurements into the primary external replication statistic;
- any sound-horizon or global scale nuisance shall be treated symmetrically between reference and RCMS models and documented before execution.

### P03-DATA-HZ — expansion-history replication

A third external expansion-history dataset may be added only if its measurements are not a simple duplicate or direct superset of the 15-point Moresco covariance-compatible table used in Protocol 01.

If no sufficiently independent H(z) compilation with auditable covariance is available, this stage shall be recorded as unavailable rather than approximated with duplicated observations.

## 4. Frozen execution stages

### P03-T1 — DES supernova replication

Fit flat \(\Lambda\)CDM and the frozen one-parameter RCMS surrogate to the external DES supernova likelihood.

Report:

- best-fit \(A_R\);
- profile interval;
- \(\Delta\chi^2\);
- \(\Delta\mathrm{AIC}\);
- \(\Delta\mathrm{BIC}\) when an effective observation count is well-defined;
- boundary contacts and nuisance estimates.

### P03-T2 — DESI-independent angular BAO replication

Apply the same frozen model pair to the DES Y6 angular BAO likelihood outside the DESI overlap region.

Report the same model-comparison quantities as applicable.

### P03-T3 — external joint replication

Combine only the independent DES supernova and DESI-independent DES angular BAO likelihoods.

The joint fit shall share the cosmological shape parameters and the single \(A_R\) coefficient while preserving probe-specific nuisances.

No Pantheon+, DESI DR2 BAO, CMB, SH0ES, or Protocol 01/02 observation may enter the primary P03-T3 statistic.

### P03-T4 — directional consistency test

Without changing the fit, compare the sign and magnitude of the external best-fit \(A_R\) with the Protocol 01/02 region.

This is not a requirement that the point estimate equal 0.187021. The test asks whether independent data prefer a compatible positive deformation or instead prefer zero/negative values.

### P03-T5 — prospective prediction record

Before incorporating any later cosmological release not already used in Protocols 01–03, record the RCMS prediction implied by the frozen posterior/profile from the completed external replication.

At minimum, the prediction record shall state:

- the sign of the expected deformation relative to flat \(\Lambda\)CDM;
- the predicted redshift dependence through \(A_R\ln(1+z)\);
- the parameter interval propagated from the completed Protocol 03 fit;
- the exact future observable or dataset class against which the prediction can be tested.

No future dataset may be described as a prospective prediction test if it was inspected before the prediction record was committed.

## 5. Replication decision framework

Protocol 03 will use one of the following labels:

- **EXTERNAL_REPLICATION_SUPPORTED:** the independent joint fit prefers \(A_R>0\), its uncertainty region is compatible with the Protocol 01/02 positive region, and no declared external probe shows a strong sign conflict;
- **EXTERNAL_REPLICATION_NULL:** the independent joint fit is compatible with \(A_R=0\) and provides no meaningful preference for the RCMS surrogate;
- **EXTERNAL_REPLICATION_CONFLICT:** the independent data prefer a materially incompatible or negative \(A_R\) region;
- **EXTERNAL_REPLICATION_INCONCLUSIVE:** the external probes are individually weak or mutually inconsistent without a stable classification.

These are replication labels for the frozen phenomenological surrogate. They are not validation of Resolutive Cosmology or proof of a fundamental resolutive law.

## 6. Anti-overfitting guardrails

During Protocol 03:

- no change to \(A_R\ln(1+z)\);
- no additional RCMS parameter;
- no redshift cut chosen from residuals;
- no removal of an external observation because it weakens RCMS;
- no Pantheon+ or DESI DR2 contribution to the primary external replication statistic;
- no CMB/SH0ES prior added after inspecting external results;
- no change of model-selection convention after results are known;
- all external data revisions, file hashes, masks, and covariance choices must be frozen before fitting.

Any revised physical model must be assigned to a later, separately preregistered protocol.

## 7. Execution order

1. freeze upstream data revisions and file hashes for DES supernovae;
2. freeze upstream data revisions and file hashes for DESI-independent DES Y6 angular BAO;
3. implement and validate the DES-SN likelihood against an upstream reference result;
4. execute P03-T1;
5. implement and validate the angular-BAO likelihood against an upstream reference result;
6. execute P03-T2;
7. execute P03-T3 external joint replication;
8. execute P03-T4 directional consistency;
9. issue the Protocol 03 consolidated report;
10. if warranted, commit P03-T5 prospective prediction before any later dataset is inspected.
