#!/usr/bin/env python3
"""Deterministic structural conformance audit for RSMS Markdown sources."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "RSMS"
CHAPTERS = DOCS / "chapters"
ID_RE = re.compile(r"(?<![A-Z0-9-])(RS-(?:[A-Z]+\d+|\d+))(?![A-Z0-9-])")
DEF_RE = re.compile(r"^###\s+(RS-(?:[A-Z]+\d+|\d+))\s+[—-]\s+(.+?)\s*$")
TAG_RE = re.compile(r"\\tag\{(RS-[A-Z]+\d+)\}")
HEADER_FIELDS = (
    "Specification", "Current RSMS version", "Chapter revision", "Introduced in",
    "Status", "Parent document", "Author",
)


def sources() -> list[Path]:
    return [DOCS / "RSMS_v1.0.md", *sorted(CHAPTERS.glob("*.md"))]


def chapter_number(path: Path) -> str:
    if path.name == "RSMS_v1.0.md":
        return "1"
    return str(int(path.name.split("_", 1)[0]))


def definitions(files: list[Path]):
    found = []
    for path in files:
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = DEF_RE.match(line)
            if match:
                found.append((match.group(1), chapter_number(path), match.group(2), path, line_no, "clause"))
            for tag in TAG_RE.findall(line):
                found.append((tag, chapter_number(path), "Tagged equation", path, line_no, "equation"))
    return found


def check(files: list[Path]) -> list[str]:
    errors: list[str] = []
    defs = definitions(files)
    locations: dict[str, list[tuple[Path, int]]] = defaultdict(list)
    for ident, _, _, path, line_no, _ in defs:
        locations[ident].append((path, line_no))
    for ident, places in sorted(locations.items()):
        if len(places) > 1:
            errors.append(f"duplicate ID {ident}: " + ", ".join(f"{p.relative_to(ROOT)}:{n}" for p, n in places))

    known = set(locations)
    for path in files:
        text = path.read_text(encoding="utf-8")
        if chapter_number(path) != "1":
            prefix = text.split("---", 1)[0]
            for field in HEADER_FIELDS:
                if len(re.findall(rf"^\*\*{re.escape(field)}:\*\*", prefix, re.M)) != 1:
                    errors.append(f"{path.relative_to(ROOT)}: metadata field {field!r} must occur exactly once")
        for line_no, line in enumerate(text.splitlines(), 1):
            for ident in ID_RE.findall(line):
                if ident not in known and ident != "RSMS-1":
                    errors.append(f"{path.relative_to(ROOT)}:{line_no}: unresolved ID {ident}")
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", line):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target_path = (path.parent / target.split("#", 1)[0]).resolve()
                if not target_path.exists():
                    errors.append(f"{path.relative_to(ROOT)}:{line_no}: broken local link {target}")

        # Equation tags are identifiers and are therefore covered by the global
        # uniqueness check above. Repeated untagged identities are legitimate.
        table_width = None
        for line_no, line in enumerate(text.splitlines(), 1):
            if line.startswith("|") and line.endswith("|"):
                width = line.count("|")
                if table_width is not None and width != table_width:
                    errors.append(f"{path.relative_to(ROOT)}:{line_no}: inconsistent table width")
                table_width = width
            else:
                table_width = None

    expected = set(range(2, 10))
    present = {int(path.name.split("_", 1)[0]) for path in CHAPTERS.glob("[0-9][0-9]_*.md")}
    if expected - present:
        errors.append(f"orphaned chapter sequence; missing {sorted(expected - present)}")
    return errors


def write_registry(files: list[Path]) -> None:
    rows = sorted(definitions(files), key=lambda row: (row[0], str(row[3]), row[4]))
    out = [
        "# Appendix B — Global Identifier Registry", "",
        "This generated registry is informative output of `tools/audit_rsms.py --write`. The source clauses remain normative.", "",
        "| ID | Chapter | Name | Category | Status |", "|---|---:|---|---|---|",
    ]
    status = {"1": "Normative draft"}
    for ident, chapter, name, _, _, category in rows:
        out.append(f"| {ident} | {chapter} | {name.replace('|', '\\|')} | {category} | {status.get(chapter, 'Normative draft')} |")
    (DOCS / "appendices" / "B_global_identifier_registry.md").write_text("\n".join(out) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="regenerate derived registries")
    args = parser.parse_args()
    files = sources()
    if args.write:
        write_registry(files)
    errors = check(files)
    if errors:
        print("RSMS audit failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"RSMS audit passed: {len(files)} chapters, {len(definitions(files))} unique identifiers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
