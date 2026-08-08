# RCMS Pantheon+ SN-alone Dataset v1 — Provenance Record

**Dataset ID:** `RCMS-DATA-PANTHEONPLUS-v1`  
**Protocol:** `docs/RCMS/protocols/01_low_redshift_observational_preregistration.md`  
**Stage:** Type Ia supernovae alone  
**Status:** source frozen; production fit blocked until exact upstream files are locally verified

## Scientific role

Protocol 01 uses supernovae as a relative luminosity-distance probe. This stage shall not import a SH0ES/Cepheid absolute calibration of H0. The absolute supernova magnitude / intercept is marginalized symmetrically in flat Lambda-CDM and RCMS.

## Frozen data source

The data source is the public Cobaya supernova-data repository, which supplies the Pantheon+ files used by its built-in `sn.pantheonplus` likelihood.

- repository: `CobayaSampler/sn_data`
- frozen commit: `61d96434cafc2770928322c38e5a750e686368ae`
- directory: `PantheonPlus/`
- data file: `Pantheon+SH0ES.dat`
- covariance file: `Pantheon+SH0ES_STAT+SYS.cov`
- config file: `PantheonPlus/config.dataset`

Frozen Git blob identities from the source repository:

- `Pantheon+SH0ES.dat`: blob `cce857db0c15e9ce7a0e0ce77452b6ff62af969a`, source size 579283 bytes;
- `Pantheon+SH0ES_STAT+SYS.cov`: blob `d1a1498154e7ba826df14bdbef35ebcb7f5efba1`, source size 33284960 bytes;
- `config.dataset`: blob `40fa08ad421564ff1c199524dd027a0184197a63`.

The upstream covariance file declares dimension 1701 before the flattened matrix entries.

## Frozen likelihood implementation

The likelihood treatment is frozen to the behavior of Cobaya's **PantheonPlus without SH0ES** implementation.

- repository: `CobayaSampler/cobaya`
- frozen commit: `b76b6fed2a6c8c5594c6f92d5058bef10079746a`
- implementation: `cobaya/likelihoods/sn/pantheonplus.py`
- settings: `cobaya/likelihoods/sn/pantheonplus.yaml`

The relevant behavior is:

1. read `m_b_corr`, `zHD`, and `zHEL` as magnitude, CMB-frame redshift, and heliocentric redshift;
2. apply the fixed mask `zCMB > 0.01`;
3. apply the same mask to the full covariance matrix;
4. invert the masked covariance;
5. because `use_abs_mag: False`, analytically marginalize the single absolute-magnitude/intercept direction by projecting the inverse covariance orthogonally to a vector of ones;
6. evaluate the quadratic magnitude residual with that projected inverse covariance.

The separate Cobaya `PantheonPlusShoes` likelihood is **not** used in this stage. That implementation explicitly retains calibrator rows and replaces their theoretical luminosity distances by Cepheid-host distances; doing so would introduce an absolute-distance calibration that is outside the SN-alone stage of Protocol 01.

## Covariance-source caution

The physical source files retain the historical `SH0ES` filename. RCMS does not infer the likelihood definition from the filename. It follows the frozen, explicit Cobaya `PantheonPlus` implementation above.

There is an open issue in the upstream PantheonPlusSH0ES data-release repository concerning interpretation of the diagonal uncertainties and the combined covariance. For this reason RCMS shall not reconstruct, edit, or diagonalize the matrix ad hoc. The exact upstream bytes and the established no-SH0ES likelihood mask/marginalization must be reproduced before a production result is accepted.

## Production gate

The SN-alone production fit remains blocked until the acquisition script has verified the exact Git blob identity of both upstream files and the following structural checks pass:

- data file has 1701 rows after its header;
- covariance declares dimension 1701 and has exactly 1701^2 numerical entries;
- the `zCMB > 0.01` mask is applied identically to data and both covariance axes;
- masked covariance is symmetric and positive definite within numerical tolerance;
- intercept marginalization reproduces the frozen Cobaya projection;
- no Cepheid-distance term or calibrator override is used.

## Frozen model accounting

For SN-alone, H0 is exactly degenerate with the additive absolute-magnitude/intercept direction and is therefore not interpreted as an independently measured parameter. The comparison uses:

- common shape parameter: `Omega_m` under flat late-time Lambda-CDM background;
- common analytically marginalized intercept;
- RCMS-only parameter: `A_R`.

The same RCMS functional form frozen in Protocol 01 is used. No SN-specific RCMS deformation is allowed.
