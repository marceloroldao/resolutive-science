#!/usr/bin/env python3
"""Fetch and verify the frozen DES-SN5YR/Dovekie Protocol 03 inputs."""
from __future__ import annotations

import hashlib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "external" / "des_sn5yr"
REV = "c9a4fcafc4cbd19bd750dee47fc76194a45c181f"
BASE = f"https://raw.githubusercontent.com/des-science/DES-SN5YR/{REV}/4_DISTANCES_COVMAT"
FILES = {
    "DES-Dovekie_HD.csv": "f80ec4e2795edcbf3442f460c539bea56226027a",
    "STAT+SYS.npz": "4289666487f427782ec81c327ae7f7741f0f5fe5",
    "DES-Dovekie-SN_Likelihood.py": "b7142093d633bf62281a2253d85ccc54db48431a",
}


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def fetch(name: str, expected_sha: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / name
    url = f"{BASE}/{name}"
    with urllib.request.urlopen(url, timeout=120) as response:
        data = response.read()
    got = git_blob_sha(data)
    if got != expected_sha:
        raise RuntimeError(f"Git blob mismatch for {name}: got {got}, expected {expected_sha}")
    target.write_bytes(data)
    print(f"verified {name}: bytes={len(data)} git_blob={got}")
    return target


def main() -> None:
    for name, sha in FILES.items():
        fetch(name, sha)
    print(f"DES-SN5YR revision={REV}")
    print("DES-SN5YR acquisition gate: READY_FOR_LIKELIHOOD_VALIDATION")


if __name__ == "__main__":
    main()
