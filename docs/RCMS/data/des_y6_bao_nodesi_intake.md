# RCMS Protocol 03 — DES Y6 DESI-independent angular BAO intake

**Status:** Frozen before P03-T2 execution  
**Protocol:** RCMS Protocol 03  
**Primary split:** `DR1tiles_noDESI`

## Upstream provenance

The DESI-independent angular BAO analysis is published as Mena-Fernández et al., *Dark Energy Survey: DESI-Independent Angular BAO Measurement*, arXiv:2601.14864v2 / Phys. Rev. D 113, 123521 (2026).

The associated public fitting-code repository is:

- repository: `juanejo95/BAOfit_wtheta`;
- frozen revision: `2076ff5d0b5eeb39f1df9a3d35213c80beb19c4a`;
- frozen tree: `3c2a72de0befcca033fbac97ab424e2d24209cea`.

The paper defines `DR1tiles_noDESI` by removing the DESI DR1 tile footprint from the DES Y6 BAO mask. This is the split designed for combinations with DESI DR1/DR2 and is the split adopted by the paper for cosmological inference.

## Frozen compressed observable

The upstream fiducial result adopted for cosmology is

\[
z_{\rm eff}=0.851,
\qquad
\alpha=0.9690\pm0.0296.
\]

The uncertainty includes the BAO systematic contribution reported by the upstream analysis.

The paper defines

\[
\alpha =
\frac{D_M(z)/r_d}{D_M^{\rm fid}(z)/r_d^{\rm fid}}.
\]

The exact record used by RCMS is stored in `data/rcms/des_y6_bao_nodesi_alpha_v1.csv`.

## Public raw-data note

The frozen `BAOfit_wtheta` code expects a dataset-local `wtheta/wtheta.zip` for the angular-correlation-function likelihood. At the frozen public revision, the repository tree exposes the `DR1tiles_noDESI` n(z) and CosmoLike covariance products but does not expose a corresponding dataset-local `wtheta.zip` in that folder.

RCMS therefore does **not** reconstruct or invent a missing angular data vector. Protocol 03 uses the published compressed BAO likelihood quantity above, which is the quantity explicitly adopted by the upstream paper for cosmological inference.

## Identifiability with a free sound-horizon/global scale

Protocol 03 pre-registered that any sound-horizon or global scale nuisance must be treated symmetrically between flat LCDM and RCMS, with no CMB or SH0ES prior added after inspecting external results.

For a flat late-time expansion model,

\[
\frac{D_M(z)}{r_d}
=
\frac{c}{H_0 r_d}
\int_0^z \frac{dz'}{E(z')}.
\]

With only one compressed transverse BAO datum and a free global scale

\[
q\equiv \frac{c}{H_0r_d},
\]

any admissible late-time shape can profile q to reproduce that single datum. Consequently, P03-T2 BAO-alone cannot identify \(A_R\) without importing an external calibration or a second independent BAO distance/redshift point.

This is an identifiability result, not a null result and not evidence for either model.

## P03-T2 rule

The P03-T2 runner shall:

1. reproduce the frozen compressed measurement metadata;
2. verify the single-point scale degeneracy numerically for multiple admissible \((\Omega_m,A_R)\) shapes;
3. report `P03_T2_IDENTIFIABILITY=SCALE_DEGENERATE_SINGLE_TRANSVERSE_BAO`;
4. not report a model-selection preference from BAO-alone.

The external joint stage P03-T3 must preserve the same free scale nuisance. If the single BAO point adds no shape information after profiling the scale, this must be reported explicitly rather than hidden by imposing a post-hoc early-Universe prior.
