"""T46 direct P_B-matched intervention audit.

Stage A reconstructs the exact T41 C/A/G-matched baseline without using M3/M7.
Stage B adds a preregistered P_B constraint. M3/M7 are computed only after
the Stage-B intervention ensemble is frozen.
"""
from __future__ import annotations
import json
import random
import numpy as np

from t25_endogenous_dimension_scan import generate
from t38_degree_matched_tree_null import degree_sequence, is_connected_tree
from t39_higher_order_topology_source import topology_vector, m3_m7
from t41_higher_order_matched_tree_null import (
    tree_to_prufer,
    edge_set,
    baseline_stats,
    cag,
    inside_box,
    decode_explicit_prufer,
    summarize,
    summarize_heldout,
)
from t45_held_out_branch_core_pair_connectivity import (
    branch_core_pair_connectivity,
)


def sample_stage_a(parent, n, parent_seed, degrees, target, mean, sd):
    parent_edges = edge_set(parent)
    current_seq = tree_to_prufer(parent)
    current_cag = target.copy()
    rng = random.Random(7000003 * n + 7919 * parent_seed)

    accepted = 0
    proposals = 0
    stored = []
    stored_edges = set()

    while proposals < 250000 and len(stored) < 99:
        proposals += 1
        i, j = rng.sample(range(len(current_seq)), 2)
        proposal_seq = list(current_seq)
        proposal_seq[i], proposal_seq[j] = proposal_seq[j], proposal_seq[i]

        if proposal_seq == current_seq:
            continue

        proposal = decode_explicit_prufer(proposal_seq, n)
        proposal_cag = cag(topology_vector(proposal), mean, sd)

        if not inside_box(proposal_cag, target):
            continue

        current_seq = proposal_seq
        current_cag = proposal_cag
        accepted += 1

        if accepted <= 500:
            continue
        if (accepted - 500) % 50 != 0:
            continue

        edges = edge_set(proposal)
        overlap = len(edges & parent_edges) / (n - 1)

        if overlap > 0.90 or edges in stored_edges:
            continue

        stored_edges.add(edges)
        stored.append(
            {
                "adj": proposal,
                "CAG": current_cag.copy(),
                "parent_edge_overlap": overlap,
            }
        )

    controls = (
        len(stored) == 99
        and all(degree_sequence(x["adj"]) == degrees for x in stored)
        and all(is_connected_tree(x["adj"]) for x in stored)
        and all(inside_box(x["CAG"], target) for x in stored)
        and all(x["parent_edge_overlap"] <= 0.90 for x in stored)
        and len(stored_edges) == len(stored)
    )

    return {
        "stored": stored,
        "proposals": proposals,
        "accepted_moves": accepted,
        "controls": controls,
    }


def sample_stage_b(
    parent,
    n,
    parent_seed,
    degrees,
    target,
    mean,
    sd,
    parent_pb,
    delta_pb,
):
    parent_edges = edge_set(parent)
    current_seq = tree_to_prufer(parent)
    current_cag = target.copy()
    current_pb = parent_pb

    rng = random.Random(11000017 * n + 104729 * parent_seed)

    accepted = 0
    proposals = 0
    stored = []
    stored_edges = set()

    def pb_match(value):
        if delta_pb == 0.0:
            return value == parent_pb
        return abs(value - parent_pb) <= delta_pb

    while proposals < 500000 and len(stored) < 99:
        proposals += 1
        i, j = rng.sample(range(len(current_seq)), 2)
        proposal_seq = list(current_seq)
        proposal_seq[i], proposal_seq[j] = proposal_seq[j], proposal_seq[i]

        if proposal_seq == current_seq:
            continue

        proposal = decode_explicit_prufer(proposal_seq, n)
        proposal_cag = cag(topology_vector(proposal), mean, sd)

        if not inside_box(proposal_cag, target):
            continue

        proposal_pb = branch_core_pair_connectivity(proposal)
        if not pb_match(proposal_pb):
            continue

        current_seq = proposal_seq
        current_cag = proposal_cag
        current_pb = proposal_pb
        accepted += 1

        if accepted <= 500:
            continue
        if (accepted - 500) % 50 != 0:
            continue

        edges = edge_set(proposal)
        overlap = len(edges & parent_edges) / (n - 1)

        if overlap > 0.90 or edges in stored_edges:
            continue

        stored_edges.add(edges)
        stored.append(
            {
                "adj": proposal,
                "CAG": current_cag.copy(),
                "PB": current_pb,
                "parent_edge_overlap": overlap,
            }
        )

    degree_control = all(degree_sequence(x["adj"]) == degrees for x in stored)
    tree_control = all(is_connected_tree(x["adj"]) for x in stored)
    cag_control = all(inside_box(x["CAG"], target) for x in stored)
    pb_control = all(pb_match(x["PB"]) for x in stored)
    diversity_control = (
        all(x["parent_edge_overlap"] <= 0.90 for x in stored)
        and len(stored_edges) == len(stored)
    )

    return {
        "stored": stored,
        "proposals": proposals,
        "accepted_moves": accepted,
        "feasible": len(stored) == 99,
        "degree_control": degree_control,
        "tree_control": tree_control,
        "cag_control": cag_control,
        "pb_control": pb_control,
        "diversity_control": diversity_control,
    }


def run_parent(n, parent_seed):
    parent = generate(n, parent_seed)
    degrees = degree_sequence(parent)

    mean, sd = baseline_stats(n, parent_seed, degrees)
    target = cag(topology_vector(parent), mean, sd)
    parent_pb = branch_core_pair_connectivity(parent)

    stage_a = sample_stage_a(
        parent, n, parent_seed, degrees, target, mean, sd
    )

    result = {
        "n": n,
        "parent_seed": parent_seed,
        "target_CAG": [float(x) for x in target],
        "parent_PB": float(parent_pb),
        "stage_a": {
            "proposals": stage_a["proposals"],
            "accepted_moves": stage_a["accepted_moves"],
            "stored_nulls": len(stage_a["stored"]),
            "controls_pass": stage_a["controls"],
        },
    }

    if not stage_a["controls"]:
        return result

    stage_a_pb = np.asarray(
        [branch_core_pair_connectivity(x["adj"]) for x in stage_a["stored"]],
        dtype=float,
    )
    sigma_pb = float(stage_a_pb.std())
    delta_pb = 0.50 * sigma_pb

    result["stage_a"]["PB"] = summarize(stage_a_pb)
    result["stage_a"]["sigma_PB"] = sigma_pb
    result["stage_a"]["delta_PB"] = delta_pb

    stage_b = sample_stage_b(
        parent,
        n,
        parent_seed,
        degrees,
        target,
        mean,
        sd,
        parent_pb,
        delta_pb,
    )

    result["stage_b"] = {
        "proposals": stage_b["proposals"],
        "accepted_moves": stage_b["accepted_moves"],
        "stored_nulls": len(stage_b["stored"]),
        "feasible": stage_b["feasible"],
        "degree_control": stage_b["degree_control"],
        "tree_control": stage_b["tree_control"],
        "cag_control": stage_b["cag_control"],
        "pb_control": stage_b["pb_control"],
        "diversity_control": stage_b["diversity_control"],
    }

    if not (
        stage_b["feasible"]
        and stage_b["degree_control"]
        and stage_b["tree_control"]
        and stage_b["cag_control"]
        and stage_b["pb_control"]
        and stage_b["diversity_control"]
    ):
        return result

    parent_m3, parent_m7 = m3_m7(parent)
    null_m3 = []
    null_m7 = []
    null_pb = []
    overlaps = []

    for item in stage_b["stored"]:
        m3, m7 = m3_m7(item["adj"])
        null_m3.append(m3)
        null_m7.append(m7)
        null_pb.append(item["PB"])
        overlaps.append(item["parent_edge_overlap"])

    result["stage_b"]["PB"] = summarize(null_pb)
    result["stage_b"]["M3"] = summarize_heldout(parent_m3, null_m3)
    result["stage_b"]["M7"] = summarize_heldout(parent_m7, null_m7)
    result["stage_b"]["parent_edge_overlap"] = summarize(overlaps)

    return result


def run():
    rows = [run_parent(2048, seed) for seed in (389, 419, 449)]

    baseline_feasible = all(
        row.get("stage_a", {}).get("controls_pass", False)
        for row in rows
    )

    intervention_feasible = all(
        row.get("stage_b", {}).get("feasible", False)
        and row.get("stage_b", {}).get("degree_control", False)
        and row.get("stage_b", {}).get("tree_control", False)
        and row.get("stage_b", {}).get("cag_control", False)
        and row.get("stage_b", {}).get("pb_control", False)
        and row.get("stage_b", {}).get("diversity_control", False)
        for row in rows
    )

    accounting = bool(
        baseline_feasible
        and intervention_feasible
        and all(
            row["stage_b"]["M3"]["classification"] == "inside"
            and row["stage_b"]["M7"]["classification"] == "inside"
            for row in rows
        )
    )

    residual = bool(
        baseline_feasible
        and intervention_feasible
        and all(
            row["stage_b"]["M3"]["classification"] == "high"
            and row["stage_b"]["M7"]["classification"] == "high"
            for row in rows
        )
    )

    return {
        "protocol": "T46 frozen",
        "N": 2048,
        "seeds": [389, 419, 449],
        "rows": rows,
        "baseline_feasibility": baseline_feasible,
        "intervention_feasibility": intervention_feasible,
        "high_radius_accounting": accounting,
        "residual_specificity_after_PB": residual,
        "guard": (
            "Only C/A/G/PB enter matching; M3/M7 held out until Stage B is frozen; "
            "no rescue seeds, tolerance relaxation, extra topology variable, "
            "graph dynamics, transition law, or physical geometry."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
