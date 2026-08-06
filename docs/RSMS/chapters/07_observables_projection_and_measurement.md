# Chapter 7 — Observables, Projection, and Measurement

**Specification:** RSMS-1.0  
**Version:** 1.0-draft.7  
**Status:** Normative draft — observable and measurement framework  
**Author:** Marcelo Roldão Matos  
**Parent document:** `docs/RSMS/RSMS_v1.0.md`

---

## 7.1 Purpose and scientific status

This chapter defines the common mathematical and methodological framework by which declared states may be related to observable quantities, measurements, datasets, and scientific inferences. It preserves the objects, notation, and scope boundaries of [Chapters 2–6](../RSMS_v1.0.md#111-organization-of-the-rsms) and does not redefine the base manifold, total state space, resolutive state, bundles, fields, action, or dynamics.

The definitions in this chapter distinguish mathematical construction from empirical operation. They do not identify a particular resolutive state with nature, specify a physical form of the observable projection, or report an experimental result.

**Scientific status:** the measurement and inference vocabulary is a **mathematical and methodological framework**. The resolutive projection architecture is a **proposed resolutive hypothesis** whose explicit physical form is unknown. No interpretation, observable correspondence, reconstructed state, or scientific conclusion is declared experimentally validated here.

## 7.2 Scope and inherited notation

This chapter inherits:

- the mapping, probability, statistical, dimensional, and uncertainty conventions of [Chapter 2](02_mathematical_conventions_and_notation.md);
- the total resolutive state space \(E_R\), resolutive state \(R\), observable space \(\mathcal O\), and reserved map \(\Pi\) of [Chapter 3](03_primitive_objects_and_resolutive_state_space.md);
- the bundle and section structures of [Chapter 4](04_geometric_and_bundle_structure.md);
- the field and operator vocabulary, including the typed signature of \(\Pi\), of [Chapter 5](05_fundamental_fields_and_operators.md); and
- the admissible dynamics and status distinctions of [Chapter 6](06_dynamics_and_variational_principles.md).

Here and below, the symbol \(O\) may denote an individual observable quantity or value, while the calligraphic symbol \(\mathcal O\) denotes the observable space defined by RS-D006. The requested signature

\[
\Pi:E_R\longrightarrow O
\]

shall therefore be written normatively as

\[
\Pi:E_R\longrightarrow\mathcal O,
\]

so that its codomain is a space rather than an individual quantity. This is a notational clarification, not a change to RS-O001 or RS-F009.

The identifier range `RS-O100` onward is reserved in this chapter for **observable definitions**, while the existing `RS-O001` remains the observable projection operator established in Chapter 3. The ranges `RS-M100` onward and `RS-P100` onward are introduced for **measurement** and **projection** definitions, respectively. Existing stable identifiers retain their meanings.

## 7.3 Observable definitions

### RS-O100 — Observable quantity

An **observable quantity** is a mathematically defined quantity \(O\) with a declared domain \(\mathcal D_O\), codomain \(\mathcal C_O\), units or dimensionless status, and evaluation rule, whose values are eligible for comparison with the output of a declared measurement model.

Eligibility for comparison does not imply direct measurability, successful measurement, physical interpretation, or validation. Every observable shall be classified under RS-O101, RS-O102, or RS-O103 and shall declare whether it is measured, inferred, or reconstructed in a particular analysis.

### RS-O101 — Primitive observable

A **primitive observable** is an observable taken as an input datum by a declared model without first being computed from other observables within that model. “Primitive” is relative to the observable model and shall not be confused with the primitive resolutive state of RS-D004. A primitive observable is not automatically a primitive physical variable or a direct instrument reading.

### RS-O102 — Derived observable

A **derived observable** is an observable obtained from other declared observables or measured values through an explicit map

\[
O_d=f(O_1,\ldots,O_n;\lambda),
\]

with assumptions, parameters \(\lambda\), units, domain, codomain, and uncertainty propagation specified. It is a specialization of the derived-quantity schema RS-D008 and does not modify that definition.

### RS-O103 — Model-dependent observable

A **model-dependent observable** is an observable whose definition or reported value depends on a declared model, parameterization, calibration, prior, approximation, or reconstruction assumption. It shall be labeled model-dependent wherever reported, and its dependencies shall be traceable. Agreement involving such a quantity shall not be represented as a model-independent measurement.

### RS-O104 — Latent variable

A **latent variable** is a declared variable that is not directly present in the dataset and is estimated, constrained, or marginalized through a model relating it to observables. A resolutive state or any of its components may be treated as latent only within an explicitly status-labeled specialization. This definition makes no claim that such a latent variable exists physically or is uniquely identifiable.

### RS-O105 — Observable uncertainty

**Observable uncertainty** is a declared representation of limited knowledge about an observable value. It may be expressed by a standard uncertainty, covariance, probability distribution, interval, ensemble, bound, or other specified structure. Its sources, correlations, coverage or probability interpretation, propagation method, and units shall be stated. Uncertainty is not itself evidence of stochastic physical behavior.

### RS-O106 — Observable domain

The **observable domain** \(\mathcal D_O\) is the set of admissible inputs on which the evaluation rule for \(O\) is defined. It shall include applicable state restrictions, parameter ranges, spacetime or sampling support, regularity, calibration regime, and missing-data policy. Extrapolation outside \(\mathcal D_O\) shall be labeled.

### RS-O107 — Observable codomain

The **observable codomain** \(\mathcal C_O\) is the declared mathematical space containing possible values of \(O\). Its scalar, vector, tensor, categorical, functional, or probabilistic structure, units, coordinate convention, and admissible range shall be stated. A computational representation shall distinguish \(\mathcal C_O\) from the finite set of values actually observed.

### RS-O108 — Measurable quantity

A **measurable quantity** is an observable for which a declared protocol and instrument model define an operational route to data over a stated domain and resolution. Mathematical observability alone does not establish measurability. Measurability is conditional on the protocol, instrument, calibration, environment, and acceptance criteria.

### RS-O109 — Inferred quantity

An **inferred quantity** is a reported quantity estimated from a dataset through a declared statistical or computational inference procedure. It shall be distinguished from a direct recorded value and shall identify its likelihood or objective, assumptions, parameters, priors when applicable, uncertainty, and diagnostics.

### RS-O110 — Model-dependent reconstructed quantity

A **model-dependent reconstructed quantity** is an inferred quantity produced by solving an inverse problem under a declared forward model, regularization, parameterization, prior, or constraint. It shall not be described as directly measured, and alternative admissible reconstructions shall be documented when nonuniqueness is material.

## 7.4 Projection structure

### RS-P100 — Mathematical observable projection

The **mathematical observable projection** is the inherited map

\[
\Pi:E_R\longrightarrow\mathcal O.
\tag{RS-P100}
\]

For \(R_x\in E_R\), \(\Pi(R_x)\) is an element of the declared observable space. The map may be defined only on a declared subset of \(E_R\), in which case that restricted domain shall be explicit.

The symbol \(\Pi\) denotes **only a mathematical projection** in the RSMS. Its explicit physical form is unknown. The word “projection” does not imply linearity, idempotence, orthogonality, surjectivity, determinism, locality, losslessness, or physical realization. Equation RS-P100 restates RS-O001 and RS-F009 without replacing either stable identifier.

**Scientific status:** using a map from a proposed resolutive state space to observable space is a **proposed resolutive architecture**, not an experimentally validated correspondence.

### RS-P101 — Specialized projection

A **specialized projection** is a fully typed realization

\[
\Pi_s:\mathcal D_s\subseteq E_R\longrightarrow\mathcal O_s
\]

defined by a specialized theory. Different specialized theories may define different operators \(\Pi_s\). Each shall declare its functional or probabilistic form, inputs, outputs, parameters, units, regularity, invariances, scale and history dependencies, approximation regime, computational implementation, and scientific status. No specialized projection becomes part of the common RSMS merely through implementation.

### RS-P102 — Normative projection hierarchy

Every empirical claim derived from a projected state shall preserve the following ordered hierarchy:

\[
\boxed{\text{physical state}}
\;\longrightarrow\;
\boxed{\text{projection}}
\;\longrightarrow\;
\boxed{\text{measurement}}
\;\longrightarrow\;
\boxed{\text{dataset}}
\;\longrightarrow\;
\boxed{\text{inference}}
\;\longrightarrow\;
\boxed{\text{scientific conclusion}}.
\tag{RS-P102}
\]

In this hierarchy:

1. **physical state** means the state that a status-labeled model proposes to represent a system; the RSMS does not assert that \(E_R\) is physically realized;
2. **projection** maps the declared model state to a mathematical observable;
3. **measurement** applies an operational protocol and measurement model;
4. **dataset** records processed or unprocessed measurement outcomes with metadata;
5. **inference** estimates quantities or compares models from that dataset; and
6. **scientific conclusion** is a status-labeled assessment supported by the preceding stages.

These stages shall not be collapsed. In particular, a projected value is not a measurement, a measurement output without its provenance is not a conforming dataset, an inferred quantity is not a direct measurement, and a numerical fit is not by itself a scientific conclusion or experimental validation.

## 7.5 Measurement definitions

### RS-M100 — Measurement operator

A **measurement operator** is a declared mathematical map or stochastic kernel that relates an observable input to possible recorded outcomes:

\[
\mathsf M:\mathcal O\times\mathcal I\longrightarrow\mathcal Y
\]

in a deterministic representation, or

\[
K_{\mathsf M}(\,dy\mid O,I,\eta),
\]

in a stochastic representation. Here \(\mathcal I\) denotes declared instrument and protocol settings, \(\mathcal Y\) the outcome space, and \(\eta\) nuisance or noise parameters. Domain, codomain, units, calibration, resolution, and uncertainty shall be explicit. This operator models measurement; it is not the projection \(\Pi\) and does not imply a particular physical mechanism.

### RS-M101 — Measurement protocol

A **measurement protocol** is an operational specification of preparation or selection conditions, apparatus and configuration, calibration, acquisition sequence, environmental controls, sampling plan, preprocessing, quality criteria, and data retention. It shall be sufficiently detailed to permit independent execution or to identify precisely why execution cannot be reproduced.

### RS-M102 — Measurement uncertainty

**Measurement uncertainty** is the uncertainty assigned to a measurement result from declared statistical, systematic, calibration, sampling, resolution, and model contributions. Components and correlations shall be reported separately where they can be distinguished, followed by the declared combination or propagation rule.

### RS-M103 — Measurement resolution

**Measurement resolution** is the declared ability of a protocol and instrument model to distinguish changes in the measured quantity along specified dimensions. It may be expressed by bin width, response width, quantization, spatial or temporal support, detection threshold, or another operational metric. Resolution shall not be used as a synonym for uncertainty or accuracy.

### RS-M104 — Sampling

**Sampling** is the rule by which a finite or countable set of measurement instances is selected from a target domain or population. A sampling declaration shall state the sampling frame, selection mechanism, cadence or density, inclusion and exclusion criteria, dependence between samples, stopping rule, missingness, weights, and random seed when randomized.

### RS-M105 — Instrument model

An **instrument model** is a mathematical or computational representation of how an apparatus and its configuration transform an eligible observable into an outcome distribution or recorded value. It shall identify calibration parameters, response, sensitivity, resolution, saturation, selection effects, drift, preprocessing, validity domain, and uncertainty. The model shall be distinguished from the physical apparatus and from \(\Pi\).

### RS-M106 — Noise model

A **noise model** specifies the probabilistic or bounded deviations assigned to recorded outcomes conditional on the observable, instrument model, and protocol. It shall declare distributions or bounds, correlations, heteroscedasticity, stationarity assumptions, nuisance parameters, estimation procedure, and random-number generation where applicable. A noise model is an analysis assumption unless separately validated.

### RS-M107 — Systematic uncertainty

**Systematic uncertainty** is the component associated with effects that may shift, distort, or select results coherently under repeated application of the protocol. Its sources, direction when known, correlations, calibration evidence, nuisance treatment, sensitivity analysis, and mitigation shall be documented. Repetition alone shall not be assumed to reduce it.

### RS-M108 — Statistical uncertainty

**Statistical uncertainty** is the component associated with finite sampling or declared stochastic variation under the adopted data-generating model. Its estimator, sampling assumptions, correlations, and dependence on sample size shall be stated. Classification as statistical does not establish that the underlying physical process is intrinsically stochastic.

### RS-M109 — Posterior estimate

A **posterior estimate** is a summary or sample representation derived from the posterior distribution defined in RS-D034. It shall identify the likelihood, prior, parameterization, conditioning data, computational method, convergence diagnostics, and summary functional. A posterior mean, median, mode, or interval shall be named explicitly; “the posterior estimate” alone is insufficient.

### RS-M110 — Confidence interval

A **confidence interval** is an interval produced by a declared frequentist procedure with stated nominal coverage under repeated sampling and stated model assumptions. The construction, confidence level, nuisance treatment, and coverage evaluation shall be declared. It shall not be interpreted as a posterior probability interval.

### RS-M111 — Credible interval

A **credible interval** is an interval containing a declared posterior probability under a specified likelihood and prior. Its probability level, construction rule, parameterization, and posterior computation shall be stated. It shall not be represented as a frequentist confidence interval unless a separately demonstrated correspondence applies.

### RS-M112 — Dataset

A **dataset** is a versioned collection of recorded or processed outcomes, associated coordinates or indices, uncertainty information, quality flags, and provenance metadata. Raw, calibrated, reduced, simulated, and inferred data products shall be labeled and versioned separately. A dataset is not itself an inference or a scientific conclusion.

## 7.6 Inverse problems and state reconstruction

Many physical theories infer latent states from observables. Resolutive Science follows the same general methodological principle while making no claim that a resolutive latent state is physically correct or uniquely recoverable.

### RS-P103 — Inverse problem

Given a forward chain containing a projection and measurement model, an **inverse problem** seeks one or more latent states or parameters compatible with data \(D\), for example through

\[
\widehat R\in
\operatorname*{argmin}_{R\in\mathcal D}
\mathcal J\!\left(D,\mathsf M(\Pi(R))\right),
\]

or through a declared conditional distribution \(p(R\mid D,\mathcal H)\), where \(\mathcal J\) is an objective and \(\mathcal H\) collects model assumptions. This schema introduces no universal estimator. A specialization shall state identifiability, degeneracies, stability, data sufficiency, regularization, priors, constraints, approximation error, and sensitivity to model misspecification.

### RS-P104 — Inverse projection

An **inverse projection** is only a computational reconstruction map or procedure,

\[
\Pi^{-}_{\mathrm{rec}}:\mathcal D_{\mathrm{data}}\longrightarrow
\widehat{\mathcal E}_R,
\]

where \(\widehat{\mathcal E}_R\) is a declared estimate or representation space. The notation \(\Pi^{-}_{\mathrm{rec}}\) shall not be written as \(\Pi^{-1}\) unless a genuine mathematical inverse has been proved on the stated domain.

An inverse projection is **not** a guaranteed inverse mapping. It need not satisfy either inverse identity, and may be nonunique, set-valued, approximate, regularized, prior-dependent, or stochastic. Its output is a model-dependent reconstructed quantity under RS-O110, not a direct observation of \(R\).

### RS-P105 — State reconstruction

**State reconstruction** is the computational process of estimating a latent state from a dataset using a declared forward model, inverse method, constraints, and uncertainty treatment. It shall report reconstruction domain, identifiability, degeneracy, regularization or priors, numerical convergence, validation on suitable reference or synthetic cases, and sensitivity to perturbations. A reconstructed state shall be labeled as an inferred model output and shall not be described as experimentally observed.

## 7.7 Common framework and specialization boundary

The RSMS defines only the common observable, projection, measurement, and inference framework. Specialized modules—including cosmology, rotation-curve analysis, lensing, electromagnetism, quantum theory, and other domains—may define additional observables and specialized \(\Pi_s\) operators in their own specifications.

Such modules shall preserve inherited identifiers; fully define every added observable, measurement model, and projection; label all physical assumptions and validation status; and avoid presenting model-dependent reconstructions as direct measurements. This chapter introduces none of those domain-specific observables, physical laws, measurement postulates, or experiments.

## 7.8 Computational conformance

Every computational implementation of the chain in RS-P102 shall record and expose, as applicable:

1. **units** or explicit dimensionless status for inputs, intermediate quantities, outputs, uncertainties, and conversion factors;
2. **uncertainty propagation**, including correlations, approximation method, Monte Carlo error where used, and sensitivity to systematic contributions;
3. **reproducibility** instructions sufficient to regenerate the relevant data product, estimate, table, or figure within declared tolerances;
4. **traceability** from observables, projections, measurement models, inference procedures, and conclusions to stable identifiers, source paths, configurations, tests, and records;
5. **metadata** describing acquisition or generation context, schema, calibration, quality flags, selection, preprocessing, licenses or access constraints when applicable, and timestamps;
6. an immutable or content-addressed **dataset version**, together with checksums where feasible;
7. the **software version**, dependency environment, build information, and execution platform relevant to reproducibility;
8. all **random seeds**, pseudorandom algorithms, stream partitioning, and nondeterministic operations, or an explicit statement that deterministic reproduction is not available;
9. **parameter provenance**, including source, units, transformations, bounds, fixed or fitted status, priors, calibration, and version history; and
10. numerical precision, algorithms, stopping rules, tolerances, missing-data handling, and uncertainty-summary conventions.

Unavailable information shall be marked explicitly; it shall not be silently omitted. A computationally reproducible projection or reconstruction remains an implemented model output and is not thereby experimentally validated.

## 7.9 Normative validation hierarchy

### RS-M113 — Validation hierarchy

Claims shall be classified by the highest completed stage of the following ordered hierarchy:

\[
\boxed{\text{mathematical consistency}}
\;\longrightarrow\;
\boxed{\text{numerical verification}}
\;\longrightarrow\;
\boxed{\text{experimental validation}}
\;\longrightarrow\;
\boxed{\text{independent reproduction}}
\;\longrightarrow\;
\boxed{\text{scientific acceptance}}.
\tag{RS-M113}
\]

1. **Mathematical consistency** requires defined objects, compatible types, dimensions, assumptions, and logically coherent derivations.
2. **Numerical verification** requires evidence that an implementation solves or evaluates its stated mathematical problem within declared errors and tolerances.
3. **Experimental validation** requires comparison with appropriate measurement data under prespecified or transparently documented criteria, including uncertainty and competing explanations.
4. **Independent reproduction** requires an independent group or implementation to reproduce the relevant result from sufficiently complete specifications, software, data, and procedures.
5. **Scientific acceptance** is a broader, revisable community assessment and shall not be self-declared solely by the authors of a model or by this specification.

Completion of a later stage presupposes documented completion of the applicable earlier stages. Passing one stage shall not be described using the name of a later stage. No resolutive interpretation advances to experimental validation through mathematical consistency or numerical agreement alone.

## 7.10 Open questions

The following questions remain unresolved and shall not be treated as established assumptions:

1. Is \(\Pi\) linear?
2. Is \(\Pi\) stochastic?
3. Does \(\Pi\) depend on scale?
4. Does \(\Pi\) depend on coherence, and if so on which explicitly defined quantity?
5. Is \(\Pi\) history dependent?
6. Does \(\Pi\) change under coarse graining?
7. Do multiple physically admissible projections exist?
8. Are latent variables unique or identifiable from available observables?
9. On which subsets, if any, is a specialized projection injective, stable, or approximately reconstructible?
10. How shall projection uncertainty be separated from instrument, noise, and inference uncertainty?

## 7.11 Conformance checklist

| Requirement | Conforming declaration |
|---|---|
| Observable | Type, class, domain, codomain, units, evaluation rule, and uncertainty are declared |
| Status | Mathematical observable, measurable quantity, direct record, inference, and reconstruction are distinguished |
| Projection | \(\Pi_s\) is typed and its physical form and status are not overstated |
| Measurement | Operator, protocol, sampling, resolution, instrument, and noise models are documented |
| Uncertainty | Statistical and systematic components, correlations, propagation, and interval meanings are explicit |
| Dataset | Data-product level, metadata, version, quality information, and provenance are retained |
| Inference | Objective or likelihood, parameters, priors, diagnostics, uncertainty, and assumptions are declared |
| Inverse problem | Nonuniqueness, identifiability, regularization, stability, and model dependence are addressed |
| Hierarchy | Every claim preserves the RS-P102 projection hierarchy and RS-M113 validation hierarchy |
| Computation | Units, versions, seeds, tolerances, dependencies, and parameter provenance are recorded |
| Scope | No specialized observable, physical projection law, interpretation, or experiment is introduced |

## 7.12 Chapter status

| Subject | Status |
|---|---|
| Observable and measurement vocabulary | Normative draft; mathematical and methodological framework |
| Projection and inference hierarchies | Normative draft |
| Explicit physical form of \(\Pi\) | Unknown; deferred to status-labeled specialized theories |
| Inverse projection and reconstructed states | Computational, model-dependent procedures only |
| Specialized observables and experiments | Not introduced; deferred to specialized specifications |
| Experimental validation | Not asserted |

Chapter 7 is designated **RSMS 1.0-draft.7** as of **2026-08-06**. Its identifiers `RS-O100`–`RS-O110`, `RS-M100`–`RS-M113`, and `RS-P100`–`RS-P105` are stable and contiguous within their declared ranges. This chapter defines how observables, measurements, datasets, and inferences shall be related; it does not establish which projection nature follows or validate any resolutive interpretation.
