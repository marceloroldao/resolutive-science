# RCMS Protocol 04 — P04-T4 LRG component-ablation freeze

**Status:** Frozen before component-ablation outputs are inspected  
**Parent:** `protocol04_independent_shape_replication.md`  
**Parent result:** P04-T3 eBOSS probe ablation  
**RSMS compatibility:** RSMS-1.0

## Purpose

Localize the LRG contribution identified by P04-T3 by separating its transverse and radial observables while leaving QSO + LYA-auto unchanged.

## Frozen model and domains

No model change is permitted.

Lambda-CDM:

`E(z)^2 = Omega_m (1+z)^3 + 1 - Omega_m`

RCMS:

`E(z)^2 = Omega_m (1+z)^3 + 1 - Omega_m + A_R ln(1+z)`

Domains remain:

- `Omega_m in [0.10, 0.50]`
- `q = c/(H0 r_d) in [20.0, 45.0]`
- `A_R in [-5.0, 5.0]`

No CMB, SH0ES, DESI, Pantheon+, DES-SN, BBN, or sound-horizon calibration is added.

## Frozen configurations

1. `FULL_LRG + QSO + LYA` — closure reference using the full 2D LRG covariance.
2. `LRG_DM_ONLY + QSO + LYA` — retain only the LRG transverse observable `DM_over_rs`.
3. `LRG_DH_ONLY + QSO + LYA` — retain only the LRG radial observable `DH_over_rs`.
4. `NO_LRG + QSO + LYA` — closure reference from P04-T3.

For the one-component LRG cases, the retained observable uses its published marginal variance `C_ii` from the same frozen LRG covariance matrix. The discarded component and its cross-covariance are removed together. No diagonal approximation is made to any two-dimensional likelihood.

## Frozen outputs

For every configuration report best-fit Lambda-CDM and RCMS parameters, `Delta chi2`, `Delta AIC`, the `Delta chi2=1` profile interval of `A_R` when finite, and boundary/identifiability state.

## Interpretation

- If `DM_ONLY` retains most of the full preference while `DH_ONLY` collapses toward the no-LRG result, the anomaly is classified as predominantly transverse.
- If `DH_ONLY` retains most of the full preference while `DM_ONLY` collapses, it is predominantly radial.
- If both one-component fits retain material positive preference, the LRG contribution is distributed across both components.
- If neither does, the full 2D LRG covariance/combination is essential and no single-component localization is claimed.

No result-dependent modification of model, bounds, covariance, nuisance treatment, or dataset membership is permitted after this freeze.
