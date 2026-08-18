# Resolutive Science v0.2.0 — Release Notes

**Status:** release-candidate documentation draft; not yet tagged  
**RSMS compatibility:** `RSMS-1.0-rc.1`  
**Scientific scope:** frozen RCMS evidence through Protocol 08

## Summary

v0.2.0 consolidates the post-v0.1.1 RCMS observational, robustness, replication, consistency, and mathematical-provenance record. It does not promote experimental material from `resolutiva-reformulacao` into the normative release.

The central release-level result is deliberately narrow: the unchanged one-parameter RCMS screening surrogate repeatedly selects a positive deformation direction across several frozen analyses, including an independent DESI DR2 replication, while robustness and complexity-penalized model selection remain insufficient for a discovery claim or for preference over Lambda-CDM.

## Frozen screening surrogate

\[
H_{\mathrm{eff}}^2(z)=H_{\Lambda\mathrm{CDM}}^2(z)+H_0^2 A_R\ln(1+z).
\]

No v0.2.0 protocol is allowed to retune this form after inspecting a favorable result.

## Evidence added or consolidated

- **P04 — Independent shape replication:** `INDEPENDENT_SHAPE_DIRECTIONAL_ONLY`. Positive direction is recovered in eBOSS DR16 shape information, but the result is strongly LRG-sensitive and is not robust model support.
- **P05 — LRG-dependence challenge:** `POSITIVE_BUT_WEAK`. Replacing the influential LRG block retains a positive best fit, but the profile is compatible with zero and the simpler model remains favored after complexity penalty.
- **P06 — DESI DR2 external replication:** `DESI_DR2_POSITIVE_DIRECTIONAL`. Independent DESI DR2 data return a positive best fit `A_R = 0.210244178`, close to the earlier amplitude scale; `Delta AIC < 0`, so this is directional replication rather than model-selection preference.
- **P07 — Cross-protocol synthesis:** `COMMON_POSITIVE_COMPATIBLE`. A descriptive common amplitude `A_R = 0.211141330` is compatible with the frozen profiles and remains positive under leave-one-out checks. Because evidence overlaps, this is not interpreted as an independent combined discovery significance.
- **P08 — Logarithmic provenance:** `LOG_FORM_CONDITIONALLY_DERIVED`. Under the explicit hypothesis of continuous additive state drift under multiplicative scale composition, the logarithmic dependence follows mathematically as `S(lambda)=s1 ln(lambda)`. The scale-composition hypothesis itself is not derived from the Resolutive Master Equation.

The complete P01–P08 record is summarized in `docs/releases/v0.2.0_EVIDENCE_MATRIX.md`.

## Reproducibility and release gates

The v0.2.0 audit branch contains an automated gate covering RSMS structural consistency, frozen scientific classifications, license/metadata boundaries, Protocol 07 regression, and Protocol 08 provenance regression. The candidate revision was additionally checked with the selected RCMS synthetic suite and release-relevant P02-T5, P03-T1, P06-T0, P06-T1, and P07 workflows.

The final tag must be created only after these gates remain green on the frozen candidate revision.

## Licensing

The repository preserves scope-based licensing:

- software/code: PolyForm Noncommercial License 1.0.0;
- documentation/scientific text: CC BY-NC-SA 4.0 where declared;
- commercial exploitation: requires a separate written commercial license;
- third-party datasets/software remain under their own licenses and are not relicensed by this repository.

Because commercial-use restrictions apply, this project must not be represented as OSI-approved Open Source software.

## Claims boundary

v0.2.0 **does not claim** experimental validation of Resolutive Physics, discovery of new physics, statistical preference of RCMS over Lambda-CDM across the evidence base, an independent combined discovery significance from P07, derivation of the logarithmic term from a fundamental Resolutive Master Equation, or physical establishment of the P08 scale-composition hypothesis.

v0.2.0 **may state**, with all protocol qualifications retained, that multiple frozen screenings repeatedly select a positive RCMS deformation direction, DESI DR2 independently reproduces that direction near the earlier amplitude scale, and the logarithmic form has a conditional mathematical derivation under the explicit P08 hypothesis.

## What remains experimental

Work in `resolutiva-reformulacao`, including later exploratory constructions involving phase closure, ZER/interface dynamics, mediated transport, branch memory, and related hypotheses, is intentionally outside the scientific scope of v0.2.0. Such material must pass its own formalization, falsification, and compatibility gates before any future promotion into the central specification.

## Citation and archival metadata

Author: Marcelo Roldão Matos  
ORCID: `0009-0003-6075-4680`

`CITATION.cff` remains on the historical v0.1.1 record until the final freeze. The v0.2.0 version and archival metadata are updated only when the release candidate is frozen; the DOI assigned to the new Zenodo version is incorporated after Zenodo deposition.

## Next scientific phase

After v0.2.0, development prioritizes falsification rather than accumulation of favorable fits: stronger null tests, alternative one-parameter controls, independent datasets, and ultimately preregistered out-of-sample prediction. A later release should attempt to derive or replace the phenomenological logarithmic surrogate from the underlying formalism rather than assuming it.
