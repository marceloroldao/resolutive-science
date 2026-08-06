# Chapter 5 — Fundamental Fields and Operators

**Specification:** RSMS-1.0
**Version:** 1.0-draft.5
**Status:** Normative draft — mathematical vocabulary only
**Parent document:** `docs/RSMS/RSMS_v1.0.md`

---

## 5.1 Purpose

This chapter defines the fields, operators, functional spaces, and algebraic operations that later RSMS chapters and specialized specifications may manipulate. It answers which mathematical objects are available, not how any object evolves.

The definitions are mathematical only. They introduce no equation of motion, variational principle, physical interpretation, measurement model, or claim about nature. In particular, naming an object “resolutive” reserves its role in the specification but does not assert its physical existence. Dynamics and variational principles belong to Chapter 6.

Unless stated otherwise, (M) is the smooth base manifold of RS-D001 and Chapter 4, \(E\to M\) is a declared smooth bundle, and \(\Gamma(E)\) denotes its smooth global sections. A specialization shall declare different regularity, local domains, additional geometric structure, or boundary conditions whenever they are needed.

---

## 5.2 Scalar fields

### RS-F001 — Scalar field

A real scalar field on (M) is a map

\[
f:M\longrightarrow\mathbb R.
\]

It assigns a real number to each point and is coordinate-independent as a map. Its expression in a chart is \(f\circ x^{-1}\). A complex or vector-valued scalar field may be introduced only with its codomain declared; it is not a real scalar field in the sense of this identifier.

### RS-F002 — Continuous and smooth scalar fields

The space of continuous real scalar fields is \(C^0(M,\mathbb R)\). The space of smooth real scalar fields is

\[
C^\infty(M)=C^\infty(M,\mathbb R).
\]

More generally, \(C^k(M,\mathbb R)\) contains fields with (k) continuous derivatives. Regularity shall not be inferred from the word “field”; it shall be stated or inherited from a cited definition.

---

## 5.3 Vector fields

### RS-F003 — Vector field

A smooth vector field is a smooth section of the tangent bundle,

\[
X\in\Gamma\(TM\),\qquad X(p)\in T_pM.
\]

This section-based definition is primary. In a chart, \(X=X^\mu\partial_\mu\), and its components transform by the differential of a coordinate transition. The component list alone is not the vector field.

Vector fields act as derivations on smooth scalar fields: \(X(f)\) is smooth, the action is real-linear, and \(X(fg)=X(f)g+fX(g)\).

---

## 5.4 Covector fields

### RS-F004 — Covector field and differential one-form

A smooth covector field, or differential one-form, is a section

\[
\alpha\in\Gamma(T^*M)=\Omega^1(M),\qquad \alpha_p:T_pM\to\mathbb R.
\]

The pairing with a vector field is the scalar field \(\alpha(X):p\mapsto\alpha_p(X_p)\). In local coordinates, \(\alpha=\alpha_\mu dx^\mu\), with covariant component transformation. The differential \(df\) of a smooth scalar field is the canonical one-form characterized by \(df(X)=X(f)\).

---

## 5.5 Tensor fields

### RS-F005 — Tensor field

For nonnegative integers \(r,s\), a type-\((r,s)\) tensor field is a declared-regularity section of the tensor bundle from RS-G007,

\[
T\in\Gamma(T^r_sM).
\]

At each point it is equivalently a multilinear map with \(r\) covector arguments and \(s\) vector arguments, subject to the index convention of Chapter 2. Scalars, vector fields, and covector fields are the cases \((0,0)\), \((1,0)\), and \((0,1)\), respectively.

### RS-F006 — Tensor transformation law

Under coordinates \(x^\mu\mapsto x^{\mu'}\), tensor components shall transform as

\[
T^{\mu'_1\ldots\mu'_r}{}_{\nu'_1\ldots\nu'_s}
=
\frac{\partial x^{\mu'_1}}{\partial x^{\mu_1}}\cdots
\frac{\partial x^{\mu'_r}}{\partial x^{\mu_r}}
\frac{\partial x^{\nu_1}}{\partial x^{\nu'_1}}\cdots
\frac{\partial x^{\nu_s}}{\partial x^{\nu'_s}}
T^{\mu_1\ldots\mu_r}{}_{\nu_1\ldots\nu_s}.
\]

An array not satisfying the applicable transformation law is not a tensor field. Symmetry, antisymmetry, density weight, complex structure, or distributional regularity shall be declared separately.

---

## 5.6 Bundle sections

### RS-F007 — Field as a bundle section

Consistently with RS-G012, a field valued in a bundle \(\pi:E\to M\) is a section \(s:M\to E\) satisfying

\[
\pi\circ s=\operatorname{id}_M.
\]

The notation \(\Gamma(E)\) means smooth global sections unless qualified. \(\Gamma(U,E|_U)\) denotes smooth local sections over an open \(U\subseteq M\). Continuous, \(C^k\), compactly supported, square-integrable, and distributional sections shall use explicit qualifiers.

Local representatives are related by the transition functions of (E). A choice of chart, frame, gauge, or trivialization represents a section but is not part of the invariant field unless the applicable specification declares it as additional data.

---

## 5.7 Resolutive field

### RS-F008 — Resolutive field

Let \(\pi_M:E_R\to M\) be the total state bundle of RS-D003, equivalently the resolutive state bundle specialized from RS-G017. A resolutive field is a section

\[
\Psi_R\in\Gamma(E_R),\qquad \pi_M\circ\Psi_R=\operatorname{id}_M.
\]

The notation \(\Psi_R\) supplies a field symbol for the object defined as a resolutive field in RS-D007; it does not replace the four-component state \(R\) of RS-D004 or alter any stable identifier. Its local value lies in the fiber \((E_R)_p\), and its local components, regularity, admissible range, and transition behavior shall follow Chapters 3 and 4.

**Scientific status:** mathematical representation of a **proposed resolutive hypothesis**. This definition supplies no dynamics and makes no assertion that nature uses or realizes \(\Psi_R\). Any physical interpretation belongs to a status-labeled specialized specification.

---

## 5.8 Projection operator

### RS-F009 — Projection operator signature specialization

Let \(\mathcal O\) be the observable space of RS-D006. The reserved projection operator has the mathematical signature

\[
\Pi:E_R\longrightarrow\mathcal O.
\]

RS-O001 is the canonical normative definition of \(\Pi\). RS-F009
cross-references and specializes that definition by recording its mathematical
signature; it does not define a distinct operator or change the meaning of
RS-O001. “Projection” names its intended mathematical role; idempotence,
linearity, orthogonality, continuity, differentiability, surjectivity, and
fiberwise action do not follow from the name and shall be declared when
applicable.

No measurement procedure, probabilistic rule, observer, uncertainty model, or physical interpretation is defined here. Those matters belong to Chapter 7 or a specialized specification.

---

## 5.9 Differential operators

The following are standard mathematical operators. Each requires the geometric structures stated in its definition; none is universally available on a bare smooth manifold merely because it is named here.

### RS-F010 — Gradient

Given a nondegenerate metric \(g\), the gradient of \(f\in C^\infty(M)\) is the vector field \(\operatorname{grad}f\) uniquely defined by

\[
g(\operatorname{grad}f,X)=df(X)
\]

for every vector field \(X\). Without a declared metric or equivalent musical isomorphism, a gradient is not defined.

### RS-F011 — Divergence

Given a connection \(\nabla\) on \(TM\), the divergence of a vector field is the contraction

\[
\operatorname{div}_\nabla X=\operatorname{tr}(Y\mapsto\nabla_YX).
\]

A volume form may alternatively define divergence through the Lie derivative of that volume form. A specialization shall state which definition and compatibility assumptions it uses.

### RS-F012 — Curl

On an oriented three-dimensional pseudo-Riemannian manifold with Hodge-star operator \(\star\), curl is the vector field determined by

\[
(\operatorname{curl}X)^\flat=\star d(X^\flat).
\]

The symbols \(\flat\) and \(\sharp\) denote the metric-induced identifications between vectors and covectors. In other dimensions, “curl” requires a separately declared generalization and codomain.

### RS-F013 — Laplacian

Given a pseudo-Riemannian metric, the Laplace–Beltrami operator on scalar fields is

\[
\Delta f=\operatorname{div}(\operatorname{grad}f).
\]

On differential forms, the Hodge Laplacian may be defined by \(\Delta_H=d\delta+\delta d\), with orientation, Hodge star, codifferential sign convention, domain, and boundary conditions declared. Sign conventions shall be explicit.

### RS-F014 — Exterior derivative

The exterior derivative is the unique graded derivation

\[
d:\Omega^k(M)\longrightarrow\Omega^{k+1}(M)
\]

that agrees with the differential on scalar fields and satisfies \(d^2=0\) and the graded Leibniz rule. It requires no metric or connection.

### RS-F015 — Covariant derivative

For a vector bundle \(E\to M\), a covariant derivative is the connection of RS-G024,

\[
\nabla:\Gamma(E)\longrightarrow\Gamma(T^*M\otimes E),
\]

with \(\nabla_Xs=(\nabla s)(X)\). Its action on tensor products and duals follows the Leibniz rule and contraction compatibility. A connection shall be specified; no canonical choice is presumed.

### RS-F016 — Lie derivative

For a vector field \(X\) with local flow \(\Phi_t\), the Lie derivative \(\mathcal L_X\) measures the infinitesimal pullback of a tensor field along that flow. On scalar fields and vector fields,

\[
\mathcal L_Xf=X(f),\qquad \mathcal L_XY=[X,Y].
\]

Its extension to tensor fields is the unique type-preserving derivation compatible with contractions. The parameter of a local flow is mathematical and shall not be interpreted as physical time without a separately labeled hypothesis.

---

## 5.10 Resolutive operators

### RS-F017 — Resolutive operator reservation

A resolutive operator is a declared map between specified spaces of resolutive or associated mathematical objects. The adjective “resolutive” adds no unstated algebraic, analytic, dynamical, or physical property. Every such operator shall declare its domain, codomain, regularity, required background structures, algebraic properties, and scientific status.

The following names are reserved for later modules:

1. **Projection operator** — a map of the form in RS-F009; no additional property is implied.
2. **Coherence operator** — an operator \(\mathcal C\) on a declared field or section space whose codomain and mathematical meaning of coherence shall be specified before use.
3. **Transport operator** — an operator \(\mathcal T_\gamma:E_{\gamma(a)}\to E_{\gamma(b)}\) assigned to an admissible path and declared connection or transport rule; this definition supplies no law of motion.
4. **Restriction operator** — the canonical map \(\operatorname{res}^U_V:\Gamma(U,E)\to\Gamma(V,E)\), \(s\mapsto s|_V\), for open sets \(V\subseteq U\).
5. **Composition operator** — ordinary composition \(A\circ B\) when the codomain of \(B\) lies in the domain of \(A\).

Only projection and restriction have complete meanings at this level. Coherence and transport shall not be used normatively until a later module supplies the missing data. No reserved operator is an equation or an evolution prescription.

---

## 5.11 Functional spaces

### RS-F018 — Smooth-function and section spaces

The space \(C^\infty(M)\) is a commutative real algebra under pointwise addition and multiplication. For a vector bundle \(E\to M\), \(\Gamma(E)\) is a module over \(C^\infty(M)\). Compactly supported spaces are denoted \(C_c^\infty(M)\) and \(\Gamma_c(E)\).

### RS-F019 — Banach space

A Banach space is a normed vector space \((B,\lVert\cdot\rVert)\) complete in the metric induced by its norm. A field space called Banach shall identify the norm, scalar field, completion, and any boundary or regularity conditions.

### RS-F020 — Hilbert space

A Hilbert space is an inner-product space \(H\) complete in the norm induced by its inner product. A field space called Hilbert shall identify its scalar field, inner product, measure or density where integration is used, and domain or boundary conditions. No quantum interpretation follows from Hilbert-space structure.

### RS-F021 — Distribution space

For a smooth manifold supplied with the density or volume data needed by the chosen convention, a scalar distribution is a continuous linear functional on a declared test-function space, commonly \(C_c^\infty(M)\). The notation \(\mathcal D'(M)\) may be used after the test-space topology and pairing convention are fixed. Distributional sections require the corresponding dual bundle and density conventions. This optional generalized regularity carries no physical interpretation.

---

## 5.12 Algebraic structure

### RS-F022 — Addition and scalar multiplication

Fields taking values in the same vector bundle may be added and multiplied by scalars fiberwise. Sections also admit multiplication by \(f\in C^\infty(M)\). Addition is not defined intrinsically for sections of a general nonlinear fiber bundle.

### RS-F023 — Composition

For maps \(B:A\to B_0\) and \(A_0:B_0\to C\), composition is \(A_0\circ B:A\to C\), evaluated right to left as specified by RS-D006. Operator sums, products, and compositions are defined only on a stated common domain, which may be a proper subspace for unbounded operators.

### RS-F024 — Tensor product

For tensor fields \(S\in\Gamma(T^r_sM)\) and \(T\in\Gamma(T^p_qM)\), their pointwise tensor product is

\[
S\otimes T\in\Gamma(T^{r+p}_{s+q}M).
\]

Tensor products of vector bundles and of their sections are understood fiberwise unless a completed topological tensor product is explicitly declared.

### RS-F025 — Commutator and anticommutator

For composable endomorphisms or operators \(A\) and \(B\) on a common invariant domain, the commutator and anticommutator are

\[
[A,B]=A\circ B-B\circ A,
\qquad
\{A,B\}=A\circ B+B\circ A.
\]

For vector fields, \([X,Y]\) denotes the Lie bracket and agrees with the commutator of their derivation actions. In graded settings, a specialization shall state whether graded signs replace these ungraded definitions. No dynamics or quantum interpretation follows from either operation.

---

## 5.13 Normative identifiers

### RS-F026 — Fundamental-field identifier family

The identifier family `RS-F###` is reserved for normative definitions and requirements concerning fundamental fields, field spaces, and operators in the RSMS. Identifiers are stable and shall not be reassigned. Extensions shall use the next available number or a specialization-specific family.

| Identifier range | Subject |
| --- | --- |
| `RS-F001`–`RS-F009` | Fields, sections, and projection signature |
| `RS-F010`–`RS-F016` | Standard differential operators |
| `RS-F017` | Resolutive operator reservation |
| `RS-F018`–`RS-F021` | Functional spaces |
| `RS-F022`–`RS-F025` | Algebraic operations |
| `RS-F026`–`RS-F028` | Identifier policy, conformance, and status |

---

## 5.14 Conformance

### RS-F027 — Field and operator conformance

A future chapter, specialized specification, or implementation conforming to this chapter shall:

1. cite every applicable `RS-F###` identifier;
2. declare each field's base, bundle or codomain, regularity, and local or global domain;
3. declare every operator's domain, codomain, common domain for compositions, and required geometric structures;
4. distinguish an invariant field or operator from its coordinate, frame, gauge, discretized, or numerical representation;
5. preserve the meanings of \(E_R\), \(R\), \(\Psi_R\), \(\mathcal O\), and \(\Pi\) established in Chapters 3–5;
6. state norms, inner products, measures, topologies, completions, boundary conditions, and operator domains whenever applicable;
7. label any resolutive physical interpretation as a hypothesis and any empirical conclusion as a validated result only when supported by declared validation;
8. avoid inferring dynamics, measurement rules, or physical existence from these mathematical definitions; and
9. place equations of motion and variational principles in Chapter 6 or a conforming later specification, not in this chapter.

---

## 5.15 Chapter status

### RS-F028 — Chapter 5 status

| Criterion | Status |
| --- | --- |
| Standard fields and bundle sections | Normative draft; standard mathematics |
| Differential operators | Normative draft; required background structures explicit |
| Resolutive field | Normative draft; mathematical representation of a proposed hypothesis |
| Projection operator | Signature only; measurement model deferred to Chapter 7 |
| Reserved resolutive operators | Names and type requirements only; later definitions required |
| Functional and algebraic structures | Normative draft; mathematical definitions only |
| Dynamics and variational principles | Not introduced; deferred to Chapter 6 |
| Physical or quantum interpretation | Not asserted |
| Experimental validation | Not asserted |
| Numerical implementation | Not introduced |

Chapter 5 is designated **RSMS 1.0-draft.5** as of **2026-08-06**. It provides the typed mathematical vocabulary on which Chapter 6 may define dynamics and variational principles without treating field existence, operator availability, or functional setting as implicit. Any future physical use remains subject to explicit scientific-status labeling.
