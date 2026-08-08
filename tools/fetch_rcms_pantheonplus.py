#!/usr/bin/env python3
"""Fetch and verify the exact Pantheon+ files frozen by RCMS Protocol 01.

This is an acquisition/integrity tool only. It performs no cosmological fit.
The source is pinned by commit and verified using Git's blob SHA-1 identity,
which hashes ``b'blob <size>\\0' + content``.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "external" / "pantheonplus_v1"
COMMIT = "61d96434cafc2770928322c38e5a750e686368ae"
BASE = f"https://raw.githubusercontent.com/CobayaSampler/sn_data/{COMMIT}/PantheonPlus"

FILES = {
    "Pantheon+SH0ES.dat": {
        "url": f"{BASE}/Pantheon+SH0ES.dat",
        "blob": "cce857db0c15e9ce7a0e0ce77452b6ff62af969a",
        "size": 579283,
    },
    "Pantheon+SH0ES_STAT+SYS.cov": {
        "url": f"{BASE}/Pantheon+SH0ES_STAT+SYS.cov",
        "blob": "d1a1498154e7ba826df14bdbef35ebcb7f5efba1",
        "size": 33284960,
    },
}


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def fetch(url: str) -> bytes:
    with urlopen(url, timeout=120) as response:
        return response.read()


def validate_dat(data: bytes) -> None:
    text = data.decode("utf-8")
    lines = text.splitlines()
    if len(lines) != 1702:
        raise RuntimeError(f"expected header + 1701 Pantheon+ rows, found {len(lines)} lines")
    header = lines[0].split()
    required = {"zHD", "zCMB", "zHEL", "m_b_corr", "IS_CALIBRATOR", "CEPH_DIST"}
    missing = required.difference(header)
    if missing:
        raise RuntimeError(f"Pantheon+ data file missing required columns: {sorted(missing)}")


def validate_cov(data: bytes) -> None:
    # Stream-like textual structural check without allocating a dense matrix.
    text = data.decode("utf-8")
    lines = text.splitlines()
    if not lines:
        raise RuntimeError("empty covariance file")
    n = int(lines[0].strip())
    if n != 1701:
        raise RuntimeError(f"expected covariance dimension 1701, found {n}")
    entries = len(lines) - 1
    expected = n * n
    if entries != expected:
        raise RuntimeError(f"expected {expected} covariance entries, found {entries}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, meta in FILES.items():
        target = OUT / name
        data = target.read_bytes() if target.exists() else fetch(meta["url"])
        if len(data) != meta["size"]:
            raise RuntimeError(f"{name}: byte-size mismatch {len(data)} != {meta['size']}")
        blob = git_blob_sha(data)
        if blob != meta["blob"]:
            raise RuntimeError(f"{name}: Git blob mismatch {blob} != {meta['blob']}")
        if name.endswith(".dat"):
            validate_dat(data)
        else:
            validate_cov(data)
        if not target.exists():
            target.write_bytes(data)
        print(f"verified {name}: bytes={len(data)} git_blob={blob}")
    print("Pantheon+ acquisition gate: READY_FOR_LIKELIHOOD_VALIDATION")


if __name__ == "__main__":
    main()
