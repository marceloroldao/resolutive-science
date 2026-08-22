# RCMS Protocol 09 T1 — DESI Covariance Null Calibration Outcome

**Status:** FROZEN OUTCOME  
**Release line:** v0.3-dev  
**Classification:** `CALIBRATION_PASS`  
**RSMS compatibility:** RSMS-1.0-rc.1

## 1. Preregistered configuration

- null truth: `A_R = 0`;
- observational structure: frozen DESI DR2 BAO 13-point mean layout with frozen 13x13 covariance;
- synthetic generator mean: nested null model with profiled nuisance parameters;
- null nuisance point: `Omega_m = 0.295000`, `q = 29.468025096`;
- final Monte Carlo realizations: `N = 5000`;
- master seed: `20260820`;
- `A_R` scan interval: `[-1, +1]`;
- `A_R` grid spacing: `0.01`;
- `Omega_m` interval: `[0.05, 0.60]`;
- `Omega_m` grid spacing: `0.005`.

No observed DESI residuals were used to tune the null generator after preregistration.

## 2. Final frozen result

The preregistered final run returned:

- `mean(A_hat) = 0.007732`;
- `std(A_hat) = 0.178679045823`;
- bias ratio `B = 0.0432731211675`;
- `P(A_hat > 0) = 0.4882`;
- one-sided nominal-95% false-positive rate = `0.0522`;
- two-sided nominal-95% coverage = `0.9492`;
- boundary-hit rate = `0.0`;
- numerical failure rate = `0.0`.

The machine-identity check passed:

`P09_T1_FINAL_IDENTITY=PASS`

The frozen classification is:

`P09_T1_CLASSIFICATION=CALIBRATION_PASS`

## 3. Interpretation

Under a null data-generating process with `A_R = 0`, using the frozen DESI DR2 BAO sampling/covariance structure and the preregistered nuisance treatment, the P09-T1 pipeline remains acceptably calibrated according to the frozen v0.3 criteria.

The recovered amplitude distribution does not show a material positive-sign bias. The nominal 95% one-sided false-positive rate is close to 5%, the two-sided 95% interval coverage is close to 95%, and no numerical or boundary failures occurred.

This result therefore does **not** support the interpretation that the recurring positive `A_R` direction from the v0.2 evidence record is trivially manufactured by the tested inference machinery under this DESI-like correlated-noise null.

This is a calibration result only. It does **not** establish RCMS as physically correct, does not provide discovery significance, and does not demonstrate preference over Lambda-CDM.

## 4. Smoke test provenance

The development smoke run used `N = 500` with the same seed and returned `CALIBRATION_PASS`. It is preserved for implementation provenance but is not the scientific outcome. The final scientific interpretation is based exclusively on the preregistered `N = 5000` run.

## 5. Artifact provenance

GitHub Actions workflow: `RCMS Protocol 09 T1 DESI Covariance Calibration`  
Run ID: `32328313572`  
Artifact: `rcms-protocol09-t1`  
Artifact ID: `9392142440`  
Artifact ZIP SHA256: `e0d6f4d13d23c588d418a4b0694758e23d13c13067eadffabaebfac1f49303df`  
Realization CSV SHA256: `d94d245c7c5f855f2064e03d858a5eccede25d948531dc183f2da030c8799f24`

## 6. Protocol-09 cumulative conclusion

Both calibration layers completed so far pass their preregistered gates:

- P09-T0 controlled diagonal-noise calibration: `CALIBRATION_PASS`;
- P09-T1 DESI-covariance calibration: `CALIBRATION_PASS`.

The appropriate next falsification stage is P10 injection/recovery. P10 must test negative, zero, and positive injected amplitudes and quantify bias, coverage, sign recovery, uncertainty calibration, and failure regions without changing the v0.2 logarithmic surrogate.
