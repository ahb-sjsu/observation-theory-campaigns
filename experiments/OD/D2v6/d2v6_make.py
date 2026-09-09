"""Builds the D2v6 files from the D2v5 ones: d2v6_hubness.py (the frozen D2v5 law as a sixth competitor),
d2v6_grade.py, d2v6_fix_tols.py and d2v6_prereg_config.json (heavy tails placed AT the transfer
dimensions in the discovery set, bracketing the unseen heavy-tailed worlds; fresh real slices; new seeds)."""
import json
import os

SP = r"C:\Users\abptl\AppData\Local\Temp\claude\C--source\f9dd774c-068a-466c-aa48-fbb6bdd82c75\scratchpad"


def rd(p):
    return open(os.path.join(SP, p), encoding="utf-8").read().replace("\r\n", "\n")


def wr(p, s):
    open(os.path.join(SP, p), "w", encoding="utf-8", newline="\n").write(s)


s = rd("d2v5_hubness.py")


def sub(a, b, count=1):
    global s
    assert s.count(a) == count, (s.count(a), a[:70])
    s = s.replace(a, b)


D2V5 = json.load(open(os.path.join(SP, "d2v5_law.json"), encoding="utf-8"))["law"]
assert D2V5["features"] == ["inv_cv_d", "log_id_twonn", "sqrt_d_eff"] and D2V5["transform"] == "identity"

sub('"""D2v5: observer-relative hubness, the law with a tail variable measured on the neighbour\ndistances (OD track, gate D2v5), built on the D2v4 workload.', '''"""D2v6: observer-relative hubness, the law with heavy tails placed at the transfer dimensions
(OD track, gate D2v6), built on the D2v5 workload.

D2v5 put four neighbour-distance tail variables into the pool and the search declined them, freezing
D2v3's form refitted. D2v6 registers the second repair D2v4's record named: heavy-tailed clouds in
the discovery set at the dimensions the transfer asks about, bracketing the unseen worlds. Student t
with 3 and with 5 degrees at d = 256 join the training worlds around the unseen Student t with 4
degrees at d = 256; Laplace at d = 192 and d = 256 join around an unseen Laplace at d = 224; so the
transfer to heavy tails is across tail weight or dimension between training neighbours, not beyond
them. The pool, the search and the target are D2v5's, and the frozen D2, D2v2, D2v3, D2v4 and D2v5
laws are carried as competitors.

D2v5 header follows.

(OD track, gate D2v5), built on the D2v4 workload.''')
sub('''D2V4_FROZEN_LAW = {''', '''D2V5_FROZEN_LAW = {"target": "skew", "features": %s, "coef": %r, "transform": "identity",
                   "note": "the law gate D2v5 froze with neighbour-distance tail variables in the pool (observation-theory-campaigns/experiments/OD/D2v5/law.json), carried as a fixed competitor"}
D2V4_FROZEN_LAW = {''' % (json.dumps(D2V5["features"]), D2V5["coef"]))
sub('''"competitor_d2v4": D2V4_FROZEN_LAW, "target": target,''', '''"competitor_d2v4": D2V4_FROZEN_LAW, "competitor_d2v5": D2V5_FROZEN_LAW, "target": target,''')
sub('''                  "d2v4_law_heldout_rmse": rmse(D2V4_FROZEN_LAW, held), "d2v4_law_train_rmse": rmse(D2V4_FROZEN_LAW, train)}''',
    '''                  "d2v4_law_heldout_rmse": rmse(D2V4_FROZEN_LAW, held), "d2v4_law_train_rmse": rmse(D2V4_FROZEN_LAW, train),
                  "d2v5_law_heldout_rmse": rmse(D2V5_FROZEN_LAW, held), "d2v5_law_train_rmse": rmse(D2V5_FROZEN_LAW, train)}''')
sub('''"rmse_d2v4_law": rmse(frozen["competitor_d2v4"], rs), "n": len(rs)}''', '''"rmse_d2v4_law": rmse(frozen["competitor_d2v4"], rs), "rmse_d2v5_law": rmse(frozen["competitor_d2v5"], rs), "n": len(rs)}''')
sub('''    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails''', '''    row = {"variables": {"cv_d": 0.2, "id_twonn": 20.0, "d_eff": 40.0}, "targets": {"skew": 1.0}}
    pred = apply_law(D2V5_FROZEN_LAW, [row])[0]; c5 = D2V5_FROZEN_LAW["coef"]; exp = c5[0] + c5[1] / 0.2 + c5[2] * np.log(20.0) + c5[3] * np.sqrt(40.0)
    ok = abs(pred - exp) < 1e-9; print("D2v5 frozen law applies: %.3f" % pred, ok); fails += 0 if ok else 1
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails''')
sub("    python d2v5_hubness.py --selftest", "    python d2v6_hubness.py --selftest")
wr("d2v6_hubness.py", s)

# grader
g = rd("d2v5_grade.py")
g = g.replace("D2v5", "D2v6").replace("PREREG-D2V5", "PREREG-D2V6").replace("d2v5_grade.py", "d2v6_grade.py").replace("from d2v5_hubness import", "from d2v6_hubness import")
old = '''d2v4 = res["law"]["competitor_d2v4"]
    REF'''
assert g.count(old) == 1
g = g.replace(old, '''d2v4 = res["law"]["competitor_d2v4"]; d2v5 = res["law"]["competitor_d2v5"]
    REF''')
g = g.replace('"competitor_d2v4": d2v4, "groups"', '"competitor_d2v4": d2v4, "competitor_d2v5": d2v5, "groups"')
g = g.replace('"rmse_d2v4": rmse(d2v4, law_rows(w))} for w in res["worlds"]}', '"rmse_d2v4": rmse(d2v4, law_rows(w)), "rmse_d2v5": rmse(d2v5, law_rows(w))} for w in res["worlds"]}')
g = g.replace('"rmse_d2v4": rmse(d2v4, rs) if rs else None}', '"rmse_d2v4": rmse(d2v4, rs) if rs else None, "rmse_d2v5": rmse(d2v5, rs) if rs else None}')
old = '''        el, en, ed, ev, e3, e4 = rmse(law, rs), rmse(comp, rs), rmse(d2, rs), rmse(d2v2, rs), rmse(d2v3, rs), rmse(d2v4, rs)
        per_group = {g: (out["groups"][g]["rmse_law"], out["groups"][g]["rmse_nominal"], out["groups"][g]["rmse_d2"], out["groups"][g]["rmse_d2v2"], out["groups"][g]["rmse_d2v3"], out["groups"][g]["rmse_d2v4"]) for g in ("unseen", "real", "scale") if out["groups"][g]["n"]}
        l5 = el <= 0.8 * en and el <= 0.8 * ed and el <= 0.9 * ev and el <= 0.95 * e3 and el <= 0.95 * e4 and all(a <= min(others) for a, *others in per_group.values())
        if min(en, ed, ev, e3, e4) < el:
            fail = True
    else:
        el = en = ed = ev = e3 = e4 = None; per_group = {}; l5 = None
    out["bars"]["L5_vs_competitors"] = {"rmse_law": el, "rmse_nominal": en, "rmse_d2": ed, "rmse_d2v2": ev, "rmse_d2v3": e3, "rmse_d2v4": e4, "per_group_law_nominal_d2_d2v2_d2v3_d2v4": per_group, "holds": l5}'''
assert g.count(old) == 1
g = g.replace(old, '''        el, en, ed, ev, e3, e4, e5 = rmse(law, rs), rmse(comp, rs), rmse(d2, rs), rmse(d2v2, rs), rmse(d2v3, rs), rmse(d2v4, rs), rmse(d2v5, rs)
        per_group = {g: (out["groups"][g]["rmse_law"], out["groups"][g]["rmse_nominal"], out["groups"][g]["rmse_d2"], out["groups"][g]["rmse_d2v2"], out["groups"][g]["rmse_d2v3"], out["groups"][g]["rmse_d2v4"], out["groups"][g]["rmse_d2v5"]) for g in ("unseen", "real", "scale") if out["groups"][g]["n"]}
        l5 = el <= 0.8 * en and el <= 0.8 * ed and el <= 0.9 * ev and el <= 0.95 * e3 and el <= 0.95 * e4 and el <= 0.95 * e5 and all(a <= min(others) for a, *others in per_group.values())
        if min(en, ed, ev, e3, e4, e5) < el:
            fail = True
    else:
        el = en = ed = ev = e3 = e4 = e5 = None; per_group = {}; l5 = None
    out["bars"]["L5_vs_competitors"] = {"rmse_law": el, "rmse_nominal": en, "rmse_d2": ed, "rmse_d2v2": ev, "rmse_d2v3": e3, "rmse_d2v4": e4, "rmse_d2v5": e5, "per_group_law_nominal_d2_d2v2_d2v3_d2v4_d2v5": per_group, "holds": l5}''')
wr("d2v6_grade.py", g)

# tolerance fixer
f = rd("d2v5_fix_tols.py").replace("D2V5", "D2V6").replace("from d2v5_hubness import", "from d2v6_hubness import")
old = '''d2v4 = res["law"]["competitor_d2v4"]; print("D2v4 frozen law: train rmse %.4f heldout rmse %.4f" % (res["law"]["d2v4_law_train_rmse"], res["law"]["d2v4_law_heldout_rmse"]))'''
assert f.count(old) == 1
f = f.replace(old, old + '''
d2v5 = res["law"]["competitor_d2v5"]; print("D2v5 frozen law: train rmse %.4f heldout rmse %.4f" % (res["law"]["d2v5_law_train_rmse"], res["law"]["d2v5_law_heldout_rmse"]))''')
f = f.replace('''d2v3 %.3f d2v4 %.3f | jac''', '''d2v3 %.3f d2v4 %.3f d2v5 %.3f | jac''')
f = f.replace('''rmse(d2v3, rs), rmse(d2v4, rs), p["hub_jaccard_same_alpha_mean"]''', '''rmse(d2v3, rs), rmse(d2v4, rs), rmse(d2v5, rs), p["hub_jaccard_same_alpha_mean"]''')
f = f.replace('''"pooled_d2v4_law": rmse(d2v4, all_rows), "FRAC_X"''', '''"pooled_d2v4_law": rmse(d2v4, all_rows), "pooled_d2v5_law": rmse(d2v5, all_rows), "FRAC_X"''')
wr("d2v6_fix_tols.py", f)

# configuration
c = json.load(open(os.path.join(SP, "d2v5_prereg_config.json"), encoding="utf-8"))
c["world"] = ("D2v5's world with heavy tails placed at the transfer dimensions in the discovery set: Student t with 3 and with 5 degrees at d = 256 join the training worlds, bracketing the unseen Student t with 4 degrees at d = 256 in tail weight; Laplace at d = 192 and at d = 256 join, bracketing an unseen Laplace at d = 224 in dimension. The neighbour-distance tail variables stay in the pool. Observers, k, budget cells, held-out worlds as before. Unseen families keep Student t with 2.5 degrees at d = 128, the log-normal at d = 192, the d = 512 clouds and the manifolds, and add Student t with 6 degrees at d = 192; real corpora on fresh slices (Wikipedia part 002 beyond the D2v5 windows, SIFT base beyond 4,000,000; the SIFT query file has 10,000 rows and its window overlaps earlier gates'); scale cells as D2v5 plus Student t with 4 degrees at d = 128 and N = 12000. The frozen D2, D2v2, D2v3, D2v4 and D2v5 laws are carried as competitors.")
c["seed_probe"] = 20261007; c["seed_pilot"] = 20261008; c["seed_run"] = 20261009
c["bars"] = "PREREG-D2V6.md Section 5; the law, its nominal-dimension competitor, and the frozen D2, D2v2, D2v3, D2v4 and D2v5 laws in law.json; REF the frozen law's error pooled over every pilot row; tolerances declared multiples of REF"
for w in c["worlds"]:
    w.pop("in_probe", None)
by = {w["name"]: w for w in c["worlds"]}
ins = c["worlds"].index(by["lap_d128"]) + 1
c["worlds"][ins:ins] = [{"name": "t3_d256", "group": "train", "family": "student", "d": 256, "N": 4000, "params": {"nu": 3.0}, "seed_offset": 107, "in_probe": True},
                        {"name": "t5_d256", "group": "train", "family": "student", "d": 256, "N": 4000, "params": {"nu": 5.0}, "seed_offset": 108},
                        {"name": "lap_d192", "group": "train", "family": "laplace", "d": 192, "N": 4000, "seed_offset": 109, "in_probe": True},
                        {"name": "lap_d256", "group": "train", "family": "laplace", "d": 256, "N": 4000, "seed_offset": 110}]
by["u_laplace_d192"].update({"name": "u_laplace_d224", "d": 224})
by["u_t4_d256"]["in_probe"] = True
ins = c["worlds"].index(by["u_lognormal_d192"]) + 1
c["worlds"][ins:ins] = [{"name": "u_t6_d192", "group": "unseen", "family": "student", "d": 192, "N": 4000, "params": {"nu": 6.0}, "seed_offset": 111}]
by["r_wiki1024"].update({"offset": 250000, "path": "/archive/tqp_real/wiki1024/part_002.npy"})
by["r_wiki1024_b"].update({"offset": 750000, "path": "/archive/tqp_real/wiki1024/part_002.npy"})
by["r_sift128"].update({"offset": 4000000})
by["r_siftq128"].update({"offset": 2000})
by["s_wiki1024_N12000"].update({"offset": 0, "path": "/archive/tqp_real/wiki1024/part_003.npy"})
by["s_sift128_N16000"].update({"offset": 5000000})
c["worlds"].append({"name": "s_t4_d128_N12000", "group": "scale", "family": "student", "d": 128, "N": 12000, "params": {"nu": 4.0}, "seed_offset": 112, "rotations": 2})
json.dump(c, open(os.path.join(SP, "d2v6_prereg_config.json"), "w", encoding="utf-8"), indent=1)
print("d2v6 files written; worlds", len(c["worlds"]), "probe worlds", [w["name"] for w in c["worlds"] if w.get("in_probe")])
