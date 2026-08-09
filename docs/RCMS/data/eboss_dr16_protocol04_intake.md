# RCMS Protocol 04 — eBOSS DR16 intake

**Status:** Frozen external multi-redshift intake before P04-T0 execution  
**Protocol:** RCMS Protocol 04 — Independent Shape Replication  
**Purpose:** Provide an external BAO shape dataset with multiple redshifts, distinct from DESI DR2 and from the single-point DES Y6 BAO used in Protocol 03.

## 1. Dataset choice

The primary P04 dataset is the completed SDSS-IV/eBOSS DR16 BAO program, restricted initially to three widely separated spectroscopic tracer blocks:

1. **LRG** at effective redshift `z_eff = 0.698`;
2. **QSO** at effective redshift `z_eff = 1.480`;
3. **Ly-alpha forest + quasar cross-correlation** at effective redshift `z_eff = 2.33`.

The ELG block near `z_eff = 0.845` is reserved for a later robustness addition because its redshift support overlaps substantially with the LRG sample. No DESI DR2 measurement enters the primary Protocol 04 statistic.

## 2. Frozen observables

### P04-DATA-LRG

Primary BAO-only observables from the completed DR16 CMASS+eBOSS LRG Fourier-space analysis:

- `D_M / r_d = 17.8637`
- `D_H / r_d = 19.3033`
- covariance

```text
C_LRG = 1e-2 * [[13.9254, -7.35600],
                [-7.35600, 30.8339]]
```

These are taken from the published BAO-only data vector and covariance matrix including the full systematic budget.

### P04-DATA-QSO

Primary BAO-only consensus observables at `z_eff = 1.480`:

- `D_M / r_d = 30.69 +/- 0.80`
- `D_H / r_d = 13.26 +/- 0.55`

P04-T0 shall acquire and freeze the associated published covariance before any RCMS fit is accepted. If the exact covariance cannot be acquired and validated, this block shall not be approximated as independent diagonal errors in the production statistic.

### P04-DATA-LYA

Primary combined Ly-alpha auto/cross BAO observables at `z_eff = 2.33`:

- `D_M / r_d = 37.5 +/- 1.1`
- `D_H / r_d = 8.99 +/- 0.19`

The upstream analysis publishes non-Gaussian Delta-chi-squared surfaces. P04-T0 shall prefer the public likelihood surface over a Gaussian approximation. If the likelihood surface cannot be acquired and validated, this block shall remain unavailable rather than be silently diagonalized.

## 3. Scale nuisance and identifiability

Protocol 04 preserves a free global BAO scale nuisance

```text
q = c / (H0 * r_d)
```

with no CMB or SH0ES calibration. Because the dataset spans multiple redshifts and includes both transverse and radial information, P04-T0 must demonstrate numerically that profiling `q` does **not** make all admissible late-time shapes exactly degenerate.

The identifiability gate fails if the profiled likelihood is flat in `A_R` within numerical tolerance.

## 4. P04-T0 acceptance gates

Before any RCMS result is read or reported, the pipeline must:

1. freeze exact upstream files/revisions or publication tables used for every active block;
2. reproduce the declared LCDM reference likelihood within a documented tolerance;
3. verify positive-definiteness and observable ordering for each covariance used;
4. verify that the global scale nuisance is treated identically in LCDM and RCMS;
5. demonstrate non-zero shape information after profiling the scale;
6. exclude any block whose covariance/likelihood cannot be reproduced without an undocumented approximation.

Only after these gates pass may P04-T1 expose the fitted `A_R` value.

## 5. Independence and scope

The P04 primary statistic shall contain no Pantheon+, DES-SN5YR, DESI DR2, DES Y6 single-point BAO, CMB, or SH0ES contribution. Protocols 01–03 parameter regions may be used only for post-fit directional comparison, never as priors or calibration targets.

## 6. Scientific status

This intake defines an external observational test of the frozen one-parameter phenomenological RCMS surrogate. It does not assert that the eBOSS measurements validate Resolutive Cosmology, and it preserves null, negative, or non-identifiable outcomes as valid scientific results.
