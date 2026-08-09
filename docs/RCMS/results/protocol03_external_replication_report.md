# RCMS Protocol 03 — External Replication Report

**Status:** Completed external-replication protocol  
**Model status:** Frozen one-parameter phenomenological screening surrogate  
**Final classification:** `EXTERNAL_REPLICATION_INCONCLUSIVE`

---

## 1. Purpose

Protocol 03 tested whether the positive low-redshift RCMS screening region observed in Protocols 01–02 would reappear in observational data that were not part of the primary discovery set.

The model was not changed:

\[
H_{\mathrm{eff}}^2(z)
=
H_{\Lambda\mathrm{CDM}}^2(z)
+
H_0^2 A_R\ln(1+z).
\]

No new RCMS coefficient, redshift dependence, CMB prior, SH0ES calibration, Pantheon+ observation, or DESI DR2 BAO datum was added to the primary Protocol 03 external statistic.

## 2. Carried-forward reference region

The Protocol 01/02 region carried forward for directional comparison was

\[
A_R^{\rm P01}=0.187021,
\]

with profile interval

\[
0.098671\le A_R\le0.276779
\]

at \(\Delta\chi^2\le1\), and the Protocol 02 null Monte Carlo calibration was

\[
p_{\rm MC}=0.03592814.
\]

These quantities were reference targets only and were not used to tune the external likelihoods.

## 3. P03-T1 — DES-SN5YR/Dovekie external supernova replication

The external supernova analysis used the frozen public DES-SN5YR/Dovekie release at upstream revision

`c9a4fcafc4cbd19bd750dee47fc76194a45c181f`.

The production Hubble diagram, statistical+systematic precision matrix, and upstream likelihood implementation were frozen by Git blob SHA before the RCMS fit was executed.

The likelihood preserved the upstream conventions for `zHD`, `zHEL`, the distance-modulus construction, and analytic marginalization of the additive supernova intercept.

Hosted result:

### Flat Lambda-CDM

\[
\chi^2_{\Lambda\mathrm{CDM}}=1640.273214,
\qquad
\Omega_m=0.330317.
\]

### RCMS surrogate

\[
\chi^2_{\rm RCMS}=1638.906815,
\qquad
\Omega_m=0.266117,
\qquad
A_R=0.382099.
\]

The profile interval was

\[
0.055322\le A_R\le0.707729.
\]

The raw likelihood improvement was

\[
\Delta\chi^2
=
\chi^2_{\Lambda\mathrm{CDM}}-\chi^2_{\rm RCMS}
=1.366399.
\]

Model-complexity diagnostics were

\[
\Delta\mathrm{AIC}=-0.633601,
\qquad
\Delta\mathrm{BIC}=-6.140193,
\]

using the convention reference minus RCMS.

Therefore the external DES-SN data selected a **positive external parameter region**, but the likelihood improvement was too small to compensate for the additional RCMS parameter under AIC/BIC.

This is directional replication, not independent model-selection evidence.

## 4. P03-T2 — DES Y6 angular BAO outside DESI overlap

The DESI-independent angular BAO target was the DES Y6 `DR1tiles_noDESI` measurement adopted by the upstream analysis for cosmological inference:

\[
z_{\rm eff}=0.851,
\qquad
\alpha=0.9690\pm0.0296.
\]

The observable is

\[
\alpha
=
\frac{D_M(z)/r_d}
{D_M^{\rm fid}(z)/r_d^{\rm fid}}.
\]

Protocol 03 had pre-registered that the global BAO scale or sound-horizon nuisance must remain free and symmetric between the two models, with no post-hoc CMB or SH0ES calibration.

For one transverse BAO datum,

\[
\frac{D_M(z)}{r_d}
=
\frac{c}{H_0r_d}
\int_0^z\frac{dz'}{E(z')},
\]

so the free scale

\[
q=\frac{c}{H_0r_d}
\]

can exactly absorb the predicted distance of any admissible late-time shape.

The hosted identifiability test verified this explicitly for multiple positive, zero, and negative \(A_R\) cases. Every case reached zero BAO residual after profiling the single global scale.

The formal result was

`P03_T2_IDENTIFIABILITY=SCALE_DEGENERATE_SINGLE_TRANSVERSE_BAO`

and

`P03_T2_MODEL_SELECTION=NOT_IDENTIFIABLE_WITH_FREE_GLOBAL_SCALE`.

This is neither evidence for RCMS nor evidence for the null model. It is a limitation of the information content of the single compressed transverse BAO datum under the frozen nuisance policy.

## 5. P03-T3 — external joint replication

P03-T3 combined only:

1. DES-SN5YR/Dovekie; and
2. the DES Y6 `DR1tiles_noDESI` angular BAO datum.

Because P03-T2 proved exact scale degeneracy for the single BAO point, the joint analysis was designed as a numerical closure test. The joint best fit was required to reproduce P03-T1 while the BAO contribution profiled to approximately zero.

The closure passed at approximately \(10^{-7}\) numerical precision.

The joint results were therefore

\[
A_R=0.382099,
\qquad
0.055322\le A_R\le0.707729,
\qquad
\Delta\chi^2=1.366399.
\]

The BAO contributions at the two model optima were

\[
\chi^2_{\rm BAO,\Lambda CDM}=0,
\qquad
\chi^2_{\rm BAO,RCMS}\simeq1.4\times10^{-29}.
\]

Thus the apparent joint positive direction is entirely carried by the DES-SN likelihood. The BAO datum supplies no independent \(A_R\) information under the preregistered free-scale treatment.

## 6. P03-T4 — directional consistency

No data were refitted in P03-T4.

The frozen regions compared were

\[
A_R^{\rm P01}=0.187021,
\qquad
[0.098671,0.276779],
\]

and

\[
A_R^{\rm P03}=0.382099,
\qquad
[0.055322,0.707729].
\]

Their interval overlap is

\[
[0.098671,0.276779],
\]

with width

\[
0.178108.
\]

Both best-fit values are positive, and the hosted T4 diagnostic returned

`P03_T4_DIRECTIONAL_COMPATIBILITY=POSITIVE_INTERVAL_OVERLAP`.

The difference between the two point estimates is small relative to the combined descriptive profile widths. This is a compatibility statement, not a significance calculation.

## 7. External-replication decision

The preregistered strongest label, `EXTERNAL_REPLICATION_SUPPORTED`, requires an informative independent joint result rather than a nominal joint combination whose second probe is exactly scale-degenerate.

Protocol 03 instead found:

- an independent DES supernova sample with a positive \(A_R\) profile region;
- quantitative overlap between the external and Protocol 01/02 positive intervals;
- no negative-sign conflict;
- but only \(\Delta\chi^2=1.366399\) in the external informative probe;
- AIC and BIC that do not favor the RCMS surrogate;
- and an external DES Y6 BAO datum that cannot independently identify \(A_R\) under the preregistered free global scale.

The appropriate Protocol 03 classification is therefore

\[
\boxed{\texttt{EXTERNAL\_REPLICATION\_INCONCLUSIVE}}.
\]

This classification is stronger than an external sign conflict and preserves the fact that the positive direction replicated in an independent supernova dataset. It is weaker than `EXTERNAL_REPLICATION_SUPPORTED` because the external evidence is not yet independently multi-probe and does not favor the extra parameter under the declared model-selection diagnostics.

## 8. Optional external H(z) stage

No additional H(z) dataset was added to the primary Protocol 03 statistic. The preregistration permitted such a stage only after a dataset with demonstrable independence from the Protocol 01 Moresco table and auditable covariance treatment had been frozen.

No such additional dataset was frozen before completion of P03-T1 through P03-T4, so no post-hoc expansion-history sample is introduced into this report.

## 9. Prospective-prediction stage

P03-T5 is **deferred**.

A prospective prediction should be issued only when there is a sufficiently informative frozen external profile to justify testing a genuinely future, unseen observation. Because the present external joint statistic is effectively DES-SN-only with respect to \(A_R\), this protocol does not promote the current profile into a discovery-level prospective claim.

Any future prospective test must be recorded in a new immutable prediction record before the target dataset is inspected.

## 10. Scientific interpretation

Protocols 01–03 establish the following limited empirical statement:

> A frozen one-parameter late-time deformation proportional to \(A_R\ln(1+z)\) produced a positive fitted \(A_R\) region in the original Pantheon+/DESI-based low-redshift analysis and again in an independent DES-SN5YR/Dovekie supernova analysis. The external parameter intervals overlap, but the independent DES-SN likelihood improvement is weak under information criteria, and the selected external DES Y6 BAO measurement is non-identifying for \(A_R\) when its global scale is left free as preregistered.

This does **not** establish experimental validation of Resolutive Cosmology, does not demonstrate a new physical law, and does not justify modifying the frozen deformation to increase significance.

The next scientifically useful stage should seek a second genuinely independent external observable with multiple redshift or distance-shape constraints capable of identifying \(A_R\) without importing a post-hoc early-Universe calibration.
