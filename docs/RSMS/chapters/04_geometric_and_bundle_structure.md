# Chapter 4 — Geometric and Bundle Structure

**Specification:** RSMS-1.0
**Version:** 1.0-draft.4
**Status:** Normative draft
**Author:** Marcelo Roldão Matos
**Parent document:** `docs/RSMS/RSMS_v1.0.md`

---

## 4.1 Purpose and base manifold

This chapter defines the geometric structures available to later RSMS chapters. It is a normative mathematical specification: every object below is independent of physical interpretation, dynamics, field equations, observations, and computational realization.

### RS-G001 — Base manifold

The base space is an abstract, Hausdorff, second-countable, finite-dimensional smooth manifold

\[
M.
\]

Its dimension is denoted by \(n=\dim M\). Unless a later module explicitly specializes \(n\), no dimension is fixed by this chapter. The word *spacetime* is retained as the registered name of \(M\), not as an additional physical assumption.

An admissible chart is a pair \((U,x)\), where \(U\subseteq M\) is open and

\[
x:U\longrightarrow x(U)\subseteq\mathbb R^n
\]

is a homeomorphism whose overlap maps are smooth wherever defined.

---

## 4.2 Internal Resolutive Space

### RS-G002 — Internal space

The **Internal Resolutive Space** is a smooth manifold

\[
\mathcal R
\]

of dimension \(q=\dim\mathcal R\). It supplies the typical fiber for the bundle defined in Section 4.3. This chapter assigns \(\mathcal R\) no state, material, causal, dynamical, or observational interpretation. Its topology and smooth structure shall be declared by any specialization that requires more than the assumptions stated here.

---

## 4.3 Resolutive Bundle

### RS-G003 — Resolutive bundle

The **Resolutive Bundle** is the smooth fiber bundle

\[
\pi_M:E_R\longrightarrow M
\]

with typical fiber \(\mathcal R\), where:

| Element | Symbol | Definition |
|---|---|---|
| Total space | \(E_R\) | A smooth manifold containing all fibers |
| Base space | \(M\) | The manifold defined by RS-G001 |
| Typical fiber | \(\mathcal R\) | The manifold defined by RS-G002 |
| Projection | \(\pi_M\) | A smooth surjection from \(E_R\) onto \(M\) |

The previously reserved symbol \(\mathcal E_R\) may be used typographically for the same total space only when a module declares \(\mathcal E_R\equiv E_R\); it shall not denote a second bundle implicitly.

No vector-bundle, principal-bundle, product-bundle, group-action, metric, or connection structure is implied by RS-G003. Any such enhancement shall be declared separately.

---

## 4.4 Fibers and local versus global structure

### RS-G004 — Fiber over a point

For every \(p\in M\), the fiber over \(p\) is

\[
E_{R,p}:=\pi_M^{-1}(\{p\})
=\{e\in E_R\mid\pi_M(e)=p\}.
\]

Each \(E_{R,p}\) is diffeomorphic to \(\mathcal R\), but no preferred diffeomorphism is assumed.

### RS-G005 — Local and global structure

The restriction over an open set \(U\subseteq M\) is

\[
E_R|_U:=\pi_M^{-1}(U).
\]

The bundle is locally a product as specified in RS-G007. Local product structure shall not be used to infer a global diffeomorphism \(E_R\cong M\times\mathcal R\). A global product identification exists only when separately established.

---

## 4.5 Charts, atlases, trivializations, and transition maps

### RS-G006 — Charts and atlases

A smooth atlas on a manifold is a collection of compatible smooth charts whose domains cover that manifold. Atlases on \(M\), \(\mathcal R\), and \(E_R\) shall be distinguished by context or explicit subscripts. Two atlases define the same smooth structure when their union is a smooth atlas.

### RS-G007 — Local trivialization

For every \(p\in M\), there exists an open neighborhood \(U\ni p\) and a diffeomorphism

\[
\Phi_U:\pi_M^{-1}(U)\longrightarrow U\times\mathcal R
\]

such that

\[
\operatorname{pr}_1\circ\Phi_U
=\pi_M|_{\pi_M^{-1}(U)}.
\]

The pair \((U,\Phi_U)\) is a local trivialization. A bundle atlas is a collection \(\{(U_a,\Phi_a)\}_{a\in A}\) whose base domains cover \(M\).

### RS-G008 — Transition map

On a nonempty overlap \(U_a\cap U_b\), the change of trivialization has the form

\[
\Phi_a\circ\Phi_b^{-1}(p,r)
=\bigl(p,g_{ab}(p)(r)\bigr),
\]

where \(g_{ab}(p):\mathcal R\to\mathcal R\) is a diffeomorphism and the induced evaluation map is smooth. The transition maps satisfy

\[
g_{aa}=\operatorname{id}_{\mathcal R},\qquad
g_{ab}=g_{ba}^{-1},\qquad
g_{ab}g_{bc}=g_{ac}
\]

on their respective domains. Composition acts from right to left. A reduced structure group is not assumed.

---

## 4.6 Sections

### RS-G009 — Smooth section

A smooth section of \(E_R\) is a smooth map

\[
s:M\longrightarrow E_R
\]

satisfying

\[
\pi_M\circ s=\operatorname{id}_M.
\]

The set of global smooth sections is denoted by \(\Gamma(E_R)\). For open \(U\subseteq M\), a local section is a smooth map \(s_U:U\to E_R|_U\) satisfying \(\pi_M\circ s_U=\operatorname{id}_U\), and the set of such sections is \(\Gamma(U,E_R)\). The existence of local sections does not imply the existence of a global section.

---

## 4.7 Tangent structures

### RS-G010 — Tangent and cotangent spaces

For \(p\in M\), the tangent space is \(T_pM\), and its dual is the cotangent space

\[
T_p^*M:=\operatorname{Hom}(T_pM,\mathbb R).
\]

The tangent and cotangent bundles are the disjoint unions

\[
TM:=\bigsqcup_{p\in M}T_pM,
\qquad
T^*M:=\bigsqcup_{p\in M}T_p^*M,
\]

with their canonical projections onto \(M\). Analogous notation applies to \(E_R\) and \(\mathcal R\).

### RS-G011 — Differential map

For a smooth map \(F:N\to P\), its differential at \(x\in N\) is the linear map

\[
dF_x:T_xN\longrightarrow T_{F(x)}P.
\]

It satisfies \(d(G\circ F)_x=dG_{F(x)}\circ dF_x\). For the bundle projection, the vertical subspace at \(e\in E_R\) is

\[
V_eE_R:=\ker(d\pi_M)_e\subseteq T_eE_R.
\]

No complementary horizontal subspace is canonical under the assumptions above.

---

## 4.8 Tensor structures

### RS-G012 — Admissible tensors

For a smooth manifold \(N\), a tensor field of type \((r,s)\) is a smooth section

\[
T\in\Gamma\!\left((TN)^{\otimes r}\otimes(T^*N)^{\otimes s}\right),
\qquad r,s\in\mathbb N.
\]

An **admissible tensor** in this chapter is any such smooth tensor on a declared manifold, or a section of a tensor bundle constructed from declared vector bundles and their duals, whose base, type, regularity, and transformation law are specified. Tensors on \(M\), \(E_R\), and \(\mathcal R\) shall not be identified without an explicit pullback, pushforward where defined, or bundle morphism.

Locally, components are written

\[
T^{\mu_1\ldots\mu_r}{}_{\nu_1\ldots\nu_s},
\]

and obey the Chapter 2 summation and free-index conventions.

---

## 4.9 Differential forms

### RS-G013 — Differential forms and wedge product

A differential \(k\)-form on a smooth manifold \(N\) is a smooth section

\[
\omega\in\Omega^k(N):=\Gamma(\Lambda^kT^*N).
\]

For \(\alpha\in\Omega^k(N)\) and \(\beta\in\Omega^\ell(N)\), the wedge product

\[
\alpha\wedge\beta\in\Omega^{k+\ell}(N)
\]

is bilinear, associative, and graded-commutative:

\[
\alpha\wedge\beta=(-1)^{k\ell}\beta\wedge\alpha.
\]

### RS-G014 — Exterior derivative

The exterior derivative is the unique family of linear maps

\[
d:\Omega^k(N)\longrightarrow\Omega^{k+1}(N)
\]

that agrees with the differential on functions and satisfies

\[
d(\alpha\wedge\beta)
=d\alpha\wedge\beta+(-1)^k\alpha\wedge d\beta,
\qquad d\circ d=0.
\]

### RS-G015 — Pullback of forms

For a smooth map \(F:N\to P\), the pullback is

\[
F^*:\Omega^k(P)\longrightarrow\Omega^k(N),
\]

defined pointwise by

\[
(F^*\omega)_x(v_1,\ldots,v_k)
=\omega_{F(x)}(dF_xv_1,\ldots,dF_xv_k).
\]

It satisfies \((G\circ F)^*=F^*\circ G^*\), \(F^*(\alpha\wedge\beta)=F^*\alpha\wedge F^*\beta\), and \(d(F^*\alpha)=F^*(d\alpha)\).

---

## 4.10 Connections

### RS-G016 — Connection on a vector bundle

For a smooth vector bundle \(\pi_V:V\to M\), a connection is an \(\mathbb R\)-linear map

\[
\nabla:\Gamma(V)\longrightarrow\Omega^1(M;V)
\]

such that, for \(f\in C^\infty(M)\) and \(\sigma\in\Gamma(V)\),

\[
\nabla(f\sigma)=df\otimes\sigma+f\nabla\sigma.
\]

Equivalently, it may be specified by covariant derivatives \(\nabla_X\sigma\) satisfying the standard linearity and Leibniz properties.

### RS-G017 — Ehresmann connection

On the smooth bundle \(E_R\), an Ehresmann connection is a smooth choice of horizontal subspaces \(H_eE_R\) such that

\[
T_eE_R=H_eE_R\oplus V_eE_R
\]

for every \(e\in E_R\). This definition introduces only an optional geometric structure. This chapter selects no connection and assigns none a physical role.

---

## 4.11 Curvature

### RS-G018 — Curvature of a vector-bundle connection

For a connection \(\nabla\) on \(V\to M\), its curvature is the \(\operatorname{End}(V)\)-valued two-form defined by

\[
R^\nabla(X,Y)\sigma
:=\nabla_X\nabla_Y\sigma
-\nabla_Y\nabla_X\sigma
-\nabla_{[X,Y]}\sigma.
\]

For an Ehresmann connection with horizontal projection \(h\) and vertical projection \(v\), its curvature may be defined on vector fields by the vertical obstruction

\[
\Omega(X,Y):=-v[hX,hY].
\]

Sign conventions shall be stated whenever curvature components are used. Curvature here is a geometric definition only; no equation or interpretation is implied.

---

## 4.12 Metrics

### RS-G019 — Metric structure

A pseudo-Riemannian metric on a smooth manifold \(N\) is a smooth section

\[
g\in\Gamma(S^2T^*N)
\]

such that \(g_p\) is a nondegenerate symmetric bilinear form on every \(T_pN\), with constant signature on each connected component. A Riemannian metric is positive definite.

Metrics on \(M\), \(E_R\), \(\mathcal R\), or associated bundles are distinct structures and shall be separately declared. Chapter 2's default signature applies if a spacetime metric is introduced, but neither the existence nor explicit components of such a metric are required here. No metric on \(\mathcal R\) or \(E_R\) is selected by this chapter.

---

## 4.13 Orientation

### RS-G020 — Orientation

An orientation of an \(n\)-dimensional manifold \(N\) is an equivalence class of atlases whose coordinate transition maps have positive Jacobian determinant on overlaps. Equivalently, when available, it may be represented by a nowhere-vanishing top-degree form up to multiplication by a positive smooth function.

Orientations of \(M\), \(\mathcal R\), and \(E_R\) are independent declarations. None is assumed unless explicitly stated. Integrals requiring orientation shall state the selected orientation; boundary orientation, when applicable, shall use the outward-normal-first convention unless a module declares otherwise.

---

## 4.14 Coordinate and index conventions

### RS-G021 — Coordinate conventions

The following conventions refine and preserve Chapter 2:

| Notation | Range and role |
|---|---|
| \(x^\mu\), \(\mu,\nu,\rho,\ldots\) | Coordinates and components on \(M\); \(\mu=0,\ldots,n-1\) |
| \(x^i\), \(i,j,k,\ldots\) | Spatially designated coordinates only after a module declares such a split |
| \(y^A\), \(A,B,C,\ldots\) | Local coordinates and components on \(\mathcal R\); \(A=1,\ldots,q\) |
| \(a,b,c,\ldots\) | Local frame indices on a declared vector bundle |
| \(a,b\in\mathcal A\) | Trivialization labels when explicitly identified as elements of an atlas index set \(\mathcal A\) |

Upper indices are contravariant and lower indices are covariant. Repeated upper-lower pairs are summed; repeated indices in the same position are not summed without declaration. Symmetrization and antisymmetrization use unit weight:

\[
T_{(\mu\nu)}:=\tfrac12(T_{\mu\nu}+T_{\nu\mu}),
\qquad
T_{[\mu\nu]}:=\tfrac12(T_{\mu\nu}-T_{\nu\mu}).
\]

An index shall be raised or lowered only with a declared nondegenerate bilinear form. Coordinate changes, changes of local frame, and changes of bundle trivialization are distinct and shall not be conflated.

---

## 4.15 Normative identifier registry

The `RS-G###` namespace is reserved for normative geometric definitions and requirements introduced by this chapter.

| Identifier range | Content | Status |
|---|---|---|
| RS-G001–RS-G003 | Base, internal, and bundle structures | Normative draft |
| RS-G004–RS-G009 | Fibers, local structure, and sections | Normative draft |
| RS-G010–RS-G015 | Tangent, tensor, and form structures | Normative draft |
| RS-G016–RS-G020 | Connections, curvature, metrics, and orientation | Normative draft |
| RS-G021 | Coordinate and index conventions | Normative draft |
| RS-G022–RS-G028 | Conformance requirements | Normative draft |

These identifiers are stable and shall not be reassigned. A future revision may refine a definition only through documented change control.

---

## 4.16 Conformance requirements

### RS-G022 — Declared geometric base

A conforming future module shall identify every geometric object's base manifold or bundle and shall document every specialization of \(M\), \(\mathcal R\), or \(E_R\).

### RS-G023 — Bundle compatibility

A conforming bundle construction shall declare its total space, base, fiber, projection, regularity, local trivializations, and transition data. It shall not infer global triviality from local triviality.

### RS-G024 — Map and section compatibility

Every geometric map shall declare its domain and codomain. Every object called a section shall satisfy the applicable projection identity, globally or on its stated local domain.

### RS-G025 — Tensor and form compatibility

Every tensor or differential form shall declare its bundle, type or degree, and minimum regularity. Operations between objects on different spaces shall use an explicitly defined geometric map.

### RS-G026 — Additional-structure declaration

Metrics, orientations, connections, horizontal distributions, group actions, and reductions of structure group shall be treated as additional structures. Their existence, conventions, and compatibility conditions shall be stated rather than inferred.

### RS-G027 — Coordinate independence

A normative construction shall be defined coordinate-free or shall provide a transformation law establishing independence from the chosen chart, frame, or trivialization.

### RS-G028 — No implicit dynamics or physical status

Conformance with this chapter establishes geometric well-formedness only. It shall not be cited as establishing dynamics, a physical hypothesis, empirical validity, or a computational model. Chapters 5 and 6 may use these structures only after separately declaring the fields, operators, assumptions, and dynamical principles they introduce.

---

## 4.17 Chapter status

| Criterion | Status |
|---|---|
| Base and internal manifolds defined | Draft complete |
| Resolutive Bundle and fibers defined | Draft complete |
| Local trivializations and transition maps defined | Draft complete |
| Sections defined | Draft complete |
| Tangent, cotangent, and tensor structures defined | Draft complete |
| Differential forms and pullbacks defined | Draft complete |
| Connections and curvature defined abstractly | Draft complete |
| Metrics and orientation defined abstractly | Draft complete |
| Coordinate conventions consolidated | Draft complete |
| Conformance requirements defined | Draft complete |
| Physical hypotheses introduced | None |
| Dynamics or field equations introduced | None |
| Empirical validation applicable | Not yet |
| Computational implementation applicable | Not yet |

---

## Foundation for subsequent chapters

Chapter 5 may define fields as sections of the bundles registered here and may define operators using the tangent, cotangent, tensor, form, and connection structures. Chapter 6 may subsequently state dynamical or variational principles on those declared objects. This dependency statement introduces neither fields nor dynamics in Chapter 4; it only fixes the geometric domains and compatibility rules that those chapters shall reference.

---

## Next chapter

**Chapter 5 — Fundamental Fields and Operators** may introduce its normative objects on the geometric framework defined here, with their status and assumptions declared independently.
