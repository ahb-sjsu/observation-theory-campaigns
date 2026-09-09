"""Grades a D2v6 results.json against the sealed bars of PREREG-D2V6.md.
Usage: python d2v6_grade.py results.json --tols tolerances.json [--out grade.json]
tolerances.json carries REF (the frozen law's error pooled over every pilot row) and FRAC_X."""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d2v6_hubness import rmse  # noqa: E402


def grade(res: dict, tols: dict) -> dict:
    law = res["law"]["law"]; comp = res["law"]["competitor_nominal"]; d2 = res["law"]["competitor_d2"]; d2v2 = res["law"]["competitor_d2v2"]; d2v3 = res["law"]["competitor_d2v3"]; d2v4 = res["law"]["competitor_d2v4"]; d2v5 = res["law"]["competitor_d2v5"]
    REF = float(tols["REF"]); FX = float(tols["FRAC_X"])
    out = {"tolerances": tols, "law": law, "competitor_nominal": comp, "competitor_d2": d2, "competitor_d2v2": d2v2, "competitor_d2v3": d2v3, "competitor_d2v4": d2v4, "competitor_d2v5": d2v5, "groups": {}, "bars": {}, "gate": None}
    fail = False

    def law_rows(w):
        return [r for r in w["rows"] if "budget_rel" not in r]

    def rows_of(groups):
        return [r for w in res["worlds"] if w["group"] in groups for r in law_rows(w)]

    per_world = {w["name"]: {"group": w["group"], "rmse_law": rmse(law, law_rows(w)), "rmse_nominal": rmse(comp, law_rows(w)), "rmse_d2": rmse(d2, law_rows(w)), "rmse_d2v2": rmse(d2v2, law_rows(w)), "rmse_d2v3": rmse(d2v3, law_rows(w)), "rmse_d2v4": rmse(d2v4, law_rows(w)), "rmse_d2v5": rmse(d2v5, law_rows(w))} for w in res["worlds"]}
    out["worlds"] = per_world
    for g in ("train", "heldout", "unseen", "real", "scale"):
        rs = rows_of({g})
        out["groups"][g] = {"n": len(rs), "rmse_law": rmse(law, rs) if rs else None, "rmse_nominal": rmse(comp, rs) if rs else None, "rmse_d2": rmse(d2, rs) if rs else None, "rmse_d2v2": rmse(d2v2, rs) if rs else None, "rmse_d2v3": rmse(d2v3, rs) if rs else None, "rmse_d2v4": rmse(d2v4, rs) if rs else None, "rmse_d2v5": rmse(d2v5, rs) if rs else None}
    # L1 fresh seeds
    e = rmse(law, rows_of({"train", "heldout"})); l1 = e <= 1.5 * REF
    out["bars"]["L1_fresh_seeds"] = {"rmse": e, "limit": 1.5 * REF, "holds": l1}
    # L2 unseen
    uns = {n: v for n, v in per_world.items() if v["group"] == "unseen"}; pooled_u = out["groups"]["unseen"]["rmse_law"]
    l2 = (all(v["rmse_law"] <= 2 * REF for v in uns.values()) and pooled_u <= 1.5 * REF) if uns else None
    out["bars"]["L2_unseen"] = {"per_world": {n: v["rmse_law"] for n, v in uns.items()}, "pooled": pooled_u, "limits": [2 * REF, 1.5 * REF], "holds": l2}
    if uns and pooled_u > 3 * REF:
        fail = True
    # L3 real
    real = {n: v for n, v in per_world.items() if v["group"] == "real"}
    l3 = all(v["rmse_law"] <= 3 * REF for v in real.values()) if real else None
    out["bars"]["L3_real"] = {"per_world": {n: v["rmse_law"] for n, v in real.items()}, "limit": 3 * REF, "holds": l3}
    # L4 scale
    sc = {n: v for n, v in per_world.items() if v["group"] == "scale"}
    l4 = all(v["rmse_law"] <= 2 * REF for v in sc.values()) if sc else None
    out["bars"]["L4_scale"] = {"per_world": {n: v["rmse_law"] for n, v in sc.items()}, "limit": 2 * REF, "holds": l4}
    # L5 against both competitors, per transfer group and pooled
    rs = rows_of({"unseen", "real", "scale"})
    if rs:
        el, en, ed, ev, e3, e4, e5 = rmse(law, rs), rmse(comp, rs), rmse(d2, rs), rmse(d2v2, rs), rmse(d2v3, rs), rmse(d2v4, rs), rmse(d2v5, rs)
        per_group = {g: (out["groups"][g]["rmse_law"], out["groups"][g]["rmse_nominal"], out["groups"][g]["rmse_d2"], out["groups"][g]["rmse_d2v2"], out["groups"][g]["rmse_d2v3"], out["groups"][g]["rmse_d2v4"], out["groups"][g]["rmse_d2v5"]) for g in ("unseen", "real", "scale") if out["groups"][g]["n"]}
        l5 = el <= 0.8 * en and el <= 0.8 * ed and el <= 0.9 * ev and el <= 0.95 * e3 and el <= 0.95 * e4 and el <= 0.95 * e5 and all(a <= min(others) for a, *others in per_group.values())
        if min(en, ed, ev, e3, e4, e5) < el:
            fail = True
    else:
        el = en = ed = ev = e3 = e4 = e5 = None; per_group = {}; l5 = None
    out["bars"]["L5_vs_competitors"] = {"rmse_law": el, "rmse_nominal": en, "rmse_d2": ed, "rmse_d2v2": ev, "rmse_d2v3": e3, "rmse_d2v4": e4, "rmse_d2v5": e5, "per_group_law_nominal_d2_d2v2_d2v3_d2v4_d2v5": per_group, "holds": l5}
    # X1 latent rank
    xr = {w["name"]: w["matrix"]["rank_eff_standardised"] / w["matrix"]["null_rank_eff_standardised"] for w in res["worlds"]}
    x1 = all(v <= FX for v in xr.values())
    out["bars"]["X1_latent_rank"] = {"ratio_by_world": xr, "limit": FX, "holds": x1}
    if sum(v > FX for v in xr.values()) > len(xr) / 2:
        fail = True
    # P1 polarity
    pr = {w["name"]: {"hub_jaccard_same": w["polarity"]["hub_jaccard_same_alpha_mean"], "hub_jaccard_diff": w["polarity"]["hub_jaccard_diff_alpha_mean"]} for w in res["worlds"] if w["polarity"]["pairs_same"] > 0}
    p1 = all(v["hub_jaccard_same"] > v["hub_jaccard_diff"] for v in pr.values())
    out["bars"]["P1_polarity"] = {"by_world": pr, "holds": p1}
    # B1 exploratory
    b1 = {}
    for w in res["worlds"]:
        for r in w["rows"]:
            if "budget_rel" in r:
                b1.setdefault(f"{w['name']}_{r['observer']}", {})[str(r["budget_rel"])] = r["polarity_changed_frac"]
    out["bars"]["B1_budget_reported"] = {k: {"changed_by_budget": v, "nondecreasing": all(v[a] <= v[b] + 1e-12 for a, b in zip(sorted(v, key=float)[:-1], sorted(v, key=float)[1:]))} for k, v in b1.items()}
    bars = [l1, l2, l3, l4, l5, x1, p1]
    if any(b is None for b in bars):
        out["gate"] = "NOT ALL GROUPS RUN (pilot or probe): " + ("all run bars hold" if all(b for b in bars if b is not None) else "a run bar fails")
        return out
    out["gate"] = "PASS" if all(bars) else ("FAIL" if fail else "INDETERMINATE")
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
