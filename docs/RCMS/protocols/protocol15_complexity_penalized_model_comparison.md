# RCMS Protocol 15 — Complexity-Penalized Model Comparison

**Status:** PREREGISTERED / FROZEN BEFORE EXECUTION  
**Release line:** v0.3-dev

## 1. Purpose

Protocol 15 asks whether the frozen logarithmic RCMS screening surrogate retains any defensible model-selection advantage after accounting for its additional parameter and after comparison with equal-complexity one-parameter controls.

P15 does not refit observational likelihoods. It uses only frozen results already produced before this protocol.

## 2. Frozen family-level inputs

Using the convention `Delta X = X_LCDM - X_RCMS`:

| Family | Delta chi2 | Delta AIC | Delta BIC | Source |
|---|---:|---:|---:|---|
| Moresco H(z) | 0.5526 | -1.4474 | -2.1555 | P01 |
| Pantheon+ | 0.4438 | -1.5562 | -6.9277 | P01 |
| DES-SN5YR | 1.366399 | -0.633601 | -6.140193 | P03 |
| eBOSS DR16 | 3.493168218 | +1.493168218 | not applied (non-IID compressed likelihood) | P04 |
| DESI DR2 | 1.305786846 | -0.694213154 | -1.259164141 (same 13-observable likelihood in P11) | P06/P11 |

The P01 full H(z)+Pantheon++DESI combination is retained only as an overlapping combined diagnostic:

- `Delta chi2 = 4.559528`;
- `Delta AIC = +2.559528`;
- `Delta BIC = -2.829418`.

It shall not be counted as an additional independent family.

## 3. Frozen equal-complexity controls

P11 compared the log term to linear, saturating-rational, and square-root controls, each with exactly one added amplitude and identical DESI DR2 nuisance structure.

Frozen P11 facts:

- best non-log control: `saturating`;
- `chi2_saturating = 8.686550489`;
- `chi2_log = 8.965255791`;
- `chi2_best_control - chi2_log = -0.278705302`;
- all deformation models have `Delta AIC <= 0` versus Lambda-CDM;
- P11 classification: `FUNCTIONALLY_NON_SPECIFIC`.

## 4. Metrics

P15 shall report:

1. number of family-level analyses with `Delta AIC > 0`;
2. number of family-level analyses with applicable `Delta BIC > 0`;
3. number with both applicable AIC and BIC favoring RCMS;
4. median family-level `Delta AIC`;
5. median applicable family-level `Delta BIC`;
6. P01 overlapping combined AIC/BIC disagreement;
7. the frozen P11 log-versus-control gap;
8. whether the log is the best equal-complexity deformation on DESI DR2.

No pseudo-combined AIC/BIC shall be formed by summing statistically overlapping family analyses.

## 5. Preregistered classification

### `LOG_MODEL_SELECTION_SUPPORTED`

Requires all conditions:

1. at least two distinct family-level analyses have `Delta AIC > 0`;
2. at least two distinct family-level analyses with applicable BIC have `Delta BIC > 0`;
3. at least two distinct families have both applicable criteria favoring RCMS;
4. P11 log beats the best non-log equal-complexity control by at least `Delta chi2 = 2`;
5. P11 log itself has `Delta AIC > 0` versus Lambda-CDM.

### `REFERENCE_MODEL_SELECTION_FAVORED`

Assigned if no family has `Delta AIC > 0`, no applicable family has `Delta BIC > 0`, and P11 does not favor the log.

### `NO_MODEL_SELECTION_PREFERENCE`

Assigned in all mixed/weak cases between the two categories above.

## 6. Boundaries

- Positive best-fit `A_R` is irrelevant to the P15 classification unless accompanied by complexity-penalized preference.
- BIC is not fabricated for likelihoods where the effective sample-count convention was not frozen.
- P15 does not combine overlapping analyses as independent evidence.
- No Bayesian evidence calculation is introduced post hoc; the release lacks a preregistered prior-volume specification suitable for that calculation.

## 7. Advancement

After P15 is frozen, proceed to P16 preregistered out-of-sample prediction. P16 remains the highest-value final gate of v0.3.
