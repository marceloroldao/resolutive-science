# RSMS-1.0

## Resolutive Science Mathematical Specification

**Version:** 1.0-draft  
**Status:** In development  
**Author:** Marcelo Roldão Matos  
**ORCID:** 0009-0003-6075-4680  
**Project:** Resolutive Science

> **From mathematical specification to reproducible science.**

---

## Document status

This document is the normative draft of the **Resolutive Science Mathematical Specification (RSMS)**. It defines the universal scientific, mathematical, and methodological basis shared by the specialized modules of Resolutive Science.

The present draft does not claim experimental validation of Resolutive Physics. It establishes the language, scope, traceability rules, and scientific commitments required for its hypotheses to be formulated, implemented, tested, and revised.

### Version history

| Version | Date | Status | Description |
|---|---:|---|---|
| 1.0-draft.1 | 2026-08-06 | Draft | Initial introduction, scope, documentation hierarchy, and scientific principles. |

---

# Chapter 1 — Introduction, Scope, and Scientific Principles

## 1.1 Purpose

Resolutive Science (RS) is a research program dedicated to the mathematical formulation, computational implementation, and empirical evaluation of hypotheses associated with Resolutive Physics.

This specification establishes the common language used by all modules of the project. Its purpose is not to present observational results or to assume the validity of a particular physical hypothesis. Its purpose is to define, as precisely as possible, the universal structures from which specialized models can be derived and independently evaluated.

Every computational implementation, technical document, scientific article, numerical experiment, or specialized specification developed within Resolutive Science shall either:

1. conform to the applicable version of this specification; or
2. identify explicitly the definitions, assumptions, or equations from which it departs.

The RSMS is therefore the primary normative reference of the Resolutive Science ecosystem.

## 1.2 Objectives

The RSMS has five primary objectives.

### 1.2.1 Uniform mathematical language

Define a stable notation for quantities, operators, indices, coordinate conventions, geometric structures, units, and states used throughout Resolutive Science.

### 1.2.2 Internal consistency

Ensure that specialized modules—such as cosmology, galactic dynamics, gravitational lensing, quantum theory, electromagnetism, inertia, and artificial intelligence—share a compatible conceptual and mathematical foundation.

### 1.2.3 Unambiguous implementation

Require every normative mathematical structure to be sufficiently defined for computational implementation, including its domain, codomain, parameters, dimensional conventions, boundary conditions, and limiting cases when applicable.

### 1.2.4 Scientific auditability

Provide traceability between:

- hypothesis;
- mathematical definition;
- equation identifier;
- software implementation;
- automated test;
- dataset;
- generated result;
- scientific interpretation.

### 1.2.5 Controlled evolution

Allow the theory and its implementations to evolve through explicit versioning, documented changes, regression tests, and comparison with earlier releases.

## 1.3 Scope

The RSMS describes only the universal foundations of Resolutive Science.

It may define:

- universal scientific principles;
- common mathematical notation;
- primitive objects and state variables;
- general geometric structures;
- universal operators;
- shared dimensional and unit conventions;
- rules for model specialization;
- traceability and validation requirements.

The RSMS does not, by itself, define complete models for cosmology, galaxies, gravitational lenses, quantum systems, electromagnetism, inertia, or artificial intelligence. Those subjects shall be developed in specialized specifications that inherit the definitions of the RSMS.

This separation is deliberate. Universal assumptions belong in the RSMS; domain-specific assumptions belong in the corresponding specialized specification.

## 1.4 Documentation hierarchy

Resolutive Science uses a hierarchical specification model.

### 1.4.1 Universal specification

- **RSMS** — Resolutive Science Mathematical Specification.

The RSMS contains the universal definitions and requirements shared by the ecosystem.

### 1.4.2 Specialized specifications

The planned specialized specifications include:

- **RCMS** — Resolutive Cosmology Mathematical Specification;
- **RGMS** — Resolutive Galaxies Mathematical Specification;
- **RLMS** — Resolutive Lensing Mathematical Specification;
- **RQMS** — Resolutive Quantum Mathematical Specification;
- **REMS** — Resolutive Electromagnetism Mathematical Specification;
- **RIMS** — Resolutive Inertia Mathematical Specification;
- **RAMS** — Resolutive Artificial Intelligence Mathematical Specification.

A specialized specification may introduce additional structures, equations, parameters, and observables, provided that it does not silently contradict the RSMS. Any intentional incompatibility shall be documented as an explicit extension, revision, or alternative formulation.

### 1.4.3 Computational implementations

Software repositories implement the corresponding specifications. A scientific implementation is not normative by itself: when code and specification disagree, the discrepancy shall be treated as a defect or as a proposed specification change requiring review.

### 1.4.4 Publications

Articles, preprints, reports, and presentations shall cite the exact versions of the specifications, software, configuration files, and datasets used to produce their results.

## 1.5 Separation of scientific stages

Resolutive Science distinguishes four stages that shall not be conflated.

### 1.5.1 Speculation

A conceptual possibility not yet expressed as a complete mathematical hypothesis.

### 1.5.2 Hypothesis

A mathematically explicit proposition with defined assumptions and, whenever possible, identifiable consequences.

### 1.5.3 Implemented model

A computational realization of a hypothesis, accompanied by tests of correctness, numerical stability, dimensional consistency, and limiting behavior.

### 1.5.4 Validated result

A result obtained from a documented implementation and evaluated against synthetic tests, known limits, experimental measurements, or observational data using declared statistical criteria.

Implementation does not imply validation. Numerical agreement in one dataset does not imply universal validity. A result shall be described according to the strongest level of support actually obtained.

## 1.6 Methodological axioms

The following axioms govern the practice of Resolutive Science. They are methodological commitments of the project, not claims about nature.

### RS-0 — Reproducibility

Every published quantitative result shall be reproducible, within declared numerical tolerances, from the referenced specification, source code, configuration, random seeds, data, and execution procedure.

### RS-1 — Consistency

Every new definition shall be checked for logical, mathematical, and dimensional consistency with the specification on which it depends.

### RS-2 — Implementability

Every normative mathematical structure shall admit an unambiguous computational interpretation. Objects that remain conceptually useful but are not yet implementable shall be labeled non-normative or provisional.

### RS-3 — Auditability

Every implemented physical equation shall be traceable to a stable specification identifier, source file, test set, and validation record.

### RS-4 — Falsifiability and discriminability

Whenever possible, a physical hypothesis shall identify observations, experiments, limits, or statistical comparisons capable of distinguishing it from competing hypotheses or revealing its failure.

### RS-5 — Symmetric comparison

Comparisons between Resolutive models and established models shall use equivalent datasets, preprocessing choices, nuisance treatments, priors, parameter-count conventions, and statistical criteria unless a deviation is explicitly justified.

### RS-6 — Revision under evidence

Definitions and models may be revised, restricted, or rejected when mathematical analysis, numerical tests, experiments, or observations reveal inconsistency or inadequate performance.

## 1.7 Normative language

The key words **shall**, **shall not**, **should**, **should not**, and **may** are used as follows:

- **shall / shall not** indicate normative requirements;
- **should / should not** indicate strong recommendations that may be departed from with justification;
- **may** indicates an allowed option.

Explanatory passages, examples, historical notes, and interpretations are non-normative unless explicitly identified otherwise.

## 1.8 Equation and definition identifiers

Normative mathematical content shall receive stable identifiers.

The initial identifier families are:

- `RS-A###` — methodological or universal axioms;
- `RS-D###` — definitions;
- `RS-E###` — equations;
- `RS-O###` — operators;
- `RS-R###` — requirements;
- `RS-T###` — tests or validation criteria.

Specialized specifications shall use their own prefixes, such as `RC-E###` for cosmological equations or `RG-E###` for galactic equations.

An identifier shall not be reassigned to a different meaning after publication. Deprecated identifiers shall remain in the historical record with an explicit replacement reference when applicable.

## 1.9 Traceability requirement

For every normative physical equation implemented in software, the project should maintain a traceability record containing at least:

| Field | Required content |
|---|---|
| Identifier | Stable equation or definition ID |
| Name | Concise descriptive name |
| Purpose | Physical or computational role |
| Inputs | Variables, parameters, domains, and units |
| Output | Quantity, codomain, and unit |
| Assumptions | Mathematical and physical assumptions |
| Limiting cases | Known limits or recovery conditions |
| Implementation | Repository and source path |
| Tests | Unit, regression, dimensional, or validation tests |
| Observables | Experimental or observational quantities affected |
| Status | Proposed, implemented, tested, validated, deprecated |

## 1.10 Scientific integrity

The objective of Resolutive Science is not to confirm Resolutive Physics at any cost. Its objective is to create a transparent framework in which resolutive hypotheses can be stated precisely, compared fairly, and revised according to evidence.

The project shall report favorable, neutral, and unfavorable results with the same methodological standards. Model failure is scientific information and shall not be hidden by selective datasets, undocumented parameter changes, or asymmetric comparisons.

## 1.11 Organization of the RSMS

The planned structure of RSMS v1.0 is:

1. Introduction, Scope, and Scientific Principles;
2. Mathematical Conventions and Notation;
3. Primitive Objects and Resolutive State Space;
4. Geometric and Bundle Structure;
5. Fundamental Fields and Operators;
6. Dynamics and Variational Principles;
7. Observables, Projection, and Measurement;
8. Dimensional Structure and Units;
9. Limiting Cases and Correspondence Principles;
10. Computational Conformance and Validation;
11. Versioning, Extensions, and Deprecation;
12. Appendices and Symbol Registry.

This organization may evolve during the draft phase. Once RSMS v1.0 is released, incompatible structural changes shall require a new major version.

## 1.12 Chapter status

| Criterion | Status |
|---|---|
| Scientific scope defined | Draft complete |
| Documentation hierarchy defined | Draft complete |
| Methodological axioms defined | Draft complete |
| Mathematical axioms introduced | Not yet |
| Dimensional consistency applicable | Not yet |
| Computational implementation applicable | Partially |
| Empirical tests defined | Not yet |

---

## Next chapter

**Chapter 2 — Mathematical Conventions and Notation** will establish the formal language required before introducing the primitive physical axioms of Resolutive Physics.
