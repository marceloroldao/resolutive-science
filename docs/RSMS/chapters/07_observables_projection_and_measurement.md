# Chapter 7 — Observables, Projection, and Measurement

**Specification:** RSMS-1.0  
**Version:** 1.0-draft.7  
**Status:** Normative draft — observable and measurement framework  
**Parent document:** `docs/RSMS/RSMS_v1.0.md`

---

## 7.1 Chapter purpose

This chapter defines the common framework by which a latent resolutive state may be related to quantities eligible for comparison with data. It specifies observable descriptions, measurement vocabulary, forward and inverse problems, uncertainty, calibration, validation, traceability, and computational conformance. It does not select a universal physical observable, apparatus model, likelihood, or inference procedure.

The chapter preserves the distinction among:

1. **established mathematical or physical methods**, which may be used when their assumptions are declared;
2. **resolutive hypotheses**, including any particular physical interpretation or functional form assigned to an observable projection; and
3. **validated results**, which have passed explicitly documented mathematical, numerical, or empirical criteria.

Implementation, successful execution, and scientific acceptance are not interchangeable with validation.

## 7.2 Scope and inherited definitions

This chapter inherits the total state space \(E_R\), observable space \(\mathcal O\), and canonical observable projection operator \(\Pi\) from RS-D006 and RS-O001. It also inherits the operator signature recorded by RS-F009. Those identifiers retain their original meanings.

This chapter does not redefine \(\Pi\), append observables to the primitive state, or infer a measurement rule from a dynamical law. A specialization may introduce contextual inputs, response operators, noise, sampling, calibration, or inference, but shall declare them rather than silently placing them inside \(\Pi\).

## 7.3 Observable projection framework

### RS-P100 — Observable projection framework

RS-P100 specializes the canonical normative definition RS-O001 for the purposes of observable modeling and measurement. It does not create a second definition of \(\Pi\). Consistently with RS-O001 and the operator-signature specialization RS-F009,

\[
\Pi:E_R\longrightarrow\mathcal O.
\]

For a state \(R\in E_R\), the idealized observable output may be written

\[
o=\Pi(R),\qquad o\in\mathcal O.
\]

This notation identifies the latent-to-observable interface only. It does not imply linearity, idempotence, orthogonality, locality, injectivity, surjectivity, deterministic measurement, direct accessibility, or experimental validation.

Every specialization of RS-O001 shall declare:

1. the applicable domain, including any restriction \(D_\Pi\subseteq E_R\);
2. the codomain and component schema of \(\mathcal O\);
3. all state, background, parameter, and contextual dependencies;
4. units, coordinate and gauge behavior, and regularity;
5. whether the mapping is deterministic, stochastic, local, nonlocal, static, or history-dependent;
6. the scientific status of its physical content;
7. its implementation and validation status; and
8. known degeneracies, failure modes, and open questions.

**Scientific status:** the framework is normative mathematical infrastructure. A particular resolutive projection is a **resolutive hypothesis** unless supported by separately documented validation; no particular projection is validated by this chapter.

### RS-P101 — Observable component

An observable component is a declared coordinate, functional, tensor component, category, event, or other element used to describe part of an output in \(\mathcal O\). For an indexed observable schema one may write

\[
o=(o^a)_{a\in A}.
\]

The index set \(A\), component meanings, units, ranges, reference frames, transformation rules, and missing-value policy shall be stated. Components shall not be interpreted as statistically independent merely because they are separately indexed.

### RS-P102 — Derived observable

A derived observable is obtained from one or more outputs of \(\Pi\) through a declared map

\[
q=G(o;b,\eta),
\]

where \(b\) denotes declared background or contextual information and \(\eta\) denotes declared parameters. The definition, units, domain, uncertainty propagation, and status of \(G\) shall be recorded. A derived observable is not a primitive component of \(R\).

### RS-P103 — Observable family

An observable family is an indexed collection \(\{\Pi_\alpha\}_{\alpha\in I}\) of specializations of RS-O001. The indexing variable may represent an observable channel, scale, apparatus setting, resolution, epoch, or other declared context. A family shall state whether its members share a domain and codomain and whether comparisons between members require transport, rescaling, or calibration.

### RS-P104 — Contextual projection

When observable extraction depends on declared context \(c\in\mathcal C\), the specialization may use

\[
\Pi_c:E_R\longrightarrow\mathcal O_c
\]

or an explicitly curried equivalent. Context may include a frame, gauge, scale, apparatus configuration, selection rule, or environment. Context is not silently part of the primitive resolutive state, and its inclusion does not alter RS-O001.

### RS-P105 — Stochastic observable kernel

When observable output is intrinsically or operationally stochastic, a specialization may replace a point prediction by a probability kernel

\[
K_\Pi(\mathrm d o\mid R,c)
\]

on a declared measurable observable space. The probability space, conditioning variables, normalization, support, correlations, and sampling procedure shall be specified. This kernel is an added measurement-model structure associated with a specialization of RS-O001, not a redefinition of \(\Pi\).

### RS-P106 — Degeneracy and identifiability

A projection is degenerate on a declared domain when distinct admissible states produce observationally indistinguishable outputs under the applicable comparison rule. Identifiability of a state component or parameter shall be asserted only relative to a declared projection, measurement model, dataset, uncertainty model, and equivalence relation.

Non-injectivity of \(\Pi\) is admissible and shall not be hidden by an inference implementation.

## 7.4 Measurement vocabulary

### RS-M100 — Measurand

A **measurand** is the explicitly described quantity intended to be measured or inferred. Its definition shall identify the system, observable component, conditions, averaging or coarse-graining, reference frame, units, and applicable time or domain.

### RS-M101 — Measurement result

A **measurement result** is the reported value or distribution assigned to a measurand together with its unit, uncertainty representation, coverage or credibility convention, provenance, and quality flags. A bare numerical value is not a conforming measurement result.

### RS-M102 — Observation

An **observation** is a recorded datum or event produced by a declared acquisition process. Observations may be direct instrument records, processed data products, or categorical records. An observation is not automatically identical to \(\Pi(R)\); the connection requires a forward measurement model.

### RS-M103 — Instrument and apparatus model

An instrument or apparatus model is a declared map or stochastic kernel representing response, acceptance, resolution, sampling, filtering, saturation, dead time, or other acquisition effects. Its calibration domain and assumptions shall be stated. Apparatus behavior shall not be absorbed into a proposed physical projection without documentation.

### RS-M104 — Calibration

Calibration is the documented procedure that relates indications or raw records to reference quantities and estimates calibration parameters and uncertainties. A calibration record shall identify reference standards or datasets, validity intervals, fitted quantities, transformations, residuals, and versioned artifacts.

### RS-M105 — Resolution and sensitivity

Resolution describes the declared ability of a measurement process to distinguish nearby inputs under a stated criterion. Sensitivity describes the response of an output or statistic to a change in a declared input. Neither term shall be used without identifying the input, output, scale, criterion, and operating point or domain.

### RS-M106 — Accuracy, precision, bias, and error

The following terms shall remain distinct:

- **accuracy** concerns agreement with an accepted reference under stated conditions;
- **precision** concerns dispersion under stated repetition conditions;
- **bias** is a systematic displacement defined relative to a stated target and expectation rule; and
- **error** is a realized or modeled difference from a reference value, not a synonym for uncertainty.

These concepts shall not be claimed when the required reference or repetition model is absent.

### RS-M107 — Uncertainty model

An uncertainty model specifies the representation and propagation of incomplete knowledge or variability affecting a result. It shall declare sources, dependence and covariance, distributional assumptions or bounds, nuisance quantities, systematic effects, and the rule used to combine or propagate them.

Aleatoric variability, epistemic uncertainty, numerical error, approximation error, and model discrepancy should be represented separately whenever they can be distinguished.

### RS-M108 — Repeatability and reproducibility conditions

Repeatability concerns agreement under declared same-condition repetitions. Reproducibility concerns agreement under declared changed conditions, which may include operator, apparatus, implementation, laboratory, dataset, or analysis team. Every use of either term shall state the varied and controlled conditions and the comparison tolerance.

### RS-M109 — Detection and decision rule

A detection, exclusion, classification, or other decision shall be produced by a prespecified rule applied to declared data and a declared null, alternative, loss, or utility structure. Thresholds, multiple-testing treatment, selection effects, and error rates shall be reported. A decision rule does not by itself establish the physical interpretation of an observable.

### RS-M110 — Forward measurement model

A forward measurement model relates a state and declared auxiliary inputs to predicted data. A generic deterministic composition is

\[
\widehat d=\mathcal A\!\left(\Pi(R);c,\eta\right),
\]

where \(\mathcal A\) represents apparatus, sampling, preprocessing, or response effects. A stochastic model may instead specify

\[
p(d\mid R,c,\eta).
\]

Every stage of the composition shall be traceable. The model shall state which elements are established methods, resolutive hypotheses, calibrated quantities, or validated results.

### RS-M111 — Comparison and goodness criterion

A comparison criterion is a declared function, statistic, likelihood, distance, score, or decision rule comparing predicted and recorded data. Its assumptions, normalization, covariance treatment, nuisance handling, reference distribution, and acceptance or rejection thresholds shall be specified before interpreting the comparison.

### RS-M112 — Validation claim

A validation claim is a bounded statement that identified evidence satisfies identified criteria for a particular mathematical proposition, implementation, model output, or empirical comparison on a declared domain. It shall cite immutable or versioned artifacts and shall state limitations and unresolved discrepancies.

Validation of one claim shall not be generalized to a different equation, implementation, parameter range, observable, dataset, or physical interpretation without additional evidence.

### RS-M113 — Independent validation categories

Validation is organized into three **independent, non-linear categories**. None is a universal prerequisite, successor, or stronger level of either other category:

1. **Mathematical validation** assesses stated propositions through proof, counterexample search, symbolic checks, dimensional consistency, well-posedness analysis, or other declared mathematical criteria.
2. **Numerical validation** assesses an implementation or computed result through tests such as convergence, stability, conservation diagnostics, manufactured or analytic solutions, benchmark comparison, precision analysis, and regression checks.
3. **Empirical validation** assesses predictions against experimental or observational data using declared acquisition, uncertainty, statistical, and comparison procedures.

A claim shall identify separately which categories apply and the outcome in each. Mathematical validity does not establish numerical correctness or empirical adequacy; numerical agreement does not prove a theorem or establish empirical adequacy; empirical agreement does not by itself prove mathematical consistency, implementation correctness, uniqueness, or universal physical truth. A project may pursue the categories in any justified order or in parallel.

Independent reproduction may apply separately to a mathematical result, a numerical result, or an empirical result. A reproduction claim shall identify the category reproduced, the independently created or controlled artifacts, the conditions varied, the comparison criterion, and any unresolved discrepancy. Reproduction in one category shall not be reported as reproduction in another.

Scientific acceptance is a social and evidential judgment external to this technical classification. It is not a technical validation stage, does not follow automatically from completing any combination of these categories, and cannot be self-declared by an author, implementation, team, or specification.

## 7.5 Forward problems

A forward problem computes an observable or data prediction from a declared state, model, parameters, and context. A conforming forward problem shall identify:

1. the state representation and domain;
2. the specialization of RS-O001;
3. every background, parameter, and contextual input;
4. the apparatus, response, selection, and noise model when data are predicted;
5. the discretization and approximation choices;
6. the output schema, units, and uncertainty representation; and
7. the domain on which existence, uniqueness, and numerical reliability have been established or remain open.

Agreement between a forward-model output and data is evidence only under the declared comparison model. It does not make the latent state uniquely recoverable.

## 7.6 Inverse problems and inference

### RS-I100 — Inverse problem

An inverse problem seeks admissible states, parameters, model classes, or derived quantities consistent with recorded data under a declared forward model. Schematically,

\[
d\longmapsto \widehat{R},\widehat\eta,
\]

but this notation does not imply that \(\Pi^{-1}\) exists. An inverse method shall not present a selected representative as the unique physical state unless identifiability and uniqueness have been established on the declared domain.

### RS-I101 — Inverse solution set

The inverse solution set is the set or distribution of admissible inputs satisfying a declared comparison criterion. Empty, disconnected, nonunique, unstable, and only approximately determined solution sets are permitted outcomes and shall be reported rather than suppressed.

### RS-I102 — Regularization

Regularization introduces additional mathematical structure to stabilize or select among inverse solutions. The regularizer, penalty, constraint, prior, stopping rule, or reduced representation shall be explicit, including its units and weight. Regularization is an inference choice and shall not be described as observed physical structure without separate evidence.

### RS-I103 — Prior information

Prior information includes distributions, bounds, symmetries, constraints, external measurements, or model-selection assumptions supplied independently of the analyzed likelihood or comparison statistic. Its provenance and sensitivity shall be documented. A posterior or fitted result shall not be attributed solely to the data when it materially depends on prior information.

### RS-I104 — Likelihood and data model

A likelihood or data model shall specify the random variables, conditioning quantities, normalization, dependence structure, selection mechanism, censoring or missingness, and nuisance parameters. A convenient loss function shall not be called a likelihood unless a corresponding probabilistic model is declared.

### RS-I105 — Estimator and uncertainty output

An estimator maps data to a point, interval, region, distribution, or decision. Its target, sampling or posterior interpretation, optimization and stopping rules, uncertainty construction, coverage or calibration evidence, and failure behavior shall be stated.

### RS-I106 — Identifiability analysis

Structural and practical identifiability shall be distinguished. Structural identifiability concerns the idealized model and exact outputs; practical identifiability concerns finite, noisy, selected, or discretized data. Both depend on the declared model, domain, parameterization, context, and equivalence relation.

### RS-I107 — Model discrepancy and misspecification

Inference shall document known differences between the forward model and the represented physical or acquisition process. When discrepancy is modeled, its separation from measurement uncertainty and parameter effects shall be stated. A good fit under a misspecified model is not validation of the omitted assumptions.

### RS-I108 — Blinding and leakage control

When empirical decisions may be influenced by the target result, the analysis should declare blinding, holdout, preregistration, or other leakage controls. Training, calibration, tuning, validation, and final evaluation data shall be separated or overlaps explicitly justified.

## 7.7 Uncertainty propagation and reporting

For a declared transformation \(y=F(x)\), uncertainty propagation shall use a method consistent with the regularity, probability, interval, or ensemble structure actually assigned to \(x\). Linear covariance propagation may be used only when its approximation is justified. Nonlinear, multimodal, bounded, discontinuous, or heavy-tailed cases may require sampling, interval, profile, or other declared methods.

Reports shall include, as applicable:

- central estimates and their definition;
- uncertainty intervals or regions and their interpretation;
- covariance or dependence information needed for reuse;
- systematic, numerical, approximation, and model-discrepancy contributions;
- sensitivity to calibration, priors, preprocessing, and selection;
- units, significant digits, and reference conventions; and
- failed, censored, excluded, or missing observations and their treatment.

An uncertainty interval is not a validation status.

## 7.8 Traceability and provenance

Every implemented observable or measurement analysis shall maintain a traceability record connecting, when applicable:

| Record | Required content |
|---|---|
| Specification | RSMS version and stable identifiers, including the RS-O001 specialization |
| Hypothesis | Physical interpretation, assumptions, and scientific-status label |
| Implementation | Repository, revision, source path, environment, and dependencies |
| Configuration | Parameters, units, seeds, tolerances, and runtime options |
| Data | Persistent identifier, version, license or access conditions, and checksums |
| Processing | Acquisition, filtering, calibration, selection, and transformations |
| Output | Schema, units, uncertainty, quality flags, and artifact checksum |
| Validation | Applicable RS-M113 categories, criteria, evidence, outcomes, and limitations |
| Reproduction | Category reproduced, independent artifacts, comparison, and discrepancies |

Corrections to approved observable definitions or results shall preserve stable identifiers and document the reason, impact, and superseded version.

## 7.9 Computational conformance

### RS-C100 — Projection implementation

An implementation of a specialization of RS-O001 shall expose or record its input and output schemas, domain restrictions, units, dependencies, context, deterministic or stochastic behavior, error handling, precision, and specification identifier. It shall not label an arbitrary placeholder as the normative \(\Pi\).

### RS-C101 — Numerical tests

Applicable tests shall include:

1. schema, range, unit, and dimensional checks;
2. analytic, limiting, invariant, or manufactured cases;
3. convergence and stability checks across declared discretizations;
4. precision and conditioning analysis;
5. deterministic seed control or distributional tests for stochastic code;
6. regression tests tied to reviewed reference artifacts; and
7. explicit tests for rejected, missing, nonfinite, and out-of-domain inputs.

Passing these tests may support numerical validation under RS-M113; it does not by itself establish mathematical or empirical validation.

### RS-C102 — Reproducible execution

A quantitative result shall be regenerable within declared tolerances from versioned code, data, configuration, environment information, and an execution procedure. Differences caused by hardware, parallel reduction, stochastic sampling, or dependency versions shall be bounded or reported.

### RS-C103 — Machine-readable result record

A result record should include the specification version, stable identifiers, implementation revision, data identifiers and checksums, configuration checksum, timestamps, units, uncertainty metadata, quality flags, validation category, and artifact checksum. Serialization shall preserve sufficient precision and distinguish absent, invalid, censored, and not-applicable values.

### RS-C104 — Computational separation of stages

Software should keep latent-state construction, projection, apparatus response, noise, calibration, preprocessing, inference, and reporting as traceable stages. Fusion for performance is permitted only when the logical boundaries and tests remain documented.

## 7.10 Interpretation constraints

The following interpretations are nonconforming unless separately justified and status-labeled:

1. treating an observable as a primitive resolutive component;
2. treating the word “projection” as proof of linearity or idempotence;
3. calling an apparatus indication the exact value of \(\Pi(R)\) without a measurement model;
4. interpreting a fitted latent state as unique without identifiability evidence;
5. presenting calibration, regularization, priors, or preprocessing as laws of nature;
6. treating numerical precision as measurement accuracy;
7. promoting agreement on one dataset to universal physical validation;
8. reporting an implemented or reproduced result as scientifically accepted; or
9. combining mathematical, numerical, and empirical validation into a mandatory ladder.

## 7.11 Open questions

The following questions remain open and shall not be treated as resolved by this chapter:

1. Which observable components, if any, are universal across resolutive specializations?
2. What functional forms of specializations of RS-O001 are mathematically admissible and empirically discriminable?
3. When should context be represented in a projection, in an apparatus model, or in the state description?
4. Which projections are local, nonlocal, deterministic, stochastic, or history-dependent?
5. What degeneracies and equivalence classes arise between resolutive states and observable outputs?
6. Which datasets and experiments can distinguish resolutive hypotheses from established alternatives?
7. How should model discrepancy be separated from measurement and numerical uncertainty?
8. What calibration standards and reference materials are required for each specialization?
9. Which inverse problems are well posed or regularizable without imposing physically misleading structure?
10. What independent mathematical, numerical, and empirical reproductions are required for particular claims?
11. How should interoperable machine-readable observable and validation records be standardized?
12. What evidence, beyond technical validation, may eventually contribute to broader scientific acceptance?

## 7.12 Conformance checklist

An implementation, analysis, or specialized specification conforms to this chapter only if all applicable items below are satisfied.

| Requirement | Conformance condition |
|---|---|
| Canonical operator | RS-O001 remains the sole normative definition of \(\Pi\); RS-F009 and RS-P100 only specialize it |
| Observable schema | Components, domains, codomains, units, ranges, and transformation behavior are declared |
| Scientific status | Established methods, resolutive hypotheses, and validated results are labeled separately |
| Measurement model | Projection, apparatus response, sampling, selection, calibration, and noise are distinguished |
| Uncertainty | Sources, dependence, propagation, interpretation, and limitations are documented |
| Forward problem | Inputs, context, approximations, outputs, and reliability domain are declared |
| Inverse problem | Nonuniqueness, regularization, priors, likelihood, discrepancy, and identifiability are addressed |
| Validation | Mathematical, numerical, and empirical categories are assessed independently where applicable |
| Reproduction | The separately reproduced category, artifacts, conditions, and criterion are identified |
| Acceptance | Scientific acceptance is neither represented as a validation stage nor self-declared |
| Traceability | Specification, code, configuration, data, processing, outputs, and evidence are linked |
| Computation | Numerical tests, reproducible execution, failure handling, and result metadata are present |
| Stable identifiers | Existing identifiers retain their meanings and every correction is documented |
| Open questions | Unresolved assumptions, degeneracies, limitations, and required evidence are recorded |

## 7.13 Chapter status

| Criterion | Status |
|---|---|
| Observable projection interface | Normative draft specializing RS-O001 |
| Measurement vocabulary | Normative draft |
| Forward and inverse problem requirements | Normative draft |
| Validation classification | Normative draft; independent categories |
| Particular resolutive observable laws | Not specified; proposed hypotheses when introduced |
| Particular measurement or apparatus models | Not specified |
| Mathematical validation results | None declared by this chapter |
| Numerical validation results | None declared by this chapter |
| Empirical validation results | None declared by this chapter |
| Scientific acceptance | External judgment; not a technical stage and not self-declarable |

## 7.14 Identifier registry

| Identifier range | Content |
|---|---|
| `RS-P100`–`RS-P106` | Observable projection framework and observable definitions |
| `RS-M100`–`RS-M113` | Measurement vocabulary, forward comparison, and validation |
| `RS-I100`–`RS-I108` | Inverse problems and inference |
| `RS-C100`–`RS-C104` | Computational conformance |

RS-O001 remains the canonical normative definition of \(\Pi\). RS-F009 records its operator signature, and RS-P100 specializes its use in this chapter; neither identifier redefines it.

---

**End of Chapter 7**
