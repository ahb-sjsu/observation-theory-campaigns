"""Grades a D1 results.json (second design, two worlds) against the sealed bars of PREREG-D1.md.
Usage: python d1_grade.py results.json --rec REC [--out grade.json]

Bars. A1 single-parameter verdicts and brackets exact. B1 in well-crossed cells at the largest
query count the medians of the Frobenius, above-threshold and below-threshold errors are at most
REC times their chance medians. B2 where the theory says the sphere does not cross the ellipsoid
the oracle is constant for every evaluator (one direction: a constant oracle under a thin crossing
is recorded, not failed). B3 the Frobenius median is non-increasing along the query ladder.
B4 in well-crossed cells of a full-rank world the estimate is nearer the predicted pencil member
P* than the truth at the median (the pencil bias is visible). The theoretical crossing is computed
here from the declared spectrum, so a constant-oracle cell is labelled by whether that was predicted."""
from __future__ import annotations

import json
import sys

import numpy as np


def grade(res: dict, rec: float) -> dict:
    cfg = res["config"]
    qs = sorted(int(q) for q in cfg["query_ladder"]); qmax = qs[-1]
    rho = float(cfg.get("rho", 1.0))
    spectra = {w["name"]: np.array(sorted(w["spectrum"], reverse=True), dtype=float) for w in cfg["worlds"]}
    out = {"rec": rec, "axis": {}, "mixed": {}, "gate": None}
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
        lam = spectra[world]
        cross_theory = bool((lam.min() * rho ** 2 < B ** 2) and (B ** 2 < lam.max() * rho ** 2))
        full_rank = bool(lam.min() > 0)
        cells = {int(c["n_queries"]): c for c in res["cells"] if c["kind"] == "mixed" and (c["world"], c["B"]) == (world, B)}
        good = {q: [r for r in c["rows"] if not r.get("skipped")] for q, c in cells.items()}
        key = f"{world}_B{B}"
        n_rows = max(len(cells[qmax]["rows"]), 1)
        n_const = cells[qmax]["summary"].get("n_skipped_constant", 0)
        if not good.get(qmax):
            # every evaluator's oracle was constant at the largest query count
            out["mixed"][key] = {"oracle_constant_in_all": True, "crossing_by_theory": cross_theory, "constant_fraction": n_const / n_rows, "graded": 0,
                                 "B2_no_crossing_oracle_constant": True,
                                 "note": "no crossing by theory: a constant oracle is what B2 predicts" if not cross_theory
                                 else "crossing by theory but thin: the oracle was constant in every evaluator's queries, consistent with B2, which binds only where there is no crossing"}
            continue
        g = good[qmax]
        if not cross_theory:
            # a non-constant oracle where the sphere does not cross the ellipsoid: B2 fails, and the registration's Fail clause applies
            fail = True; all_pass = False
            out["mixed"][key] = {"crossing_by_theory": False, "graded": len(g), "constant_fraction": n_const / n_rows,
                                 "B2_no_crossing_oracle_constant": False, "verdict": "FAIL"}
            continue
        well = bool(cells[qmax]["summary"].get("well_crossed", False))
        if not well:
            out["mixed"][key] = {"crossing_by_theory": True, "well_crossed": False, "graded": len(g), "constant_fraction": n_const / n_rows,
                                 "answer_balance_median": cells[qmax]["summary"].get("answer_balance_median"),
                                 "frobenius_median": float(np.median([r["frobenius_rel_err"] for r in g])),
                                 "chance_frobenius": float(np.median([r["chance"]["frobenius_rel_err"] for r in g])),
                                 "note": "poorly crossed: reported, not graded under B1, B3 or B4"}
            continue
        frob = float(np.median([r["frobenius_rel_err"] for r in g])); ch_frob = float(np.median([r["chance"]["frobenius_rel_err"] for r in g]))
        below = [x for r in g for x in r["below_rel_err"]]; ch_below = [r["chance"]["below_rel_err"] for r in g if r["chance"]["below_rel_err"] == r["chance"]["below_rel_err"]]
        above = [x for r in g for x in r["above_rel_err"]]; ch_above = [r["chance"]["above_rel_err"] for r in g if r["chance"]["above_rel_err"] == r["chance"]["above_rel_err"]]
        b1 = frob <= rec * ch_frob
        b1b = (np.median(below) <= rec * np.median(ch_below)) if (below and ch_below) else True
        b1a = (np.median(above) <= rec * np.median(ch_above)) if (above and ch_above) else True
        seq = [float(np.median([r["frobenius_rel_err"] for r in good[q]])) for q in qs if good.get(q)]
        b3 = all(seq[i + 1] <= seq[i] * 1.05 for i in range(len(seq) - 1))
        entry = {"crossing_by_theory": True, "well_crossed": True, "graded": len(g),
                 "B1_full_recovery": bool(b1), "frobenius_median": frob, "chance_frobenius": ch_frob,
                 "B1a_above": bool(b1a), "above_median": float(np.median(above)) if above else None, "chance_above": float(np.median(ch_above)) if ch_above else None,
                 "B1b_below_recovered_too": bool(b1b), "below_median": float(np.median(below)) if below else None, "chance_below": float(np.median(ch_below)) if ch_below else None,
                 "B3_monotone": bool(b3), "frobenius_by_queries": seq}
        cell_pass = b1 and b1a and b1b and b3
        if full_rank and "frobenius_rel_err_vs_pencil" in g[0]:
            fp = float(np.median([r["frobenius_rel_err_vs_pencil"] for r in g]))
            b4 = fp <= frob
            entry.update({"B4_nearer_pencil_member": bool(b4), "frobenius_vs_pencil_median": fp, "pencil_s_star": g[0].get("pencil_s_star")})
            cell_pass = cell_pass and b4
        if frob > 0.5 * ch_frob:
            fail = True
        all_pass = all_pass and cell_pass
        entry["verdict"] = "PASS" if cell_pass else "not all bars"
        out["mixed"][key] = entry
    out["gate"] = "PASS" if all_pass else ("FAIL" if fail else "INDETERMINATE")
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0]
    rec = float(argv[argv.index("--rec") + 1])
    outp = argv[argv.index("--out") + 1] if "--out" in argv else None
    g = grade(json.load(open(path, encoding="utf-8-sig")), rec)
    text = json.dumps(g, indent=1)
    if outp:
        open(outp, "w", encoding="utf-8").write(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
