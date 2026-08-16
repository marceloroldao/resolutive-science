# Resolutive Science v0.2.0 — Release Notes

Status: **release-candidate audit draft; not yet tagged**

**RSMS compatibility:** `RSMS-1.0-rc.1`

## Scope

v0.2.0 extends the frozen RCMS evidence record through Protocol 08 while preserving the earlier Protocol 01–03 evidence and all scientifically relevant weak, null, negative, and conditional outcomes.

No experimental material from `resolutiva-reformulacao` is imported into this release.

## Evidence added or consolidated

- **P04 — independent shape replication:** `INDEPENDENT_SHAPE_DIRECTIONAL_ONLY`. Positive multi-redshift direction, with substantial LRG sensitivity and insufficient robustness for a stronger claim.
- **P05 — LRG-dependence challenge:** `POSITIVE_BUT_WEAK`. The best fit remains positive after the challenge, but zero remains compatible and complexity penalties favor the simpler model.
- **P06 — DESI DR2 external replication:** `DESI_DR2_POSITIVE_DIRECTIONAL`. Independent DESI DR2 data reproduce a positive direction with best-fit `A_R = 0.210244178`; negative Delta AIC prevents a model-preference claim.
- **P07 — cross-protocol consistency:** `COMMON_POSITIVE_COMPATIBLE`. Descriptive synthesis gives `A_R = 0.211141330`; overlapping evidence is not treated as statistically independent and no combined discovery significance is claimed.
- **P08 — logarithmic provenance:** `LOG_FORM_CONDITIONALLY_DERIVED`. Under continuity and additive drift with multiplicative scale composition, the logarithmic form follows mathematically. The scale-composition premise remains an explicit hypothesis rather than a derived physical law.

## Consolidated interpretation

Across the frozen RCMS screenings, the unchanged one-parameter surrogate repeatedly selects a positive deformation direction. The v0.2.0 record treats this as a reproducible directional pattern, not as experimental validation, discovery significance, or proof that RCMS is preferred over Lambda-CDM.

The evidence remains mixed in precisely the scientifically relevant sense: positive directional recurrence coexists with sensitivity tests, zero-compatible challenges, and unfavorable or weak complexity-penalized comparisons. These limiting results are frozen as part of the release rather than removed or retuned.

## Claims boundary

v0.2.0 does **not** claim:

- experimental validation of Resolutive Physics;
- discovery of new physics;
- global statistical preference of RCMS over Lambda-CDM;
- a combined discovery significance from P07;
- derivation of the logarithmic term from a fundamental Resolutive Master Equation;
- physical establishment of the P08 scale-composition hypothesis.

## Reproducibility and release audit

The release branch includes an automated audit gate covering RSMS structural consistency, frozen v0.2.0 release markers, P07 consistency regression, and P08 provenance regression. The release audit is intended to detect accidental scientific/documentary drift before tagging.

See `REPRODUCIBILITY.md` and `docs/releases/v0.2.0_EVIDENCE_MATRIX.md` for the reproduction contract and consolidated evidence boundary.

## Licensing

The repository uses a noncommercial licensing model for the covered material. Academic, educational, and research use must follow the repository license terms; commercial exploitation requires the applicable commercial authorization/license. The project must not be represented as OSI Open Source where the commercial-use restriction applies.

## Citation and archival metadata

Author: Marcelo Roldão Matos  
ORCID: `0009-0003-6075-4680`

`CITATION.cff` will be advanced to v0.2.0 only at the final release freeze. The Zenodo DOI assigned to v0.2.0 must then be incorporated into the repository citation metadata and README.

## Publication gate

Tagging `v0.2.0` and Zenodo deposition are permitted only after the publication checklist is fully satisfied and no release-blocking inconsistency remains.
