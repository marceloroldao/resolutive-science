# RCMS Protocol 06 — DESI DR2 External Replication Outcome

**Final classification:** `DESI_DR2_POSITIVE_DIRECTIONAL`  
**RSMS compatibility:** RSMS-1.0  

## 1. Frozen test

Protocol 06 tested the unchanged one-parameter RCMS cosmological surrogate

\[
E_{\rm RCMS}^2(z)=\Omega_m(1+z)^3+(1-\Omega_m)+A_R\ln(1+z)
\]

against the public DESI DR2 combined BAO all-tracer likelihood, using the same global scale nuisance

\[
q=c/(H_0r_d)
\]

under both Lambda-CDM and RCMS.

No external calibration or response-dependent model change was introduced.

## 2. P06-T0 gate

P06-T0 passed before any RCMS parameter was exposed.

- measurements: 13;
- redshift range: `0.295 <= z <= 2.33`;
- measurement blob: `8aff444fdb42c0946342aa0011ab287eda097c4c`;
- covariance blob: `fd8e5697ab61379b07b52efb781ea6713417a4d9`;
- covariance minimum eigenvalue: `0.00578998687`;
- Lambda-CDM `Omega_m = 0.297461819`;
- Lambda-CDM `q = 29.524633391`;
- Lambda-CDM `chi2 = 10.271041003`;
- boundary: `False`;
- profiled Omega_m span: `Delta chi2 = 1529.352093440`;
- shape-identifiability gate: `PASS`.

## 3. P06-T1 reveal

The preregistered external DESI DR2 reveal returned:

- Lambda-CDM `chi2 = 10.271041003`;
- RCMS `chi2 = 8.965254157`;
- RCMS `Omega_m = 0.299132409`;
- RCMS `q = 30.115437772`;
- RCMS `A_R = 0.210244178`;
- approximate `Delta chi2 <= 1` profile interval: `[0.05, 0.40]`;
- `Delta chi2 = 1.305786846`;
- `Delta AIC = -0.694213154`;
- RCMS boundary: `False`.

The profile interval is the frozen grid-profile result from the preregistered implementation and is not retrospectively refined to strengthen the outcome.

## 4. Interpretation

DESI DR2 independently selects the same **positive direction** for `A_R` as the earlier low-redshift and external tests. The best-fit amplitude, approximately `0.21`, is also close to the original primary reference value (`~0.187`) in scale.

However, the model-selection evidence is weak. The improvement in chi-square is only about `1.31` for one additional parameter, and the AIC difference is negative, so the added RCMS parameter is not preferred after the frozen complexity penalty.

Therefore the stronger preregistered category `DESI_DR2_POSITIVE_SUPPORTED` is **not** satisfied.

The correct Protocol 06 classification is:

`DESI_DR2_POSITIVE_DIRECTIONAL`

## 5. Cumulative meaning

Protocols 04–06 now show a consistent qualitative pattern:

- eBOSS DR16 primary shape fit: positive direction, but internally sensitive to LRG;
- eBOSS ELG replacement challenge: positive but weak and zero-compatible;
- DESI DR2 external multi-redshift fit: positive direction again, with an amplitude near the primary low-redshift reference, but without complexity-penalized model preference.

This is stronger than a single-dataset anomaly in sign, but it remains insufficient for a claim that RCMS is statistically preferred over Lambda-CDM.

## 6. Scientific boundary

Protocol 06 tests a frozen phenomenological cosmological surrogate. It does not establish a derivation from, or experimental validation of, the full Resolutive Physics ontology.

The negative/limiting result in model selection is preserved as part of the scientific record and must not be removed or tuned away in later work.
