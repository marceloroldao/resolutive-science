# RCMS Protocol 17 — Residual Topology and Sign Map

**Status:** PREREGISTERED / DIAGNOSTIC  
**Release line:** v0.4-dev  
**Parent evidence:** v0.3.0 — DOI `10.5281/zenodo.22643804`

## 1. Purpose

P17 is the first post-falsification diagnostic. It does **not** introduce or fit a new cosmological law. Its purpose is to map where the frozen v0.3 Lambda-CDM and logarithmic RCMS surrogate leave signed residual structure across redshift and BAO observable channel.

The frozen RCMS surrogate remains

\[
E^2(z)=\Omega_m(1+z)^3+(1-\Omega_m)+A_R\ln(1+z).
\]

No response-dependent modification is permitted.

## 2. Frozen stage-A datasets

P17-A uses only BAO datasets for which the repository already contains or can reproducibly acquire the full measurement vector and covariance used in the v0.3 line:

1. **DESI DR2 BAO** — 13-observable vector from the frozen repository files used by P13;
2. **SDSS-III BOSS DR12 BAO consensus** — six-observable held-out vector from the frozen upstream revision used by P16.

This stage is intentionally narrower than the full v0.3 family set. Supernova and H(z) residual topology may be added later only with equally explicit frozen likelihood/data provenance. P17-A must not synthesize pseudo-residuals from family-level summary amplitudes.

## 3. Frozen model states

P17-A compares each dataset under the same model/likelihood conventions used in v0.3.

### DESI DR2

Recompute the full-covariance P13 baseline fits using the unchanged bounds and nuisance profiling:

- Lambda-CDM: `A_R = 0`;
- RCMS: `A_R in [-1,1]`, step `0.01`, with `Omega_m` and the global BAO scale profiled as in P13.

The run must close to the published P13 baseline to numerical tolerance before residuals are accepted.

### BOSS DR12

Recompute the P16 optimized likelihood using the frozen upstream revision, checksums, `r_d,fid=147.78 Mpc`, bounds, and nuisance convention:

- Lambda-CDM: `A_R = 0`;
- RCMS: the frozen P16 primary-domain fit, `A_R in [-1,1]`, step `0.005`.

The run must reproduce P16-T0 and the published boundary-limited P16-T1 result before residuals are accepted. The `A_R` bound is not widened.

## 4. Residual definitions

For each measurement `i`, define the native residual

\[
r_i = d_i-m_i.
\]

Report two diagnostics.

### 4.1 Marginally standardized residual

\[
s_i = \frac{d_i-m_i}{\sqrt{C_{ii}}}.
\]

This is easy to interpret per observable but does not remove covariance.

### 4.2 Covariance-whitened residual

With `C = L L^T` from a Cholesky factorization,

\[
w=L^{-1}(d-m).
\]

Then `sum(w_i^2)=chi2` up to floating-point tolerance. Whitened components are diagnostic coordinates, not independent physical observables.

## 5. Canonical channel sign

DESI radial measurements are `DH_over_rs`; their native residual sign is already in distance orientation.

BOSS DR12 radial measurements are `bao_Hz_rs`. Because `H` and `D_H=c/H` move in opposite directions, P17 defines a **canonical radial sign** for cross-survey sign maps by multiplying the BOSS `bao_Hz_rs` standardized residual by `-1`.

Transverse/volume observables retain their native sign.

This sign conversion is only for cross-survey qualitative channel comparison. Native residuals and whitened residuals are always retained unchanged in the machine-readable output.

## 6. Frozen summary diagnostics

For each model and dataset report:

- total chi-square;
- residual row for every observable: survey, redshift, kind, data, prediction, native residual, marginal sigma, standardized residual, canonical channel sign, whitened residual;
- mean canonical standardized residual for radial channels;
- mean canonical standardized residual for transverse/volume channels;
- radial-minus-transverse canonical mean gap;
- low-z versus high-z canonical mean residual, splitting each survey at its median unique redshift;
- maximum absolute standardized residual;
- maximum absolute whitened residual.

Also report the RCMS-minus-Lambda-CDM change in each row's absolute standardized residual.

## 7. Diagnostic classification

P17 is diagnostic, not a hypothesis test. The following labels are frozen before execution.

### `CHANNEL_ORGANIZED_TENSION`

Assigned when, in either survey under RCMS, the absolute radial-minus-transverse canonical mean gap is at least `0.50` marginal sigma **and** the two channel means have opposite signs.

### `REDSHIFT_ORGANIZED_TENSION`

Assigned when the channel criterion above is not met, but in either survey under RCMS the absolute low-z minus high-z canonical mean gap is at least `0.50` marginal sigma **and** the two redshift-bin means have opposite signs.

### `DIFFUSE_RESIDUAL_STRUCTURE`

Assigned when neither organized criterion is met and all fits close numerically.

### `P17_INVALID`

Assigned if dataset checksums/covariances fail, the v0.3 likelihood closure fails, or residual chi-square reconstruction fails.

These labels do not establish a physical cause.

## 8. Non-negotiable rules

- No new free parameter.
- No widened P16 bound.
- No deletion of the BOSS sign failure/boundary outcome.
- No dataset-specific correction term.
- No interpretation of whitened coordinates as independent physical measurements.
- Any later model proposal must wait for P18–P20 and must not be retroactively counted as part of P17.

## 9. Scientific meaning

A channel-organized map would strengthen the case that the v0.3 amplitude heterogeneity is tied to radial/transverse structure rather than a single universal scalar deformation. A redshift-organized map would motivate locality/change-point diagnostics in P19. A diffuse map would weaken both narratives. None of these outcomes validates Resolutive Physics.
