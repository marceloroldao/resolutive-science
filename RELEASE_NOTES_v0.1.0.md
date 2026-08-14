# Resolutive Science v0.1.0 — Cosmology Foundation

**Release date:** 2026-08-14  
**Maturity:** First public scientific release candidate  
**Author:** Marcelo Roldão Matos  
**ORCID:** 0009-0003-6075-4680

## Scope

v0.1.0 freezes the first publicly reviewable Resolutive Science package. It contains the RSMS mathematical/methodological foundation and the completed RCMS cosmology validation record through Protocol 03.

The release is cumulative and auditable: preregistrations, implementation decisions, robustness tests, external-data provenance, negative results, inconclusive results, and known limitations are retained rather than rewritten after observing outcomes.

## Frozen cosmology model

The tested RCMS background surrogate uses the frozen deformation

```text
H_eff(z)^2 = H_LCDM(z)^2 + H0^2 A_R ln(1+z)
```

with `A_R = 0` as the null/reference limit for the tested extension. This phenomenological surrogate is not by itself a derivation or validation of the full Resolutive Physics ontology.

## Completed validation record

### Protocol 01

Established the primary low-redshift anchor and model-comparison workflow. The combined analysis produced a positive best-fit `A_R` region, but the protocol did not establish discovery-level evidence.

### Protocol 02

Performed numerical reproduction, DESI jackknife tests, Pantheon+ redshift splits, covariance ablations, null Monte Carlo, and residual localization. The final preregistered classification was:

`INCONCLUSIVE_ROBUSTNESS`

The signal remained numerically stable and was uncommon under the null Monte Carlo, but a substantial fraction of the improvement was localized in the approximate redshift interval `0.6 <= z < 1.0`.

### Protocol 03

Performed external replication with DES-SN5YR/Dovekie and an independent DES Y6 angular-BAO product. DES-SN reproduced the positive direction for `A_R`; the single-point BAO observable was demonstrated to be non-identifying for `A_R` when the global BAO scale is correctly left free. The final preregistered classification was:

`EXTERNAL_REPLICATION_INCONCLUSIVE`

The positive direction replicated in an independent supernova dataset, but the protocol did not obtain a second independent informative external probe.

## Protocol 04 disposition

Protocol 04 was preregistered to test independent multi-redshift shape information with eBOSS DR16. Its P04-T0 execution was not completed before the v0.1.0 freeze because private-repository GitHub Actions quota was exhausted and no hosted runner was allocated. No RCMS parameter from P04 was evaluated for this release.

Protocol 04 is therefore **future work** and is not included in the evidentiary claims of v0.1.0.

## Scientific interpretation

v0.1.0 reports a **candidate observational pattern requiring further falsification and independent replication**. It does not claim:

- discovery of new physics;
- experimental validation of Resolutive Physics;
- replacement of Lambda-CDM;
- proof that the phenomenological `A_R` term derives from the fundamental Resolutive ontology.

## Reproducibility

The repository retains, where applicable, model equations, scripts, tests, workflow definitions, frozen protocol documents, data manifests, upstream revisions, hashes, random seeds, numerical tolerances, and reports. See `REPRODUCIBILITY.md`.

## Licensing

Project-owned software is covered by PolyForm Noncommercial 1.0.0. Project-owned scientific specifications/documentation are covered by CC BY-NC-SA 4.0 unless otherwise stated. Commercial use requires separate written authorization. Third-party datasets retain their original terms.

## Archival plan

After the GitHub `v0.1.0` release is public, the same immutable version should be deposited in Zenodo. The minted DOI must then be added to `README.md`, `CITATION.cff`, and the relevant release documentation without changing the scientific content of the archived v0.1.0 snapshot.
