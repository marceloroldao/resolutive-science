#!/usr/bin/env python3
"""Fetch and verify the frozen eBOSS DR16 BAO inputs for RCMS Protocol 04."""

from __future__ import annotations

import hashlib
import pathlib
import urllib.request

RELEASE = "v2.6"
BASE = f"https://raw.githubusercontent.com/CobayaSampler/bao_data/{RELEASE}"
OUT = pathlib.Path("data/external/eboss_dr16")

FILES = {
    "sdss_DR16_LRG_BAO_DMDH.dat": "122f8dd418d427eef891ea0512695e32002ee876",
    "sdss_DR16_LRG_BAO_DMDH_covtot.txt": "76aef07f03e2352dbf6ea444c0f577d28d1c70a5",
    "sdss_DR16_QSO_BAO_DMDH.txt": "3e1e5b7cc7e739534c464e59ffc0fa2e21531994",
    "sdss_DR16_QSO_BAO_DMDH_covtot.txt": "4add5e7e9ebadf336258469872a994a5d0df2bb3",
    "sdss_DR16_LYAUTO_BAO_DMDHgrid.txt": "266086971a82e0c64750e5853d77962fb283253f",
    "sdss_DR16_LYxQSO_BAO_DMDHgrid.txt": "e27a260556b1f4a658aad78090fd0cde7f29e056",
}


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, expected in FILES.items():
        url = f"{BASE}/{name}"
        data = urllib.request.urlopen(url, timeout=60).read()
        got = git_blob_sha(data)
        if got != expected:
            raise SystemExit(f"blob mismatch for {name}: got={got} expected={expected}")
        path = OUT / name
        path.write_bytes(data)
        print(f"verified {name}: bytes={len(data)} git_blob={got}")
    print(f"eBOSS DR16 acquisition gate: READY release={RELEASE}")


if __name__ == "__main__":
    main()
