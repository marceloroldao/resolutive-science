# RCMS Protocol 05 — LRG-Dependence Challenge

**Status:** Preregistered before any Protocol 05 RCMS fit  
**Parent result:** Protocol 04 — `INDEPENDENT_SHAPE_DIRECTIONAL_ONLY`  
**Model status:** Frozen one-parameter phenomenological screening surrogate  
**RSMS compatibility:** RSMS-1.0-rc.1

---

## 1. Motivation

Protocol 04 identified a positive RCMS direction in the eBOSS DR16 multi-redshift shape likelihood, but its leave-one-block-out diagnostic showed strong dependence on the LRG block at `z_eff = 0.698`.

The primary Protocol 04 fit gave

\[
A_R = 1.662222508,
\qquad
\Delta\chi^2 = 3.493168218,
\]

while the preregistered LRG omission gave

\[
A_R = 0.053320883,
\qquad
\Delta\chi^2 = 0.000844980.
\]

Protocol 05 therefore asks a narrower question:

> Is the Protocol 04 positive direction specific to the eBOSS DR16 LRG block, or does comparable low/intermediate-redshift BAO information recover a positive RCMS direction when the original LRG block is not used?

Protocol 05 is a diagnostic/falsification protocol. It is not allowed to redefine the RCMS surrogate in response to Protocol 04.

## 2. Frozen RCMS surrogate

The model remains exactly

\[
E^2_{\mathrm{RCMS}}(z)
=
\Omega_m(1+z)^3+(1-\Omega_m)+A_R\ln(1+z),
\]

with null model

\[
A_R=0.
\]

No new coefficient, exponent, transition redshift, spline, probe-specific correction, or redshift-dependent nuisance may be introduced.

The inherited parameter domains remain

\[
0.10\le\Omega_m\le0.50,
\qquad
20\le q\le45,
\qquad
-5\le A_R\le5,
\]

where

\[
q=\frac{c}{H_0r_d}.
\]

The global BAO scale `q` must be treated identically in Lambda-CDM and RCMS.

## 3. Frozen challenge dataset

The first Protocol 05 challenge shall use the **eBOSS DR16 ELG BAO-only likelihood** that was explicitly reserved rather than included in the Protocol 04 primary statistic.

This challenge is not classified as a fully independent cosmological replication because it comes from the same broad eBOSS/SDSS program and its redshift coverage is not independent of all Protocol 04 structure. Its role is narrower: test whether replacing the influential Protocol 04 LRG block with a different tracer/observable causes the positive RCMS direction to persist or collapse.

The frozen comparison statistic is:

- Protocol 04 QSO block retained;
- Protocol 04 Lyman-alpha auto block retained;
- Protocol 04 LRG block removed;
- eBOSS DR16 ELG BAO-only likelihood inserted as the replacement low/intermediate-redshift challenge block.

The exact upstream ELG file revision, likelihood convention, redshift definition, units, and checksum must be frozen before `A_R` is evaluated.

## 4. P05-T0 — ELG acquisition and likelihood gate

Before any Protocol 05 RCMS result is exposed, P05-T0 must:

1. acquire the frozen eBOSS DR16 ELG BAO-only upstream data;
2. verify the upstream file by immutable checksum/Git blob SHA;
3. reproduce the documented ELG likelihood convention;
4. verify units and effective-redshift handling;
5. combine ELG + QSO + Lyman-alpha auto using no new external calibration;
6. fit Lambda-CDM with the common `q` nuisance;
7. verify that the resulting challenge likelihood has nonzero shape information after profiling `q`;
8. print no Protocol 05 `A_R` result.

If P05-T0 fails, Protocol 05 stops before reveal.

## 5. P05-T1 — frozen RCMS challenge fit

Only after P05-T0 passes, fit the frozen ELG + QSO + Lyman-alpha-auto statistic under:

### Null

\[
A_R=0,
\]

and

### RCMS

\[
A_R\;\text{free}.
\]

Record:

- best-fit `A_R`;
- `Delta chi2 <= 1` profile interval for `A_R`;
- best-fit `Omega_m`;
- best-fit `q`;
- `Delta chi2 = chi2_LCDM - chi2_RCMS`;
- `Delta AIC`;
- boundary/convergence diagnostics.

BIC shall be reported only if its assumptions are defensible for the compressed mixed likelihood.

## 6. P05-T2 — diagnostic classification

Protocol 05 shall classify the ELG-replacement challenge using only the following preregistered outcomes:

- `LRG_SPECIFIC_SUPPORTED`: replacing LRG with ELG makes the RCMS profile zero-compatible and removes meaningful likelihood improvement;
- `LOWZ_SHAPE_PERSISTENCE`: replacing LRG with ELG still gives `A_R > 0` with a profile excluding zero at `Delta chi2 <= 1`;
- `POSITIVE_BUT_WEAK`: the best fit remains positive but the profile includes zero or the likelihood improvement is negligible;
- `SIGN_REVERSAL`: the replacement statistic prefers `A_R < 0` with a profile excluding zero;
- `NOT_IDENTIFIABLE`: the replacement statistic cannot constrain the RCMS shape after the shared scale nuisance is profiled;
- `INCONCLUSIVE_PROTOCOL05`: technical or statistical limitations prevent a defensible classification.

These labels are diagnostic. None by itself upgrades Protocol 04 to `INDEPENDENT_SHAPE_REPLICATION_SUPPORTED`.

## 7. Anti-tuning rule

After this preregistration is merged:

- the RCMS functional form cannot be changed because of the Protocol 05 result;
- the original Protocol 04 LRG result cannot be deleted or reweighted;
- ELG cannot be dropped because it weakens RCMS;
- QSO or Lyman-alpha cannot be dropped after inspecting the result;
- no CMB, SH0ES, BBN, sound-horizon, absolute-magnitude, or other post-hoc calibration may be added to rescue identifiability or significance;
- any alternate dataset requested after seeing P05-T1 belongs to a later protocol and must preserve Protocol 05 unchanged.

## 8. Interpretation boundary

Protocol 05 tests whether the Protocol 04 LRG sensitivity is tracer/block-specific. It does not establish physical validation of Resolutive Physics, and it does not convert a phenomenological screening term into a fundamental derivation.

A positive result is evidence only that the frozen phenomenological direction persists under this specific replacement challenge. A null or adverse result is retained with equal scientific status.

## 9. Next permitted operation

The next permitted operation is **P05-T0 only**: freeze and validate the eBOSS DR16 ELG BAO-only likelihood and construct the ELG + QSO + Lyman-alpha-auto Lambda-CDM challenge statistic without evaluating `A_R`.
