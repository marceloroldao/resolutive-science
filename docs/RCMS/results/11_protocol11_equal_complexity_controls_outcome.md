# RCMS Protocol 11 — Equal-Complexity Functional Controls Outcome

**Status:** FROZEN OUTCOME  
**Release line:** v0.3-dev  
**Classification:** `FUNCTIONALLY_NON_SPECIFIC`  
**Additional flag:** `NO_DEFORMATION_PREFERENCE=True`  
**RSMS compatibility:** RSMS-1.0-rc.1

## 1. Frozen execution

- dataset: frozen DESI DR2 13-observable BAO vector and full 13x13 covariance;
- common nuisance treatment: `q=c/(H0*r_d)` profiled analytically, `Omega_m` profiled identically;
- all four one-parameter deformation functions normalized to `f(0)=0`, `f(1)=ln(2)`;
- amplitude interval: `[-5,+5]`, step `0.01`;
- GitHub Actions run: `32588124809`;
- artifact: `rcms-protocol11-functional-controls`;
- artifact ID: `9479605468`.

## 2. Frozen results

Lambda-CDM reference:

- `chi2 = 10.271041008`;
- `Omega_m = 0.297461819`;
- `q = 29.524633401`.

| Rank | Shape | chi2 | Best A | Delta chi2 vs LCDM | Delta AIC vs LCDM | Delta BIC vs LCDM | Boundary |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | saturating | 8.686550489 | 0.220 | 1.584490519 | -0.415509481 | -0.980458839 | false |
| 2 | logarithmic RCMS | 8.965255791 | 0.210 | 1.305785217 | -0.694214783 | -1.259164141 | false |
| 3 | square-root | 9.106367409 | 0.210 | 1.164673599 | -0.835326401 | -1.400275759 | false |
| 4 | linear | 9.244829998 | 0.220 | 1.026211009 | -0.973788991 | -1.538738348 | false |

Logarithmic profile interval (`Delta chi2 <= 1`):

`A = [0.03, 0.40]`.

Best non-log control: `saturating`.

Using the preregistered definition

`Delta_chi2_log_ctrl = chi2_best_control - chi2_log`,

the result is

`Delta_chi2_log_ctrl = -0.278705302`.

The saturating control therefore fits numerically slightly better than the logarithm, but the separation is far below the preregistered absolute discrimination threshold of `2.0`.

## 3. Frozen classification

`P11_CLASSIFICATION=FUNCTIONALLY_NON_SPECIFIC`

The four equal-complexity deformations are not discriminated by the tested DESI DR2 likelihood at the preregistered threshold.

In addition, every one-parameter deformation has `Delta AIC <= 0` relative to Lambda-CDM, therefore:

`NO_DEFORMATION_PREFERENCE=True`.

## 4. Scientific interpretation

P11 falsifies the stronger claim that the current DESI DR2 evidence specifically selects the logarithmic RCMS functional form over representative equally complex smooth alternatives. In this test the data support, at most, a weak generic smooth positive deformation direction.

The positive amplitude scale remains similar across the four normalized functions (`A ~ 0.21–0.22` at the fixed `z=1` pivot), but that common direction is not evidence for uniqueness of `ln(1+z)`.

The result also does not establish model preference over Lambda-CDM because AIC and BIC favor the simpler reference for every tested one-parameter deformation.

This negative/discriminating result is permanent evidence for v0.3 and must not be removed or used to retune the logarithmic RCMS equation.

## 5. Non-claims

P11 does not test every mathematically possible control function, does not provide an independent dataset replication, and does not invalidate the conditional mathematical result of P08. It shows only that the tested observational likelihood does not distinguish the RCMS logarithm from the preregistered equal-complexity controls.
