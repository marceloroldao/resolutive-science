# Appendix B — Canonical symbol registry

**Status:** Normative registry for RSMS-1.0-rc.1  
**Scope:** Universal RSMS symbols and cross-chapter aliases.  
**Authority:** Governing definitions in Chapters 2–12 remain authoritative.

This appendix implements the minimum symbol-governance requirements of Chapter 12. It does not introduce new mathematical or physical objects.

## B.1 Universal symbols

| Symbol | Name / role | Mathematical type | Governing definition | Scope / notes | Status |
|---|---|---|---|---|---|
| `M` | Base spacetime manifold | Smooth manifold | RS-D001 | Canonical universal base-space symbol | Active |
| `\mathcal R` | Internal resolutive space | Internal state space | RS-D002 | Space of admissible minimal states | Active |
| `E_R` | Total resolutive state space / bundle | Fiber bundle over `M` | RS-D003, RS-G017 | Typical fiber `\mathcal R` | Active |
| `\pi_M` | Resolutive bundle projection | Map `E_R\to M` | RS-D003 | Canonical bundle projection | Active |
| `R` | Resolutive state | Fiber element / ordered tuple | RS-D004 | Exactly four primitive components | Active |
| `\rho_R` | Resolutive density/depth | Real scalar coordinate | RS-D004 | Primitive state component | Active |
| `\Theta_R` | Resolutive phase | Phase coordinate | RS-D004 | Primitive state component; periodicity declared by specialization | Active |
| `\iota_R` | Resolutive inclination | Real scalar coordinate | RS-D004 | Primitive state component | Active |
| `\kappa_R` | Local resolutive curvature | Real scalar coordinate | RS-D004 | Not automatically spacetime curvature | Active |
| `a_R` | Resolutive address | Label/index/key | RS-D005 | Not part of `R` | Active |
| `\mathcal A_R` | Address space | Representation-dependent space | RS-D005 | Contains admissible addresses | Active |
| `\mathcal O` | Observable space | Declared observable codomain | RS-D006 | Model-dependent structure | Active |
| `\mathcal R_f` | Resolutive field | Section of `E_R\to M` | RS-D007 | Canonical structural field notation | Active |
| `\Psi_R` | Resolutive field-symbol alias | Section of `E_R\to M` | RS-F008, RS-Z010 | Alias for section-level role; no automatic quantum interpretation | Alias |
| `\Pi` | Observable projection operator | Map `E_R\to\mathcal O` | RS-O001, RS-F009 | No implied linearity, orthogonality, or idempotence | Active |
| `\Phi` | Dynamical field tuple | Model-dependent configuration | RS-V001 | Used only after fields are declared dynamical | Active |
| `\mathfrak C` | Configuration space | Declared functional/configuration space | RS-V002 | Structure depends on specialization | Active |
| `\mathcal S` | Action functional | Functional | RS-V003 | Optional variational framework | Active |
| `\mathcal L` | Lagrangian scalar/density context | Scalar or density context | RS-V004 | Exact transformation role must be declared | Active |
| `\mathfrak D` | Dynamical-law operator/schema | Declared map/operator | RS-Y001 | Generic dynamical architecture | Active |
| `U(\tau_2,\tau_1)` | Evolution operator | State-propagation map | RS-Y004 | Composition, invertibility, unitarity, etc. are not presumed | Active |
| `\operatorname{Red}` | Reduction map | Map between description spaces | RS-COR007 | Distinct from `R`, `\mathcal R`, and `\Pi` | Active |
| `\mathcal X_{\mathrm{source}}` | Source-description space | Declared mathematical space | RS-COR007 | Correspondence framework | Active |
| `\mathcal X_{\mathrm{target}}` | Target-description space | Declared mathematical space | RS-COR007 | Correspondence framework | Active |

## B.2 Reserved mathematical notation inherited from Chapter 2

The mathematical conventions of Chapter 2 remain authoritative. Common universal notation includes:

| Symbol | Meaning | Governing definition |
|---|---|---|
| `\mathbb R` | Real numbers | RS-N001 |
| `\mathbb C` | Complex numbers | RS-N002 |
| `\mathbb N` | Natural numbers | RS-N003 |
| `C^k(X,Y)` | `k`-times continuously differentiable maps | RS-N004 |
| `C^\infty(X,Y)` | Smooth maps | RS-N004 |
| `L^2(X,\mu)` | Square-integrable functions | RS-N004 |
| `\operatorname{id}_X` | Identity map on `X` | RS-N007 |
| `\partial_\mu` | Coordinate partial derivative | RS-N019 |
| `\nabla_\mu` | Spacetime/geometric covariant derivative | RS-N020 |
| `D_\mu` | Internal covariant derivative when declared | RS-N021 |

## B.3 Alias and collision rules

1. `R` shall not be used as a field map `M\to E_R`; it denotes a resolutive state element.
2. `\mathcal R` denotes the internal resolutive space and shall not be reused as a generic reduction map.
3. `\mathcal R_f` and `\Psi_R` are compatible section-level notations under RS-Z010. A derivation shall choose one consistently or state the alias transition.
4. `\Pi` is reserved for the observable projection role defined by RS-O001.
5. `\operatorname{Red}` is reserved for the abstract correspondence/reduction map of RS-COR007.
6. Specialized specifications may introduce local symbols only when they do not create unresolved ambiguity with active universal entries.

## B.4 Registry maintenance

Changes to this appendix shall be synchronized with the governing clauses under RS-VSN015 and Chapter 12. A symbol may be added without changing scientific content when it only indexes an already normative definition. A symbol reassignment that changes mathematical meaning is a semantic change and shall follow Chapter 11.

This registry is machine-verifiable through `tools/build_rsms_registries.py`, which generates the release-candidate symbol index from this table and records the governing RSMS version.