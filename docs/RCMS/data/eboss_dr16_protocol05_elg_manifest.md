# RCMS Protocol 05 — eBOSS DR16 ELG frozen manifest

**Status:** Frozen before P05-T0 execution  
**Protocol:** RCMS Protocol 05 — LRG-Dependence Challenge  
**Upstream likelihood implementation:** `CobayaSampler/cobaya@v3.6.2`  
**Upstream BAO data release:** `CobayaSampler/bao_data@v2.6`

## Frozen challenge statistic

Protocol 05 replaces the Protocol 04 LRG block with the eBOSS DR16 ELG BAO-only likelihood while retaining the Protocol 04 QSO and Lyman-alpha auto blocks.

The frozen primary challenge is therefore:

1. ELG BAO-only at `z_eff = 0.845`, observable `DV_over_rs`;
2. QSO at `z_eff = 1.48`, observables `DM_over_rs` and `DH_over_rs`;
3. Lyman-alpha auto at `z_eff = 2.334`, using the same 2D probability grid frozen in Protocol 04.

The original Protocol 04 LRG block is excluded by design and is not reweighted.

## Frozen ELG upstream definition

Cobaya `v3.6.2` defines `bao.sdss_dr16_bao_elg` with:

- grid file: `sdss_DR16_ELG_BAO_DVtable.txt`;
- observable: `DV_over_rs`;
- redshift: `0.845`;
- likelihood convention: spline interpolation of `log(probability)` from the second grid column.

The ELG data file is frozen to `CobayaSampler/bao_data@v2.6` with Git blob SHA:

`25e8c0f773174ed3d05dcfad0929f268d90c2019`

## Frozen distance prediction

For flat Lambda-CDM,

\[
E(z)=\sqrt{\Omega_m(1+z)^3+1-\Omega_m},
\]

\[
\frac{D_M}{r_d}=q\int_0^z\frac{dz'}{E(z')},
\qquad
\frac{D_H}{r_d}=\frac{q}{E(z)},
\qquad
q=\frac{c}{H_0r_d}.
\]

The isotropic ELG observable is

\[
\frac{D_V(z)}{r_d}=
\left[z\left(\frac{D_M}{r_d}\right)^2\left(\frac{D_H}{r_d}\right)\right]^{1/3}.
\]

## P05-T0 gates

Before any `A_R` evaluation, P05-T0 must:

1. verify the ELG data blob SHA;
2. reproduce the one-dimensional log-probability likelihood convention;
3. retain the frozen QSO and Lyman-alpha conventions from Protocol 04;
4. obtain a finite interior Lambda-CDM optimum in `(Omega_m, q)`;
5. demonstrate nonzero profiled shape information in `Omega_m`;
6. print `RCMS_PARAMETER_EVALUATED=NO` and no `A_R` value.

Passing P05-T0 establishes only acquisition integrity, likelihood implementation, and challenge-statistic identifiability. It is not evidence for RCMS.
