# RCMS Protocol 11 — Equal-Complexity Functional Controls

**Status:** PREREGISTERED — outcome not inspected  
**Release line:** v0.3-dev  
**RSMS compatibility:** RSMS-1.0-rc.1  
**Parent evidence:** v0.2.0 + P09 calibration + P10 injection/recovery

## 1. Purpose

Protocol 11 tests whether the frozen RCMS logarithmic deformation carries discriminating information beyond a generic smooth one-parameter deformation of the same expansion channel.

The frozen RCMS surrogate is

\[
E^2(z)=\Omega_m(1+z)^3+1-\Omega_m+A\,f(z),
\]

with RCMS

\[
f_{\log}(z)=\ln(1+z).
\]

P11 does not change the RCMS equation. It compares that already-frozen shape against preregistered controls with exactly one additional amplitude parameter each.

## 2. Dataset and nuisance structure

Use exactly the frozen DESI DR2 BAO structure already used by the v0.2/P09/P10 line:

- `data/rcms/desi_dr2_bao_all_mean.txt`;
- `data/rcms/desi_dr2_bao_all_cov.txt`;
- all 13 observables and their published ordering;
- full 13x13 covariance;
- observable kinds `DV_over_rs`, `DM_over_rs`, `DH_over_rs`;
- `q=c/(H0*r_d)` profiled analytically;
- `0.05 <= Omega_m <= 0.60`;
- no CMB, SH0ES, or added calibration.

No dataset may be removed or reweighted after outcome inspection.

## 3. Frozen control functions

All functions are required to satisfy

\[
f(0)=0,\qquad f(1)=\ln2,
\]

so the fitted amplitude has the same additive interpretation at the fixed pivot `z*=1`.

The four preregistered one-parameter shapes are:

### RCMS logarithmic

\[
f_{\log}(z)=\ln(1+z).
\]

### Linear control

\[
f_{\rm lin}(z)=(\ln2)z.
\]

### Saturating rational control

\[
f_{\rm sat}(z)=2(\ln2)\frac{z}{1+z}.
\]

### Square-root control

\[
f_{\sqrt{}}(z)=\ln2\,\frac{\sqrt{1+z}-1}{\sqrt2-1}.
\]

These controls were selected before P11 output inspection because they span three qualitatively different smooth curvatures around the logarithmic form: faster-than-log growth, stronger saturation, and intermediate concave growth. No control may be added, removed, or renormalized after inspecting P11 results.

## 4. Frozen estimator

For each shape independently:

- amplitude interval: `A in [-5,+5]`;
- amplitude grid spacing: `0.01`;
- `Omega_m` is profiled continuously on `[0.05,0.60]` using the same one-dimensional minimization convention for every shape;
- `q` is profiled analytically at every `(Omega_m,A)` point;
- the same covariance inverse, quadrature, numerical tolerances, and validity checks are used for all shapes;
- Lambda-CDM is the nested `A=0` reference and is common to all four families.

Each model has the same effective parameter count (`q`, `Omega_m`, one deformation amplitude), so pairwise AIC/BIC differences among the four deformations reduce to their minimum-chi-square ordering. Null-versus-deformation AIC/BIC penalties remain reported explicitly.

## 5. Required outputs

For Lambda-CDM and each deformation report:

1. minimum chi-square;
2. best `Omega_m`;
3. best amplitude;
4. best `q`;
5. profile `Delta chi2 <= 1` amplitude interval;
6. `Delta chi2 = chi2_LCDM - chi2_model`;
7. `Delta AIC = AIC_LCDM - AIC_model`;
8. `Delta BIC = BIC_LCDM - BIC_model`;
9. boundary-contact flag;
10. ranking of the four one-parameter shapes.

Also report the chi-square gap

\[
\Delta\chi^2_{\log-ctrl}=\chi^2_{\rm best\ control}-\chi^2_{\log},
\]

which is positive when the logarithm fits better than the best control.

## 6. Preregistered classification

The shape-specific classification is frozen as follows.

### `LOG_DISCRIMINATING`

Require all of:

- logarithmic RCMS has the lowest chi-square among all four one-parameter shapes;
- `Delta chi2_log-ctrl >= 2.0` relative to the best non-log control;
- logarithmic `Delta AIC > 0` relative to Lambda-CDM;
- no amplitude or `Omega_m` boundary contact.

### `FUNCTIONALLY_NON_SPECIFIC`

Classify this if the best log/control chi-square separation has absolute magnitude `< 2.0`, regardless of which one is numerically first. This means the tested data do not discriminate the logarithmic shape from equally complex smooth alternatives at the preregistered threshold.

### `CONTROL_PREFERRED`

Classify this if a non-log control beats the logarithm by `Delta chi2 >= 2.0` and has no boundary contact.

### `NO_DEFORMATION_PREFERENCE`

If all four deformation families have `Delta AIC <= 0` relative to Lambda-CDM, record this additional release-level flag even if one shape ranks first among the deformations.

Boundary-limited cases must be explicitly reported and cannot receive `LOG_DISCRIMINATING`.

The threshold `2.0` is a preregistered discrimination convention for this falsification protocol, not a discovery significance threshold.

## 7. Falsification rule

If the logarithmic function is not discriminated from equally complex controls, the v0.3 evidence must state that the current data support at most a generic smooth deformation direction rather than a uniquely logarithmic RCMS form.

If a control is materially preferred, that outcome must be preserved and the RCMS logarithmic equation must not be modified inside P11 to recover preference.

## 8. Non-claims

P11 cannot by itself establish:

- physical validity of Resolutive Science;
- discovery of new physics;
- uniqueness of the logarithm outside the tested control set;
- independent replication, because it reuses the frozen DESI DR2 evidence structure.
