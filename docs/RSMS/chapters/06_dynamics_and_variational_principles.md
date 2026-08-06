# Chapter 6 — Dynamics and Variational Principles

**Specification:** RSMS-1.0  
**Version:** 1.0-draft.6  
**Status:** Normative draft — admissible dynamical architecture  
**Parent document:** `docs/RSMS/RSMS_v1.0.md`

---

## 6.1 Chapter purpose

This chapter defines the admissible mathematical forms in which dynamics may be stated in Resolutive Science. It establishes common requirements for configurations, actions, equations of motion, evolution maps, constraints, conservation statements, initial and boundary data, and numerical realizations. It deliberately does not select a universal physical law.

The chapter preserves four distinct scientific statuses:

1. **mathematical framework** — standard or generic machinery available for constructing a model;
2. **proposed resolutive dynamics** — an explicitly identified, unvalidated physical hypothesis using that machinery;
3. **implemented model** — a computational realization traceable to a proposed law and its declared choices; and
4. **validated result** — an output evaluated under declared empirical or mathematical validation criteria.

Moving from one status to another shall require explicit evidence and documentation. In particular, implementation is not validation.

## 6.2 Scope boundary and inherited objects

This chapter uses the base manifold \(\mathcal M\), internal space \(\mathcal R\), total state space \(E_R\), state \(R\), observable space \(\mathcal O\), and projection \(\Pi\) with the meanings established in Chapters 3–5. It uses the bundles, sections, metrics, connections, fields, and operators of Chapters 4–5 only when they have been declared for the applicable model. It neither changes their definitions nor assumes that every optional structure exists.

This chapter does not introduce cosmological, galactic, lensing, electromagnetic, or quantum-specific dynamics. Such laws belong in specialized specifications. A symbol introduced here is not a claim that the corresponding object exists in nature.

## 6.3 Variational definitions

### RS-V001 — Admissible configuration

An admissible configuration is a declared tuple of dynamical fields

\[
\Phi=(\Phi^A)_{A\in I}
\]

on \(\mathcal M\), where each \(\Phi^A\) is a section of a specified bundle from the vocabulary of Chapters 3–5 and satisfies declared regularity, domain, boundary, range, reality, and constraint conditions. The index set \(I\) shall be declared and may include \(\Psi_R\) only when the specialization explicitly makes the resolutive field dynamical. Prescribed backgrounds and external sources are not components of \(\Phi\).

### RS-V002 — Configuration space

For declared bundles \(E_A\to\mathcal M\), the configuration space is a specified subset

\[
\mathfrak C\subseteq\prod_{A\in I}\Gamma_{r_A}(E_A),
\]

where each \(\Gamma_{r_A}(E_A)\) denotes the chosen regularity class of sections. The topology, norm or other functional structure, boundary conditions, and incorporated constraints shall be stated. The notation \(\mathfrak C\) alone does not imply linearity, completeness, or a Hilbert-space structure.

### RS-V003 — Action functional

When a variational formulation is selected, an action is a functional

\[
\mathcal S:\mathfrak C\longrightarrow\mathbb R
\quad\text{or}\quad
\mathcal S:\mathfrak C\longrightarrow\mathbb C
\]

of the generic form

\[
\mathcal S[\Phi;g,J,\lambda]=
\int_{\mathcal M}
\mathcal L(\Phi,\nabla\Phi,g,J;\lambda)\,dV_g.
\]

Here \(\Phi\) denotes the declared dynamical fields, \(g\) the available geometric structure, \(J\) external sources or prescribed background data, \(\lambda\) model parameters, and \(dV_g\) a declared volume element. If the metric does not define the measure, another declared density or measure shall replace \(dV_g\). The domain of integration and convergence conditions shall be explicit.

**Scientific status:** an action is an admissible **mathematical framework**. Any particular resolutive action is a **proposed resolutive dynamics** unless a stronger status is separately established; none is declared experimentally validated here.

### RS-V004 — Lagrangian density

The Lagrangian density \(\mathcal L\,dV_g\) is the integrable top-degree density defining \(\mathcal S\). A specialization shall declare all field dependencies, derivative order, locality, parameters, sources, backgrounds, symmetry properties, units, and explicit dependence on position or an evolution parameter. The scalar \(\mathcal L\) and the density \(\mathcal L\,dV_g\) shall not be conflated when their transformation properties differ.

### RS-V005 — Stationary-action condition

For every admissible variation \(\delta\Phi\), stationarity means

\[
\delta\mathcal S[\Phi;\delta\Phi]=0.
\]

The principle of stationary action is permitted by the RSMS as a **mathematical framework**; it is not an experimentally established resolutive law. A specialization choosing it as physical dynamics shall label that choice as a proposed hypothesis and state its admissible variations and boundary policy.

### RS-V006 — Euler–Lagrange operator

For a local first-derivative Lagrangian with sufficient regularity and unconstrained interior variations, the Euler–Lagrange operator has components

\[
\mathcal E_A(\mathcal L)=
\frac{\partial\mathcal L}{\partial\Phi^A}
-\nabla_\mu\!\left(
\frac{\partial\mathcal L}{\partial(\nabla_\mu\Phi^A)}
\right),
\]

and the corresponding generic field equation is

\[
\frac{\partial\mathcal L}{\partial\Phi^A}
-\nabla_\mu\!\left(
\frac{\partial\mathcal L}{\partial(\nabla_\mu\Phi^A)}
\right)=0.
\]

This form presumes that the connection, volume density, component pairing, and integrations by parts are compatible with the stated expression. Higher-derivative theories require the generalized Euler operator and additional boundary data. Constrained and gauge systems require constraint or reduction machinery. Nonlocal systems require functional or integral derivatives. Stochastic systems require a declared stochastic calculus and variational meaning. Dissipative systems may require an extended action, auxiliary variables, a nonconservative variational principle, or a direct evolution law. None of those cases shall be represented silently by the simple formula above.

### RS-V007 — Boundary term policy

Every variational model shall display or characterize the boundary term produced by variation and integration by parts. It shall state whether variations or normal derivatives are fixed, natural boundary conditions are imposed, counterterms are added, the domain has no boundary, or decay makes the term vanish. Discarding a boundary term without a cited condition is nonconforming.

### RS-V008 — Admissible variation

An admissible variation at \(\Phi\in\mathfrak C\) is a tangent direction \(\delta\Phi\) generated by a curve \(\Phi_\epsilon\in\mathfrak C\) with \(\Phi_0=\Phi\) and

\[
\delta\Phi=\left.\frac{d\Phi_\epsilon}{d\epsilon}\right|_{\epsilon=0}.
\]

Its support, regularity, endpoint or boundary behavior, and compatibility with field ranges and bundle structure shall be declared.

### RS-V009 — Constrained variation

A constrained variation is an admissible variation tangent to the declared constraint set. A model shall state whether it enforces constraints by parametrization, Lagrange multipliers, projection, penalty methods, reduction, or another explicit procedure. Distinct procedures shall not be assumed equivalent without proof or a stated approximation.

## 6.4 Dynamical evolution definitions

### RS-Y001 — Dynamical law

A dynamical law is a declared equation or rule selecting admissible histories or relating states, such as

\[
\mathfrak D[\Phi;g,J,\lambda]=0
\]

or a specified transition law. Its domain, codomain, differential or integral order, evolution parameter, data, parameters, sources, constraints, and scientific status shall be stated. Derivation from an action is optional, not presumed.

### RS-Y002 — Initial-value formulation

An initial-value formulation specifies a data space \(\mathfrak I\), an initial hypersurface or parameter value, constraint-compatible initial data \(u_0\in\mathfrak I\), and a law determining a history on a declared interval or domain. Required derivatives, gauge data, and compatibility conditions shall be included in \(\mathfrak I\).

### RS-Y003 — Boundary-value formulation

A boundary-value formulation specifies a domain \(\Omega\subseteq\mathcal M\), boundary operator \(\mathcal B\), boundary data \(b\), and equations satisfying

\[
\mathfrak D[\Phi]=0\ \text{in }\Omega,
\qquad
\mathcal B[\Phi]=b\ \text{on }\partial\Omega.
\]

Mixed initial-boundary problems shall declare both data sets and all corner compatibility conditions.

### RS-Y004 — Evolution operator

When the dynamics defines state propagation, the evolution operator is a family

\[
U(\tau_2,\tau_1):\mathfrak I_{\tau_1}\longrightarrow\mathfrak I_{\tau_2}.
\]

Its domain may be restricted. Composition \(U(\tau_3,\tau_2)\circ U(\tau_2,\tau_1)=U(\tau_3,\tau_1)\), identity, invertibility, linearity, continuity, semigroup structure, and unitarity shall not be inferred; each property requires stated assumptions. The parameter \(\tau\) has no universal physical interpretation in this chapter.

### RS-Y005 — Well-posedness requirement

A proposed or implemented initial-value dynamics shall document, on its declared domain of validity:

1. **existence** of solutions;
2. **uniqueness**, or the explicitly characterized source of nonuniqueness;
3. **continuous dependence on initial data** in a declared topology;
4. the parameter, field-amplitude, geometric, and other limits defining its **domain of validity**; and
5. the **regularity assumptions** on fields, coefficients, sources, backgrounds, and data.

A proof may be replaced at an exploratory stage by an explicit open requirement and numerical evidence, but numerical evidence shall not be called a proof of well-posedness.

### RS-Y006 — Hamiltonian representation

A Hamiltonian description is admissible when an evolution parameter and phase space are declared and a Legendre transform, symplectic or Poisson structure, or another precisely defined Hamiltonian construction yields equations equivalent to the intended dynamics on a stated domain. The Hamiltonian functional \(H\), brackets, phase-space variables, boundary terms, and constraint treatment shall be specified.

Such a description may fail or require extension for singular Lagrangians, constrained systems, gauge systems, dissipative systems, or nonlocal theories. A formal symbol \(H\) does not establish equivalence to the Lagrangian or direct-evolution formulation.

### RS-Y007 — Canonical momentum

For a first-order Lagrangian expressed relative to a declared evolution parameter \(\tau\), the canonical momentum conjugate to \(\Phi^A\) is, when the derivative exists,

\[
\pi_A=\frac{\partial\mathcal L}{\partial(\partial_\tau\Phi^A)}.
\]

Its tensor or density character, units, boundary conditions, and transformation properties shall be declared. Failure of the map \(\partial_\tau\Phi^A\mapsto\pi_A\) to be invertible signals a singular Legendre map and requires a constraint analysis rather than an assumed ordinary Hamiltonian formulation.

## 6.5 Constraints and conservation

### RS-C001 — Algebraic constraint

An algebraic constraint is a pointwise relation

\[
C_a(\Phi,g,J;\lambda)=0
\]

containing no derivatives of the constrained dynamical variables. Its index set, independence, preservation conditions, and enforcement method shall be declared.

### RS-C002 — Differential constraint

A differential constraint is a relation involving one or more derivatives of the dynamical variables. Its order, operator domain, boundary data, compatibility with the evolution law, and numerical enforcement shall be declared.

### RS-C003 — Compatibility constraint

A compatibility constraint is a condition required for jointly specified equations, initial data, boundary data, backgrounds, gauges, or regularity classes to admit a common solution. A specialization shall identify when and how it is checked, including whether evolution preserves it.

### RS-C004 — Conservation statement

A conservation statement is a theorem or conditional claim that a declared quantity \(Q\) is invariant along specified solutions, or that a current obeys a declared local balance equation. It shall state the equations, regularity, symmetry, source, boundary, and flux assumptions under which it holds. Approximate or numerically observed conservation shall be labeled as such and supplied with a tolerance and interval.

### RS-C005 — Symmetry-derived conservation candidate

Let \(T_\epsilon:\mathfrak C\to\mathfrak C\) be a differentiable one-parameter family with \(T_0=\operatorname{id}_{\mathfrak C}\). It is a continuous symmetry of an action when it preserves admissibility and

\[
\mathcal S[T_\epsilon\Phi]=\mathcal S[\Phi]
\]

for all sufficiently small \(\epsilon\), or changes the Lagrangian density only by a declared boundary term. Under the differentiability, locality, on-shell, and boundary assumptions of an applicable Noether-type theorem, its infinitesimal generator defines a **conservation candidate**.

Noether-type correspondence is admitted here as a standard mathematical framework. A candidate becomes a conservation statement under RS-C004 only after all theorem hypotheses, possible anomalies or explicit breaking, boundary fluxes, and source terms have been addressed. Gauge redundancy may instead yield identities or constraints and shall not automatically be reported as a physical conserved quantity.

## 6.6 Classes of dynamics

A specialization shall classify its law along each applicable axis and shall not silently select a universal option:

- **Deterministic dynamics** assigns a unique history or transition after all admissible data are fixed, subject to RS-Y005.
- **Stochastic dynamics** assigns a probability law to histories or transitions and shall declare its probability space, noise law, filtration when applicable, stochastic calculus convention, correlations, and random seeds for reproducible implementations.
- **Continuous-time dynamics** uses a continuous evolution parameter and declares the differentiability or weak-solution meaning of evolution.
- **Discrete-time dynamics** uses declared steps \(\tau_n\) and a transition map or recurrence; it shall distinguish fundamental discreteness from numerical discretization.
- **Local dynamics** determines its equation at a point from fields and finitely many derivatives in a declared neighborhood or jet order.
- **Nonlocal dynamics** depends on data across separated points, histories, or integral kernels and shall declare the kernel, support or memory, causality assumptions if any, and functional setting.

Hybrid, stochastic-deterministic, discrete-continuous, or local-nonlocal models are admissible when their interfaces are explicit. Whether any class is universal remains an open resolutive hypothesis.

## 6.7 Dimensional consistency and units

Every dynamical specification shall conform to the dimensional rules of Chapter 2 and shall declare:

1. the physical dimension and unit of \(\mathcal S\), including whether it is dimensionless or normalized by a declared constant;
2. the dimension and density weight of \(\mathcal L\), together with the dimension of the integration measure;
3. the dimension and interpretation of each evolution parameter, including the distinction between \(t\), proper time, and an internal parameter;
4. the dimensions and units of all couplings and parameters \(\lambda\); and
5. the dimensions of sources \(J\), canonical momenta, constraints, and every term in an evolution equation.

All additive terms shall be dimensionally homogeneous. Natural units, nondimensionalization, lattice units, or rescaled variables shall be declared together with an invertible conversion convention wherever physical units apply.

## 6.8 External sources, prescribed backgrounds, and backreaction

An external source \(J\) or prescribed background \(g\) is fixed data rather than a varied component of \(\Phi\). A model shall declare its regularity, units, domain, provenance, transformation behavior, and any dependence on the evolution parameter. Treating a field as prescribed shall be distinguished from solving its dynamics.

If \(\Phi\) influences \(J\), \(g\), or another background, the model shall specify a coupled equation, update rule, or approximation defining that **backreaction**. Neglecting backreaction is a model assumption whose regime and error control shall be documented. A one-way source, self-consistent coupling, and externally calibrated background shall not be conflated.

## 6.9 Proposed resolutive dynamical architecture

**Scientific status: proposed resolutive architecture; deliberately incomplete and not experimentally validated.** Specialized resolutive models may define dynamics through:

- an action principle;
- a direct evolution equation;
- a constrained flow;
- a projection-induced effective dynamics; or
- a stochastic or dissipative law.

The projection \(\Pi\), a coherence operator, the \(4\pi\) phase structure, or any component of \(R\) acquires no dynamical role merely by appearing in earlier chapters. Any such role shall be introduced as a stable, status-labeled hypothesis in the applicable specialization. This chapter chooses no final universal equation and asserts no validated resolutive dynamics.

## 6.10 Specialization rules

A conforming specialized dynamics shall:

1. cite the inherited RSMS identifiers and preserve their meanings;
2. list every dynamical field and distinguish it from sources, backgrounds, observables, and derived quantities;
3. select and fully type its variational, direct, constrained, stochastic, dissipative, or hybrid law;
4. declare data, parameter domains, units, regularity, gauge or coordinate choices, constraints, and boundary policy;
5. label the law as mathematical framework, proposed resolutive dynamics, implemented model, or validated result, with traceability supporting the label;
6. document correspondence between alternative formulations rather than presuming it;
7. keep domain-specific dynamics in its specialized specification; and
8. state departures from this chapter explicitly without reassigning stable identifiers.

## 6.11 Computational conformance

An implemented model shall provide, at minimum:

1. the declared spatial, temporal, field-space, and nonlocal **discretization**, including order and mesh or step controls;
2. solver algorithms, stopping criteria, absolute and relative **tolerances**, precision, and random seeds where applicable;
3. monitored conserved quantities, conservation candidates, algebraic constraints, differential constraints, and compatibility residuals, with acceptance thresholds;
4. refinement or other **convergence tests** that distinguish truncation, iteration, sampling, and regularization errors;
5. documentation of dependence on gauge, coordinates, initial and boundary conditions, and regularization choices;
6. discrete handling of variational boundary terms, sources, backgrounds, and backreaction; and
7. traceability from each implemented law and constraint to its stable specification identifier, source path, tests, configuration, and result.

A numerical solution is an **implemented model** output. It becomes a **validated result** only through separately declared validation criteria; apparent numerical stability alone is insufficient.

## 6.12 Open questions

The following questions remain unresolved and shall not be treated as settled assumptions:

1. Is universal resolutive dynamics variational?
2. Is evolution local, nonlocal, or regime-dependent?
3. Is the evolution parameter spacetime time, proper time, an internal parameter, or model-dependent?
4. Is dissipation fundamental or emergent?
5. Is universal resolutive dynamics first-order, second-order, or of another order?
6. Is gauge redundancy present, and if so what is its group and constraint structure?
7. How, if at all, does the \(4\pi\) phase structure enter dynamics?
8. Is coherence primitive, derived, or effective, and how would it be operationally defined?
9. Which functional setting yields well-posed universal dynamics?
10. Under what assumptions are variational, Hamiltonian, projected, and direct formulations equivalent?

## 6.13 Conformance checklist

| Requirement | Conforming declaration |
|---|---|
| Scientific status | Framework, proposed dynamics, implemented model, and validated result are separated |
| Fields | \(\Phi\), bundles, domains, ranges, regularity, and configuration space are declared |
| Law | Action or direct law, derivative order, locality, parameters, and evolution parameter are declared |
| Variations | Admissible variations, constraints, and boundary terms are declared |
| Data | Initial and/or boundary data and compatibility conditions are declared |
| Well-posedness | Existence, uniqueness, continuous dependence, validity domain, and regularity are addressed |
| Hamiltonian form | Legendre map, phase structure, constraints, and limitations are declared when used |
| Constraints | Algebraic, differential, and compatibility constraints are identified and monitored |
| Symmetry | Symmetry assumptions and Noether-type hypotheses precede conservation claims |
| Units | Action, density, measure, evolution parameter, sources, momenta, and couplings have declared dimensions |
| Backgrounds | Sources, prescribed backgrounds, and backreaction approximations are distinguished |
| Computation | Discretization, tolerances, convergence, residuals, gauge, coordinates, boundaries, and regularization are documented |
| Traceability | Stable identifiers connect specification, implementation, tests, and results |
| Scope | No specialized physical dynamics or universal resolutive equation is asserted |

## 6.14 Chapter status

| Subject | Status |
|---|---|
| Variational, Euler–Lagrange, and Hamiltonian machinery | Normative draft; mathematical framework |
| Evolution, data, constraints, and well-posedness requirements | Normative draft; mathematical framework |
| Proposed resolutive dynamical architecture | Open hypothesis space; no universal law selected |
| Specialized physical dynamics | Not introduced; deferred to specialized specifications |
| Computational model | Requirements defined; no implementation supplied here |
| Experimental validation | Not asserted |

Chapter 6 is designated **RSMS 1.0-draft.6** as of **2026-08-06**. Its identifiers `RS-V001`–`RS-V009`, `RS-Y001`–`RS-Y007`, and `RS-C001`–`RS-C005` are stable and contiguous. The chapter defines how dynamics may be specified and assessed; it does not determine which law nature follows.
