"""Grades a D3v2 results.json against the sealed bars of PREREG-D3V2.md (the horizon offset law).
Usage: python d3v2_grade.py results.json --tols tolerances.json [--out grade.json]"""
from __future__ import annotations

import json
import sys

import numpy as np

EPS = 1e-9


def spearman(a, b):
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])


def grade(res: dict, tols: dict) -> dict:
    cfg = res["config"]; Ts = [str(float(t)) for t in cfg["T_ladder"]]; Bs = [str(float(b)) for b in cfg["B_ladder"]]
    OBs = [str(float(b)) for b in cfg["offset_budgets"]]
    out = {"tolerances": tols, "exact": {}, "offsets": {}, "bars": {}, "gate": None}
    fail = False; all_pass = True
    e1_viol = e1_checked = h1_viol = h1_checked = 0
    for w in res["worlds"]:
        specs = w["observers"]
        for r in w["rows"]:
            t0 = r["t0"]
            for name, spec in specs.items():
                ro = r["observers"][name]
                if spec["pd"]:
                    for T in Ts:
                        lo, lc = ro["exponent"][T], r["classical"][T]
                        if lo == lo and lc == lc:
                            e1_checked += 1
                            if abs(lo - lc) > np.log(spec["max"] / spec["min"]) / (2 * (float(T) - t0)) + EPS:
                                e1_viol += 1
                hs = [ro["horizon"][B] for B in Bs]
                for i in range(len(hs) - 1):
                    h1_checked += 1
                    if hs[i + 1] < hs[i] - EPS:
                        h1_viol += 1
                if spec["pd"] and name in r.get("euclid_horizon_scaled", {}):
                    for B in Bs:
                        lo_, hi_ = r["euclid_horizon_scaled"][name][B]; h1_checked += 1
                        if not (lo_ - EPS <= ro["horizon"][B] <= hi_ + EPS):
                            h1_viol += 1
                if spec["max"] <= 1.0 + EPS:
                    for B in Bs:
                        h1_checked += 1
                        if ro["horizon"][B] < r["euclid_horizon"][B] - EPS:
                            h1_viol += 1
    out["exact"] = {"E1_pd_bound": {"checked": e1_checked, "violations": e1_viol, "holds": e1_viol == 0},
                    "H1_horizons": {"checked": h1_checked, "violations": h1_viol, "holds": h1_viol == 0}}
    if e1_viol or h1_viol:
        fail = True; all_pass = False
    # offsets
    o1_errs = []; o2_diffs = []; sign_ok = True; sign_fail_big = False
    for w in res["worlds"]:
        clv = w["clv"]; lam1 = clv["lambda_1"]; rows = [r for r in w["rows"] if r["direction"] == "random"]
        out["offsets"][w["name"]] = {"lambda_1": lam1, "observers": {}}
        for name in w["observers"]:
            if name == "full":
                continue
            fp = clv["observers"][name]["first_passage_offset"]; pred = fp[OBs[-1]]
            entry = {"predicted_offset_by_B": fp, "constant_fraction_offset": clv["observers"][name]["constant_fraction_offset"], "mean_log_f": clv["observers"][name]["mean_log_f"], "by_B": {}}
            for B in Bs:
                d = [r["observers"][name]["horizon"][B] - r["observers"]["full"]["horizon"][B] for r in rows
                     if np.isfinite(r["observers"][name]["horizon"][B]) and np.isfinite(r["observers"]["full"]["horizon"][B])]
                d = np.array(d)
                entry["by_B"][B] = {"mean_offset": float(d.mean()) if len(d) else float("nan"), "se": float(d.std(ddof=1) / np.sqrt(len(d))) if len(d) > 1 else float("nan"),
                                    "n": int(len(d)), "fraction_later": float((d > 0).mean()) if len(d) else float("nan"), "error": float(abs(d.mean() - fp[B])) if len(d) else float("nan")}
            for B in OBs:
                e = entry["by_B"][B]
                o1_errs.append((w["name"], name, B, e["error"]))
                if fp[B] != 0 and np.sign(e["mean_offset"]) != np.sign(fp[B]):
                    sign_ok = False
                    if abs(fp[B]) > 0.1 and B == OBs[-1]:
                        sign_fail_big = True
            o2_diffs.append((w["name"], name, abs(entry["by_B"][OBs[-1]]["mean_offset"] - entry["by_B"][OBs[0]]["mean_offset"])))
            out["offsets"][w["name"]]["observers"][name] = entry
    o1 = all(e[3] <= tols["O1"] for e in o1_errs); worst = max(o1_errs, key=lambda e: e[3])
    out["bars"]["O1_offset_law"] = {"holds": o1, "worst": {"world": worst[0], "observer": worst[1], "B": worst[2], "error": worst[3]}, "n_cells": len(o1_errs)}
    o2 = all(d[2] <= tols["O2"] for d in o2_diffs); worst2 = max(o2_diffs, key=lambda d: d[2])
    out["bars"]["O2_convergence"] = {"holds": o2, "worst": {"world": worst2[0], "observer": worst2[1], "diff": worst2[2]}}
    l63 = out["offsets"].get("lorenz63", {}).get("observers", {})
    names = list(l63.keys())
    rho = spearman([l63[n]["by_B"][OBs[-1]]["mean_offset"] for n in names], [l63[n]["predicted_offset_by_B"][OBs[-1]] for n in names]) if len(names) >= 3 else float("nan")
    o3 = sign_ok and rho >= 0.9
    out["bars"]["O3_sign_and_order"] = {"holds": o3, "signs_agree": sign_ok, "spearman_lorenz63_at_largest_B": rho}
    if sign_fail_big:
        fail = True
    l96 = out["offsets"].get("lorenz96", {})
    if l96 and "sub" in l96["observers"] and "sub2" in l96["observers"]:
        a, b = l96["observers"]["sub"], l96["observers"]["sub2"]
        dpred = max(abs(a["predicted_offset_by_B"][B] - b["predicted_offset_by_B"][B]) for B in OBs); dmeas = max(abs(a["by_B"][B]["mean_offset"] - b["by_B"][B]["mean_offset"]) for B in OBs)
        o4 = dpred <= tols["O4"] and dmeas <= tols["O4"]
        out["bars"]["O4_symmetry"] = {"holds": o4, "predicted_diff": dpred, "measured_diff_max": dmeas}
    else:
        o4 = True
    o5 = True; brk = {}
    for w in res["worlds"]:
        if "aniso" in w["observers"]:
            a, b = w["observers"]["aniso"]["min"], w["observers"]["aniso"]["max"]; lam1 = w["clv"]["lambda_1"]
            lo, hi = -np.log(np.sqrt(b)) / lam1, -np.log(np.sqrt(a)) / lam1
            ent = out["offsets"][w["name"]]["observers"]["aniso"]
            inside = all(lo - EPS <= ent["by_B"][B]["mean_offset"] <= hi + EPS for B in OBs) and all(lo - EPS <= ent["predicted_offset_by_B"][B] <= hi + EPS for B in OBs)
            brk[w["name"]] = {"bracket": [lo, hi], "predicted": {B: ent["predicted_offset_by_B"][B] for B in OBs}, "measured": {B: ent["by_B"][B]["mean_offset"] for B in OBs}, "inside": inside}
            o5 = o5 and inside
    out["bars"]["O5_bracket"] = {"holds": o5, "by_world": brk}
    all_pass = all_pass and o1 and o2 and o3 and o4 and o5
    out["gate"] = "PASS" if all_pass else ("FAIL" if fail else "INDETERMINATE")
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0]
    tols = json.load(open(argv[argv.index("--tols") + 1], encoding="utf-8-sig"))
    outp = argv[argv.index("--out") + 1] if "--out" in argv else None
    g = grade(json.load(open(path, encoding="utf-8-sig")), tols)
    text = json.dumps(g, indent=1)
    if outp:
        open(outp, "w", encoding="utf-8").write(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
