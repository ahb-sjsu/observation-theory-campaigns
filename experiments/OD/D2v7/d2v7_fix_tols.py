"""Fixes the D2v7 tolerances from the pilot by the rule of PREREG-D2V7 Section 5 and prints the pilot
summary: REF = the frozen law's RMS log-ratio error pooled over every pilot row; FRAC_X = 1.5 x the pilot's
largest ratio of effective ranks, rounded up to two decimals, at most 0.9."""
import json
import math
import sys

import numpy as np

sys.path.insert(0, r"C:\Users\abptl\AppData\Local\Temp\claude\C--source\f9dd774c-068a-466c-aa48-fbb6bdd82c75\scratchpad")
from d2v7_hubness import rmse  # noqa: E402

res = json.load(open(sys.argv[1], encoding="utf-8-sig")); out = sys.argv[2]
law = res["law"]["law"]; comp = res["law"]["competitor_nominal"]; unity = res["law"]["competitor_unity"]
print("law:", law["features"], [round(c, 4) for c in law["coef"]], "train rmse %.4f heldout rmse %.4f" % (law["train_rmse"], law["heldout_rmse"]))
print("competitor:", comp["features"], [round(c, 4) for c in comp["coef"]], "train rmse %.4f heldout rmse %.4f" % (comp["train_rmse"], comp["heldout_rmse"]))
print("unity: train rmse %.4f heldout rmse %.4f" % (res["law"]["unity_train_rmse"], res["law"]["unity_heldout_rmse"]))
ratios = {w["name"]: w["matrix"]["rank_eff_standardised"] / w["matrix"]["null_rank_eff_standardised"] for w in res["worlds"]}
print("rank ratios:", {k: round(v, 3) for k, v in ratios.items()})
for w in res["worlds"]:
    p = w["polarity"]; rs = [r for r in w["rows"] if "budget_rel" not in r]
    print("%-18s %-8s rmse law %.3f nominal %.3f unity %.3f | jac same %.3f diff %.3f | excess range %.2f..%.2f" % (
        w["name"], w["group"], rmse(law, rs), rmse(comp, rs), rmse(unity, rs), p["hub_jaccard_same_alpha_mean"], p["hub_jaccard_diff_alpha_mean"],
        min(r["targets"]["excess"] for r in rs), max(r["targets"]["excess"] for r in rs)))
    for r in w["rows"]:
        if "budget_rel" in r:
            print("   budget a=%.1f b=%.2f excess %.2f changed %.3f rev %.4f" % (r["alpha"], r["budget_rel"], r["targets"]["excess"], r["polarity_changed_frac"], r["reversal_frac"]))
all_rows = [r for w in res["worlds"] if w["group"] in ("train", "heldout") for r in w["rows"] if "budget_rel" not in r]
pooled = rmse(law, all_rows); print("pooled pilot RMS log-ratio error of the frozen law over train + heldout rows (%d): %.4f (nominal %.4f, unity %.4f)" % (len(all_rows), pooled, rmse(comp, all_rows), rmse(unity, all_rows)))
tols = {"REF": float(pooled), "REF_note": "the frozen law's RMS error in log excess pooled over every pilot row (training and held-out), the held-out error alone being " + "%.4f" % law["heldout_rmse"], "pooled_nominal": rmse(comp, all_rows), "pooled_unity": rmse(unity, all_rows), "FRAC_X": min(math.ceil(max(ratios.values()) * 1.5 * 100) / 100, 0.9),
        "rule": "PREREG-D2V7 Section 5: REF = the frozen law's RMS log-ratio error pooled over every pilot row; FRAC_X = 1.5 x pilot max rank ratio rounded up to 2 decimals, at most 0.9",
        "pilot_rank_ratios": ratios}
json.dump(tols, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in tols.items() if k != "pilot_rank_ratios"}, indent=1))
