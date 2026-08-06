# Chapter 4 — Geometric and Bundle Structure

**Specification:** RSMS-1.0
**Current RSMS version:** 1.0-draft.10
**Chapter revision:** 1.0
**Introduced in:** 1.0-draft.4
**Status:** Normative draft — mathematical structure only
**Parent document:** `docs/RSMS/RSMS_v1.0.md`
**Author:** Marcelo Roldão Matos

---

## 4.1 Status and scope

**Specification status:** Normative draft
**Scientific status:** Mathematical structure only; no physical hypothesis or validated result is asserted in this chapter.

This chapter defines the geometric language available to specialized Resolutive Science specifications. It builds on the primitive objects of Chapter 3 and introduces no dynamics, field equations, empirical interpretation, or claim that a particular structure describes nature. A specialized specification shall explicitly label any physical interpretation or hypothesis that it adds.

## 4.2 Manifold structure

### RS-G001 — Smooth base manifold

The base spacetime set \(M\) of RS-D001 shall be modeled, when differential geometry is required, as a Hausdorff, second-countable smooth manifold of declared dimension \(n\). Its differentiability class shall be stated; absent a specialization, it is \(C^\infty\).

### RS-G002 — Coordinate chart

A chart is a pair \((U,x)\), where \(U\subseteqM\) is open and \(x:U\to x(U)\subseteq\mathbb R^n\) is a homeomorphism with mutually smooth transition maps on chart overlaps.

### RS-G003 — Atlas

An atlas \(\mathfrak A=\{(U_i,x_i)\}\) covers \(M\). Compatible atlases represent the same smooth structure. Coordinate expressions shall not be treated as coordinate-independent objects.

### RS-G004 — Tangent space

For \(p\inM\), \(T_pM\) denotes the real vector space of tangent vectors at \(p\), defined equivalently by derivations or chart-equivalence classes of curves.

### RS-G005 — Tangent bundle

The tangent bundle is the disjoint union

\[
TM=\bigsqcup_{p\inM}T_pM,
\]

with canonical projection \(\pi_{TM}:TM\toM\).

### RS-G006 — Cotangent bundle

The cotangent space is \(T_p^*M=(T_pM)^*\), and the cotangent bundle is \(T^*M=\bigsqcup_pT_p^*M\), with its canonical projection to \(M\).

### RS-G007 — Tensor bundle

For nonnegative integers \(r,s\), the type-\((r,s)\) tensor bundle is

\[
T^r_sM=(TM)^{\otimes r}\otimes(T^*M)^{\otimes s}.
\]

A tensor field is a declared-regularity section of this bundle.

### RS-G008 — Differential-form bundle

The degree-\(k\) exterior bundle is \(\Lambda^kT^*M\). Its smooth sections are differential \(k\)-forms, written \(\Omega^k\(M\)\).

## 4.3 Fiber and bundle structure

### RS-G009 — Fiber bundle

A smooth fiber bundle is a quadruple \((E,M,\pi,F)\) with surjective projection \(\pi:E\toM\), typical fiber \(F\), and local trivializations \(\varphi_i:\pi^{-1}(U_i)\to U_i\times F\) whose transition maps satisfy the declared smoothness conditions.

### RS-G010 — Fiber

The fiber over \(p\inM\) is \(E_p=\pi^{-1}(p)\). Identifying fibers at distinct points requires an explicitly defined bundle map, trivialization, or connection.

### RS-G011 — Local trivialization

A local trivialization shall commute with projection: \(\operatorname{pr}_1\circ\varphi_i=\pi\). On overlaps, \(\varphi_i\circ\varphi_j^{-1}\) defines the transition function.

### RS-G012 — Bundle section

A section is a map \(s:M\to E\) satisfying \(\pi\circ s=\operatorname{id}_{M}\). Local and global sections shall be distinguished explicitly.

### RS-G013 — Bundle morphism

A bundle morphism from \((E,M,\pi_E)\) to \((E',M',\pi_{E'})\) is a pair \((\Phi,f)\) satisfying \(\pi_{E'}\circ\Phi=f\circ\pi_E\). A morphism over the identity has \(f=\operatorname{id}_{M}\).

### RS-G014 — Vector bundle

A vector bundle is a fiber bundle whose fibers are vector spaces and whose transition maps are fiberwise linear. Its rank shall be declared and constant on each connected component unless explicitly stated otherwise.

### RS-G015 — Principal bundle

For a declared Lie group \(G\), a principal \(G\)-bundle \(P(M,G)\) carries a free right \(G\)-action, has orbit space \(M\), and is locally equivariantly trivial.

### RS-G016 — Associated bundle

Given a principal \(G\)-bundle \(P\) and a left action \(\rho:G\times F\to F\), the associated bundle is

\[
P\times_G F=(P\times F)/G,
\]

using the equivalence relation induced by the two actions. The convention for that relation shall be stated.

## 4.4 Resolutive bundle

### RS-G017 — Resolutive state bundle

The geometric carrier of the internal resolutive space \(\mathcal R\) of RS-D002 is a fiber bundle

\[
\pi_M:E_R\longrightarrowM,
\]

whose typical fiber is \(\mathcal R\). This definition is structural and does not assert that \(E_R\) is physically realized.

### RS-G018 — Local resolutive field

A local resolutive state is a section \(R:U\toE_R\) over an open set \(U\subseteqM\). Its components are exactly those established by RS-D004; no additional primitive component is introduced here.

### RS-G019 — Global resolutive field

A global resolutive field is a section defined on all of \(M\). The existence of local sections does not imply the existence of a global section.

### RS-G020 — Resolutive address as bundle data

The resolutive address of RS-D005 shall be represented by a base point together with fiber data in \((E_R)_p\). A coordinate tuple is a representation of that address, not the invariant address itself.

### RS-G021 — Resolutive bundle chart

A resolutive bundle chart is a compatible pair consisting of a base chart on \(U\) and a trivialization \(\pi_M^{-1}(U)\cong U\times\mathcal R\). Component transformations shall follow the transition functions of the bundle.

### RS-G022 — Structure group

The structure group \(G_{\mathcal R}\) is the declared group acting on \(\mathcal R\) through resolutive bundle transition functions. This chapter selects no physical symmetry group; a specialization shall state and justify any restriction of \(G_{\mathcal R}\).

## 4.5 Connections and transport

### RS-G023 — Ehresmann connection

An Ehresmann connection on a bundle \(\pi:E\toM\) is a smooth horizontal subbundle \(HE\subset TE\) such that

\[
TE=HE\oplus VE,\qquad VE=\ker(d\pi).
\]

Its introduction is mathematical and supplies no law of motion.

### RS-G024 — Covariant derivative

For a vector bundle \(E\), a connection may be expressed as a covariant derivative

\[
\nabla:\Gamma(E)\to\Gamma(T^*M\otimes E)
\]

that is real-linear and satisfies \(\nabla(fs)=df\otimes s+f\nabla s\).

### RS-G025 — Parallel transport

A declared connection assigns parallel transport along an admissible piecewise-smooth curve between the corresponding endpoint fibers. Transport is path-dependent unless path independence is separately established.

### RS-G026 — Curvature

The curvature of a covariant derivative is the bundle-endomorphism-valued two-form

\[
\mathcal F_\nabla(X,Y)s=
\nabla_X\nabla_Ys-\nabla_Y\nabla_Xs-\nabla_{[X,Y]}s.
\]

No physical interpretation of \(\mathcal F_\nabla\) is asserted by this definition.

### RS-G027 — Pullback bundle

For a smooth map \(f:N\toM\), the pullback bundle \(f^*E\to N\) has fiber \((f^*E)_q=E_{f(q)}\). Pullbacks shall be used when comparing bundle data defined over different base spaces.

### RS-G028 — Geometric compatibility requirement

Every specialized geometric structure shall declare its base space, total space, fiber, projection, regularity, transition functions, structure group when applicable, and compatibility with RS-D001–RS-D006 and RS-O001. Coordinates, gauges, or trivializations shall not be presented as invariant physical observables without a separately identified and status-labeled hypothesis.

## 4.6 Conformance

A conforming specialization shall:

1. cite the stable identifiers it uses;
2. distinguish invariant objects from coordinate representatives;
3. state all smoothness, dimension, signature, topology, and boundary assumptions;
4. label physical interpretations as hypotheses and empirical conclusions as validated results; and
5. introduce dynamics only in the chapter or specialized specification assigned to dynamics.

This chapter establishes vocabulary and compatibility constraints only. It neither chooses a metric, connection, topology, gauge group, nor dynamical principle for nature.
