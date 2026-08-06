#!/usr/bin/env python3
"""GG-1 consumer-invariance across gauge-fixed observers.

Protocol declared in GAUGE-TRACK.md before this run. Three declared
spanning-tree observers on the GG-0 substrate. Gauge-invariant
observables agree across every observer to machine precision, and
every observer's gauge-variant link reading equals the
full-ensemble expectation of the loop its tree selects, with the
GF(2) plaquette decomposition certifying contractible loops against
the exact closed form and winding loops against zero. Verdict
computed from the measured items.

Exploratory label. No claim about continuum gauge theory.
"""
from __future__ import annotations

import json
import math
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gg0_instrument import (  # noqa: E402
    K, LSIZE, NLINK, all_configs, link_index, plaquette_links)
from projection_fold import canonical_sha256  # noqa: E402


def link_ends(li):
    kind, rest = divmod(li, 9)
    i, j = divmod(rest, LSIZE)
    if kind == 0:
        return (i, j), (i, (j + 1) % LSIZE)
    return (i, j), ((i + 1) % LSIZE, j)


def tree_paths(tree):
    """BFS paths (as link sets) from site (0,0) to every site."""
    adj: dict = {}
    for li in tree:
        a, b = link_ends(li)
        adj.setdefault(a, []).append((b, li))
        adj.setdefault(b, []).append((a, li))
    paths = {(0, 0): frozenset()}
    frontier = [(0, 0)]
    while frontier:
        nxt = []
        for u in frontier:
            for v, li in adj.get(u, []):
                if v not in paths:
                    paths[v] = paths[u] ^ {li}
                    nxt.append(v)
        frontier = nxt
    assert len(paths) == 9, "tree must span"
    return paths


def gf2_solve(bmat, target):
    """Solve bmat x = target over GF(2); return x or None."""
    m = np.concatenate([bmat.copy(), target[:, None]], axis=1) % 2
    rows, cols = m.shape[0], bmat.shape[1]
    piv = []
    r = 0
    for c in range(cols):
        rr = next((i for i in range(r, rows) if m[i, c]), None)
        if rr is None:
            continue
        m[[r, rr]] = m[[rr, r]]
        for i in range(rows):
            if i != r and m[i, c]:
                m[i] ^= m[r]
        piv.append(c)
        r += 1
    if any(m[i, -1] for i in range(r, rows)):
        return None
    x = np.zeros(cols, dtype=np.int64)
    for idx, c in enumerate(piv):
        x[c] = m[idx, -1]
    return x


def main() -> int:
    record: dict = {"schema": "gg1-observer-family-v1",
                    "label": "exploratory"}
    items = {}
    plaqs = plaquette_links()
    cfgs = all_configs()
    plaq_prod = np.ones((cfgs.shape[0], 9), dtype=np.int8)
    for p, (a, b, c, d) in enumerate(plaqs):
        plaq_prod[:, p] = (cfgs[:, a] * cfgs[:, b]
                           * cfgs[:, c] * cfgs[:, d])
    w = np.exp(K * plaq_prod.sum(axis=1, dtype=np.float64))
    z = math.fsum(w)

    def full_exp(cols):
        prod = np.ones(cfgs.shape[0], dtype=np.float64)
        for li in cols:
            prod *= cfgs[:, li]
        return math.fsum(prod * w) / z

    trees = {
        "A": [link_index(0, i, j) for i in range(3)
              for j in range(2)]
        + [link_index(1, i, 0) for i in range(2)],
        "B": [link_index(1, i, j) for i in range(2)
              for j in range(3)]
        + [link_index(0, 0, j) for j in range(2)],
        "snake": [link_index(0, 0, 0), link_index(0, 0, 1),
                  link_index(1, 0, 2), link_index(0, 1, 1),
                  link_index(0, 1, 0), link_index(1, 1, 0),
                  link_index(0, 2, 0), link_index(0, 2, 1)]}

    loop2 = frozenset(plaqs[0]) ^ frozenset(plaqs[1])
    invariants = {f"plaquette_{p}": plaqs[p] for p in range(9)}
    invariants["loop_area2"] = sorted(loop2)
    full_inv = {k: full_exp(cols) for k, cols in invariants.items()}

    bmat = np.zeros((NLINK, 9), dtype=np.int64)
    for p, links in enumerate(plaqs):
        for li in links:
            bmat[li, p] = 1
    t = np.tanh(K)

    dev_g1 = 0.0
    dev_g2 = 0.0
    dev_wind = 0.0
    readings = {}
    n_wind = 0
    for name, tree in trees.items():
        mask = np.ones(cfgs.shape[0], dtype=bool)
        for li in tree:
            mask &= cfgs[:, li] == 1
        zm = math.fsum(w[mask])

        def slice_exp(cols, mask=mask, zm=zm):
            prod = np.ones(int(mask.sum()), dtype=np.float64)
            sub = cfgs[mask]
            for li in cols:
                prod *= sub[:, li]
            return math.fsum(prod * w[mask]) / zm

        for k2, cols in invariants.items():
            dev_g1 = max(dev_g1, abs(slice_exp(cols)
                                     - full_inv[k2]))
        paths = tree_paths(tree)
        obs = {}
        for li in range(NLINK):
            reading = slice_exp([li])
            obs[li] = reading
            if li in tree:
                continue
            a, b = link_ends(li)
            loop = frozenset({li}) ^ paths[a] ^ paths[b]
            pred = full_exp(sorted(loop))
            dev_g2 = max(dev_g2, abs(reading - pred))
            lv = np.zeros(NLINK, dtype=np.int64)
            for x in loop:
                lv[x] = 1
            sol = gf2_solve(bmat, lv)
            if sol is None:
                n_wind += 1
                dev_wind = max(dev_wind, abs(reading))
            else:
                area = int(sol.sum())
                closed = (t ** area + t ** (9 - area)) \
                    / (1 + t ** 9)
                dev_g2 = max(dev_g2, abs(reading - closed))
        readings[name] = {str(li): float(v)
                          for li, v in obs.items()}

    spread = 0.0
    names = list(trees)
    for li in range(NLINK):
        vals = [readings[nm][str(li)] for nm in names]
        spread = max(spread, max(vals) - min(vals))
    elitzur = max(abs(full_exp([li])) for li in range(NLINK))

    items["G1_invariants_agree"] = dev_g1 <= 1e-12
    items["G2_detector_model_exact"] = (dev_g2 <= 1e-12
                                        and dev_wind <= 1e-13)
    items["G3_observers_disagree"] = (spread >= 0.1
                                      and elitzur <= 1e-13)

    record["measured"] = {
        "g1_max_dev": float(dev_g1),
        "g2_max_dev": float(dev_g2),
        "winding_loops_found": int(n_wind),
        "winding_max_reading": float(dev_wind),
        "max_pairwise_link_spread": float(spread),
        "elitzur_full": float(elitzur),
        "wilson_plaquette_full": float(full_inv["plaquette_0"]),
        "loop_area2_full": float(full_inv["loop_area2"])}
    record["items"] = {k: bool(v) for k, v in items.items()}
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "gg1-observer-family.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("g1", dev_g1, "g2", dev_g2, "wind", n_wind, dev_wind,
          "spread", spread)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
