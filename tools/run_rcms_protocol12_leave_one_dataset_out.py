#!/usr/bin/env python3
"""RCMS Protocol 12 — leave-one-dataset-family-out descriptive stress test."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/rcms_protocol12_leave_one_dataset_out.json"

FAMILIES = {
    "HZ_MORESCO": {"best": -1.280000, "lo": -2.580000, "hi": 0.540000},
    "PANTHEON_PLUS": {"best": 0.213900, "lo": -0.108700, "hi": 0.527400},
    "DES_SN5YR": {"best": 0.382099, "lo": 0.055322, "hi": 0.707729},
    "EBOSS_DR16": {"best": 1.662222508, "lo": 0.650565914, "hi": 3.103626193},
    "DESI_DR2": {"best": 0.210244178, "lo": 0.050000, "hi": 0.400000},
}


def contrib(a: float, p: dict[str, float]) -> float:
    best = p["best"]
    sig = best - p["lo"] if a < best else p["hi"] - best
    if sig <= 0:
        raise RuntimeError("invalid frozen interval")
    return ((a - best) / sig) ** 2


def total(a: float, names: list[str]) -> float:
    return sum(contrib(a, FAMILIES[n]) for n in names)


def golden_min(fn, lo=-5.0, hi=5.0, tol=1e-12):
    g = (math.sqrt(5.0) - 1.0) / 2.0
    c = hi - g * (hi - lo)
    d = lo + g * (hi - lo)
    fc, fd = fn(c), fn(d)
    while hi - lo > tol:
        if fc < fd:
            hi, d, fd = d, c, fc
            c = hi - g * (hi - lo)
            fc = fn(c)
        else:
            lo, c, fc = c, d, fd
            d = lo + g * (hi - lo)
            fd = fn(d)
    x = 0.5 * (lo + hi)
    return x, fn(x)


def bisect_level(fn, target, lo, hi, increasing: bool, tol=1e-12):
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        v = fn(mid) - target
        if increasing:
            if v < 0:
                lo = mid
            else:
                hi = mid
        else:
            if v > 0:
                lo = mid
            else:
                hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def summarize(names: list[str], label: str, full_best: float | None = None) -> dict:
    fn = lambda a: total(a, names)
    best, smin = golden_min(fn)
    target = smin + 1.0
    # broad fixed brackets safely contain all frozen family summaries.
    lo = bisect_level(fn, target, -5.0, best, increasing=False)
    hi = bisect_level(fn, target, best, 5.0, increasing=True)
    return {
        "label": label,
        "families": names,
        "A_common": best,
        "interval_deltaS_1": [lo, hi],
        "zero_in_interval": bool(lo <= 0.0 <= hi),
        "DeltaS_zero": fn(0.0) - smin,
        "shift_from_full": None if full_best is None else best - full_best,
    }


def main():
    names = list(FAMILIES)
    full = summarize(names, "FULL")
    loo = []
    for omitted in names:
        kept = [n for n in names if n != omitted]
        loo.append(summarize(kept, f"OMIT_{omitted}", full["A_common"]))

    if full["A_common"] <= 0.0 or full["zero_in_interval"]:
        classification = "NO_COMMON_POSITIVE_DIRECTION"
    elif any(r["A_common"] <= 0.0 for r in loo):
        classification = "SINGLE_FAMILY_DEPENDENT_OR_UNSTABLE"
    elif any(r["zero_in_interval"] for r in loo):
        classification = "POSITIVE_BUT_DATASET_SENSITIVE"
    else:
        classification = "DATASET_DISTRIBUTED_POSITIVE"

    payload = {
        "protocol": "P12",
        "status": "FINAL",
        "method": "P07-compatible asymmetric piecewise-quadratic descriptive profile synthesis",
        "independence_assumed": False,
        "frozen_inputs": FAMILIES,
        "full": full,
        "leave_one_family_out": loo,
        "classification": classification,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("RCMS Protocol 12 — Leave-one-dataset-family-out")
    print(f"FULL A={full['A_common']:.9f} interval={full['interval_deltaS_1']} zero={full['zero_in_interval']} DeltaS0={full['DeltaS_zero']:.9f}")
    for r in loo:
        print(f"{r['label']} A={r['A_common']:.9f} interval={r['interval_deltaS_1']} zero={r['zero_in_interval']} shift={r['shift_from_full']:.9f} DeltaS0={r['DeltaS_zero']:.9f}")
    print(f"P12_CLASSIFICATION={classification}")
    print(f"machine_readable={OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
