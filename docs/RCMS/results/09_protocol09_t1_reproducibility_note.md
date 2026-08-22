# RCMS Protocol 09 T1 — Cross-Run Numerical Reproducibility Note

**Status:** AUDIT NOTE  
**Release line:** v0.3-dev  
**Frozen scientific outcome:** `CALIBRATION_PASS`

## Purpose

A later rerun of the unchanged P09-T1 runner produced the same scientific classification and the same recovered `A_hat` value for all 5000 realizations, but a different SHA256 for the realization CSV. This note records the audit rather than replacing the original frozen outcome.

## Compared executions

Original frozen execution:

- run ID: `32328313572`
- runner commit: `be0172ce8a41a8c57f3260bd510f29913c7f509a`
- Python: `3.12.14`
- NumPy: `2.5.2`
- Ubuntu runner image: `20260816.277.1`
- CSV SHA256: `d94d245c7c5f855f2064e03d858a5eccede25d948531dc183f2da030c8799f24`

Audit rerun:

- run ID: `32587458349`
- same P09-T1 runner source relative to the original execution
- Python: `3.12.14`
- NumPy: `2.5.2`
- Ubuntu runner image: `20260816.277.1`
- CSV SHA256: `390dcc2f766b81cb95073357d093522d2f9c1a12a38de7818a78a0671f5f1dce`

## Direct artifact comparison

The two archived CSVs were compared row by row.

- number of realizations in each: `5000`
- differing `A_hat` values: `0`
- differing coverage flags: `0`
- differing one-sided false-positive flags: `0`
- differing boundary-hit flags: `0`
- differing fit-failure flags: `0`
- rows with different serialized `DeltaChi2_A0`: `3916`
- maximum absolute `DeltaChi2_A0` difference: approximately `1.8e-10`

The JSON summaries differ only in the CSV hash, `q` at about `7e-15`, and `DeltaChi2` quantiles at roughly `1e-10` scale. All preregistered metrics and the final classification are unchanged.

## Interpretation

The byte-level CSV hash is therefore host-sensitive at sub-nanoscopic floating-point precision even under the same Python, NumPy, runner image, seed, and unchanged scientific code. The P09-T1 scientific result is numerically reproducible to a tolerance far tighter than any preregistered decision threshold, but the CSV should not be treated as guaranteed bitwise reproducible across hosted runner hardware.

The original frozen artifact and hash remain authoritative provenance for the scientific execution. Later reruns are reproducibility checks, not replacements.

This note does not modify any P09-T1 gate, model, estimator, threshold, or classification.
