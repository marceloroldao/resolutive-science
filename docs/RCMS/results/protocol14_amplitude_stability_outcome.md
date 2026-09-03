# RCMS Protocol 14 — Amplitude Stability Outcome

**Status:** FINAL / FROZEN  
**Release line:** v0.3-dev  
**Classification:** `AMPLITUDE_FAMILY_HETEROGENEOUS`

## 1. Hosted execution

GitHub Actions workflow: `RCMS Protocol 14 Amplitude Stability`  
Run ID: `33708859114`  
Job ID: `100503840828`  
Artifact: `rcms-protocol14-amplitude-stability`  
Artifact ID: `9876205782`  
Artifact ZIP SHA256: `3d9410d309324e5baf96ad27f1ae8c96fb405a0a173977ef71afc83625554e5c`

Identity gate: `P14_FINAL_IDENTITY=PASS`.

## 2. Observational-family layer

Using the frozen P01/P03/P04/P06 one-dimensional family profiles, the descriptive synthesis returned:

- `A_common = 0.264079766`;
- common `Delta S <= 1` interval = `[0.121971100, 0.407494649]`;
- heterogeneity `Q = 2.866338926` for 4 descriptive degrees of freedom;
- descriptive `I2 = 0.0`;
- maximum absolute leave-one-family-out shift = `0.071803487`.

The Q and leave-one-out-shift gates individually pass the preregistered stability thresholds. However, not every family `Delta chi2 <= 1` interval intersects the common interval. In particular, the high-amplitude eBOSS DR16 profile begins above the upper end of the common interval.

Therefore Layer A fails the complete family-stability criterion.

## 3. DESI internal channel layer

P13 froze:

- radial-only: `A_R = -0.580`, interval `[-0.830, -0.240]`;
- transverse/volume-only: `A_R = 0.860`, interval `[0.100, 1.000]`.

P14 returned:

- best-fit sign agreement: `False`;
- `Delta chi2 <= 1` interval overlap: `False`;
- minimum interval gap: `0.340`;
- descriptive diagonal-width separation diagnostic: `1.72955`.

No formal p-value is attached to this separation because the two channel subsets share the same parent DESI DR2 dataset and are not treated as independent experiments.

## 4. Frozen classification

The preregistered `AMPLITUDE_STABLE` and `AMPLITUDE_FAMILY_STABLE_CHANNEL_TENSION` labels both require the complete Layer-A family-stability conditions to pass.

Because not every family interval intersects the common interval, the frozen classification is:

`P14_CLASSIFICATION=AMPLITUDE_FAMILY_HETEROGENEOUS`

## 5. Scientific interpretation

P14 does not support treating a single effective amplitude near `A_R ~ 0.21` as already demonstrated to be stable across all observational families and internal channels.

Two facts coexist:

1. the broad descriptive family synthesis remains positive and has low Q under the frozen asymmetric-profile approximation;
2. the eBOSS high-amplitude profile is not locally compatible with the common `Delta S <= 1` interval, while the DESI radial/transverse decomposition shows opposite-sign best fits.

Thus the recurring positive direction remains a real feature of the frozen screening record, but amplitude universality is not established.

This result must not trigger a new redshift-dependent amplitude or additional degree of freedom in v0.3. The frozen one-parameter surrogate remains unchanged through the rest of the falsification release.

## 6. Advancement

Proceed to P15 complexity-penalized model comparison. P15 must evaluate whether any likelihood improvements survive AIC/BIC accounting and whether the logarithmic surrogate has an advantage over equal-complexity controls. A positive amplitude alone is insufficient.
