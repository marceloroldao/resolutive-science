# Appendix A — Canonical identifier registry

**Status:** Normative registry for RSMS-1.0-draft.10
**Scope:** Cross-chapter lookup; definitions remain normative in their cited chapters.

This registry does not redefine an identifier. The canonical chapter definition controls if a summary differs from its source.

## A.1 Core cross-chapter terms

| Term | Canonical identifier | Canonical meaning | Defined in |
|---|---|---|---|
| Resolutive state | RS-D004 | A fiber element represented by \(R=(\rho_R,\Theta_R,\iota_R,\kappa_R)\) | Chapter 3 |
| Resolutive address | RS-D005 | A separate identifier \(a_R\in\mathcal A_R\) | Chapter 3 |
| Observable space | RS-D006 | The codomain \(\mathcal O\) of observable outputs | Chapter 3 |
| Resolutive field | RS-D007 | A section denoted by \(\mathcal R_f\) | Chapter 3 |
| Observable | RS-P100 | The general observable projection framework specializing RS-O001 | Chapter 7 |
| Observable component | RS-P101 | A declared part of an output in \(\mathcal O\) | Chapter 7 |
| Observable projection operator | RS-O001 | The canonical map \(\Pi:E_R\to\mathcal O\) | Chapter 3 |
| Validation claim | RS-M112 | A bounded statement that identified evidence satisfies identified criteria on a declared domain | Chapter 7 |
| Independent validation categories | RS-M113 | Independent mathematical, numerical, and empirical validation categories | Chapter 7 |
| Conforming implementation | RS-COMP001 | A versioned computational realization traceable to its governing specification identifiers | Chapter 10 |
| Verification plan | RS-VER001 | Declared software and numerical verification scope, tests, tolerances, and failure criteria | Chapter 10 |
| Validation evidence record | RS-VAL001 | Operational evidence record supporting a validation claim under RS-M112 and RS-M113 | Chapter 10 |

The general term **observable** points to RS-P100, not to the narrower observable-component definition RS-P101. The terms **validation claim** and **validation categories** remain governed by Chapter 7; Chapter 10 operationalizes their computational evidence and reporting requirements.

## A.2 Chapter 10 identifier families

| Identifier family | Reserved purpose | Defined in |
|---|---|---|
| `RS-COMP001`–`RS-COMP017` | Computational conformance, provenance, reproducibility, CI, reference implementations, and failure handling | Chapter 10 |
| `RS-VER001`–`RS-VER007` | Software and numerical verification requirements | Chapter 10 |
| `RS-VAL001`–`RS-VAL013` | Operational evidence, comparison, robustness, and reporting requirements for applying RS-M112 and RS-M113 | Chapter 10 |

These families distinguish computational realization from verification and validation. A passing implementation or automated test shall not be represented as empirical validation unless the canonical Chapter 7 validation requirements and the applicable Chapter 10 evidence requirements are separately satisfied.
