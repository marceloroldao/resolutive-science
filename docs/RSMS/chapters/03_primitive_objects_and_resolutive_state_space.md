# Chapter 3 — Primitive Objects and Resolutive State Space

**Specification:** RSMS-1.0
**Version:** 1.0-draft.3
**Status:** Normative draft — proposed foundational hypotheses
**Author:** Marcelo Roldão Matos
**Parent document:** `docs/RSMS/RSMS_v1.0.md`

---

## 3.1 Chapter purpose

This chapter defines the primitive objects required to state later resolutive models. It fixes their mathematical roles and the minimum metadata required for implementation, without assigning equations of motion or claiming empirical support.

Every physical structure specific to Resolutive Physics in this chapter is a **proposed foundational hypothesis**. None is an experimentally validated fact or a validated result. Standard mathematical notions used to express these hypotheses do not acquire a new empirical status by their use here.

This chapter introduces no dynamics, Lagrangian, Hamiltonian, field equation, cosmological equation, quantum evolution, or experimental claim.

---

## 3.2 Primitive-object policy

### RS-R013 — Minimality of primitives

A quantity shall be primitive only when it is required to define the universal resolutive state before any model specialization. A quantity computable from primitive objects, supplied by a specialized model, or associated with observation shall not be promoted to a universal primitive merely for convenience.

The primitive physical content adopted here consists of a base spacetime manifold and a four-component internal resolutive state. The internal space, total state space, fields, observable space, and projection operator provide the mathematical structures in which that content is represented.

**Assumptions:** the proposed resolutive description admits a local state representation.
**Implementation status:** specification only; no reference implementation is designated.
**Open questions:** whether later consistency or validation work requires a smaller, constrained, or differently structured primitive set.

### RS-R014 — Scientific-status separation

Implementations and specialized specifications shall label the structures defined in this chapter as resolutive hypotheses until the applicable validation criteria have been specified and satisfied. They shall distinguish these hypotheses from established mathematical or physical background structures and from validated results.

---

## 3.3 Base manifold

### RS-D001 — Base spacetime manifold

The **base spacetime manifold** is denoted by

\[
M.
\]

It is the domain over which local resolutive states may be assigned. For the minimal RSMS construction, \(M\) shall be a four-dimensional, Hausdorff, second-countable smooth manifold. A Lorentzian metric may be supplied by a later geometric specification, but no metric, connection, causal structure, or dynamics is made primitive by this definition.

| Metadata | Normative content |
|---|---|
| Mathematical type | Smooth manifold |
| Domain | Not applicable; \(M\) is a space |
| Codomain | Not applicable |
| Units | Coordinates may carry declared units; \(M\) itself has no unit |
| Assumptions | Dimension four; Hausdorff; second-countable; smooth atlas |
| Implementation status | Abstract interface only |
| Open questions | Global topology; boundary; metric structure; differentiability refinements |

**Scientific status:** the use of a smooth spacetime base is established mathematical practice; its role as the base of the resolutive construction is a **proposed foundational hypothesis of Resolutive Physics**, not a validated result.

---

## 3.4 Internal resolutive space

### RS-D002 — Internal resolutive space

The **internal resolutive space** is denoted by

\[
\mathcal R.
\]

It is the space of admissible values of the minimal resolutive state. Provisionally,

\[
\mathcal R
\subseteq
\mathcal D_{\rho}
\times S^1_{\Theta}
\times \mathcal D_{\iota}
\times \mathcal D_{\kappa},
\tag{RS-E028}
\]

where \(\mathcal D_{\rho}\), \(\mathcal D_{\iota}\), and \(\mathcal D_{\kappa}\) are declared admissible scalar domains and \(S^1_{\Theta}\) is the phase space. Unless a specialization states otherwise, \(\mathcal D_{\rho}=\mathbb R_{\geq 0}\), \(\mathcal D_{\iota}\subseteq\mathbb R\), and \(\mathcal D_{\kappa}\subseteq\mathbb R\). The equivalence relation and period used to realize \(S^1_{\Theta}\) shall be declared by the applicable specialization; they shall not be inferred from the symbol alone.

| Metadata | Normative content |
|---|---|
| Mathematical type | Internal state space, provisionally a subset of a product space |
| Domain | Not applicable; \(\mathcal R\) is a space |
| Codomain | Not applicable |
| Units | Component-dependent as specified in RS-D004; \(\mathcal R\) has no aggregate unit |
| Assumptions | Four primitive coordinates; non-negative density/depth; periodic phase |
| Implementation status | Schema specified; admissible ranges and topology are partly provisional |
| Open questions | Exact ranges; topology; internal metric; coordinate singularities; constraints among components |

**Scientific status:** the existence and four-coordinate structure of \(\mathcal R\) are **proposed foundational hypotheses of Resolutive Physics** and are not experimentally validated.

---

## 3.5 Total state space

### RS-D003 — Total state space

The **total state space** is denoted by

\[
E_R,
\]

and shall be equipped with a surjective bundle projection

\[
\pi_M:E_R\to M.
\tag{RS-E029}
\]

Each fiber \(E_{R,x}=\pi_M^{-1}(x)\) shall be modeled on \(\mathcal R\). The minimal un-twisted representation may use

\[
E_R=M\times\mathcal R,
\tag{RS-E030}
\]

but the product form is not required universally. No connection, metric, transport law, or evolution law on \(E_R\) is defined here.

| Metadata | Normative content |
|---|---|
| Mathematical type | Fiber bundle, provisionally allowing the product bundle |
| Domain | Base \(M\), through \(\pi_M\) |
| Codomain | \(M\), for \(\pi_M\) |
| Units | Inherited component-wise from base coordinates and fiber coordinates |
| Assumptions | Nonempty fibers modeled on \(\mathcal R\); surjective bundle projection |
| Implementation status | Abstract data model; product representation permitted |
| Open questions | Whether nontrivial bundles are required; transition functions; global sections; bundle category |

**Scientific status:** interpreting \(E_R\) as the total state space of a resolutive description is a **proposed foundational hypothesis of Resolutive Physics**, not a validated fact.

---

## 3.6 Minimal resolutive state

### RS-D004 — Resolutive state

A **resolutive state** at \(x\in M\) is an element \(R_x\in E_{R,x}\) represented in a local trivialization by the ordered tuple

\[
R=(\rho_R,\Theta_R,\iota_R,\kappa_R)\in\mathcal R,
\tag{RS-E031}
\]

where:

- \(\rho_R\) is **resolutive density or depth**;
- \(\Theta_R\) is **resolutive phase**;
- \(\iota_R\) is **resolutive inclination**;
- \(\kappa_R\) is **local resolutive curvature**.

These names define semantic roles, not dynamical or experimentally established interpretations. In particular, \(\kappa_R\) is a primitive local scalar coordinate and shall not be identified with spacetime curvature unless a later normative mapping explicitly establishes that relation.

| Component | Mathematical type | Domain | Codomain/value space | Units | Assumptions | Implementation status | Open questions |
|---|---|---|---|---|---|---|---|
| \(\rho_R\) | Real scalar coordinate | A state in \(\mathcal R\) | \(\mathcal D_\rho\), default \(\mathbb R_{\geq0}\) | Undetermined; shall be declared by specialization | Non-negative under the default domain | Scalar storage supported conceptually | Physical dimension, normalization, bounds |
| \(\Theta_R\) | Phase coordinate | A state in \(\mathcal R\) | \(S^1_\Theta\) | Dimensionless; radians may label values | A declared periodic equivalence relation is required | Wrapped scalar or equivalent representation | Periodicity and global chart treatment |
| \(\iota_R\) | Real scalar coordinate | A state in \(\mathcal R\) | \(\mathcal D_\iota\subseteq\mathbb R\) | Undetermined; dimensionless if interpreted as an angle | Range and equivalences shall be declared | Scalar storage supported conceptually | Exact geometric meaning, range, degeneracies |
| \(\kappa_R\) | Real scalar coordinate | A state in \(\mathcal R\) | \(\mathcal D_\kappa\subseteq\mathbb R\) | Undetermined; shall not be inferred from the word “curvature” | Locality only; no spacetime-curvature identity | Scalar storage supported conceptually | Dimension, bounds, relation to later geometry |

**Scientific status:** the tuple and the proposed semantic roles of its components are **proposed foundational hypotheses of Resolutive Physics**. They have not been experimentally validated.

### RS-R015 — Primitive-state closure

The universal primitive resolutive state shall contain exactly the four ordered components in RS-D004. Chirality, orientation, observables, coherence measures, and other model-dependent quantities shall not be appended as primitive components of \(R\).

---

## 3.7 Distinction between state and address

### RS-D005 — Resolutive address

A **resolutive address** is an identifier or coordinate label used to locate a state-bearing element within a declared base, fiber, chart, discretization, layer, subsystem, or data structure. It is denoted generically by

\[
a_R\in\mathcal A_R,
\]

where \(\mathcal A_R\) is the address space defined by the applicable representation.

| Metadata | Normative content |
|---|---|
| Mathematical type | Label, index, coordinate tuple, or implementation key |
| Domain | The represented collection of state-bearing elements |
| Codomain | Declared address space \(\mathcal A_R\) |
| Units | Representation-dependent; indices and keys are dimensionless |
| Assumptions | Addresses identify or locate; they do not add physical state content |
| Implementation status | Representation-specific and not standardized |
| Open questions | Canonical addressing across charts, meshes, layers, and distributed systems |

The resolutive address is **not part of the resolutive state**:

\[
a_R\notin R,
\qquad
R=(\rho_R,\Theta_R,\iota_R,\kappa_R).
\tag{RS-E032}
\]

Changing an address without changing the represented fiber element shall not be interpreted as changing the resolutive state. Conversely, equal local state tuples may occur at distinct addresses.

**Scientific status:** the state/address separation is a normative modeling rule. Any claim that a particular address has physical significance would be an additional resolutive hypothesis and is not made here.

---

## 3.8 Fields as sections

### RS-D007 — Resolutive field

A **resolutive field** is a section of the total state space,

\[
\mathcal R_f:M\to E_R,
\qquad
\pi_M\circ\mathcal R_f=\operatorname{id}_M.
\tag{RS-E033}
\]

In a local trivialization it may be written

\[
\mathcal R_f(x)
=
\bigl(x;\rho_R(x),\Theta_R(x),\iota_R(x),\kappa_R(x)\bigr).
\tag{RS-E034}
\]

This notation assigns states to base points only; it introduces no field dynamics.

| Metadata | Normative content |
|---|---|
| Mathematical type | Section of \(\pi_M:E_R\to M\) |
| Domain | \(M\) |
| Codomain | \(E_R\), with \(\mathcal R_f(x)\in E_{R,x}\) |
| Units | Component-wise units of RS-D004 |
| Assumptions | A section exists on its declared domain; regularity shall be declared |
| Implementation status | Pointwise callable or sampled-field interface permitted; no reference implementation |
| Open questions | Required regularity; global existence; singular sets; interpolation and chart transitions |

**Scientific status:** the section concept is standard mathematics; representing a physical resolutive configuration by such a section is a **proposed foundational hypothesis of Resolutive Physics**, not a validated result.

---

## 3.9 Observable space and projection

### RS-D006 — Observable space

The **observable space** is denoted by

\[
\mathcal O.
\]

It is a declared mathematical space whose elements represent quantities eligible for comparison with a measurement or an observational data model. This definition does not assert that any element has been measured or validated.

| Metadata | Normative content |
|---|---|
| Mathematical type | Model-dependent measurable, topological, vector, tensor, or product space |
| Domain | Not applicable; \(\mathcal O\) is a space |
| Codomain | Not applicable |
| Units | Declared separately for each observable component |
| Assumptions | Sufficient structure exists for the intended comparison or data model |
| Implementation status | Placeholder interface; no universal observable schema |
| Open questions | Universal versus model-specific observables; uncertainty representation; calibration and coarse-graining |

**Scientific status:** the distinction between latent state and observable output is a modeling principle. Any proposed resolutive observable remains a hypothesis until independently validated.

### RS-O001 — Observable projection operator

The **observable projection operator** is the map

\[
\Pi:E_R\to\mathcal O.
\tag{RS-E035}
\]

It maps a total-state-space element to an element of the observable space. The name “projection” denotes its observable-extraction role and does not require \(\Pi\) to be a linear, idempotent, orthogonal, or coordinate projection.

| Metadata | Normative content |
|---|---|
| Mathematical type | Map; linearity and other operator properties are unspecified |
| Domain | \(E_R\) |
| Codomain | \(\mathcal O\) |
| Units | Its output units are those declared for the applicable components of \(\mathcal O\) |
| Assumptions | Well-defined on the declared subset of \(E_R\); dependencies shall be explicit |
| Implementation status | Signature only; detailed physical and numerical form deferred |
| Open questions | Functional form; locality; degeneracy; uncertainty; calibration; dependence on context or apparatus |

No detailed physical form for \(\Pi\) is specified in this chapter. An implementation shall not invent a normative form and attribute it to RSMS-1.0.

**Scientific status:** the existence of a resolutive-to-observable mapping is a **proposed foundational hypothesis of Resolutive Physics**. No particular mapping and no experimental correspondence is validated here.

---

## 3.10 Derived quantities

### RS-D008 — Derived quantity

A **derived quantity** is any quantity \(Q\) obtained by a declared map from primitive states, fields, background structures, parameters, or combinations thereof:

\[
Q=F[R;B,P],
\tag{RS-E036}
\]

where \(B\) denotes explicitly declared background structures and \(P\) denotes explicitly declared parameters. Equation RS-E036 is a dependency schema, not a physical equation or evolution law.

| Metadata | Normative content |
|---|---|
| Mathematical type | Output of a declared functional or map \(F\) |
| Domain | Declared subset of primitive states, fields, backgrounds, and parameters |
| Codomain | Quantity-specific declared space |
| Units | Derived from the defining map and declared inputs; shall be dimensionally consistent |
| Assumptions | All dependencies, conventions, and regularity requirements are explicit |
| Implementation status | Quantity-specific; not implemented by this chapter |
| Open questions | Which derived quantities are universal; uniqueness; invariance; operational interpretation |

Chirality, orientation, observables, coherence measures, and all other quantities not listed in RS-D004 shall be treated as derived or specialized quantities. An observable may depend on a derived quantity or be produced through \(\Pi\), but it is not thereby a primitive state variable.

**Scientific status:** a formula defining a resolutive derived quantity is a proposed hypothesis unless separately classified. This chapter validates no such formula.

---

## 3.11 Specialization rules

### RS-R016 — Conforming specialization

A specialized specification may restrict domains, choose units, fix phase periodicity, impose algebraic constraints, select bundle structure, define derived quantities, or specify an observable projection, provided that it shall:

1. preserve the ordered primitive state and the stable identifiers of this chapter;
2. declare every restriction, additional structure, and dependency;
3. label physical additions by scientific status;
4. treat chirality, orientation, observables, coherence measures, and other additions as derived or specialized rather than primitive;
5. define the domain, codomain, units, assumptions, implementation status, and open questions where applicable; and
6. avoid presenting implementation choices as universal RSMS requirements.

A specialization that replaces or enlarges the primitive tuple is nonconforming unless adopted through a documented RSMS revision.

### RS-R017 — No implicit dynamics

Neither a state-space definition, a field representation, nor an observable projection shall be interpreted as an equation of motion. Dynamics require separate normative definitions in a later chapter.

---

## 3.12 Computational representation

### RS-R018 — Minimum computational schema

A conforming computational representation of a resolutive state shall:

- store or expose exactly the named fields `rho_R`, `Theta_R`, `iota_R`, and `kappa_R` in the normative order;
- represent an address separately from the state payload;
- declare numeric types, units, admissible ranges, phase wrapping, missing-value policy, and precision;
- associate sampled fields with their base-domain representation and chart or mesh metadata;
- identify the implemented specification version and applicable specialization; and
- keep derived quantities and observables distinguishable from primitive values.

The following language-neutral record is illustrative and non-normative:

```text
ResolutiveState {
    rho_R
    Theta_R
    iota_R
    kappa_R
}

AddressedState {
    address
    state: ResolutiveState
}
```

Serialization formats, floating-point precision, coordinate systems, storage layout, and evaluation strategy remain implementation choices unless fixed by a specialized specification.

---

## 3.13 Unresolved questions

The following questions remain open and shall not be treated as resolved by this chapter:

1. What exact topology and admissible ranges shall \(\mathcal R\) have?
2. What period and equivalence relation shall apply to \(\Theta_R\)?
3. What physical dimensions and operational definitions, if any, shall be assigned to \(\rho_R\), \(\iota_R\), and \(\kappa_R\)?
4. Is \(E_R\) globally a product bundle, or are nontrivial transition functions required?
5. What regularity class shall resolutive fields satisfy?
6. Which symmetries or redundancies act on the state representation?
7. Which quantities are invariant under admissible coordinate and internal reparameterizations?
8. What detailed form, domain restrictions, and uncertainty model shall \(\Pi\) possess?
9. Which derived quantities are universal and which belong only to specialized specifications?
10. What mathematical, computational, and empirical tests could reject or constrain these proposed foundational hypotheses?

---

## 3.14 Conformance checklist

An implementation or specialized specification conforms to this chapter only if all applicable items below are satisfied.

| Requirement | Conformance condition |
|---|---|
| Scientific status | Resolutive physical structures are labeled proposed hypotheses, not validated facts |
| Base | \(M\) is identified and its additional structures are declared |
| Internal space | \(\mathcal R\), component domains, ranges, units, and phase equivalence are declared |
| Total space | \(E_R\), \(\pi_M\), fibers, and any nontrivial bundle structure are declared |
| Primitive state | \(R=(\rho_R,\Theta_R,\iota_R,\kappa_R)\) is preserved in order and meaning |
| Address separation | The resolutive address is stored and interpreted separately from \(R\) |
| Derived status | Chirality, orientation, observables, coherence measures, and other additions are non-primitive |
| Field | A resolutive field is represented as a section on its declared domain |
| Observable mapping | Any implemented \(\Pi\) declares domain, codomain, units, dependencies, and status |
| Traceability | Stable identifiers and the applicable RSMS version are recorded |
| Dynamics boundary | No dynamics are inferred from the structures of this chapter |
| Open metadata | Assumptions, implementation status, and unresolved questions are documented |

---

## 3.15 Chapter status

| Criterion | Status |
|---|---|
| Primitive-object policy | Normative draft |
| Base, internal, and total spaces | Normative draft; proposed foundational hypotheses |
| Minimal resolutive state | Normative draft; proposed foundational hypothesis |
| State/address distinction | Normative draft |
| Field representation | Normative draft; no dynamics |
| Observable space and projection signature | Normative draft; detailed form deferred |
| Derived-quantity and specialization rules | Normative draft |
| Computational schema | Normative draft; no reference implementation |
| Experimental validation | Not established |
| Unresolved questions | Open |

Chapter 3 is designated **RSMS 1.0-draft.3** as of **2026-08-06**. Its proposed physical structures remain unvalidated and subject to controlled revision.
