#!/usr/bin/env python3
"""Fetch and verify the frozen eBOSS DR16 ELG BAO-only input for RCMS Protocol 05."""
from __future__ import annotations

import hashlib
import pathlib
import urllib.request

RELEASE = "v2.6"
NAME = "sdss_DR16_ELG_BAO_DVtable.txt"
EXPECTED_GIT_BLOB = "25e8c0f773174ed3d05dcfad0929f268d90c2019"
BASE = f"https://raw.githubusercontent.com/CobayaSampler/bao_data/{RELEASE}"
OUT = pathlib.Path("data/external/eboss_dr16")


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    data = urllib.request.urlopen(f"{BASE}/{NAME}", timeout=60).read()
    got = git_blob_sha(data)
    if got != EXPECTED_GIT_BLOB:
        raise SystemExit(f"blob mismatch for {NAME}: got={got} expected={EXPECTED_GIT_BLOB}")
    (OUT / NAME).write_bytes(data)
    print(f"verified {NAME}: bytes={len(data)} git_blob={got}")
    print(f"P05 ELG acquisition gate: READY release={RELEASE}")


if __name__ == "__main__":
    main()
