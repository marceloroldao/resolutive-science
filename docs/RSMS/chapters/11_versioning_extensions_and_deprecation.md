# Chapter 11 — Versioning, Extensions, and Deprecation

**Specification:** RSMS-1.0  
**Current RSMS version:** 1.0-draft.11  
**Chapter revision:** 1.0  
**Introduced in:** 1.0-draft.11  
**Status:** Normative draft — specification evolution and compatibility framework  
**Parent document:** `docs/RSMS/RSMS_v1.0.md`  
**Author:** Marcelo Roldão Matos

---

## 11.1 Chapter purpose

This chapter defines how RSMS specifications evolve without silently changing the meaning of established mathematical objects, identifiers, computational interfaces, scientific claims, or published results.

It establishes normative rules for version identifiers, compatibility, extensions, revisions, deprecation, supersession, migration, historical traceability, and specialized specifications. It introduces no new physical law, observable law, dynamical equation, or resolutive hypothesis.

The central requirement is that **scientific evolution shall be explicit and traceable**. A revised theory, notation, algorithm, or interpretation shall not be made to appear retroactively identical to an earlier version when its meaning or behavior has changed.

## 11.2 Scope and inherited authority

This chapter inherits the stable-identifier policy of Chapter 1, the notation namespace of Chapter 2, the canonical primitive objects of Chapter 3, the cross-chapter namespace rules established by the RSMS audit, and the computational provenance and change-classification requirements of Chapter 10.

Where an identifier is already defined by an earlier chapter, this chapter governs only its lifecycle and compatibility status. It does not redefine that identifier.

## 11.3 Versioning framework

The family `RS-VSN###` is reserved for specification-versioning requirements.

### RS-VSN001 — Specification version

Every normative RSMS document shall declare an explicit specification version. A version identifies a fixed normative state of the specification and shall be sufficient to determine the applicable definitions, identifier meanings, requirements, and compatibility rules.

A document that omits its governing specification version shall not claim full RSMS conformance.

### RS-VSN002 — Draft version

A draft version has the form

```text
1.0-draft.N
```

or another explicitly documented draft scheme adopted by the project.

Draft status permits controlled revision before release. Draft status does not permit silent identifier reassignment or undocumented semantic change.

### RS-VSN003 — Released version

A released version is a published, immutable specification snapshot intended for external citation and implementation. Once released, its normative content shall not be edited in place except for explicitly non-normative presentation corrections that do not change meaning.

Substantive corrections shall produce a new version.

### RS-VSN004 — Version components

Released RSMS versions should use semantic version components of the form

\[
\text{MAJOR.MINOR.PATCH}.
\]

The intended meanings are:

- **MAJOR** — incompatible normative change;
- **MINOR** — backward-compatible normative addition or compatible clarification;
- **PATCH** — correction that preserves intended normative semantics and compatibility.

The applicable compatibility judgment shall be documented rather than inferred solely from the number.

### RS-VSN005 — Chapter revision

A chapter revision identifies edits to a chapter within the current specification-development process. It shall not substitute for the governing RSMS version.

Every chapter header shall distinguish, at minimum:

- current RSMS version;
- chapter revision;
- version in which the chapter was introduced; and
- normative status.

### RS-VSN006 — Immutable citation target

Scientific publications, datasets, software releases, and validation records shall cite an immutable specification target, such as a tagged release, archival identifier, or commit corresponding to the declared version.

A mutable branch name alone is insufficient for archival scientific citation.

### RS-VSN007 — Change classification

Every normative change shall be classified as one or more of:

1. editorial;
2. clarification;
3. compatible addition;
4. compatible restriction;
5. identifier migration;
6. behavioral change;
7. semantic change;
8. incompatible change;
9. deprecation;
10. removal.

The classification shall describe actual scientific or implementation impact, not merely the size of the textual diff.

### RS-VSN008 — Version history

Every RSMS version shall maintain a version-history record stating at least the date, status, affected chapters, change classification, compatibility impact, and a concise description.

A version-history entry shall not claim “no scientific change” when a normative definition, equation, identifier meaning, validation rule, or interpretation has materially changed.

## 11.4 Compatibility

### RS-VSN009 — Backward compatibility

A change is **backward-compatible** when an implementation, specialization, dataset schema, or scientific statement conforming to the earlier version remains valid under the later version without changing its intended semantics.

Recompilation, formatting differences, or additional optional metadata do not necessarily break compatibility. A changed physical meaning, required parameter, unit convention, identifier meaning, or output interpretation normally does.

### RS-VSN010 — Forward compatibility

A representation is **forward-compatible** only when an older consumer can safely process or reject newer content without silently assigning an incorrect meaning.

Ignoring unknown normative fields is permitted only when the governing schema explicitly declares such behavior safe.

### RS-VSN011 — Compatibility declaration

Every substantive RSMS revision shall state whether it is:

- backward-compatible;
- conditionally compatible;
- migration-required; or
- incompatible.

Conditional compatibility shall identify the conditions explicitly.

### RS-VSN012 — Compatibility boundary

Compatibility may differ across layers. A revision may preserve mathematical meaning while changing a serialization schema, or preserve software interfaces while changing a scientific interpretation.

Compatibility declarations shall therefore identify the relevant layer, including as applicable:

- mathematical specification;
- symbol namespace;
- identifier namespace;
- computational API;
- serialized data;
- numerical behavior;
- observable definition;
- validation record; and
- scientific interpretation.

## 11.5 Extension framework

The family `RS-EXT###` is reserved for controlled extensions.

### RS-EXT001 — Extension

An **extension** is a declared addition that builds on an existing RSMS version without silently modifying the inherited definitions.

An extension shall identify its parent specification version, scope, new identifiers, dependencies, compatibility status, and scientific status.

### RS-EXT002 — Specialized specification

A specialized specification such as RCMS, RGMS, RLMS, RQMS, REMS, RIMS, or RAMS is an extension layer that inherits the RSMS unless an explicit deviation is declared.

A specialized specification shall not redefine a canonical RSMS identifier to mean something different.

### RS-EXT003 — Extension namespace

Every extension shall use a namespace that does not collide with RSMS identifiers or with another registered specialization.

Specialization-specific equations, definitions, operators, requirements, and tests shall use their declared prefixes.

### RS-EXT004 — Extension manifest

A normative extension shall include an extension manifest stating:

1. extension name and version;
2. parent RSMS version;
3. inherited identifiers;
4. newly introduced identifier families;
5. modified or restricted assumptions;
6. compatibility status;
7. implementation dependencies where applicable;
8. scientific status of added physical content; and
9. known unresolved conflicts or limitations.

### RS-EXT005 — Conforming extension

An extension is conforming when it preserves the meanings of all inherited normative identifiers and satisfies the inherited `shall` requirements applicable to its scope.

Additional restrictions are permitted when they are declared and do not retroactively redefine the parent specification.

### RS-EXT006 — Nonconforming extension

An extension that intentionally violates or replaces an inherited normative requirement shall identify itself as nonconforming with respect to that parent version and document the exact deviations.

A nonconforming extension shall not claim unqualified RSMS conformance.

### RS-EXT007 — Experimental extension

An experimental extension may introduce provisional mathematical or physical structures for evaluation before inclusion in the universal RSMS.

Its identifiers shall be clearly marked provisional or specialization-scoped. Experimental adoption shall not reserve universal RSMS meaning unless formally incorporated through the RSMS revision process.

### RS-EXT008 — Promotion to universal RSMS

A specialized or experimental structure may be proposed for promotion into the universal RSMS only when its cross-domain necessity, mathematical consistency, identifier migration, compatibility impact, computational implications, and scientific status have been reviewed.

Usage frequency alone is insufficient justification for universal promotion.

### RS-EXT009 — Extension dependency

An extension depending on another extension shall declare the dependency and compatible version range. Cyclic normative dependencies should be avoided; if unavoidable, their resolution order and shared authority shall be explicit.

### RS-EXT010 — Extension conflict

If two extensions assign incompatible assumptions to the same inherited object or domain, the conflict shall be documented. Their combination shall not be assumed valid without a separately specified reconciliation or higher-level specialization.

## 11.6 Deprecation and supersession

The family `RS-DEP###` is reserved for deprecation and lifecycle requirements.

### RS-DEP001 — Deprecation

A **deprecated** identifier or feature remains part of the historical specification but is no longer recommended for new conforming work.

Deprecation shall not erase its previous meaning.

### RS-DEP002 — Deprecation notice

A deprecation notice shall state:

- deprecated identifier or feature;
- version in which deprecation begins;
- reason;
- replacement when one exists;
- compatibility implications;
- migration guidance; and
- planned removal version, if known.

### RS-DEP003 — Supersession

A **superseded** identifier or formulation has been replaced by a newer normative object for future use. The historical object remains citable under the version in which it was valid.

Supersession shall identify the replacement and whether the replacement is semantically equivalent, approximately equivalent, restricted, extended, or incompatible.

### RS-DEP004 — Removal

A normative identifier shall not be reused after removal. The identifier remains permanently reserved in historical registries with status `removed` and a reference to its last valid version.

### RS-DEP005 — Identifier migration

When an identifier must change because of namespace repair, scope correction, or other controlled revision, the specification shall provide a migration record containing:

| Field | Required content |
|---|---|
| Old identifier | Historical identifier |
| Old meaning | Meaning before migration |
| Replacement | New identifier or `none` |
| New meaning | Meaning after migration |
| First affected version | Version in which migration occurs |
| Compatibility | Compatible, conditional, or incompatible |
| Reason | Technical or scientific justification |

### RS-DEP006 — No silent reassignment

A stable identifier shall never be silently assigned a new meaning. If a previous definition is erroneous, the project shall preserve the historical record and issue a correction, migration, supersession, or deprecation as appropriate.

### RS-DEP007 — Published-result preservation

A later deprecation or revision shall not alter the historical specification context of a published result. Reanalysis under a newer version is a new analysis and shall receive its own provenance and validation record.

### RS-DEP008 — Legacy implementation

An implementation targeting a deprecated or superseded specification may remain scientifically useful when it declares the exact historical version it implements. It shall not be represented as conforming to a newer version without migration and verification.

## 11.7 Revision governance

### RS-VSN013 — Normative change proposal

A substantive normative change should be introduced through a reviewable change proposal containing:

- motivation;
- affected identifiers;
- exact normative change;
- mathematical impact;
- computational impact;
- scientific-status impact;
- compatibility classification;
- migration plan;
- validation implications; and
- alternatives considered.

### RS-VSN014 — Review separation

A change to scientific meaning should be distinguishable from editorial restructuring, formatting, generated registries, or implementation refactoring. Pull requests or equivalent review units should keep unrelated normative changes separate when practical.

### RS-VSN015 — Registry synchronization

Every accepted identifier addition, migration, deprecation, supersession, or removal shall update the applicable canonical registries in the same normative change set.

Generated registries may be informative, but they shall derive from authoritative source clauses and shall not silently override them.

### RS-VSN016 — Reproducible specification build

Where the RSMS is rendered into HTML, PDF, machine-readable registries, or other publication artifacts, the build process should be reproducible from the cited source revision and toolchain.

Generated presentation artifacts shall not introduce normative content absent from the source specification.

## 11.8 Specialized scientific revisions

A specialized specification may evolve independently of the universal RSMS when the changed content is domain-specific. It shall declare the parent RSMS versions with which each release is compatible.

A domain-specific empirical failure does not automatically require an RSMS major revision. Conversely, a change to a universal primitive, canonical projection interface, dimensional rule, or global identifier meaning normally requires RSMS-level review.

## 11.9 Open governance questions

The following remain open:

1. At what milestone should `RSMS-1.0` leave draft status?
2. Which registries should become machine-generated normative artifacts versus informative indexes?
3. Which compatibility guarantees should be required across minor releases?
4. How long should deprecated identifiers remain supported by reference implementations?
5. Which changes require formal external review before release?
6. Should experimental extensions use a dedicated provisional prefix?
7. What archival service should provide immutable long-term citation of released RSMS versions?
8. How should multiple specialized specifications negotiate shared structures that are not yet universal?

## 11.10 Conformance checklist

| Requirement | Conformance condition |
|---|---|
| Version identity | Exact specification version is declared |
| Immutable citation | Published work cites an immutable specification target |
| Change classification | Normative revisions identify their actual impact |
| Compatibility | Backward, forward, and layer-specific compatibility are declared where applicable |
| Extension parent | Extensions declare their parent RSMS version |
| Namespace | Extension identifiers do not collide with canonical RSMS identifiers |
| Deviations | Nonconforming extensions identify inherited requirements they violate |
| Deprecation | Deprecated objects retain historical meaning and migration guidance |
| Migration | Identifier changes have explicit migration records |
| Removal | Removed identifiers remain permanently reserved |
| Published results | Historical provenance is not rewritten by later revisions |
| Registries | Canonical registries are synchronized with lifecycle changes |
| Scientific status | Versioning operations do not inflate evidential status |
| Scope | No physical law or resolutive hypothesis is introduced by this chapter |

## 11.11 Chapter status

| Subject | Status |
|---|---|
| Specification versioning | Normative draft |
| Compatibility framework | Normative draft |
| Extension mechanism | Normative draft |
| Specialized-specification inheritance | Normative draft |
| Deprecation, supersession, and migration | Normative draft |
| Revision governance | Normative draft |
| Release archival mechanism | Open |
| New physical hypotheses or equations | None introduced |
| Experimental validation of Resolutive Physics | Not asserted |

Chapter 11 is designated **RSMS 1.0-draft.11** as of **2026-08-07**. Its identifier families `RS-VSN001`–`RS-VSN016`, `RS-EXT001`–`RS-EXT010`, and `RS-DEP001`–`RS-DEP008` are reserved by this chapter.