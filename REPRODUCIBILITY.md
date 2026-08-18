# Reproducibility Guide — v0.2.0 release candidate

This document defines the reproducibility contract for the Resolutive Science v0.2.0 scientific release scope.

**RSMS compatibility:** `RSMS-1.0-rc.1`

## Scientific boundary

Reproducing a numerical or analytic result verifies that the documented computation can be repeated under the declared assumptions. It does not by itself establish experimental validation, physical truth, discovery significance, or scientific acceptance.

## Reproduction workflow

1. Clone the repository and, after release, check out the immutable `v0.2.0` tag.
2. Use the Python/dependency configuration committed with that tag.
3. Read the applicable RCMS protocol before executing its runner. Protocol documents define frozen hypotheses, datasets, nuisance treatment, thresholds, and interpretation rules.
4. Acquire third-party datasets only from the authoritative locations recorded by the repository. Do not substitute newer data releases unless performing a new, explicitly versioned analysis.
5. Verify recorded hashes, upstream revisions, manifests, or provenance records where provided.
6. Run the relevant validation/analysis script without changing frozen thresholds, parameter bounds, covariance treatment, seeds, data selection, or model definitions.
7. Compare generated metrics against the frozen report for that protocol within documented numerical tolerances.
8. Report deviations, environment differences, failed acquisitions, or unavailable upstream material rather than silently replacing inputs.

## Release-audit path

The release branch includes an automated v0.2.0 audit gate. A clean checkout must be able to execute the structural RSMS audit, the v0.2.0 release-document audit, Protocol 07 consistency regression, and Protocol 08 provenance regression using the dependencies declared by the workflow.

The release gate protects the frozen classifications and the claims boundary. Passing it demonstrates repository-level reproducibility of those checks; it does not upgrade the evidentiary strength of any scientific result.

## Data policy

Third-party data are not relicensed by this repository. Some workflows download public upstream bytes at execution time; others retain only manifests, checksums, references, or derived products where permitted. Researchers are responsible for complying with the original dataset terms.

## Provenance requirements

A reproduction report should record at minimum:

- repository tag and commit SHA;
- RSMS compatibility baseline;
- operating system and architecture;
- Python version and dependency environment;
- executed command/script;
- dataset version, upstream revision, manifest, or hash;
- random seed where stochastic computation is used;
- relevant numerical tolerances;
- resulting fit parameters and model-comparison metrics;
- any deviations from the frozen protocol.

## Frozen v0.2.0 evidence boundary

The proposed v0.2.0 scientific evidence boundary covers RCMS Protocols 01–08. The consolidated release matrix is `docs/releases/v0.2.0_EVIDENCE_MATRIX.md`.

The additional v0.2.0 record preserves both positive and limiting outcomes. In particular, directional positive fits must not be reinterpreted as discovery significance or global model preference, and Protocol 08 remains a conditional mathematical derivation rather than a derivation from a fundamental Resolutive Master Equation.

Experimental material from other repositories, including `resolutiva-reformulacao`, is outside this release boundary unless explicitly incorporated by a future versioned protocol.

## Independent reproduction

Independent researchers are encouraged to:

- reproduce the frozen results without modifying the model;
- test the same frozen model on independent datasets;
- report null and negative results;
- compare against conventional competing cosmological extensions with appropriate complexity penalties;
- open an issue or provide a reproducible report when discrepancies are found.

## DOI

The existing v0.1.x DOI remains historical metadata for those releases. After the v0.2.0 Zenodo deposition, the DOI for the new immutable release must be recorded in `CITATION.cff`, the README, and the corresponding release metadata without overwriting historical provenance.
