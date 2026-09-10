"""Builds the D2v9 files: d2v9_hubness.py (D2v8's workload with a D2v9 header; no search, the frozen
D2v7 law is applied), law.json (the D2v7 law and its competitors, verbatim), d2v9_grade.py (scope-aware
grader with the boundary bar S1), d2v9_fix_tols.py (REF on in-scope pilot rows) and
d2v9_prereg_config.json (D2v8's world plus an unseen ball at d = 256, fresh real slices, new seeds)."""
import json
import os

SP = r"C:\Users\abptl\AppData\Local\Temp\claude\C--source\f9dd774c-068a-466c-aa48-fbb6bdd82c75\scratchpad"
TAU = 0.015


def rd(p):
    return open(os.path.join(SP, p), encoding="utf-8").read().replace("\r\n", "\n")


def wr(p, s):
    open(os.path.join(SP, p), "w", encoding="utf-8", newline="\n").write(s)


s = rd("d2v8_hubness.py")
old = '"""D2v8: observer-relative hubness, the excess law with full-dimensional worlds at d = 384 to 512\nin the discovery set (OD track, gate D2v8), built on the D2v7 workload.'
assert s.count(old) == 1
s = s.replace(old, '''"""D2v9: observer-relative hubness, the boundary of the excess law (OD track, gate D2v9), built on the
D2v8 workload with no search: the frozen D2v7 law is applied as it stands.

Eight registrations and an exploration on their rows placed the D2v7 law at the frontier of the declared
family on this world and named its boundary: the concentration term, a reciprocal of the coefficient of
variation of the k-th neighbour distance, diverges on over-concentrated worlds under near-isotropic readers
(the uniform ball at d = 384 reads cv_knn 0.003), where the law predicts an excess near zero against a truth
of 1.4. D2v9 registers that boundary as the claim: inside a declared scope, cv_knn at least 0.015 on the
observed data, the frozen law predicts the log hub excess on fresh worlds within its limits; outside it,
the law is not claimed and its failure is recorded. The grader masks rows by scope. The world is D2v8's
with an unseen ball at d = 256 added, fresh real slices and fresh seeds.

D2v8 header follows.

(OD track, gate D2v8), built on the D2v7 workload.''')
s = s.replace("    python d2v8_hubness.py --selftest", "    python d2v9_hubness.py --selftest")
# no D2v7 competitor entry in D2v9's law.json (the D2v7 law IS the law); drop it from the evaluation line
old_ev = ', "rmse_d2v7_law": rmse(frozen["competitor_d2v7"], rs), "n": len(rs)}'
assert s.count(old_ev) == 1
s = s.replace(old_ev, ', "n": len(rs)}')
wr("d2v9_hubness.py", s)

# the law: D2v7's law.json verbatim, with a note
law = json.load(open(os.path.join(SP, "d2v7_law.json"), encoding="utf-8"))
law["note"] = "the frozen D2v7 law (observation-theory-campaigns/experiments/OD/D2v7/law.json) and its competitors, applied without change; D2v9 registers its boundary"
law["scope"] = {"variable": "cv_knn", "min": TAU, "note": "a row is in scope when the coefficient of variation of the k_law-th neighbour distance on the observed data is at least 0.015"}
json.dump(law, open(os.path.join(SP, "d2v9_law.json"), "w", encoding="utf-8"), indent=1)

# grader, scope-aware
wr("d2v9_grade.py", '''"""Grades a D2v9 results.json against the sealed bars of PREREG-D2V9.md (the boundary claim).
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
        open(outp, "w", encoding="utf-8").write(text + "\\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
''')

# tolerance fixer: REF on in-scope pilot rows; no search
wr("d2v9_fix_tols.py", '''"""Fixes the D2v9 tolerances from the pilot by the rule of PREREG-D2V9 Section 5: REF = the frozen law's RMS
log-ratio error pooled over the IN-SCOPE pilot rows (cv_knn >= TAU); FRAC_X = 1.5 x the pilot's largest ratio of
effective ranks, rounded up to two decimals, at most 0.9. Prints the pilot summary."""
import json
import math
import sys

import numpy as np

sys.path.insert(0, r"C:\\Users\\abptl\\AppData\\Local\\Temp\\claude\\C--source\\f9dd774c-068a-466c-aa48-fbb6bdd82c75\\scratchpad")
from d2v9_hubness import apply_law, rmse  # noqa: E402

TAU = %r
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
    print("%%-18s %%-8s in %%2d/%%2d rmse law %%.3f nominal %%.3f unity %%.3f | out %%2d rmse %%s med res %%s | jac same %%.3f diff %%.3f | excess %%.2f..%%.2f" %% (
        w["name"], w["group"], len(ins), len(rs), rmse(law, ins) if ins else float("nan"), rmse(comp, ins) if ins else float("nan"), rmse(unity, ins) if ins else float("nan"),
        len(outs), ("%%.2f" %% rmse(law, outs)) if outs else "-", ("%%.2f" %% np.median(ro)) if outs else "-", p["hub_jaccard_same_alpha_mean"], p["hub_jaccard_diff_alpha_mean"],
        min(r["targets"]["excess"] for r in rs), max(r["targets"]["excess"] for r in rs)))
pooled = rmse(law, allin)
print("pilot rows %%d, in scope %%d, out of scope %%d; REF (in-scope pooled) %%.4f; nominal %%.4f unity %%.4f; out-of-scope rmse %%s" %% (
    len(allin) + len(allout), len(allin), len(allout), pooled, rmse(comp, allin), rmse(unity, allin), ("%%.3f" %% rmse(law, allout)) if allout else "-"))
tols = {"REF": float(pooled), "REF_note": "the frozen D2v7 law's RMS error in log excess pooled over the in-scope pilot rows (cv_knn >= TAU)", "TAU": TAU,
        "pooled_nominal": rmse(comp, allin), "pooled_unity": rmse(unity, allin), "n_in": len(allin), "n_out": len(allout), "rmse_out": rmse(law, allout) if allout else None,
        "FRAC_X": min(math.ceil(max(ratios.values()) * 1.5 * 100) / 100, 0.9),
        "rule": "PREREG-D2V9 Section 5: REF = the frozen law's RMS log-ratio error pooled over the in-scope pilot rows; TAU = 0.015 declared; FRAC_X = 1.5 x pilot max rank ratio rounded up to 2 decimals, at most 0.9",
        "pilot_rank_ratios": ratios}
json.dump(tols, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in tols.items() if k != "pilot_rank_ratios"}, indent=1))
''' % TAU)

# configuration: D2v8's world plus an unseen ball at d = 256; fresh slices; new seeds
c = json.load(open(os.path.join(SP, "d2v8_prereg_config.json"), encoding="utf-8"))
c["world"] = ("D2v8's world (41 training, 9 held-out, 17 unseen worlds, 4 real slices, 8 scale cells) with an unseen ball at d = 256 added, under the log Poisson hub-excess target, with NO search: the frozen D2v7 law is applied as it stands. The claim is the law's boundary: a row is in scope when the coefficient of variation of the k-th neighbour distance on the observed data is at least 0.015, and the law is claimed inside the scope only. Real corpora on fresh slices (Wikipedia part 004 at 600,000 and 800,000, SIFT base at 10,000,000 and 11,000,000; the SIFT query file has 10,000 rows and its window overlaps earlier gates'); the scale Wikipedia cell on part 002 at 900,000. Competitors: the nominal-only law frozen with D2v7 and the chance level.")
c["seed_probe"] = 20261016; c["seed_pilot"] = 20261017; c["seed_run"] = 20261018
c["bars"] = "PREREG-D2V9.md Section 5; the frozen D2v7 law, its nominal-dimension competitor and the chance level in law.json; the scope threshold TAU = 0.015 on cv_knn; REF the frozen law's RMS log-ratio error pooled over the in-scope pilot rows; tolerances declared multiples of REF; S1 the boundary bar"
for w in c["worlds"]:
    w.pop("in_probe", None)
by = {w["name"]: w for w in c["worlds"]}
for n in ("u_ball_d384", "cube_d512", "lap_d128"):
    by[n]["in_probe"] = True
ins = c["worlds"].index(by["u_ball_d384"]) + 1
c["worlds"][ins:ins] = [{"name": "u_ball_d256", "group": "unseen", "family": "ball", "d": 256, "N": 4000, "seed_offset": 119}]
by["r_wiki1024"].update({"offset": 600000, "path": "/archive/tqp_real/wiki1024/part_004.npy"})
by["r_wiki1024_b"].update({"offset": 800000, "path": "/archive/tqp_real/wiki1024/part_004.npy"})
by["r_sift128"].update({"offset": 10000000})
by["r_siftq128"].update({"offset": 3000})
by["s_wiki1024_N12000"].update({"offset": 900000, "path": "/archive/tqp_real/wiki1024/part_002.npy"})
by["s_sift128_N16000"].update({"offset": 11000000})
json.dump(c, open(os.path.join(SP, "d2v9_prereg_config.json"), "w", encoding="utf-8"), indent=1)
print("d2v9 files written; worlds", len(c["worlds"]), "probe", [w["name"] for w in c["worlds"] if w.get("in_probe")], "TAU", TAU)
