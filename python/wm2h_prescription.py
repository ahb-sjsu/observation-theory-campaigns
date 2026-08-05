#!/usr/bin/env python3
"""WM-2h: the hypergraph prescription audit (exploratory, WM track).

The hypergraph version of WM-2, closing the WM track's last unbuilt
experiment. The WM-4 rewriter selects matches by scanning relation
indices in storage order, which is an update prescription, exactly
the object WM-2 audits. This runner reruns the same rule under four
declared prescriptions (storage order, reversed, two seeded
permutations, and sort by second vertex makes five) and classifies
each observable as prescription-invariant or prescription-borne.

Observables. Relation and vertex counts per run, the sorted degree
multiset of the spatial graph, and the WM-4 dimension estimate
(power-law fit of the shell profile with its held-out test), so the
audit directly asks whether the track's measured dimension claim is
prescription-robust at the same sizes.

Trap. A planted non-confluent contraction rule, two adjacent
relations x-y, y-z contract to x-z, run to exhaustion on a declared
path graph under the same prescriptions. Overlapping matches
conflict, so distinct terminal states must appear and be flagged,
proving the audit can catch prescription dependence.

Exploratory label. No physics claim.
"""
from __future__ import annotations

import json
import os
import platform
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402
from wm4_hypergraph import (  # noqa: E402
    fit_and_test,
    shell_profile,
    spatial_graph,
)

GENERATIONS = 11
N_SOURCES = 24
R_MAX = 9
SEED_SOURCES = 20260805
PRESCRIPTIONS = ("storage", "reversed", "shuffle_a", "shuffle_b",
                 "by_second")


def order_indices(name: str, relations) -> list[int]:
    idx = list(range(len(relations)))
    if name == "storage":
        return idx
    if name == "reversed":
        return idx[::-1]
    if name == "shuffle_a":
        rng = np.random.RandomState(11)
        return list(rng.permutation(len(relations)))
    if name == "shuffle_b":
        rng = np.random.RandomState(22)
        return list(rng.permutation(len(relations)))
    if name == "by_second":
        return sorted(idx, key=lambda k: (relations[k][1],
                                          relations[k][0], k))
    raise ValueError(name)


def rewrite(prescription: str, n_generations: int):
    relations = [(0, 0), (0, 0)]
    next_vertex = 1
    for _ in range(n_generations):
        by_first = defaultdict(list)
        order = order_indices(prescription, relations)
        rank = {k: r for r, k in enumerate(order)}
        for idx in order:
            by_first[relations[idx][0]].append(idx)
        used = set()
        events = []
        for idx in order:
            if idx in used:
                continue
            x = relations[idx][0]
            partner = next((j for j in by_first[x]
                            if j != idx and j not in used), None)
            if partner is None:
                continue
            used.add(idx)
            used.add(partner)
            events.append((idx, partner))
        new_relations = [rel for i, rel in
                         sorted(((i, r) for i, r in
                                 enumerate(relations) if i not in used),
                                key=lambda t: rank[t[0]])]
        for idx, partner in events:
            x, y = relations[idx]
            _, z = relations[partner]
            w = next_vertex
            next_vertex += 1
            new_relations.extend([(x, z), (x, w), (y, w), (z, w)])
        relations = new_relations
    return relations, next_vertex


def dimension_estimate(relations):
    adjacency = spatial_graph(relations)
    rng = np.random.RandomState(SEED_SOURCES)
    keys = sorted(adjacency)
    sources = [keys[i] for i in rng.choice(len(keys), N_SOURCES,
                                           replace=False)]
    shells = shell_profile(adjacency, sources, R_MAX)
    fits = fit_and_test(shells)
    return fits


def contraction_to_exhaustion(prescription: str, n_path: int):
    # a fork, not a path: path contraction is confluent (any order
    # composes to one edge, verified en route), while a fork forces
    # a choice of which branch survives composition
    relations = [(i, i + 1) for i in range(n_path)] \
        + [(n_path // 2, n_path + 10 + k) for k in range(3)]
    while True:
        order = order_indices(prescription, relations)
        match = None
        for idx in order:
            x, y = relations[idx]
            for jdx in order:
                if jdx == idx:
                    continue
                a, b = relations[jdx]
                if a == y:
                    match = (idx, jdx)
                    break
            if match:
                break
        if match is None:
            return tuple(sorted(relations))
        idx, jdx = match
        x, y = relations[idx]
        _, z = relations[jdx]
        relations = [r for k, r in enumerate(relations)
                     if k not in (idx, jdx)] + [(x, z)]


def main() -> int:
    runs = {}
    for p in PRESCRIPTIONS:
        relations, n_vertices = rewrite(p, GENERATIONS)
        degs = sorted(len(v) for v in
                      spatial_graph(relations).values())
        fits = dimension_estimate(relations)
        runs[p] = {"relations": len(relations),
                   "vertices": n_vertices,
                   "degree_multiset_head": degs[-8:],
                   "degree_sum": int(sum(degs)),
                   "dimension": float(fits["d_hat_train"]),
                   "power_vs_exp_sse": [fits["power_law_held_sse"],
                                        fits["exponential_held_sse"]]}
        print(f"{p}: rel {len(relations)}, vert {n_vertices}, "
              f"fits {runs[p]['dimension']}")

    rel_counts = {runs[p]["relations"] for p in PRESCRIPTIONS}
    vert_counts = {runs[p]["vertices"] for p in PRESCRIPTIONS}
    deg_sums = {runs[p]["degree_sum"] for p in PRESCRIPTIONS}
    dims = [runs[p]["dimension"] for p in PRESCRIPTIONS]
    dim_spread = (max(dims) - min(dims)) / max(np.mean(dims), 1e-300)

    terminals = {p: contraction_to_exhaustion(p, 12)
                 for p in PRESCRIPTIONS}
    distinct_terminals = len(set(terminals.values()))
    assert distinct_terminals >= 2, \
        "trap not flagged: contraction terminals all agree"

    invariant = {
        "relation_count": len(rel_counts) == 1,
        "vertex_count": len(vert_counts) == 1,
        "degree_sum": len(deg_sums) == 1,
        "dimension_within_5_percent": bool(dim_spread < 0.05),
    }
    verdict = (
        f"hypergraph prescription audit: relation counts "
        f"{sorted(rel_counts)}, vertex counts {sorted(vert_counts)}, "
        f"degree sums {sorted(deg_sums)} across five prescriptions "
        + ("are identical, the growth rule's bulk bookkeeping is "
           "prescription-invariant at measured sizes"
           if all([invariant['relation_count'],
                   invariant['vertex_count'],
                   invariant['degree_sum']]) else
           "DIFFER, the bulk bookkeeping is prescription-borne, "
           "recorded per prescription")
        + f"; the dimension estimate spans {min(dims):.3f} to "
        f"{max(dims):.3f} (spread {dim_spread:.3f}), so the WM-4 "
        f"dimension claim "
        + ("is prescription-robust within five percent"
           if invariant["dimension_within_5_percent"] else
           "carries a prescription dependence larger than five "
           "percent, a caveat the WM-4 record now inherits")
        + f"; the planted contraction trap is flagged with "
        f"{distinct_terminals} distinct terminals across "
        f"prescriptions, so the audit detects non-confluence")

    record = {
        "schema": "wm2h-prescription-v1", "label": "exploratory",
        "declared": {"generations": GENERATIONS,
                     "prescriptions": list(PRESCRIPTIONS),
                     "sources": N_SOURCES, "r_max": R_MAX,
                     "trap": "contraction x-y,y-z -> x-z on a "
                             "12-relation path with a 3-branch fork "
                             "at its midpoint, to exhaustion (a bare "
                             "path is confluent, verified en route)"},
        "runs": runs,
        "dimension_spread": float(dim_spread),
        "trap_distinct_terminals": distinct_terminals,
        "invariance": invariant,
        "verdict": verdict,
        "runtime": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version, "numpy": np.__version__,
            "platform": platform.platform(),
            "hostname": platform.node(),
            "code_commit": os.environ.get("CODE_COMMIT", "unknown")},
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "wm2h-prescription.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("invariance:", invariant)
    print("trap terminals distinct:", distinct_terminals)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
