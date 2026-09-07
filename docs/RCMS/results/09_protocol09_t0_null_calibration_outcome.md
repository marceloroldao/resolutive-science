# RCMS Protocol 09 T0 — Null False-Positive Calibration Outcome

**Status:** FROZEN OUTCOME  
**Release line:** v0.3-dev  
**Protocol:** P09-T0  
**RSMS compatibility:** RSMS-1.0-rc.1  
**Parent release:** v0.2.0 — DOI 10.5281/zenodo.22002018

## 1. Frozen execution identity

The preregistered final execution completed in GitHub Actions workflow:

- workflow: `RCMS Protocol 09 T0 Null Calibration`
- run ID: `32180054736`
- job ID: `95850697845`
- final scientific run size: `N = 10000`
- master seed: `20260818`
- null truth: `A_R = 0`
- final identity check: `PASS`

The workflow also ran a development smoke test at `N = 1000`. That smoke result is not the scientific outcome and is preserved only as an implementation diagnostic.

## 2. Final preregistered results

For the frozen `N = 10000` run:

| Metric | Result |
|---|---:|
| analytic/nominal sigma_A | 0.0149832353207 |
| mean recovered A_hat | 8.10374758665e-05 |
| std(A_hat) | 0.0150314081658 |
| bias ratio B = abs(mean)/std | 0.00539120985689 |
| fraction A_hat > 0 | 0.505200000 |
| one-sided nominal-95% false-positive rate | 0.050200000 |
| two-sided 95% coverage | 0.948500000 |
| boundary-hit rate | 0.000000000 |
| numerical failure rate | 0.000000000 |

Final classification:

`CALIBRATION_PASS`

Overall preregistered gate:

`P09_T0_OVERALL_PASS=True`

## 3. Comparison with preregistered gates

### Sign symmetry

Preregistered nominal band:

`0.485 <= P(A_hat > 0) <= 0.515`

Observed:

`P(A_hat > 0) = 0.5052`

Result: **PASS**.

### Mean-bias diagnostic

Preregistered negligible-bias criterion:

`B <= 0.05`

Observed:

`B = 0.00539120985689`

Result: **PASS**.

### 95% coverage

Preregistered nominal calibration band:

`0.94 <= coverage <= 0.96`

Observed:

`coverage = 0.9485`

Result: **PASS**.

### Numerical failure rate

Preregistered failure criterion:

`failure_rate > 0.01`

Observed:

`failure_rate = 0.0`

Result: **PASS**.

## 4. False-positive calibration

The observed one-sided nominal-95% false-positive rate was

`0.0502`,

which is effectively the nominal 5% target in this controlled T0 design.

This means the tested one-parameter statistical core does not show evidence of manufacturing a positive RCMS amplitude under the controlled null generator used here.

This is a calibration result, not evidence that RCMS is physically correct.

## 5. Smoke-test preservation

The implementation smoke test used `N = 1000` and returned:

- `mean_A_hat = 0.00105036787097`
- `std_A_hat = 0.0152290392284`
- `B = 0.0689713812683`
- `P(A_hat > 0) = 0.531`
- one-sided FPR95 = `0.060`
- coverage95 = `0.945`
- classification = `CALIBRATION_FAIL`

This smoke-test classification is preserved and is not reinterpreted as the scientific result. The preregistration explicitly defined `N = 10000` as the final scientific run; small-N smoke tests were allowed only for implementation validation.

The difference illustrates why the preregistered final sample size matters: the `N=1000` sign fraction fluctuated outside the narrow final-run symmetry band, while the frozen `N=10000` ensemble converged inside all preregistered gates.

## 6. Artifact integrity

Final realization CSV SHA256:

`07b65beef0afac08075b9fd5217e230d7365f6f13b480f13f177b13aadb753b9`

Uploaded GitHub Actions artifact:

- artifact name: `rcms-protocol09-t0`
- artifact ID: `9340425718`
- artifact ZIP SHA256 reported by GitHub Actions: `6c1ea49f92c40385eb447443a6784af84bf5859a4635ba3073370f599a61d054`

The artifact contains:

- `rcms_protocol09_t0_summary.json`
- `rcms_protocol09_t0_realizations.csv`

## 7. Scientific interpretation

P09-T0 answers a narrow question:

> In the controlled diagonal-noise null design preregistered for T0, does the inference core itself produce an anomalous positive-amplitude bias or miscalibrated false-positive rate?

The answer is **no evidence of such a failure** under this controlled design.

The outcome does **not** establish that release-relevant observational covariance, nuisance structure, selection effects, or dataset-specific systematics are equally well calibrated. Those are explicitly deferred to P09-T1 and later v0.3 falsification protocols.

## 8. Frozen classification

`P09_T0_CLASSIFICATION=CALIBRATION_PASS`

This classification must not be promoted to a physical-validation claim.

## 9. Next gate

Proceed to P09-T1: null calibration using a frozen release-relevant observational sampling/covariance structure, with its generator, nuisance treatment, seeds, metrics, and decision thresholds preregistered before inspecting the final T1 outcome.
