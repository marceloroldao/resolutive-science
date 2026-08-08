#!/usr/bin/env python3
"""Generate machine-readable RSMS identifier and symbol registries.

The normative Markdown clauses remain authoritative. This tool provides a
deterministic machine-readable index required by RS-Z017.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "RSMS"

HEADING = re.compile(r"^### (RS-[A-Z0-9]+) — (.+)$", re.M)
TAG = re.compile(r"\\tag\{(RS-[A-Z0-9]+)\}")
MASTER_VERSION = re.compile(r"\*\*Version:\*\*\s*([^\n]+)")
TABLE_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def version() -> str:
    text = read(DOCS / "RSMS_v1.0.md")
    match = MASTER_VERSION.search(text)
    if not match:
        raise SystemExit("master RSMS version not found")
    return match.group(1).strip()


def markdown_files() -> list[Path]:
    return sorted(DOCS.rglob("*.md"))


def identifier_registry() -> dict:
    entries: list[dict] = []
    seen: set[str] = set()
    for path in markdown_files():
        rel = path.relative_to(ROOT).as_posix()
        text = read(path)
        for ident, title in HEADING.findall(text):
            if ident in seen:
                raise SystemExit(f"duplicate identifier while generating registry: {ident}")
            seen.add(ident)
            entries.append(
                {
                    "identifier": ident,
                    "kind": "clause",
                    "title": title.strip(),
                    "source": rel,
                    "status": "active",
                }
            )
        for ident in TAG.findall(text):
            if ident in seen:
                raise SystemExit(f"duplicate identifier/equation tag while generating registry: {ident}")
            seen.add(ident)
            entries.append(
                {
                    "identifier": ident,
                    "kind": "equation",
                    "title": None,
                    "source": rel,
                    "status": "active",
                }
            )
    entries.sort(key=lambda item: item["identifier"])
    return {
        "schema": "rsms.identifier-registry.v1",
        "specification": "RSMS-1.0",
        "version": version(),
        "authority": "normative Markdown clauses",
        "count": len(entries),
        "entries": entries,
    }


def symbol_registry() -> dict:
    path = DOCS / "appendices" / "B_symbol_registry.md"
    if not path.exists():
        raise SystemExit("Appendix B symbol registry not found")
    entries: list[dict] = []
    for line in read(path).splitlines():
        match = TABLE_ROW.match(line)
        if not match:
            continue
        symbol, name, typ, governing, notes, status = [value.strip() for value in match.groups()]
        if symbol == "Symbol":
            continue
        entries.append(
            {
                "symbol": symbol,
                "name": name,
                "type": typ,
                "governing_definition": governing,
                "notes": notes,
                "status": status,
            }
        )
    if not entries:
        raise SystemExit("no symbol entries parsed from Appendix B")
    return {
        "schema": "rsms.symbol-registry.v1",
        "specification": "RSMS-1.0",
        "version": version(),
        "authority": "Appendix B plus governing clauses",
        "count": len(entries),
        "entries": entries,
    }


def dump(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="build/rsms_registries")
    args = parser.parse_args()

    out = ROOT / args.output_dir
    identifiers = identifier_registry()
    symbols = symbol_registry()
    dump(identifiers, out / "identifiers.json")
    dump(symbols, out / "symbols.json")

    # Round-trip validation ensures emitted files are valid JSON and deterministic
    # with respect to the current source tree.
    for name in ("identifiers.json", "symbols.json"):
        json.loads(read(out / name))

    print(
        f"Generated {identifiers['count']} identifiers and {symbols['count']} symbols "
        f"for {identifiers['version']} in {out.relative_to(ROOT)}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
