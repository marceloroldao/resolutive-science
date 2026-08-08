# RCMS Cosmic-Chronometer Production Sample — Moresco BC03 v1

**Dataset ID:** `RCMS-DATA-CC-MORESCO-BC03-v1`  
**Protocol:** `docs/RCMS/protocols/01_low_redshift_observational_preregistration.md`  
**Status:** covariance-compatible production sample, selected before RCMS residual inspection

## Selection rationale

The broad `cc_hz_v1.csv` compilation contains 32 measurements from multiple source families. The public covariance implementation released with Moresco et al. (2020) is tied to a specific 15-point `HzTable_MM_BC03.dat` table. The numerical H(z) values in that source table are not identical to the later 32-point compilation for several overlapping redshifts.

Therefore, directly attaching the released 15-point covariance prescription to the 32-point compilation would mix incompatible data products. The 32-point table remains retained as an auditable broad/exploratory compilation. The primary H(z) production likelihood under Protocol 01 instead uses the exact source-compatible 15-point BC03 table in `cc_hz_moresco_bc03_v1.csv`.

This choice is based solely on provenance and covariance compatibility and was fixed before the RCMS production residuals were inspected.

## Frozen upstream sources

- Michele Moresco, `Cosmic chronometers covariance estimate`
- upstream repository: `https://gitlab.com/mmoresco/CCcovariance`
- frozen revision: `881413330a7f1e1e5203607d6964db49b4c6c461`
- source measurement table: `data/HzTable_MM_BC03.dat`
- source systematic table: `data/data_MM20.dat`
- covariance example: `examples/CC_covariance.ipynb`
- methodological reference: Moresco et al. (2020), arXiv:2003.07362

## Covariance reproduction

The frozen upstream notebook constructs

`C = C_diag + C_IMF + C_SPS-ooo`,

where `C_diag` contains the squared tabulated scalar errors and the two model terms are fully correlated outer products after interpolation of the percentage systematic curves to the measurement redshifts.

The RCMS reproduction uses the same `numpy.interp` endpoint convention: linear interpolation inside the systematic table range and constant endpoint extrapolation outside it.

The upstream notebook reports a determinant of approximately `4.560e33`. The RCMS implementation must reproduce this value within numerical-rounding tolerance and must pass symmetry, positive-definiteness, invertibility, and inverse-residual checks before the production likelihood is evaluated.

## Frozen production parameter bounds

These bounds are fixed before the first production CI run:

- `40 <= H0 <= 100` km s^-1 Mpc^-1;
- `0.05 <= Omega_m <= 0.60`;
- `-5 <= A_R <= 5`.

`H0` and `Omega_m` are common to flat Lambda-CDM and RCMS. `A_R` is the single additional RCMS parameter. The optimizer must report any boundary contact.

## Relationship to the 32-point intake

`RCMS-DATA-CC-HZ-v1` is not deleted or hidden. It remains the broad observational intake and can be used for explicitly labeled diagonal/exploratory checks or future likelihood work if a covariance product compatible with that exact compilation is established. It is not substituted into the covariance-ready production likelihood by approximation.
