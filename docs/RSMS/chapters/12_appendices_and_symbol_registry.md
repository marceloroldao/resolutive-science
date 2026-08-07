# Chapter 12 — Appendices and Symbol Registry

**Specification:** RSMS-1.0  
**Version:** 1.0-draft.12  
**Status:** Normative draft — registry, cross-reference, and release-readiness governance  
**Parent document:** `docs/RSMS/RSMS_v1.0.md`

---

## 12.1 Purpose

This chapter closes the planned normative structure of RSMS-1.0 by defining how appendices, identifiers, symbols, aliases, cross-references, and release-readiness records are governed.

It introduces no physical law, empirical result, interaction, observable, or dynamical hypothesis. Its purpose is specification integrity: a reader or implementation shall be able to determine what a symbol or stable identifier means, where it is defined, whether an alternate notation is permitted, and whether the specification is sufficiently audited for a tagged release.

## 12.2 Registry architecture

### RS-Z001 — Canonical registry set

RSMS-1.0 shall maintain, at minimum, the following registries:

1. a stable identifier registry;
2. a symbol registry;
3. an alias and notation-compatibility registry;
4. a normative cross-reference registry or mechanically auditable equivalent; and
5. a release-readiness record for each release candidate or final release.

A registry may be represented in Markdown, a machine-readable format, or both. When two representations exist, the project shall designate which representation is authoritative and shall test them for consistency.

### RS-Z002 — Registry entry requirements

Each canonical registry entry shall contain enough information to disambiguate the referenced object. As applicable, an entry shall include:

- stable identifier;
- canonical name;
- canonical symbol;
- governing chapter or specification;
- definition location;
- mathematical role or type;
- status;
- aliases or historical notation;
- replacement identifier when deprecated or superseded; and
- notes needed to prevent semantic collision.

Absence of a field that is not applicable shall be distinguishable from an unknown or unresolved value.

## 12.3 Stable identifier registry

### RS-Z003 — Identifier uniqueness

Every normative stable identifier shall have exactly one canonical meaning within its governing specification version. An identifier shall not be reused for a different object, even after deprecation.

The identifier registry shall detect or permit automated detection of duplicate assignments, missing definitions, malformed identifiers, and references to identifiers that do not exist in the applicable specification baseline.

### RS-Z004 — Identifier families

The universal RSMS identifier namespace includes the families defined by Chapters 1–11, including their chapter-specific extensions. New universal families shall be documented before normative use.

Specialized specifications shall use their assigned specialization prefix or another explicitly registered namespace. A specialized identifier shall not masquerade as a universal RSMS identifier.

### RS-Z005 — Identifier status

Each identifier shall have a status compatible with Chapter 11, such as active, provisional, deprecated, or superseded. Deprecated and superseded identifiers remain reserved permanently and shall retain a traceable historical entry.

## 12.4 Symbol registry

### RS-Z006 — Canonical symbol

A canonical symbol is the preferred mathematical notation for a registered object in a declared scope. A symbol registry entry shall identify both the glyph or expression and its semantic referent; visual similarity alone does not establish identity.

The same symbol may be reused only when scopes make the meanings unambiguous or when the governing specification explicitly permits the overload. Ambiguous overload in the same mathematical context is nonconforming.

### RS-Z007 — Symbol metadata

For each normative or widely reused symbol, the registry should record:

| Field | Meaning |
|---|---|
| Symbol | Canonical rendered or source notation |
| Name | Human-readable name |
| Identifier | Stable definition or governing identifier when available |
| Type | Scalar, field, map, bundle, space, parameter, index, operator, etc. |
| Domain | Mathematical domain when applicable |
| Codomain | Mathematical codomain when applicable |
| Dimension/unit | Declared dimension or unit status |
| Scope | Universal RSMS or named specialization |
| Status | Active, provisional, deprecated, superseded, or alias |
| Defined in | Canonical chapter/section |

Machine-readable registries may normalize these fields but shall preserve their semantics.

### RS-Z008 — Symbol collision control

Before a new normative symbol is introduced, its author shall check the active registry for collision. If reuse is intentional, the new definition shall state the scope distinction. If reuse would create ambiguity, a different symbol shall be selected.

## 12.5 Aliases and historical notation

### RS-Z009 — Alias policy

An alias is a permitted alternate notation for an already defined object. An alias shall not silently create a second definition.

Every normative alias shall point to one canonical referent and shall state whether it is:

- a local convenience alias;
- a specialization-specific alias;
- a compatibility alias retained from an earlier draft; or
- a deprecated notation scheduled for removal from active prose.

### RS-Z010 — Resolutive-field notation compatibility

RS-D007 defines the resolutive field structurally as a section and uses `\mathcal R_f` in its local field notation. RS-F008 introduces `\Psi_R` as a field symbol for the same section-level mathematical role and explicitly does not replace the state `R`.

For RSMS-1.0 draft compatibility:

- `R` remains the canonical symbol for an individual four-component resolutive state;
- `\mathcal R_f` remains a valid structural notation for a resolutive field/section inherited from Chapter 3;
- `\Psi_R` is a permitted field-symbol alias introduced by Chapter 5;
- neither `\mathcal R_f` nor `\Psi_R` may be interpreted as adding a fifth primitive state component; and
- a specialized specification shall choose one notation consistently within a derivation and declare any switch between them.

This rule records compatibility; it does not introduce a physical wavefunction interpretation for `\Psi_R`.

### RS-Z011 — Historical notation preservation

When notation changes, published equations, releases, and citations shall remain interpretable. Historical notation shall therefore be recorded as an alias or deprecated symbol rather than erased from the registry. Migration notes shall identify the first version using the replacement notation.

## 12.6 Cross-reference integrity

### RS-Z012 — Normative reference resolution

Every normative cross-reference to an identifier, chapter, appendix, table, equation, software artifact, or external specification shall resolve to a uniquely identifiable target in the declared baseline.

Broken normative references are release blockers unless explicitly documented as unresolved dependencies of a pre-release draft.

### RS-Z013 — Definition-before-dependence rule

A normative object should be defined before substantive dependence on it. Forward references are permitted when necessary, but they shall identify the later governing definition and shall not assign a conflicting provisional meaning.

### RS-Z014 — Cross-chapter semantic consistency

Cross-chapter reuse of an object shall preserve its mathematical type and semantic role unless an explicit extension, specialization, or revision states otherwise. A change in symbol alone does not change the object; a change in mathematical meaning requires the versioning procedure of Chapter 11.

## 12.7 Appendices

### RS-Z015 — Appendix status

An appendix shall declare whether it is normative or informative. Normative appendices may contain registries, schemas, compatibility tables, or requirements that are binding on conformance. Informative appendices may contain examples, derivations, explanatory notes, historical material, or implementation guidance.

A normative requirement shall not be hidden in an appendix labeled informative.

### RS-Z016 — Appendix naming and stability

Normative appendices should use stable lettered designations and descriptive filenames. Once cited by a released specification, an appendix designation shall not be silently reassigned to unrelated content.

## 12.8 Machine-readable indexes

### RS-Z017 — Machine-readable registry requirement

Before RSMS-1.0 final release, the project shall provide a machine-readable representation of the stable identifier registry and symbol registry, or a deterministic tool that generates them from the normative sources.

The representation shall support automated checks for at least:

1. duplicate identifiers;
2. duplicate canonical symbols within conflicting scopes;
3. unresolved normative references;
4. deprecated identifiers lacking required migration metadata; and
5. registry entries whose governing source cannot be located.

The serialization format is not fixed by this chapter.

### RS-Z018 — Generated artifact provenance

A generated registry or index shall record or be reproducibly associated with the specification version and source revision from which it was generated. Generated artifacts shall not be manually edited in a way that breaks reproducibility.

## 12.9 Release-readiness gate

### RS-Z019 — RSMS release-readiness record

A release candidate shall have a documented readiness record. At minimum it shall report the result of checks for:

- identifier uniqueness and resolution;
- symbol-registry consistency;
- internal links and cross-references;
- dimensional and notation consistency where mechanically checkable;
- version and status consistency across normative files;
- absence or explicit disposition of unresolved release-blocking audit findings;
- availability of required machine-readable indexes;
- reproducibility of the registry/audit tooling; and
- traceability to the source revision proposed for release.

A failed mandatory check shall be either corrected or explicitly classified under the exception procedure of Chapter 11 before release.

### RS-Z020 — Draft completion is not scientific validation

Completion of all planned RSMS chapters, registries, audits, and release-readiness checks establishes specification maturity only. It shall not be described as experimental validation of Resolutive Physics, validation of any specialized physical model, or evidence that nature realizes the structures defined by RSMS.

## 12.10 Minimum canonical symbol table

The following table establishes the minimum universal entries that shall appear in the RSMS symbol registry. It is not exhaustive.

| Symbol | Canonical role | Governing definition | Notes |
|---|---|---|---|
| `M` | Base spacetime manifold | RS-D001 | Universal base-space symbol |
| `\mathcal R` | Internal resolutive space | RS-D002 | Space of admissible minimal states |
| `E_R` | Total/resolutive state bundle | RS-D003, RS-G017 | Fiber modeled on `\mathcal R` |
| `R` | Resolutive state | RS-D004 | Four components only |
| `\rho_R` | Resolutive density/depth coordinate | RS-D004 | Primitive state component |
| `\Theta_R` | Resolutive phase coordinate | RS-D004 | Primitive state component |
| `\iota_R` | Resolutive inclination coordinate | RS-D004 | Primitive state component |
| `\kappa_R` | Local resolutive curvature coordinate | RS-D004 | Not automatically spacetime curvature |
| `a_R` | Resolutive address | RS-D005 | Not part of `R` |
| `\mathcal O` | Observable space | RS-D006 | Model-dependent structure |
| `\mathcal R_f` | Resolutive field/section notation | RS-D007 | Valid structural notation |
| `\Psi_R` | Resolutive field-symbol alias | RS-F008, RS-Z010 | No automatic quantum interpretation |
| `\Pi` | Observable projection map | RS-O001, RS-F009 | No implied linearity/idempotence |
| `\Phi` | Tuple of dynamical fields | RS-V001 | Model-dependent configuration |
| `\mathcal S` | Action functional | RS-V003 | Used only when variational formulation selected |
| `\mathcal L` | Lagrangian scalar/density context | RS-V004 | Transformation role shall be explicit |
| `U(\tau_2,\tau_1)` | Evolution operator | RS-Y004 | Properties are not presumed |

## 12.11 Conformance

A conforming RSMS release or specialization shall:

1. preserve stable identifier meanings;
2. register normative symbols and aliases needed to interpret its equations;
3. prevent ambiguous symbol collisions in a common scope;
4. preserve historical traceability for deprecated notation;
5. keep normative cross-references resolvable;
6. distinguish normative from informative appendices;
7. provide or generate the machine-readable indexes required by RS-Z017 for RSMS-1.0 final release; and
8. complete the applicable release-readiness record before a release is declared final.

## 12.12 Closure of the planned RSMS-1.0 chapter structure

With this chapter, the twelve-chapter architecture planned in Chapter 1 is structurally complete at normative-draft level. Further work before RSMS-1.0 final release is an audit-and-hardening phase: registry completion, cross-chapter consistency review, machine-readable indexing, automated checks, correction of identified defects, and release-candidate review.

No statement in this closure changes the scientific status of any resolutive hypothesis.