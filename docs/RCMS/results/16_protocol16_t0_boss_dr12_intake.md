# RCMS Protocol 16 — P16-T0 BOSS DR12 intake outcome

**Status:** FINAL / FROZEN BEFORE RCMS TARGET REVEAL  
**Classification:** `READY_FOR_BLIND_RCMS_REVEAL`

The held-out BOSS DR12 consensus target passed the preregistered intake and identifiability gate before any target `A_R` evaluation.

Frozen upstream revision: `CobayaSampler/bao_data@bb0c1c9009dc76d1391300e169e8df38fd1096db`.

Verified SHA256:

- `sdss_DR12Consensus_bao.dat`: `fc43f1cd9c815bb58b09f4d8d1d272d2c4ec57e05e4893e2121c20dc08f4f862`
- `BAO_consensus_covtot_dM_Hz.txt`: `05c04829c8edc117870efe809494593a23de6c35547f8b66760a5250804b65cf`

Covariance checks:

- maximum asymmetry: `0.0`
- minimum eigenvalue: `1.866164783` (>0)

Flat-Lambda-CDM with the single global BAO scale nuisance profiled gave:

- `Omega_m = 0.364867611`
- `q = 30.509014587`
- `chi2 = 2.061158601`

The profiled `Omega_m` chi-square span across the frozen domain was `53.617085474`, so the three-redshift target retains shape information after global-scale profiling.

Formal gates:

- `P16_T0_SHAPE_IDENTIFIABILITY=PASS`
- `RCMS_PARAMETER_EVALUATED=NO`
- `P16_T0_STATUS=READY_FOR_BLIND_RCMS_REVEAL`

Workflow run: `34074572958`  
Artifact: `rcms-protocol16-t0-boss-dr12`  
Artifact ZIP SHA256: `8cf6c8e995a7d3c704ad15ceddd6c1e2dda876e6cfbec103da7e56d08fc170d2`

This gate does not constitute evidence for or against RCMS; it only establishes that the preregistered held-out target is usable for P16-T1.