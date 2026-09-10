"""Fixes the D7v3 tolerances from the pilot by the rules of PREREG-D7V3 Section 5 and prints the pilot summary.
Scope: ranks at least R_MIN = 64. M2 = half the pilot's pooled relative advantage of the read-energy closure over the
energy closure in scope, rounded down to 0.01, at least 0. TOL2 = 1.25 x the pilot's largest relative shortfall of the
read-energy closure against the energy closure in any in-scope cell, rounded up to 0.01. TOL_N = 1.5 x the change of
the in-scope pooled read-energy advantage between the two pilot resolutions, rounded up to 0.01."""
import json
import math
import sys

import numpy as np

sys.path.insert(0, r"C:\Users\abptl\AppData\Local\Temp\claude\C--source\f9dd774c-068a-466c-aa48-fbb6bdd82c75\scratchpad")
from d7v3_grade import cells, adv, R_MIN  # noqa: E402

res = json.load(open(sys.argv[1], encoding="utf-8-sig")); out = sys.argv[2]
for w in res["worlds"]:
    for sn in w["snapshots"]:
        print("%-10s n %3d t %.1f kc %2d sub %4d sv_rank %6.1f subgrid %.3f | %s | full %s" % (w["name"], w["n"], sn["t"], sn["kc"], sn["n_sub_pairs"], sn["sv_effective_rank"], sn["subgrid_norm_over_resolved"],
              " ".join("r%s eig %.3f re %.3f en %.3f rnd %.3f" % (r, v["err_read"], v["err_read_energy"], v["err_energy"], v["err_random_median"]) for r, v in sn["ranks"].items() if r != "full"),
              ("%.3f" % sn["ranks"]["full"]["err_read"]) if "full" in sn["ranks"] else "-"))
cs = cells(res); below = [c for c in cells(res, 16) if c["r"] < R_MIN]
adv2 = [adv(c) for c in cs]; advb = [adv(c) for c in below]
ns = sorted(set(c["n"] for c in cs)); pa = {n: float(np.mean([a for c, a in zip(cs, adv2) if c["n"] == n])) for n in ns}
M2 = max(0.0, math.floor(0.5 * float(np.mean(adv2)) * 100) / 100)
TOL2 = math.ceil(1.25 * max(0.0, -min(adv2)) * 100) / 100
TOL_N = math.ceil(1.5 * abs(pa[ns[-1]] - pa[ns[-2]]) * 100) / 100 if len(ns) >= 2 else None
print("in-scope cells %d (ranks >= %d): read-energy vs energy pooled %.3f, min %.3f, cells behind %d, by n %s | below scope %d cells pooled %.3f" % (
    len(cs), R_MIN, float(np.mean(adv2)), min(adv2), sum(1 for a in adv2 if a < 0), {k: round(v, 3) for k, v in pa.items()}, len(below), float(np.mean(advb)) if advb else float("nan")))
tols = {"M2": M2, "TOL2": TOL2, "TOL_N": TOL_N, "R_MIN": R_MIN, "pilot": {"pooled_adv_readenergy_in_scope": float(np.mean(adv2)), "min_adv_readenergy_in_scope": float(min(adv2)), "pooled_by_n": pa, "pooled_adv_below_scope": float(np.mean(advb)) if advb else None},
        "rule": "PREREG-D7V3 Section 5: scope ranks >= 64; M2 = 0.5 x pilot in-scope pooled read-energy advantage rounded down to 0.01 (at least 0); TOL2 = 1.25 x pilot max in-scope read-energy shortfall rounded up to 0.01; TOL_N = 1.5 x the change of the in-scope pooled advantage between the pilot resolutions rounded up to 0.01"}
json.dump(tols, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in tols.items() if k != "pilot"}, indent=1))
