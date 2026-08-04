#!/usr/bin/env python3
"""WM-4 held-out dimension scaling on a hypergraph rule (exploratory).

A minimal Wolfram-model rewriter for the rule

    {{x, y}, {x, z}} -> {{x, z}, {x, w}, {y, w}, {z, w}}

with w fresh, from the double self-loop initial condition, updated in
generations (a maximal scan-ordered set of non-overlapping matches per
generation, the declared prescription; the WM-2 lesson that
prescriptions matter is on the record, and this run declares exactly
one). The grown spatial hypergraph is read as a simple graph and its
dimension is measured with the WM-0-validated shell estimator, in the
PF-4 pattern: a training radius window fits the power law, held-out
larger radii test it, and the preregistered-style alternative
(exponential shell growth, the tree signature) competes on the same
held-out shells. The verdict is reported at measured sizes only, per
the track document's finite-size qualifier. No assertion picks a
winner; the record carries both residuals.

Exploratory label.
"""
from __future__ import annotations

import json
import math
import os
import platform
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402
from wm0_dimension import ball_volumes  # noqa: E402

GENERATIONS = 11
TRAIN_WINDOW = (2, 5)
HELD_WINDOW = (6, 9)
N_SOURCES = 30
SEED = 20260805


def rewrite_generations(n_generations: int):
    relations = [(0, 0), (0, 0)]
    next_vertex = 1
    for _ in range(n_generations):
        by_first = defaultdict(list)
        for idx, rel in enumerate(relations):
            by_first[rel[0]].append(idx)
        used = set()
        events = []
        for idx in range(len(relations)):
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
        new_relations = [rel for i, rel in enumerate(relations)
                         if i not in used]
        for idx, partner in events:
            x, y = relations[idx]
            _, z = relations[partner]
            w = next_vertex
            next_vertex += 1
            new_relations.extend([(x, z), (x, w), (y, w), (z, w)])
        relations = new_relations
    return relations, next_vertex


def spatial_graph(relations) -> dict:
    adjacency = defaultdict(set)
    for a, b in relations:
        if a != b:
            adjacency[a].add(b)
            adjacency[b].add(a)
    return {v: list(nbrs) for v, nbrs in adjacency.items()}


def shell_profile(adjacency, sources, r_max):
    shells = []
    for s in sources:
        v = ball_volumes(adjacency, s, r_max)
        if len(v) <= r_max:
            continue
        shells.append([v[r] - v[r - 1] for r in range(1, r_max + 1)])
    return np.mean(np.array(shells), axis=0)


def fit_and_test(shells):
    lo_t, hi_t = TRAIN_WINDOW
    lo_h, hi_h = HELD_WINDOW
    r_train = np.arange(lo_t, hi_t + 1)
    r_held = np.arange(lo_h, hi_h + 1)
    s_train = shells[lo_t - 1:hi_t]
    s_held = shells[lo_h - 1:hi_h]

    power_coef = np.polyfit(np.log(r_train), np.log(s_train), 1)
    power_pred = np.exp(np.polyval(power_coef, np.log(r_held)))
    power_sse = float(np.sum((np.log(s_held) - np.log(power_pred)) ** 2))

    exp_coef = np.polyfit(r_train, np.log(s_train), 1)
    exp_pred = np.exp(np.polyval(exp_coef, r_held))
    exp_sse = float(np.sum((np.log(s_held) - np.log(exp_pred)) ** 2))

    return {
        "d_hat_train": float(power_coef[0]) + 1.0,
        "power_law_held_sse": power_sse,
        "exponential_held_sse": exp_sse,
        "held_shells_measured": [float(x) for x in s_held],
        "held_shells_power_pred": [float(x) for x in power_pred],
        "held_shells_exp_pred": [float(x) for x in exp_pred],
    }


def main() -> int:
    relations, n_vertices = rewrite_generations(GENERATIONS)
    adjacency = spatial_graph(relations)
    rng = np.random.RandomState(SEED)
    keys = list(adjacency)
    sources = [keys[i] for i in rng.choice(len(keys), N_SOURCES,
                                           replace=False)]
    shells = shell_profile(adjacency, sources, HELD_WINDOW[1])
    fits = fit_and_test(shells)

    winner = ("finite-dimension power law"
              if fits["power_law_held_sse"] < fits["exponential_held_sse"]
              else "exponential growth")
    record = {
        "schema": "wm4-hypergraph-v1",
        "label": "exploratory",
        "declared": {
            "rule": "{{x,y},{x,z}} -> {{x,z},{x,w},{y,w},{z,w}}",
            "initial": "double self-loop", "generations": GENERATIONS,
            "prescription": "generational maximal scan-ordered "
                            "non-overlapping matching, declared single "
                            "prescription",
            "train_window": TRAIN_WINDOW, "held_window": HELD_WINDOW,
            "n_sources": N_SOURCES, "seed": SEED,
        },
        "graph": {"n_relations": len(relations),
                  "n_vertices": len(adjacency)},
        "fits": fits,
        "held_out_winner_at_measured_sizes": winner,
        "statement": "the verdict holds at measured sizes only; a "
            "finite-size crossover beyond the held-out window cannot be "
            "excluded, per the track document's qualifier",
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
        / "wm4-hypergraph.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print(f"graph: {len(relations)} relations, {len(adjacency)} vertices")
    print(f"d_hat(train) = {fits['d_hat_train']:.3f}; held-out SSE "
          f"power {fits['power_law_held_sse']:.4f} vs exponential "
          f"{fits['exponential_held_sse']:.4f} -> {winner}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
