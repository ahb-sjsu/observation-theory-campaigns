"""Fixes REC for D1v2 from its pilot by the rule of PREREG-D1V2 Section 5: REC = 1.5 x the largest of the graded
ratios (median Frobenius, above-threshold and below-threshold errors over their chance medians) over the pilot's
well-crossed cells at the largest query count, rounded up to 0.01; the registration is not sealed if that exceeds
0.45. Usage: python d1v2_fix_tols.py pilot.json tolerances.json"""
import json
import math
import sys

sys.path.insert(0, "C:/source/observation-theory-campaigns/experiments/OD/D1")
from d1_grade import grade  # noqa: E402

res = json.load(open(sys.argv[1], encoding="utf-8-sig")); out = sys.argv[2]
g = grade(res, 1.0); ratios = {}
for name, e in g["mixed"].items():
    if not e.get("well_crossed"): continue
    r = {"frobenius": e["frobenius_median"] / e["chance_frobenius"]}
    if e.get("above_median") is not None and e.get("chance_above"): r["above"] = e["above_median"] / e["chance_above"]
    if e.get("below_median") is not None and e.get("chance_below"): r["below"] = e["below_median"] / e["chance_below"]
    ratios[name] = {k: round(v, 4) for k, v in r.items()}
    print("%-22s" % name, ratios[name], "B4" if "B4_nearer_pencil_member" in e else "", e.get("B4_nearer_pencil_member", ""))
mx = max(v for r in ratios.values() for v in r.values())
REC = math.ceil(1.5 * mx * 100) / 100
print("well-crossed cells %d, largest ratio %.4f -> REC %.2f (%s)" % (len(ratios), mx, REC, "SEALABLE" if REC <= 0.45 else "NOT SEALABLE, rule gives more than 0.45"))
json.dump({"REC": REC, "pilot_max_ratio": mx, "pilot_ratios": ratios, "sealable": REC <= 0.45,
           "rule": "PREREG-D1V2 Section 5: REC = 1.5 x the pilot's largest graded ratio over its well-crossed cells at the largest query count, rounded up to 0.01; not sealed above 0.45"}, open(out, "w"), indent=1)
