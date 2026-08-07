# RSMS cross-chapter audit — 2026-08

## Scope and status

This audit makes targeted cross-chapter corrections; it does not broadly rewrite any chapter. Mathematical vocabulary in Chapter 4 is established mathematics. The use of that vocabulary for resolutive structures remains specification infrastructure, not a validated physical result.

## Namespace-only corrections

- Chapter 4 now uses the Chapter 3 canonical base, bundle, projection, state, field, and address symbols: \(M\), \(E_R\), \(\pi_M\), \(R\), \(\mathcal R_f\), and \(a_R\).
- Mechanical replacement damage in Chapter 4 was repaired, including missing spaces after relation and map commands and malformed function notation.
- Appendix A now directs the general term “observable” to RS-P100, while retaining RS-P101 for “observable component.”

## Normative corrections

The following meanings changed relative to the pre-audit Chapter 4 text:

| Identifier | Pre-audit meaning | Corrected meaning | Compatibility |
|---|---|---|---|
| RS-G018 | A “local resolutive state,” represented by a section named \(R\) | A local resolutive field \(\mathcal R_f:U\to E_R\), with \(\pi_M\circ\mathcal R_f=\operatorname{id}_U\) | **Not backward-compatible** for documents or code that treated \(R\) as a field; migrate the field symbol to \(\mathcal R_f\). State elements remain \(R\) under RS-D004. |
| RS-G019 | A “global resolutive state” section | A global resolutive field using \(\mathcal R_f\) | **Not backward-compatible** for uses of the old title or state/field conflation; use “global resolutive field.” |
| RS-G020 | An address comprising a base point together with fiber data | A distinct address \(a_R\in\mathcal A_R\); a representation may pair it with state as \((a_R,R)\) | **Not backward-compatible** for composite-address schemas; split address and state fields. |

These are normative Chapter 4 corrections, not namespace-only edits. They restore Chapter 4's conformance with the prior canonical definitions RS-D004, RS-D005, and RS-D007.

## Chapter 7 identifier-stability audit

The baseline is commit `c6edfa2`, which introduced the complete corrected Chapter 7, and the comparison target is this audit. All 35 Chapter 7 heading identifiers and their heading meanings are unchanged. No Chapter 7 identifier was added, removed, renamed, deprecated, or reassigned, and Chapter 7 was not substantively rewritten by this audit. Consequently, no Chapter 7 migration entry is required and Chapter 7 remains backward-compatible.

## Chapter 2 namespace migration

Chapter 2 formerly reused identifier families later assigned canonically in Chapter 3. The following migrations change identifiers, not meanings. They are not backward-compatible for direct identifier lookup; consumers shall update the identifier while retaining the same semantic content.

| Old identifier | Old meaning | Replacement identifier | New meaning | Reason | Compatibility status |
|---|---|---|---|---|---|
| RS-D001 | Real numbers | RS-N001 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D002 | Complex numbers | RS-N002 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D003 | Natural numbers and index sets | RS-N003 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D004 | Function spaces | RS-N004 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D005 | Mapping notation | RS-N005 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D006 | Composition | RS-N006 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D007 | Identity map | RS-N007 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D008 | Spacetime indices | RS-N008 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D009 | Spatial indices | RS-N009 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D010 | Internal resolutive indices | RS-N010 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D011 | Layer, mode, or subsystem indices | RS-N011 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D012 | Scalar | RS-N012 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D013 | Vector and covector | RS-N013 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D014 | Tensor | RS-N014 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D015 | Differential form | RS-N015 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D016 | Metric tensor | RS-N016 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D017 | Signature convention | RS-N017 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D018 | Raising and lowering indices | RS-N018 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D019 | Partial derivative | RS-N019 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D020 | Covariant derivative | RS-N020 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D021 | Internal covariant derivative | RS-N021 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D022 | Polar representation | RS-N022 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D023 | Resolutive phase symbol | RS-N023 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D024 | Linear operator | RS-N024 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D025 | Commutator | RS-N025 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D026 | Anticommutator | RS-N026 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D027 | Adjoint | RS-N027 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D028 | Inner product | RS-N028 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D029 | Norm | RS-N029 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D030 | Expectation value | RS-N030 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D031 | Probability distribution | RS-N031 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D032 | Conditional probability | RS-N032 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D033 | Likelihood | RS-N033 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D034 | Posterior | RS-N034 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D035 | Physical dimension | RS-N035 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D036 | Dimensionless quantities | RS-N036 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D037 | Initial condition | RS-N037 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D038 | Boundary condition | RS-N038 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D039 | Singular set | RS-N039 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D040 | Continuous field | RS-N040 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-D041 | Discrete approximation | RS-N041 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-R001 | Explicit domains | RS-N101 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-R002 | Einstein summation convention | RS-N102 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-R003 | Free-index consistency | RS-N103 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-R004 | Derivative disambiguation | RS-N104 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-R005 | Periodicity declaration | RS-N105 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-R006 | Operator metadata | RS-N106 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-R007 | Statistical transparency | RS-N107 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-R008 | Dimensional homogeneity | RS-N108 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-R009 | Natural units | RS-N109 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-R010 | Numerical tolerance | RS-N110 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-R011 | Condition declaration | RS-N111 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-R012 | Regularity declaration | RS-N112 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-R013 | Singular behavior | RS-N113 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-R014 | Discretization traceability | RS-N114 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-R015 | Representation equivalence | RS-N115 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E001 | Chapter 2 notation equation | RS-N201 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E002 | Chapter 2 notation equation | RS-N202 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E003 | Chapter 2 notation equation | RS-N203 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E004 | Chapter 2 notation equation | RS-N204 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E005 | Chapter 2 notation equation | RS-N205 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E006 | Chapter 2 notation equation | RS-N206 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E007 | Chapter 2 notation equation | RS-N207 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E008 | Chapter 2 notation equation | RS-N208 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E009 | Chapter 2 notation equation | RS-N209 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E010 | Chapter 2 notation equation | RS-N210 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E011 | Chapter 2 notation equation | RS-N211 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E012 | Chapter 2 notation equation | RS-N212 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E013 | Chapter 2 notation equation | RS-N213 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E014 | Chapter 2 notation equation | RS-N214 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E015 | Chapter 2 notation equation | RS-N215 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E016 | Chapter 2 notation equation | RS-N216 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E017 | Chapter 2 notation equation | RS-N217 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E018 | Chapter 2 notation equation | RS-N218 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E019 | Chapter 2 notation equation | RS-N219 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E020 | Chapter 2 notation equation | RS-N220 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E021 | Chapter 2 notation equation | RS-N221 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E022 | Chapter 2 notation equation | RS-N222 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E023 | Chapter 2 notation equation | RS-N223 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E024 | Chapter 2 notation equation | RS-N224 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E025 | Chapter 2 notation equation | RS-N225 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E026 | Chapter 2 notation equation | RS-N226 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E027 | Chapter 2 notation equation | RS-N227 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
| RS-E028 | Chapter 2 notation equation | RS-N228 | Unchanged | Remove cross-chapter namespace collision | Identifier lookup requires migration; semantic content is compatible |
