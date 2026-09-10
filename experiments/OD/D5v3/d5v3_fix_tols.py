"""Fixes the D5 tolerances from the pilot by the rules of PREREG-D5V3 Section 5 and prints the pilot summary.
TOL_N = 1.5 x the pilot's largest N1 difference on f_B(t)/f_B(0) at budgets 8 and above (N against 2N, same initial condition and viscosity),
rounded up to 0.01. TOL_C = 1.5 x the pilot's largest per-viscosity median bin IQR of the scaled collapse,
rounded up to 0.01. MARGIN_L = 0.02 (declared, not from the pilot: one sample interval)."""
import json
import math
import sys

import numpy as np

sys.path.insert(0, r"C:\Users\abptl\AppData\Local\Temp\claude\C--source\f9dd774c-068a-466c-aa48-fbb6bdd82c75\scratchpad")
from d5_grade import points, scatter
from d5v3_grade import control_points, NU_MAX  # noqa: E402

res = json.load(open(sys.argv[1], encoding="utf-8-sig")); out = sys.argv[2]
burg = [w for w in res["worlds"] if w.get("t_star") is not None]; ctrl = [w for w in res["worlds"] if w.get("t_star") is None]
for w in burg:
    rec = w["record"]; f2 = [g["2"]["read_fraction"] for g in rec["geom"]]; fb = [g[max(k for k in rec["geom"][0] if k != "total_energy")]["read_fraction"] for g in rec["geom"]]
    print("%-22s N %4d nu %-6g t* %.3f | classical alarm %s | obs alarms %s | f_2 %.3f -> %.3f | f_max %.3f -> %.3f | max_grad x%.1f" % (
        w["name"], w["N"], w["nu"], w["t_star"], w["alarm_classical"], {k: v for k, v in w["alarms_obs"].items() if v is not None}, f2[0], f2[-1], fb[0], fb[-1], rec["max_grad"][-1] / rec["max_grad"][0]))
for w in ctrl:
    print("%-22s control N %d nu %g | alarms %s | max_grad ratio %.3f" % (w["name"], w["N"], w["nu"], w["alarms_obs"], w["max_grad_ratio"]))
diffs = {}
for a in burg:
    for b in burg:
        if a["ic_seed"] == b["ic_seed"] and a["nu"] == b["nu"] and b["N"] == 2 * a["N"]:
            ta = np.array(a["record"]["t"]); tb = np.array(b["record"]["t"]); n = min(len(ta), len(tb)); keep = ta[:n] <= 0.9 * a["t_star"]
            shared = [bb for bb in a["record"]["geom"][0] if bb != "total_energy" and bb in b["record"]["geom"][0]]
            diffs[f"{a['name']}|{b['name']}"] = max(float(np.max(np.abs(np.array([g[bb]["read_fraction"] for g in a["record"]["geom"][:n]])[keep] - np.array([g[bb]["read_fraction"] for g in b["record"]["geom"][:n]])[keep]))) for bb in shared)
print("raw resolution differences (all budgets, reported):", {k: round(v, 4) for k, v in diffs.items()})
from d5v3_grade import grade as _grade_v3  # noqa: E402
raw_diffs = diffs
diffs = _grade_v3(res, {"TOL_N": 1.0, "TOL_C": 1.0, "RATIO": 1.0})["bars"]["N1_convergence_in_scope"]["pairs"]
print("N1 differences on f_B(t)/f_B(0) at budgets >= 8 (the bar):", {k: round(v, 4) for k, v in diffs.items()})
TOL_N = math.ceil(1.5 * max(diffs.values()) * 100) / 100 if diffs else None
med = []; coll = {}
for nu in sorted(set(w["nu"] for w in burg)):
    ws = [w for w in burg if w["nu"] == nu]
    sc = scatter(sum((points(w, True) for w in ws), [])); un = scatter(sum((points(w, False) for w in ws), [])); coll[str(nu)] = {"scaled": sc, "unscaled": un}
    print("nu %g: scaled collapse median IQR %s max %s (%d bins, %d points); unscaled median IQR %s" % (nu, sc["median_iqr"], sc["max_iqr"], sc["n_bins"], sc["n_points"], un["median_iqr"]))
    if sc["median_iqr"] is not None: med.append(sc["median_iqr"])
TOL_C = math.ceil(1.5 * max(med) * 100) / 100 if med else None
ratios = [coll[k]["scaled"]["median_iqr"] / coll[k]["unscaled"]["median_iqr"] for k in coll if float(k) <= NU_MAX + 1e-12 and coll[k]["scaled"]["median_iqr"] and coll[k]["unscaled"]["median_iqr"]]
RATIO = min(0.9, math.ceil(1.25 * max(ratios) * 20) / 20) if ratios else None
if ctrl:
    scc = scatter(sum((control_points(w, True) for w in ctrl), [])); unc = scatter(sum((control_points(w, False) for w in ctrl), []))
    print("control: scaled median IQR %s, unscaled %s" % (scc["median_iqr"], unc["median_iqr"]))
print("in-scope scaled/unscaled ratios:", [round(r, 3) for r in ratios], "-> RATIO", RATIO)
tols = {"TOL_N": TOL_N, "TOL_C": TOL_C, "RATIO": RATIO, "pilot": {"resolution_diffs_normalised_B8plus": diffs, "resolution_diffs_raw_all_budgets": raw_diffs, "collapse": coll},
        "rule": "PREREG-D5V3 Section 5: TOL_N = 1.5 x pilot max in-scope N1 difference on f_B(t)/f_B(0) at budgets 8 and above rounded up to 0.01; TOL_C = 1.5 x pilot max in-scope per-viscosity median bin IQR of the scaled collapse rounded up to 0.01; RATIO = 1.25 x the pilot's largest in-scope scaled-over-unscaled ratio rounded up to 0.05, at most 0.9"}
json.dump(tols, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in tols.items() if k != "pilot"}, indent=1))
