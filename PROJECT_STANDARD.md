# Resolutive Science Project Standard (RSPS)

**Version:** 1.0-draft  
**Status:** Normative project-governance draft  
**Applies to:** Resolutive Science and all derived or affiliated repositories

> This document defines the minimum engineering, scientific, licensing, release, and archival requirements for projects developed under the Resolutive Science ecosystem.

---

## 1. Normative authority and compatibility

1. The `resolutive-science` repository is the normative source of truth for shared terminology, mathematical notation, identifiers, scientific status labels, and methodological conventions.
2. Derived projects MUST reuse the nomenclature and definitions established by the current applicable Resolutive Science Mathematical Specification (RSMS) and related normative specifications.
3. A derived repository MUST NOT silently redefine an existing Resolutive Science term, symbol, primitive, state variable, identifier, or mathematical object.
4. When a genuinely new cross-project concept is introduced, maintainers SHOULD evaluate whether it belongs first in the normative specification before adopting divergent local terminology.
5. Each publishable repository SHOULD state the RSMS or other normative specification version with which it is compatible.
6. Established physics, Resolutive hypotheses, computational constructs, empirical observations, and validated results MUST remain explicitly distinguishable.

## 2. Repository naming and structure

1. Project names, modules, variables, documentation, equations, and API terminology SHOULD follow the vocabulary established by `resolutive-science`.
2. Stable scientific identifiers MUST be preserved across releases unless a documented migration is unavoidable.
3. Normative specifications SHOULD be written in English. Additional translations MAY be provided as non-normative companions.
4. Repositories SHOULD contain, when applicable:
   - `README.md`;
   - `LICENSE` or an equivalent licensing document;
   - `CITATION.cff`;
   - reproducibility instructions;
   - tests;
   - methodology and assumptions;
   - benchmark or validation results;
   - limitations and known failure modes;
   - changelog or release notes;
   - machine-readable environment/dependency information.

## 3. Scientific and engineering reproducibility

A project intended for scientific publication MUST provide sufficient information for an independent technically qualified person to reproduce its principal computational claims whenever legally and technically possible.

The repository SHOULD therefore preserve:

- equations and model definitions;
- assumptions and parameter ranges;
- data provenance or authoritative dataset references;
- preprocessing procedures;
- executable scripts or notebooks where appropriate;
- random seeds for stochastic experiments when relevant;
- benchmark configuration;
- hardware/software requirements where they materially affect results;
- quantitative results and evaluation metrics;
- negative or inconclusive results when scientifically relevant;
- explicit known limitations.

Results MUST NOT be described as experimentally validated solely because they are internally consistent or numerically reproducible.

## 4. Version lifecycle

Projects SHOULD use a maturity lifecycle that distinguishes at least:

- experimental / research prototype;
- alpha;
- beta;
- release candidate;
- stable release.

A version MAY be considered a **publication candidate** when its principal functionality is stable, its relevant tests pass, its methodology is reproducible, its scientific claims are appropriately classified, its licensing is reviewed, and its documentation is sufficient for an external reader.

When a project reaches this threshold, maintainers and assisting development agents MUST explicitly flag it as a publication candidate instead of continuing indefinitely without a release checkpoint.

A stable release SHOULD receive a semantic or otherwise unambiguous version identifier and SHOULD be represented by an immutable Git tag or GitHub Release.

## 5. Publication-readiness review

Before a project is presented as a stable scientific release, the following SHOULD be reviewed:

- implementation stability;
- automated and manual test status;
- reproducibility;
- benchmark integrity;
- claim classification;
- terminology compatibility with `resolutive-science`;
- citations and attribution;
- licensing consistency;
- release notes;
- Zenodo metadata readiness.

Known scientific or engineering limitations SHOULD be documented rather than hidden in order to obtain a release designation.

## 6. Licensing policy

All Resolutive Science projects MUST undergo a licensing review before a public release.

The intended ecosystem policy is:

1. academic, educational, and non-commercial research use by universities and qualifying research institutions is permitted under the applicable license terms;
2. commercial exploitation requires a separate commercial authorization or paid commercial license from the rights holder;
3. repository documentation MUST NOT describe a license as OSI-approved "open source" unless its actual terms satisfy the Open Source Definition;
4. source availability and academic-use permission MUST NOT be confused with unrestricted commercial-use rights;
5. code, documentation, datasets, and scientific manuscripts MAY require distinct licensing instruments where their legal treatment differs;
6. third-party dependencies and datasets MUST be checked for license compatibility before redistribution.

The exact legal license text SHOULD be reviewed independently before major commercial deployment. This project standard defines policy intent and does not itself replace the operative license grant.

## 7. Zenodo and archival publication

Stable or scientifically significant releases SHOULD be prepared for archival deposition in Zenodo.

Before deposition, the repository SHOULD contain or define:

- version number;
- release date;
- complete author list;
- ORCID identifiers where available;
- title and abstract/description;
- keywords;
- licensing metadata;
- citation metadata;
- related publications and repositories;
- release notes;
- reproducibility instructions;
- appropriate archived artifacts.

Where GitHub-Zenodo integration is used, the GitHub Release/tag and the Zenodo deposition SHOULD refer to the same immutable project version.

After a DOI is minted, the DOI SHOULD be added to the repository's README, citation metadata, and relevant scientific documentation.

## 8. Cross-project traceability

Derived repositories SHOULD identify their relationship to the Resolutive Science core specification.

Recommended metadata example:

```text
Resolutive Science compatibility: RSMS 1.0
Project Standard: RSPS 1.0
```

If a project intentionally deviates from the normative specification, the deviation MUST be documented, justified, and versioned.

## 9. Governance of changes

1. Changes to this standard SHOULD be made through pull requests rather than direct edits to the default branch.
2. Material changes SHOULD include a rationale and version-history entry.
3. Existing published releases MUST remain interpretable under the specification version they originally declared.
4. Backward-incompatible terminology or identifier changes SHOULD include a migration note.

## 10. Release checklist

A publication candidate SHOULD satisfy the following checklist:

- [ ] terminology aligned with `resolutive-science`;
- [ ] applicable RSMS compatibility declared;
- [ ] scientific claims correctly classified;
- [ ] tests passing or failures explicitly documented;
- [ ] reproducibility instructions complete;
- [ ] benchmark methodology documented;
- [ ] known limitations documented;
- [ ] third-party licenses reviewed;
- [ ] academic/non-commercial and commercial licensing terms verified;
- [ ] citation metadata complete;
- [ ] version and Git tag/release prepared;
- [ ] Zenodo metadata prepared;
- [ ] DOI added back to repository after deposition.

---

## Status of this document

This is the first draft of the Resolutive Science Project Standard. It is intended to become the shared governance baseline for current and future Resolutive Science repositories while remaining subordinate to more specific normative scientific specifications where those specifications govern technical or mathematical definitions.
