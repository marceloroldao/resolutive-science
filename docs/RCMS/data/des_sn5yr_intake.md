# RCMS Protocol 03 — DES-SN5YR/Dovekie intake

**Status:** Frozen external-replication intake before P03-T1 output inspection  
**Protocol:** RCMS Protocol 03  
**Purpose:** Freeze provenance, byte identity, ordering, likelihood conventions, and the first external-replication runner.

## Upstream source

- Repository: `des-science/DES-SN5YR`
- Frozen revision: `c9a4fcafc4cbd19bd750dee47fc76194a45c181f`
- Upstream description: DES Supernova Cosmological Analysis

The revision above was frozen before any RCMS P03-T1 fit output was inspected.

## Production files

The production Hubble-diagram/precision pairing is:

- `4_DISTANCES_COVMAT/DES-Dovekie_HD.csv`
  - Git blob SHA: `f80ec4e2795edcbf3442f460c539bea56226027a`
- `4_DISTANCES_COVMAT/STAT+SYS.npz`
  - Git blob SHA: `4289666487f427782ec81c327ae7f7741f0f5fe5`
- reference likelihood: `4_DISTANCES_COVMAT/DES-Dovekie-SN_Likelihood.py`
  - Git blob SHA: `b7142093d633bf62281a2253d85ccc54db48431a`

The metadata table is not substituted for the production Hubble diagram because the upstream README explicitly warns that its ordering differs from the covariance-compatible file.

## Precision-matrix convention

The frozen upstream revision clarifies that the supplied matrix products are already inverse covariance matrices (precision matrices). The official likelihood reconstructs the symmetric precision matrix from the packed upper-triangular `.npz` representation.

RCMS therefore does not interpret `STAT+SYS.npz` as a covariance matrix requiring a second scientific inversion.

## Supernova likelihood convention

The reference likelihood:

1. uses `zHD` as the CMB-frame velocity-corrected redshift;
2. uses `zHEL` as the heliocentric redshift;
3. forms the distance modulus using both redshifts and angular-diameter distance;
4. analytically marginalizes the additive SN absolute-magnitude/intercept direction;
5. therefore does not identify H0 from DES-SN alone.

The RCMS implementation preserves these semantics symmetrically for flat LCDM and the frozen one-parameter RCMS surrogate.

## Acquisition and execution gate

The committed fetcher downloads the three frozen upstream files and verifies their Git blob SHA values before use. The P03-T1 runner was committed before any external-fit output was inspected.

P03-T1 output is valid only if all of the following pass first:

- byte/hash verification;
- Hubble-diagram/precision dimension agreement;
- precision symmetry and positive-definiteness checks;
- analytic intercept-marginalization invariance to an arbitrary additive magnitude offset.

The runner, parameter bounds, nuisance treatment, and optimization procedure must not be modified after the sign or magnitude of external `A_R` is known within this protocol.

## Scientific scope

This intake does not assume that DES-SN will reproduce the Protocol 01/02 positive region. A positive, null-compatible, or negative result is admissible. Any outcome is an external-replication result for the frozen screening surrogate only and is not validation of Resolutive Cosmology.
