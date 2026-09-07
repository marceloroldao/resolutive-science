# Resolutive Science

The official scientific specification and development framework for Resolutive Science.

This repository is the versioned source of truth for the universal mathematical specification, specialized scientific specifications, reproducible analyses, validation protocols, software, and shared documentation of the Resolutive Science research program.

## Release

**Current public scientific release:** `v0.2.0` — RCMS Extended Validation, consolidating the frozen RCMS evidence record through Protocol 08 under `RSMS-1.0-rc.1` compatibility.

**Zenodo DOI (v0.2.0):** `10.5281/zenodo.22002018`

**Current development candidate:** `v0.3-dev` — RCMS Falsification Release candidate. Protocols 09–16 are now complete on the development branch; release audit and metadata synchronization remain before `v0.3.0` publication.

The prior `v0.1.1` release remains the immutable metadata/archive correction of the `v0.1.0` Cosmology Foundation snapshot. No historical scientific results are rewritten by later releases.

## Primary specifications

- **RSMS** — Resolutive Science Mathematical Specification (`1.0-rc.1`)
- **RCMS** — Resolutive Cosmology Mathematical Specification (`0.1` research line)

## Scientific status

Resolutive Science is a research program. Mathematical consistency, software verification, numerical performance, observational agreement, external replication, independent scientific validation, and scientific acceptance are distinct stages.

The published v0.2.0 RCMS record through Protocol 08 contains a recurring positive one-parameter deformation direction, including independent DESI DR2 directional replication, but robustness and complexity-penalized model-selection results are insufficient for a discovery claim or preference over Lambda-CDM.

The v0.3 falsification line deliberately subjects that pattern to stronger adversarial tests without changing the frozen logarithmic surrogate. The completed v0.3 protocols show simultaneously that:

- the inference pipeline passes null and injection/recovery calibration tests;
- the positive descriptive direction is not carried by only one previously analyzed dataset family;
- the logarithmic form is not uniquely selected against equally complex smooth controls;
- fitted amplitudes are sensitive to analysis channel/systematics and are not universal across all probes;
- complexity penalties do not establish model preference over Lambda-CDM; and
- the preregistered held-out BOSS DR12 positive prediction is not reproduced within the frozen primary domain and instead drives the fit to the negative `A_R=-1` boundary.

The P16 boundary rule classifies that target fit as `OUT_OF_SAMPLE_INVALID`; the parameter range is not widened post hoc. The failed quantitative and directional predictions remain part of the scientific record.

Publication of this repository does not imply that Resolutive Physics is established physics.

## Reproducibility

The repository preserves model definitions, protocol preregistrations, data provenance/manifests, analysis runners, numerical gates, workflows, frozen scientific reports, and unfavorable outcomes where applicable. Third-party datasets are referenced or acquired under their original terms and are not relicensed by this repository.

For the current published release see [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md), [`RELEASE_NOTES_v0.2.0.md`](RELEASE_NOTES_v0.2.0.md), and [`docs/releases/v0.2.0_EVIDENCE_MATRIX.md`](docs/releases/v0.2.0_EVIDENCE_MATRIX.md).

For the v0.3 release candidate see [`RELEASE_NOTES_v0.3.0.md`](RELEASE_NOTES_v0.3.0.md), [`docs/releases/v0.3.0_EVIDENCE_MATRIX.md`](docs/releases/v0.3.0_EVIDENCE_MATRIX.md), and [`docs/releases/v0.3.0_PUBLICATION_CHECKLIST.md`](docs/releases/v0.3.0_PUBLICATION_CHECKLIST.md).

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

Zenodo DOI for `v0.2.0`: **10.5281/zenodo.22002018**.

Historical Zenodo DOI for `v0.1.1`: **10.5281/zenodo.21940994**.

The v0.3.0 DOI will be added after the final immutable release is archived; until then `CITATION.cff` intentionally remains on the current public v0.2.0 release.

## Author

Marcelo Roldão Matos  
ORCID: 0009-0003-6075-4680

## Status

**Published scientific snapshot:** `v0.2.0`.  
**Development publication candidate:** `v0.3-dev`, Protocols 09–16 complete; release audit pending.  
**RSMS compatibility baseline:** `RSMS-1.0-rc.1`.