#!/usr/bin/env python3
"""WM-0 dimension-estimator instrument net (exploratory, WM track).

The Wolfram program infers emergent spatial dimension from ball-volume
growth in causal or spatial hypergraphs. Per the campaign rule that no
claim-bearing measurement precedes a validated instrument, this net
validates the estimator on graphs of exactly known dimension before it
ever touches a rewriting rule.

Estimator: breadth-first ball volumes V(r) averaged over declared
source vertices, dimension estimate d-hat = slope of log V against
log r over the declared window. Exact controls: path (d = 1), 2D
torus (d = 2), 3D torus (d = 3), each within the sealed-style
tolerance. Diverging control: a regular tree, whose running local
slope must increase with radius and exceed every finite control, so a
claim of finite dimension on exponentially growing graphs is caught by
construction.

Exploratory label. No claim about any Wolfram rule is made here.
"""
from __future__ import annotations

import json
import math
import os
import platform
import sys
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402

TOLERANCE = 0.15
WINDOW = (2, 10)
N_SOURCES = 24
SEED = 20260805


def ball_volumes(adjacency: dict, source, r_max: int) -> list[int]:
    seen = {source}
    frontier = deque([source])
    volumes = [1]
    for _ in range(r_max):
        nxt = deque()
        for _ in range(len(frontier)):
            node = frontier.popleft()
            for nb in adjacency[node]:
                if nb not in seen:
                    seen.add(nb)
                    nxt.append(nb)
        frontier = nxt
        volumes.append(len(seen))
        if not frontier:
            break
    return volumes


def dimension_estimate(adjacency: dict, sources, r_max: int,
                       window=WINDOW) -> dict:
    lo, hi = window
    logs = []
    for s in sources:
        v = ball_volumes(adjacency, s, r_max)
        if len(v) <= hi:
            continue
        logs.append([math.log(v[r]) for r in range(lo, hi + 1)])
    mean_log_v = np.mean(np.array(logs), axis=0)
    log_r = np.log(np.arange(lo, hi + 1))
    slope = float(np.polyfit(log_r, mean_log_v, 1)[0])
    local = list(np.diff(mean_log_v) / np.diff(log_r))
    return {"d_hat": slope, "local_slopes": [float(x) for x in local]}


def path_graph(n: int) -> dict:
    return {i: [j for j in (i - 1, i + 1) if 0 <= j < n]
            for i in range(n)}


def torus_2d(n: int) -> dict:
    adj = {}
    for x in range(n):
        for y in range(n):
            adj[(x, y)] = [((x + 1) % n, y), ((x - 1) % n, y),
                           (x, (y + 1) % n), (x, (y - 1) % n)]
    return adj


def torus_3d(n: int) -> dict:
    adj = {}
    for x in range(n):
        for y in range(n):
            for z in range(n):
                adj[(x, y, z)] = [
                    ((x + 1) % n, y, z), ((x - 1) % n, y, z),
                    (x, (y + 1) % n, z), (x, (y - 1) % n, z),
                    (x, y, (z + 1) % n), (x, y, (z - 1) % n)]
    return adj


def regular_tree(branching: int, depth: int) -> dict:
    adj = {0: []}
    nxt = 1
    frontier = [0]
    for _ in range(depth):
        newf = []
        for node in frontier:
            for _ in range(branching):
                adj[node].append(nxt)
                adj[nxt] = [node]
                newf.append(nxt)
                nxt += 1
        frontier = newf
    return adj


def main() -> int:
    rng = np.random.RandomState(SEED)

    controls = {}
    graph = path_graph(600)
    sources = rng.choice(np.arange(150, 450), N_SOURCES, replace=False)
    controls["path_d1"] = dimension_estimate(graph, list(sources), 24)

    graph = torus_2d(40)
    keys = list(graph)
    sources = [keys[i] for i in
               rng.choice(len(keys), N_SOURCES, replace=False)]
    controls["torus_d2"] = dimension_estimate(graph, sources, 16)

    graph = torus_3d(14)
    keys = list(graph)
    sources = [keys[i] for i in
               rng.choice(len(keys), N_SOURCES, replace=False)]
    controls["torus_d3"] = dimension_estimate(graph, sources, 6,
                                              window=(1, 5))

    tree = regular_tree(3, 12)
    tree_est = dimension_estimate(tree, [0], 11, window=(2, 10))
    controls["tree_diverging"] = tree_est

    for name, target in (("path_d1", 1.0), ("torus_d2", 2.0),
                         ("torus_d3", 3.0)):
        err = abs(controls[name]["d_hat"] - target)
        assert err < TOLERANCE, f"{name} failed: {controls[name]['d_hat']}"
    slopes = tree_est["local_slopes"]
    assert slopes[-1] > slopes[0], "tree local slope must increase"
    assert tree_est["d_hat"] > 4.0, "tree must exceed every finite control"

    record = {
        "schema": "wm0-dimension-v1",
        "label": "exploratory",
        "declared": {"tolerance": TOLERANCE, "window": WINDOW,
                     "n_sources": N_SOURCES, "seed": SEED},
        "controls": controls,
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
        / "wm0-dimension.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    for name, entry in controls.items():
        print(f"{name}: d_hat {entry['d_hat']:.3f}, local slopes "
              f"{[round(s, 2) for s in entry['local_slopes'][:4]]}...")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
