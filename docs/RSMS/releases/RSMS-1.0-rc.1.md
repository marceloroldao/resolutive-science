# RSMS-1.0-rc.1 — Release Candidate Notes

**Release-candidate date:** 2026-08-07  
**Specification:** Resolutive Science Mathematical Specification  
**Version:** 1.0-rc.1  
**Status:** Release candidate for external technical review

---

## Purpose

RSMS-1.0-rc.1 is the first hardened release candidate of the universal Resolutive Science Mathematical Specification. It freezes a reviewable candidate baseline for mathematical, methodological, computational, and specification-level criticism before a stable RSMS-1.0 release is considered.

Release-candidate status is a statement about specification maturity only. It is not experimental validation of Resolutive Physics and is not evidence that any specialized resolutive physical model is correct.

## Included architecture

RC1 contains the complete planned twelve-chapter architecture:

1. Introduction, Scope, and Scientific Principles;
2. Mathematical Conventions and Notation;
3. Primitive Objects and Resolutive State Space;
4. Geometric and Bundle Structure;
5. Fundamental Fields and Operators;
6. Dynamics and Variational Principles;
7. Observables, Projection, and Measurement;
8. Dimensional Structure, Units, and Scaling;
9. Symmetry, Invariance, and Correspondence Principles;
10. Computational Conformance and Validation;
11. Versioning, Extensions, and Deprecation; and
12. Appendices and Symbol Registry.

## Hardening completed before RC1

The pre-RC hardening phase established or verified:

- canonical base-manifold notation `M`;
- state/address separation;
- canonical observable projection ownership under `RS-O001`;
- independent validation categories under `RS-M113`;
- controlled identifier lifecycle and migration rules;
- canonical identifier and symbol registries;
- explicit compatibility of `R`, `\mathcal R_f`, and `\Psi_R` notation;
- automated detection of duplicate identifiers and unresolved stable references;
- Markdown-link and selected malformed-LaTeX checks;
- deterministic machine-readable identifier and symbol registry generation;
- automated GitHub Actions release-readiness auditing; and
- correction of the release-blocking Chapter 5 and Chapter 6 notation/reference defects identified during RC1 hardening.

## Automated audit result

The RC1 branch passed the configured RSMS audit workflow, including:

- cross-chapter audit against the `main` baseline;
- stable-identifier meaning checks;
- generation of **358 machine-readable identifiers**;
- generation of **24 canonical symbol entries**;
- JSON round-trip validation; and
- the release-readiness gate.

These checks establish only that the configured specification-integrity tests passed.

## Compatibility statement

The transition from `1.0-draft.12` to `1.0-rc.1` is intended as a compatible release-status transition after hardening. It does not intentionally reassign any stable identifier or introduce a new universal physical hypothesis.

Any correction made after RC1 shall be compatibility-classified under Chapter 11. A material semantic change may require a subsequent release candidate rather than silent modification of the RC1 citation target.

## External review requested

Reviewers are encouraged to test and criticize, in particular:

- mathematical type consistency;
- global versus local bundle assumptions;
- sufficiency and minimality of the primitive state definition;
- dimensional declarations and scaling rules;
- projection/measurement separation;
- inverse-problem and identifiability language;
- validation and model-comparison requirements;
- symbol and identifier consistency;
- implementability of normative clauses; and
- whether any statement unintentionally overstates the evidential status of a resolutive hypothesis.

A useful criticism need not accept the Resolutive Physics hypotheses. Counterexamples, incompatibilities, ambiguous definitions, failed implementations, and negative empirical comparisons are all scientifically relevant outcomes under the RSMS methodology.

## Immutable citation target

The intended Git tag for this candidate is:

`RSMS-1.0-rc.1`

The tag should point to the final commit containing these RC1 release notes and citation metadata. Once created, that tag shall not be moved. Later corrections shall use a later release candidate or release version.

## Citation metadata

Repository citation metadata is provided in the root `CITATION.cff`. No DOI is assigned by this release note. If an archival DOI is later minted for this exact candidate, it may be added through a traceable metadata-only release record without changing the scientific meaning of the tagged specification.
