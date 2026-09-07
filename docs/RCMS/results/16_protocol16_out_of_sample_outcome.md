# RCMS Protocol 16 — BOSS DR12 out-of-sample outcome

**Status:** FINAL  
**Preregistered target:** SDSS-III BOSS DR12 BAO-only consensus  
**Formal classification:** `OUT_OF_SAMPLE_INVALID`

## 1. Pre-target prediction

Before any RCMS target fit, P16 froze:

- predicted best-fit interval: `0.121971100 <= A_R <= 0.407494649`;
- directional prediction: `A_R > 0`;
- primary fit domain: `-1.0 <= A_R <= +1.0`;
- no external calibration prior;
- boundary contact => `OUT_OF_SAMPLE_INVALID` with no stronger interpretation allowed.

## 2. P16-T0 gate

P16-T0 passed before target `A_R` was evaluated:

- Lambda-CDM `Omega_m = 0.364867611`;
- `q = 30.509014587`;
- `chi2 = 2.061158601`;
- covariance positive definite;
- profiled `Omega_m` chi-square span = `53.617085474`;
- `P16_T0_SHAPE_IDENTIFIABILITY=PASS`;
- `RCMS_PARAMETER_EVALUATED=NO`.

## 3. P16-T1 blind reveal

The computationally optimized executor preserved the exact frozen scientific specification and first reproduced the T0 baseline within tolerance.

Hosted reveal:

- Lambda-CDM `chi2 = 2.061158601`;
- Lambda-CDM `Omega_m = 0.364867610`;
- Lambda-CDM `q = 30.509014582`;
- RCMS `chi2 = 1.019163004`;
- RCMS `A_R = -1.000000`;
- RCMS `Omega_m = 0.463637737`;
- RCMS `q = 29.262146982`;
- frozen-grid `Delta chi2 <= 1` profile: `[-1.000000, -0.040000]`;
- `Delta chi2 = 1.041995597`;
- `Delta AIC = -0.958004403`;
- `Delta BIC = -0.749763872`;
- quantitative prediction hit: `False`;
- directional prediction hit: `False`;
- boundary contact: `True`.

Formal preregistered output:

`P16_CLASSIFICATION=OUT_OF_SAMPLE_INVALID`

## 4. Scientific interpretation

P16 does **not** provide an out-of-sample confirmation of the positive RCMS screening direction. Both the frozen quantitative prediction and the frozen positive-sign prediction fail on the held-out BOSS DR12 target.

The unconstrained optimum within the preregistered domain is driven to the negative boundary. Because boundary contact was explicitly defined before reveal as invalidating the primary classification, the authors do not widen the `A_R` range post hoc and do not assign the stronger `OUT_OF_SAMPLE_SIGN_FAILURE` label.

Nevertheless, the observed target behavior is adverse to the preregistered positive prediction and must be preserved as a substantive falsification outcome. The fact that the `Delta chi2 <= 1` region within the frozen domain remains negative up to approximately `A_R=-0.04` does not override the boundary rule.

Complexity penalties also do not favor RCMS on this target (`Delta AIC < 0`, `Delta BIC < 0`).

## 5. Computational execution note

The first T1 implementation was found, before producing a hosted result, to recompute shape integrals unnecessarily inside every evaluation of the global scale nuisance. A documented optimized executor cached the fixed `(Omega_m, A_R)` shape while preserving all data, equations, bounds, grid spacing, integration rule, likelihood, prediction interval, and classification criteria. It reproduced P16-T0 before revealing the target result.

Original execution note: `docs/RCMS/protocols/protocol16_t1_execution_note.md`.

## 6. Traceability

- P16-T0 workflow run: `34074572958`
- P16-T0 artifact ZIP SHA256: `8cf6c8e995a7d3c704ad15ceddd6c1e2dda876e6cfbec103da7e56d08fc170d2`
- P16-T1 optimized workflow run: `34075274161`
- P16-T1 artifact: `rcms-protocol16-t1-boss-dr12-optimized`
- P16-T1 artifact ZIP SHA256: `0feff37730bfbbd04f14dfc4b29e880dfd461df4fae9c00b0c9784304b92843a`

## 7. Publication consequence

P16 completes the highest-value v0.3 falsification gate with an unfavorable result. This does not invalidate the previously observed positive best-fit pattern in other datasets, but it prevents presenting that pattern as a successfully preregistered out-of-sample prediction.

No model modification, interval widening, external prior, or target substitution is introduced in response.