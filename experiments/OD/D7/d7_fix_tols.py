"""Fixes the D7 tolerances from the pilot by the rules of PREREG-D7 Section 5 and prints the pilot summary.
M1 = half the pilot's median relative advantage of the eigen-direction closure over the energy closure (ranks >= 16),
rounded down to 0.01, at least 0. M2 = half the pilot's pooled relative advantage of the read-energy closure over the
energy closure, rounded down to 0.01, at least 0. TOL2 = 1.25 x the pilot's largest relative shortfall of the
read-energy closure against the energy closure in any cell, rounded up to 0.01. TOL_N = 1.5 x the change of the
pooled read-energy advantage between the two pilot resolutions, rounded up to 0.01."""
import json
import math
import sys

import numpy as np

sys.path.insert(0, r"C:\Users\abptl\AppData\Local\Temp\claude\C--source\f9dd774c-068a-466c-aa48-fbb6bdd82c75\scratchpad")
from d7_grade import cells  # noqa: E402

res = json.load(open(sys.argv[1], encoding="utf-8-sig")); out = sys.argv[2]
for w in res["worlds"]:
    for sn in w["snapshots"]:
        print("%-10s n %3d t %.1f kc %2d sub %4d sv_rank %6.1f subgrid %.3f | %s | full %s" % (w["name"], w["n"], sn["t"], sn["kc"], sn["n_sub_pairs"], sn["sv_effective_rank"], sn["subgrid_norm_over_resolved"],
              " ".join("r%s eig %.3f re %.3f en %.3f rnd %.3f" % (r, v["err_read"], v["err_read_energy"], v["err_energy"], v["err_random_median"]) for r, v in sn["ranks"].items() if r != "full"),
              ("%.3f" % sn["ranks"]["full"]["err_read"]) if "full" in sn["ranks"] else "-"))
cs = cells(res)
adv1 = [(c["err_energy"] - c["err_read"]) / c["err_energy"] for c in cs]
adv2 = [(c["err_energy"] - c["err_read_energy"]) / c["err_energy"] for c in cs]
ns = sorted(set(c["n"] for c in cs)); pa = {n: float(np.mean([a for c, a in zip(cs, adv2) if c["n"] == n])) for n in ns}
M1 = max(0.0, math.floor(0.5 * float(np.median(adv1)) * 100) / 100)
M2 = max(0.0, math.floor(0.5 * float(np.mean(adv2)) * 100) / 100)
TOL2 = math.ceil(1.25 * max(0.0, -min(adv2)) * 100) / 100
TOL_N = math.ceil(1.5 * abs(pa[ns[-1]] - pa[ns[-2]]) * 100) / 100 if len(ns) >= 2 else None
print("cells %d (ranks >= 16) | eigen vs energy: median advantage %.3f, min %.3f, cells behind %d | read-energy vs energy: pooled %.3f, min %.3f, by n %s" % (
    len(cs), float(np.median(adv1)), min(adv1), sum(1 for a in adv1 if a < 0), float(np.mean(adv2)), min(adv2), {k: round(v, 3) for k, v in pa.items()}))
tols = {"M1": M1, "M2": M2, "TOL2": TOL2, "TOL_N": TOL_N, "pilot": {"median_adv_eigen": float(np.median(adv1)), "pooled_adv_readenergy": float(np.mean(adv2)), "min_adv_readenergy": float(min(adv2)), "pooled_by_n": pa},
        "rule": "PREREG-D7 Section 5: M1 = 0.5 x pilot median eigen advantage rounded down to 0.01 (at least 0); M2 = 0.5 x pilot pooled read-energy advantage rounded down to 0.01 (at least 0); TOL2 = 1.25 x pilot max read-energy shortfall rounded up to 0.01; TOL_N = 1.5 x the change of the pooled read-energy advantage between the pilot resolutions rounded up to 0.01"}
json.dump(tols, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in tols.items() if k != "pilot"}, indent=1))
