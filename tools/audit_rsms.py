#!/usr/bin/env python3
"""Static cross-chapter and release-readiness checks for RSMS Markdown sources."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "RSMS"
MASTER = DOCS / "RSMS_v1.0.md"

HEADING = re.compile(r"^### (RS-[A-Z0-9]+) — (.+)$", re.M)
TAG = re.compile(r"\\tag\{(RS-[A-Z0-9]+)\}")
REF = re.compile(r"\bRS-[A-Z][A-Z0-9]*[0-9]{3}\b")
VERSION = re.compile(r"\*\*(?:Current RSMS version|Version):\*\*\s*([^\n]+)")
MASTER_VERSION = re.compile(r"\*\*Version:\*\*\s*([^\n]+)")

BAD_LATEX = [
    (re.compile(r"\\(?:subseteq|supseteq|in|notin|to|longrightarrow)M\b"), "missing space before M"),
    (re.compile(r"\\Omega\^[^{\\s]\\\("), "malformed Omega function notation"),
    (re.compile(r"\\Gamma\\\("), "malformed Gamma function notation"),
]


def files() -> list[Path]:
    return sorted(DOCS.rglob("*.md"))


def current_text() -> dict[str, str]:
    return {p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8") for p in files()}


def baseline_text(ref: str, path: str) -> str | None:
    cp = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return cp.stdout if cp.returncode == 0 else None


def definitions(texts: dict[str, str]):
    found: dict[str, tuple[str, str]] = {}
    errors: list[str] = []
    for path, text in texts.items():
        entries = HEADING.findall(text) + [(ident, "equation") for ident in TAG.findall(text)]
        for ident, title in entries:
            if ident in found:
                errors.append(f"duplicate {ident}: {found[ident][0]} and {path}")
            else:
                found[ident] = (path, title.strip())
    return found, errors


def section(text: str, ident: str) -> str:
    match = re.search(rf"### {re.escape(ident)}.*?(?=\n### |\Z)", text, re.S)
    return match.group() if match else ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", help="Git ref used to detect stable-heading meaning changes")
    ap.add_argument(
        "--release-readiness",
        action="store_true",
        help="enable stricter checks intended for an RSMS release candidate",
    )
    args = ap.parse_args()

    texts = current_text()
    defs, errors = definitions(texts)

    # References must resolve to an extant heading/equation.
    for path, text in texts.items():
        if "/audits/" in f"/{path}":
            continue
        for ident in sorted(set(REF.findall(text))):
            if ident not in defs:
                errors.append(f"nonexistent registry reference {ident} in {path}")

    # Markdown links to repository files must exist.
    for path, text in texts.items():
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
            if "://" not in target and not target.startswith("#"):
                dest = (ROOT / path).parent / target.split("#", 1)[0]
                if not dest.exists():
                    errors.append(f"broken Markdown link {target} in {path}")

    # LaTeX delimiters and known replacement damage.
    for path, text in texts.items():
        if text.count(r"\(") != text.count(r"\)"):
            errors.append(f"unbalanced inline LaTeX delimiters in {path}")
        if text.count(r"\[") != text.count(r"\]"):
            errors.append(f"unbalanced display LaTeX delimiters in {path}")
        for pattern, label in BAD_LATEX:
            for match in pattern.finditer(text):
                errors.append(f"{label} in {path}: {match.group(0)}")

    # Chapter metadata.
    chapter_paths = [p for p in texts if "/chapters/" in f"/{p}"]
    for path in chapter_paths:
        if not texts[path].startswith("# Chapter "):
            errors.append(f"missing chapter title metadata in {path}")

    # Canonical field/state symbols and address separation.
    ch4 = texts["docs/RSMS/chapters/04_geometric_and_bundle_structure.md"]
    g18 = section(ch4, "RS-G018")
    g20 = section(ch4, "RS-G020")
    for required in (r"\mathcal R_f:U\to E_R", r"\pi_M\circ\mathcal R_f=\operatorname{id}_U"):
        if required not in g18:
            errors.append(f"RS-G018 lacks canonical field expression: {required}")
    if re.search(r"\bR\s*:\s*U\s*\\to", g18):
        errors.append("RS-G018 misuses R as a field symbol")
    if r"a_R\in\mathcal A_R" not in g20 or "Fiber data shall not be defined as part of the address" not in g20:
        errors.append("RS-G020 does not preserve canonical address/state separation")

    # Registry presence and governing-version synchronization.
    identifier_registry = texts.get("docs/RSMS/appendices/A_identifier_registry.md", "")
    symbol_registry = texts.get("docs/RSMS/appendices/B_symbol_registry.md", "")
    chapter12 = texts.get("docs/RSMS/chapters/12_appendices_and_symbol_registry.md", "")
    master = texts.get("docs/RSMS/RSMS_v1.0.md", "")

    master_match = MASTER_VERSION.search(master)
    master_version = master_match.group(1).strip() if master_match else None
    if not master_version:
        errors.append("master RSMS version is missing")
    if master_version and master_version not in identifier_registry:
        errors.append("identifier registry is not synchronized with master RSMS version")
    if master_version and master_version not in symbol_registry:
        errors.append("symbol registry is not synchronized with master RSMS version")
    if "RS-Z019" not in chapter12:
        errors.append("Chapter 12 lacks the release-readiness definition RS-Z019")

    # Canonical symbol registry minimum entries.
    minimum_symbols = (
        "`M`",
        "`\\mathcal R`",
        "`E_R`",
        "`R`",
        "`\\mathcal R_f`",
        "`\\Psi_R`",
        "`\\Pi`",
        "`\\operatorname{Red}`",
    )
    for symbol in minimum_symbols:
        if symbol not in symbol_registry:
            errors.append(f"symbol registry missing minimum entry {symbol}")

    # Known semantic/cross-reference hardening checks.
    ch5 = texts["docs/RSMS/chapters/05_fundamental_fields_and_operators.md"]
    f23 = section(ch5, "RS-F023")
    if "RS-D006" in f23:
        errors.append("RS-F023 cites RS-D006 for composition; canonical composition identifier is RS-N006")

    ch6 = texts["docs/RSMS/chapters/06_dynamics_and_variational_principles.md"]
    if r"base manifold \(\mathcal M\)" in ch6 or r"on \(\mathcal M\)" in ch6:
        errors.append("Chapter 6 still uses historical \\mathcal M for the canonical base manifold M")

    # Strict release-candidate checks.
    if args.release_readiness:
        if not symbol_registry:
            errors.append("release readiness requires Appendix B symbol registry")
        if "RSMS-1.0 hardening phase" not in master:
            errors.append("master document does not declare the hardening phase")
        if "Normative draft complete" not in master:
            errors.append("master chapter-status table is incomplete")
        if not (DOCS / "audits").exists():
            errors.append("release readiness requires an audits directory")

    # Baseline stable heading meanings. A changed title must have a migration-table row.
    if args.baseline:
        base: dict[str, tuple[str, str]] = {}
        for path in texts:
            old = baseline_text(args.baseline, path)
            if old:
                for ident, title in HEADING.findall(old):
                    base[ident] = (path, title.strip())
        report = texts.get("docs/RSMS/audits/2026-08_cross_chapter_audit.md", "")
        for ident, (_, title) in base.items():
            if ident in defs and defs[ident][1] != title and not re.search(rf"\| {re.escape(ident)} \|", report):
                errors.append(
                    f"meaning/title changed without migration row: {ident}: {title!r} -> {defs[ident][1]!r}"
                )
            if ident not in defs and ident not in report:
                errors.append(f"identifier removed without migration entry: {ident} ({title!r})")

    if errors:
        print("RSMS audit failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    print(f"RSMS audit passed: {len(defs)} unique identifiers across {len(texts)} Markdown files.")
    if master_version:
        print(f"Master version: {master_version}.")
    if args.baseline:
        print(f"Stable identifier meanings checked against {args.baseline}.")
    if args.release_readiness:
        print("Release-readiness checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
