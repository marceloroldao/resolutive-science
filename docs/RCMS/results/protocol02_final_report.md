# RCMS Protocol 02 — Consolidated Robustness Report

**Status:** completed  
**Frozen model:** `A_R ln(1+z)`  
**Reference:** flat Lambda-CDM (`A_R = 0`)  
**Protocol 01 anchor:** `A_R = 0.187021`, `Delta chi2 = 4.559528`

## Executive result

Protocol 02 was designed to challenge the positive `A_R` region obtained in Protocol 01 without modifying the deformation, parameter bounds, covariances, datasets, or selection criteria.

The result is mixed but nontrivial:

- the signal is numerically reproducible;
- it survives DESI block jackknife without sign reversal or multi-block collapse;
- it remains positive in preregistered low-/high-redshift Pantheon+ splits;
- full covariance treatment reduces the apparent strength relative to diagonal approximations, confirming covariance sensitivity but not eliminating the signal;
- a 500-realization Lambda-CDM null Monte Carlo gives `p_MC = 0.03592814` (17 exceedances), classifying the observed improvement as uncommon under the calibrated null;
- residual localization shows that the likelihood gain is not uniformly distributed: approximately 64% of the net improvement lies in the fixed `0.6 <= z < 1.0` bin.

According to the preregistered decision framework, the appropriate Protocol 02 label is:

`INCONCLUSIVE_ROBUSTNESS`

This label is intentionally more conservative than `ROBUST_SIGNAL_REGION` because the preregistered condition that no single residual region dominate the improvement is not clearly satisfied.

## T1 — numerical reproducibility

Production and independent optimizers agreed to high precision:

- `|Delta A_R| = 9.93e-06`;
- `|Delta Omega_m| = 1.64e-06`;
- `|Delta Delta-chi2| = 3e-08`.

Result: **PASS**.

## T2 — DESI DR2 block jackknife

All seven single-block omissions retained positive best-fit `A_R`. No omission generated parameter-boundary contact or the preregistered multi-collapse warning.

The strongest reduction occurred when omitting the `z=0.706` block:

- `A_R = 0.154896`;
- `Delta chi2 = 3.002978`.

Result: no single DESI block explains the complete signal.

## T3 — Pantheon+ redshift split

Using the fixed split `z_CMB=0.3`:

- low-z SN + BAO: `A_R = 0.248686`;
- high-z SN + BAO: `A_R = 0.383249`;
- H(z)+low-z SN+BAO: `A_R = 0.244611`;
- H(z)+high-z SN+BAO: `A_R = 0.373225`.

No sign reversal occurred.

## T4 — covariance ablation

Production full-covariance anchor:

- `A_R = 0.187021`;
- `Delta chi2 = 4.559528`.

Diagnostic diagonal approximations produced:

- SN diagonal only: `A_R = 0.253942`, `Delta chi2 = 12.748141`;
- BAO diagonal only: `A_R = 0.189771`, `Delta chi2 = 4.221895`;
- SN+BAO diagonal: `A_R = 0.256131`, `Delta chi2 = 11.492614`.

Interpretation: Pantheon+ covariance correlations materially suppress the apparent signal strength. The production analysis must therefore retain the full covariance.

## T5 — Lambda-CDM null Monte Carlo

Frozen test:

- simulations: `500`;
- seed: `20260809`;
- observed threshold: `Delta chi2 = 4.559528`.

Result:

- exceedances: `17 / 500`;
- `p_MC = 0.03592814`;
- null median `Delta chi2 = 0.403105`;
- null 95th percentile `= 3.905768`;
- null 99th percentile `= 6.647125`.

The observed improvement is therefore uncommon, but not discovery-level, under the calibrated Lambda-CDM null pipeline.

## T6 — residual localization

Per-probe net likelihood gain:

| Probe | Delta chi2 |
|---|---:|
| H(z) | -0.113403 |
| Pantheon+ | +2.736882 |
| DESI DR2 BAO | +1.936050 |
| **Total** | **+4.559528** |

Fixed redshift-bin net contributions:

| Redshift bin | Combined Delta chi2 |
|---|---:|
| [0.0, 0.3) | +1.434080 |
| [0.3, 0.6) | +1.063748 |
| [0.6, 1.0) | **+2.927009** |
| [1.0, 1.5) | -1.130085 |
| [1.5, inf) | +0.264776 |

The `0.6 <= z < 1.0` interval contributes approximately `64.2%` of the **net** full-combination improvement. This localization prevents an unqualified claim that the likelihood gain is broadly distributed across all redshifts.

## Final Protocol 02 classification

The preregistered labels were `ROBUST_SIGNAL_REGION`, `FRAGILE_SIGNAL_REGION`, `NULL_COMPATIBLE`, and `INCONCLUSIVE_ROBUSTNESS`.

The data do not support `NULL_COMPATIBLE`: the positive region survives T1-T4 and the Monte Carlo tail probability is approximately 3.6%.

The data also do not cleanly support `FRAGILE_SIGNAL_REGION`: the signal does not depend on one numerical path, one DESI block, or one SN redshift half, and its sign remains stable.

However, `ROBUST_SIGNAL_REGION` requires that no single residual block dominate the improvement. T6 shows substantial concentration in `0.6 <= z < 1.0`. Consequently the conservative preregistered classification is:

**INCONCLUSIVE_ROBUSTNESS**.

## Scientific meaning

This classification applies only to the frozen one-parameter RCMS screening surrogate. It does not validate Resolutive Cosmology or establish a new physical law.

The result justifies a later, separately preregistered external-replication protocol. Any future model revision, new redshift dependence, CMB inclusion, SH0ES inclusion, RSD inclusion, or external `r_d` prior must be introduced only in a new protocol and shall not retroactively alter Protocol 02.