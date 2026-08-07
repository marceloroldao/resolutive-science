# Chapter 10 — Computational Conformance and Validation

**Specification:** RSMS-1.0  
**Current RSMS version:** 1.0-draft.10  
**Chapter revision:** 1.0  
**Introduced in:** 1.0-draft.10  
**Status:** Normative draft — computational conformance and validation framework  
**Parent document:** `docs/RSMS/RSMS_v1.0.md`  
**Author:** Marcelo Roldão Matos

---

## 10.1 Chapter purpose

This chapter defines the common requirements by which a computational implementation, numerical experiment, benchmark, validation study, or reproducibility package may claim conformance with RSMS-1.0.

It establishes a traceable chain from normative mathematical content to software, configuration, data, execution, numerical verification, empirical comparison, and reported scientific conclusions. It introduces no new physical law, observable law, dynamical equation, or resolutive hypothesis.

The central principle is that **implementation, verification, validation, reproduction, and scientific interpretation are distinct activities**. Passing one category shall not be represented as passing another.

## 10.2 Scope and inherited requirements

This chapter inherits:

- the reproducibility, consistency, implementability, auditability, falsifiability, symmetric-comparison, and revision commitments of Chapter 1;
- the notation, numerical-tolerance, regularity, and discretization rules of Chapter 2;
- the primitive objects and canonical symbols of Chapter 3;
- the geometric and bundle declarations of Chapter 4;
- the field, operator, functional-space, and domain requirements of Chapter 5;
- the numerical and dynamical conformance requirements of Chapter 6;
- the measurement, inference, uncertainty, inverse-problem, and validation distinctions of Chapter 7;
- the dimensional, unit, normalization, and scaling requirements of Chapter 8; and
- the symmetry, invariance, compatibility-region, and correspondence requirements of Chapter 9.

A computational artifact shall not silently redefine an inherited object or stable identifier. Any intentional departure shall be documented as a nonconforming implementation, extension, proposed revision, or specialized specification.

## 10.3 Computational conformance identifiers

The family `RS-COMP###` is reserved for common computational-conformance definitions and requirements introduced by this chapter.

### RS-COMP001 — Conforming implementation

A **conforming implementation** is a versioned computational realization that declares the RSMS version and specialized specification version it implements and provides sufficient traceability to determine how each implemented normative object, equation, operator, constraint, observable, or procedure corresponds to its governing identifier.

Conformance means agreement with the declared specification within stated numerical and representational tolerances. It does not mean physical correctness or empirical validation.

### RS-COMP002 — Implementation manifest

Every conforming implementation shall provide an **implementation manifest** containing, at minimum:

1. specification version;
2. specialized specification version, when applicable;
3. source-code revision or immutable commit identifier;
4. implemented normative identifiers;
5. programming language and interpreter or compiler version;
6. dependency lock or equivalent environment description;
7. numeric precision and arithmetic mode;
8. hardware-relevant assumptions where numerical results depend materially on them;
9. configuration-file versions;
10. dataset identifiers and checksums when data are used;
11. random seeds or stochastic-state provenance when applicable; and
12. known deviations, unsupported features, and implementation limitations.

### RS-COMP003 — Traceability matrix

A conforming scientific implementation shall maintain a machine-readable or systematically auditable mapping

\[
\text{specification identifier}
\longleftrightarrow
\text{source implementation}
\longleftrightarrow
\text{tests}
\longleftrightarrow
\text{generated artifacts}.
\]

Where an identifier is intentionally not implemented, the traceability record shall state `not implemented`, `not applicable`, or an equivalent explicit status rather than omit the dependency silently.

### RS-COMP004 — Computational environment

The computational environment shall be sufficiently specified to reproduce the intended execution. This shall include dependency versions, platform assumptions, environment variables that affect numerical behavior, accelerator or backend selection when relevant, and external libraries whose behavior contributes materially to the result.

Container images, environment lock files, reproducible-build systems, or equivalent mechanisms should be used when practical. Their use does not eliminate the requirement to identify the specification and source revisions being executed.

### RS-COMP005 — Numeric representation

Every implementation shall declare the numeric representations used for normative quantities, including applicable floating-point format, complex representation, integer width, arbitrary precision, interval arithmetic, fixed point, or stochastic representation.

A change of numeric representation that can alter a reported result beyond its declared tolerance shall be treated as a material implementation change.

### RS-COMP006 — Determinism and stochastic reproducibility

A deterministic computation shall produce equivalent outputs within declared tolerances when executed under its declared reproducibility conditions.

A stochastic computation shall instead declare the pseudorandom generator or stochastic source, seed or state-management policy, sampling procedure, ensemble size, and statistical reproducibility criterion. Bitwise identity shall not be required when the declared target is distributional reproducibility.

### RS-COMP007 — Configuration provenance

Every parameter supplied to an execution shall have traceable provenance. The implementation shall distinguish at least:

- specification constants;
- specialization-defined parameters;
- fitted parameters;
- nuisance parameters;
- calibration parameters;
- numerical parameters;
- initial and boundary data;
- random seeds; and
- user-selected presentation parameters that do not affect the underlying computation.

A parameter shall not change category silently during an analysis.

### RS-COMP008 — Dataset provenance

A dataset used for scientific comparison shall be identified by an immutable version, content hash, release identifier, or equivalent provenance mechanism. The implementation shall record preprocessing, filtering, unit conversion, masking, quality cuts, derived columns, missing-data treatment, and train/validation/test partitioning where applicable.

An analysis performed on a modified dataset shall not cite the unmodified source dataset alone as if no transformation occurred.

### RS-COMP009 — Artifact provenance

Every scientific output intended for publication or validation—including tables, figures, posterior samples, fitted parameters, benchmark summaries, and machine-readable result files—shall be traceable to the source revision, configuration, data, and execution that generated it.

Manual post-processing that changes scientific content shall be documented as part of the computational workflow.

## 10.4 Verification identifiers

The family `RS-VER###` is reserved for numerical and software verification requirements.

### RS-VER001 — Software verification

**Software verification** asks whether the implementation correctly realizes its declared mathematical and computational specification. It is distinct from empirical validation.

Verification evidence may include unit tests, analytic reference cases, manufactured solutions, regression tests, dimensional checks, conservation or constraint residuals, property-based tests, symmetry checks, convergence studies, and independent implementations.

### RS-VER002 — Unit and component tests

Normative computational units shall be tested at the smallest practical scope. Tests shall exercise nominal behavior and, where applicable, domain boundaries, invalid inputs, singular cases, exceptional conditions, and declared invariants.

A passing unit test confirms only the tested implementation property under the tested conditions.

### RS-VER003 — Reference-case test

When a closed-form solution, independently evaluated value, limiting case, or trusted benchmark exists, an implementation should provide a reference-case test with explicit absolute and relative tolerances.

The provenance of the reference result shall be recorded. A result generated by the same code path under test shall not be presented as an independent reference.

### RS-VER004 — Convergence test

A discretized or iterative implementation shall test convergence with respect to the controlling numerical resolution when convergence is mathematically expected. The study shall identify the refinement parameter, norm or comparison statistic, expected or measured convergence behavior, and stopping criterion.

A stable-looking output at one resolution is not a convergence demonstration.

### RS-VER005 — Constraint and invariant residuals

When a model declares algebraic constraints, differential constraints, conservation statements, invariants, gauge conditions, or symmetry conditions, the implementation shall monitor applicable residuals and report acceptance thresholds.

An exact mathematical identity may be satisfied only approximately by a numerical implementation. The magnitude and scaling of the residual shall therefore be reported rather than described simply as “satisfied.”

### RS-VER006 — Regression test

A regression test compares an implementation with a versioned reference output to detect unintended changes. The reference output, tolerance, platform assumptions, and reason for any accepted update shall be recorded.

Updating a regression baseline solely because a test failed is nonconforming unless the change is reviewed and justified.

### RS-VER007 — Cross-implementation verification

When practical, scientifically important calculations should be reproduced by a computationally independent implementation, algorithm, or software stack. Agreement shall be assessed under explicitly matched mathematical assumptions, inputs, units, and tolerances.

Shared source code or shared low-level numerical kernels shall be disclosed when they materially reduce independence.

## 10.5 Validation identifiers

The family `RS-VAL###` is reserved for validation and scientific-comparison requirements.

### RS-VAL001 — Validation claim

A **validation claim** is a bounded statement that a declared model or prediction has been evaluated against an explicitly identified reference, observation, or experiment under specified criteria.

Every validation claim shall state:

- what is being validated;
- the validation category;
- the dataset or experiment;
- the observable or measurand;
- the uncertainty model;
- the comparison statistic or decision rule;
- the compatibility domain;
- competing or reference models when applicable;
- the result; and
- limitations of the claim.

### RS-VAL002 — Mathematical validation category

A result may be described as **mathematically validated** only relative to stated mathematical requirements, such as proof obligations, identities, domain conditions, conservation theorems, or independently checked derivations.

Numerical evidence alone shall not be described as a mathematical proof.

### RS-VAL003 — Numerical validation category

A computational result may be described as **numerically validated** only relative to declared numerical criteria such as convergence, reference solutions, residual thresholds, stability, sensitivity, or cross-implementation agreement.

Numerical validation does not establish that the underlying physical hypothesis is correct.

### RS-VAL004 — Empirical validation category

A prediction or model may be described as **empirically validated within a declared domain** only after comparison with observational or experimental data using a documented measurement model, uncertainty treatment, statistical criterion, and applicable controls.

The validation domain and tested observables shall be stated. Empirical agreement outside the tested domain shall not be inferred.

### RS-VAL005 — Independent reproduction

An **independent reproduction** is a repetition of a specified mathematical, numerical, or empirical result by an independent analyst, group, implementation, or workflow with sufficient independence to provide additional evidence beyond rerunning the originating artifact.

The degree of independence shall be described. Independent reproduction is not identical to scientific acceptance and does not require that every other validation category have been completed.

### RS-VAL006 — Failure and null-result reporting

A conforming validation program shall preserve and report scientifically material failures, null results, unstable regimes, incompatible datasets, and adverse comparisons. Excluding such results requires an explicit methodological justification traceable to prespecified criteria or documented quality controls.

### RS-VAL007 — Validation boundary

Every validation statement shall include a **validation boundary** identifying the variables, parameter ranges, scales, data regimes, approximations, and observables for which the evidence applies.

A claim shall not be generalized beyond that boundary without additional evidence or an explicitly labeled extrapolation.

## 10.6 Symmetric model comparison

### RS-VAL008 — Comparison parity

A comparison between a resolutive model and another model shall satisfy the symmetric-comparison commitment RS-5. At minimum, the analysis shall document whether the models use equivalent:

- datasets and quality cuts;
- preprocessing and calibration;
- nuisance-parameter treatment;
- priors and parameter bounds when Bayesian methods are used;
- train/test partitions where learning or tuning occurs;
- numerical precision and optimization budgets where relevant;
- model-selection criteria; and
- uncertainty propagation.

Any unavoidable asymmetry shall be declared and its likely effect assessed.

### RS-VAL009 — Parameter accounting

Model comparison shall distinguish physical, nuisance, calibration, latent, and numerically tuned parameters. Effective parameter count, prior volume, regularization, hyperparameter search, and dataset-specific tuning shall be reported where they affect the comparison.

A parameter shall not be omitted from complexity accounting merely because it is encoded indirectly in preprocessing or optimization.

### RS-VAL010 — Data separation and leakage control

When parameters, hyperparameters, model forms, stopping rules, or analysis decisions are informed by data, the analysis shall identify which data influenced those choices. Training, validation, calibration, and held-out test roles shall be separated when the scientific question requires out-of-sample assessment.

Information leakage into a nominally held-out evaluation shall be reported as a validation defect.

### RS-VAL011 — Sensitivity and robustness analysis

A validation study should evaluate sensitivity to scientifically material choices, including applicable priors, calibration, nuisance models, selection cuts, initial conditions, numerical tolerances, discretization, optimizer or sampler settings, and alternative admissible data treatments.

A result that exists only under a narrow undocumented choice shall not be presented as robust.

## 10.7 Reproducibility package

### RS-COMP010 — Minimum reproducibility package

A quantitative result intended for external scientific evaluation shall provide, subject to lawful data-access restrictions:

1. versioned source code;
2. specification and specialization versions;
3. environment definition;
4. configuration files;
5. data acquisition or access instructions;
6. preprocessing scripts or exact transformation records;
7. random seeds or stochastic-state policy;
8. executable commands or workflow entry point;
9. expected runtime-relevant resource assumptions when material;
10. tests required before scientific execution;
11. machine-readable outputs underlying reported figures and tables; and
12. checksums or equivalent integrity metadata for critical artifacts.

When an artifact cannot be redistributed, the package shall state the restriction and provide sufficient metadata for an authorized party to obtain or identify the same input.

### RS-COMP011 — Reproduction modes

A project may distinguish:

- **bitwise reproduction**, requiring identical serialized outputs;
- **numerical reproduction**, requiring agreement within declared tolerances;
- **statistical reproduction**, requiring agreement of declared distributional summaries or tests; and
- **scientific reproduction**, requiring the same substantive conclusion under the declared analysis criteria.

The required mode shall be stated. One mode shall not be substituted silently for another.

## 10.8 Continuous integration and automated conformance

### RS-COMP012 — Automated conformance checks

Repositories implementing RSMS specifications should execute automated checks on proposed changes. Applicable checks include:

- identifier uniqueness and reference resolution;
- formatting and documentation links;
- unit tests;
- dimensional tests;
- numerical reference tests;
- convergence or reduced regression tests;
- serialization and schema tests;
- deterministic or seeded reproducibility tests;
- static analysis and type checks when available; and
- generation of traceability or manifest records.

A green continuous-integration result establishes only that the configured automated checks passed. It is not a scientific validation result.

### RS-COMP013 — Change classification

A software or specification change shall be classified according to its potential scientific impact. At minimum, projects should distinguish:

- documentation-only changes;
- non-scientific implementation refactors;
- numerical changes within existing tolerance;
- changes to defaults or configurations;
- changes to algorithms or inference procedures;
- changes to normative mathematical content; and
- changes that alter previously published scientific outputs.

The required review and regression scope should increase with scientific impact.

## 10.9 Reference implementations

### RS-COMP014 — Reference implementation status

A repository may designate one or more **reference implementations** for interoperability and reproducibility. Such a designation means only that the implementation is an official computational realization of a specified version.

A reference implementation is not itself normative over the written specification. If the implementation and specification disagree, the discrepancy shall be resolved explicitly by correcting the implementation or revising the specification under controlled change management.

### RS-COMP015 — Alternative implementation

An alternative implementation may claim conformance when it realizes the same normative interfaces and requirements within declared tolerances. Programming language, numerical library, hardware backend, storage model, or algorithmic formulation may differ unless the applicable specification constrains them.

Implementation diversity is encouraged where it provides independent verification of scientifically important calculations.

## 10.10 Validation records and reporting

### RS-VAL012 — Validation record

Every formal validation claim shall be accompanied by a versioned validation record containing, at minimum:

| Field | Required content |
|---|---|
| Claim identifier | Stable local or publication identifier |
| Model | Model and specification version |
| Implementation | Source revision and environment |
| Data | Dataset or experimental record and version |
| Observable | Observable or measurand evaluated |
| Domain | Validation boundary and compatibility region |
| Uncertainty | Statistical and systematic treatment |
| Criterion | Metric, statistic, threshold, or comparison rule |
| Baselines | Reference or competing models when applicable |
| Result | Quantitative outcome with uncertainty |
| Robustness | Sensitivity analyses performed |
| Reproduction | Reproduction status and degree of independence |
| Limitations | Known exclusions, failures, and unresolved issues |

### RS-VAL013 — Claim language

Scientific reporting shall distinguish at least the following statements:

- **implemented** — code exists and executes;
- **verified** — declared software or numerical checks have passed;
- **mathematically validated** — stated mathematical criteria have been satisfied;
- **numerically validated** — stated numerical criteria have been satisfied;
- **empirically validated within a declared domain** — stated empirical criteria have been satisfied;
- **independently reproduced** — a declared result has been reproduced with stated independence; and
- **not validated** — the relevant validation has not been completed or did not pass.

Terms such as “confirmed,” “proved,” “verified experimentally,” or “validated” without qualification should not be used where they obscure the actual evidence category.

## 10.11 Failure handling and revision

### RS-COMP016 — Reproducible failure

A reproducible failure is a scientifically useful computational artifact. When a normative test, benchmark, correspondence check, or empirical comparison fails, the project shall retain sufficient information to reproduce the failure and determine whether it originates from implementation, numerical approximation, model assumptions, data, or the hypothesis itself.

### RS-COMP017 — No silent repair

A scientific result shall not be repaired by undocumented parameter changes, altered quality cuts, hidden regularization, changed seeds, post-hoc exclusions, or modified acceptance thresholds.

Any such change made during investigation shall create a new traceable analysis version and shall be disclosed when it materially affects the scientific conclusion.

## 10.12 Specialized specifications

A specialized specification may strengthen the requirements of this chapter for its scientific domain. For example, a cosmological specification may require specific likelihood validation; a galactic specification may require predefined train/test splits or galaxy-level blocking; a lensing specification may require PSF and selection-function provenance; and a quantum specification may require hardware-calibration and shot-noise records.

A specialization shall not weaken a `shall` requirement of this chapter without declaring the deviation and its justification.

## 10.13 Open questions

The following remain open methodological questions rather than settled physical assumptions:

1. Which calculations require independent dual implementations before publication?
2. Which minimum reproducibility mode is appropriate for stochastic and hardware-dependent computations?
3. Which validation records should become mandatory machine-readable artifacts?
4. How should computational cost and energy use be reported for fair algorithmic comparison?
5. Which benchmark suites should be normative for individual specialized specifications?
6. When is a surrogate or emulator sufficiently verified to replace a direct solver in validation workflows?
7. How should uncertainty from model discrepancy be separated from measurement and numerical uncertainty in each specialized domain?
8. Which parts of a validation workflow should be preregistered for high-stakes scientific claims?

## 10.14 Conformance checklist

| Requirement | Conformance condition |
|---|---|
| Specification identity | Exact RSMS and specialization versions are declared |
| Manifest | Code, environment, precision, configuration, data, and seeds are recorded |
| Traceability | Normative identifiers map to code, tests, and outputs |
| Data provenance | Dataset versions and transformations are reproducible |
| Artifact provenance | Figures, tables, and result files trace to executions |
| Verification | Unit, reference, convergence, residual, and regression tests are applied as relevant |
| Validation categories | Mathematical, numerical, and empirical claims remain distinct |
| Validation boundary | Claims state the tested domain and observables |
| Comparison parity | Competing models receive symmetric data and methodological treatment |
| Parameter accounting | Fitted, nuisance, latent, calibration, and tuning parameters are disclosed |
| Leakage control | Data roles and information flow are documented |
| Robustness | Material analysis choices are sensitivity-tested where appropriate |
| Reproducibility | Required reproduction mode and package are declared |
| CI boundary | Automated-check success is not represented as empirical validation |
| Failure reporting | Material failures and null results are retained and reported |
| Claim language | Scientific status matches the strongest evidence actually obtained |

## 10.15 Chapter status

| Subject | Status |
|---|---|
| Computational conformance | Normative draft |
| Software and numerical verification | Normative draft |
| Validation categories and records | Normative draft |
| Symmetric model comparison | Normative draft |
| Reproducibility package | Normative draft |
| Reference implementations | Normative draft; implementation is subordinate to specification |
| Domain-specific validation criteria | Deferred to specialized specifications |
| New physical hypotheses or equations | None introduced |
| Experimental validation of Resolutive Physics | Not asserted |

Chapter 10 is designated **RSMS 1.0-draft.10** as of **2026-08-07**. Its identifier families `RS-COMP001`–`RS-COMP017`, `RS-VER001`–`RS-VER007`, and `RS-VAL001`–`RS-VAL013` are reserved by this chapter. The chapter defines how computational and validation claims shall be documented and assessed; it does not establish which resolutive hypotheses are physically correct.
