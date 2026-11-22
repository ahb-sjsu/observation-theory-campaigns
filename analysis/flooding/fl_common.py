"""Shared pieces of the FL track (IS-IS flood reduction in FRR, measured with topology-builders): reading `measure`
records, the link-change LSP saving per topology, and the two-hop multiplicity of a graph.

The saving is defined as `topology-builders report` defines it, recomputed here so the track does not depend on
that code: over every link-down and link-up window of every run of one topology file, 1 - mean LSPs sent with flood
reduction on / mean LSPs sent with it off (Level-2 LSPs, summed over the routers). Timing runs are left out."""
import gzip
import hashlib
import json
import os

import networkx as nx

LINK_PHASES = ("link-down", "link-up")


def read(path):
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8") as fh:
        return [json.loads(x) for x in fh if x.strip()]


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load_graph(path):
    with open(path, encoding="utf-8") as fh:
        return nx.node_link_graph(json.load(fh), edges="edges")


def topology_index(directory):
    """sha256 -> path of every topology file under `directory` (manifest and lab files left out)."""
    out = {}
    for root, _, names in os.walk(directory):
        for n in sorted(names):
            if n.endswith(".json") and n not in ("manifest.json", "lab.json"):
                p = os.path.join(root, n)
                out.setdefault(sha256(p), p)
    return out


def two_hop_multiplicity(g):
    """Mean, over ordered pairs of routers exactly two hops apart, of the number of neighbors they share."""
    adj = {u: set(g.neighbors(u)) for u in g}
    total = pairs = 0
    for u, nu in adj.items():
        counts = {}
        for x in nu:
            for w in adj[x]:
                if w != u:
                    counts[w] = counts.get(w, 0) + 1
        for w, c in counts.items():
            if w not in nu:
                total += c
                pairs += 1
    return total / pairs if pairs else None


def by_topology(records):
    """Records of non-timing runs grouped by the sha256 of the topology file their labs were written from."""
    out = {}
    for r in records:
        if not r.get("timing"):
            out.setdefault(r["source_sha256"], []).append(r)
    return out


def lsp_saving(records):
    """(saving, off windows, on windows) over the link windows of one topology's records; saving None if a side
    has no window."""
    lsps = {False: [], True: []}
    for r in records:
        on = bool(r["settings"]["flood_reduction"])
        lsps[on] += [p["counters"].get("tx_l2_lsp", 0) for p in r["phases"] if p["phase"] in LINK_PHASES]
    if not lsps[False] or not lsps[True] or sum(lsps[False]) == 0:
        return None, len(lsps[False]), len(lsps[True])
    off, on = sum(lsps[False]) / len(lsps[False]), sum(lsps[True]) / len(lsps[True])
    return 1 - on / off, len(lsps[False]), len(lsps[True])


def isotonic(xs, ys):
    """Pool-adjacent-violators: the non-decreasing least-squares fit of ys on xs (equal xs averaged first).
    Returns the knots [(x, fitted y)], sorted by x."""
    pts = {}
    for x, y in zip(xs, ys, strict=True):
        pts.setdefault(x, []).append(y)
    blocks = [[x, sum(v) / len(v), len(v)] for x, v in sorted(pts.items())]  # x, mean, weight
    merged = []
    for b in blocks:
        merged.append([[b[0]], b[1], b[2]])
        while len(merged) > 1 and merged[-2][1] > merged[-1][1]:
            xs2, m2, w2 = merged.pop()
            xs1, m1, w1 = merged.pop()
            merged.append([xs1 + xs2, (m1 * w1 + m2 * w2) / (w1 + w2), w1 + w2])
    return [(x, m) for xs_, m, _ in merged for x in xs_]


def interpolate(knots, x):
    """Piecewise-linear through the knots, constant beyond the first and last."""
    if x <= knots[0][0]:
        return knots[0][1]
    if x >= knots[-1][0]:
        return knots[-1][1]
    for (x0, y0), (x1, y1) in zip(knots, knots[1:], strict=False):
        if x0 <= x <= x1:
            return y0 if x1 == x0 else y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return knots[-1][1]
