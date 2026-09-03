# RCMS Protocol 14 — Amplitude Stability Across Families and Channels

**Status:** PREREGISTERED / FROZEN BEFORE EXECUTION  
**Release line:** v0.3-dev  
**Parent release:** v0.2.0 — DOI `10.5281/zenodo.22002018`

## 1. Purpose

Protocol 14 tests whether the effective amplitude of the frozen logarithmic RCMS screening surrogate can reasonably be described as stable across observational families and across the radial/transverse decomposition exposed by P13.

The target scale near `A_R ~ 0.21` is a value to falsify, not a value to enforce.

No likelihood is refitted in P14. Only already-frozen one-dimensional best fits and `Delta chi2 <= 1` intervals are used.

## 2. Layer A — observational-family stability

The following five frozen family-level profiles are used:

| Family | Best A_R | Delta chi2 <= 1 interval | Source |
|---|---:|---:|---|
| Moresco H(z) | -1.2800 | [-2.58, 0.54] | P01 |
| Pantheon+ | 0.2139 | [-0.1087, 0.5274] | P01 |
| DES-SN5YR | 0.382099 | [0.055322, 0.707729] | P03 |
| eBOSS DR16 | 1.662222508 | [0.650565914, 3.103626193] | P04 |
| DESI DR2 BAO | 0.210244178 | [0.03, 0.40] | P06 |

These are not assumed statistically independent for discovery inference. P14 uses them only for descriptive amplitude-stability diagnostics.

Each profile is represented by the same asymmetric piecewise-quadratic approximation used in P07/P12.

P14 shall compute:

- common descriptive minimizer `A_common`;
- `Delta S <= 1` common interval;
- heterogeneity `Q` at the common minimizer;
- descriptive `I2` using `max(0,(Q-df)/Q)`;
- leave-one-family-out common amplitudes;
- maximum absolute leave-one-family-out shift;
- whether every family's `Delta chi2 <= 1` interval intersects the common `Delta S <= 1` interval.

## 3. Layer B — DESI internal channel stability

P13 froze the following non-independent diagnostic subsets of the same DESI DR2 vector:

| Channel | Best A_R | Delta chi2 <= 1 interval |
|---|---:|---:|
| radial-only (`DH_over_rs`) | -0.580 | [-0.830, -0.240] |
| transverse/volume (`DM_over_rs`, `DV_over_rs`) | 0.860 | [0.100, 1.000] |

P14 shall report:

- sign agreement or disagreement;
- interval overlap or non-overlap;
- minimum gap between the two `Delta chi2 <= 1` intervals;
- a descriptive separation statistic using the average of the lower/upper one-sigma widths appropriate to the direction of separation.

Because these subsets come from the same parent DESI dataset, this statistic is a diagnostic only and must not be converted into a formal p-value.

## 4. Preregistered classification

### `AMPLITUDE_STABLE`

Requires all of the following:

1. Layer-A heterogeneity `Q <= 9.488` (descriptive chi-square 95% reference for 4 df);
2. maximum leave-one-family-out shift `<= 0.10`;
3. every family interval intersects the common interval;
4. radial and transverse/volume channels have the same best-fit sign;
5. radial and transverse/volume `Delta chi2 <= 1` intervals overlap.

### `AMPLITUDE_FAMILY_STABLE_CHANNEL_TENSION`

Assigned when Layer A meets conditions 1–3 but Layer B fails either sign agreement or interval overlap.

### `AMPLITUDE_FAMILY_HETEROGENEOUS`

Assigned when Layer A fails any of conditions 1–3, regardless of Layer B.

### `AMPLITUDE_INDETERMINATE`

Assigned only if required frozen inputs are missing or invalid.

No favorable reinterpretation of these thresholds is permitted after execution.

## 5. Scientific boundaries

- P14 is descriptive and retrospective; it is not a combined discovery likelihood.
- Statistical independence among family profiles is not assumed.
- P13 radial/transverse subsets are explicitly non-independent and are used only as an internal stability diagnostic.
- No new amplitude, nuisance parameter, prior, covariance, cut, or deformation may be introduced.
- A failure of amplitude stability is a valid falsification outcome and shall not trigger retuning.

## 6. Advancement

After P14 is frozen, proceed to P15 complexity-penalized model comparison regardless of outcome.
