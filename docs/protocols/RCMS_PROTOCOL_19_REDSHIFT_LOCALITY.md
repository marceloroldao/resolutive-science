# RCMS Protocol 19 — Redshift Locality / Change-Point Diagnostic

Status: **PREREGISTERED**
Branch: `v0.4-dev`

## Motivation
P16 falsified the held-out RCMS prediction. P17 found only diffuse residual structure after survey-specific fitting. P18 audits radial/transverse consistency. P19 asks the next diagnostic question without introducing new physics: **is the remaining RCMS amplitude discrepancy localized in redshift rather than global?**

## Scientific rule
Diagnosis precedes extension. No new physical parameter, coupling, scale, or functional form may be introduced in P19.

## Data scope
Use the same frozen BAO inputs and covariance conventions already validated for the DESI DR2 and BOSS DR12 RCMS analyses in this repository. Do not add or remove points after inspecting P19 outcomes.

## Observable orientation
Put transverse and radial observables in the same physical sign orientation before comparing residual/amplitude trends. In particular, a BOSS radial observable expressed as `H r_d` must be sign-oriented consistently with the equivalent `D_H/r_d` interpretation used by the diagnostic layer.

## Primary diagnostic
For each survey and channel:
1. retain the frozen baseline/model conventions;
2. order measurements by effective redshift;
3. compute the signed standardized residual sequence;
4. evaluate every admissible internal split with at least one datum on each side;
5. for each split compute the inverse-variance weighted mean residual below and above the split and their difference;
6. report the split with maximum absolute standardized contrast.

The diagnostic is descriptive, not a new fitted cosmological model. The selected split is therefore a localization statistic and **must not** be promoted to a physical transition scale.

## Cross-survey criterion
A localized-redshift interpretation is supported only if DESI and BOSS independently indicate compatible contrast direction and overlapping/adjacent redshift localization. A strong split in only one survey is classified as survey-localized heterogeneity, not RCMS evidence.

## Outcome classes
- `NO_REDSHIFT_LOCALIZATION`: no material standardized contrast.
- `SURVEY_LOCALIZED_HETEROGENEITY`: material localization occurs in only one survey or at incompatible redshifts/signs.
- `CROSS_SURVEY_LOCALIZATION`: independently compatible localization appears in DESI and BOSS.
- `INSUFFICIENT_CHANNEL_SUPPORT`: sampling is too sparse for the preregistered comparison.

## Guardrails
- No threshold may be tuned after seeing the result.
- No inferred change point is a physical parameter in v0.4-dev.
- P19 cannot rescue P16 by itself.
- Any candidate extension remains forbidden until P20 is completed.

## Next step
P20 tests cross-survey concordance at comparable redshift. Only after P17–P20 diagnosis may P21 generate minimal-extension candidates, and those candidates remain exploratory until calibration, complexity-aware comparison, and a genuinely new held-out prediction (P22–P24).