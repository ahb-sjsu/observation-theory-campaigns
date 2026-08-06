#!/usr/bin/env python3
"""GG-0 exact gauge-orbit instrument layer (exploratory).

Protocol declared in GAUGE-TRACK.md before this run. Z2 gauge
theory on a 3 by 3 periodic lattice, 18 links, all 2^18
configurations enumerated exactly at K = 0.4. Orbit structure,
route agreement against the tree-gauge-fixed enumeration and the
exact torus closed form, and the Elitzur control with the
gauge-fixed observer's nonzero bookkeeping recorded. Verdict
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

from projection_fold import canonical_sha256  # noqa: E402

LSIZE = 3
NLINK = 2 * LSIZE * LSIZE  # horizontal then vertical
K = 0.4


def link_index(kind, i, j):
    # kind 0: horizontal from (i,j) to (i,(j+1)%3)
    # kind 1: vertical from (i,j) to ((i+1)%3,j)
    return kind * 9 + i * LSIZE + j


def plaquette_links():
    plaqs = []
    for i in range(LSIZE):
        for j in range(LSIZE):
            plaqs.append([link_index(0, i, j),
                          link_index(1, i, (j + 1) % LSIZE),
                          link_index(0, (i + 1) % LSIZE, j),
                          link_index(1, i, j)])
    return plaqs


def all_configs():
    idx = np.arange(2 ** NLINK, dtype=np.int64)
    bits = (idx[:, None] >> np.arange(NLINK)) & 1
    return (1 - 2 * bits).astype(np.int8)  # bit 0 -> +1


def gauge_transform(cfg, site_signs):
    out = cfg.copy()
    for i in range(LSIZE):
        for j in range(LSIZE):
            g = site_signs[i, j]
            for kind, ni, nj in ((0, i, (j + 1) % LSIZE),
                                 (1, (i + 1) % LSIZE, j)):
                li = link_index(kind, i, j)
                out[li] = out[li] * g * site_signs[ni, nj]
    return out


def action(cfg, plaqs):
    return K * sum(cfg[a] * cfg[b] * cfg[c] * cfg[d]
                   for a, b, c, d in plaqs)


def main() -> int:
    record: dict = {"schema": "gg0-instrument-v1",
                    "label": "exploratory"}
    items = {}
    plaqs = plaquette_links()
    cfgs = all_configs()
    plaq_prod = np.ones((cfgs.shape[0], 9), dtype=np.int8)
    for p, (a, b, c, d) in enumerate(plaqs):
        plaq_prod[:, p] = (cfgs[:, a] * cfgs[:, b]
                           * cfgs[:, c] * cfgs[:, d])
    s = K * plaq_prod.sum(axis=1, dtype=np.float64)
    w = np.exp(s)
    z = math.fsum(w)

    # C1 orbit structure on 200 seeded configurations
    rng = np.random.RandomState(20260812)
    site_patterns = [(1 - 2 * ((g >> np.arange(9)) & 1)).reshape(
        LSIZE, LSIZE) for g in range(2 ** 9)]
    max_action_dev = 0.0
    orbit_sizes = []
    ok_pow2 = True
    for _ in range(200):
        cfg = (1 - 2 * rng.randint(0, 2, NLINK)).astype(np.int8)
        base = action(cfg, plaqs)
        seen = set()
        for sp in site_patterns:
            tc = gauge_transform(cfg, sp)
            max_action_dev = max(max_action_dev,
                                 abs(action(tc, plaqs) - base))
            seen.add(tc.tobytes())
        n = len(seen)
        orbit_sizes.append(n)
        ok_pow2 = ok_pow2 and (512 % n == 0) and (n & (n - 1) == 0)
    items["C1_orbit_structure"] = (max_action_dev == 0.0
                                   and ok_pow2)

    # C2 route agreement and closed form
    wp_full = math.fsum(plaq_prod[:, 0] * w) / z
    # tree gauge, fix a spanning tree of links to +1
    tree = [link_index(0, i, j) for i in range(LSIZE)
            for j in range(LSIZE - 1)]
    tree += [link_index(1, i, 0) for i in range(LSIZE - 1)]
    mask = np.ones(cfgs.shape[0], dtype=bool)
    for li in tree:
        mask &= cfgs[:, li] == 1
    wp_fixed = (math.fsum(plaq_prod[mask, 0] * w[mask])
                / math.fsum(w[mask]))
    t = np.tanh(K)
    wp_closed = (t + t ** 8) / (1 + t ** 9)
    dev2 = max(abs(wp_full - wp_fixed), abs(wp_full - wp_closed))
    items["C2_route_and_closed_form"] = dev2 <= 1e-12

    # C3 Elitzur control and the gauge-fixed observer's bookkeeping
    link_exp_full = np.array(
        [abs(math.fsum(cfgs[:, li].astype(np.float64) * w))
         for li in range(NLINK)]) / z
    dev3 = float(link_exp_full.max())
    zm = math.fsum(w[mask])
    link_exp_fixed = np.array(
        [math.fsum(cfgs[mask, li].astype(np.float64) * w[mask])
         for li in range(NLINK)]) / zm
    nontree = [li for li in range(NLINK) if li not in tree]
    fixed_max = float(np.max(np.abs(link_exp_fixed[nontree])))
    items["C3_elitzur"] = dev3 <= 1e-13

    record["measured"] = {
        "z_log": float(np.log(z)),
        "max_action_dev_on_orbits": float(max_action_dev),
        "orbit_sizes_counts": {str(n): orbit_sizes.count(n)
                               for n in sorted(set(orbit_sizes))},
        "wilson_plaquette_full": wp_full,
        "wilson_plaquette_tree_fixed": wp_fixed,
        "wilson_plaquette_closed_form": float(wp_closed),
        "elitzur_max_link_exp": dev3,
        "tree_fixed_max_nontree_link_exp": fixed_max,
        "note_c3": "the gauge-fixed observer's nonzero link "
                   "readings are its bookkeeping, recorded"}
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
        / "gg0-instrument.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("wilson", wp_full, wp_fixed, wp_closed,
          "elitzur", dev3, "fixed obs", fixed_max)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
