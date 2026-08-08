# Appendix A — Canonical identifier registry

**Status:** Normative registry for RSMS-1.0-draft.12  
**Scope:** Cross-chapter lookup; definitions remain normative in their cited chapters.  
**Registry authority:** Chapter definitions are authoritative; this appendix is a synchronized normative index.

This registry does not redefine an identifier. The canonical chapter definition controls if a summary differs from its source. Identifier lifecycle and migration follow Chapter 11; registry governance follows Chapter 12.

## A.1 Core cross-chapter terms

| Term | Canonical identifier | Canonical meaning | Defined in |
|---|---|---|---|
| Base spacetime manifold | RS-D001 | The canonical base manifold `M` | Chapter 3 |
| Internal resolutive space | RS-D002 | The admissible minimal-state space `\mathcal R` | Chapter 3 |
| Total state space | RS-D003 | The total/resolutive state bundle `E_R` over `M` | Chapter 3 |
| Resolutive state | RS-D004 | A fiber element represented by `R=(\rho_R,\Theta_R,\iota_R,\kappa_R)` | Chapter 3 |
| Resolutive address | RS-D005 | A separate identifier `a_R\in\mathcal A_R` | Chapter 3 |
| Observable space | RS-D006 | The codomain `\mathcal O` of observable outputs | Chapter 3 |
| Resolutive field | RS-D007 | A section structurally denoted by `\mathcal R_f` | Chapter 3 |
| Derived quantity | RS-D008 | A quantity obtained by a declared map from primitive states, fields, backgrounds, or parameters | Chapter 3 |
| Observable projection operator | RS-O001 | The canonical map `\Pi:E_R\to\mathcal O` | Chapter 3 |
| Observable framework | RS-P100 | Observable-modeling specialization of RS-O001 | Chapter 7 |
| Observable component | RS-P101 | A declared part of an output in `\mathcal O` | Chapter 7 |
| Validation claim | RS-M112 | A bounded statement that identified evidence satisfies identified criteria on a declared domain | Chapter 7 |
| Independent validation categories | RS-M113 | Independent mathematical, numerical, and empirical validation categories | Chapter 7 |
| Conforming implementation | RS-COMP001 | A versioned computational realization traceable to its governing specification identifiers | Chapter 10 |
| Verification plan | RS-VER001 | Declared software and numerical verification scope, tests, tolerances, and failure criteria | Chapter 10 |
| Validation evidence record | RS-VAL001 | Operational evidence record supporting a validation claim under RS-M112 and RS-M113 | Chapter 10 |
| Specification version | RS-VSN001 | An explicit identifier for a fixed normative state of the RSMS | Chapter 11 |
| Extension | RS-EXT001 | A declared addition built on an identified parent specification without silently redefining inherited content | Chapter 11 |
| Deprecation | RS-DEP001 | Historical retention of an identifier or feature no longer recommended for new conforming work | Chapter 11 |
| Canonical registry set | RS-Z001 | Minimum registry architecture required by RSMS-1.0 | Chapter 12 |
| Canonical symbol | RS-Z006 | Preferred mathematical notation for a registered object in a declared scope | Chapter 12 |
| Resolutive-field notation compatibility | RS-Z010 | Compatibility rule for `R`, `\mathcal R_f`, and `\Psi_R` | Chapter 12 |
| Release-readiness record | RS-Z019 | Required readiness evidence for an RSMS release candidate/final release | Chapter 12 |

The general observable framework is RS-P100, while the canonical projection operator itself remains RS-O001. Validation claims and validation categories remain governed by Chapter 7; Chapter 10 operationalizes their computational evidence and reporting requirements.

## A.2 Identifier families by governing chapter

| Identifier family | Reserved purpose | Governing chapter |
|---|---|---|
| `RS-N###` | Mathematical conventions, notation, and notation requirements | Chapter 2 |
| `RS-D###` | Primitive/core definitions | Chapter 3 |
| `RS-E###` | Stable equation tags and dependency schemas where assigned | Chapters 2–3 and inherited use |
| `RS-O###` | Canonical observable/operator definitions | Chapter 3 |
| `RS-R###` | Cross-cutting requirements and primitive-state requirements where assigned | Chapters 2–3 |
| `RS-G###` | Geometric and bundle structure | Chapter 4 |
| `RS-F###` | Fields, functional spaces, and operators | Chapter 5 |
| `RS-V###` | Variational structures | Chapter 6 |
| `RS-Y###` | Dynamical evolution | Chapter 6 |
| `RS-C###` | Constraints and conservation | Chapter 6 |
| `RS-P###` | Observable projection framework | Chapter 7 |
| `RS-M###` | Measurement and validation vocabulary | Chapter 7 |
| `RS-I###` | Inverse problems and inference | Chapter 7 |
| `RS-DIM###` | Dimensional structure | Chapter 8 |
| `RS-U###` | Units | Chapter 8 |
| `RS-S###` | Scaling and normalization | Chapter 8 |
| `RS-SYM###` | Symmetry | Chapter 9 |
| `RS-INV###` | Invariance and covariance | Chapter 9 |
| `RS-COR###` | Correspondence and reduction | Chapter 9 |
| `RS-COMP###` | Computational conformance, provenance, reproducibility, and failure handling | Chapter 10 |
| `RS-VER###` | Software and numerical verification | Chapter 10 |
| `RS-VAL###` | Operational validation evidence and reporting | Chapter 10 |
| `RS-VSN###` | Versioning and compatibility | Chapter 11 |
| `RS-EXT###` | Controlled extensions and specialization inheritance | Chapter 11 |
| `RS-DEP###` | Deprecation, supersession, removal, and migration | Chapter 11 |
| `RS-Z###` | Registry, alias, appendix, cross-reference, and release-readiness governance | Chapter 12 |

## A.3 Lifecycle rule

Every identifier is governed by its defining clause. Once assigned, it shall not be silently reused for a different meaning. Deprecation, supersession, migration, and removal shall follow `RS-DEP001`–`RS-DEP008`, while registry synchronization shall follow `RS-VSN015` and Chapter 12.

A generated or summarized registry is subordinate to the normative source definition. A mismatch between this appendix and a governing chapter is a specification defect and a release-readiness failure until resolved.