# RCMS Protocol 04 — Final outcome

**Protocol:** Independent Shape Replication  
**RSMS compatibility:** RSMS-1.0  
**Final classification:** `INDEPENDENT_SHAPE_DIRECTIONAL_ONLY`

## Summary

Protocol 04 tested the frozen one-parameter RCMS screening surrogate

\[
E_{\mathrm{RCMS}}^2(z)=\Omega_m(1+z)^3+(1-\Omega_m)+A_R\ln(1+z)
\]

against an independent multi-redshift eBOSS DR16 BAO shape dataset using LRG, QSO, and Lyman-alpha auto-correlation blocks. The global BAO scale nuisance

\[
q=\frac{c}{H_0r_d}
\]

was profiled symmetrically under Lambda-CDM and RCMS.

No CMB, SH0ES, DESI, Pantheon+, DES-SN, BBN, sound-horizon, or other external calibration was introduced.

## P04-T0 — baseline and identifiability gate

P04-T0 passed before any RCMS parameter was exposed.

The frozen upstream data files matched their preregistered Git blob SHAs. The Gaussian LRG/QSO likelihood convention and the logarithmic Lyman-alpha grid likelihood convention were reproduced. The flat Lambda-CDM baseline yielded an interior optimum:

- `Omega_m = 0.304383014`
- `q = 30.016136523`
- relative `chi2 = 5.377064289`

The profiled likelihood retained non-zero shape information after `q` profiling.

P04-T0 status:

`P04_T0_STATUS=READY_FOR_PREREGISTERED_RCMS_REVEAL`

## P04-T1 — blind RCMS reveal

The preregistered blind reveal returned:

- Lambda-CDM relative `chi2 = 5.377064289`
- RCMS relative `chi2 = 1.883896070`
- RCMS `Omega_m = 0.354751755`
- RCMS `q = 35.124366290`
- RCMS `A_R = 1.662222508`
- `Delta chi2 = 3.493168218`
- `Delta AIC = 1.493168218`
- BIC not applied because the compressed likelihood is non-IID
- no fitted RCMS parameter was boundary-limited

The frozen `Delta chi2 <= 1` profile interval was

\[
0.650565914\le A_R\le3.103626193.
\]

Zero is outside this profile interval.

## P04-T2 — directional consistency

The result was classified by the preregistered rule as

`POSITIVE_COMPATIBLE`.

The P04 profile does not overlap the narrow Protocol 01/02 primary interval but overlaps the carried-forward DES-SN5YR positive interval near its upper edge. The amplitude is substantially larger than the earlier best-fit values, so this is not interpreted as numerical agreement of amplitudes.

## P04-T3 — leave-one-redshift-block-out robustness

The upstream data structure defined three primary blocks. Each was removed exactly once, without changing the model or nuisance treatment.

| Omitted block | A_R | Omega_m | q | Delta chi2 | Boundary | Sign reversal |
|---|---:|---:|---:|---:|---|---|
| LRG, z=0.698 | 0.053320883 | 0.294527685 | 29.994957911 | 0.000844980 | No | No |
| QSO, z=1.48 | 1.977806376 | 0.370607577 | 35.989196478 | 4.155344814 | No | No |
| Lyman-alpha auto, z=2.334 | 2.903677442 | 0.301405115 | 37.288927425 | 3.326587592 | No | No |

No leave-one-block-out fit reversed the sign of `A_R`, and none was boundary-limited. However, removing the LRG block collapses the fitted amplitude close to zero and removes essentially all likelihood improvement. Therefore the primary positive result is strongly influenced by the LRG block and does not satisfy the robustness requirement for `INDEPENDENT_SHAPE_REPLICATION_SUPPORTED`.

## Model-selection interpretation

The blind primary fit favors the RCMS surrogate directionally and improves the likelihood by `Delta chi2 = 3.493168218`, but the complexity-penalized improvement is modest (`Delta AIC = 1.493168218`). Together with the strong LRG influence found in P04-T3, the evidence is insufficient for the protocol-level `SUPPORTED` category.

Accordingly, the preregistered protocol-level classification is:

`INDEPENDENT_SHAPE_DIRECTIONAL_ONLY`

This means that an eligible independent multi-redshift dataset identified a compatible positive RCMS direction, while model-selection support and internal robustness remain too weak or ambiguous for a stronger claim.

## Scientific interpretation

Protocol 04 does not validate Resolutive Physics, does not establish new physics, and does not replace Lambda-CDM. It records an independent positive screening direction that remains scientifically interesting but is not yet robust enough to support a discovery-level or framework-validation claim.

The LRG sensitivity must be preserved as part of the evidence record rather than removed or tuned away. Any modification to the RCMS functional form, parameter bounds, covariance treatment, or dataset membership in response to this result belongs to a later protocol/version.

## Traceability

- P04-T0 public rerun: PR #63
- P04-T1/T2 reveal: PR #64
- P04-T3 robustness: PR #65
- P04-T1 workflow run: `31856299051`
- P04-T1 artifact SHA256: `ded3dd64abf4126bca812b82807cbe880cd1ac6bb4275e8cd6f47d55518f3e0b`
- P04-T3 workflow run: `31856440726`
- P04-T3 artifact SHA256: `c1ebfd71fb19729fb4038147076fd9b116b1937dca005ee8d8c6c6b4b2c38691`

The published v0.1.0/v0.1.1 scientific snapshot remains unchanged; Protocol 04 is post-v0.1.1 cumulative evidence.
