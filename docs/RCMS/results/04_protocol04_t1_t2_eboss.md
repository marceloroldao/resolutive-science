# RCMS Protocol 04 — P04-T1/T2 eBOSS DR16 reveal

**Status:** Executed and frozen  
**Protocol:** RCMS Protocol 04 — Independent Shape Replication  
**Dataset:** eBOSS DR16 LRG + QSO + Lyman-alpha auto  
**RSMS compatibility:** RSMS-1.0  
**Execution workflow:** `RCMS Protocol 04 eBOSS T1`  
**Workflow run:** `31856299051`  
**Head commit:** `8dc51b28a198b454b5fb4ea9e8fd7ea407333cd6`

## Gate status

P04-T0 was re-run immediately before the reveal and passed.

```text
UPSTREAM_LIKELIHOOD_CONVENTION=PASS
P04_T0_SHAPE_IDENTIFIABILITY=PASS
P04_T0_STATUS=READY_FOR_PREREGISTERED_RCMS_REVEAL
```

No P04-T1 interpretation is accepted independently of this gate.

## Frozen model

The RCMS surrogate was unchanged from Protocols 01–03:

\[
E^2(z)=\Omega_m(1+z)^3+(1-\Omega_m)+A_R\ln(1+z).
\]

The null remains exactly `A_R = 0`. The same global BAO nuisance scale `q=c/(H_0 r_d)` was profiled under both models.

## P04-T1 result

```text
LCDM_chi2_relative=5.377064289
LCDM_Omega_m=0.304383012
LCDM_q=30.016136454

RCMS_chi2_relative=1.883896070
RCMS_Omega_m=0.354751755
RCMS_q=35.124366290
RCMS_A_R=1.662222508
A_R_profile_delta_chi2_1=[0.650565914,3.103626193]

Delta_chi2_LCDM_minus_RCMS=3.493168218
Delta_AIC_LCDM_minus_RCMS=1.493168218
BIC_STATUS=NOT_APPLICABLE_NONIID_COMPRESSED_LIKELIHOOD
RCMS_boundary=False
```

The best-fit RCMS point is interior to the frozen parameter bounds.

## P04-T2 directional classification

Frozen Protocol 04 classification rule output:

```text
P04_T2_DIRECTION=POSITIVE_COMPATIBLE
```

The P04 interval is positive and overlaps the previously frozen DES-SN positive profile interval near its upper edge. It does not overlap the narrower Protocol 01/02 primary interval.

This therefore constitutes directional compatibility with at least one carried-forward positive region under the preregistered rule. It does not imply amplitude agreement with the primary low-redshift fit.

## Model-selection interpretation

The likelihood improvement is

\[
\Delta\chi^2 = 3.493168218,
\]

for one additional RCMS parameter.

The AIC difference in the convention `AIC_LCDM - AIC_RCMS` is

\[
\Delta AIC = 1.493168218,
\]

which is a modest improvement and is not, by itself, strong model-selection evidence.

BIC was not reported because the frozen statistic combines non-iid compressed likelihood components for which a naive observation count would not provide a defensible BIC penalty.

## Scientific interpretation

P04-T1/T2 provides an independent multi-redshift shape result with a positive best-fit `A_R` and a positive `Delta chi2 <= 1` profile interval. This is stronger than a purely non-identifying external comparison, but it is not a validation of Resolutive Physics and does not yet satisfy the Protocol 04 terminal criterion `INDEPENDENT_SHAPE_REPLICATION_SUPPORTED`.

The next preregistered step is P04-T3 internal shape robustness. The primary result above is frozen before those robustness results are inspected and must not be modified in response to them.

## Artifact provenance

The workflow uploaded machine-readable artifact `rcms-protocol04-t1` with artifact ID `9239128298` and SHA-256 digest:

```text
ded3dd64abf4126bca812b82807cbe880cd1ac6bb4275e8cd6f47d55518f3e0b
```

The artifact was produced directly by the successful GitHub Actions execution.
