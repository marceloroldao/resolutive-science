# RCMS Protocol 13 — Systematics and Nuisance Sensitivity Outcome

**Status:** FINAL / FROZEN  
**Release line:** v0.3-dev  
**Classification:** `SYSTEMATICS_SENSITIVE`  
**Frozen surrogate:** `H_eff^2 = H_LCDM^2 + H0^2 A_R ln(1+z)`

## 1. Hosted execution

GitHub Actions workflow: `RCMS Protocol 13 Systematics Sensitivity`  
Run ID: `33708618120`  
Job ID: `100503127303`  
Artifact: `rcms-protocol13-systematics`  
Artifact ID: `9876140949`  
Artifact ZIP SHA256: `21e7623d92f8082241d5ec6d16b62eabbfd86570c3d0320b943cf7d91f52f1bf`

The frozen execution identity check passed:

`P13_FINAL_IDENTITY=PASS`

## 2. Complete sensitivity map

| Branch | N | Best A_R | Delta-chi2 <= 1 interval | Delta chi2 | Delta AIC | Zero in interval |
|---|---:|---:|---:|---:|---:|---|
| B0 full covariance | 13 | 0.210 | [0.030, 0.400] | 1.3058 | -0.6942 | No |
| B1 diagonal-only covariance | 13 | 0.240 | [0.050, 0.440] | 1.5428 | -0.4572 | No |
| B2 half off-diagonal correlations | 13 | 0.230 | [0.040, 0.430] | 1.3793 | -0.6207 | No |
| B3 drop minimum-redshift observables | 12 | 0.220 | [0.000, 0.450] | 0.9414 | -1.0586 | Yes |
| B4 drop maximum-redshift observables | 11 | 0.730 | [0.340, 1.000] | 3.7719 | +1.7719 | No |
| B5 radial-only (`DH_over_rs`) | 6 | -0.580 | [-0.830, -0.240] | 2.3158 | +0.3158 | No |
| B6 transverse/volume-only (`DM_over_rs`, `DV_over_rs`) | 7 | 0.860 | [0.100, 1.000] | 1.3031 | -0.6969 | No |

No branch failed numerically or through covariance invalidity, and none reported a parameter-boundary contact under the runner's frozen boundary rule.

## 3. Preregistered classification

The preregistered `SYSTEMATICS_STABLE_POSITIVE` classification required at least five of the six non-baseline branches to retain `A_R > 0` and no branch with at least five observations to have `A_R < -0.05`.

That criterion fails because B5, the radial-only subset, returns

`A_R = -0.580`,

with its complete `Delta chi2 <= 1` interval negative.

The majority-sign-reversal criterion is not met because only one of the six non-baseline branches is negative.

Therefore the frozen classification is:

`P13_CLASSIFICATION=SYSTEMATICS_SENSITIVE`

## 4. Scientific interpretation

P13 does not support the claim that the DESI DR2 positive RCMS direction is insensitive to analysis structure.

The positive baseline is robust to two covariance-correlation diagnostics (diagonal-only and half-correlation) and remains positive after removing the minimum- or maximum-redshift edge. However, decomposing the same DESI DR2 vector by observable type reveals strong tension:

- radial BAO information alone prefers a negative effective amplitude;
- transverse/volume BAO information alone prefers a much larger positive effective amplitude.

Thus the full-vector best fit near `A_R ~ 0.21` is partly a compromise between internally different directional tendencies. This is a genuine falsification-relevant limitation and must not be hidden by quoting only the full-covariance branch.

The positive direction seen in P12 across broader dataset families and the P13 internal DESI sensitivity are not contradictory: P12 asks whether the descriptive cross-dataset positive pattern is dominated by one dataset family, while P13 asks whether one specific high-value dataset is internally stable under preregistered decompositions.

## 5. Model-selection boundary

Only B4 and B5 have positive `Delta AIC`, and neither constitutes an independent model-selection claim. The official full-covariance baseline remains `Delta AIC < 0`.

P13 therefore does not establish RCMS preference over Lambda-CDM.

## 6. Advancement

Proceed to P14 amplitude stability without retuning the logarithmic surrogate. P14 must explicitly test compatibility of effective amplitudes across redshift ranges and observational channels, with the P13 radial/transverse tension treated as evidence to be tested rather than repaired.
