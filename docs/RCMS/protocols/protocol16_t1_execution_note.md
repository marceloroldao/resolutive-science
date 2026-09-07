# RCMS P16-T1 — execution note

**Status:** execution implementation note  
**Scientific specification:** unchanged

The first hosted P16-T1 runner (`tools/run_rcms_protocol16_t1_boss_dr12_reveal.py`, commit `668da531b47d518c49189f637a893d46104a4692`) was started after P16-T0 passed. No hosted target result had been produced when a deterministic performance defect was identified: the numerical integration for a fixed `(Omega_m, A_R)` pair was recomputed inside every evaluation of the global scale nuisance `q`, even though the expansion shape is independent of `q`.

A computationally optimized executor is therefore permitted with the following non-negotiable identity:

- identical frozen BOSS DR12 vector and covariance;
- identical upstream revision and SHA256 checks;
- identical `Omega_m`, `A_R`, and `q` domains;
- identical `A_R` grid step;
- identical Simpson integration rule and resolution;
- identical Gaussian chi-square;
- identical preregistered prediction interval and classification rules;
- no new data, priors, calibration, thresholds, or model terms.

The optimization may only cache the `D_M` and `H(z)` shape components for a fixed `(Omega_m, A_R)` and reuse them while profiling `q`. It must reproduce the P16-T0 `A_R=0` baseline within numerical tolerance before its target classification is accepted.

This note records an implementation-efficiency correction, not a response-dependent scientific modification. The original slow run remains part of the Actions history.