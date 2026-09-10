"""Fixes the D6v2 tolerances from the pilot by the rules of PREREG-D6V2 Section 5 and prints the pilot summary.
FACTOR = 1.25 x the pilot's largest greedy-over-exhaustive ratio, rounded up to one decimal, at least 1.0.
PHI = half the pilot's fraction of discriminating cells in which greedy needs strictly fewer sensors than the
energy ranking, rounded down to 0.05. TOL_H = 1.25 x the pilot's largest relative horizon shortfall against the
energy placement, rounded up to 0.05 (0 if none). MARGIN_H = half the pilot's pooled relative horizon advantage
over the discriminating growth cells, rounded down to 0.05, at least 0."""
import json
import math
import sys

import numpy as np

res = json.load(open(sys.argv[1], encoding="utf-8-sig")); out = sys.argv[2]
cells = []
for w in res["worlds"]:
    for c in w["cells"]:
        cc = dict(c); cc["world"] = w["name"]; cc["has_growth"] = w["has_growth"]; cells.append(cc)
feas = [c for c in cells if c["feasible"]]
for c in feas:
    s = "%-16s frac %-6g m %2d | greedy k=%d d=%d | energy k_needed=%s d@k=%d | random k_needed %.1f | exh k*=%s factor %s" % (
        c["world"], c["frac"], c["m"], c["k"], c["d_obs_greedy"], c["k_energy_needed"], c["d_obs_energy"], c["k_random_needed_median"], c["exhaustive_min"], ("%.2f" % c["greedy_factor"]) if c["greedy_factor"] else "-")
    if "h_greedy" in c:
        s += " | h greedy %.2f energy %.2f random %.2f" % (c["h_greedy"], c["h_energy"], c["h_random_median"])
    print(s)
ratios = [c["greedy_factor"] for c in feas if c["greedy_factor"]]
FACTOR = max(1.0, math.ceil(1.25 * max(ratios) * 10) / 10) if ratios else 1.0
disc = [c for c in feas if c["k_random_needed_median"] > c["k"]]
strict = [c for c in disc if c["k_energy_needed"] is None or c["k"] < c["k_energy_needed"]]
frac_strict = len(strict) / len(disc) if disc else 0.0
PHI = math.floor(0.5 * frac_strict * 20) / 20
gr = [c for c in feas if c["has_growth"] and "h_greedy" in c]
shortfalls = [1 - c["h_greedy"] / c["h_energy"] for c in gr if c["h_greedy"] < c["h_energy"]]
TOL_H = math.ceil(1.25 * max(shortfalls) * 20) / 20 if shortfalls else 0.0
gd = [c for c in gr if c["k_random_needed_median"] > c["k"]]
adv = (np.mean([c["h_greedy"] for c in gd]) / np.mean([c["h_energy"] for c in gd]) - 1.0) if gd else 0.0
MARGIN_H = max(0.0, math.floor(0.5 * adv * 20) / 20)
worse = [c for c in feas if c["k_energy_needed"] is not None and c["k"] > c["k_energy_needed"]]
print("lookahead vs greedy: fewer in %d cells, more in %d" % (sum(1 for c in feas if c["k"] < c["k_greedy"]), sum(1 for c in feas if c["k"] > c["k_greedy"])))
print("feasible cells %d; discriminating %d; greedy strictly fewer than energy in %d (%.2f); energy needs fewer in %d; greedy factors max %s; growth cells %d, shortfalls %s, pooled horizon advantage over energy on discriminating growth cells %.3f" % (
    len(feas), len(disc), len(strict), frac_strict, len(worse), ("%.2f" % max(ratios)) if ratios else "-", len(gr), ["%.3f" % s for s in shortfalls], adv))
tols = {"FACTOR": FACTOR, "PHI": PHI, "TOL_H": TOL_H, "MARGIN_H": MARGIN_H,
        "pilot": {"n_feasible": len(feas), "n_discriminating": len(disc), "frac_strict": frac_strict, "max_ratio": max(ratios) if ratios else None, "shortfalls": shortfalls, "pooled_horizon_advantage": adv, "n_growth_cells": len(gr)},
        "rule": "PREREG-D6V2 Section 5: FACTOR = 1.25 x pilot max greedy/exhaustive ratio rounded up to 0.1 (at least 1.0); PHI = 0.5 x pilot strict fraction rounded down to 0.05; TOL_H = 1.25 x pilot max relative horizon shortfall rounded up to 0.05; MARGIN_H = 0.5 x pilot pooled horizon advantage rounded down to 0.05 (at least 0)"}
json.dump(tols, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in tols.items() if k != "pilot"}, indent=1))
