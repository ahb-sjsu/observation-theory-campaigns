"""Grades a D1 results.json (second design, two worlds) against the sealed bars of PREREG-D1.md.
Usage: python d1_grade.py results.json --rec REC [--unrev 0.5] [--out grade.json]"""
from __future__ import annotations

import json
import sys

import numpy as np


def grade(res: dict, rec: float, unrev: float = 0.5) -> dict:
    cfg = res["config"]
    qs = sorted(int(q) for q in cfg["query_ladder"]); qmax = qs[-1]
    out = {"rec": rec, "unrev": unrev, "axis": {}, "mixed": {}, "gate": None}
    fail = False; all_pass = True
    # World A
    for c in res["cells"]:
        if c["kind"] != "axis":
            continue
        rows = c["rows"]
        verd = float(np.mean([r["verdicts_match"] for r in rows])); brk = float(np.mean([r["bracket_holds_all"] for r in rows]))
        a1 = verd == 1.0 and brk == 1.0
        if verd < 0.5:
            fail = True
        all_pass = all_pass and a1
        out["axis"][f"{c['world']}_B{c['B']}"] = {"A1_verdicts_and_brackets_exact": bool(a1), "verdicts_match_fraction": verd, "bracket_holds_fraction": brk}
    # World B
    keys = sorted({(c["world"], c["B"]) for c in res["cells"] if c["kind"] == "mixed"})
    for world, B in keys:
        cells = {int(c["n_queries"]): c for c in res["cells"] if c["kind"] == "mixed" and (c["world"], c["B"]) == (world, B)}
        good = {q: [r for r in c["rows"] if not r.get("skipped")] for q, c in cells.items()}
        crossing_by_theory = None
        rec_entry = {}
        if not good.get(qmax):
            # the oracle was constant: predicted exactly when the sphere does not cross the ellipsoid
            n_const = cells[qmax]["summary"].get("n_skipped_constant", 0)
            rec_entry = {"B2_no_crossing_oracle_constant": True, "constant_fraction": n_const / max(len(cells[qmax]["rows"]), 1), "graded": 0}
            out["mixed"][f"{world}_B{B}"] = rec_entry
            continue
        g = good[qmax]
        crossing = bool(np.mean([r["crossing"] for r in g]) > 0.5)
        frob = float(np.median([r["frobenius_rel_err"] for r in g])); ch_frob = float(np.median([r["chance"]["frobenius_rel_err"] for r in g]))
        below = [x for r in g for x in r["below_rel_err"]]; ch_below = [r["chance"]["below_rel_err"] for r in g if r["chance"]["below_rel_err"] == r["chance"]["below_rel_err"]]
        above = [x for r in g for x in r["above_rel_err"]]; ch_above = [r["chance"]["above_rel_err"] for r in g if r["chance"]["above_rel_err"] == r["chance"]["above_rel_err"]]
        b1 = (frob <= rec * ch_frob) if crossing else True
        b1b = (np.median(below) <= rec * np.median(ch_below)) if (crossing and below and ch_below) else True
        b1a = (np.median(above) <= rec * np.median(ch_above)) if (crossing and above and ch_above) else True
        seq = [float(np.median([r["frobenius_rel_err"] for r in good[q]])) for q in qs if good.get(q)]
        b3 = all(seq[i + 1] <= seq[i] * 1.05 for i in range(len(seq) - 1))
        if crossing and frob > 0.5 * ch_frob:
            fail = True
        cell_pass = b1 and b1a and b1b and b3
        all_pass = all_pass and cell_pass
        out["mixed"][f"{world}_B{B}"] = {"crossing": crossing, "graded": len(g),
                                        "B1_full_recovery": bool(b1), "frobenius_median": frob, "chance_frobenius": ch_frob,
                                        "B1a_above": bool(b1a), "B1b_below_recovered_too": bool(b1b),
                                        "below_median": float(np.median(below)) if below else None, "chance_below": float(np.median(ch_below)) if ch_below else None,
                                        "B3_monotone": bool(b3), "frobenius_by_queries": seq,
                                        "verdict": "PASS" if cell_pass else "not all bars"}
    out["gate"] = "PASS" if all_pass else ("FAIL" if fail else "INDETERMINATE")
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0]
    rec = float(argv[argv.index("--rec") + 1])
    unrev = float(argv[argv.index("--unrev") + 1]) if "--unrev" in argv else 0.5
    outp = argv[argv.index("--out") + 1] if "--out" in argv else None
    g = grade(json.load(open(path, encoding="utf-8")), rec, unrev)
    text = json.dumps(g, indent=1)
    if outp:
        open(outp, "w", encoding="utf-8").write(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
