# Resolutive Science v0.4.0 — Post-Falsification Diagnostic Release

**Status:** release candidate  
**Parent:** v0.3.0 — DOI `10.5281/zenodo.22643804`  
**Compatibility:** `RSMS-1.0-rc.1`

## Purpose

v0.4.0 is a diagnostic negative release. It follows the failed preregistered v0.3 held-out prediction and asks whether the observed RCMS inconsistency can be organized by residual channel, radial/transverse parameter direction, redshift locality, or cross-survey epoch.

The published one-parameter surrogate is not modified:

\[
E^2(z)=\Omega_m(1+z)^3+(1-\Omega_m)+A_R\ln(1+z).
\]

No new cosmological parameter or functional form is introduced in this release.

## Added protocols

v0.4.0 adds the diagnosis-before-extension block:

- **P17** — residual topology and sign map;
- **P18** — radial/transverse parameter-consistency audit;
- **P19** — redshift-locality diagnostic with look-elsewhere calibration;
- **P20** — exact-redshift DESI/BOSS cross-survey concordance.

## Principal results

### P17 — residual topology is diffuse

`DIFFUSE_RESIDUAL_STRUCTURE`

After fitting the frozen RCMS separately to DESI DR2 and BOSS DR12, the remaining marginal residual field does not satisfy the preregistered threshold for a strong channel-organized or low/high-redshift pattern.

### P18 — DESI channel tension is not universal

`SURVEY_SPECIFIC_CHANNEL_TENSION`

DESI DR2 reproduces the strong radial/transverse amplitude split:

- radial `A_R=-0.58`, profile `[-0.83,-0.24]`;
- transverse/volume `A_R=+0.86`, profile `[+0.10,+1.00]`.

BOSS DR12 does not replicate this sign reversal. Its three-point channel subsets are weakly identifying and both one-sigma amplitude profiles span the full frozen domain.

### P19 — no redshift-locality evidence

`NO_REDSHIFT_LOCALITY_EVIDENCE`

With full-fit nuisance states frozen and a preregistered scan over admissible redshift cuts:

- DESI `D_max=0.060`, look-elsewhere `p=0.931034`;
- BOSS `D_max=0.005`, look-elsewhere `p=0.758121`.

The data do not support a simple redshift change-point explanation.

### P20 — exact-redshift survey discordance

`EXACT_Z_SURVEY_DISCORDANCE`

At the exact common redshift `z=0.51`, with each survey's global nuisance state frozen:

- DESI local `A_R=+0.160`, profile `[+0.08,+0.25]`;
- BOSS local `A_R=-1.000`, profile `[-1.00,-0.89]`;
- signs are opposite;
- the local profiles do not overlap;
- BOSS is boundary-limited.

Therefore cosmic epoch alone cannot account for the DESI/BOSS difference inside this diagnostic framework.

## Development stop gate

The v0.4 development plan preregistered a stop condition: if P17–P20 indicate survey/channel heterogeneity without a stable cross-survey organizing structure, the release may close without generating a new RCMS form.

That condition is met.

The frozen development decision is:

`DIAGNOSTIC_STOP_NO_EXTENSION`

P21–P24 are not activated and are not counted as failed protocols. Their prerequisite — a scientifically motivated candidate emerging from P17–P20 — is absent.

## Scientific interpretation

The cumulative evidence rejects several simple post-hoc rescue narratives:

- the inconsistency is not captured by a strong post-fit channel residual pattern;
- the DESI radial/transverse split is not independently reproduced by BOSS;
- no calibrated redshift-local transition is detected;
- independent surveys disagree even at the same redshift.

The current data therefore do not provide a defensible empirical template for adding a redshift switch, channel coefficient, survey offset, or extra cosmological amplitude to RCMS.

v0.4.0 does not establish that Lambda-CDM is complete and does not falsify every possible Resolutive Cosmology. It establishes a narrower and reproducible result: **the current one-parameter RCMS line should not be extended from these same residuals without an independent likelihood/data-convention/systematics audit.**

## Recommended next line

A later version may investigate:

- independent implementation of the DESI/BOSS likelihoods;
- BAO observable and fiducial-convention matching;
- covariance/compression sensitivity;
- survey-specific calibration structure;
- independent BAO data not used to formulate P17–P20.

Only if a stable cross-survey structure survives that audit should a new cosmological candidate be preregistered.

## Preservation boundary

The v0.3 tag, DOI, held-out prediction failure, and all v0.4 diagnostic outcomes remain immutable historical evidence. No result is rewritten to motivate a later candidate.
