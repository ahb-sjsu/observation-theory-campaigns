"""Fixes the D2v9 tolerances from the pilot by the rule of PREREG-D2V9 Section 5: REF = the frozen law's RMS
log-ratio error pooled over the IN-SCOPE pilot rows (cv_knn >= TAU); FRAC_X = 1.5 x the pilot's largest ratio of
effective ranks, rounded up to two decimals, at most 0.9. Prints the pilot summary."""
import json
import math
import sys

import numpy as np

sys.path.insert(0, r"C:\Users\abptl\AppData\Local\Temp\claude\C--source\f9dd774c-068a-466c-aa48-fbb6bdd82c75\scratchpad")
from d2v9_hubness import apply_law, rmse  # noqa: E402

TAU = 0.015
res = json.load(open(sys.argv[1], encoding="utf-8-sig")); out = sys.argv[2]
law = res["law"]["law"]; comp = res["law"]["competitor_nominal"]; unity = res["law"]["competitor_unity"]
print("law (frozen D2v7):", law["features"], [round(c, 4) for c in law["coef"]])
ratios = {w["name"]: w["matrix"]["rank_eff_standardised"] / w["matrix"]["null_rank_eff_standardised"] for w in res["worlds"]}
allin = []; allout = []
for w in res["worlds"]:
    p = w["polarity"]; rs = [r for r in w["rows"] if "budget_rel" not in r]
    ins = [r for r in rs if r["variables"]["cv_knn"] >= TAU]; outs = [r for r in rs if r["variables"]["cv_knn"] < TAU]
    allin += ins; allout += outs
    ro = (apply_law(law, outs) - np.array([r["targets"]["log_excess"] for r in outs])) if outs else np.array([])
    print("%-18s %-8s in %2d/%2d rmse law %.3f nominal %.3f unity %.3f | out %2d rmse %s med res %s | jac same %.3f diff %.3f | excess %.2f..%.2f" % (
        w["name"], w["group"], len(ins), len(rs), rmse(law, ins) if ins else float("nan"), rmse(comp, ins) if ins else float("nan"), rmse(unity, ins) if ins else float("nan"),
        len(outs), ("%.2f" % rmse(law, outs)) if outs else "-", ("%.2f" % np.median(ro)) if outs else "-", p["hub_jaccard_same_alpha_mean"], p["hub_jaccard_diff_alpha_mean"],
        min(r["targets"]["excess"] for r in rs), max(r["targets"]["excess"] for r in rs)))
pooled = rmse(law, allin)
print("pilot rows %d, in scope %d, out of scope %d; REF (in-scope pooled) %.4f; nominal %.4f unity %.4f; out-of-scope rmse %s" % (
    len(allin) + len(allout), len(allin), len(allout), pooled, rmse(comp, allin), rmse(unity, allin), ("%.3f" % rmse(law, allout)) if allout else "-"))
tols = {"REF": float(pooled), "REF_note": "the frozen D2v7 law's RMS error in log excess pooled over the in-scope pilot rows (cv_knn >= TAU)", "TAU": TAU,
        "pooled_nominal": rmse(comp, allin), "pooled_unity": rmse(unity, allin), "n_in": len(allin), "n_out": len(allout), "rmse_out": rmse(law, allout) if allout else None,
        "FRAC_X": min(math.ceil(max(ratios.values()) * 1.5 * 100) / 100, 0.9),
        "rule": "PREREG-D2V9 Section 5: REF = the frozen law's RMS log-ratio error pooled over the in-scope pilot rows; TAU = 0.015 declared; FRAC_X = 1.5 x pilot max rank ratio rounded up to 2 decimals, at most 0.9",
        "pilot_rank_ratios": ratios}
json.dump(tols, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in tols.items() if k != "pilot_rank_ratios"}, indent=1))
