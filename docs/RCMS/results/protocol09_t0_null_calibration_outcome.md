# RCMS Protocol 09 T0 — Frozen Null-Calibration Outcome

**Release line:** v0.3-dev  
**Parent release:** v0.2.0 — DOI `10.5281/zenodo.22002018`  
**Status:** FINAL / FROZEN  
**Classification:** `CALIBRATION_PASS`

## Scientific run identity

- Monte Carlo realizations: `N = 10000`
- master seed: `20260818`
- null truth: `A_R = 0`
- runner: `tools/run_rcms_protocol09_t0.py`
- GitHub Actions run: `32180054736`
- scientific CSV SHA256: `07b65beef0afac08075b9fd5217e230d7365f6f13b480f13f177b13aadb753b9`
- archived workflow artifact: `rcms-protocol09-t0`, artifact ID `9340425718`

## Frozen result

| Metric | Result | Preregistered interpretation |
|---|---:|---|
| `sigma_A` | `0.0149832353207` | diagnostic |
| mean recovered `A_R` | `8.10374758665e-05` | near zero |
| std recovered `A_R` | `0.0150314081658` | diagnostic |
| mean-bias ratio `B` | `0.00539120985689` | PASS (`<= 0.10`) |
| fraction `A_hat > 0` | `0.5052` | PASS / symmetric |
| one-sided nominal-95% FPR | `0.0502` | PASS |
| two-sided 95% null coverage | `0.9485` | PASS |
| boundary-hit rate | `0.0` | PASS |
| numerical failure rate | `0.0` | PASS |

## Interpretation

The controlled one-parameter statistical core does not show evidence of manufacturing a positive RCMS amplitude when the data-generating truth is `A_R = 0`. This is a calibration result only. It does not validate RCMS, does not increase the observational significance of the v0.2 evidence, and does not establish a physical origin for the positive real-data direction.

The preregistered smoke run with `N = 1000` classified as `CALIBRATION_FAIL`; it is not the scientific outcome and is retained in the Actions log. The preregistered scientific run was explicitly fixed at `N = 10000`, for which all final gates passed.

## Advancement

P09-T0 is now frozen. P09-T1 may proceed using the preregistered DESI DR2 correlated-covariance null calibration without changing the RCMS logarithmic equation or its T1 thresholds after outcome inspection.
