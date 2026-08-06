# Chapter 2 — Mathematical Conventions and Notation

**Specification:** RSMS-1.0
**Current RSMS version:** 1.0-draft.10
**Chapter revision:** 1.0
**Introduced in:** 1.0-draft.2
**Status:** Normative draft — mathematical conventions
**Parent document:** `docs/RSMS/RSMS_v1.0.md`
**Author:** Marcelo Roldão Matos

---

## 2.1 Purpose

This chapter establishes the mathematical language used throughout the Resolutive Science Mathematical Specification and its specialized descendants.

Its purpose is to reduce ambiguity before primitive physical objects, state spaces, fields, operators, and dynamics are introduced. Every specialized specification shall either adopt these conventions or declare its deviations explicitly.

No physical claim is introduced in this chapter. The definitions below specify notation, domains, regularity assumptions, dimensional rules, index conventions, and standards for mathematical implementation.

---

## 2.2 Foundational mathematical domains

### RS-MATH001 — Real numbers

The symbol

\[
\mathbb{R}
\]

denotes the field of real numbers.

The subsets

\[
\mathbb{R}_{>0},\qquad \mathbb{R}_{\ge 0}
\]

denote the strictly positive and non-negative real numbers, respectively.

### RS-MATH002 — Complex numbers

The symbol

\[
\mathbb{C}
\]

denotes the field of complex numbers, with imaginary unit

\[
i^2=-1.
\]

For \(z\in\mathbb{C}\), the complex conjugate, modulus, real part, and imaginary part are written

\[
z^*,\qquad |z|,\qquad \operatorname{Re}(z),\qquad \operatorname{Im}(z).
\]

### RS-MATH003 — Natural numbers and index sets

The natural numbers are denoted by

\[
\mathbb{N}=\{0,1,2,\ldots\}.
\]

When indices begin at one, the notation

\[
\mathbb{N}_{>0}=\{1,2,3,\ldots\}
\]
shall be used.

A finite index set may be written as

\[
I_n=\{1,2,\ldots,n\}.
\]

### RS-MATH004 — Function spaces

Let \(X\) and \(Y\) be mathematical spaces. The set of functions from \(X\) to \(Y\) is denoted by

\[
Y^X=\{f\mid f:X\to Y\}.
\]

The space of \(k\)-times continuously differentiable functions is denoted by

\[
C^k(X,Y),
\]

and smooth functions by

\[
C^\infty(X,Y).
\]

Square-integrable functions on \(X\), with respect to a declared measure \(\mu\), are denoted by

\[
L^2(X,\mu).
\]

Whenever a measure is omitted, the applicable measure shall be clear from context or explicitly defined in the corresponding specialized specification.

---

## 2.3 Sets, mappings, and composition

### RS-MATH005 — Mapping notation

A mapping is written

\[
f:X\to Y,
\]

where \(X\) is the domain and \(Y\) is the codomain.

The image of \(x\in X\) is written \(f(x)\). The image and inverse image of sets are written

\[
f(A),\qquad f^{-1}(B),
\]

for \(A\subseteq X\) and \(B\subseteq Y\).

### RS-MATH006 — Composition

For maps

\[
f:X\to Y,
\qquad
g:Y\to Z,
\]

the composition is

\[
(g\circ f)(x)=g(f(x)).
\tag{RS-E001}
\]

Composition is read from right to left.

### RS-MATH007 — Identity map

The identity map on \(X\) is denoted by

\[
\operatorname{id}_X:X\to X,
\qquad
\operatorname{id}_X(x)=x.
\tag{RS-E002}
\]

### RS-R001 — Explicit domains

Every normative operator or mapping shall declare its domain and codomain either at first definition or in an associated metadata record.

---

## 2.4 Coordinate and index conventions

### RS-MATH008 — Spacetime indices

Unless otherwise stated, lowercase Greek indices from the middle of the alphabet,

\[
\mu,\nu,\alpha,\beta,\ldots,
\]
label spacetime components.

For a four-dimensional spacetime chart,

\[
\mu,\nu\in\{0,1,2,3\}.
\]

The coordinate \(x^0\) may be written as \(ct\) or \(t\), but the convention shall be declared explicitly because it changes dimensional bookkeeping.

### RS-D009 — Spatial indices

Lowercase Latin indices from the middle of the alphabet,

\[
i,j,k,\ell,\ldots,
\]
label spatial components. In three spatial dimensions,

\[
i,j,k\in\{1,2,3\}.
\]

### RS-D010 — Internal resolutive indices

Uppercase Latin indices,

\[
A,B,C,D,\ldots,
\]
shall be reserved for internal or resolutive-space components unless a specialized specification declares another use.

The range of internal indices is not fixed by this chapter and shall be defined by the structure in which they appear.

### RS-D011 — Layer, mode, or subsystem indices

Indices such as

\[
n,m,r,s
\]
may label layers, modes, subsystems, or discrete states. Their domain shall be stated explicitly.

### RS-R002 — Einstein summation convention

Repeated upper and lower indices are summed unless otherwise stated:

\[
A^\mu B_\mu
=
\sum_{\mu}A^\mu B_\mu.
\tag{RS-E003}
\]

Repeated indices in the same position shall not imply summation unless explicitly declared.

### RS-R003 — Free-index consistency

Both sides of a tensor equation shall contain exactly the same free indices in the same positions.

---

## 2.5 Scalars, vectors, tensors, and forms

### RS-D012 — Scalar

A scalar field on a manifold \(M\) is a map

\[
\phi:M\to\mathbb{K},
\]

where \(\mathbb{K}=\mathbb{R}\) or \(\mathbb{C}\).

### RS-D013 — Vector and covector

At \(p\in M\), a tangent vector belongs to the tangent space

\[
V_p\in T_pM,
\]

while a covector belongs to the cotangent space

\[
\omega_p\in T_p^*M.
\]

In local coordinates,

\[
V=V^\mu\partial_\mu,
\qquad
\omega=\omega_\mu\,dx^\mu.
\tag{RS-E004}
\]

### RS-D014 — Tensor

A tensor of type \((r,s)\) at \(p\) is an element of

\[
T_p^{(r,s)}M
=
\underbrace{T_pM\otimes\cdots\otimes T_pM}_{r}
\otimes
\underbrace{T_p^*M\otimes\cdots\otimes T_p^*M}_{s}.
\tag{RS-E005}
\]

Its components are written

\[
T^{\mu_1\ldots\mu_r}{}_{\nu_1\ldots\nu_s}.
\]

### RS-D015 — Differential form

A differential \(p\)-form is a totally antisymmetric covariant tensor field,

\[
\omega\in\Omega^p(M).
\]

The exterior product is denoted by \(\wedge\), and the exterior derivative by \(d\).

The exterior derivative satisfies

\[
d^2=0.
\tag{RS-E006}
\]

---

## 2.6 Metrics and signatures

### RS-D016 — Metric tensor

A metric on a manifold \(M\) is written

\[
g=g_{\mu\nu}\,dx^\mu\otimes dx^\nu.
\]

Its inverse satisfies

\[
g^{\mu\alpha}g_{\alpha\nu}=\delta^\mu{}_{\nu}.
\tag{RS-E007}
\]

### RS-D017 — Signature convention

The default spacetime signature of the RSMS is

\[
(-,+,+,+).
\tag{RS-E008}
\]

A specialized specification may use \((+,-,-,-)\), but shall declare the change explicitly and adjust all sign-sensitive expressions consistently.

### RS-D018 — Raising and lowering indices

Indices are raised and lowered with the applicable metric:

\[
V_\mu=g_{\mu\nu}V^\nu,
\qquad
V^\mu=g^{\mu\nu}V_\nu.
\tag{RS-E009}
\]

Internal indices shall be raised or lowered using the declared internal metric, provisionally denoted by

\[
\mathcal{I}_{AB}.
\]

The existence and physical interpretation of \(\mathcal{I}_{AB}\) will be specified in a later chapter.

---

## 2.7 Derivatives and connections

### RS-D019 — Partial derivative

The coordinate partial derivative is

\[
\partial_\mu
=
\frac{\partial}{\partial x^\mu}.
\]

### RS-D020 — Covariant derivative

The spacetime covariant derivative is denoted by

\[
\nabla_\mu.
\]

For a vector field,

\[
\nabla_\mu V^\nu
=
\partial_\mu V^\nu
+
\Gamma^\nu{}_{\mu\lambda}V^\lambda.
\tag{RS-E010}
\]

For a covector field,

\[
\nabla_\mu\omega_\nu
=
\partial_\mu\omega_\nu
-
\Gamma^\lambda{}_{\mu\nu}\omega_\lambda.
\tag{RS-E011}
\]

### RS-D021 — Internal covariant derivative

When an internal connection is present, the corresponding derivative shall be denoted provisionally by

\[
D_\mu.
\]

Its detailed form depends on the internal group, representation, and connection introduced later. A typical local form may be

\[
D_\mu
=
\partial_\mu+\mathcal{A}_\mu,
\tag{RS-E012}
\]

where \(\mathcal{A}_\mu\) is representation-valued. This expression is structural, not yet a physical axiom.

### RS-R004 — Derivative disambiguation

Whenever \(\partial_\mu\), \(\nabla_\mu\), and \(D_\mu\) coexist, the specification shall identify which geometric or internal connection each derivative uses.

---

## 2.8 Complex fields and phase conventions

### RS-D022 — Polar representation

A nonzero complex field may be represented as

\[
\Psi=\sqrt{\rho}\,e^{i\vartheta},
\tag{RS-E013}
\]

where

\[
\rho=|\Psi|^2\ge 0
\]

and \(\vartheta\) is a phase variable.

### RS-D023 — Resolutive phase symbol

The symbol

\[
\Theta_R
\]
shall denote a resolutive phase when such a phase is introduced by a later physical axiom.

The candidate representation

\[
\Psi_R=\sqrt{\rho_R}\,e^{i\Theta_R/2}\,\zeta_R
\tag{RS-E014}
\]

is reserved for later normative treatment. In this chapter it is registered only as a notation target and shall not yet be interpreted as an established physical equation.

### RS-R005 — Periodicity declaration

Every phase variable shall declare its equivalence relation. For example,

\[
\vartheta\sim\vartheta+2\pi
\]

or

\[
\Theta_R\sim\Theta_R+4\pi.
\]

A periodicity shall not be inferred solely from notation.

---

## 2.9 Operators

### RS-D024 — Linear operator

A linear operator \(\hat A:V\to W\) satisfies

\[
\hat A(av+bw)
=
a\hat A(v)+b\hat A(w)
\tag{RS-E015}
\]

for all admissible scalars \(a,b\) and vectors \(v,w\).

### RS-D025 — Commutator

The commutator of two operators is

\[
[\hat A,\hat B]
=
\hat A\hat B-\hat B\hat A.
\tag{RS-E016}
\]

### RS-D026 — Anticommutator

The anticommutator is

\[
\{\hat A,\hat B\}
=
\hat A\hat B+\hat B\hat A.
\tag{RS-E017}
\]

### RS-D027 — Adjoint

The adjoint of \(\hat A\) is denoted by \(\hat A^\dagger\) and is defined relative to a declared inner product:

\[
\langle u,\hat A v\rangle
=
\langle \hat A^\dagger u,v\rangle.
\tag{RS-E018}
\]

### RS-R006 — Operator metadata

Every normative operator shall declare:

- domain;
- codomain;
- linearity or nonlinearity;
- dimensional action;
- boundary conditions when relevant;
- adjoint or symmetry properties when relevant;
- numerical realization when implemented.

---

## 2.10 Inner products, norms, and expectation values

### RS-D028 — Inner product

An inner product is denoted by

\[
\langle u,v\rangle.
\]

For a complex vector space it is conjugate-linear in the first argument and linear in the second unless another convention is declared.

### RS-D029 — Norm

The induced norm is

\[
\|v\|
=
\sqrt{\langle v,v\rangle}.
\tag{RS-E019}
\]

### RS-D030 — Expectation value

For a normalized state \(|\Psi\rangle\) and operator \(\hat A\), the expectation value is

\[
\langle \hat A\rangle_\Psi
=
\langle\Psi|\hat A|\Psi\rangle.
\tag{RS-E020}
\]

This notation shall be used only where a Hilbert-space structure has been explicitly introduced.

---

## 2.11 Probability and statistical notation

### RS-D031 — Probability distribution

A probability density for a continuous variable \(x\) is denoted by

\[
p(x),
\qquad
p(x)\ge0,
\qquad
\int p(x)\,dx=1.
\tag{RS-E021}
\]

### RS-D032 — Conditional probability

Conditional probability is denoted by

\[
p(x\mid y).
\]

### RS-D033 — Likelihood

For data \(\mathcal D\), model \(\mathcal M\), and parameters \(\theta\), the likelihood is

\[
\mathcal L(\theta)
=
p(\mathcal D\mid\theta,\mathcal M).
\tag{RS-E022}
\]

### RS-D034 — Posterior

Bayes' theorem is written

\[
p(\theta\mid\mathcal D,\mathcal M)
=
\frac{p(\mathcal D\mid\theta,\mathcal M)p(\theta\mid\mathcal M)}
{p(\mathcal D\mid\mathcal M)}.
\tag{RS-E023}
\]

### RS-R007 — Statistical transparency

Every statistical result shall declare the likelihood, priors, nuisance parameters, data covariance treatment, numerical sampler, convergence diagnostics, and comparison metric used.

---

## 2.12 Dimensional notation

### RS-D035 — Physical dimension

The physical dimension of a quantity \(Q\) is denoted by

\[
[Q].
\]

The base SI dimensions are represented by

\[
\mathsf{M},\quad
\mathsf{L},\quad
\mathsf{T},\quad
\mathsf{I},\quad
\mathsf{\Theta},\quad
\mathsf{N},\quad
\mathsf{J},
\]

corresponding to mass, length, time, electric current, thermodynamic temperature, amount of substance, and luminous intensity.

### RS-D036 — Dimensionless quantities

A dimensionless quantity satisfies

\[
[Q]=1.
\]

Angles and phases are dimensionless, although radians may be retained as semantic unit labels.

### RS-R008 — Dimensional homogeneity

Every additive equation shall be dimensionally homogeneous. If

\[
A=B+C,
\]
then

\[
[A]=[B]=[C].
\tag{RS-E024}
\]

Arguments of exponential, logarithmic, and trigonometric functions shall be dimensionless.

### RS-R009 — Natural units

Natural units such as \(c=1\), \(\hbar=1\), or \(k_B=1\) may be used only when explicitly declared. Conversion back to SI or another declared physical unit system shall remain possible.

---

## 2.13 Approximation and equality symbols

The following symbols shall be distinguished:

- \(=\): exact equality within the adopted formalism;
- \(\equiv\): identity or definition;
- \(\approx\): numerical or asymptotic approximation;
- \(\propto\): proportionality;
- \(\sim\): equivalence relation, asymptotic behavior, or order relation, with meaning declared by context;
- \(\simeq\): approximate equivalence, to be used sparingly and defined when ambiguity is possible.

### RS-R010 — Numerical tolerance

A computational equality shall specify a tolerance where exact floating-point equality is not mathematically justified. A generic conformance condition may be written

\[
|x_{\mathrm{num}}-x_{\mathrm{ref}}|
\le
\varepsilon_{\mathrm{abs}}
+
\varepsilon_{\mathrm{rel}}|x_{\mathrm{ref}}|.
\tag{RS-E025}
\]

---

## 2.14 Boundary, initial, and normalization conditions

### RS-R011 — Condition declaration

A differential model shall declare all conditions required for a well-posed problem, including as applicable:

- initial conditions;
- boundary conditions;
- gauge conditions;
- normalization conditions;
- regularity assumptions;
- asymptotic conditions.

### RS-D037 — Initial condition

An initial condition may be written

\[
X(t_0)=X_0.
\tag{RS-E026}
\]

### RS-D038 — Boundary condition

A boundary condition on \(\partial\Omega\) may be written generically as

\[
\mathcal B[X]\big|_{\partial\Omega}=0,
\tag{RS-E027}
\]

where \(\mathcal B\) is the declared boundary operator.

---

## 2.15 Mathematical regularity and singularities

### RS-R012 — Regularity declaration

The minimum regularity class required by each equation shall be declared. For example, if second derivatives occur, the field should ordinarily belong to at least \(C^2\) locally unless weak derivatives are intended.

### RS-D039 — Singular set

For a field or operator undefined on a subset \(S\subset M\), the singular set shall be identified explicitly:

\[
\operatorname{Sing}(X)=S.
\]

### RS-R019 — Singular behavior

A singularity shall not be hidden by numerical clipping, regularization, or coordinate transformation. Any such treatment shall be documented and its physical and numerical consequences tested.

---

## 2.16 Discrete and continuous representations

### RS-D040 — Continuous field

A continuous field is written

\[
X:M\to V.
\]

### RS-D041 — Discrete approximation

A discrete approximation on nodes \(x_a\) is written

\[
X_a\approx X(x_a).
\tag{RS-E028}
\]

### RS-R020 — Discretization traceability

A numerical implementation shall distinguish the continuum equation from its discretization. The approximation order, grid or basis, timestep rule, convergence criterion, and stability restrictions shall be documented.

---

## 2.17 Coordinate-free and coordinate expressions

Coordinate-free definitions are preferred for universal geometric structures. Coordinate expressions shall be provided when required for implementation.

For example, a metric may be introduced abstractly as

\[
g\in\Gamma(T^*M\otimes T^*M),
\]

and locally as

\[
g=g_{\mu\nu}\,dx^\mu\otimes dx^\nu.
\]

### RS-R021 — Representation equivalence

When both forms are given, their equivalence shall be established or treated as a conformance test.

---

## 2.18 Symbol namespace

The following namespace is reserved provisionally for later RSMS chapters:

| Symbol | Intended role | Status |
|---|---|---|
| \(M\) | Base spacetime or physical manifold | Reserved |
| \(E_R\) | Resolutive total space | Reserved |
| \(\pi_M:E_R\to M\) | Bundle projection | Reserved |
| \(G_R\) | Internal resolutive group | Reserved |
| \(\Psi_R\) | Resolutive field or state field | Reserved |
| \(\rho_R\) | Resolutive density or depth variable | Reserved |
| \(\Theta_R\) | Resolutive phase | Reserved |
| \(\iota_R\) | Resolutive inclination variable | Reserved |
| \(\kappa_R\) | Resolutive curvature or turning variable | Reserved |
| \(\chi_R\) | Resolutive coherence field or measure | Reserved |
| \(\mathcal I_{AB}\) | Internal metric or inertial response metric | Reserved |
| \(\Pi_H\) | Horizontal projection operator | Reserved |
| \(\Pi_V\) | Vertical or internal projection operator | Reserved |

Registration does not confer physical meaning. Normative meaning shall be introduced only by explicit definitions and axioms in later chapters.

---

## 2.19 Conformance requirements

An RSMS-conformant mathematical statement shall satisfy, where applicable:

1. every symbol is defined;
2. every mapping has a declared domain and codomain;
3. every physical quantity has a declared dimension or is explicitly dimensionless;
4. every tensor equation has consistent free indices;
5. every derivative identifies its connection or coordinate meaning;
6. every approximation is distinguished from an exact identity;
7. every differential model declares sufficient conditions for evaluation;
8. every implemented equation has a numerical tolerance and test strategy;
9. every specialized convention documents departures from this chapter.

---

## 2.20 Chapter status

| Criterion | Status |
|---|---|
| Number systems and function spaces | Draft complete |
| Mapping and composition conventions | Draft complete |
| Index conventions | Draft complete |
| Tensor and differential-form notation | Draft complete |
| Metric signature | Draft complete |
| Derivative notation | Draft complete |
| Complex-field notation | Draft complete |
| Statistical notation | Draft complete |
| Dimensional rules | Draft complete |
| Numerical tolerance rule | Draft complete |
| Physical axioms introduced | Not yet |
| Empirical validation applicable | Not yet |

---

## Next chapter

**Chapter 3 — Primitive Objects and Resolutive State Space** will introduce the first physical definitions of Resolutive Physics, including the base manifold, the internal resolutive space, the distinction between physical state and resolutive address, and the minimum state variables required by the theory.
