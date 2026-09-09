"""Summarises a D3 probe/pilot json: the statistics every bar of PREREG-D3 uses."""
import json
import sys

import numpy as np

sys.path.insert(0, r"C:\Users\abptl\AppData\Local\Temp\claude\C--source\f9dd774c-068a-466c-aa48-fbb6bdd82c75\scratchpad")
from d3_grade import sign_p, med  # noqa: E402

res = json.load(open(sys.argv[1], encoding="utf-8-sig"))
cfg = res["config"]; Ts = [str(float(t)) for t in cfg["T_ladder"]]; Bs = [str(float(b)) for b in cfg["B_ladder"]]
print(len(res["worlds"]), "worlds", res["started"], res.get("finished"))
for w in res["worlds"]:
    print("==", w["name"], "rows", len(w["rows"]), "%.0fs" % w["seconds"])
    dirs = sorted({r["direction"] for r in w["rows"]})
    for d in dirs:
        rs = [r for r in w["rows"] if r["direction"] == d]
        print("  direction", d, "classical median by T:", [round(med([r["classical"][T] for r in rs]), 3) for T in Ts])
        for o in w["observers"]:
            diff = [med([abs(r["observers"][o]["exponent"][T] - r["classical"][T]) for r in rs]) for T in Ts]
            exc = [med([r["observers"][o]["exponent"][T] - r["classical"][T] for r in rs]) for T in Ts]
            frac1 = np.mean([r["observers"][o]["exponent"][Ts[0]] > r["classical"][Ts[0]] for r in rs])
            hz = [(med([r["observers"][o]["horizon"][B] for r in rs]), sum(not np.isfinite(r["observers"][o]["horizon"][B]) for r in rs)) for B in Bs]
            print("    %-6s |diff| med by T %s  excess med %s  frac>cl@T1 %.2f  horizon med (unreached) %s" % (o, [round(x, 4) for x in diff], [round(x, 3) for x in exc], frac1, [(round(h, 2), u) for h, u in hz]))
    if w.get("mu") is not None:
        rs = w["rows"]
        gaps = [r["classical"][Ts[-1]] - r["observers"]["core"]["exponent"][Ts[-1]] for r in rs]
        kx = max(abs(r["observers"]["core"]["exponent"][T] - r["core_part"][T]) for r in rs for T in Ts)
        print("  K: gap cl-obs at T20 min %.3f med %.3f max %.3f; classical T20 min %.3f max %.3f; KX max dev %.2e" % (min(gaps), med(gaps), max(gaps), min(r["classical"][Ts[-1]] for r in rs), max(r["classical"][Ts[-1]] for r in rs), kx))
    if w["name"] == "lorenz63":
        rs = [r for r in w["rows"] if r["direction"] == "random"]
        for B in Bs:
            print("  H2 x vs z at B=%s: sign p=%.4f n=%d frac=%.2f" % ((B,) + sign_p([r["observers"]["x_only"]["horizon"][B] for r in rs], [r["observers"]["z_only"]["horizon"][B] for r in rs])))
    if w["name"] == "lorenz96":
        rs = [r for r in w["rows"] if r["direction"] == "random"]
        for B in Bs:
            print("  H2 sub vs sub2 at B=%s: sign p=%.4f n=%d frac=%.2f" % ((B,) + sign_p([r["observers"]["sub"]["horizon"][B] for r in rs], [r["observers"]["sub2"]["horizon"][B] for r in rs])))
# E1 worst ratio
worst = 0.0
for w in res["worlds"]:
    for o, spec in w["observers"].items():
        pd = (min(spec) > 0) if isinstance(spec, list) else spec["min"] > 0
        if not pd:
            continue
        a, b = (min(spec), max(spec)) if isinstance(spec, list) else (spec["min"], spec["max"])
        for r in w["rows"]:
            for T in Ts:
                bound = np.log(b / a) / (2 * (float(T) - r["t0"]))
                if bound > 0:
                    worst = max(worst, abs(r["observers"][o]["exponent"][T] - r["classical"][T]) / bound)
print("E1 worst |diff|/bound over positive definite observers with b > a:", round(worst, 4))
