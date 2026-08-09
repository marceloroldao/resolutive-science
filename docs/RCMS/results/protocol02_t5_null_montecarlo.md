# RCMS Protocol 02 — T5 Null Monte Carlo Result

**Status:** completed preregistered robustness test  
**Model:** frozen one-parameter surrogate `A_R ln(1+z)`  
**Simulations:** 500  
**RNG seed:** `20260809`  
**Frozen observed threshold:** `Delta chi2 = 4.559528`

## Result

The preregistered null Monte Carlo generated 500 realizations from the best-fit flat Lambda-CDM model under the same H(z), Pantheon+, and DESI DR2 likelihood structure used for Protocol 01.

The number of null realizations with

`Delta chi2_sim >= 4.559528`

was **17 / 500**.

Using the preregistered finite-sample estimator,

`p_MC = (1 + exceedances) / (1 + N_sim)`,

the empirical probability is

`p_MC = 0.03592814`.

The null distribution had:

- mean `Delta chi2 = 0.992775`;
- median `Delta chi2 = 0.403105`;
- 90th percentile `= 2.962338`;
- 95th percentile `= 3.905768`;
- 99th percentile `= 6.647125`.

The fitted null `A_R` distribution was centered near zero:

- mean `A_R = -0.002550`;
- median `A_R = 0.000000`;
- positive fraction `= 0.436`.

## Grid validation note

The accelerated precomputed grid reproduced the real-data combined fit at approximately

- `A_R = 0.175`;
- `Omega_m = 0.300`;
- `Delta chi2 = 4.856345`.

This differs modestly from the production continuous-optimization anchor `Delta chi2 = 4.559528`. The Monte Carlo exceedance threshold was nevertheless kept at the **preregistered production value 4.559528**, rather than being raised to the grid value. Therefore this approximation does not make the reported tail probability artificially smaller; using the higher grid anchor would be a stricter threshold and could only reduce the exceedance count.

## Interpretation

The observed Protocol 01 improvement is **uncommon under the calibrated Lambda-CDM null** at the approximately 3.6% empirical-tail level. This is evidence against the proposition that the observed improvement is a completely routine fluctuation of this exact null-analysis pipeline, but it is not sufficient to establish a physical Resolutive effect or a discovery-level model preference.

The preregistered classification for this test is:

`T5_NULL_CALIBRATION = UNCOMMON_UNDER_LCDM`

T6 residual localization remains required before Protocol 02 can be closed.