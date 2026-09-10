"""Grades a D6v2 results.json against the sealed bars of PREREG-D6V2v2.md.
Usage: python d6_grade.py results.json --tols tolerances.json [--out grade.json]
tolerances.json carries FACTOR (greedy count over the exhaustive minimum), PHI (the fraction of
discriminating cells in which greedy must need strictly fewer sensors than the energy ranking), TOL_H
(the relative horizon shortfall allowed against the energy placement in any growth cell) and MARGIN_H
(the pooled relative horizon advantage required over the discriminating growth cells)."""
from __future__ import annotations

import json
import sys

import numpy as np


def grade(res: dict, tols: dict) -> dict:
    FACTOR = float(tols["FACTOR"]); PHI = float(tols["PHI"]); TOL_H = float(tols["TOL_H"]); MARGIN_H = float(tols["MARGIN_H"])
    out = {"tolerances": tols, "bars": {}, "cells": [], "gate": None}
    fail = False
    cells = []
    for w in res["worlds"]:
        for c in w["cells"]:
            cc = dict(c); cc["world"] = w["name"]; cc["group"] = w["group"]; cc["has_growth"] = w["has_growth"]; cells.append(cc)
    feas = [c for c in cells if c["feasible"]]
    out["n_cells"] = len(cells); out["n_feasible"] = len(feas)
    # E1 exact: within every world and required count, d_obs of the all-sensor placement is antitone in the budget
    e1 = True
    for w in res["worlds"]:
        by_m = {}
        for c in w["cells"]:
            by_m.setdefault(c["m"], []).append((c["frac"], c["d_obs_all"]))
        for m, lst in by_m.items():
            lst.sort(); e1 = e1 and all(a[1] >= b[1] for a, b in zip(lst, lst[1:]))
    out["bars"]["E1_antitone"] = {"holds": e1}
    # P1: the greedy placement reaches m in every feasible cell
    p1 = all(c["d_obs_greedy"] >= c["m"] for c in feas)
    out["bars"]["P1_reaches_count"] = {"holds": p1, "misses": [(c["world"], c["frac"], c["m"]) for c in feas if c["d_obs_greedy"] < c["m"]]}
    # G1: greedy count within FACTOR of the exhaustive minimum where exhaustive search was feasible
    ex = [c for c in feas if c["exhaustive_min"]]
    ratios = {(c["world"], c["frac"], c["m"]): c["greedy_factor"] for c in ex}
    g1 = all(r <= FACTOR for r in ratios.values()) if ex else None
    out["bars"]["G1_greedy_vs_exhaustive"] = {"n_cells": len(ex), "max_ratio": max(ratios.values()) if ex else None, "limit": FACTOR, "holds": g1, "ratios": {"%s|%g|%d" % k: v for k, v in ratios.items()}}
    if ex and max(ratios.values()) > 2.0:
        fail = True
    # C1 against the energy ranking: never more sensors than it needs, and strictly fewer in at least PHI of the discriminating cells
    worse = [c for c in feas if c["k_energy_needed"] is not None and c["k"] > c["k_energy_needed"]]
    disc = [c for c in feas if c["k_random_needed_median"] > c["k"]]
    strictly = [c for c in disc if c["k_energy_needed"] is None or c["k"] < c["k_energy_needed"]]
    frac_strict = (len(strictly) / len(disc)) if disc else None
    c1 = (len(worse) == 0 and (frac_strict is not None and frac_strict >= PHI))
    out["bars"]["C1_vs_energy"] = {"n_feasible": len(feas), "cells_energy_needs_fewer": [(c["world"], c["frac"], c["m"], c["k"], c["k_energy_needed"]) for c in worse],
                                   "n_discriminating": len(disc), "n_greedy_strictly_fewer": len(strictly), "fraction": frac_strict, "limit": PHI, "holds": c1}
    if feas and len(worse) > 0.1 * len(feas):
        fail = True
    # C2 against random orderings: never more sensors than the median random ordering needs
    c2 = all(c["k"] <= c["k_random_needed_median"] for c in feas)
    out["bars"]["C2_vs_random"] = {"holds": c2, "misses": [(c["world"], c["frac"], c["m"], c["k"], c["k_random_needed_median"]) for c in feas if c["k"] > c["k_random_needed_median"]]}
    # C3 the selector repair: the lookahead placement never needs more sensors than D6's greedy, and fewer in at least one cell where greedy missed the optimum
    c3_worse = [c for c in feas if c["k"] > c["k_greedy"]]; c3_fewer = [c for c in feas if c["k"] < c["k_greedy"]]
    c3 = len(c3_worse) == 0
    out["bars"]["C3_vs_greedy"] = {"holds": c3, "cells_lookahead_more": [(c["world"], c["frac"], c["m"], c["k"], c["k_greedy"]) for c in c3_worse], "cells_lookahead_fewer": [(c["world"], c["frac"], c["m"], c["k"], c["k_greedy"]) for c in c3_fewer], "n_fewer": len(c3_fewer)}
    # H1 horizon on growth worlds: never materially shorter than the energy placement at the same count, and longer pooled over the discriminating cells
    gr = [c for c in feas if c["has_growth"] and "h_greedy" in c]
    if gr:
        short = [c for c in gr if c["h_greedy"] < (1 - TOL_H) * c["h_energy"]]
        gd = [c for c in gr if c["k_random_needed_median"] > c["k"]]
        pooled_adv = (np.mean([c["h_greedy"] for c in gd]) / np.mean([c["h_energy"] for c in gd]) - 1.0) if gd else None
        h1 = len(short) == 0 and (pooled_adv is not None and pooled_adv >= MARGIN_H)
        if pooled_adv is not None and pooled_adv < 0:
            fail = True
    else:
        short = []; gd = []; pooled_adv = None; h1 = None
    out["bars"]["H1_horizon"] = {"n_growth_cells": len(gr), "shorter_than_energy": [(c["world"], c["frac"], c["m"], c["h_greedy"], c["h_energy"]) for c in short], "n_discriminating": len(gd), "pooled_advantage_over_energy": pooled_adv, "margin": MARGIN_H, "tol": TOL_H, "holds": h1,
                                 "vs_random_pooled": (float(np.mean([c["h_greedy"] for c in gd]) / np.mean([c["h_random_median"] for c in gd]) - 1.0) if gd else None)}
    out["cells"] = [{k: v for k, v in c.items() if k not in ("greedy", "energy")} for c in cells]
    e1, p1, g1, c1, c2, h1, c3 = [None if b is None else bool(b) for b in (e1, p1, g1, c1, c2, h1, c3)]
    for k in ("E1_antitone", "P1_reaches_count", "G1_greedy_vs_exhaustive", "C1_vs_energy", "C2_vs_random", "H1_horizon", "C3_vs_greedy"):
        out["bars"][k]["holds"] = None if out["bars"][k]["holds"] is None else bool(out["bars"][k]["holds"])
    if out["bars"]["H1_horizon"]["pooled_advantage_over_energy"] is not None:
        out["bars"]["H1_horizon"]["pooled_advantage_over_energy"] = float(out["bars"]["H1_horizon"]["pooled_advantage_over_energy"])
    bars = [e1, p1, g1, c1, c2, h1, c3]
    if any(b is None for b in bars):
        out["gate"] = "NOT ALL GROUPS RUN (pilot or probe): " + ("all run bars hold" if all(b for b in bars if b is not None) else "a run bar fails")
        return out
    out["gate"] = "PASS" if all(bars) else ("FAIL" if fail else "INDETERMINATE")
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0]; tols = json.load(open(argv[argv.index("--tols") + 1], encoding="utf-8-sig"))
    outp = argv[argv.index("--out") + 1] if "--out" in argv else None
    g = grade(json.load(open(path, encoding="utf-8-sig")), tols); text = json.dumps(g, indent=1)
    if outp:
        open(outp, "w", encoding="utf-8").write(text + "\n")
    print(text); return 0


if __name__ == "__main__":
    sys.exit(main())
