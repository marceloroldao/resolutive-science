# RCMS Protocol 05 — P05-T1 execution freeze

**Status:** Frozen after successful P05-T0 and before P05-T1 reveal  
**Parent protocol:** `protocol05_lrg_dependence_challenge.md`

## Frozen statistic

P05-T1 uses exactly the challenge statistic validated in P05-T0:

- eBOSS DR16 ELG BAO-only at `z=0.845`, `DV_over_rs`;
- eBOSS DR16 QSO at `z=1.48`, `DM_over_rs` + `DH_over_rs`;
- eBOSS DR16 Lyman-alpha auto at `z=2.334`;
- Protocol 04 LRG excluded by preregistration.

## Frozen model and bounds

The RCMS surrogate remains

\[
E^2(z)=\Omega_m(1+z)^3+(1-\Omega_m)+A_R\ln(1+z).
\]

Parameter domains are unchanged:

- `Omega_m in [0.10, 0.50]`;
- `q = c/(H0 r_d) in [20, 45]`;
- `A_R in [-5, 5]`.

The null model is `A_R=0` and uses the same `Omega_m` and `q` treatment.

## Frozen numerical procedure

- deterministic multi-start minimization;
- all three parameters re-fit for RCMS;
- `Omega_m` and `q` re-fit at every fixed `A_R` for the profile;
- `Delta chi2 <= 1` profile interval for `A_R`;
- `Delta chi2 = chi2_LCDM - chi2_RCMS`;
- `Delta AIC = Delta chi2 - 2` for the single added RCMS parameter;
- BIC only if assumptions are defensible for this compressed mixed likelihood;
- boundary status recorded explicitly.

## Frozen diagnostic classification

Classification must use Section 6 of the Protocol 05 preregistration without modification:

- `LRG_SPECIFIC_SUPPORTED`;
- `LOWZ_SHAPE_PERSISTENCE`;
- `POSITIVE_BUT_WEAK`;
- `SIGN_REVERSAL`;
- `NOT_IDENTIFIABLE`;
- `INCONCLUSIVE_PROTOCOL05`.

No response-dependent model, data, calibration, parameter-bound, or nuisance change is permitted after this freeze.
