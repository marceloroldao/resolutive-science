# RCMS Protocol 04 — P04-T3 probe-ablation freeze

**Status:** Frozen before probe-ablation outputs are inspected  
**Parent:** `protocol04_independent_shape_replication.md`  
**Parent result:** P04-T1 / P04-T2 eBOSS DR16 independent-shape reveal  
**RSMS compatibility:** RSMS-1.0

## Purpose

Determine whether the P04-T1 preference for positive `A_R` is distributed across the eBOSS DR16 redshift lever arm or is driven primarily by one probe.

## Frozen model and parameters

No model change is permitted.

Lambda-CDM:

`E(z)^2 = Omega_m (1+z)^3 + 1 - Omega_m`

RCMS:

`E(z)^2 = Omega_m (1+z)^3 + 1 - Omega_m + A_R ln(1+z)`

Parameter domains remain exactly:

- `Omega_m in [0.10, 0.50]`
- `q = c/(H0 r_d) in [20.0, 45.0]`
- `A_R in [-5.0, 5.0]`

No CMB, SH0ES, DESI, Pantheon+, DES-SN, BBN, or sound-horizon calibration is added.

## Frozen ablations

The primary P04-T1 statistic is `LRG + QSO + LYA-auto`. The following leave-one-probe-out fits are executed independently:

1. `QSO + LYA-auto` — remove LRG;
2. `LRG + LYA-auto` — remove QSO;
3. `LRG + QSO` — remove LYA-auto.

The full `LRG + QSO + LYA-auto` result is re-evaluated in the same runner as a closure reference.

The Lyman-alpha x QSO grid and ELG block remain excluded. No replacement data are introduced.

## Frozen outputs

For each configuration the runner reports:

- best-fit Lambda-CDM `chi2`, `Omega_m`, and `q`;
- best-fit RCMS `chi2`, `Omega_m`, `q`, and `A_R`;
- `Delta chi2 = chi2_LCDM - chi2_RCMS`;
- `Delta AIC = Delta chi2 - 2`;
- profile-likelihood `Delta chi2=1` interval for `A_R`, when a finite two-sided interval exists;
- boundary/identifiability state.

## Interpretation rule

This test is diagnostic rather than a new discovery test.

- If removing one probe causes the positive best-fit `A_R` to collapse toward zero, reverse sign, become boundary-limited, or lose most of `Delta chi2`, that probe is flagged as influential.
- If all three leave-one-out fits retain positive finite `A_R` with broadly compatible profiles, the preference is classified as distributed across the redshift lever arm.
- A subset with insufficient information to establish a finite two-sided profile is reported as `NOT_IDENTIFIABLE`; it is not converted into evidence for or against RCMS.

No response-dependent change to data membership, model form, priors, parameter domains, likelihood conventions, or nuisance treatment is permitted after this freeze.
