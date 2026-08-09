# RCMS Protocol 02 — T6 Residual Localization

**Status:** completed preregistered diagnostic  
**Model:** frozen one-parameter surrogate `A_R ln(1+z)`

## Full-combination anchor

- Lambda-CDM: `chi2 = 1422.383648`, `Omega_m = 0.304474`;
- RCMS: `chi2 = 1417.824120`, `Omega_m = 0.298908`, `A_R = 0.187021`;
- total `Delta chi2 = 4.559528`.

The additive residual decomposition reproduces the total gain with closure error `2.651e-09`.

## Per-probe localization

| Probe | Delta chi2 (LCDM - RCMS) |
|---|---:|
| H(z) | -0.113403 |
| Pantheon+ | +2.736882 |
| DESI DR2 BAO | +1.936050 |
| **Total** | **+4.559528** |

Thus H(z) slightly disfavors the RCMS best-fit deformation inside the full combination, while the likelihood gain is supplied by Pantheon+ and BAO.

## Redshift localization

Using the bins fixed before T6 execution:

| Redshift bin | H(z) | Pantheon+ | BAO | Combined Delta chi2 |
|---|---:|---:|---:|---:|
| [0.0, 0.3) | -0.007634 | +1.416037 | +0.025677 | +1.434080 |
| [0.3, 0.6) | -0.030080 | +0.654322 | +0.439506 | +1.063748 |
| [0.6, 1.0) | -0.077458 | +1.893883 | +1.110584 | **+2.927009** |
| [1.0, 1.5) | -0.020590 | -1.316321 | +0.206826 | -1.130085 |
| [1.5, inf) | +0.022359 | +0.088960 | +0.153457 | +0.264776 |

The `0.6 <= z < 1.0` bin supplies approximately `2.927009 / 4.559528 = 0.642` of the **net** full-combination likelihood improvement. This is not a new fitted subset and shall not be used to tune a later Protocol 02 model.

## Interpretation

The gain is not produced by a single probe alone: both Pantheon+ and DESI DR2 BAO improve under the same positive deformation. However, the net gain is not uniformly distributed in redshift. A substantial fraction is localized around `0.6 <= z < 1.0`, while the `1.0 <= z < 1.5` Pantheon+ contribution moves in the opposite direction.

Therefore T6 does not support an unqualified statement that the RCMS improvement is broadly distributed across all low-redshift observations. This localization must be carried into the final Protocol 02 robustness classification.
