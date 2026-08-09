# RCMS Protocol 03 — DES-SN Dovekie Intake Record

**Protocol:** RCMS Protocol 03 — External Replication  
**Stage:** P03-DATA-SN  
**Status:** Frozen before P03-T1 fitting  

## 1. Upstream source

- Repository: `des-science/DES-SN5YR`
- Upstream revision: `c9a4fcafc4cbd19bd750dee47fc76194a45c181f`
- Revision date: 2026-01-28
- Upstream path: `4_DISTANCES_COVMAT/`

The upstream revision is frozen before any RCMS fit to this dataset.

## 2. Frozen files

| Role | Upstream file | Git blob SHA | Size (bytes) |
|---|---|---:|---:|
| Reference likelihood | `DES-Dovekie-SN_Likelihood.py` | `b7142093d633bf62281a2253d85ccc54db48431a` | 7,674 |
| Ordered Hubble diagram | `DES-Dovekie_HD.csv` | `f80ec4e2795edcbf3442f460c539bea56226027a` | 148,002 |
| Full statistical+systematic precision matrix product | `STAT+SYS.npz` | `4289666487f427782ec81c327ae7f7741f0f5fe5` | 6,244,951 |
| Statistical-only precision product, diagnostic only | `STATONLY.npz` | `6d8b618da9871e55a05f1bdb84b149b2e0576e0c` | 19,366 |
| Upstream usage notes | `README.md` | `d5900bc1a4a2ce345012c878c929204cef5b5c52` | 1,680 |

`DES-Dovekie_Metadata.csv` is not the production ordering source for the covariance pairing and shall not be substituted for `DES-Dovekie_HD.csv` in P03-T1.

## 3. Matrix convention

The upstream release explicitly states that the covariance products supplied in this directory are already **inverse covariance matrices / precision matrices** and that the supplied likelihood contains the code required to unpack and use them.

RCMS shall therefore not invert these products a second time.

Before fitting, the implementation shall verify:

1. the frozen upstream commit;
2. each required Git blob SHA;
3. array dimensions and ordering;
4. symmetry of the unpacked precision matrix within numerical tolerance;
5. finite likelihood evaluation on an upstream reference cosmology.

## 4. Likelihood replication requirement

Before RCMS P03-T1 is accepted, an implementation using the frozen files shall reproduce an upstream/reference DES-SN likelihood value or parameter result within a declared numerical tolerance.

Only after that replication gate passes may the same likelihood be evaluated for the frozen RCMS deformation

\[
H_{\mathrm{eff}}^2(z)=H_{\Lambda\mathrm{CDM}}^2(z)+H_0^2A_R\ln(1+z).
\]

## 5. Nuisance treatment

The absolute supernova calibration/intercept direction shall be treated identically for flat \(\Lambda\)CDM and RCMS. No SH0ES, Pantheon+, DESI DR2, CMB, or external sound-horizon information may enter P03-T1.

## 6. Scientific guardrail

This intake record freezes provenance and numerical conventions only. It contains no RCMS observational result and shall not be modified based on the sign or magnitude of the future P03-T1 best-fit \(A_R\).
