#!/usr/bin/env python3
"""Structural validation for RCMS-DATA-CC-HZ-v1.

This script deliberately performs no cosmological fit. The production fit remains
blocked until the covariance requirement in the provenance record is satisfied.
"""
from __future__ import annotations

import csv
from math import isfinite
from pathlib import Path

DATA = Path("data/rcms/cc_hz_v1.csv")
EXPECTED_ROWS = 32


def main() -> None:
    with DATA.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    if len(rows) != EXPECTED_ROWS:
        raise SystemExit(f"expected {EXPECTED_ROWS} rows, found {len(rows)}")

    seen = set()
    redshifts = []
    for line_no, row in enumerate(rows, start=2):
        try:
            z = float(row["z"])
            hz = float(row["H_km_s_Mpc"])
            sigma = float(row["sigma_km_s_Mpc"])
            ref = row["reference_key"].strip()
        except (KeyError, ValueError) as exc:
            raise SystemExit(f"invalid row {line_no}: {exc}") from exc

        if not all(isfinite(v) for v in (z, hz, sigma)):
            raise SystemExit(f"non-finite value at row {line_no}")
        if z < 0 or hz <= 0 or sigma <= 0:
            raise SystemExit(f"nonphysical scalar value at row {line_no}")
        if not ref:
            raise SystemExit(f"missing reference key at row {line_no}")

        key = (z, ref)
        if key in seen:
            raise SystemExit(f"duplicate (z, reference) at row {line_no}: {key}")
        seen.add(key)
        redshifts.append(z)

    if min(redshifts) != 0.07 or max(redshifts) != 1.965:
        raise SystemExit("unexpected redshift coverage")

    print(
        f"RCMS-DATA-CC-HZ-v1 OK: rows={len(rows)} "
        f"z_min={min(redshifts):.4f} z_max={max(redshifts):.4f}"
    )
    print("Production-fit gate: BLOCKED pending covariance reproduction/import.")


if __name__ == "__main__":
    main()
