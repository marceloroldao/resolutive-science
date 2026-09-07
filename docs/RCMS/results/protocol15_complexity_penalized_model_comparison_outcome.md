# RCMS Protocol 15 — Complexity-Penalized Model Comparison Outcome

**Status:** FINAL / FROZEN  
**Release line:** v0.3-dev  
**Classification:** `NO_MODEL_SELECTION_PREFERENCE`

## 1. Hosted execution

GitHub Actions workflow: `RCMS Protocol 15 Model Selection`  
Run ID: `33709020629`  
Job ID: `100504334259`  
Artifact: `rcms-protocol15-model-selection`  
Artifact ID: `9876259140`  
Artifact ZIP SHA256: `232c20db16e4a2830a213113e5881a109057b55c8143707075675ae33a4fff7b`

Identity gate: `P15_FINAL_IDENTITY=PASS`.

## 2. Frozen metrics

Across the five preregistered family-level analyses:

- families with `Delta AIC > 0`: `1`;
- families with applicable `Delta BIC > 0`: `0`;
- families with both applicable criteria favoring RCMS: `0`;
- median family-level `Delta AIC = -0.694213154`;
- median applicable family-level `Delta BIC = -4.147846500`.

The only family with positive AIC support is eBOSS DR16. Its compressed non-IID likelihood did not have a frozen BIC convention and no BIC was invented post hoc.

The overlapping P01 combined diagnostic remains mixed:

- `Delta AIC = +2.559528`;
- `Delta BIC = -2.829418`.

It is not counted as an additional independent family.

## 3. Equal-complexity control gate

P11 had already established:

- best non-log control: saturating rational;
- `chi2_best_control - chi2_log = -0.278705302`;
- log `Delta AIC < 0` versus Lambda-CDM;
- classification `FUNCTIONALLY_NON_SPECIFIC`.

Therefore the logarithmic surrogate does not satisfy the preregistered equal-complexity discrimination gate.

## 4. Frozen classification

The `LOG_MODEL_SELECTION_SUPPORTED` criteria require support in at least two family-level AIC analyses, at least two applicable BIC analyses, at least two families satisfying both, and a log-versus-control advantage of at least `Delta chi2 = 2`.

None of those model-selection requirements is met.

The stricter `REFERENCE_MODEL_SELECTION_FAVORED` category also does not apply because eBOSS DR16 has positive `Delta AIC`.

Therefore:

`P15_CLASSIFICATION=NO_MODEL_SELECTION_PREFERENCE`

## 5. Scientific interpretation

The recurring positive RCMS amplitude direction does not currently translate into robust complexity-penalized preference for the logarithmic surrogate over flat Lambda-CDM.

This is fully compatible with the earlier evidence record: several datasets prefer a positive best-fit amplitude or lower raw chi-square, but the additional parameter generally fails to earn its complexity cost, and the logarithmic functional form is not uniquely selected over equal-complexity smooth controls.

P15 therefore strengthens the boundary between a reproducible phenomenological screening pattern and a statistically selected cosmological model.

## 6. Advancement

Proceed to P16 preregistered out-of-sample prediction. P16 must freeze the target, quantitative prediction, uncertainty/acceptance criterion, code identity, and analysis plan before the target RCMS outcome is inspected.
