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
| Conforming implementation | RS-COMP001 | A versioned computational realization traceable to its governing specification identifiers | Chapter 10 |
| Software verification | RS-VER001 | Assessment that an implementation realizes its declared mathematical and computational specification | Chapter 10 |
| Validation claim | RS-VAL001 | A bounded, evidence-qualified statement comparing a declared model or prediction with an identified reference, observation, or experiment | Chapter 10 |

The general term **observable** points to RS-P100, not to the narrower observable-component definition RS-P101.

## A.2 Chapter 10 identifier families

| Identifier family | Reserved purpose | Defined in |
|---|---|---|
| `RS-COMP001`–`RS-COMP017` | Computational conformance, provenance, reproducibility, CI, reference implementations, and failure handling | Chapter 10 |
| `RS-VER001`–`RS-VER007` | Software and numerical verification | Chapter 10 |
| `RS-VAL001`–`RS-VAL013` | Mathematical, numerical, empirical, and independent validation requirements | Chapter 10 |

These families distinguish computational realization from verification and validation. A passing implementation or automated test shall not be represented as empirical validation unless the applicable `RS-VAL###` requirements are separately satisfied.
