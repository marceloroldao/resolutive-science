# RCMS Protocol 08 — Logarithmic Provenance Outcome

**Final classification:** `LOG_FORM_CONDITIONALLY_DERIVED`  
**RSMS compatibility:** RSMS-1.0-rc.1  
**Protocol:** `docs/RCMS/protocols/protocol08_logarithmic_provenance.md`  

## 1. Result boundary

Protocol 08 establishes a **conditional mathematical provenance** for the logarithmic state drift used in RCMS. It does not derive the scale-composition hypothesis from a fundamental Resolutive Master Equation and does not establish a new physical law.

The frozen workflow explicitly reported:

- `PHYSICAL_LAW_CLAIM=NO`;
- `MASTER_EQUATION_DERIVATION=NO`;
- `CONDITIONAL_SCALE_COMPOSITION_DERIVATION=YES`.

## 2. Conditional derivation

The preregistered hypothesis P08-H001 assumes a continuous scalar drift `S` on positive scale ratios with

\[
S(1)=0,
\qquad
S(\lambda_1\lambda_2)=S(\lambda_1)+S(\lambda_2).
\]

Define

\[
f(x)=S(e^x),\qquad x\in\mathbb R.
\]

Then

\[
f(x+y)
=S(e^{x+y})
=S(e^xe^y)
=S(e^x)+S(e^y)
=f(x)+f(y).
\]

Because `S` is continuous, `f` is continuous. The continuous solutions of the additive Cauchy equation are linear, so for some real dimensionless constant `s_1`,

\[
f(x)=s_1x.
\]

Substituting `x=ln(lambda)` gives

\[
\boxed{S(\lambda)=s_1\ln\lambda}.
\]

RCMS already declares

\[
1+z=\frac{a(t_0)}{a(t)},
\]

therefore for the scale ratio `lambda=1+z`,

\[
\boxed{S_R(z)=s_1\ln(1+z)}.
\]

Thus the functional form of RC-E018 is no longer arbitrary **conditional on P08-H001**. The physical truth of P08-H001 remains open.

## 3. T1 — composition regression

The deterministic numerical regression used multiple positive scale ratios and signed drift coefficients.

Results:

- maximum composition residual: `1.776e-15`;
- maximum identity residual: `0.000e+00`;
- `T1_PASS=True`.

These values verify the software implementation of the exact logarithmic homomorphism to floating-point precision. They are not empirical evidence for P08-H001.

## 4. Link to the bounded RCMS candidate

The existing bounded candidate is

\[
H_A^2(z)
=H_{\rm ref}^2(z)
+H_0^2\epsilon_R\tanh\!\left[s_1\ln(1+z)\right].
\]

For

\[
x=s_1\ln(1+z),
\]

the expansion

\[
\tanh x=x-\frac{x^3}{3}+O(x^5)
\]

gives

\[
H_A^2-H_{\rm ref}^2
=H_0^2\epsilon_Rs_1\ln(1+z)+O(x^3).
\]

With the reduced effective amplitude

\[
A_R^{\rm eff}=\epsilon_Rs_1,
\]

the first-order limit is exactly the one-parameter surrogate used by Protocols 01–07:

\[
\boxed{
H_A^2(z)
\approx H_{\rm ref}^2(z)
+H_0^2A_R^{\rm eff}\ln(1+z)
}.
\]

This establishes a direct mathematical bridge between RC-E020 and the observational surrogate, but only in a quantified small-drift regime.

## 5. T2 — quantified linearization domain

The preregistered relative error was

\[
\delta_{\rm lin}(x)
=\frac{|\tanh x-x|}{|\tanh x|}
\]

away from the numerical zero safeguard.

The largest permitted magnitudes were:

| Relative deformation error | Maximum `|x|` |
|---:|---:|
| 0.1% | `0.054777733328` |
| 1% | `0.173378397072` |
| 5% | `0.389241019198` |

The small-`x` cubic regression gave

`T2_small_x_cubic_ratio=0.999999600054`,

consistent with the frozen `-x^3/3` leading correction.

## 6. T3 — descriptive domain diagnostic at the recurring amplitude

Only after T0–T2 were fixed, the descriptive cross-protocol value

\[
A_R\simeq0.211141330
\]

was inserted through

\[
\epsilon_Rs_1=A_R.
\]

For each error threshold and maximum redshift, T3 computes the largest allowed `|s_1|` and the corresponding minimum `|epsilon_R|` required to preserve the product.

| Error | Redshift domain | `|s1| max` | minimum `|epsilon_R|` for `A_R=0.211141330` |
|---:|---:|---:|---:|
| 0.1% | `z<=1` | `0.079027564224` | `2.671742854207` |
| 0.1% | `z<=2.33` | `0.045535323753` | `4.636868975510` |
| 0.1% | `z<=3` | `0.039513782112` | `5.343485708414` |
| 1% | `z<=1` | `0.250132153653` | `0.844119106305` |
| 1% | `z<=2.33` | `0.144125011438` | `1.464987429273` |
| 1% | `z<=3` | `0.125066076827` | `1.688238212611` |
| 5% | `z<=1` | `0.561556088108` | `0.375993305871` |
| 5% | `z<=2.33` | `0.323566068734` | `0.652544720855` |
| 5% | `z<=3` | `0.280778044054` | `0.751986611743` |

The domain is mathematically nonempty at every preregistered threshold and redshift range. These values are not separate measurements of `epsilon_R` and `s_1`; the observational one-parameter surrogate identifies their product in the linearized limit.

## 7. Interpretation

Protocol 08 changes the status of the logarithmic form in a limited but meaningful way.

Before Protocol 08, RC-E018 was only a phenomenological low-complexity drift function.

After Protocol 08, the same form has a conditional derivation:

\[
\text{continuous additive drift under multiplicative scale composition}
\Longrightarrow
S_R(z)=s_1\ln(1+z).
\]

Together with the existing bounded candidate RC-E020,

\[
\epsilon_R\tanh[S_R]
\xrightarrow{|S_R|\ll1}
(\epsilon_Rs_1)\ln(1+z),
\]

which explains why the observational surrogate is the first-order member of the bounded candidate rather than an unrelated fitted function.

However, the crucial physical question has merely moved one level deeper: **why should the resolutive scalar drift satisfy P08-H001?**

That question cannot be answered by this protocol because RSMS-1.0 deliberately does not select a universal dynamics. A future derivation must obtain the additive scale-composition law from a separately specified resolutive dynamics, action, master equation, or geometric principle without using the observational success of the log form as a premise.

## 8. Final classification

The preregistered conditions are satisfied:

- logarithmic uniqueness follows from the frozen hypothesis;
- dimensional admissibility is preserved because the logarithm acts on the dimensionless positive ratio `1+z`;
- numerical composition and identity regressions pass;
- the bounded candidate has a quantified nonempty linearization domain;
- no observational fit was used to select the functional form.

Therefore:

\[
\boxed{\texttt{LOG\_FORM\_CONDITIONALLY\_DERIVED}}
\]

This classification does **not** mean `MASTER_EQUATION_DERIVED` and does not validate the full Resolutive Physics ontology.

## 9. Traceability

- preregistration: PR #75;
- execution: PR #76;
- workflow run: `31859575132`;
- artifact: `rcms-protocol08-log-provenance`;
- artifact SHA256: `4661d8b9de334427a39b9f24aaf88edfc13e74d07cb5906f224c33fd8dbb8908`.
