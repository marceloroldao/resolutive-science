# RCMS DESI DR2 BAO — Provenance Record

**Dataset role:** Protocol 01 BAO-alone stage  
**Status:** Frozen before formal BAO interpretation  
**Source implementation:** `CobayaSampler/cobaya` commit `b76b6fed2a6c8c5594c6f92d5058bef10079746a`  
**Source data:** `CobayaSampler/bao_data` commit `bb0c1c9009dc76d1391300e169e8df38fd1096db`

The frozen Cobaya likelihood is `bao.desi_dr2.desi_bao_all`. Its YAML points to the all-tracer DR2 Gaussian BAO measurement and covariance products with `rs_fid = 1 Mpc`.

Frozen upstream blobs:

- measurements: `8aff444fdb42c0946342aa0011ab287eda097c4c`;
- covariance: `fd8e5697ab61379b07b52efb781ea6713417a4d9`.

The measurement vector has 13 entries: one `DV/rs` datum at z=0.295 and paired `DM/rs`, `DH/rs` measurements through z=2.33. The covariance is 13x13 and preserves the published within-bin correlations.

DESI's public data support confirmed in July 2026 that the measurement and covariance files in the current Cobaya `bao.desi_dr2.desi_bao_all` likelihood are byte-identical to those used by the historical external likelihood that generated the public DR2 cosmology chains.

## RCMS treatment

For BAO-alone, the sound horizon is not imported from CMB physics. The likelihood therefore profiles the common scale combination

`q = c / (H0 * r_d)`

because all three BAO observables scale linearly with q for a fixed late-time expansion shape. This is algebraically equivalent to leaving `H0` and `r_d` free in BAO-only data, where they are not separately identifiable.

The shape parameters are `Omega_m` for flat Lambda-CDM and `(Omega_m, A_R)` for the frozen Protocol 01 RCMS surrogate. The RCMS model has exactly one additional identifiable shape parameter relative to the reference.

No CMB prior on `r_d`, no SH0ES prior on `H0`, and no RSD information is included in this stage.
