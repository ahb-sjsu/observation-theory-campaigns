#!/usr/bin/env python3
"""WM-3 foliation-covariance audit (exploratory, WM track).

Events of a string rewriting run form a causal graph once token
genealogy is tracked: an event depends on the events that produced the
tokens it consumes. A foliation is any antichain layering respecting
the partial order, and different foliations are different observers.
The audit separates causal-graph quantities into the invariant and the
foliation-borne, and separately checks the prescription face: for the
causal-invariant sorting rule the causal-graph invariants must agree
across update orders, while the planted non-confluent rule must
disagree.

Systems and prescriptions are those of WM-2. Foliations sampled: the
earliest layering (each event as soon as its parents are done), the
latest layering (each event as late as its children allow), and seeded
random linear extensions grouped greedily into antichains. Invariant
witnesses: event count, causal-edge count, depth (longest chain), and
the degree-sequence multiset. Foliation-borne witnesses: slice count,
maximum and mean slice width. The earliest and latest layerings both
achieve exactly depth slices, random extensions at least that, and the
spread between them is the measured content of the statement that
simultaneity is bookkeeping.

Exploratory label.
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

SEED = 20260805
STRING_LENGTH = 24
N_RANDOM_FOLIATIONS = 5


def evolve_with_causal_graph(initial: str, rules, prescription: str,
                             *, max_events: int = 10_000):
    """Rewriting with token genealogy. Returns the causal edge set."""
    tokens = [(c, -1) for c in initial]  # (char, producer event id)
    edges = set()
    n_events = 0
    while n_events < max_events:
        state = "".join(c for c, _ in tokens)
        found = []
        for lhs, rhs in rules:
            start = 0
            while True:
                i = state.find(lhs, start)
                if i < 0:
                    break
                found.append((i, lhs, rhs))
                start = i + 1
        if not found:
            break
        found.sort(key=lambda m: (m[0], m[1]))
        pick = found[0] if prescription == "leftmost" else found[-1]
        i, lhs, rhs = pick
        event = n_events
        for _, producer in tokens[i:i + len(lhs)]:
            if producer >= 0:
                edges.add((producer, event))
        tokens[i:i + len(lhs)] = [(c, event) for c in rhs]
        n_events += 1
    return n_events, edges


def graph_invariants(n_events: int, edges: set) -> dict:
    children = defaultdict(list)
    indeg = defaultdict(int)
    for a, b in edges:
        children[a].append(b)
        indeg[b] += 1
    level = {}
    order = []
    frontier = [e for e in range(n_events) if indeg[e] == 0]
    seen_indeg = dict(indeg)
    while frontier:
        nxt = []
        for e in frontier:
            level[e] = max((level[p] + 1 for p, c in edges if c == e),
                           default=0) if indeg[e] else 0
            order.append(e)
            for c in children[e]:
                seen_indeg[c] -= 1
                if seen_indeg[c] == 0:
                    nxt.append(c)
        frontier = nxt
    for e in order:
        parents = [p for p, c in edges if c == e]
        level[e] = 1 + max((level[p] for p in parents), default=-1)
    depth = 1 + max(level.values()) if level else 0
    degs = sorted((len(children[e]) for e in range(n_events)))
    return {"n_events": n_events, "n_edges": len(edges), "depth": depth,
            "out_degree_multiset": degs, "earliest_level": level}


def foliation_stats(n_events, edges, assignment) -> dict:
    slices = defaultdict(int)
    for e in range(n_events):
        slices[assignment[e]] += 1
    widths = [slices[s] for s in sorted(slices)]
    return {"n_slices": len(widths), "max_width": max(widths),
            "mean_width": float(np.mean(widths))}


def latest_levels(n_events, edges, depth) -> dict:
    parents = defaultdict(list)
    children = defaultdict(list)
    for a, b in edges:
        parents[b].append(a)
        children[a].append(b)
    level = {}
    for e in reversed(range(n_events)):
        below = [level[c] for c in children[e]]
        level[e] = (min(below) - 1) if below else (depth - 1)
    return level


def random_extension_foliation(n_events, edges, rng) -> dict:
    parents = defaultdict(set)
    children = defaultdict(list)
    for a, b in edges:
        parents[b].add(a)
        children[a].append(b)
    remaining = {e: set(parents[e]) for e in range(n_events)}
    ready = [e for e in range(n_events) if not remaining[e]]
    done = set()
    assignment = {}
    slice_id = 0
    current = set()
    while ready:
        e = ready.pop(rng.randint(len(ready)))
        if remaining[e] & current or any(p in current for p in parents[e]):
            slice_id += 1
            current = set()
        if any(p not in done for p in parents[e]):
            pass
        assignment[e] = slice_id
        current.add(e)
        done.add(e)
        for c in children[e]:
            remaining[c].discard(e)
            if not remaining[c] and c not in done and c not in ready:
                ready.append(c)
    return assignment


def main() -> int:
    rng = np.random.RandomState(SEED)
    initial = "".join(rng.choice(["A", "B"], STRING_LENGTH))
    sorting_rules = [("BA", "AB")]

    per_prescription = {}
    for p in ("leftmost", "rightmost"):
        n_events, edges = evolve_with_causal_graph(initial, sorting_rules, p)
        inv = graph_invariants(n_events, edges)
        per_prescription[p] = {
            "n_events": inv["n_events"], "n_edges": inv["n_edges"],
            "depth": inv["depth"],
            "out_degree_multiset": inv["out_degree_multiset"],
        }
    a, b = per_prescription["leftmost"], per_prescription["rightmost"]
    prescription_invariant = (
        a["n_events"] == b["n_events"] and a["n_edges"] == b["n_edges"]
        and a["depth"] == b["depth"]
        and a["out_degree_multiset"] == b["out_degree_multiset"]
    )
    assert prescription_invariant, \
        "sorting-rule causal invariants disagreed across prescriptions"

    trap_inv = {}
    for p in ("leftmost", "rightmost"):
        n_events, edges = evolve_with_causal_graph(
            "ABABABAB", [("AB", "B"), ("BA", "A")], p)
        trap_inv[p] = {"n_events": n_events, "n_edges": len(edges)}
    trap_flagged = trap_inv["leftmost"] != trap_inv["rightmost"]
    assert trap_flagged, "trap causal graphs failed to differ"

    n_events, edges = evolve_with_causal_graph(initial, sorting_rules,
                                               "leftmost")
    inv = graph_invariants(n_events, edges)
    depth = inv["depth"]
    earliest = foliation_stats(n_events, edges, inv["earliest_level"])
    latest = foliation_stats(n_events, edges,
                             latest_levels(n_events, edges, depth))
    randoms = []
    frng = np.random.RandomState(SEED + 9)
    for _ in range(N_RANDOM_FOLIATIONS):
        assignment = random_extension_foliation(n_events, edges, frng)
        randoms.append(foliation_stats(n_events, edges, assignment))

    assert earliest["n_slices"] == depth, "earliest layering must equal depth"
    assert latest["n_slices"] == depth, "latest layering must equal depth"
    for r in randoms:
        assert r["n_slices"] >= depth, "foliation beat the depth bound"

    slice_counts = [earliest["n_slices"], latest["n_slices"]] + \
        [r["n_slices"] for r in randoms]
    max_widths = [earliest["max_width"], latest["max_width"]] + \
        [r["max_width"] for r in randoms]

    record = {
        "schema": "wm3-foliation-v1",
        "label": "exploratory",
        "declared": {"seed": SEED, "string_length": STRING_LENGTH,
                     "n_random_foliations": N_RANDOM_FOLIATIONS},
        "prescription_face": {
            "sorting_invariants": per_prescription,
            "agree": True,
            "trap_invariants": trap_inv,
            "trap_flagged": True,
        },
        "foliation_face": {
            "invariants": {"n_events": inv["n_events"],
                           "n_edges": inv["n_edges"], "depth": depth},
            "earliest": earliest, "latest": latest, "randoms": randoms,
            "slice_count_range": [min(slice_counts), max(slice_counts)],
            "max_width_range": [min(max_widths), max(max_widths)],
        },
        "statement": "for the causal-invariant rule the causal-graph "
            "invariants are prescription-independent and "
            "foliation-independent, while slice counts and widths, the "
            "observer's simultaneity bookkeeping, vary across foliations "
            "between the depth bound and the sampled maximum; the "
            "non-confluent trap's causal graph itself differs across "
            "prescriptions",
        "runtime": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "numpy": np.__version__,
            "platform": platform.platform(),
            "hostname": platform.node(),
            "code_commit": os.environ.get("CODE_COMMIT", "unknown"),
        },
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"}
    )
    output = Path(__file__).resolve().parents[1] / "results" \
        / "wm3-foliation.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print(f"invariants: events {inv['n_events']}, edges {inv['n_edges']}, "
          f"depth {depth} (prescriptions agree exactly; trap differs "
          f"{trap_inv['leftmost']} vs {trap_inv['rightmost']})")
    print(f"foliations: slice counts {slice_counts} (depth bound {depth}), "
          f"max widths {max_widths}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
