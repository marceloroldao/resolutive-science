"""T57 ordinary low-voltage bench-data audit.

No file contents are assumed to represent an actual measurement. Self-tests use
synthetic in-memory fixtures and explicitly state that provenance.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

EDGES = (
    ("r", "A"), ("r", "B"), ("r", "C"),
    ("A", "U"), ("B", "V"), ("B", "B1"),
    ("C", "W"), ("C", "C1"), ("C", "C2"),
)
EDGE_KEYS = {frozenset(e) for e in EDGES}
PATHS = {
    "U": (("r", "A"), ("A", "U")),
    "V": (("r", "B"), ("B", "V")),
    "W": (("r", "C"), ("C", "W")),
}
OFFPATH = {"U": "B-B1", "V": "C-C1", "W": "B-B1"}
RESISTOR_FIELDS = (
    "a", "b", "R_pre_ohm", "u_R_pre_ohm",
    "R_post_ohm", "u_R_post_ohm",
)
PORT_FIELDS = (
    "repeat", "target", "nominal_voltage_V", "measured_port_V",
    "u_V", "measured_port_I_A", "u_I_A", "offpath_edge",
    "offpath_drop_V", "u_offpath_V",
)


def require_fields(rows, required, name):
    for i, row in enumerate(rows, 2):
        missing = set(required) - set(row)
        if missing:
            raise ValueError(f"{name} row {i}: missing columns {sorted(missing)}")


def positive_number(row, key, name):
    try:
        x = float(row[key])
    except (ValueError, TypeError, KeyError) as exc:
        raise ValueError(f"{name}: invalid {key}") from exc
    if not math.isfinite(x) or x <= 0:
        raise ValueError(f"{name}: {key} must be positive finite")
    return x


def finite_number(row, key, name):
    try:
        x = float(row[key])
    except (ValueError, TypeError, KeyError) as exc:
        raise ValueError(f"{name}: invalid {key}") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name}: {key} must be finite")
    return x


def parse_resistors(rows):
    if len(rows) != len(EDGES):
        raise ValueError("resistors.csv requires exactly nine measured edges")
    require_fields(rows, RESISTOR_FIELDS, "resistors")
    out = {}
    for i, row in enumerate(rows, 2):
        a, b = row["a"].strip(), row["b"].strip()
        key = frozenset((a, b))
        if key not in EDGE_KEYS or len(key) != 2 or key in out:
            raise ValueError(f"resistors row {i}: invalid or duplicate edge")
        name = f"resistors row {i}"
        pre = positive_number(row, "R_pre_ohm", name)
        upre = positive_number(row, "u_R_pre_ohm", name)
        post = positive_number(row, "R_post_ohm", name)
        upost = positive_number(row, "u_R_post_ohm", name)
        drift_u = math.hypot(upre, upost)
        drift_z = (post - pre) / drift_u
        out[key] = {
            "edge": "-".join((a, b)),
            "R_pre_ohm": pre,
            "u_R_pre_ohm": upre,
            "R_post_ohm": post,
            "u_R_post_ohm": upost,
            "drift_ohm": post - pre,
            "drift_standardized": drift_z,
            "stability_pass": abs(drift_z) <= 3.0,
        }
    if set(out) != EDGE_KEYS:
        raise ValueError("resistors.csv missing a frozen graph edge")
    return out


def parse_ports(rows):
    if len(rows) != 30:
        raise ValueError("ports.csv requires exactly 30 observations")
    require_fields(rows, PORT_FIELDS, "ports")
    out = {}
    for i, row in enumerate(rows, 2):
        name = f"ports row {i}"
        try:
            rep = int(row["repeat"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{name}: invalid repeat") from exc
        if rep not in range(1, 6) or str(rep) != str(row["repeat"]).strip():
            raise ValueError(f"{name}: repeat must be 1..5")
        target = row["target"].strip()
        nominal = finite_number(row, "nominal_voltage_V", name)
        key = (rep, target, nominal)
        if target not in PATHS or nominal not in (3.0, 6.0):
            raise ValueError(f"{name}: invalid target or voltage")
        if key in out:
            raise ValueError(f"{name}: duplicate acquisition")
        if row["offpath_edge"].strip() != OFFPATH[target]:
            raise ValueError(f"{name}: unexpected off-path edge")
        out[key] = {
            "repeat": rep,
            "target": target,
            "nominal_voltage_V": nominal,
            "measured_port_V": positive_number(row, "measured_port_V", name),
            "u_V": positive_number(row, "u_V", name),
            "measured_port_I_A": positive_number(row, "measured_port_I_A", name),
            "u_I_A": positive_number(row, "u_I_A", name),
            "offpath_edge": OFFPATH[target],
            "offpath_drop_V": finite_number(row, "offpath_drop_V", name),
            "u_offpath_V": positive_number(row, "u_offpath_V", name),
        }
    expected = {
        (rep, target, voltage)
        for rep in range(1, 6)
        for target in PATHS
        for voltage in (3.0, 6.0)
    }
    if set(out) != expected:
        raise ValueError("ports.csv: incomplete acquisition matrix")
    return out


def evaluate(resistor_rows, port_rows):
    resistors = parse_resistors(resistor_rows)
    ports = parse_ports(port_rows)
    per_resistor = sorted(resistors.values(), key=lambda x: x["edge"])
    resistance_stable = all(item["stability_pass"] for item in per_resistor)

    out = []
    for (rep, target, nominal), row in sorted(ports.items()):
        path = [resistors[frozenset(edge)] for edge in PATHS[target]]
        R = sum(x["R_pre_ohm"] for x in path)
        u_R = math.hypot(*(x["u_R_pre_ohm"] for x in path))
        V = row["measured_port_V"]
        u_V = row["u_V"]
        I = row["measured_port_I_A"]
        u_I = row["u_I_A"]
        pred = V / R
        u_pred = math.hypot(u_V / R, V * u_R / (R * R))
        u_combined = math.hypot(u_I, u_pred)
        residual = I - pred
        z = residual / u_combined
        off_z = row["offpath_drop_V"] / row["u_offpath_V"]
        port = {
            **row,
            "path_resistance_ohm": R,
            "u_path_resistance_ohm": u_R,
            "predicted_current_A": pred,
            "u_predicted_current_A": u_pred,
            "current_residual_A": residual,
            "u_current_residual_A": u_combined,
            "current_standardized_residual": z,
            "current_gate": abs(z) <= 3.0,
            "offpath_standardized_drop": off_z,
            "offpath_gate": abs(off_z) <= 3.0,
            "nominal_setting_gate": abs(V - nominal) <= 0.5,
            "predicted_port_power_W": V * pred,
            "observed_port_power_W": V * I,
        }
        out.append(port)
    current_gate = all(x["current_gate"] for x in out)
    offpath_gate = all(x["offpath_gate"] for x in out)
    setting_gate = all(x["nominal_setting_gate"] for x in out)
    passed = resistance_stable and current_gate and offpath_gate and setting_gate

    return {
        "protocol": "T57 frozen",
        "provenance": "DATA_SUBMITTED_UNVERIFIED",
        "resistor_count": len(per_resistor),
        "port_count": len(out),
        "resistors": per_resistor,
        "ports": out,
        "resistor_stability_gate": resistance_stable,
        "current_comparator_gate": current_gate,
        "offpath_gate": offpath_gate,
        "source_setting_gate": setting_gate,
        "classical_calibration_gate": passed,
        "physical_measurement_authenticated": False,
        "lambda_R_measured": False,
        "new_physics": "NOT_ESTABLISHED",
    }


def synthetic_fixture():
    resistors = [
        {
            "a": a, "b": b,
            "R_pre_ohm": "1000", "u_R_pre_ohm": "2",
            "R_post_ohm": "1000", "u_R_post_ohm": "2",
        }
        for a, b in EDGES
    ]
    ports = [
        {
            "repeat": str(rep), "target": target,
            "nominal_voltage_V": str(voltage),
            "measured_port_V": str(voltage), "u_V": "0.01",
            "measured_port_I_A": str(voltage / 2000),
            "u_I_A": "0.00002",
            "offpath_edge": OFFPATH[target],
            "offpath_drop_V": "0", "u_offpath_V": "0.002",
        }
        for rep in range(1, 6)
        for target in PATHS
        for voltage in (3.0, 6.0)
    ]
    return resistors, ports


def self_test():
    def clone(value):
        return json.loads(json.dumps(value))

    rs, ps = synthetic_fixture()
    good = evaluate(rs, ps)
    if not good["classical_calibration_gate"]:
        raise AssertionError("synthetic ideal fixture failed")
    checks = {"ideal_fixture_passes": True}

    bad = clone(ps)
    bad[0]["measured_port_I_A"] = "0.0025"
    checks["altered_current_rejected"] = not evaluate(rs, bad)["current_comparator_gate"]

    bad = clone(ps)
    bad[0]["offpath_drop_V"] = "0.1"
    checks["nonzero_offpath_rejected"] = not evaluate(rs, bad)["offpath_gate"]

    for name, altered in (
        ("missing_record_rejected", ps[:-1]),
        ("duplicate_record_rejected", ps[:-1] + [ps[0]]),
    ):
        try:
            evaluate(rs, altered)
        except ValueError:
            checks[name] = True
        else:
            checks[name] = False

    bad_r = clone(rs)
    bad_r[0]["R_post_ohm"] = "1040"
    checks["resistor_drift_rejected"] = not evaluate(bad_r, ps)["resistor_stability_gate"]

    return {
        "protocol": "T57 frozen",
        "provenance": "SYNTHETIC_SELF_TEST",
        "checks": checks,
        "all_self_tests_pass": all(checks.values()),
        "physical_measurement": "NOT_EXECUTED",
        "new_physics": "NOT_ESTABLISHED",
    }


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--analyze", action="store_true")
    parser.add_argument("--resistors", type=Path)
    parser.add_argument("--ports", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
        code = 0 if result["all_self_tests_pass"] else 1
    else:
        if args.resistors is None or args.ports is None:
            parser.error("--analyze requires --resistors and --ports")
        try:
            result = evaluate(load_csv(args.resistors), load_csv(args.ports))
        except (ValueError, OSError) as exc:
            result = {
                "protocol": "T57 frozen",
                "provenance": "DATA_SUBMITTED_UNVERIFIED",
                "schema_gate": False,
                "error": str(exc),
                "physical_measurement_authenticated": False,
                "new_physics": "NOT_ESTABLISHED",
            }
        code = 0 if result.get("classical_calibration_gate", False) else 1
    output = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    print(output)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
