"""Grades a D1 results.json against the sealed bars of PREREG-D1.md Section 5.
Usage: python d1_grade.py results.json --frac FRAC --rec REC [--unrev 0.5] [--out grade.json]"""
from __future__ import annotations

import json
import sys

import numpy as np


def grade(res: dict, frac: float, rec: float, unrev: float = 0.5) -> dict:
    cfg = res["config"]
    qs = sorted(int(q) for q in cfg["query_ladder"]); qmax = qs[-1]
    keys = sorted({(c["world"], c["B"]) for c in res["cells"]})
    out = {"frac": frac, "rec": rec, "unrev": unrev, "cells": {}, "gate": None}
    fail = False; all_pass = True
    for world, B in keys:
        cells = {int(c["n_queries"]): c for c in res["cells"] if (c["world"], c["B"]) == (world, B)}
        good = {q: [r for r in c["rows"] if not r.get("skipped")] for q, c in cells.items()}
        if not good.get(qmax):
            out["cells"][f"{world}_B{B}"] = {"verdict": "not graded, no evaluators"}; continue
        match = {q: float(np.mean([r["count_matches"] for r in g])) if g else float("nan") for q, g in good.items()}
        seq = [match[q] for q in qs if q in match and match[q] == match[q]]
        inv = [seq[i] - seq[i + 1] for i in range(len(seq) - 1) if seq[i + 1] < seq[i]]
        p1 = match[qmax] >= frac and len(inv) <= 1 and all(x <= 0.05 + 1e-12 for x in inv)
        if match[qmax] < 0.5:
            fail = True
        g = good[qmax]
        above = [x for r in g for x in r["above_rel_err"]]
        ch_above = [r["chance"]["above_rel_err"] for r in g if r["chance"]["above_rel_err"] == r["chance"]["above_rel_err"]]
        ang = [r["top_subspace_angle_deg"] for r in g]; ch_ang = [r["chance"]["top_subspace_angle_deg"] for r in g]
        if above and ch_above:
            p2 = (np.median(above) <= rec * np.median(ch_above)) and (np.median(ang) <= rec * max(np.median(ch_ang), 1e-9))
        else:
            p2 = True
        below = [x for r in g for x in r["below_rel_err"]]
        ch_below = [r["chance"]["below_rel_err"] for r in g if r["chance"]["below_rel_err"] == r["chance"]["below_rel_err"]]
        pushed_b = float(np.mean([r["below_pushed_above"] for r in g]))
        p3 = ((np.median(below) >= unrev * np.median(ch_below)) if (below and ch_below) else True) and pushed_b <= 0.10
        pushed_k = float(np.mean([r["kernel_pushed_above"] for r in g]))
        p4 = pushed_k <= 0.10
        if pushed_b > 0.3 or pushed_k > 0.3:
            fail = True
        med_above = [float(np.median([x for r in good[q] for x in r["above_rel_err"]])) for q in qs if good.get(q) and any(r["above_rel_err"] for r in good[q])]
        p5 = all(med_above[i + 1] <= med_above[i] * 1.05 for i in range(len(med_above) - 1))
        cell_pass = p1 and p2 and p3 and p4 and p5
        all_pass = all_pass and cell_pass
        out["cells"][f"{world}_B{B}"] = {
            "d_obs": g[0]["d_obs"], "P1": {"holds": bool(p1), "count_match_by_queries": {str(q): match[q] for q in qs if q in match}},
            "P2": {"holds": bool(p2), "above_median": float(np.median(above)) if above else None, "chance": float(np.median(ch_above)) if ch_above else None,
                   "angle_median": float(np.median(ang)), "chance_angle": float(np.median(ch_ang))},
            "P3": {"holds": bool(p3), "below_median": float(np.median(below)) if below else None, "chance": float(np.median(ch_below)) if ch_below else None, "pushed_above_fraction": pushed_b},
            "P4": {"holds": bool(p4), "kernel_pushed_above_fraction": pushed_k},
            "P5": {"holds": bool(p5), "above_median_by_queries": med_above},
            "verdict": "PASS" if cell_pass else "not all bars"}
    out["gate"] = "PASS" if all_pass else ("FAIL" if fail else "INDETERMINATE")
    out["cells_passing"] = sum(1 for v in out["cells"].values() if v.get("verdict") == "PASS")
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0]
    frac = float(argv[argv.index("--frac") + 1]); rec = float(argv[argv.index("--rec") + 1])
    unrev = float(argv[argv.index("--unrev") + 1]) if "--unrev" in argv else 0.5
    outp = argv[argv.index("--out") + 1] if "--out" in argv else None
    g = grade(json.load(open(path, encoding="utf-8")), frac, rec, unrev)
    text = json.dumps(g, indent=1)
    if outp:
        open(outp, "w", encoding="utf-8").write(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
