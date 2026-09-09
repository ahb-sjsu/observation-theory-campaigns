"""Fixes the D2 tolerances from the pilot by the rule of PREREG-D2 Section 5 and prints the pilot
summary: REF = the frozen law's held-out error; FRAC_X = 1.5 x the pilot's largest ratio of
effective ranks, rounded up to two decimals, at most 0.9."""
import json
import math
import sys

import numpy as np

sys.path.insert(0, r"C:\Users\abptl\AppData\Local\Temp\claude\C--source\f9dd774c-068a-466c-aa48-fbb6bdd82c75\scratchpad")
from d2_hubness import rmse  # noqa: E402

res = json.load(open(sys.argv[1], encoding="utf-8-sig")); out = sys.argv[2]
law = res["law"]["law"]; comp = res["law"]["competitor_nominal"]
print("law:", law["features"], [round(c, 4) for c in law["coef"]], "train rmse %.4f heldout rmse %.4f" % (law["train_rmse"], law["heldout_rmse"]))
print("competitor:", comp["features"], [round(c, 4) for c in comp["coef"]], "train rmse %.4f heldout rmse %.4f" % (comp["train_rmse"], comp["heldout_rmse"]))
ratios = {w["name"]: w["matrix"]["rank_eff_standardised"] / w["matrix"]["null_rank_eff_standardised"] for w in res["worlds"]}
print("rank ratios:", {k: round(v, 3) for k, v in ratios.items()})
for w in res["worlds"]:
    p = w["polarity"]; rs = [r for r in w["rows"] if "budget_rel" not in r]
    print("%-18s %-8s rmse law %.3f comp %.3f | jac same %.3f diff %.3f | rev same %.5f diff %.5f | skew range %.2f..%.2f" % (
        w["name"], w["group"], rmse(law, rs), rmse(comp, rs), p["hub_jaccard_same_alpha_mean"], p["hub_jaccard_diff_alpha_mean"],
        p["reversal_frac_same_alpha_mean"], p["reversal_frac_diff_alpha_mean"], min(r["targets"]["skew"] for r in rs), max(r["targets"]["skew"] for r in rs)))
    for r in w["rows"]:
        if "budget_rel" in r:
            print("   budget a=%.1f b=%.2f skew %.2f changed %.3f rev %.4f" % (r["alpha"], r["budget_rel"], r["targets"]["skew"], r["polarity_changed_frac"], r["reversal_frac"]))
all_rows = [r for w in res["worlds"] if w["group"] in ("train", "heldout") for r in w["rows"] if "budget_rel" not in r]
pooled = rmse(law, all_rows); print("pooled pilot RMSE of the frozen law over train + heldout rows (%d): %.4f (competitor %.4f)" % (len(all_rows), pooled, rmse(comp, all_rows)))
tols = {"REF": float(pooled), "REF_note": "the frozen law's RMSE pooled over every pilot row (training and held-out), the held-out RMSE alone being " + "%.4f" % law["heldout_rmse"], "FRAC_X": min(math.ceil(max(ratios.values()) * 1.5 * 100) / 100, 0.9),
        "rule": "PREREG-D2 Section 5: REF = frozen law's held-out RMSE at the pilot; FRAC_X = 1.5 x pilot max rank ratio rounded up to 2 decimals, at most 0.9",
        "pilot_rank_ratios": ratios}
json.dump(tols, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in tols.items() if k != "pilot_rank_ratios"}, indent=1))
