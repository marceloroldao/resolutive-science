# RCMS Protocol 12 — Leave-One-Dataset-Family-Out Stress Test

**Status:** PREREGISTERED — outcome not inspected  
**Release line:** v0.3-dev  
**RSMS compatibility:** RSMS-1.0-rc.1

## 1. Purpose

Protocol 12 asks whether the recurring positive RCMS amplitude direction is descriptively distributed across observational families or whether it disappears when any single family is removed.

P12 is deliberately distinct from P07. P07 removed one already-combined protocol profile at a time. P12 operates on five observational-family profiles, including separate `H(z)` and Pantheon+ profiles from P01.

No likelihood is refitted in P12.

## 2. Frozen family inputs

The following already-published `Delta chi2 <= 1` profile summaries are frozen before P12 execution:

| Family | Source | Best A_R | Lower | Upper |
|---|---|---:|---:|---:|
| `HZ_MORESCO` | P01 cosmic chronometers | -1.280000 | -2.580000 | 0.540000 |
| `PANTHEON_PLUS` | P01 Pantheon+ | 0.213900 | -0.108700 | 0.527400 |
| `DES_SN5YR` | P03 external SN | 0.382099 | 0.055322 | 0.707729 |
| `EBOSS_DR16` | P04 shape replication | 1.662222508 | 0.650565914 | 3.103626193 |
| `DESI_DR2` | P06 external BAO replication | 0.210244178 | 0.050000 | 0.400000 |

P05 is excluded because it is a challenge rearrangement of eBOSS rather than a new family. The P01 combined profiles and P07 common profile are excluded to avoid double-counting the same inputs inside this diagnostic.

## 3. Frozen approximation

Each family profile is represented by the same asymmetric piecewise-quadratic approximation used in P07:

\[
\Delta\chi_i^2(A)=
\begin{cases}
((A-\hat A_i)/\sigma_{i,-})^2,&A<\hat A_i,\\
((A-\hat A_i)/\sigma_{i,+})^2,&A\ge\hat A_i,
\end{cases}
\]

where `sigma_- = best-lower` and `sigma_+ = upper-best`.

The descriptive aggregate is

\[
S(A)=\sum_i \Delta\chi_i^2(A).
\]

The common descriptive amplitude is the minimizer of `S(A)`; its local interval is the set `S(A)-S_min <= 1`.

This construction is not a combined likelihood and makes no independence assumption.

## 4. Leave-one-family-out test

Compute the full five-family descriptive profile and five additional profiles, each omitting exactly one family:

- omit `HZ_MORESCO`;
- omit `PANTHEON_PLUS`;
- omit `DES_SN5YR`;
- omit `EBOSS_DR16`;
- omit `DESI_DR2`.

For each report:

1. common best amplitude;
2. `Delta S <= 1` interval;
3. whether zero lies in the interval;
4. `DeltaS_zero = S(0)-S_min` as a directional diagnostic only;
5. shift from the full common best fit.

## 5. Preregistered classification

### `DATASET_DISTRIBUTED_POSITIVE`

Require all of:

- full common best amplitude is positive;
- full `Delta S <= 1` interval excludes zero;
- every leave-one-family-out best amplitude remains positive;
- every leave-one-family-out `Delta S <= 1` interval excludes zero.

### `POSITIVE_BUT_DATASET_SENSITIVE`

Use when the full best amplitude is positive and every leave-one-family-out best remains positive, but at least one leave-one-family-out `Delta S <= 1` interval includes zero.

### `SINGLE_FAMILY_DEPENDENT_OR_UNSTABLE`

Use when removing at least one family moves the common best amplitude to zero or negative.

### `NO_COMMON_POSITIVE_DIRECTION`

Use when the full five-family best amplitude is non-positive or its `Delta S <= 1` interval includes zero before any omission.

## 6. Interpretation boundary

P12 is a robustness diagnostic, not a significance combination. Pantheon+ and DES-SN can share supernova content, and eBOSS/DESI can have survey-volume or tracer relationships. Unknown cross-family covariance means `DeltaS_zero` must not be converted into sigma or a formal p-value.

A positive P12 result would show only that the descriptive positive direction is not eliminated by removing one named family. It would not establish RCMS preference over Lambda-CDM, especially in light of P11's `FUNCTIONALLY_NON_SPECIFIC` result.

Negative or sensitive outcomes must be preserved without changing the RCMS logarithmic surrogate.
