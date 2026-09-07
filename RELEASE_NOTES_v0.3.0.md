# Resolutive Science v0.3.0 — Falsification Release

**Status:** final release metadata  
**Release date:** 2026-09-07  
**Parent:** v0.2.0 — DOI `10.5281/zenodo.22002018`  
**Compatibility:** `RSMS-1.0-rc.1`

## Purpose

v0.3.0 is an adversarial falsification release for the frozen one-parameter RCMS cosmological screening surrogate

\[
E_{\rm RCMS}^2(z)=\Omega_m(1+z)^3+(1-\Omega_m)+A_R\ln(1+z).
\]

The equation was not modified in response to unfavorable results.

## Added scientific protocols

v0.3.0 adds Protocols 09–16:

- **P09:** null false-positive calibration, including realistic DESI DR2 covariance;
- **P10:** injection/recovery calibration;
- **P11:** equally complex functional controls;
- **P12:** leave-one-dataset-family-out stress test;
- **P13:** systematics and nuisance sensitivity map;
- **P14:** amplitude stability diagnostics;
- **P15:** complexity-penalized model-selection synthesis;
- **P16:** preregistered out-of-sample BOSS DR12 prediction.

## Principal findings

### Pipeline calibration survives

P09 and P10 find no material evidence that the inference pipeline intrinsically manufactures positive amplitudes. Null false-positive rates and interval coverage remain close to nominal, and injected negative/zero/positive amplitudes are recovered approximately linearly.

### Positive direction remains descriptive, not model-selective

P12 preserves a positive descriptive common direction when each frozen observational family is removed in turn. However, this does not establish statistical preference for RCMS.

### Logarithmic form is not uniquely selected

P11 classifies the current DESI DR2 functional comparison as `FUNCTIONALLY_NON_SPECIFIC`. A preregistered saturating one-parameter control is slightly better in chi-square than the logarithmic form, and no deformation gains AIC preference over Lambda-CDM in that test.

### Systematics/channel sensitivity is material

P13 returns `SYSTEMATICS_SENSITIVE`. In particular, the DESI DR2 radial-only branch yields a negative best-fit amplitude while the transverse/volume-only branch yields a much larger positive amplitude.

### One universal amplitude is not established

P14 returns `AMPLITUDE_FAMILY_HETEROGENEOUS`. The descriptive common profile remains positive, but not all family intervals intersect it and the radial/transverse channel comparison has opposite signs.

### No complexity-penalized model preference

P15 returns `NO_MODEL_SELECTION_PREFERENCE`: only one frozen family has positive Delta AIC, no applicable family has positive Delta BIC, and the logarithmic shape does not beat the best equally complex control by the preregistered threshold.

### Highest-value out-of-sample prediction is not confirmed

P16 froze BOSS DR12 as a held-out target before RCMS inspection and predicted

`0.121971100 <= A_R <= 0.407494649`, with positive sign.

P16-T0 passed the intake and identifiability gates without evaluating `A_R`.

The blind P16-T1 fit then reached the frozen lower boundary:

- `A_R = -1.000000`;
- profile within the frozen domain `[-1.000000, -0.040000]`;
- quantitative prediction hit: `False`;
- directional prediction hit: `False`;
- `Delta AIC = -0.9580`;
- `Delta BIC = -0.7498`.

By the preregistered boundary rule the formal classification is `OUT_OF_SAMPLE_INVALID`. The parameter range is not widened post hoc. The result is preserved as an unfavorable out-of-sample falsification outcome.

## Release-level scientific conclusion

v0.3.0 does not validate Resolutive Physics and does not establish RCMS as preferred over Lambda-CDM.

The release narrows the evidence claim substantially:

- the numerical/statistical inference machinery passes important calibration tests;
- positive best-fit recurrence exists descriptively across several previously analyzed datasets;
- the logarithmic form is not uniquely identified;
- the fitted amplitude is not stable across all analysis channels/families;
- complexity penalties do not select RCMS;
- and the preregistered held-out BOSS DR12 positive prediction is not reproduced within the frozen primary domain.

The scientific value of v0.3.0 is therefore the reproducible falsification record itself.

## Reproducibility

Protocol preregistrations, runners, workflows, frozen upstream revisions, checksums, machine-readable artifacts, and scientific outcome reports are preserved in the repository. See:

- `docs/releases/v0.3.0_EVIDENCE_MATRIX.md`;
- `docs/RCMS/protocols/`;
- `docs/RCMS/results/`;
- `tools/`;
- `.github/workflows/`.

## Archival metadata

The version is finalized as `v0.3.0` with release date `2026-09-07`. The Zenodo DOI is intentionally not invented in advance; after archival deposition, the assigned DOI must be added back to `CITATION.cff`, `README.md`, and the version metadata in a provenance-preserving follow-up commit.

## Publication boundary

No additional cosmological model term, wider P16 amplitude bound, new external calibration, or substitute target is introduced in v0.3.0 after the P16 reveal. Any later model revision belongs to a new version and must preserve this frozen record.