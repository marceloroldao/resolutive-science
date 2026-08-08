# RCMS Protocol 01 — Low-Redshift Observational Outcome

**Protocol:** `docs/RCMS/protocols/01_low_redshift_observational_preregistration.md`  
**Status:** Completed observational screening protocol  
**Scientific status:** Inconclusive model-selection result; no empirical validation claim  
**Model under test:** frozen one-parameter effective RCMS screening surrogate

---

## 1. Purpose

Protocol 01 tested a single pre-registered late-time RCMS screening deformation against flat \(\Lambda\)CDM using real low-redshift observations. The tested deformation was frozen before observational fitting:

\[
H_{\mathrm{eff}}^2(z)=H_{\Lambda\mathrm{CDM}}^2(z)+H_0^2 A_R\ln(1+z).
\]

The parameter \(A_R\) is an effective low-signal surrogate derived from the RC-E020 family. It is not asserted to be a fundamental resolutive law.

The protocol was designed to allow three scientifically acceptable outcomes: preference for RCMS, preference for the reference model, or no preference. No post-hoc change to the deformation was permitted after real-data residuals were inspected.

## 2. Observational inputs and nuisance treatment

### 2.1 Cosmic chronometers — \(H(z)\)

The production sample used the exact 15-point Moresco BC03 table compatible with the reproduced public covariance prescription. The covariance was validated for symmetry, positive definiteness, inverse consistency, and agreement with the published determinant.

Parameters:

- shared shape parameter: \(\Omega_m\);
- profiled absolute expansion scale: \(H_0\);
- RCMS-only parameter: \(A_R\).

### 2.2 Pantheon+ Type Ia supernovae

The Pantheon+ stage used the frozen Cobaya `PantheonPlus` likelihood semantics without SH0ES:

- fixed \(z_{\rm CMB}>0.01\) mask;
- 1590 retained supernovae;
- exact full masked covariance;
- no Cepheid-host distance override;
- one additive absolute-magnitude/intercept direction analytically marginalized in both models.

Therefore this stage tests relative distance-redshift geometry and does not independently measure \(H_0\).

### 2.3 DESI DR2 BAO

The BAO stage used the public DESI DR2 all-tracer Gaussian BAO vector and full 13×13 covariance with \(D_V/r_d\), \(D_M/r_d\), and \(D_H/r_d\) measurements through \(z=2.33\).

Without a CMB or external sound-horizon prior, BAO does not separately identify \(H_0\) and \(r_d\). The exactly equivalent common scale

\[
q=\frac{c}{H_0 r_d}
\]

was therefore profiled as a nuisance parameter.

No CMB, SH0ES, RSD, or external \(r_d\) prior entered Protocol 01.

## 3. Model-selection convention

The reported differences use

\[
\Delta X = X_{\Lambda\mathrm{CDM}}-X_{\mathrm{RCMS}}.
\]

Thus positive \(\Delta\chi^2\) indicates a lower best-fit chi-square for RCMS. Positive \(\Delta\mathrm{AIC}\) or \(\Delta\mathrm{BIC}\) indicates preference for RCMS under the corresponding information criterion.

The protocol does not promote a likelihood improvement to a model-selection claim when the pre-registered criteria conflict.

## 4. Complete Protocol 01 results

| Stage | Best \(A_R\) | \(\Delta\chi^2\le1\) profile interval | \(\Delta\chi^2\) | \(\Delta\mathrm{AIC}\) | \(\Delta\mathrm{BIC}\) | Protocol decision |
|---|---:|---:|---:|---:|---:|---|
| \(H(z)\) | -1.2800 | [-2.58, 0.54] | 0.5526 | -1.4474 | -2.1555 | No preference |
| Pantheon+ SN | 0.2139 | [-0.1087, 0.5274] | 0.4438 | -1.5562 | -6.9277 | No preference |
| DESI DR2 BAO | 0.2100 | [0.0300, 0.4000] | 1.3058 | -0.6942 | -1.2592 | No preference |
| \(H(z)+\)SN | 0.1376 | [-0.1569, 0.4256] | 0.2209 | -1.7791 | -7.1600 | No preference |
| \(H(z)+\)BAO | 0.2027 | [0.0206, 0.3973] | 1.2483 | -0.7517 | -2.0839 | Reference favored by AIC/BIC |
| SN+BAO | 0.1896 | [0.1011, 0.2794] | 4.6734 | +2.6734 | -2.7062 | No preference — AIC/BIC conflict |
| \(H(z)+\)SN+BAO | 0.1870 | [0.0987, 0.2768] | 4.5595 | +2.5595 | -2.8294 | No preference — AIC/BIC conflict |

No reported best fit contacted the frozen parameter boundaries.

## 5. Full low-redshift combination

For the final \(H(z)+\)Pantheon+ + DESI DR2 BAO combination:

### Flat \(\Lambda\)CDM

\[
\chi^2=1422.383648,
\qquad
\Omega_m=0.304474,
\]

with profiled nuisance values

\[
H_0=68.398996\;\mathrm{km\,s^{-1}\,Mpc^{-1}},
\qquad
q=29.684486.
\]

Probe contributions were

\[
\chi_H^2=6.243289,
\qquad
\chi_{\rm SN}^2=1405.224151,
\qquad
\chi_{\rm BAO}^2=10.916208.
\]

### Effective RCMS screening model

\[
\chi^2=1417.824120,
\qquad
\Omega_m=0.298908,
\qquad
A_R=0.187021,
\]

with

\[
H_0=67.448786\;\mathrm{km\,s^{-1}\,Mpc^{-1}},
\qquad
q=30.050086.
\]

Probe contributions were

\[
\chi_H^2=6.356692,
\qquad
\chi_{\rm SN}^2=1402.487269,
\qquad
\chi_{\rm BAO}^2=8.980158.
\]

The profile interval was

\[
0.098671\le A_R\le0.276779
\qquad(\Delta\chi^2\le1).
\]

The raw likelihood improvement was

\[
\Delta\chi^2=4.559528,
\]

but the information criteria disagreed:

\[
\Delta\mathrm{AIC}=+2.559528,
\qquad
\Delta\mathrm{BIC}=-2.829418.
\]

Under the frozen Protocol 01 decision rule, this disagreement is classified **NO PREFERENCE**.

## 6. Interpretation

Protocol 01 does not provide a robust model-selection preference for the effective RCMS surrogate.

Several distinctions are important:

1. **Likelihood preference is not model-selection preference.** The SN+BAO and full combinations achieve a lower chi-square with \(A_R\approx0.19\), but the additional parameter is treated differently by AIC and BIC at the available sample size.
2. **A profile interval excluding zero is not by itself evidence that RCMS is the preferred cosmological model.** Parameter estimation is conditional on the tested model family; model selection additionally penalizes flexibility and compares alternatives.
3. **The individual probes do not independently establish the same effect at decisive strength.** H(z) and Pantheon+ individually include \(A_R=0\) within their \(\Delta\chi^2\le1\) profiles, while BAO shows only a modest raw improvement that is rejected by AIC/BIC complexity accounting.
4. **No post-hoc deformation was introduced.** The same one-parameter function was retained through all individual and combined analyses.
5. **Protocol completion is not validation of Resolutive Cosmology.** RCMS remains a proposed and computationally tested framework.

The scientifically conservative summary is therefore:

\[
\boxed{\text{Protocol 01 outcome: inconclusive / no robust model preference}}
\]

The positive \(A_R\) region in the SN+BAO and full fits is a feature suitable for independent replication and robustness testing, not a validated discovery claim.

## 7. Traceability

| Stage | Repository record |
|---|---|
| Pre-registration | PR #34 |
| Cosmic-chronometer covariance and H(z) result | PR #36 |
| Pantheon+ intake, likelihood, and SN result | PR #37 |
| DESI DR2 BAO result | PR #38 |
| H(z)+Pantheon+ joint result | PR #39 |
| H+BAO, SN+BAO, and full combination | PR #40 |

Each observational result was generated by a versioned deterministic runner. Pantheon+ external bytes were cryptographically verified before likelihood evaluation. The three final combinations in PR #40 were implemented together before any of their results were revealed.

## 8. Next scientific stage

No new RCMS deformation should be introduced as a reaction to Protocol 01 residuals.

A separate **Protocol 02** should be pre-registered before additional observational calculations. Its purpose should be robustness and independent replication of the frozen Protocol 01 signal region rather than optimization of the model.

Appropriate Protocol 02 targets include:

- an independent supernova compilation or independently implemented Pantheon+ likelihood;
- an alternative covariance-compatible cosmic-chronometer analysis;
- DESI BAO tracer/redshift ablations declared before inspection;
- null calibration of the full model-selection pipeline by Monte Carlo;
- residual and posterior-predictive diagnostics;
- independent software reproduction of the full low-redshift fit;
- sensitivity to explicitly predeclared nuisance and numerical choices.

CMB should remain outside this late-time protocol until RCMS specifies a consistent high-redshift/early-universe evolution law and the required sound-horizon physics.
