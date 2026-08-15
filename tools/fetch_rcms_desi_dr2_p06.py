#!/usr/bin/env python3
import hashlib
from pathlib import Path
from urllib.request import urlopen

BASE = "https://raw.githubusercontent.com/CobayaSampler/bao_data/v2.6/desi_bao_dr2"
FILES = {
    "desi_gaussian_bao_ALL_GCcomb_mean.txt": "8aff444fdb42c0946342aa0011ab287eda097c4c",
    "desi_gaussian_bao_ALL_GCcomb_cov.txt": "fd8e5697ab61379b07b52efb781ea6713417a4d9",
}
OUT = Path("data/rcms/protocol06/desi_dr2")
OUT.mkdir(parents=True, exist_ok=True)


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()

for name, expected in FILES.items():
    data = urlopen(f"{BASE}/{name}", timeout=60).read()
    actual = git_blob_sha(data)
    if actual != expected:
        raise SystemExit(f"blob mismatch for {name}: {actual} != {expected}")
    (OUT / name).write_bytes(data)
    print(f"verified {name}: bytes={len(data)} git_blob={actual}")

print("P06 DESI DR2 acquisition gate: READY release=v2.6")
