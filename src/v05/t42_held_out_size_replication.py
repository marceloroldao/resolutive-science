"""T42 held-out size replication.

Reuses T41 run_parent unchanged at the preregistered hold-out N and seeds.
"""
from __future__ import annotations
import json
from t41_higher_order_matched_tree_null import run_parent


def run():
    rows = [run_parent(1024, seed) for seed in (59, 83, 101)]
    controls = all(
        row["match_feasible"]
        and row["degree_control"]
        and row["tree_control"]
        and row["match_control"]
        and row["diversity_control"]
        for row in rows
    )
    both_high = sum(
        1
        for row in rows
        if row.get("M3", {}).get("classification") == "high"
        and row.get("M7", {}).get("classification") == "high"
    )
    return {
        "protocol": "T42 frozen",
        "N": 1024,
        "seeds": [59, 83, 101],
        "rows": rows,
        "replication_feasibility": controls,
        "both_high_count": both_high,
        "both_high_replication": bool(controls and both_high == 3),
        "partial_replication": bool(controls and both_high in (1, 2)),
        "replication_failure": bool(controls and both_high == 0),
        "guard": (
            "Exact T41 matcher; no rescue seeds, new predictors, M3/M7 matching, "
            "graph dynamics, transition law, or physical geometry."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
