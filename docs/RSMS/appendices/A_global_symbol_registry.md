# Appendix A — Global Symbol and Terminology Registry

**Specification:** RSMS-1.0
**Current RSMS version:** 1.0-draft.10
**Chapter revision:** 1.0
**Introduced in:** 1.0-draft.10
**Status:** Normative registry — specification vocabulary
**Parent document:** `docs/RSMS/RSMS_v1.0.md`
**Author:** Marcelo Roldão Matos

---

## A.1 Registry authority

This registry is the authoritative global namespace for RSMS-1.0. A chapter shall not assign a competing symbol or meaning to a registered object. A specialization may introduce local symbols only when it declares their scope, type, relationship to this registry, and scientific status. This appendix consolidates existing definitions; it introduces no physical claim or equation.

| Symbol | Meaning | Mathematical type | Origin | Identifier | Scientific status |
|---|---|---|---:|---|---|
| \(M\) | Base spacetime manifold | Four-dimensional smooth manifold in the minimal construction | 3 | RS-D001 | Proposed foundational hypothesis as a physical carrier; established mathematics as a manifold |
| \(\mathcal R\) | Internal resolutive space | Declared four-coordinate internal space | 3 | RS-D002 | Proposed foundational hypothesis |
| \(E_R\) | Total resolutive state space | Fiber bundle over \(M\) | 3 | RS-D003 | Proposed foundational hypothesis |
| \(\pi_M\) | Bundle projection | Surjection \(E_R\to M\) | 3 | RS-D003 | Proposed foundational hypothesis |
| \(R\) | Resolutive state | Element of a fiber modeled on \(\mathcal R\) | 3 | RS-D004 | Proposed foundational hypothesis |
| \(a_R\) | Resolutive address | Element of declared address space \(\mathcal A_R\) | 3 | RS-D005 | Proposed foundational hypothesis |
| \(\mathcal R_f\) | Resolutive field | Section of \(\pi_M:E_R\to M\) | 3 | RS-D007 | Proposed foundational hypothesis |
| \(\mathcal O\) | Observable space | Declared codomain of observable descriptions | 3 | RS-D006 | Proposed foundational hypothesis as interface; no validated mapping implied |
| \(\Pi\) | Canonical observable projection | Map \(E_R\to\mathcal O\) | 3 | RS-O001 | Proposed foundational hypothesis; particular forms unvalidated |
| \(\rho_R\) | Resolutive depth coordinate | Scalar coordinate | 3 | RS-D004 | Proposed foundational hypothesis |
| \(\Theta_R\) | Resolutive phase coordinate | Element of declared phase space | 3 | RS-D004 | Proposed foundational hypothesis |
| \(\iota_R\) | Resolutive inclination coordinate | Real scalar coordinate | 3 | RS-D004 | Proposed foundational hypothesis |
| \(\kappa_R\) | Local resolutive curvature coordinate | Real scalar coordinate; not spacetime curvature | 3 | RS-D004 | Proposed foundational hypothesis |

## A.2 Normative terminology

| Term | Single normative meaning | Governing identifier |
|---|---|---|
| state | A resolutive state \(R\), unless a qualifier explicitly names a different mathematical state. | RS-D004 |
| address | Representation data that locate or identify a resolutive state; not a primitive component of \(R\). | RS-D005 |
| bundle | A locally trivialized fibered structure with declared base, projection, and typical fiber. | RS-G009 |
| field | A map or bundle section with explicitly declared domain, codomain, and regularity. | RS-F007 |
| projection | The observable-extraction role of \(\Pi\); it does not imply a linear, idempotent, or orthogonal projection. | RS-O001 |
| fiber | The inverse image of a base point under a declared bundle projection. | RS-G010 |
| observable | An eligible output description in \(\mathcal O\), not automatically a measurement result. | RS-P101 |
| coherence | A derived or specialized quantity; it is not a primitive state coordinate in RSMS-1.0. | RS-D008 |
| layer | An indexed model subdivision whose index set and semantics shall be declared; it is not a primitive object. | RS-D011 |
| phase | The periodic coordinate \(\Theta_R\), with period and equivalence relation explicitly declared. | RS-D004 |
| depth | The semantic role assigned to scalar coordinate \(\rho_R\); no unlabelled physical interpretation follows. | RS-D004 |
| curvature | Either geometric curvature under RS-G026 or, when qualified as *local resolutive curvature*, coordinate \(\kappa_R\); the two shall not be identified implicitly. | RS-G026 / RS-D004 |
| inclination | The semantic role assigned to scalar coordinate \(\iota_R\), with range and geometric meaning declared by a specialization. | RS-D004 |

## A.3 Namespace rule

The canonical base-manifold symbol is \(M\), not \(\mathcal M\). The canonical total space is \(E_R\), not \(\mathcal E_{\mathcal R}\). Chapter 4 bundle language shall be read as structural elaboration of \(E_R\), not as creation of a second total state space. The global symbols above are reserved; local uses of the same glyph for statistically conventional objects shall be qualified or confined to an explicitly declared local scope.

