# RCMS Protocol 17-A — Residual Topology and Sign Map Outcome

**Status:** FINAL / FROZEN  
**Release line:** v0.4-dev  
**Classification:** `DIFFUSE_RESIDUAL_STRUCTURE`  
**Parent release:** v0.3.0 — DOI `10.5281/zenodo.22643804`

## 1. Hosted execution

GitHub Actions workflow: `RCMS Protocol 17 Residual Topology`  
Run ID: `34257377610`  
Job ID: `102166488241`  
Artifact: `rcms-protocol17-residual-topology`  
Artifact ID: `10068427578`  
Artifact ZIP SHA256: `c16ec2797537fd3e34254c00a081ae4f1bdb4adac7c9e05572453244efd9593c`

The frozen identity check passed:

`P17_FINAL_IDENTITY=PASS`

Both v0.3 likelihood closures passed before any residual topology result was accepted.

## 2. Scope

P17-A is deliberately limited to BAO datasets with complete reproducible measurement vectors and covariance matrices already used in v0.3:

- DESI DR2 BAO (13 observables);
- SDSS-III BOSS DR12 consensus BAO (6 observables).

No supernova or H(z) pseudo-residuals were reconstructed from summary amplitudes.

No new physical parameter or functional form was introduced.

## 3. Frozen summary

| Survey | Model | chi2 | radial canonical mean | transverse/volume canonical mean | radial-transverse gap | low-z mean | high-z mean | low-high gap |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| DESI DR2 | Lambda-CDM | 10.271041 | -0.294403 | +0.293507 | -0.587910 | -0.103915 | +0.169255 | -0.273170 |
| DESI DR2 | RCMS | 8.965256 | -0.168998 | +0.183700 | -0.352698 | -0.063068 | +0.118898 | -0.181966 |
| BOSS DR12 | Lambda-CDM | 2.061159 | +0.291874 | -0.214474 | +0.506347 | +0.112130 | -0.108159 | +0.220289 |
| BOSS DR12 | RCMS | 1.019163 | +0.115022 | -0.091574 | +0.206596 | +0.036249 | -0.037326 | +0.073575 |

The BOSS radial standardized residual sign is canonicalized from native `H r_d` orientation to the equivalent `D_H/r_d` direction only for cross-survey channel sign summaries; native residuals and covariance-whitened residuals remain unchanged in the machine-readable artifact.

## 4. Preregistered classification

`CHANNEL_ORGANIZED_TENSION` required, under RCMS in at least one survey:

1. absolute radial-minus-transverse canonical mean gap >= 0.50 marginal sigma; and
2. opposite signs between the two channel means.

That criterion is not met:

- DESI RCMS gap magnitude = `0.352698`;
- BOSS RCMS gap magnitude = `0.206596`.

`REDSHIFT_ORGANIZED_TENSION` required, if the channel criterion failed, a low-z versus high-z canonical mean gap >= 0.50 marginal sigma with opposite signs. That criterion is also not met:

- DESI RCMS redshift gap magnitude = `0.181966`;
- BOSS RCMS redshift gap magnitude = `0.073575`.

Therefore:

`P17_CLASSIFICATION=DIFFUSE_RESIDUAL_STRUCTURE`

## 5. Scientific interpretation

P17-A does **not** support a simple claim that the remaining v0.3 discrepancy is visible as a strong residual channel split or a strong low-versus-high-redshift split after fitting the frozen RCMS separately to each survey.

There is channel opposition in the marginal standardized residual means under both Lambda-CDM fits, but the fitted RCMS reduces rather than strengthens those residual gaps. The preregistered 0.50-sigma organized-tension threshold is not reached under RCMS.

This result does not erase P13. P13 asked a different question: whether independently fitting radial-only and transverse/volume-only DESI subsets produces compatible inferred amplitudes. It did not. P17 instead asks whether the *residuals remaining after the full-vector fit* retain a strong organized channel topology. They do not at the frozen threshold.

Thus the current evidence is more specific:

- parameter inference is channel-sensitive (P13/P14);
- but the post-fit residual field in P17-A is not strongly channel-organized or redshift-organized by the preregistered rule.

This distinction argues against prematurely introducing a redshift switch or radial/transverse correction term.

## 6. Advancement

Proceed to P18 as a **parameter-consistency audit**, not a residual-pattern rescue attempt.

P18 should test whether radial/transverse amplitude incompatibility recurs across independent BAO surveys under matched conventions, while preserving the P17 result that the post-fit residual topology itself is diffuse.
