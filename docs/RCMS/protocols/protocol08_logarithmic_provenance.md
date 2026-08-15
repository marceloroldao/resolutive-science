# RCMS Protocol 08 — Logarithmic Provenance Test

**Status:** Preregistered theoretical consistency protocol  
**RSMS compatibility:** RSMS-1.0-rc.1  
**Parent specification:** RCMS-0.1-draft.2  

## 1. Purpose

Protocol 08 tests whether the logarithmic state drift already used phenomenologically in RCMS,

\[
S_R(z)=s_1\ln(1+z),
\]

can be obtained from a simple, independently stated scale-composition hypothesis rather than being selected solely as a convenient fit function.

This protocol does **not** attempt to prove the full Resolutive Physics ontology, derive a universal Resolutive Master Equation, or infer a fundamental value of the empirical amplitude `A_R`.

## 2. Existing specification boundary

RCMS currently labels

\[
S_R(z)=s_1\ln(1+z)
\tag{RC-E018}
\]

as a phenomenological low-complexity state-evolution model. The preferred bounded candidate is

\[
H_A^2(z)=H_{\rm ref}^2(z)+H_0^2\epsilon_R\tanh\!\left[s_1\ln(1+z)\right].
\tag{RC-E020}
\]

RSMS Chapter 6 deliberately does not select a universal physical dynamics. Therefore Protocol 08 may establish only a conditional mathematical provenance: **if** the new scale-composition hypothesis holds, **then** the logarithmic form follows.

## 3. Frozen scale variable

RCMS retains the standard background redshift map

\[
1+z=\frac{a(t_0)}{a(t_{\rm em})}.
\tag{RC-E004}
\]

Define the positive dimensionless scale ratio

\[
\lambda\equiv\frac{a(t_0)}{a(t)}=1+z,
\qquad \lambda>0.
\tag{P08-E001}
\]

No alternative redshift law is introduced in this protocol.

## 4. New hypothesis under test

### P08-H001 — Additive scale-composition drift

Let `S(λ)` denote the accumulated dimensionless background resolutive drift between two scale states related by positive ratio `λ`.

Freeze the following assumptions before the derivation is evaluated:

1. **Identity:** `S(1)=0`.
2. **Composition:** successive scale changes compose multiplicatively while accumulated drift composes additively,

   \[
   S(\lambda_1\lambda_2)=S(\lambda_1)+S(\lambda_2).
   \tag{P08-E002}
   \]

3. **Regularity:** `S` is continuous on `R_{>0}`. Continuity may be weakened mathematically, but no weaker assumption will be introduced after results are inspected.
4. **One-dimensionality:** this test concerns only the reduced scalar `S_R`; it does not assert that the full resolutive state is one-dimensional.

P08-H001 is a **new RCMS hypothesis**, not an inherited RSMS law and not an experimentally validated statement.

## 5. Frozen mathematical proposition

### P08-P001 — Logarithmic uniqueness under continuous scale composition

Protocol 08 shall verify that P08-H001 implies

\[
S(\lambda)=s_1\ln\lambda
\tag{P08-E003}
\]

for some real dimensionless constant `s_1`.

With P08-E001 this becomes

\[
S_R(z)=s_1\ln(1+z),
\tag{P08-E004}
\]

which has the same functional form as RC-E018.

The proof shall use only the stated composition and regularity assumptions and standard real analysis/group-homomorphism facts. It shall not use the observationally fitted value of `A_R`.

## 6. Link to the observational surrogate

The bounded RCMS candidate RC-E020 has deformation

\[
F_A(z)=\epsilon_R\tanh[S_R(z)].
\]

For sufficiently small `|S_R|`, the frozen linearization is

\[
\tanh S_R=S_R-\frac{S_R^3}{3}+O(S_R^5).
\tag{P08-E005}
\]

Therefore, conditional on P08-H001 and in the declared small-drift regime,

\[
F_A(z)=\epsilon_Rs_1\ln(1+z)+O\!\left([s_1\ln(1+z)]^3\right).
\tag{P08-E006}
\]

Define only for this reduced-limit comparison

\[
A_R^{\rm eff}\equiv\epsilon_Rs_1.
\tag{P08-E007}
\]

Then

\[
H_A^2(z)\approx H_{\rm ref}^2(z)+H_0^2A_R^{\rm eff}\ln(1+z),
\tag{P08-E008}
\]

which is the one-parameter surrogate used by the observational screening protocols.

P08-E008 is **not** valid outside a quantified small-drift domain merely because the first-order term has the desired form.

## 7. Preregistered tests

### P08-T0 — Logical provenance audit

Verify that:

- `λ` is positive and dimensionless;
- the logarithm is dimensionally admissible under RSMS Chapter 8;
- P08-E003 follows from P08-H001 without observational input;
- `S(1)=0` is recovered;
- the composition identity is satisfied exactly by the derived form.

### P08-T1 — Functional-equation numerical regression

For a deterministic grid of positive `λ1, λ2` and several signed `s1` values, verify numerically that

\[
S(\lambda_1\lambda_2)-S(\lambda_1)-S(\lambda_2)
\]

is zero within floating-point tolerance.

This is a software regression test, not evidence for the physical truth of P08-H001.

### P08-T2 — Linearization error map

For `x=s1 ln(1+z)`, compute

\[
\delta_{\rm lin}(x)=\frac{|\tanh x-x|}{\max(|\tanh x|,\epsilon_{\rm num})}.
\tag{P08-E009}
\]

Report the largest `|x|` for which the relative deformation error remains below frozen thresholds of `0.1%`, `1%`, and `5%`.

No threshold may be changed after execution to make the observational surrogate appear more fundamental.

### P08-T3 — Observational-domain consistency diagnostic

Using the observationally recurring descriptive value `A_R≈0.21` **only after** T0–T2 are complete, report what combinations of `(epsilon_R, s1)` satisfy `epsilon_R s1≈0.21` while remaining inside each T2 small-drift domain over declared redshift ranges `z<=1`, `z<=2.33`, and `z<=3`.

T3 is an identifiability/domain diagnostic. It shall not claim separate measurement of `epsilon_R` or `s1`, and shall not tune either parameter to improve an observational likelihood.

## 8. Frozen outcomes

Protocol 08 shall use one of the following classifications:

- `LOG_FORM_CONDITIONALLY_DERIVED` — P08-H001 implies the log form and T0–T2 pass; the bounded candidate reduces to the observational surrogate in a quantified nonempty domain.
- `LOG_FORM_MATHEMATICALLY_VALID_BUT_SURROGATE_DOMAIN_NARROW` — the log proposition passes but the linearized observational surrogate has only a very restricted domain.
- `LOG_FORM_PROVENANCE_FAILED` — the stated assumptions do not imply the claimed form or an implementation/audit reveals a mathematical inconsistency.

No classification states that P08-H001 is a law of nature or that the full Resolutive Physics ontology has been derived.

## 9. Anti-circularity rule

The positive observational results for `A_R` may not be used to justify P08-H001. P08-H001 is judged by mathematical coherence and later, if an independent physical derivation becomes available, by that derivation.

The observational value enters only the post-derivation T3 domain diagnostic. Failure of T3 to accommodate `A_R≈0.21` in a useful small-drift domain shall be preserved as a negative result.

## 10. Promotion rule

If Protocol 08 passes, RC-E018 may be reclassified in a future RCMS revision from a purely phenomenological drift function to a **conditionally derived scale-composition candidate**, with P08-H001 stated explicitly.

It shall not be reclassified as a fundamental resolutive law until P08-H001 itself is derived from a separately specified resolutive dynamics or master equation.
