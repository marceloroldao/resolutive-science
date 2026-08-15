# RCMS Protocol 05 — ELG-Replacement Challenge Outcome

**Final diagnostic classification:** `POSITIVE_BUT_WEAK`  
**Protocol:** RCMS Protocol 05 — LRG-Dependence Challenge  
**RSMS compatibility:** RSMS-1.0

## 1. Question tested

Protocol 05 tested whether the positive direction observed in Protocol 04 depended specifically on the eBOSS DR16 LRG block.

The challenge statistic was frozen before the RCMS reveal:

- remove the Protocol 04 LRG block at `z_eff = 0.698`;
- insert the eBOSS DR16 ELG BAO-only likelihood at `z_eff = 0.845` using `DV_over_rs`;
- retain the eBOSS DR16 QSO block at `z_eff = 1.48`;
- retain the eBOSS DR16 Lyman-alpha auto block at `z_eff = 2.334`;
- retain the same global BAO scale nuisance and the same RCMS surrogate used in the preceding protocols.

No model or data selection was changed after the result was exposed.

## 2. P05-T0 gate

P05-T0 passed before any `A_R` value was evaluated.

The frozen ELG file from `CobayaSampler/bao_data@v2.6` was verified by Git blob SHA:

`25e8c0f773174ed3d05dcfad0929f268d90c2019`

The upstream one-dimensional log-probability convention passed.

The Lambda-CDM challenge baseline was:

- `Omega_m = 0.281891846`;
- `q = 29.352110485`;
- relative `chi2 = 1.661263571`;
- profiled `Omega_m` span `Delta chi2 = 42.339250007`.

Therefore the challenge statistic retained nonzero shape information after profiling the shared BAO scale nuisance.

P05-T0 classification:

`READY_FOR_PREREGISTERED_RCMS_CHALLENGE`

## 3. P05-T1 reveal

The frozen RCMS surrogate remained

\[
E^2_{\mathrm{RCMS}}(z)
=
\Omega_m(1+z)^3+(1-\Omega_m)+A_R\ln(1+z).
\]

The null model gave:

- `chi2_relative = 1.661263571`;
- `Omega_m = 0.281891841`;
- `q = 29.352110328`.

The RCMS fit gave:

- `chi2_relative = 1.635706372`;
- `Omega_m = 0.294382162`;
- `q = 30.449846217`;
- `A_R = 0.293880907`;
- `A_R` profile at `Delta chi2 <= 1`: `[-1.043863342, 3.656939376]`;
- `Delta chi2 = 0.025557199`;
- `Delta AIC = -1.974442801`;
- no parameter-boundary failure.

BIC was not applied because the assumptions required for a conventional iid-observation interpretation are not appropriate for this mixed compressed likelihood.

## 4. Frozen classification

Under the preregistered Protocol 05 decision rules, the result is:

`POSITIVE_BUT_WEAK`

The best-fit direction remains positive after replacing the LRG block with ELG, but the profile is broadly zero-compatible and the likelihood gain is negligible.

The negative `Delta AIC` means that, under this challenge statistic, the complexity penalty favors the simpler Lambda-CDM model over the one-parameter RCMS extension.

## 5. Relation to Protocol 04

Protocol 04 produced a primary eBOSS result of

- `A_R = 1.662222508`;
- `Delta chi2 = 3.493168218`;
- profile `[0.650565914, 3.103626193]`;
- directional classification `POSITIVE_COMPATIBLE`.

Its leave-one-block-out diagnostic showed that omitting LRG reduced the result to

- `A_R = 0.053320883`;
- `Delta chi2 = 0.000844980`.

Protocol 05 shows that replacing LRG with ELG moves the best fit back to a positive value (`A_R = 0.293880907`), but does not restore a statistically informative positive profile or meaningful likelihood improvement.

Therefore the evidence does not support the statement that a positive RCMS shape signal robustly persists across these two low/intermediate-redshift tracers.

At the same time, the challenge does not produce a sign reversal. The most accurate interpretation is that the positive direction is weakly retained but is not robustly identified without the original LRG block.

## 6. Scientific conclusion

Protocol 05 strengthens the limitation identified in Protocol 04.

The current evidence hierarchy is:

1. the original low-redshift analysis identified a positive phenomenological direction;
2. DES-SN reproduced a compatible positive direction with weak model-selection support;
3. Protocol 04 eBOSS multi-redshift shape data produced a positive compatible result, but with strong LRG influence;
4. Protocol 05 ELG replacement retained only a weak positive best fit, with a zero-compatible profile and no model-selection advantage.

This does not validate Resolutive Physics, does not establish discovery of new physics, and does not justify modifying the RCMS model to increase significance.

The appropriate next scientific step is an independently preregistered test using data that are not simply another internal rearrangement of the same eBOSS blocks.

## 7. Preservation rule

This result is frozen as a negative/limiting robustness result of the current RCMS screening surrogate. Future protocols must preserve it unchanged and may not remove or reinterpret the ELG challenge solely because it weakens the positive Protocol 04 result.
