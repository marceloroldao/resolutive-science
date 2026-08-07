# Chapter 10 — Computational Conformance and Validation

**Specification:** RSMS-1.0  
**Current RSMS version:** 1.0-draft.10  
**Chapter revision:** 1.1  
**Introduced in:** 1.0-draft.10  
**Status:** Normative draft — computational conformance and validation framework  
**Parent document:** `docs/RSMS/RSMS_v1.0.md`  
**Author:** Marcelo Roldão Matos

---

## 10.1 Chapter purpose

This chapter defines the common requirements by which a computational implementation, numerical experiment, benchmark, validation study, or reproducibility package may claim conformance with RSMS-1.0.

It establishes a traceable chain from normative mathematical content to software, configuration, data, execution, numerical verification, empirical comparison, and reported scientific conclusions. It introduces no new physical law, observable law, dynamical equation, or resolutive hypothesis.

Implementation, verification, validation, reproduction, and scientific interpretation are distinct activities. Passing one category shall not be represented as passing another.

## 10.2 Scope and inherited authority

This chapter inherits the requirements of Chapters 1–9. In particular:

- `RS-M112` in Chapter 7 remains the **canonical definition of a validation claim**;
- `RS-M113` remains the **canonical definition of the independent mathematical, numerical, and empirical validation categories**;
- the `RS-VAL###` family introduced here does **not** redefine those concepts; it specifies operational, computational, provenance, comparison, and reporting requirements for applying them.

A computational artifact shall not silently redefine an inherited object or stable identifier. Any intentional departure shall be documented as a nonconforming implementation, extension, proposed revision, or specialized specification.

## 10.3 Computational conformance

The family `RS-COMP###` is reserved for common computational-conformance requirements.

### RS-COMP001 — Conforming implementation

A **conforming implementation** is a versioned computational realization that declares the RSMS version and any specialized specification version it implements and provides sufficient traceability to determine how each implemented normative object, equation, operator, constraint, observable, or procedure corresponds to its governing identifier.

Conformance means agreement with the declared specification within stated numerical and representational tolerances. It does not mean physical correctness or empirical validation.

### RS-COMP002 — Implementation manifest

Every conforming implementation shall provide an implementation manifest containing, at minimum:

1. specification and specialization versions;
2. source-code revision or immutable commit identifier;
3. implemented normative identifiers;
4. programming language and interpreter or compiler version;
5. dependency lock or equivalent environment description;
6. numeric precision and arithmetic mode;
7. hardware-relevant assumptions when material;
8. configuration-file versions;
9. dataset identifiers and checksums when data are used;
10. random seeds or stochastic-state provenance when applicable; and
11. known deviations, unsupported features, and implementation limitations.

### RS-COMP003 — Traceability matrix

A conforming scientific implementation shall maintain an auditable mapping

\[
\text{specification identifier}
\longleftrightarrow
\text{source implementation}
\longleftrightarrow
\text{tests}
\longleftrightarrow
\text{generated artifacts}.
\]

An identifier intentionally not implemented shall be marked explicitly as `not implemented`, `not applicable`, or an equivalent declared status.

### RS-COMP004 — Computational environment

The computational environment shall be sufficiently specified to reproduce the intended execution. This includes dependency versions, platform assumptions, environment variables that affect numerical behavior, accelerator or backend selection when relevant, and external libraries whose behavior materially contributes to the result.

### RS-COMP005 — Numeric representation

Every implementation shall declare the numeric representations used for normative quantities, including applicable floating-point format, complex representation, integer width, arbitrary precision, interval arithmetic, fixed point, or stochastic representation.

A representation change capable of altering a reported result beyond its declared tolerance shall be treated as a material implementation change.

### RS-COMP006 — Determinism and stochastic reproducibility

A deterministic computation shall reproduce equivalent outputs within declared tolerances under its declared execution conditions.

A stochastic computation shall instead declare the pseudorandom generator or stochastic source, seed or state-management policy, sampling procedure, ensemble size, and statistical reproducibility criterion. Bitwise identity is not required when distributional reproducibility is the declared target.

### RS-COMP007 — Configuration provenance

Every execution parameter shall have traceable provenance. The implementation shall distinguish specification constants, specialization parameters, fitted parameters, nuisance parameters, calibration parameters, numerical parameters, initial or boundary data, random seeds, and presentation-only settings.

A parameter shall not silently change category during an analysis.

### RS-COMP008 — Dataset provenance

A dataset used for scientific comparison shall be identified by an immutable version, content hash, release identifier, or equivalent provenance mechanism. Preprocessing, filtering, unit conversion, masking, quality cuts, derived columns, missing-data treatment, and train/validation/test partitioning shall be recorded when applicable.

### RS-COMP009 — Artifact provenance

Every scientific output intended for publication or validation—including tables, figures, posterior samples, fitted parameters, benchmark summaries, and machine-readable result files—shall be traceable to the source revision, configuration, data, and execution that generated it.

Manual post-processing that changes scientific content shall be documented as part of the computational workflow.

### RS-COMP010 — Minimum reproducibility package

A quantitative result intended for external scientific evaluation shall provide, subject to lawful data-access restrictions:

1. versioned source code;
2. specification versions;
3. environment definition;
4. configuration files;
5. data acquisition or access instructions;
6. preprocessing scripts or exact transformation records;
7. random seeds or stochastic-state policy;
8. executable commands or workflow entry point;
9. tests required before scientific execution;
10. machine-readable outputs underlying reported figures and tables; and
11. integrity metadata for critical artifacts.

### RS-COMP011 — Reproduction modes

A project may distinguish:

- **bitwise reproduction** — identical serialized outputs;
- **numerical reproduction** — agreement within declared tolerances;
- **statistical reproduction** — agreement of declared distributional summaries or tests; and
- **scientific reproduction** — the same substantive conclusion under declared analysis criteria.

The required mode shall be stated explicitly.

### RS-COMP012 — Automated conformance checks

Repositories implementing RSMS specifications should execute automated checks on proposed changes, including applicable identifier, link, dimensional, unit, numerical, serialization, deterministic or seeded reproducibility, regression, type, and traceability checks.

A green continuous-integration result establishes only that the configured checks passed. It is not an empirical validation result.

### RS-COMP013 — Change classification

A change should be classified by scientific impact, distinguishing at least documentation-only changes, implementation refactors, numerical changes within tolerance, changes to defaults, changes to algorithms or inference procedures, changes to normative mathematical content, and changes that alter previously published scientific outputs.

### RS-COMP014 — Reference implementation status

A repository may designate one or more **reference implementations** for interoperability and reproducibility. Such designation means only that the implementation is an official computational realization of a specified version.

A reference implementation is subordinate to the written specification. A discrepancy shall be resolved explicitly by correcting the implementation or revising the specification through controlled change management.

### RS-COMP015 — Alternative implementation

An alternative implementation may claim conformance when it realizes the same normative interfaces and requirements within declared tolerances. Programming language, numerical library, hardware backend, storage model, or algorithmic formulation may differ unless constrained by the applicable specification.

### RS-COMP016 — Reproducible failure

A reproducible failure is a scientifically useful computational artifact. When a normative test, benchmark, correspondence check, or empirical comparison fails, the project shall retain sufficient information to reproduce the failure and determine whether it originates from implementation, numerical approximation, model assumptions, data, or the hypothesis itself.

### RS-COMP017 — No silent repair

A scientific result shall not be repaired by undocumented parameter changes, altered quality cuts, hidden regularization, changed seeds, post-hoc exclusions, or modified acceptance thresholds.

A change made during investigation that materially affects a scientific conclusion shall create a new traceable analysis version.

## 10.4 Verification

The family `RS-VER###` is reserved for software and numerical verification. Verification asks whether an implementation correctly realizes its declared mathematical and computational specification. It is not empirical validation.

### RS-VER001 — Verification plan

A scientifically material implementation shall declare a verification plan identifying applicable tests, reference cases, expected properties, tolerances, and failure criteria.

### RS-VER002 — Unit and component tests

Normative computational units shall be tested at the smallest practical scope. Tests shall exercise nominal behavior and, where applicable, domain boundaries, invalid inputs, singular cases, exceptional conditions, and declared invariants.

### RS-VER003 — Reference-case test

When a closed-form solution, independently evaluated value, limiting case, or trusted benchmark exists, an implementation should provide a reference-case test with explicit tolerances and reference provenance.

A result generated by the same code path under test shall not be presented as an independent reference.

### RS-VER004 — Convergence test

A discretized or iterative implementation shall test convergence with respect to the controlling numerical resolution when convergence is mathematically expected. The refinement parameter, comparison norm or statistic, convergence behavior, and stopping criterion shall be declared.

A stable-looking output at one resolution is not a convergence demonstration.

### RS-VER005 — Constraint and invariant residuals

When a model declares algebraic constraints, differential constraints, conservation statements, invariants, gauge conditions, or symmetry conditions, the implementation shall monitor applicable residuals and report acceptance thresholds.

### RS-VER006 — Regression test

A regression test compares an implementation with a versioned reference output to detect unintended changes. Updating a baseline solely because a test failed is nonconforming unless the change is reviewed and justified.

### RS-VER007 — Cross-implementation verification

Scientifically important calculations should, when practical, be reproduced by a computationally independent implementation, algorithm, or software stack under explicitly matched assumptions, inputs, units, and tolerances.

Shared numerical kernels or source components shall be disclosed when they materially reduce independence.

## 10.5 Operational validation requirements

The family `RS-VAL###` operationalizes `RS-M112` and `RS-M113`. It does not create new validation categories.

### RS-VAL001 — Validation evidence record

Every formal validation claim under RS-M112 shall be accompanied by a versioned evidence record identifying:

- the claim being evaluated;
- applicable RS-M113 category or categories;
- specification and model versions;
- implementation revision;
- reference, dataset, or experiment;
- observable or measurand;
- uncertainty treatment;
- criterion, statistic, threshold, or comparison rule;
- validation boundary;
- result; and
- limitations and unresolved discrepancies.

### RS-VAL002 — Mathematical-category evidence

When the mathematical category of RS-M113 is claimed, the record shall identify the proposition and the mathematical evidence used, such as proof, independently checked derivation, symbolic identity, well-posedness argument, or dimensional-consistency result.

Numerical evidence alone shall not be described as proof.

### RS-VAL003 — Numerical-category evidence

When the numerical category of RS-M113 is claimed, the record shall identify the applicable convergence, stability, reference-solution, residual, precision, sensitivity, benchmark, regression, or cross-implementation evidence and its acceptance thresholds.

Numerical-category success does not establish empirical adequacy of the underlying physical hypothesis.

### RS-VAL004 — Empirical-category evidence

When the empirical category of RS-M113 is claimed, the record shall identify the observational or experimental data, measurement model, uncertainty treatment, statistical or comparison criterion, applicable controls, and tested domain.

Empirical agreement outside the tested validation boundary shall not be inferred.

### RS-VAL005 — Independent reproduction record

A reproduction claim, consistent with RS-M113, shall state the category reproduced, independently created or controlled artifacts, conditions varied, comparison criterion, degree of independence, and unresolved discrepancies.

Independent reproduction is not equivalent to scientific acceptance.

### RS-VAL006 — Failure and null-result reporting

A conforming validation program shall preserve scientifically material failures, null results, unstable regimes, incompatible datasets, and adverse comparisons. Exclusion requires an explicit methodological justification traceable to declared criteria or quality controls.

### RS-VAL007 — Validation boundary

Every validation record shall define the variables, parameter ranges, scales, data regimes, approximations, and observables for which its evidence applies.

### RS-VAL008 — Comparison parity

A comparison between a resolutive model and another model shall satisfy RS-5. At minimum, the analysis shall document whether the models use equivalent datasets, preprocessing, calibration, nuisance treatment, priors or parameter bounds, train/test partitions, optimization budgets, model-selection criteria, and uncertainty propagation.

Any unavoidable asymmetry shall be declared and its likely effect assessed.

### RS-VAL009 — Parameter accounting

Model comparison shall distinguish physical, nuisance, calibration, latent, and numerically tuned parameters. Effective parameter count, prior volume, regularization, hyperparameter search, and dataset-specific tuning shall be reported when they affect the comparison.

### RS-VAL010 — Data separation and leakage control

When parameters, hyperparameters, model forms, stopping rules, or analysis decisions are informed by data, the analysis shall identify which data influenced those choices. Information leakage into a nominally held-out evaluation shall be reported as a validation defect.

### RS-VAL011 — Sensitivity and robustness analysis

A validation study should evaluate sensitivity to scientifically material choices, including applicable priors, calibration, nuisance models, selection cuts, initial conditions, numerical tolerances, discretization, optimizer or sampler settings, and alternative admissible data treatments.

### RS-VAL012 — Validation report

A validation report shall combine the applicable evidence records into a bounded scientific statement that cites RS-M112, identifies the RS-M113 category outcomes separately, states the validation boundary, and distinguishes implemented, verified, validated, reproduced, and unresolved status.

### RS-VAL013 — Claim language

Scientific reporting shall use qualified status language. In particular, `implemented`, `verified`, `mathematically validated`, `numerically validated`, `empirically validated within a declared domain`, `independently reproduced`, and `not validated` shall not be treated as synonyms.

Terms such as “confirmed,” “proved,” or “validated” without qualification should not be used where they obscure the actual evidence category.

## 10.6 Specialized specifications

A specialized specification may strengthen this chapter for its domain. For example, a cosmological specification may require particular likelihood or covariance checks; a galactic specification may require galaxy-level blocking; a lensing specification may require PSF and selection-function provenance; and a quantum specification may require hardware-calibration and sampling records.

A specialization shall not weaken a `shall` requirement without declaring the deviation and its justification.

## 10.7 Open methodological questions

The following remain open:

1. Which calculations require independent dual implementations before publication?
2. Which minimum reproduction mode is appropriate for stochastic and hardware-dependent computations?
3. Which validation records should become mandatory machine-readable artifacts?
4. How should computational cost and energy use be reported for fair algorithmic comparison?
5. Which benchmark suites should be normative for individual specialized specifications?
6. When is a surrogate or emulator sufficiently verified to replace a direct solver in a validation workflow?
7. How should model-discrepancy uncertainty be separated from measurement and numerical uncertainty in each specialized domain?
8. Which validation workflows should be preregistered for high-impact scientific claims?

## 10.8 Conformance checklist

| Requirement | Conformance condition |
|---|---|
| Specification identity | Exact RSMS and specialization versions are declared |
| Manifest | Code, environment, precision, configuration, data, and seeds are recorded |
| Traceability | Normative identifiers map to code, tests, and outputs |
| Data provenance | Dataset versions and transformations are reproducible |
| Artifact provenance | Figures, tables, and result files trace to executions |
| Verification | Unit, reference, convergence, residual, and regression tests are applied as relevant |
| Validation authority | RS-M112 and RS-M113 remain the canonical validation definitions |
| Validation boundary | Claims state the tested domain and observables |
| Comparison parity | Competing models receive symmetric methodological treatment |
| Parameter accounting | Fitted, nuisance, latent, calibration, and tuning parameters are disclosed |
| Leakage control | Data roles and information flow are documented |
| Robustness | Material analysis choices are sensitivity-tested where appropriate |
| Reproducibility | Required reproduction mode and package are declared |
| CI boundary | Automated-check success is not represented as empirical validation |
| Failure reporting | Material failures and null results are retained and reported |
| Claim language | Scientific status matches the strongest evidence actually obtained |

## 10.9 Chapter status

| Subject | Status |
|---|---|
| Computational conformance | Normative draft |
| Software and numerical verification | Normative draft |
| Operationalization of RS-M112/RS-M113 | Normative draft; Chapter 7 remains canonical |
| Symmetric model comparison | Normative draft |
| Reproducibility package | Normative draft |
| Reference implementations | Normative draft; implementation subordinate to specification |
| Domain-specific validation criteria | Deferred to specialized specifications |
| New physical hypotheses or equations | None introduced |
| Experimental validation of Resolutive Physics | Not asserted |

Chapter 10 is designated **RSMS 1.0-draft.10** as of **2026-08-07**. Its identifier families `RS-COMP001`–`RS-COMP017`, `RS-VER001`–`RS-VER007`, and `RS-VAL001`–`RS-VAL013` are reserved by this chapter. The `RS-VAL###` family operationalizes the canonical Chapter 7 validation framework and does not redefine it.
