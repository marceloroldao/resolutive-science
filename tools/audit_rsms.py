#!/usr/bin/env python3
"""Static cross-chapter checks for the RSMS Markdown sources."""
from __future__ import annotations
import argparse, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "RSMS"
HEADING = re.compile(r"^### (RS-[A-Z0-9]+) — (.+)$", re.M)
TAG = re.compile(r"\\tag\{(RS-[A-Z0-9]+)\}")
REF = re.compile(r"\bRS-[A-Z][0-9]{3}\b")
BAD_LATEX = [
    (re.compile(r"\\(?:subseteq|supseteq|in|notin|to|longrightarrow)M\b"), "missing space before M"),
    (re.compile(r"\\Omega\^[^{\\s]\\\("), "malformed Omega function notation"),
]

def files(): return sorted(DOCS.rglob("*.md"))
def current_text(): return {p.relative_to(ROOT).as_posix(): p.read_text() for p in files()}
def baseline_text(ref: str, path: str) -> str | None:
    cp=subprocess.run(["git","show",f"{ref}:{path}"],cwd=ROOT,text=True,capture_output=True)
    return cp.stdout if cp.returncode == 0 else None

def definitions(texts):
    found={}
    errors=[]
    for path,text in texts.items():
        entries = HEADING.findall(text) + [(ident, "equation") for ident in TAG.findall(text)]
        for ident,title in entries:
            if ident in found: errors.append(f"duplicate {ident}: {found[ident][0]} and {path}")
            else: found[ident]=(path,title.strip())
    return found,errors

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--baseline",help="Git ref used to detect stable-heading meaning changes")
    args=ap.parse_args(); texts=current_text(); defs, errors=definitions(texts)
    # References must resolve to an extant heading.
    for path,text in texts.items():
        if "/audits/" in f"/{path}": continue
        for ident in sorted(set(REF.findall(text))):
            if ident not in defs: errors.append(f"nonexistent registry reference {ident} in {path}")
    # Markdown links to repository files must exist.
    for path,text in texts.items():
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)",text):
            if "://" not in target and not target.startswith("#"):
                dest=(ROOT/path).parent/(target.split("#",1)[0])
                if not dest.exists(): errors.append(f"broken Markdown link {target} in {path}")
    # LaTeX delimiters and known replacement damage.
    for path,text in texts.items():
        if text.count(r"\(") != text.count(r"\)"): errors.append(f"unbalanced inline LaTeX delimiters in {path}")
        if text.count(r"\[") != text.count(r"\]"): errors.append(f"unbalanced display LaTeX delimiters in {path}")
        for pattern,label in BAD_LATEX:
            for m in pattern.finditer(text): errors.append(f"{label} in {path}: {m.group(0)}")
    # Chapter metadata.
    for path,text in texts.items():
        if "/chapters/" in f"/{path}" and not text.startswith("# Chapter "):
            errors.append(f"missing chapter title metadata in {path}")
    # Canonical field/state symbols and address separation in their defining entries.
    ch4=texts["docs/RSMS/chapters/04_geometric_and_bundle_structure.md"]
    g18=re.search(r"### RS-G018.*?(?=\n### )",ch4,re.S).group()
    g20=re.search(r"### RS-G020.*?(?=\n### )",ch4,re.S).group()
    for required in (r"\mathcal R_f:U\to E_R",r"\pi_M\circ\mathcal R_f=\operatorname{id}_U"):
        if required not in g18: errors.append(f"RS-G018 lacks canonical field expression: {required}")
    if re.search(r"\bR\s*:\s*U\s*\\to",g18): errors.append("RS-G018 misuses R as a field symbol")
    if r"a_R\in\mathcal A_R" not in g20 or "Fiber data shall not be defined as part of the address" not in g20:
        errors.append("RS-G020 does not preserve canonical address/state separation")
    # Baseline stable heading meanings. A changed title must have a migration-table row.
    if args.baseline:
        base={}
        for path in texts:
            old=baseline_text(args.baseline,path)
            if old:
                for ident,title in HEADING.findall(old): base[ident]=(path,title.strip())
        report=texts.get("docs/RSMS/audits/2026-08_cross_chapter_audit.md","")
        for ident,(path,title) in base.items():
            if ident in defs and defs[ident][1] != title and not re.search(rf"\| {re.escape(ident)} \|",report):
                errors.append(f"meaning/title changed without migration row: {ident}: {title!r} -> {defs[ident][1]!r}")
            if ident not in defs and ident not in report:
                errors.append(f"identifier removed without migration entry: {ident} ({title!r})")
    if errors:
        print("RSMS audit failed:"); print("\n".join(f"- {e}" for e in errors)); return 1
    print(f"RSMS audit passed: {len(defs)} unique identifiers across {len(texts)} Markdown files.")
    if args.baseline: print(f"Stable identifier meanings checked against {args.baseline}.")
    return 0
if __name__ == "__main__": sys.exit(main())
