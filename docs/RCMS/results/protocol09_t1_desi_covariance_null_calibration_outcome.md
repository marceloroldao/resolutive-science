# RCMS Protocol 09 T1 — Frozen DESI-Covariance Null-Calibration Outcome

**Release line:** v0.3-dev  
**Parent release:** v0.2.0 — DOI `10.5281/zenodo.22002018`  
**Status:** FINAL / FROZEN  
**Classification:** `CALIBRATION_PASS`

## Scientific run identity

- Monte Carlo realizations: `N = 5000`
- master seed: `20260820`
- null truth: `A_R = 0`
- frozen correlated structure: DESI DR2 13-observable BAO covariance
- fitted null reference: `Omega_m = 0.295000`, `q = 29.468025096`
- runner: `tools/run_rcms_protocol09_t1.py`
- GitHub Actions run: `32587458349`
- scientific CSV SHA256: `390dcc2f766b81cb95073357d093522d2f9c1a12a38de7818a78a0671f5f1dce`
- archived workflow artifact: `rcms-protocol09-t1`, artifact ID `9479420644`

## Frozen result

| Metric | Result | Preregistered gate |
|---|---:|---|
| mean recovered `A_R` | `0.007732` | diagnostic |
| std recovered `A_R` | `0.178679045823` | diagnostic |
| mean-bias ratio `B` | `0.0432731211675` | PASS (`<= 0.10`) |
| fraction `A_hat > 0` | `0.4882` | PASS (`0.47–0.53`) |
| one-sided nominal-95% FPR | `0.0522` | PASS (`0.035–0.065`) |
| two-sided 95% null coverage | `0.9492` | PASS (`0.92–0.98`) |
| boundary-hit rate | `0.0` | PASS (`<= 0.01`) |
| fit-failure rate | `0.0` | PASS (`<= 0.01`) |

## Interpretation

P09-T1 finds no material evidence that the frozen RCMS DESI-like correlated-covariance inference pipeline manufactures a positive deformation direction when the generator truth is `A_R = 0`. This is a calibration/falsification result only. It does not validate the RCMS physical interpretation and does not convert the v0.2 positive real-data direction into a discovery claim.

The frozen RCMS logarithmic surrogate and all preregistered T1 thresholds remain unchanged.
