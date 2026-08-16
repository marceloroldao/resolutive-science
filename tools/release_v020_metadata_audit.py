from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

AUTHOR = "Marcelo Roldão Matos"
ORCID = "0009-0003-6075-4680"
HISTORICAL_DOI = "10.5281/zenodo.21940994"


def read(rel: str) -> str:
    path = ROOT / rel
    assert path.exists(), f"missing required release file: {rel}"
    return path.read_text(encoding="utf-8")


def main() -> None:
    license_md = read("LICENSE.md")
    commercial = read("COMMERCIAL_LICENSE.md")
    notice = read("NOTICE")
    readme = read("README.md")
    citation = read("CITATION.cff")

    # Scope-based licensing must remain explicit.
    assert "PolyForm Noncommercial License 1.0.0" in license_md
    assert "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International" in license_md
    assert "Commercial use is **not granted" in license_md
    assert "not relicensed by this repository" in license_md
    assert "separate written commercial license" in commercial

    # Author identity and ORCID must be internally consistent.
    assert AUTHOR in notice, "author mismatch in NOTICE"
    assert ORCID in notice, "ORCID mismatch in NOTICE"
    assert 'family-names: "Matos"' in citation, "family name mismatch in CITATION.cff"
    assert 'given-names: "Marcelo Roldão"' in citation, "given names mismatch in CITATION.cff"
    assert ORCID in citation, "ORCID mismatch in CITATION.cff"

    # Before final v0.2.0 freeze, historical v0.1.1 archival metadata must stay intact.
    assert 'version: "0.1.1"' in citation
    assert HISTORICAL_DOI in citation
    assert HISTORICAL_DOI in readme

    # The README must not misrepresent the noncommercial licensing scheme as OSI Open Source.
    lower = readme.lower()
    assert "not as osi-approved open-source software" in lower
    assert "commercial use requires a separate written commercial license" in lower

    # Current public release remains historical until final freeze/tagging.
    assert "Current public scientific release:** `v0.1.1`" in readme

    print("V020_METADATA_AUDIT=PASS")
    print(f"AUTHOR={AUTHOR}")
    print(f"ORCID={ORCID}")
    print("LICENSE_BOUNDARY=SOFTWARE_POLYFORM_DOCUMENTATION_CC_BY_NC_SA")
    print("CITATION_STATE=HISTORICAL_V0.1.1_PRESERVED_UNTIL_FINAL_FREEZE")


if __name__ == "__main__":
    main()
