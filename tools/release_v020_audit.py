from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "docs/RCMS/results/04_protocol04_independent_shape_replication.md": "INDEPENDENT_SHAPE_DIRECTIONAL_ONLY",
    "docs/RCMS/results/05_protocol05_elg_challenge_outcome.md": "POSITIVE_BUT_WEAK",
    "docs/RCMS/results/06_protocol06_desi_dr2_outcome.md": "DESI_DR2_POSITIVE_DIRECTIONAL",
    "docs/RCMS/results/07_protocol07_cross_protocol_consistency.md": "COMMON_POSITIVE_COMPATIBLE",
    "docs/RCMS/results/08_protocol08_logarithmic_provenance_outcome.md": "LOG_FORM_CONDITIONALLY_DERIVED",
    "docs/releases/v0.2.0_PUBLICATION_CHECKLIST.md": "release audit in progress",
    "docs/releases/v0.2.0_EVIDENCE_MATRIX.md": "P08",
}

PROTOCOL_DOCS = [
    "docs/RCMS/protocols/protocol04_independent_shape_replication.md",
    "docs/RCMS/protocols/protocol05_lrg_dependence_challenge.md",
    "docs/RCMS/protocols/protocol06_desi_dr2_external_replication.md",
    "docs/RCMS/protocols/protocol07_cross_protocol_parameter_consistency.md",
    "docs/RCMS/protocols/protocol08_logarithmic_provenance.md",
]

FORBIDDEN_RELEASE_CLAIMS = [
    "RCMS is statistically preferred over Lambda-CDM",
    "experimental validation of Resolutive Physics",
    "discovery of new physics",
]


def read(rel):
    p = ROOT / rel
    assert p.exists(), f"missing required file: {rel}"
    return p.read_text(encoding="utf-8")


def main():
    for rel, marker in REQUIRED.items():
        text = read(rel)
        assert marker in text, f"missing frozen marker {marker!r} in {rel}"

    rcms = read("docs/RCMS/RCMS_v0.1.md")
    assert "Parent specification:** RSMS-1.0-rc.1" in rcms
    assert "inherits **RSMS-1.0-rc.1**" in rcms

    p08 = read(PROTOCOL_DOCS[-1])
    assert "RSMS-1.0-rc.1" in p08

    for rel in PROTOCOL_DOCS:
        text = read(rel)
        assert "Protocol" in text
        assert "RSMS" in text

    matrix = read("docs/releases/v0.2.0_EVIDENCE_MATRIX.md")
    for phrase in FORBIDDEN_RELEASE_CLAIMS:
        if phrase in matrix:
            idx = matrix.index(phrase)
            context = matrix[max(0, idx-80):idx+len(phrase)+80].lower()
            assert ("does not" in context or "non-claims" in context or "not establish" in context), \
                f"unqualified release claim detected: {phrase}"

    print("V020_RELEASE_AUDIT=PASS")
    print("RSMS_BASELINE=RSMS-1.0-rc.1")
    print("FROZEN_RESULTS=P04,P05,P06,P07,P08")
    print("EVIDENCE_MATRIX=PASS")


if __name__ == "__main__":
    main()
