# RCMS Protocol 04 — P04-T3 execution freeze

**Status:** Frozen before P04-T3 output inspection  
**Parent result:** P04-T1/T2 eBOSS DR16 reveal  
**RSMS compatibility:** RSMS-1.0

## Purpose

P04-T3 performs the preregistered internal shape robustness diagnostic by removing each primary redshift block in turn and refitting the unchanged Lambda-CDM and RCMS models.

## Frozen primary blocks

The primary P04 statistic contains exactly three upstream blocks:

1. `LRG` at `z_eff=0.698`;
2. `QSO` at `z_eff=1.48`;
3. `LYA_AUTO` at `z_eff=2.334`.

The robustness runs are therefore exactly:

- omit `LRG`;
- omit `QSO`;
- omit `LYA_AUTO`.

No block is selected or removed based on the P04-T1 residuals.

## Model and nuisance treatment

The model remains

\[
E^2(z)=\Omega_m(1+z)^3+(1-\Omega_m)+A_R\ln(1+z),
\]

with null `A_R=0` and the same global BAO scale `q=c/(H_0 r_d)` profiled symmetrically under both models.

Frozen domains remain:

- `Omega_m in [0.10,0.50]`;
- `q in [20,45]`;
- `A_R in [-5,5]`.

## Required diagnostics

For each leave-one-block-out run, record:

- best-fit `A_R`;
- best-fit `Omega_m` and `q`;
- `Delta chi2 = chi2_LCDM - chi2_RCMS`;
- whether the RCMS optimum is boundary-limited;
- whether the sign of `A_R` reverses relative to the positive P04-T1 result.

P04-T3 does not introduce a new post-hoc binary pass/fail threshold. The diagnostics are interpreted under the already-preregistered Protocol 04 Section 10 and Section 12 rules.

## Anti-tuning rule

The primary P04-T1/T2 result is frozen and cannot be changed in response to P04-T3. A block that weakens RCMS remains part of the primary statistic. No parameter range, covariance treatment, nuisance policy, or RCMS functional form may be changed in response to the robustness output.
