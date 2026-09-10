"""Grades a D2v9 results.json against the sealed bars of PREREG-D2V9.md (the boundary claim).
Usage: python d2v9_grade.py results.json --tols tolerances.json [--out grade.json]
tolerances.json carries REF (the frozen law's RMS log-ratio error pooled over the in-scope pilot rows),
FRAC_X, and TAU (the scope threshold on cv_knn)."""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d2v9_hubness import apply_law, rmse  # noqa: E402


def grade(res: dict, tols: dict) -> dict:
    law = res["law"]["law"]; comp = res["law"]["competitor_nominal"]; unity = res["law"]["competitor_unity"]
    REF = float(tols["REF"]); FX = float(tols["FRAC_X"]); TAU = float(tols["TAU"])
    out = {"tolerances": tols, "law": law, "competitor_nominal": comp, "competitor_unity": unity, "groups": {}, "bars": {}, "gate": None}
    fail = False

    def law_rows(w):
        return [r for r in w["rows"] if "budget_rel" not in r]

    def in_scope(rows):
        return [r for r in rows if r["variables"]["cv_knn"] >= TAU]

    def out_scope(rows):
        return [r for r in rows if r["variables"]["cv_knn"] < TAU]

    def rows_of(groups):
        return [r for w in res["worlds"] if w["group"] in groups for r in law_rows(w)]

    def e(l, rows):
        return rmse(l, rows) if rows else None

    per_world = {}
    for w in res["worlds"]:
        rs = law_rows(w); ins = in_scope(rs); outs = out_scope(rs)
        resid_out = (apply_law(law, outs) - np.array([r["targets"]["log_excess"] for r in outs])) if outs else np.array([])
        per_world[w["name"]] = {"group": w["group"], "n": len(rs), "n_in": len(ins), "n_out": len(outs), "rmse_law_in": e(law, ins), "rmse_nominal_in": e(comp, ins), "rmse_unity_in": e(unity, ins),
                                "rmse_law_out": e(law, outs), "median_residual_out": float(np.median(resid_out)) if len(resid_out) else None, "rmse_law_all": e(law, rs)}
    out["worlds"] = per_world
    for g in ("train", "heldout", "unseen", "real", "scale"):
        rs = in_scope(rows_of({g}))
        out["groups"][g] = {"n_in": len(rs), "rmse_law": e(law, rs), "rmse_nominal": e(comp, rs), "rmse_unity": e(unity, rs)}
    # L1 fresh seeds, in scope
    er = e(law, in_scope(rows_of({"train", "heldout"}))); l1 = er <= 1.5 * REF
    out["bars"]["L1_fresh_seeds"] = {"rmse": er, "limit": 1.5 * REF, "holds": l1}
    # L2 unseen, in scope: per world (worlds with in-scope rows) and pooled
    uns = {n: v for n, v in per_world.items() if v["group"] == "unseen"}; pooled_u = out["groups"]["unseen"]["rmse_law"]
    l2 = (all(v["rmse_law_in"] <= 2 * REF for v in uns.values() if v["n_in"]) and pooled_u <= 1.5 * REF) if uns else None
    out["bars"]["L2_unseen"] = {"per_world": {n: v["rmse_law_in"] for n, v in uns.items()}, "pooled": pooled_u, "limits": [2 * REF, 1.5 * REF], "holds": l2}
    if uns and pooled_u is not None and pooled_u > 3 * REF:
        fail = True
    real = {n: v for n, v in per_world.items() if v["group"] == "real"}
    l3 = all(v["rmse_law_in"] <= 3 * REF for v in real.values() if v["n_in"]) if real else None
    out["bars"]["L3_real"] = {"per_world": {n: v["rmse_law_in"] for n, v in real.items()}, "limit": 3 * REF, "holds": l3}
    sc = {n: v for n, v in per_world.items() if v["group"] == "scale"}
    l4 = all(v["rmse_law_in"] <= 2 * REF for v in sc.values() if v["n_in"]) if sc else None
    out["bars"]["L4_scale"] = {"per_world": {n: v["rmse_law_in"] for n, v in sc.items()}, "limit": 2 * REF, "holds": l4}
    rs = in_scope(rows_of({"unseen", "real", "scale"}))
    if rs:
        el, en, eu = rmse(law, rs), rmse(comp, rs), rmse(unity, rs)
        per_group = {g: (out["groups"][g]["rmse_law"], out["groups"][g]["rmse_nominal"], out["groups"][g]["rmse_unity"]) for g in ("unseen", "real", "scale") if out["groups"][g]["n_in"]}
        l5 = el <= 0.8 * en and el <= 0.8 * eu and all(a <= b and a <= c for a, b, c in per_group.values())
        if en < el or eu < el:
            fail = True
    else:
        el = en = eu = None; per_group = {}; l5 = None
    out["bars"]["L5_vs_competitors"] = {"rmse_law": el, "rmse_nominal": en, "rmse_unity": eu, "per_group_law_nominal_unity": per_group, "holds": l5}
    # S1 the boundary is real: the out-of-scope rows, pooled over every world, err by more than 2 REF, and there are at least 30 of them
    outs = out_scope(rows_of({"train", "heldout", "unseen", "real", "scale"}))
    eo = e(law, outs)
    s1 = (len(outs) >= 30 and eo > 2 * REF) if outs else None
    out["bars"]["S1_boundary_real"] = {"n_out": len(outs), "rmse_law_out": eo, "limit": 2 * REF, "holds": s1,
                                       "by_world": {n: {"n_out": v["n_out"], "rmse_out": v["rmse_law_out"], "median_residual": v["median_residual_out"]} for n, v in per_world.items() if v["n_out"]}}
    if outs and len(outs) >= 30 and eo <= REF:
        fail = True  # the scope excluded rows the law fits: the boundary claim is false as stated
    xr = {w["name"]: w["matrix"]["rank_eff_standardised"] / w["matrix"]["null_rank_eff_standardised"] for w in res["worlds"]}
    x1 = all(v <= FX for v in xr.values())
    out["bars"]["X1_latent_rank"] = {"ratio_by_world": xr, "limit": FX, "holds": x1}
    if sum(v > FX for v in xr.values()) > len(xr) / 2:
        fail = True
    pr = {w["name"]: {"hub_jaccard_same": w["polarity"]["hub_jaccard_same_alpha_mean"], "hub_jaccard_diff": w["polarity"]["hub_jaccard_diff_alpha_mean"]} for w in res["worlds"] if w["polarity"]["pairs_same"] > 0}
    p1 = all(v["hub_jaccard_same"] > v["hub_jaccard_diff"] for v in pr.values())
    out["bars"]["P1_polarity"] = {"by_world": pr, "holds": p1}
    b1 = {}
    for w in res["worlds"]:
        for r in w["rows"]:
            if "budget_rel" in r:
                b1.setdefault(f"{w['name']}_{r['observer']}", {})[str(r["budget_rel"])] = r["polarity_changed_frac"]
    out["bars"]["B1_budget_reported"] = {k: {"changed_by_budget": v, "nondecreasing": all(v[a] <= v[b] + 1e-12 for a, b in zip(sorted(v, key=float)[:-1], sorted(v, key=float)[1:]))} for k, v in b1.items()}
    bars = [l1, l2, l3, l4, l5, s1, x1, p1]
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
