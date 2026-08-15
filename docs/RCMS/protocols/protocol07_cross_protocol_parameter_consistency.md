# RCMS Protocol 07 — Cross-Protocol Parameter Consistency Synthesis

**Status:** Preregistered retrospective synthesis before computation of the synthesis statistic  
**RSMS compatibility:** RSMS-1.0  
**Model form:** frozen one-parameter RCMS screening surrogate, `A_R ln(1+z)`

## 1. Purpose

Protocol 07 asks a narrower question than the earlier observational protocols:

> Are the already-frozen `A_R` estimates from the principal RCMS screening protocols mutually compatible with a common positive amplitude, or is there statistically important cross-protocol heterogeneity?

This is a retrospective consistency synthesis. It is **not** a new blind observational test and it must not be presented as independent discovery evidence.

## 2. Frozen inputs

Only already-published/frozen profile summaries are used. No earlier likelihood is refitted.

### P01/02 primary reference

- best fit: `A_R = 0.187021`
- frozen `Delta chi2 <= 1` interval: `[0.098671, 0.276779]`

### P03 DES-SN5YR external supernova replication

- best fit: `A_R = 0.382099`
- frozen `Delta chi2 <= 1` interval: `[0.055322, 0.707729]`

### P04 eBOSS DR16 independent shape fit

- best fit: `A_R = 1.662222508`
- frozen `Delta chi2 <= 1` interval: `[0.650565914, 3.103626193]`
- known robustness limitation: strong LRG influence

### P06 DESI DR2 external multi-redshift fit

- best fit: `A_R = 0.210244178`
- frozen grid-profile `Delta chi2 <= 1` interval: `[0.05, 0.40]`

P05 is excluded from the primary synthesis because it is a challenge rearrangement of the eBOSS dataset rather than an independent observational likelihood. Its positive-but-weak result is retained only as a qualitative sensitivity diagnostic.

## 3. Dependence warning

The four primary profile summaries are **not assumed statistically independent**.

In particular:

- the P01 discovery statistic included Pantheon+/DESI information;
- P06 uses DESI DR2;
- survey/sample overlap and shared cosmological systematics can create covariance not represented by the published one-dimensional profile summaries;
- P03 and P01 supernova samples can also share calibration/systematics at some level even though P03 used an external DES-SN5YR release.

Therefore Protocol 07 must not interpret a sum of profile contributions as a discovery-level combined likelihood or quote a combined Gaussian sigma as if the inputs were independent.

## 4. Frozen profile approximation

Each reported profile is approximated by an asymmetric piecewise quadratic centered on its frozen best fit `a_i`:

```text
DeltaChi2_i(A) = ((A-a_i)/(a_i-L_i))^2,  A <= a_i
               = ((A-a_i)/(U_i-a_i))^2,  A >  a_i
```

where `[L_i,U_i]` is the frozen `Delta chi2 <= 1` interval.

No interval may be narrowed, symmetrized, rescaled, or replaced after the synthesis result is seen.

## 5. Primary consistency statistic

Define the descriptive common-amplitude profile

```text
S(A) = sum_i DeltaChi2_i(A)
```

and let `A_common` minimize `S(A)`.

The cross-protocol heterogeneity statistic is

```text
Q = S(A_common)
```

with descriptive degrees of freedom `k-1 = 3` for four profile summaries.

For context only, compute

```text
I2 = max(0, (Q-(k-1))/Q)
```

when `Q > 0`, and the chi-square tail probability for `Q` with three degrees of freedom.

Because unmodelled cross-dataset covariance may exist, these quantities are diagnostics of consistency, not a formal proof of independence.

## 6. Common-amplitude profile interval

The descriptive common-amplitude `Delta S <= 1` interval is the set of `A` satisfying

```text
S(A) - S(A_common) <= 1.
```

This interval is reported only as a cross-protocol compatibility summary.

## 7. Zero-direction diagnostic

Compute

```text
DeltaS_zero = S(0) - S(A_common).
```

This diagnostic indicates how much the frozen one-dimensional summaries collectively favor a positive common direction under the piecewise-profile construction.

**It must not be converted into a discovery sigma or p-value**, because the required cross-protocol covariance matrix is not available and the inputs are not guaranteed independent.

## 8. Leave-one-protocol-out robustness

Repeat the minimization after removing each of P01, P03, P04, and P06 once.

Record for every omission:

- common best-fit amplitude;
- `Delta S <= 1` interval;
- whether the common best fit remains positive;
- whether zero lies inside the descriptive `Delta S <= 1` interval;
- heterogeneity `Q` for the remaining profiles.

This test is particularly important for determining whether the high-amplitude, LRG-sensitive P04 result controls the synthesis.

## 9. Frozen classifications

Protocol 07 must use one of these classifications:

### `COMMON_POSITIVE_COMPATIBLE`

Use if:

- `A_common > 0`;
- the common `Delta S <= 1` interval excludes zero;
- heterogeneity is not large (`Q <= 7.815`, the conventional 95% chi-square threshold for 3 descriptive degrees of freedom);
- and every leave-one-out common best fit remains positive.

### `COMMON_POSITIVE_HETEROGENEOUS`

Use if `A_common > 0` but `Q > 7.815` or a major leave-one-out inconsistency appears.

### `COMMON_ZERO_COMPATIBLE`

Use if zero lies within the common `Delta S <= 1` interval.

### `COMMON_SIGN_CONFLICT`

Use if the synthesis or leave-one-out diagnostics show a substantive sign conflict.

## 10. Anti-tuning rules

After the first Protocol 07 synthesis is executed:

- no frozen P01/P03/P04/P06 value or interval may be changed;
- P04 may not be removed merely because it has a higher amplitude;
- P05 may not be promoted into the primary set to improve the result;
- no independence assumption may be introduced post hoc;
- no combined discovery sigma may be inferred from `DeltaS_zero`;
- adverse or heterogeneous results must be preserved.

## 11. Scientific boundary

Protocol 07 evaluates the consistency of a phenomenological RCMS cosmological surrogate across previously executed screening protocols. It does not validate the full Resolutive Physics ontology, derive the surrogate from the Resolutive Master Equation, or establish that the surrogate is preferred over Lambda-CDM.
