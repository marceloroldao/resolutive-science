# RCMS Protocol 04 — P04-T1 eBOSS DR16 result

**Status:** Frozen observational screening result  
**Protocol:** RCMS Protocol 04 — Independent Shape Replication  
**Execution:** GitHub Actions run `32097939634`  
**Dataset:** eBOSS DR16 LRG + QSO + Lyman-alpha auto  
**Model form:** `A_R ln(1+z)` frozen before reveal

## Result

Lambda-CDM null:

- `Omega_m = 0.304383012`
- `q = c/(H0 r_d) = 30.016136454`
- `chi2_relative = 5.377064289`

RCMS:

- `Omega_m = 0.354751755`
- `q = c/(H0 r_d) = 35.124366290`
- `A_R = 1.662222508`
- `chi2_relative = 1.883896070`

Profile interval at `Delta chi2 = 1`:

- `A_R in [0.650565914, 3.103626193]`

Model-comparison diagnostics:

- `Delta chi2 (LCDM - RCMS) = 3.493168218`
- `Delta AIC (LCDM - RCMS) = 1.493168218`
- BIC not reported because the frozen likelihood is hybrid/non-i.i.d. and no defensible independent-observation count was preregistered.

Directional classification:

- `POSITIVE_COMPATIBLE`
- optimizer solution is not boundary-limited.

## Interpretation boundary

This is an independent-shape screening result. The best-fit direction is positive and the profile excludes zero at the internal `Delta chi2 = 1` level. However, the preferred amplitude is substantially larger than the earlier low-redshift RCMS fits, and `Delta AIC = 1.49` is only modest evidence. This result does not validate Resolutive Physics and requires probe-level robustness analysis before stronger interpretation.

## Next falsification step

Protocol 04 should next perform preregistered probe ablations while preserving the same model, nuisance treatment, parameter bounds, and frozen upstream data. The purpose is to determine whether the positive preference is distributed across LRG, QSO, and Lyman-alpha or is driven primarily by one block.
