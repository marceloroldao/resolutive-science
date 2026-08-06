# Chapter 8 — Dimensional Structure, Units, and Scaling

**Specification:** RSMS-1.0
**Current RSMS version:** 1.0-draft.10
**Chapter revision:** 1.0
**Introduced in:** 1.0-draft.8
**Status:** Normative draft — dimensional and metrological framework
**Parent document:** `docs/RSMS/RSMS_v1.0.md`
**Author:** Marcelo Roldão Matos

---

## 8.1 Chapter purpose

This chapter defines the common dimensional framework of Resolutive Science. It specifies physical dimensions, units, conversions, scaling, dimensionless representations, normalization, dimensional analysis, and the metadata required for computation and reporting.

This framework introduces no physical law. Dimensional analysis can reject an inconsistent expression, but dimensional consistency alone does not establish that an expression is mathematically well posed, physically correct, resolutive, or empirically validated.

## 8.2 Scope, inheritance, and scientific status

This chapter inherits all definitions in Chapters 2–7, including the meanings of state, field, bundle, action, observable, and dynamics. It does not redefine, replace, or add physical content to any of them. When a quantity belonging to an inherited object is assigned a dimension or unit, that assignment is metadata for the inherited object rather than a new definition of it.

The definitions in this chapter are an **established mathematical and metrological framework** unless explicitly labeled otherwise. No resolutive hypothesis and no validated result is asserted here. A specialized module shall separately label established physics, resolutive hypotheses, implemented models, and validated results in accordance with the parent specification.

## 8.3 Quantity declaration and notation

Every mathematical quantity used in a normative equation, implementation, dataset, or result shall have a declaration containing:

| Field | Required declaration |
|---|---|
| Symbol | Unique typeset and machine-readable symbol in the applicable scope |
| Domain | Set of admissible inputs, including coordinate or parameter domain when applicable |
| Codomain | Mathematical space of values, including shape, scalar field, or tensor type |
| Dimension | Dimension expression in the declared base-dimension basis |
| Unit | Declared unit for stored, computed, or reported numerical values |
| Reference system | Coordinate frame, chart, observer convention, gauge convention, reference epoch, calibration reference, or an explicit statement that none applies |

For a quantity (Q), its physical dimension is written ([Q]), its declared unit is written (operatorname{unit}(Q)), and a numerical representation in a unit (u) may be written ({Q}_u), so that

\[
Q=\{Q\}_u\,u.
\]

The symbol (1) denotes the multiplicative dimensionless unit. A declaration shall distinguish a quantity, its numerical value, and its unit. A symbol reused under different reference systems or conventions shall be qualified so that the declarations remain unambiguous.

## 8.4 Dimensions

### RS-DIM001 — Physical dimension

A **physical dimension** is an equivalence class describing how a quantity participates in dimensional products and transformations, independently of the magnitude chosen as its unit. Given declared base dimensions (B_1,\ldots,B_k), the dimension of (Q) shall be expressible as

\[
[Q]=\prod_{a=1}^{k}B_a^{q_a},
\qquad q_a\in\mathbb R,
\]

with the exponent domain restricted further when a model requires it. Equality of dimensions means equality of all exponents in the same declared basis.

### RS-DIM002 — Dimensionless quantity

A **dimensionless quantity** has the identity dimension,

\[
[Q]=1.
\]

Dimensionless does not imply unitless. A dimensionless quantity may be reported using a named or scaled unit such as radian, steradian, percent, or a declared count convention. Its unit and semantic kind shall remain in metadata whenever needed to prevent invalid operations between distinct dimensionless quantities.

Arguments of exponential, logarithmic, and trigonometric functions shall be dimensionless after any declared reference quantity or angular unit has been applied. Their semantic kinds and conventions shall be retained where relevant.

### RS-DIM003 — Base dimensions

**Base dimensions** are a declared independent basis used to represent all dimensions in a unit system. The default RSMS reporting basis is the seven-dimensional SI basis

\[
\mathsf L,\quad \mathsf M,\quad \mathsf T,\quad
\mathsf I,\quad \mathsf\Theta,\quad \mathsf N,\quad \mathsf J,
\]

for length, mass, time, electric current, thermodynamic temperature, amount of substance, and luminous intensity, respectively. A model using a reduced, extended, or alternative basis shall provide the mapping to this basis when such a mapping exists and shall document any dimension not represented by it.

The choice of base dimensions is a representational convention; it is not a new physical claim about which quantities are fundamental in nature.

### RS-DIM004 — Derived dimensions

A **derived dimension** is a product of powers of declared base dimensions. For quantities (Q_1,Q_2) and a real exponent (a), dimensional multiplication, division, and exponentiation obey

\[
[Q_1Q_2]=[Q_1][Q_2],\qquad
\left[\frac{Q_1}{Q_2}\right]=\frac{[Q_1]}{[Q_2]},\qquad
[Q_1^a]=[Q_1]^a,
\]

where the mathematical operation and exponent are defined on the declared domain. A named derived SI unit does not create a new base dimension.

### RS-DIM005 — Dimensional consistency

An equation is **dimensionally consistent** when:

1. quantities added, subtracted, equated, ordered, or compared have compatible dimensions and units are converted as required;
2. products, quotients, powers, derivatives, integrals, and operator outputs follow their declared dimensional rules;
3. function arguments satisfy the dimensional restrictions of the function; and
4. both sides of every equality have the same dimension.

Zero values, fitted coefficients, discretized arrays, and implicit constants shall not be used to bypass these requirements. Dimensional consistency is necessary for a physical equation but is not sufficient evidence for a physical law or validation claim.

### RS-DIM006 — Dimensional transformation

A **dimensional transformation** is an explicitly declared map between dimension representations,

\[
T_D:\mathcal D\longrightarrow\mathcal D',
\]

where (mathcal D) and (mathcal D') are dimension spaces or bases. The map shall state its domain, codomain, basis ordering, treatment of constants, invertibility domain, and effect on units and numerical values.

A mere change between compatible units preserves physical dimension. A convention such as setting (c=1) may identify dimensions in a reduced representation; restoring the original representation shall use the declared constants and powers. No dimensional transformation may silently change the physical interpretation of a quantity.

## 8.5 Units

### RS-U001 — Declared unit

A **declared unit** is the specified reference magnitude used to represent the numerical value of a quantity. Every quantity declaration shall name its unit, including the unit (1) or a named dimensionless unit where applicable. Unit symbols shall not be used as quantity symbols in the same scope without qualification.

### RS-U002 — SI compatibility

A unit system is **SI-compatible** when every represented physical dimension can be mapped to SI units by documented conversions, without changing the represented quantity. SI is the default reporting system for RSMS results. Reports using another computational or presentation system shall also provide SI values or an unambiguous conversion to them, except where no SI representation has been established; that exception shall be explicit.

### RS-U003 — Non-SI units

**Non-SI units** are permitted when scientifically or operationally appropriate. Their definitions, symbols, dimensions, conversion factors, reference standards, and validity conditions shall be declared. A familiar name is not a substitute for a conversion record, especially where multiple definitions exist.

### RS-U004 — Natural units

**Natural units** are allowed. A natural-unit convention fixes one or more declared dimensional constants to specified numerical values, commonly (1), and thereby reduces or changes the numerical dimension representation. The convention shall list every fixed constant, its original dimension and reference value, the resulting independent dimensions, and the procedure for restoring SI-compatible quantities.

Use of natural units does not make the underlying dimensional distinctions nonexistent and shall not be presented as a physical law.

### RS-U005 — Internal model units

**Internal model units** are allowed for analytic or computational work. An internal unit system shall declare its base units, links to reference scales, conversions at all input and output boundaries, and any quantities for which no external conversion is currently defined. Internal computational units shall not be mislabeled as SI or observational units.

The RSMS does not assume that every internal resolutive quantity possesses an SI-representable physical dimension. A specialized specification may introduce an internal dimension only if it declares:

- its symbol and semantic meaning;
- its algebraic behavior;
- its relation, if any, to the SI dimensional basis;
- whether that relation is exact, conventional, model-dependent, or unknown;
- its conversion or mapping rule when one exists; and
- an explicit statement when no SI mapping is currently defined.

An internal resolutive dimension shall not be represented as a validated physical dimension merely because it is mathematically declared.

### RS-U006 — Conversion factors

A **conversion factor** is a documented multiplicative factor, or where necessary an explicitly affine or nonlinear map, relating numerical representations of the same quantity under two unit conventions. For multiplicatively related units (u) and (v),

\[
\{Q\}_v=C_{u\to v}\{Q\}_u,
\qquad
C_{v\to u}C_{u\to v}=1.
\]

The factor or map shall declare direction, exact or measured status, precision, uncertainty when applicable, validity domain, and source. Offset units shall not be processed as purely multiplicative units.

### RS-U007 — Unit provenance

**Unit provenance** is the traceable record of how a unit and its conversion were selected, defined, calibrated, or derived. It shall identify the unit-system version, authoritative definition or reference artifact, conversion-table version, constants and reference scales used, uncertainty where applicable, and transformation history from acquisition through reporting.

## 8.6 Scaling and dimensionless representations

### RS-S001 — Normalization

**Normalization** is a declared map that imposes a specified magnitude, integral, norm, probability, range, or reference convention on a quantity or collection of quantities. For example,

\[
N:X\longrightarrow X_N,
\]

shall declare its input and output domains, codomains, dimensions, units, reference system, normalization condition, parameters, invertibility, and behavior for singular inputs. Normalization may change numerical values and may produce dimensionless quantities, but it does not automatically do either.

### RS-S002 — Reference scale

A **reference scale** (Q_{\mathrm{ref}}) is a declared nonzero quantity used to compare, convert, or nondimensionalize another quantity of compatible dimension. Its symbol, value, dimension, unit, provenance, reference system, validity domain, and uncertainty or exact status shall be recorded.

### RS-S003 — Characteristic scale

A **characteristic scale** (Q_*) is a reference scale selected from a problem's stated parameters, boundary data, distribution, or solution behavior according to a declared rule. The selection rule and dependence on model or data shall be reported. Calling a scale characteristic does not make it universal or fundamental.

### RS-S004 — Dimensionless variables

A **dimensionless variable** is obtained through a declared construction whose resulting dimension is (1). For a nonzero compatible reference scale (Q_{\mathrm{ref}}),

\[
\widehat Q=\frac{Q}{Q_{\mathrm{ref}}},
\qquad [\widehat Q]=1.
\]

The map shall retain the reference scale and unit metadata needed to reconstruct (Q). Hats are the default notation for dimensionless variables, but a specialization may use another nonconflicting notation if it declares it.

### RS-S005 — Scaling transformation

A **scaling transformation** is a parameterized map that multiplies declared quantities or coordinates by specified scale factors while preserving the stated mathematical type. A general component form is

\[
Q_a\longmapsto Q'_a=\lambda^{w_a}Q_a,
\qquad \lambda\in\Lambda,
\]

where (Lambda) is declared, (w_a) is the scaling weight, and the domain, codomain, dimensions, units, reference system, fixed quantities, and transformation of parameters and operators are specified. A scaling transformation is not necessarily a symmetry.

### RS-S006 — Similarity transformation

A **similarity transformation** is a scaling transformation that maps a declared mathematical problem or family of problems to another with the same specified dimensionless structure. The invariant dimensionless groups, transformed parameters, domains, boundary or initial data, and criterion of similarity shall be identified. Similarity is a mathematical relation and does not establish empirical equivalence.

### RS-S007 — Coarse-graining scale

A **coarse-graining scale** (ell_{\mathrm{cg}}) is the declared resolution, support, cutoff, cell size, bandwidth, or aggregation scale associated with a coarse-graining operation. Its dimension, unit, domain, reference system, kernel or aggregation rule, boundary treatment, and relation to discretization shall be recorded. Dependence on (ell_{\mathrm{cg}}) shall not be interpreted as physical scale dependence without a separately status-labeled hypothesis and evidence.

## 8.7 Analysis and transformation vocabulary

The following terms are normative process definitions and do not redefine the quantities to which they are applied:

- **Dimensional analysis** is the determination and comparison of dimensions in expressions, transformations, models, or data schemas to test RS-DIM005 and identify admissible dimensionless groups.
- **Nondimensionalization** is the construction of dimensionless variables and equations using declared reference scales. All substitutions and the inverse reconstruction shall be documented.
- **Normalization** is the operation defined by RS-S001. It shall not be used as a synonym for every rescaling or nondimensionalization.
- **Rescaling** is a declared change of numerical scale or variable representation. It shall identify whether dimensions, units, domains, or physical quantities change.
- **Coordinate scaling** applies a scaling map to coordinates and shall declare the induced transformation of coordinate components, bases, measures, derivatives, metrics, and domains where applicable.
- **Parameter scaling** applies a scaling map to model or algorithm parameters and shall preserve their declared dimensions or document the dimensional transformation used.
- **Field scaling** applies a scaling map to field values and shall declare the transformation of arguments, components, bases, field dimension, boundary data, and operators acting on the field.
- **Observable scaling** applies a scaling map to an observable representation and shall preserve the observable definition and measurement provenance. A scaled observable is not a new validated result merely because its numerical range is convenient.

Normalization, nondimensionalization, unit conversion, and scaling shall be recorded as distinct transformations even when a pipeline combines them.

## 8.8 Buckingham Pi theorem

The Buckingham Pi theorem may be used only as an established mathematical framework for dimensional analysis. For a declared relation among (n) dimensional quantities whose dimension-exponent matrix has rank (r), it provides, under its mathematical assumptions, a representation in terms of (n-r) independent dimensionless groups,

\[
\Pi_1,\ldots,\Pi_{n-r}.
\]

The Buckingham Pi theorem is adopted only as an established mathematical tool for dimensional analysis and nondimensionalization. Its inclusion does not support, validate, or provide evidence for any specific resolutive hypothesis, state variable, interaction, or physical law.

An application shall declare the quantity list, base-dimension basis, exponent matrix, its rank, the selected independent groups, and the domain on which the transformation is valid. The theorem does not determine numerical coefficients or a unique physical law, prove causality, select a preferred group basis, or validate a model. This specification claims no resolutive extension of the Buckingham Pi theorem.

## 8.9 Dimensional rules for mathematical operations

The following rules apply unless a more restrictive declared mathematical structure governs the operation:

1. **Addition and subtraction:** operands shall have the same dimension and be expressed in compatible units before numerical combination.
2. **Products and contractions:** dimensions multiply; tensor contraction does not itself alter the product dimension of the contracted components and bases.
3. **Differentiation:** if (f) depends on (x), then ([\partial f/\partial x]=[f]/[x]), subject to the coordinate and basis declarations.
4. **Integration:** the dimension of an integral includes the dimension of its measure. Measures and Jacobians shall be declared.
5. **Powers:** a dimensional base raised to a variable dimensional exponent is nonconforming. Fractional powers require a declared domain and resulting dimension.
6. **Transcendental functions:** exponential and logarithmic arguments shall be dimensionless; angular-function conventions shall be declared.
7. **Matrices and arrays:** elements combined by an operation shall have compatible dimensions, or the schema shall carry per-component dimensions. Storage in one array does not imply common dimension.
8. **Operators:** every normative operator shall declare the dimension and unit behavior from its domain to codomain.
9. **Losses and objective functions:** every term shall be dimensionally compatible before addition. Weights, likelihood conventions, and reductions shall be dimensioned or normalized explicitly.
10. **Uncertainty:** uncertainties, covariance entries, probability densities, and distribution parameters shall carry the dimensions implied by their definitions.

## 8.10 Computational conformance

Every implementation shall declare and version the following:

| Computational record | Required content |
|---|---|
| Floating-point precision | Numeric type, bit width or decimal precision, rounding mode where controlled, mixed-precision policy, and relevant tolerance policy |
| Unit system | External, internal, natural, and reporting units; base dimensions; named-unit definitions; and boundary conversions |
| Conversion tables | Machine-readable factors or maps, direction, provenance, exactness or uncertainty, validity domain, and table version or checksum |
| Normalization | Transformation, reference scales, fitting scope, inverse map, singular behavior, and whether statistics were learned from data |
| Loss scaling | Dimension and unit of every loss term, reduction convention, weights, dynamic or static scaling, and inverse interpretation where one exists |
| Parameter scaling | Stored and physical parameter representations, transformations, bounds, priors, optimizer coordinates, and inverse map |
| Serialization format | Format and version, schema, endianness where relevant, numeric precision, unit encoding, missing/nonfinite-value policy, and compatibility rules |
| Metadata | RSMS version, stable identifiers, symbol, domain, codomain, dimension, unit, reference system, provenance, configuration, software revision, and timestamps |

Conversions and normalization shall occur at traceable pipeline boundaries. Tests shall cover round trips, dimensional failures, reference cases, precision loss, serialization recovery, and metadata completeness. Serialization shall preserve enough information to reconstruct the physical quantity; a bare number is not a conforming serialized physical quantity.

## 8.11 Specialized-module inheritance

The Cosmology, Quantum Theory, Rotation Curves, Lensing, and Electromagnetism modules may introduce additional units, dimension bases, reference scales, natural-unit conventions, and internal normalization conventions, provided that they:

1. inherit RS-DIM001–RS-DIM006, RS-U001–RS-U007, and RS-S001–RS-S007;
2. preserve all inherited identifiers and definitions;
3. declare every added quantity using the record in Section 8.3;
4. map added units to SI or state explicitly why no such mapping is defined;
5. provide conversions and provenance at module boundaries;
6. distinguish representational conventions from physical hypotheses;
7. document cross-module interoperability and incompatible conventions; and
8. report outputs in SI by default, alongside specialized units when useful.

A module-specific convention shall not silently become a universal RSMS convention.

## 8.12 Open questions

The following questions remain unresolved and shall not be treated as conclusions or physical claims:

1. Can internal resolutive quantities possess dimensions not directly represented in SI?
2. Should coherence always be dimensionless?
3. Can phase possess effective dimensional meaning?
4. Should address coordinates have units?
5. Can different specialized theories define different internal normalization conventions?

Until resolved by an approved specification change, each specialized use shall declare its choice, scientific status, consequences for conversion and interoperability, and tests. No answer is implied by allowing the metadata field.

## 8.13 Conformance checklist

An equation, implementation, dataset, result, or specialized specification conforms to this chapter only when every applicable row is satisfied.

| Requirement | Compliance condition | Evidence required |
|---|---|---|
| Inherited definitions | State, field, bundle, action, observables, and dynamics retain their prior meanings | Cross-references to Chapters 2–7 and no conflicting definition |
| Scientific status | Established framework, resolutive hypothesis, implemented model, and validated result remain separate | Explicit status labels |
| Quantity declaration | Symbol, domain, codomain, dimension, unit, and reference system are present | Quantity registry or schema |
| Dimension basis | Base dimensions and ordering are declared | Dimension-basis record |
| Derived dimensions | Exponents and derivations are consistent | Machine-readable or reviewed dimension expressions |
| Dimensionless semantics | Dimension (1), named units, and semantic kinds are distinguished | Quantity metadata |
| Dimensional consistency | All equations and operations satisfy RS-DIM005 and Section 8.9 | Automated checks and/or review record |
| Dimensional transformations | Basis map, constants, domain, codomain, and reversibility are documented | Transformation specification and tests |
| Declared units | Every numerical physical quantity carries an explicit unit | Schema and serialized examples |
| SI reporting | SI is used by default or a conversion/explicit exception is supplied | Report and conversion record |
| Non-SI units | Definitions, dimensions, conversions, and validity are explicit | Unit registry |
| Natural units | Fixed constants and SI restoration are documented | Convention record and round-trip test |
| Internal units | Base units and all input/output conversions are documented | Model-unit registry |
| Conversion factors | Direction, exactness, precision, uncertainty, validity, and provenance are recorded | Versioned conversion table |
| Unit provenance | Definitions, standards, constants, and transformation history are traceable | Provenance metadata |
| Reference scales | Value, dimension, unit, origin, validity, and uncertainty are declared | Reference-scale registry |
| Normalization | Condition, scope, parameters, inverse, and singular behavior are declared | Normalization record and tests |
| Dimensionless variables | Construction and reconstruction scales are retained | Nondimensionalization map |
| Scaling transformations | Weights, transformed objects, fixed objects, and domains are declared | Scaling specification |
| Similarity | Invariant groups and similarity criterion are stated | Similarity analysis |
| Coarse graining | Scale, kernel or rule, boundary treatment, and discretization relation are stated | Coarse-graining configuration |
| Buckingham Pi use | Quantity list, exponent matrix, rank, groups, and assumptions are declared without an extension claim | Dimensional-analysis record |
| Numerical precision | Type, precision, rounding/mixed-precision policy, and tolerances are declared | Runtime configuration |
| Loss scaling | Term dimensions, weights, reductions, and scaling policy are declared | Training or optimization configuration |
| Parameter scaling | Physical/stored maps, bounds, priors, and inverse are declared | Parameter schema |
| Serialization | Format, schema, precision, units, and exceptional values are preserved | Round-trip tests |
| Metadata | Specification, identifiers, quantity declarations, provenance, configuration, and revision are stored | Machine-readable result record |
| Specialized modules | Added conventions inherit this framework and define SI/inter-module boundaries | Module conformance statement |
| Open questions | Unresolved choices are not presented as established or validated | Limitations and status record |
| Stable identifiers | Identifier meanings are preserved and new identifiers are unique | Identifier-registry check |

## 8.14 Chapter status and identifier registry

| Item | Status |
|---|---|
| Dimensional algebra and analysis | Normative draft; established mathematical framework |
| Unit, conversion, and provenance rules | Normative draft; metrological framework |
| Scaling and normalization vocabulary | Normative draft; mathematical framework |
| Buckingham Pi theorem | Established mathematical framework only; no resolutive extension claimed |
| Particular dimensional assignment for unresolved internal quantities | Not specified; open question |
| New physical laws | None introduced |
| Resolutive hypotheses | None asserted by this chapter |
| Validated physical or computational results | None asserted by this chapter |

| Identifier range | Content |
|---|---|
| `RS-DIM001`–`RS-DIM006` | Dimensions and dimensional consistency |
| `RS-U001`–`RS-U007` | Units, conversions, and provenance |
| `RS-S001`–`RS-S007` | Normalization, scales, and scaling transformations |

---

**End of Chapter 8**
