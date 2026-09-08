# Resolutive Science

The official scientific specification and development framework for Resolutive Science.

This repository is the versioned source of truth for the universal mathematical specification, specialized scientific specifications, reproducible analyses, validation protocols, software, and shared documentation of the Resolutive Science research program.

## Release

**Release candidate:** `v0.4.0` — Post-Falsification Diagnostic Release, adding Protocols 17–20 under `RSMS-1.0-rc.1` compatibility.

**Target release date:** `2026-09-08`.

**Zenodo DOI (v0.4.0):** pending archival deposition. The assigned DOI will be backfilled without rewriting the frozen scientific record.

**Current public release:** `v0.3.0` — RCMS Falsification Release. Zenodo DOI: `10.5281/zenodo.22643804`.

**Previous release:** `v0.2.0` — RCMS Extended Validation. Zenodo DOI: `10.5281/zenodo.22002018`.

The prior `v0.1.1` release remains the immutable metadata/archive correction of the `v0.1.0` Cosmology Foundation snapshot. No historical scientific results are rewritten by later releases.

## Primary specifications

- **RSMS** — Resolutive Science Mathematical Specification (`1.0-rc.1`)
- **RCMS** — Resolutive Cosmology Mathematical Specification (`0.1` research line)

## Scientific status

Resolutive Science is a research program. Mathematical consistency, software verification, numerical performance, observational agreement, external replication, independent scientific validation, and scientific acceptance are distinct stages.

The v0.4 line follows the failed preregistered v0.3 held-out BOSS DR12 prediction and performs diagnosis before any attempted model extension. The frozen one-parameter logarithmic surrogate is not modified.

The completed v0.4 diagnostic block shows:

- P17: `DIFFUSE_RESIDUAL_STRUCTURE` — no preregistered strong post-fit channel or redshift residual topology;
- P18: `SURVEY_SPECIFIC_CHANNEL_TENSION` — the DESI radial/transverse amplitude sign reversal is not independently replicated by BOSS;
- P19: `NO_REDSHIFT_LOCALITY_EVIDENCE` — preregistered split scans with look-elsewhere calibration do not support a redshift change-point;
- P20: `EXACT_Z_SURVEY_DISCORDANCE` — at exactly `z=0.51`, DESI and BOSS pull the unchanged surrogate in opposite directions with non-overlapping local profiles, with BOSS boundary-limited.

Because no stable cross-survey organizing structure emerges, the preregistered development decision is:

`DIAGNOSTIC_STOP_NO_EXTENSION`

P21–P24 are not activated. No new redshift term, channel coefficient, survey offset, or other cosmological free parameter is introduced from the same residuals.

Publication of this repository does not imply that Resolutive Physics is established physics.

## Reproducibility

The repository preserves model definitions, protocol preregistrations, data provenance/manifests, analysis runners, numerical gates, workflows, frozen scientific reports, and unfavorable outcomes where applicable. Third-party datasets are referenced or acquired under their original terms and are not relicensed by this repository.

For v0.4.0 see [`RELEASE_NOTES_v0.4.0.md`](RELEASE_NOTES_v0.4.0.md), [`docs/releases/v0.4.0_EVIDENCE_MATRIX.md`](docs/releases/v0.4.0_EVIDENCE_MATRIX.md), [`docs/releases/v0.4.0_DIAGNOSTIC_GATE.md`](docs/releases/v0.4.0_DIAGNOSTIC_GATE.md), and [`docs/releases/v0.4.0_PUBLICATION_CHECKLIST.md`](docs/releases/v0.4.0_PUBLICATION_CHECKLIST.md).

Historical v0.3.0 materials remain available in [`RELEASE_NOTES_v0.3.0.md`](RELEASE_NOTES_v0.3.0.md) and [`docs/releases/v0.3.0_EVIDENCE_MATRIX.md`](docs/releases/v0.3.0_EVIDENCE_MATRIX.md).

## Licensing

Resolutive Science uses **scope-based dual licensing**.

### Software

Project-owned source code, tools, tests, scripts, analysis runners, and workflow code are licensed for permitted noncommercial use under the **PolyForm Noncommercial License 1.0.0**.

Commercial use requires a separate written commercial license.

### Scientific specifications and documentation

Project-owned scientific specifications, mathematical documentation, reports, explanatory text, and original figures are licensed under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** unless otherwise stated.

### Third-party data

Third-party datasets and externally sourced material retain their original licenses and are not relicensed by this repository. Provenance, checksums, download scripts, and references do not change the rights in the underlying external data.

See:

- [`LICENSE.md`](LICENSE.md) — repository licensing overview;
- [`LICENSES/PolyForm-Noncommercial-1.0.0.md`](LICENSES/PolyForm-Noncommercial-1.0.0.md) — software license;
- [`LICENSES/CC-BY-NC-SA-4.0.md`](LICENSES/CC-BY-NC-SA-4.0.md) — documentation license notice;
- [`COMMERCIAL_LICENSE.md`](COMMERCIAL_LICENSE.md) — commercial licensing policy;
- [`NOTICE`](NOTICE) — copyright and required notice.

Because commercial use is restricted, this project should be described as **public-source/source-available for scientific research**, not as OSI-approved open-source software.

## Citation

Citation metadata is provided in [`CITATION.cff`](CITATION.cff).

Zenodo DOI for `v0.4.0`: pending archival deposition.

Zenodo DOI for `v0.3.0`: **10.5281/zenodo.22643804**.

Zenodo DOI for `v0.2.0`: **10.5281/zenodo.22002018**.

Historical Zenodo DOI for `v0.1.1`: **10.5281/zenodo.21940994**.

## Author

Marcelo Roldão Matos  
ORCID: 0009-0003-6075-4680

## Status

**Release candidate:** `v0.4.0`.  
**Frozen diagnostic scope:** RCMS Protocols 17–20; P21–P24 not activated by preregistered stop gate.  
**RSMS compatibility baseline:** `RSMS-1.0-rc.1`.
