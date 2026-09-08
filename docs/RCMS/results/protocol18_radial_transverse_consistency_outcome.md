# RCMS Protocol 18 — Radial/Transverse Consistency Outcome

**Status:** FINAL / FROZEN  
**Release line:** v0.4-dev  
**Classification:** `SURVEY_SPECIFIC_CHANNEL_TENSION`  
**Parent release:** v0.3.0 — DOI `10.5281/zenodo.22643804`

## 1. Hosted execution

GitHub Actions workflow: `RCMS Protocol 18 Channel Consistency`  
Run ID: `34257694571`  
Job ID: `102167555295`  
Artifact: `rcms-protocol18-channel-consistency`  
Artifact ID: `10068585300`  
Artifact ZIP SHA256: `9378940cdc6b85a11ce60e28f5d619a7c2b252002210a752f1434c5395a31236`

Frozen identity gate:

`P18_FINAL_IDENTITY=PASS`

All required P13/P16 closure gates passed before classification.

## 2. DESI DR2 channel fits

### Radial-only

- N = 6
- best `A_R = -0.580`
- profile `Delta chi2 <= 1`: `[-0.83, -0.24]`
- `Delta chi2 = 2.315754454`
- `Delta AIC = +0.315754454`
- boundary contact: `False`

### Transverse/volume-only

- N = 7
- best `A_R = +0.860`
- profile `Delta chi2 <= 1`: `[+0.10, +1.00]`
- `Delta chi2 = 1.303084548`
- `Delta AIC = -0.696915452`
- boundary contact: `False` for the best fit

DESI diagnostics:

- opposite best-fit signs: `True`
- profile overlap: `False`
- profile gap: `0.34`
- best-amplitude separation: `1.44`

This reproduces the P13 channel tension.

## 3. BOSS DR12 channel fits

### Radial-only

- N = 3
- best `A_R = -0.175`
- profile `Delta chi2 <= 1`: `[-1.0, +1.0]`
- `Delta chi2 = 0.000244088`
- `Delta AIC = -1.999755912`
- boundary-limited diagnostic: `True`

### Transverse-only

- N = 3
- best `A_R = -1.000`
- profile `Delta chi2 <= 1`: `[-1.0, +1.0]`
- `Delta chi2 = 0.010311263`
- `Delta AIC = -1.989688737`
- boundary-limited diagnostic: `True`

BOSS diagnostics:

- opposite best-fit signs: `False`
- profile overlap: `True`
- profile gap: `0.0`
- best-amplitude separation: `0.825`
- both channel profiles are effectively non-identifying across the frozen amplitude domain.

## 4. Preregistered classification

`CROSS_SURVEY_CHANNEL_SIGN_REVERSAL` required opposite radial/transverse best-fit signs in both DESI and BOSS.

That criterion fails because BOSS has negative best fits in both channels and extremely broad profiles.

Exactly one survey — DESI — exhibits opposite radial/transverse signs. Therefore:

`P18_CLASSIFICATION=SURVEY_SPECIFIC_CHANNEL_TENSION`

## 5. Scientific interpretation

The strong DESI radial/transverse amplitude split is real within the frozen diagnostic, but P18 does **not** support promoting it to a generic BAO-channel property.

BOSS DR12 does not replicate the sign reversal. More importantly, the three-point radial and three-point transverse BOSS subsets are too weak to identify `A_R` within the frozen `[-1,+1]` domain: both one-sigma profiles span the entire domain.

Therefore the correct conclusion is narrower than P13 alone suggested:

- DESI contains a marked channel-dependent parameter tension;
- BOSS does not provide an independent replication of that channel sign reversal;
- current evidence is consistent with survey-specific channel sensitivity rather than a universal radial/transverse RCMS effect.

This result, combined with P17 `DIFFUSE_RESIDUAL_STRUCTURE`, argues against introducing a channel-dependent correction term at this stage.

## 6. Advancement

Proceed to P19 redshift-locality diagnostics without adding a redshift-dependent parameter to the physical model. P19 should determine whether the amplitude inconsistency is better organized by redshift than by channel, using preregistered redshift partitions/change-point diagnostics with an explicit look-elsewhere boundary.
