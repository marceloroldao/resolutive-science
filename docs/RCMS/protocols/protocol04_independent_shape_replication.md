# RCMS Protocol 04 — Independent Shape Replication

**Status:** Preregistered — no Protocol 04 fit executed at freeze time  
**Model status:** Frozen one-parameter phenomenological screening surrogate  
**Parent evidence:** Protocols 01–03  
**RSMS compatibility:** RSMS-1.0

---

## 1. Purpose

Protocol 04 tests whether the positive RCMS screening direction observed in the primary low-redshift analysis and reproduced directionally in DES-SN5YR can be recovered by an **independent multi-redshift expansion-shape dataset** that was not used to define or tune the RCMS surrogate.

This protocol is designed specifically to address the main limitation of Protocol 03: the external DES Y6 angular BAO target contained only one transverse compressed datum and was therefore exactly degenerate with a free global BAO scale.

Protocol 04 must use a dataset with enough redshift structure to constrain the *shape* of the late-time expansion after all preregistered global scale nuisances are profiled or marginalized.

## 2. Frozen RCMS surrogate

The RCMS screening surrogate remains unchanged:

\[
H_{\mathrm{eff}}^2(z)
=
H_{\Lambda\mathrm{CDM}}^2(z)
+
H_0^2 A_R\ln(1+z).
\]

Equivalently,

\[
E_{\mathrm{RCMS}}^2(z)
=
\Omega_m(1+z)^3+(1-\Omega_m)+A_R\ln(1+z)
\]

for the flat late-time background used in Protocols 01–03.

The null model is exactly

\[
A_R=0.
\]

No additional RCMS coefficient, redshift exponent, transition scale, spline, piecewise term, or probe-specific RCMS parameter may be introduced in Protocol 04.

## 3. Carried-forward regions — comparison only

The primary Protocol 01/02 reference is frozen as

\[
A_R^{\rm primary}=0.187021,
\]

with profile interval

\[
0.098671\le A_R\le0.276779
\]

at \(\Delta\chi^2\le1\).

The external DES-SN5YR Protocol 03 result is frozen as

\[
A_R^{\rm DES-SN}=0.382099,
\]

with profile interval

\[
0.055322\le A_R\le0.707729.
\]

These values are **comparison targets only**. They shall not be used as priors, calibration constraints, initialization restrictions, or tuning targets for Protocol 04.

## 4. Dataset eligibility — frozen before dataset selection

A candidate Protocol 04 dataset is eligible only if all of the following are satisfied:

1. it is public or has a stable public scientific release;
2. it was not part of the Protocol 01 primary likelihood;
3. it was not used to choose the functional form \(A_R\ln(1+z)\);
4. it contains at least two genuinely shape-informative redshift measurements, or an equivalent uncompressed likelihood with multi-redshift information;
5. after all allowed global scale nuisances are profiled or marginalized, the likelihood remains non-degenerate in \(A_R\);
6. covariance information required by the release is available and retained;
7. the upstream release, files, and checksums can be frozen before the RCMS fit is inspected;
8. the observable can be predicted under both flat Lambda-CDM and the frozen RCMS surrogate without introducing a model-specific calibration advantage.

If no available dataset satisfies these conditions, Protocol 04 shall report `NO_ELIGIBLE_INDEPENDENT_SHAPE_DATASET` rather than weaken the criteria.

## 5. Independence policy

Protocol 04 distinguishes three levels:

- **dataset independence:** no observation used in Protocol 01 is reused in the primary P04 statistic;
- **analysis independence:** the upstream observable/covariance construction is preserved rather than reconstructed to favor RCMS;
- **model independence:** all nuisance parameters and calibrations are shared symmetrically between Lambda-CDM and RCMS.

Overlap in sky footprint or source populations must be documented. Material covariance with Protocol 01 data disqualifies the dataset from being called fully independent unless that covariance is explicitly modeled.

## 6. Scale and calibration policy

No post-hoc CMB, SH0ES, BBN, sound-horizon, absolute-magnitude, or other external calibration may be introduced merely to make \(A_R\) identifiable.

A global nuisance scale may be profiled or marginalized only if the same nuisance exists with the same domain and treatment under both models.

The P03-T2 failure mode is an explicit gate: if the selected dataset can fit every admissible \(A_R\) equally well after profiling one or more allowed scale nuisances, the result is classified `NOT_IDENTIFIABLE` and no model-selection claim is permitted.

## 7. P04-T0 — upstream reproduction and identifiability gate

Before inspecting the RCMS best-fit value, the implementation must:

1. reproduce an upstream/reference Lambda-CDM result or documented benchmark within a declared numerical/statistical tolerance;
2. verify units, ordering, covariance, redshift convention, and nuisance treatment;
3. demonstrate numerically that the selected data contain nonzero shape information after allowed nuisance profiling;
4. freeze the exact data revision, hashes, code revision, optimizer settings, parameter bounds, and numerical tolerances.

Failure of this gate stops the protocol before interpretation of \(A_R\).

## 8. P04-T1 — blind external shape fit

After P04-T0 passes, fit the same data under:

### Null

\[
A_R=0.
\]

### RCMS

\[
A_R\ \text{free}
\]

with the same non-RCMS nuisance policy.

Record at minimum:

- \(\chi^2_{\min}\) or the corresponding frozen likelihood statistic;
- \(\Omega_m\) where identifiable;
- \(A_R\);
- the \(\Delta\chi^2\le1\) profile interval for \(A_R\);
- \(\Delta\chi^2\equiv\chi^2_{\rm null}-\chi^2_{\rm RCMS}\);
- AIC and BIC where their assumptions are applicable;
- nuisance best fits and boundaries;
- numerical convergence diagnostics.

## 9. P04-T2 — directional consistency

Without refitting to the previous results, compare the P04 profile with the frozen primary and DES-SN regions.

Possible directional outcomes are:

- `POSITIVE_COMPATIBLE`: P04 prefers \(A_R>0\) and its profile is compatible with at least one carried-forward positive region;
- `POSITIVE_TENSION`: P04 prefers \(A_R>0\) but is materially inconsistent with both carried-forward regions;
- `NULL_COMPATIBLE`: P04 is consistent with \(A_R=0\) and provides no meaningful positive preference;
- `SIGN_REVERSAL`: P04 prefers \(A_R<0\) with a profile excluding zero at the frozen profile criterion;
- `NOT_IDENTIFIABLE`: shape information is insufficient after allowed nuisance treatment.

## 10. P04-T3 — internal shape robustness

If the dataset permits, perform preregistered leave-one-redshift-block-out or equivalent influence diagnostics. The grouping must be determined from the upstream data structure, not from residual inspection.

Record whether the sign of \(A_R\) reverses, whether the fit collapses to a boundary, and how much the model-improvement statistic changes under each removal.

No removed block may be permanently excluded from the primary result because it weakens RCMS.

## 11. Model-selection interpretation

A positive best-fit \(A_R\) alone is not evidence that RCMS is preferred.

Protocol 04 shall distinguish:

1. directional replication;
2. likelihood improvement;
3. complexity-penalized model preference;
4. statistical calibration;
5. physical interpretation.

No one item substitutes for the others.

## 12. Protocol-level classifications

Protocol 04 may end only with one of:

- `INDEPENDENT_SHAPE_REPLICATION_SUPPORTED` — an eligible independent multi-redshift dataset identifies \(A_R\), prefers the same positive direction, survives the frozen internal robustness checks, and provides nontrivial model-selection/statistical support;
- `INDEPENDENT_SHAPE_DIRECTIONAL_ONLY` — an eligible dataset independently identifies a compatible positive \(A_R\) region but model-selection/statistical support remains weak or ambiguous;
- `INDEPENDENT_SHAPE_NULL_COMPATIBLE` — the independent dataset is informative but does not reproduce the positive region;
- `INDEPENDENT_SHAPE_TENSION` — the informative independent dataset materially conflicts with the carried-forward positive region;
- `INDEPENDENT_SHAPE_NOT_IDENTIFIABLE` — the candidate data do not constrain shape after allowed nuisance treatment;
- `NO_ELIGIBLE_INDEPENDENT_SHAPE_DATASET` — no candidate meets the frozen eligibility criteria;
- `INCONCLUSIVE_PROTOCOL04` — technical or statistical limitations prevent a defensible classification above.

## 13. Anti-tuning rule

After the first eligible Protocol 04 dataset is frozen, no change to the RCMS functional form, parameter bounds, redshift dependence, nuisance asymmetry, covariance treatment, or dataset membership may be made in response to the observed \(A_R\) result.

Any scientifically motivated modification must be proposed in a later protocol/version and must preserve the Protocol 04 result unchanged in the historical record.

## 14. Publication and traceability

All Protocol 04 artifacts shall retain:

- upstream citations and revisions;
- data manifests and checksums;
- exact software commit;
- hosted workflow configuration;
- machine-readable outputs where practical;
- negative, null, degenerate, and inconclusive results;
- explicit links to the RSMS/RCMS version used.

Protocol 04 is part of the cumulative evidence record planned for the first public cosmology release. It does not, by itself, validate the full Resolutive Science framework.

## 15. Freeze statement

This document freezes Protocol 04 **before selection and inspection of the first eligible independent shape-fit result**.

The next permitted operation is dataset discovery against Section 4, followed by P04-T0 upstream reproduction and identifiability testing. No P04-T1 RCMS result may be interpreted before P04-T0 passes.