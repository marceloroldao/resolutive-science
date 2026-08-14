# Reproducibility Guide — v0.1.0

This document describes the reproducibility contract for the first public Resolutive Science release.

## Scientific boundary

Reproducing a numerical result verifies that the documented computation can be repeated under the declared assumptions. It does not by itself establish experimental validation, physical truth, or scientific acceptance.

## Reproduction workflow

1. Clone the repository and check out the immutable `v0.1.0` tag after release.
2. Use the Python/dependency configuration committed with that tag.
3. Read the applicable RCMS protocol before executing its runner; protocol documents define frozen hypotheses, datasets, nuisance treatment, thresholds, and interpretation rules.
4. Acquire third-party datasets only from the authoritative locations recorded by the repository. Do not substitute newer data releases unless performing a new, explicitly versioned analysis.
5. Verify recorded hashes or upstream revisions where provided.
6. Run the relevant validation/analysis script without changing frozen thresholds, parameter bounds, covariance treatment, seeds, or data selection.
7. Compare generated metrics against the frozen report for that protocol within the documented numerical tolerances.
8. Report deviations, environment differences, failed acquisitions, or unavailable upstream material rather than silently replacing inputs.

## Data policy

Third-party data are not relicensed by this repository. Some workflows download public upstream bytes at execution time; others retain only manifests, checksums, references, or derived products where permitted. Researchers are responsible for complying with the original dataset terms.

## Provenance requirements

A reproduction report should record at minimum:

- repository tag and commit SHA;
- operating system and architecture;
- Python version and dependency environment;
- executed command/script;
- dataset version, upstream revision, or hash;
- random seed where stochastic computation is used;
- relevant numerical tolerances;
- resulting fit parameters and model-comparison metrics;
- any deviations from the frozen protocol.

## Completed v0.1.0 evidence boundary

The scientific evidence frozen for v0.1.0 ends with completed RCMS Protocol 03. Protocol 04 preregistration/intake material may be present in repository history, but P04-T0 did not complete before the release freeze and no P04 RCMS parameter evaluation is part of v0.1.0.

## Independent reproduction

Independent researchers are encouraged to:

- reproduce the frozen results without modifying the model;
- test the same frozen model on independent datasets;
- report null and negative results;
- compare against conventional competing cosmological extensions with appropriate complexity penalties;
- open an issue or provide a reproducible report when discrepancies are found.

## DOI

After Zenodo deposition, the DOI for the corresponding immutable release should be recorded in the repository citation metadata and README.
