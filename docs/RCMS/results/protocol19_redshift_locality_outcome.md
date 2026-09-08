# RCMS Protocol 19 — Redshift Locality Outcome

**Status:** FINAL / FROZEN  
**Release line:** v0.4-dev  
**Classification:** `NO_REDSHIFT_LOCALITY_EVIDENCE`  
**Parent release:** v0.3.0 — DOI `10.5281/zenodo.22643804`

## 1. Hosted execution

GitHub Actions workflow: `RCMS Protocol 19 Redshift Locality`  
Run ID: `34258251442`  
Job ID: `102169412395`  
Artifact: `rcms-protocol19-redshift-locality`  
Artifact ID: `10068775051`  
Artifact ZIP SHA256: `959fac45bae41506f407b4d291cebd9f39ab908788773d9de5d43cbc24a672f4`

Identity gate:

`P19_FINAL_IDENTITY=PASS`

Monte Carlo design was executed exactly as preregistered:

- seed `190019`;
- 2000 constant-amplitude full-covariance null simulations per survey;
- all admissible redshift splits scanned in each realization;
- plus-one empirical look-elsewhere p-value.

## 2. DESI DR2

The maximizing diagnostic split is approximately

`z_s = 0.82`.

At that split, with full-vector `Omega_m` and BAO scale frozen:

- low-z best `A_R = +0.250`;
- high-z best `A_R = +0.190`;
- `D_max = 0.060`;
- opposite signs: `False`;
- one-sigma profile overlap: `True`;
- boundary contact: `False`;
- look-elsewhere empirical p-value: `0.931034`.

The observed redshift separation is therefore entirely unexceptional under the frozen constant-amplitude null calibration.

## 3. BOSS DR12

The maximizing diagnostic split is approximately

`z_s = 0.445`.

At that split:

- low-z best `A_R = -1.000`;
- high-z best `A_R = -0.995`;
- `D_max = 0.005`;
- opposite signs: `False`;
- one-sigma profile overlap: `True`;
- boundary contact: `True`;
- look-elsewhere empirical p-value: `0.758121`.

The BOSS local pulls remain boundary-affected but show essentially no low/high-redshift separation inside the frozen primary domain.

## 4. Preregistered classification

Neither survey satisfies the calibrated `p <= 0.05` locality criterion. Neither exhibits a raw `D_max >= 0.50` with opposite-sign local amplitudes.

Therefore:

`P19_CLASSIFICATION=NO_REDSHIFT_LOCALITY_EVIDENCE`

## 5. Scientific interpretation

P19 gives no support for explaining the v0.3 amplitude heterogeneity by a simple redshift-local change in the frozen logarithmic deformation.

Together with P17 and P18, the diagnostic picture is now:

- P17: post-fit residual topology is diffuse rather than strongly channel- or redshift-organized;
- P18: the strong radial/transverse amplitude sign reversal is survey-specific to DESI and is not independently reproduced by BOSS;
- P19: no calibrated redshift-local amplitude split appears in either DESI or BOSS.

Accordingly, there is currently no empirical basis in these diagnostics for adding either a radial/transverse switch or a redshift change-point to RCMS.

## 6. Advancement

Proceed to P20 cross-survey concordance at overlapping redshift. P20 should ask whether DESI and BOSS measurements in comparable redshift windows prefer compatible directions under the same frozen surrogate, while keeping survey calibration/nuisance conventions explicit. Only after P20 is frozen may P21 consider whether any minimal extension is scientifically motivated.
