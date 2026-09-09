"""Fixes the D3v2 tolerances from the pilot by the rule of PREREG-D3V2 Section 5 (1.5 x the pilot's
largest value, rounded up to three decimals; O2 and O4 floored at 0.05) and prints the offsets."""
import json
import math
import sys

import numpy as np

res = json.load(open(sys.argv[1], encoding="utf-8-sig")); out = sys.argv[2]
cfg = res["config"]; Bs = [str(float(b)) for b in cfg["B_ladder"]]; OBs = [str(float(b)) for b in cfg["offset_budgets"]]
errs = []; convs = []; sym = []
for w in res["worlds"]:
    clv = w["clv"]; rows = [r for r in w["rows"] if r["direction"] == "random"]
    print("==", w["name"], "lambda_1 %.4f over %d points" % (clv["lambda_1"], clv["n_grid"]))
    means = {}
    for name in w["observers"]:
        if name == "full":
            continue
        fp = clv["observers"][name]["first_passage_offset"]; line = []
        for B in Bs:
            d = np.array([r["observers"][name]["horizon"][B] - r["observers"]["full"]["horizon"][B] for r in rows
                          if np.isfinite(r["observers"][name]["horizon"][B]) and np.isfinite(r["observers"]["full"]["horizon"][B])])
            means[(name, B)] = d.mean()
            line.append("B=%s %.3f±%.3f (n=%d, later %.2f)" % (B, d.mean(), d.std(ddof=1) / np.sqrt(len(d)), len(d), (d > 0).mean()))
            if B in OBs:
                errs.append((w["name"], name, B, abs(d.mean() - fp[B])))
        convs.append((w["name"], name, abs(means[(name, OBs[-1])] - means[(name, OBs[0])])))
        print("  %-9s pred %s (const-f %.3f) | %s" % (name, {B: round(fp[B], 3) for B in Bs}, clv["observers"][name]["constant_fraction_offset"], " | ".join(line)))
    if "sub" in w["observers"] and "sub2" in w["observers"]:
        dp = max(abs(clv["observers"]["sub"]["first_passage_offset"][B] - clv["observers"]["sub2"]["first_passage_offset"][B]) for B in OBs)
        dm = max(abs(means[("sub", B)] - means[("sub2", B)]) for B in OBs)
        sym += [dp, dm]; print("  symmetry: predicted diff %.3f, measured diff max %.3f" % (dp, dm))
worst = max(errs, key=lambda e: e[3]); worst2 = max(convs, key=lambda c: c[2])
print("O1 worst error", worst, "| O2 worst conv", worst2, "| O4 max", max(sym) if sym else None)
up = lambda x: math.ceil(x * 1.5 * 1000) / 1000
tols = {"O1": up(worst[3]), "O2": max(up(worst2[2]), 0.05), "O4": max(up(max(sym)), 0.05) if sym else 0.05,
        "rule": "PREREG-D3V2 Section 5: 1.5 x pilot largest value rounded up to 3 decimals; O2, O4 floored at 0.05",
        "pilot_statistics": {"O1_worst": worst, "O2_worst": worst2, "O4_max": max(sym) if sym else None}}
json.dump(tols, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in tols.items() if k != "pilot_statistics"}, indent=1))
