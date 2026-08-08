# RSMS-1.0 RC1 Release-Readiness Report

**Assessment date:** 2026-08-07  
**Baseline:** RSMS-1.0-draft.12  
**Target:** RSMS-1.0-rc.1  
**Status:** Not yet ready for RC1 tagging  
**Assessment type:** Specification hardening and release-readiness audit

---

## 1. Purpose

This report records the release-readiness state of RSMS-1.0 after completion of the planned twelve-chapter normative-draft architecture. It evaluates specification integrity only. It does not evaluate or claim empirical validation of Resolutive Physics.

The applicable release-readiness requirement is RS-Z019. Versioning, compatibility, and migration requirements are governed by Chapter 11.

## 2. Current strengths

The following structural milestones are complete or implemented in the RC1 hardening branch:

- all twelve planned RSMS chapters exist;
- the parent specification is synchronized to `1.0-draft.12`;
- stable identifier lifecycle rules exist;
- a canonical identifier registry exists;
- a canonical symbol registry exists;
- the `R` / `\mathcal R_f` / `\Psi_R` relationship is explicitly governed by RS-Z010;
- state and address are separated normatively;
- validation categories remain separated from implementation and scientific acceptance;
- computational conformance and reproducibility requirements are defined;
- release-readiness requirements are defined by Chapter 12;
- automated static auditing is available through `tools/audit_rsms.py`;
- deterministic machine-readable registry generation is implemented in `tools/build_rsms_registries.py`;
- GitHub Actions executes the cross-chapter audit, registry generation, JSON validation, and release-readiness audit on RSMS changes.

## 3. Release blockers

The following findings shall be resolved before `RSMS-1.0-rc.1` is tagged.

### RC1-B001 — Incorrect composition cross-reference in Chapter 5

`RS-F023 — Composition` states that evaluation order follows `RS-D006`. The canonical composition convention is `RS-N006`; `RS-D006` defines the observable space.

**Required correction:** replace the cross-reference to `RS-D006` with `RS-N006` without altering the mathematical meaning of RS-F023.

**Classification:** editorial/cross-reference defect; no intended scientific change.

### RC1-B002 — Historical base-manifold notation remains in Chapter 6

Chapter 3 establishes `M` as the canonical base spacetime manifold. Chapter 6 still uses `\mathcal M` in multiple scope and formula contexts for the same base object.

**Required correction:** migrate those occurrences to `M` where they refer to the canonical base manifold, while preserving unrelated uses of `\mathcal M` that denote a statistical/model object in other chapters or scopes.

**Classification:** notation harmonization; intended semantics unchanged.

### RC1-B003 — Malformed Gamma notation in Chapter 5

At least one expression contains the malformed source form `\Gamma\(TM\)` rather than `\Gamma(TM)`.

**Required correction:** repair malformed LaTeX tokens and scan the chapter for equivalent replacement damage.

**Classification:** editorial/LaTeX defect.

## 4. Machine-readable registry status

The former registry hardening item is now substantially implemented:

- `tools/build_rsms_registries.py` deterministically generates `identifiers.json` from normative headings/equation tags and `symbols.json` from Appendix B;
- duplicate identifier assignments stop generation;
- generated registries carry specification/version metadata and source provenance;
- the CI workflow generates both registries and round-trip validates the JSON schema fields and entry counts.

This satisfies the RS-Z017 alternative permitting a deterministic generator. **Final closure remains conditional on a successful CI execution of the generator and audit on the corrected RC1 source tree.**

## 5. Non-blocking hardening items

The following should be addressed during RC iterations:

1. standardize chapter headers so every chapter exposes current RSMS version, chapter revision, introduced-in version, status, parent document, and author;
2. review historical `Version:` fields in Chapters 2–9 and clarify whether they denote introduction version or current specification version;
3. expand Appendix A from family-level registry coverage toward a generated complete identifier index for publication;
4. enrich machine-readable symbol scope/status metadata as specialized specifications are introduced;
5. validate all equation tags and identifier references against the canonical source graph;
6. classify every unresolved open question as non-blocking, specialization-dependent, or release-blocking;
7. establish the immutable archival target and citation procedure required by RS-VSN006 before final release.

## 6. Automated audit policy

The repository audit shall fail on:

- duplicate stable identifiers;
- unresolved stable-identifier references;
- broken repository-local Markdown links;
- known malformed LaTeX patterns;
- violation of canonical state/address separation;
- missing minimum symbol-registry entries;
- registry/master-version desynchronization;
- known Chapter 5 composition-reference defect;
- known Chapter 6 canonical base-manifold notation defect; and
- stable-identifier title changes lacking migration documentation when a baseline is supplied.

The CI workflow additionally generates and parses machine-readable identifier/symbol registries. A green audit indicates only that configured specification-integrity checks passed. It is not empirical validation.

## 7. RC1 decision

**Current decision: NOT READY TO TAG.**

The twelve-chapter architecture and registry-generation infrastructure are complete enough for RC hardening, but RC1-B001 through RC1-B003 are direct source defects and shall be corrected before the first release-candidate tag.

After those source defects are corrected and the full audit/registry workflow passes, the project may prepare `RSMS-1.0-rc.1` as an immutable candidate for external review.

## 8. Scientific-status boundary

Passing this release-readiness process establishes only that the specification meets its declared structural and governance requirements. It does not establish that the proposed resolutive state space, projection architecture, dynamics, or any specialized Resolutive Physics model is empirically correct.