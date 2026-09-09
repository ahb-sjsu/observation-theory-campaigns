"""Builds the D2v7 files from the D2v6 ones: d2v7_hubness.py (target = log Poisson hub excess; competitors
the nominal-only law and the chance level; no frozen skew laws), d2v7_grade.py, d2v7_fix_tols.py and
d2v7_prereg_config.json (D2v6's world, fresh real slices, new seeds)."""
import json
import os
import re

SP = r"C:\Users\abptl\AppData\Local\Temp\claude\C--source\f9dd774c-068a-466c-aa48-fbb6bdd82c75\scratchpad"


def rd(p):
    return open(os.path.join(SP, p), encoding="utf-8").read().replace("\r\n", "\n")


def wr(p, s):
    open(os.path.join(SP, p), "w", encoding="utf-8", newline="\n").write(s)


s = rd("d2v6_hubness.py")


def sub(a, b, count=1):
    global s
    assert s.count(a) == count, (s.count(a), a[:70])
    s = s.replace(a, b)


sub('"""D2v6: observer-relative hubness, the law with heavy tails placed at the transfer dimensions\n(OD track, gate D2v6), built on the D2v5 workload.', '''"""D2v7: observer-relative hubness, the law with the Poisson hub excess as the target (OD track,
gate D2v7), built on the D2v6 workload.

Three registrations (D2v4, D2v5, D2v6) placed the same worlds on both sides of the same limit and
the record named the family, not the discovery set, as the limit: every law's largest errors sat
where the hubness skewness exceeds 12, on isotropic readers of heavy-tailed or very high-dimensional
clouds, where a linear law in the skewness cannot turn over. D2v7 changes the target. The hubness
measure is the Poisson hub excess of the program's instrument, the busiest point's occurrence count
divided by the ceiling that a random assignment of the same retrieval slots would reach; it is
measured in the log, so the law predicts log excess, errors are root-mean-square log ratios, and the
chance level is the constant zero. The world, observers, k, budget cells and feature pool are D2v6's,
so the two registrations differ in the target alone. The frozen skew laws are not competitors for a
different target; the competitors are the nominal-only law and the chance level.

D2v6 header follows.

(OD track, gate D2v6), built on the D2v5 workload.''')
# the target
sub('''    return {"skew": skewness(counts), "excess": float(counts.max() / max(poisson_null_max(float(k), N), 1)),''',
    '''    excess = float(counts.max() / max(poisson_null_max(float(k), N), 1))
    return {"skew": skewness(counts), "excess": excess, "log_excess": float(np.log(max(excess, 1e-6))),''')
# transforms: identity only for a target already in the log
sub('''def discover(train: list[dict], heldout: list[dict], target: str, max_terms: int = 2, pool: set | None = None, transforms=("identity", "log1p")) -> dict:''',
    '''UNITY_LAW = {"target": "log_excess", "features": [], "coef": [0.0], "transform": "identity", "note": "the chance level: hub excess 1, the busiest point explained by a random assignment of the retrieval slots"}


def discover(train: list[dict], heldout: list[dict], target: str, max_terms: int = 2, pool: set | None = None, transforms=("identity",)) -> dict:''')
# the frozen block in run()
a = s.index('        frozen = {"law": law, "competitor_nominal": comp,'); b = s.index('rmse(D2V5_FROZEN_LAW, train)}', a) + len('rmse(D2V5_FROZEN_LAW, train)}')
s = s[:a] + '''        frozen = {"law": law, "competitor_nominal": comp, "competitor_unity": UNITY_LAW, "target": target, "frozen_from": seed_role, "seed": seed, "n_train": len(train), "n_heldout": len(held),
                  "unity_heldout_rmse": rmse(UNITY_LAW, held), "unity_train_rmse": rmse(UNITY_LAW, train)}''' + s[b:]
s = re.sub(r'            result\["evaluation"\]\[w\["name"\]\] = \{.*\n',
           '''            result["evaluation"][w["name"]] = {"group": w["group"], "rmse_law": rmse(frozen["law"], rs), "rmse_competitor": rmse(frozen["competitor_nominal"], rs), "rmse_unity": rmse(frozen["competitor_unity"], rs), "n": len(rs)}\n''', s, count=1)
assert s.count('"rmse_unity"') == 1
# self-test: the excess target on planted counts, the unity law, and a planted log-excess law
sub('''    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails''', '''    # hub excess: counts with one point at 3 x the Poisson ceiling read excess 3 and log excess log 3; the unity law predicts 0
    cnt = np.full(2000, 10); ceil = poisson_null_max(10.0, 2000); cnt[0] = 3 * ceil; hs = hub_stats(cnt, 2000, 10)
    ok = abs(hs["excess"] - 3.0) < 1e-9 and abs(hs["log_excess"] - np.log(3.0)) < 1e-9 and apply_law(UNITY_LAW, [{"variables": {}, "targets": hs}])[0] == 0.0
    print("hub excess target: excess %.2f log %.3f (ceiling %d), unity predicts 0" % (hs["excess"], hs["log_excess"], ceil), ok); fails += 0 if ok else 1
    rows3 = [{"variables": {**{k: 1.0 for k in BASE}, "id_twonn": float(i), "k": 10.0, "N": 4000.0}, "targets": {"log_excess": 0.3 + 0.8 * np.log(i)}} for i in (2, 4, 8, 16, 32)]
    law3 = discover(rows3, rows3, "log_excess", 1, {"log_id_twonn", "id_twonn", "log_N"}); ok = law3["features"] == ["log_id_twonn"] and law3["transform"] == "identity" and abs(law3["coef"][1] - 0.8) < 1e-9
    print("planted log-excess law recovered:", ok, law3["features"]); fails += 0 if ok else 1
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails''')
sub("    python d2v6_hubness.py --selftest", "    python d2v7_hubness.py --selftest")
# the log1p round-trip check of the earlier family is kept, with the transform it tests named explicitly
sub('''law2 = discover(rows2, rows2, "skew", 1, {"log_d_eff", "d_eff"})''', '''law2 = discover(rows2, rows2, "skew", 1, {"log_d_eff", "d_eff"}, transforms=("identity", "log1p"))''')
wr("d2v7_hubness.py", s)

# grader, fresh
wr("d2v7_grade.py", '''"""Grades a D2v7 results.json against the sealed bars of PREREG-D2V7.md.
Usage: python d2v7_grade.py results.json --tols tolerances.json [--out grade.json]
tolerances.json carries REF (the frozen law's error, in log excess, pooled over every pilot row) and FRAC_X."""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d2v7_hubness import rmse  # noqa: E402


def grade(res: dict, tols: dict) -> dict:
    law = res["law"]["law"]; comp = res["law"]["competitor_nominal"]; unity = res["law"]["competitor_unity"]
    REF = float(tols["REF"]); FX = float(tols["FRAC_X"])
    out = {"tolerances": tols, "law": law, "competitor_nominal": comp, "competitor_unity": unity, "groups": {}, "bars": {}, "gate": None}
    fail = False

    def law_rows(w):
        return [r for r in w["rows"] if "budget_rel" not in r]

    def rows_of(groups):
        return [r for w in res["worlds"] if w["group"] in groups for r in law_rows(w)]

    per_world = {w["name"]: {"group": w["group"], "rmse_law": rmse(law, law_rows(w)), "rmse_nominal": rmse(comp, law_rows(w)), "rmse_unity": rmse(unity, law_rows(w))} for w in res["worlds"]}
    out["worlds"] = per_world
    for g in ("train", "heldout", "unseen", "real", "scale"):
        rs = rows_of({g})
        out["groups"][g] = {"n": len(rs), "rmse_law": rmse(law, rs) if rs else None, "rmse_nominal": rmse(comp, rs) if rs else None, "rmse_unity": rmse(unity, rs) if rs else None}
    e = rmse(law, rows_of({"train", "heldout"})); l1 = e <= 1.5 * REF
    out["bars"]["L1_fresh_seeds"] = {"rmse": e, "limit": 1.5 * REF, "holds": l1}
    uns = {n: v for n, v in per_world.items() if v["group"] == "unseen"}; pooled_u = out["groups"]["unseen"]["rmse_law"]
    l2 = (all(v["rmse_law"] <= 2 * REF for v in uns.values()) and pooled_u <= 1.5 * REF) if uns else None
    out["bars"]["L2_unseen"] = {"per_world": {n: v["rmse_law"] for n, v in uns.items()}, "pooled": pooled_u, "limits": [2 * REF, 1.5 * REF], "holds": l2}
    if uns and pooled_u > 3 * REF:
        fail = True
    real = {n: v for n, v in per_world.items() if v["group"] == "real"}
    l3 = all(v["rmse_law"] <= 3 * REF for v in real.values()) if real else None
    out["bars"]["L3_real"] = {"per_world": {n: v["rmse_law"] for n, v in real.items()}, "limit": 3 * REF, "holds": l3}
    sc = {n: v for n, v in per_world.items() if v["group"] == "scale"}
    l4 = all(v["rmse_law"] <= 2 * REF for v in sc.values()) if sc else None
    out["bars"]["L4_scale"] = {"per_world": {n: v["rmse_law"] for n, v in sc.items()}, "limit": 2 * REF, "holds": l4}
    rs = rows_of({"unseen", "real", "scale"})
    if rs:
        el, en, eu = rmse(law, rs), rmse(comp, rs), rmse(unity, rs)
        per_group = {g: (out["groups"][g]["rmse_law"], out["groups"][g]["rmse_nominal"], out["groups"][g]["rmse_unity"]) for g in ("unseen", "real", "scale") if out["groups"][g]["n"]}
        l5 = el <= 0.8 * en and el <= 0.8 * eu and all(a <= b and a <= c for a, b, c in per_group.values())
        if en < el or eu < el:
            fail = True
    else:
        el = en = eu = None; per_group = {}; l5 = None
    out["bars"]["L5_vs_competitors"] = {"rmse_law": el, "rmse_nominal": en, "rmse_unity": eu, "per_group_law_nominal_unity": per_group, "holds": l5}
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
        open(outp, "w", encoding="utf-8").write(text + "\\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
''')

# tolerance fixer, fresh
wr("d2v7_fix_tols.py", '''"""Fixes the D2v7 tolerances from the pilot by the rule of PREREG-D2V7 Section 5 and prints the pilot
summary: REF = the frozen law's RMS log-ratio error pooled over every pilot row; FRAC_X = 1.5 x the pilot's
largest ratio of effective ranks, rounded up to two decimals, at most 0.9."""
import json
import math
import sys

import numpy as np

sys.path.insert(0, r"C:\\Users\\abptl\\AppData\\Local\\Temp\\claude\\C--source\\f9dd774c-068a-466c-aa48-fbb6bdd82c75\\scratchpad")
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
''')

# configuration
c = json.load(open(os.path.join(SP, "d2v6_prereg_config.json"), encoding="utf-8"))
c["world"] = ("D2v6's world unchanged (37 training, 9 held-out, 15 unseen worlds, 4 real slices, 8 scale cells; the same observers, k ladder and budget cells) with the target changed: the law predicts the log of the Poisson hub excess of the program's instrument, the busiest point's occurrence count over the ceiling a random assignment of the retrieval slots would reach. Errors are root-mean-square log ratios. Real corpora on fresh slices (Wikipedia part 003 at 250,000 and 750,000, SIFT base at 6,000,000 and 7,000,000; the SIFT query file has 10,000 rows and its window overlaps earlier gates'); the scale Wikipedia cell on part 004. Competitors: the nominal-only law on the same target and the chance level, log excess 0. The frozen skew laws of D2 to D2v6 predict a different target and are not competitors.")
c["law_target"] = "log_excess"
c["seed_probe"] = 20261010; c["seed_pilot"] = 20261011; c["seed_run"] = 20261012
c["bars"] = "PREREG-D2V7.md Section 5; the law, its nominal-dimension competitor and the chance level in law.json; REF the frozen law's RMS log-ratio error pooled over every pilot row; tolerances declared multiples of REF"
for w in c["worlds"]:
    w.pop("in_probe", None)
by = {w["name"]: w for w in c["worlds"]}
for n in ("g_a0_d64", "t3_d256", "roll_d64", "h_g_a05_d192"):
    by[n]["in_probe"] = True
by["r_wiki1024"].update({"offset": 250000, "path": "/archive/tqp_real/wiki1024/part_003.npy"})
by["r_wiki1024_b"].update({"offset": 750000, "path": "/archive/tqp_real/wiki1024/part_003.npy"})
by["r_sift128"].update({"offset": 6000000})
by["r_siftq128"].update({"offset": 4000})
by["s_wiki1024_N12000"].update({"offset": 0, "path": "/archive/tqp_real/wiki1024/part_004.npy"})
by["s_sift128_N16000"].update({"offset": 7000000})
json.dump(c, open(os.path.join(SP, "d2v7_prereg_config.json"), "w", encoding="utf-8"), indent=1)
print("d2v7 files written; worlds", len(c["worlds"]), "target", c["law_target"], "probe", [w["name"] for w in c["worlds"] if w.get("in_probe")])
