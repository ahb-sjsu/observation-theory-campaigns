"""Derive a realistic per-link CHANNEL-FILL distribution from a real SNDlib demand
matrix (janos-us-ca: US-Canada backbone, 39 nodes, 1482 demands), to ground the
heterogeneous fill in the XPROTO-QOT capacity result (OFC Sec. 3.2).

Route each demand on the shortest (hop) path, aggregate per link, and normalise so
the busiest link is a full C-band (76 ch). The spread of per-link fill is the real
heterogeneity a single uniform margin cannot fit. Emits SNDlib-fill.json.

    python sndlib_fill.py data/janos-us-ca.txt     (fetch: SNDlib native bundle)
"""
from __future__ import annotations

import json
import os
import re
import sys

import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_FILL = 76
MIN_FILL = 2


def main(path=os.path.join(HERE, "data", "janos-us-ca.txt")):
    txt = open(path, encoding="latin1").read()
    li, di = txt.index("LINKS ("), txt.index("DEMANDS (")
    links = re.findall(r"\bL\d+\s*\(\s*(\w+)\s+(\w+)\s*\)", txt[li:di])
    dems = re.findall(r"\bD\d+\s*\(\s*(\w+)\s+(\w+)\s*\)\s+\d+\s+([\d.]+)", txt[di:])
    g = nx.Graph()
    g.add_edges_from(links)
    load = {tuple(sorted(e)): 0.0 for e in links}
    routed = 0
    for s, t, v in dems:
        try:
            p = nx.shortest_path(g, s, t)
        except Exception:
            continue
        routed += 1
        for a, b in zip(p[:-1], p[1:]):
            load[tuple(sorted((a, b)))] += float(v)
    vals = [x for x in load.values() if x > 0]
    hi = max(vals)
    fill = sorted(max(MIN_FILL, min(MAX_FILL, round(MAX_FILL * x / hi))) for x in vals)
    rec = {"source": "SNDlib janos-us-ca (39 nodes, US-Canada)", "n_links": len(fill),
           "n_demands_routed": routed, "max_fill": MAX_FILL,
           "fill_levels": fill,
           "fill_pctiles": {p: int(sorted(fill)[int(p / 100 * (len(fill) - 1))])
                            for p in (10, 25, 50, 75, 90)}}
    json.dump(rec, open(os.path.join(HERE, "SNDlib-fill.json"), "w"), indent=1)
    print(f"routed {routed} demands over {len(links)} links; fill levels (ch): "
          f"min={min(fill)} median={sorted(fill)[len(fill)//2]} max={max(fill)}", flush=True)
    print(f"percentiles {rec['fill_pctiles']} -> SNDlib-fill.json", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
