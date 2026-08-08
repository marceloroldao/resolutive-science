# RCMS Cosmic-Chronometer H(z) Dataset v1 — Provenance Record

**Dataset ID:** `RCMS-DATA-CC-HZ-v1`  
**Status:** Ingested; primary observational fit blocked pending covariance reproduction  
**Protocol:** `docs/RCMS/protocols/01_low_redshift_observational_preregistration.md`  
**Ingested:** 2026-08-08

## Scope

This dataset contains 32 published cosmic-chronometer measurements of the Hubble parameter over approximately `0.07 <= z <= 1.965`.

The values in `cc_hz_v1.csv` were transcribed from the cosmic-chronometer table published in:

- *Cosmic chronometers to calibrate the ladders and measure the curvature of the Universe. A model-independent study*, Monthly Notices of the Royal Astronomical Society, volume 523 (2023), page 3406 and associated table.
- Source page: https://academic.oup.com/mnras/article/523/3/3406/7188316

That table cites the original measurement papers individually and states that the covariance matrix is computed using the method presented in Moresco et al. (2020), incorporating statistical and systematic errors.

## Covariance source

The systematic-covariance methodology and public supporting data are maintained by Michele Moresco in:

- project: `Cosmic chronometers covariance estimate`;
- repository: https://gitlab.com/mmoresco/CCcovariance
- revision frozen for RCMS reproduction work: `881413330a7f1e1e5203607d6964db49b4c6c461`;
- method paper: Moresco et al. (2020), *Setting the Stage for Cosmic Chronometers. II. Impact of Stellar Population Synthesis Models Systematics and Full Covariance Matrix*, arXiv:2003.07362.

The public repository describes the covariance as

`Cov = Cov_stat + Cov_syst`, with systematic contributions from metallicity, young stellar contamination, star-formation history, IMF, stellar library, and stellar-population-synthesis modeling. Some model contributions are correlated across redshift.

## Production-fit gate

The scalar uncertainties in `cc_hz_v1.csv` are sufficient for data-integrity checks and exploratory plotting, but **they shall not be treated as a declaration that all 32 observations are statistically independent**.

Under RCMS Observational Protocol 01, the primary production fit is blocked until one of the following is completed and documented:

1. the appropriate published covariance matrix is reproduced from the frozen Moresco methodology/data and mapped to the adopted measurements; or
2. a source-provided covariance product for the exact adopted compilation is ingested and verified.

A diagonal-only fit may be implemented solely as an explicitly labeled exploratory/software-validation result. It shall not be reported as the pre-registered primary observational comparison.

## Data-integrity rules

The ingestion layer shall verify:

- exactly 32 rows;
- unique `(z, reference_key)` records;
- finite positive `H` and uncertainty values;
- monotonically sortable redshifts;
- units `km s^-1 Mpc^-1`;
- no residual-based exclusion of points.

## References represented in the table

The compact `reference_key` field maps to the source families named in the published compilation:

- `Jimenez2003` — Jimenez et al. (2003);
- `Simon2005` — Simon, Verde & Jimenez (2005);
- `Stern2010` — Stern et al. (2010);
- `Moresco2012` — Moresco et al. (2012);
- `Zhang2014` — Zhang et al. (2014);
- `Moresco2015` — Moresco (2015);
- `Moresco2016` — Moresco et al. (2016);
- `Ratsimbazafy2017` — Ratsimbazafy et al. (2017);
- `Borghi2022` — Borghi, Moresco & Cimatti (2022).

The provenance record, not the compact key, is the governing source declaration.

## Scientific-status note

Ingestion of published observations is not a fit result and is not evidence for or against RCMS. Model interpretation begins only after the pre-registered likelihood/covariance requirements are satisfied.