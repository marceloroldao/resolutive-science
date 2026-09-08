# RCMS Protocol 20 — Cross-Survey Concordance Outcome

**Status:** FINAL / FROZEN  
**Release line:** v0.4-dev  
**Classification:** `EXACT_Z_SURVEY_DISCORDANCE`  
**Parent release:** v0.3.0 — DOI `10.5281/zenodo.22643804`

## 1. Hosted execution

GitHub Actions workflow: `RCMS Protocol 20 Cross-Survey Concordance`  
Run ID: `34258540967`  
Job ID: `102170400550`  
Artifact: `rcms-protocol20-cross-survey-concordance`  
Artifact ID: `10068891022`  
Artifact ZIP SHA256: `3ad27ee398edd11661b06db7c5bdfa085ff418fd701a838a4a704916ab99e131`

Identity gate:

`P20_FINAL_IDENTITY=PASS`

## 2. Primary exact-redshift comparison

The primary comparison was frozen at the exact common survey redshift

`z = 0.51`

before execution.

Each survey retained its own full-vector RCMS best-fit `Omega_m` and BAO scale nuisance; only the local diagnostic amplitude was scanned. No local nuisance re-fit or redshift interpolation was allowed.

### DESI DR2 at z=0.51

- observables: `DM_over_rs`, `DH_over_rs`;
- N = 2;
- best local `A_R = +0.160`;
- `Delta chi2 <= 1` interval: `[+0.08, +0.25]`;
- boundary contact: `False`.

### BOSS DR12 at z=0.51

- observables: `DM_over_rs`, `bao_Hz_rs`;
- N = 2;
- best local `A_R = -1.000`;
- `Delta chi2 <= 1` interval: `[-1.00, -0.89]`;
- boundary contact: `True`.

Cross-survey diagnostics:

- opposite best-fit signs: `True`;
- one-sigma profile overlap: `False`;
- interval gap: `0.97`;
- best-amplitude separation: `1.16`;
- boundary-limited because of BOSS: `True`.

## 3. Secondary frozen-window diagnostic

For the fixed BOSS span `0.38 <= z <= 0.61`:

- DESI remains represented by its exact `z=0.51` pair and prefers `A_R=+0.160`, interval `[+0.08,+0.25]`;
- BOSS uses all six DR12 observables and prefers `A_R=-1.000`, interval `[-1.00,-0.915]`;
- profiles remain disjoint;
- signs remain opposite;
- interval gap is approximately `0.995`.

The secondary diagnostic agrees with, but does not define, the primary classification.

## 4. Preregistered classification

`EXACT_Z_SURVEY_DISCORDANCE` required:

1. opposite DESI/BOSS best-fit local amplitude signs at exactly `z=0.51`; and
2. non-overlapping `Delta chi2 <= 1` intervals.

Both criteria are met.

Therefore:

`P20_CLASSIFICATION=EXACT_Z_SURVEY_DISCORDANCE`

## 5. Scientific interpretation

P20 demonstrates that cosmic epoch alone cannot explain the DESI-versus-BOSS amplitude disagreement inside this diagnostic framework: at the same redshift, with matched radial/transverse content and survey-specific global nuisances frozen, the two surveys pull the unchanged RCMS surrogate in opposite directions.

The BOSS result is boundary-limited, so the numerical amplitude separation cannot be interpreted as a well-localized physical difference. However, the sign and profile discordance inside the frozen domain are sufficient for the preregistered diagnostic label.

P20 does **not** identify the cause. Plausible classes include:

- inadequacy of the one-parameter universal RCMS surrogate;
- survey-specific systematics;
- differences in BAO compression or likelihood convention;
- calibration/nuisance structure not captured by this diagnostic;
- statistical fluctuation combined with weak local identifiability.

No one cause is selected by P20.

## 6. Combined diagnosis after P17–P20

The completed diagnosis-before-extension block now reads:

- **P17:** `DIFFUSE_RESIDUAL_STRUCTURE` — no strong post-fit channel/redshift residual topology;
- **P18:** `SURVEY_SPECIFIC_CHANNEL_TENSION` — DESI radial/transverse sign reversal is not independently replicated by BOSS;
- **P19:** `NO_REDSHIFT_LOCALITY_EVIDENCE` — calibrated split scans do not support a redshift change-point;
- **P20:** `EXACT_Z_SURVEY_DISCORDANCE` — DESI and BOSS disagree at the exact same redshift.

This pattern does not provide a stable cross-survey structure from which to motivate a new RCMS functional form.

## 7. Advancement gate

The v0.4 development plan explicitly allows the diagnostic block to stop before P21 when P17–P20 indicate survey/channel heterogeneity without stable cross-survey structure.

P20 therefore recommends activating that stop gate: **do not generate a new cosmological RCMS extension from these residuals.**

The next scientifically defensible work is a likelihood/data-convention/systematics audit, or closure of v0.4 as a diagnostic negative release, while preserving the v0.3 and v0.4 results unchanged.
