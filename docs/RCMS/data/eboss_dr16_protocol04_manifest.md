# RCMS Protocol 04 — eBOSS DR16 frozen data manifest

**Status:** Frozen before P04-T0 execution  
**Protocol:** RCMS Protocol 04 — Independent Shape Replication  
**Upstream likelihood implementation:** `CobayaSampler/cobaya@v3.6.2`  
**Upstream BAO data release:** `CobayaSampler/bao_data@v2.6`

## Primary shape dataset

Protocol 04 uses the following eBOSS DR16 BAO-only blocks as its first independent multi-redshift shape dataset:

1. LRG at `z_eff = 0.698`, using `DM_over_rs` and `DH_over_rs` with the published covariance;
2. QSO at `z_eff = 1.48`, using `DM_over_rs` and `DH_over_rs` with the published covariance;
3. Lyman-alpha auto-correlation at `z_eff = 2.334`, using the published two-dimensional probability grid in `(DM_over_rs, DH_over_rs)`.

The Lyman-alpha cross-correlation with quasars (`LYxQSO`) is frozen at the same time but is **reserved for robustness** and is not added to the primary statistic. This avoids treating the auto- and cross-correlation likelihoods as independent without an explicit joint covariance.

The eBOSS ELG block remains reserved for robustness because its redshift window overlaps the LRG window.

## Frozen upstream files

| Role | File | Git blob SHA |
|---|---|---|
| LRG measurement | `sdss_DR16_LRG_BAO_DMDH.dat` | `122f8dd418d427eef891ea0512695e32002ee876` |
| LRG covariance | `sdss_DR16_LRG_BAO_DMDH_covtot.txt` | `76aef07f03e2352dbf6ea444c0f577d28d1c70a5` |
| QSO measurement | `sdss_DR16_QSO_BAO_DMDH.txt` | `3e1e5b7cc7e739534c464e59ffc0fa2e21531994` |
| QSO covariance | `sdss_DR16_QSO_BAO_DMDH_covtot.txt` | `4add5e7e9ebadf336258469872a994a5d0df2bb3` |
| Lyman-alpha auto probability grid | `sdss_DR16_LYAUTO_BAO_DMDHgrid.txt` | `266086971a82e0c64750e5853d77962fb283253f` |
| Lyman-alpha x QSO probability grid, robustness only | `sdss_DR16_LYxQSO_BAO_DMDHgrid.txt` | `e27a260556b1f4a658aad78090fd0cde7f29e056` |

Cobaya v3.6.2 declares `CobayaSampler/bao_data` release `v2.6` as the install source for BAO likelihood data. Its DR16 LRG and QSO likelihoods use the measurement/covariance files above. Its Lyman-alpha likelihood uses the grid by interpolating the logarithm of the third column as a two-dimensional log-likelihood surface.

## Frozen nuisance treatment

No CMB, SH0ES, DESI, Pantheon+, or DES-SN calibration is imported. The global BAO scale remains

\[
q = \frac{c}{H_0 r_d}
\]

and is profiled symmetrically in all models.

For flat Lambda-CDM the late-time shape evaluated in P04-T0 is

\[
E(z)=\sqrt{\Omega_m(1+z)^3+1-\Omega_m},
\]

\[
\frac{D_M(z)}{r_d}=q\int_0^z\frac{dz'}{E(z')},
\qquad
\frac{D_H(z)}{r_d}=\frac{q}{E(z)}.
\]

## P04-T0 gates

Before any RCMS parameter is evaluated, P04-T0 must:

1. verify every downloaded upstream file by Git blob SHA;
2. reproduce the Gaussian LRG/QSO likelihood convention and the Cobaya logarithmic Lyman-alpha grid convention;
3. obtain a finite interior flat-Lambda-CDM optimum in `(Omega_m, q)`;
4. demonstrate non-flat profile likelihood in `Omega_m` after `q` is re-profiled;
5. report only Lambda-CDM and identifiability diagnostics.

`A_R` is not evaluated or printed by P04-T0.

## Scientific status

This manifest freezes data selection and nuisance treatment before the Protocol 04 RCMS fit is exposed. Passing P04-T0 establishes only data integrity, baseline likelihood reproducibility, and shape identifiability. It is not evidence for RCMS.
