"""Builds the D2v8 files from the D2v7 ones: d2v8_hubness.py (the frozen D2v7 excess law as a third
competitor), d2v8_grade.py, d2v8_fix_tols.py and d2v8_prereg_config.json (full-dimensional worlds at
d = 384 and 512 in the discovery set, bracketing unseen worlds; fresh real slices; new seeds)."""
import json
import os

SP = r"C:\Users\abptl\AppData\Local\Temp\claude\C--source\f9dd774c-068a-466c-aa48-fbb6bdd82c75\scratchpad"


def rd(p):
    return open(os.path.join(SP, p), encoding="utf-8").read().replace("\r\n", "\n")


def wr(p, s):
    open(os.path.join(SP, p), "w", encoding="utf-8", newline="\n").write(s)


s = rd("d2v7_hubness.py")


def sub(a, b, count=1):
    global s
    assert s.count(a) == count, (s.count(a), a[:70])
    s = s.replace(a, b)


D2V7 = json.load(open(os.path.join(SP, "d2v7_law.json"), encoding="utf-8"))["law"]
assert D2V7["features"] == ["inv_cv_knn", "log_d_eff", "sqrt_id_twonn"] and D2V7["target"] == "log_excess"

sub('"""D2v7: observer-relative hubness, the law with the Poisson hub excess as the target (OD track,\ngate D2v7), built on the D2v6 workload.', '''"""D2v8: observer-relative hubness, the excess law with full-dimensional worlds at d = 384 to 512
in the discovery set (OD track, gate D2v8), built on the D2v7 workload.

D2v7 changed the target to the log Poisson hub excess and held the heavy tails at d = 256, the
Gaussian at d = 512, the real corpora and the heavy tails at N = 16000 at once; it missed the cube
at d = 512 by a factor of 2.3, the one full-dimensional world beyond its training dimensions, and
its record named the coverage repair. D2v8 puts full-dimensional clouds at d = 384 and 512 into the
training worlds (the cube and an isotropic Gaussian at 384, the cube and a Gaussian with covariance
exponent 0.5 at 512), so that an unseen cube at d = 448 and an unseen ball at d = 384 are bracketed
in dimension, the isotropic Gaussian at d = 512 stays unseen, and a cube at d = 640 sits one step
beyond. Target, pool, search and errors are D2v7's; the frozen D2v7 law, which predicts the same
quantity, is carried as a third competitor beside the nominal-only law and the chance level.

D2v7 header follows.

(OD track, gate D2v7), built on the D2v6 workload.''')
sub('''UNITY_LAW = {"target": "log_excess",''', '''D2V7_FROZEN_LAW = {"target": "log_excess", "features": %s, "coef": %r, "transform": "identity",
                   "note": "the excess law gate D2v7 froze on D2v6's world (observation-theory-campaigns/experiments/OD/D2v7/law.json), carried as a fixed competitor"}
UNITY_LAW = {"target": "log_excess",''' % (json.dumps(D2V7["features"]), D2V7["coef"]))
sub('''        frozen = {"law": law, "competitor_nominal": comp, "competitor_unity": UNITY_LAW, "target": target, "frozen_from": seed_role, "seed": seed, "n_train": len(train), "n_heldout": len(held),
                  "unity_heldout_rmse": rmse(UNITY_LAW, held), "unity_train_rmse": rmse(UNITY_LAW, train)}''',
    '''        frozen = {"law": law, "competitor_nominal": comp, "competitor_unity": UNITY_LAW, "competitor_d2v7": D2V7_FROZEN_LAW, "target": target, "frozen_from": seed_role, "seed": seed, "n_train": len(train), "n_heldout": len(held),
                  "unity_heldout_rmse": rmse(UNITY_LAW, held), "unity_train_rmse": rmse(UNITY_LAW, train),
                  "d2v7_law_heldout_rmse": rmse(D2V7_FROZEN_LAW, held), "d2v7_law_train_rmse": rmse(D2V7_FROZEN_LAW, train)}''')
sub('''"rmse_unity": rmse(frozen["competitor_unity"], rs), "n": len(rs)}''', '''"rmse_unity": rmse(frozen["competitor_unity"], rs), "rmse_d2v7_law": rmse(frozen["competitor_d2v7"], rs), "n": len(rs)}''')
sub('''    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails''', '''    row = {"variables": {"cv_knn": 0.2, "d_eff": 40.0, "id_twonn": 20.0}, "targets": {"log_excess": 1.0}}
    pred = apply_law(D2V7_FROZEN_LAW, [row])[0]; c7 = D2V7_FROZEN_LAW["coef"]; exp = c7[0] + c7[1] / 0.2 + c7[2] * np.log(40.0) + c7[3] * np.sqrt(20.0)
    ok = abs(pred - exp) < 1e-9; print("D2v7 frozen law applies: log excess %.3f (excess %.2f)" % (pred, np.exp(pred)), ok); fails += 0 if ok else 1
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails''')
sub("    python d2v7_hubness.py --selftest", "    python d2v8_hubness.py --selftest")
wr("d2v8_hubness.py", s)

# grader
g = rd("d2v7_grade.py").replace("D2v7", "D2v8").replace("PREREG-D2V7", "PREREG-D2V8").replace("d2v7_grade.py", "d2v8_grade.py").replace("from d2v7_hubness import", "from d2v8_hubness import")
old = '''unity = res["law"]["competitor_unity"]
    REF'''
assert g.count(old) == 1
g = g.replace(old, '''unity = res["law"]["competitor_unity"]; d2v7 = res["law"]["competitor_d2v7"]
    REF''')
g = g.replace('"competitor_unity": unity, "groups"', '"competitor_unity": unity, "competitor_d2v7": d2v7, "groups"')
g = g.replace('"rmse_unity": rmse(unity, law_rows(w))} for w in res["worlds"]}', '"rmse_unity": rmse(unity, law_rows(w)), "rmse_d2v7": rmse(d2v7, law_rows(w))} for w in res["worlds"]}')
g = g.replace('"rmse_unity": rmse(unity, rs) if rs else None}', '"rmse_unity": rmse(unity, rs) if rs else None, "rmse_d2v7": rmse(d2v7, rs) if rs else None}')
old = '''        el, en, eu = rmse(law, rs), rmse(comp, rs), rmse(unity, rs)
        per_group = {g: (out["groups"][g]["rmse_law"], out["groups"][g]["rmse_nominal"], out["groups"][g]["rmse_unity"]) for g in ("unseen", "real", "scale") if out["groups"][g]["n"]}
        l5 = el <= 0.8 * en and el <= 0.8 * eu and all(a <= b and a <= c for a, b, c in per_group.values())
        if en < el or eu < el:
            fail = True
    else:
        el = en = eu = None; per_group = {}; l5 = None
    out["bars"]["L5_vs_competitors"] = {"rmse_law": el, "rmse_nominal": en, "rmse_unity": eu, "per_group_law_nominal_unity": per_group, "holds": l5}'''
assert g.count(old) == 1
g = g.replace(old, '''        el, en, eu, e7 = rmse(law, rs), rmse(comp, rs), rmse(unity, rs), rmse(d2v7, rs)
        per_group = {g: (out["groups"][g]["rmse_law"], out["groups"][g]["rmse_nominal"], out["groups"][g]["rmse_unity"], out["groups"][g]["rmse_d2v7"]) for g in ("unseen", "real", "scale") if out["groups"][g]["n"]}
        l5 = el <= 0.8 * en and el <= 0.8 * eu and el <= 0.95 * e7 and all(a <= min(others) for a, *others in per_group.values())
        if min(en, eu, e7) < el:
            fail = True
    else:
        el = en = eu = e7 = None; per_group = {}; l5 = None
    out["bars"]["L5_vs_competitors"] = {"rmse_law": el, "rmse_nominal": en, "rmse_unity": eu, "rmse_d2v7": e7, "per_group_law_nominal_unity_d2v7": per_group, "holds": l5}''')
wr("d2v8_grade.py", g)

# tolerance fixer
f = rd("d2v7_fix_tols.py").replace("D2V7", "D2V8").replace("from d2v7_hubness import", "from d2v8_hubness import")
old = '''print("unity: train rmse %.4f heldout rmse %.4f" % (res["law"]["unity_train_rmse"], res["law"]["unity_heldout_rmse"]))'''
assert f.count(old) == 1
f = f.replace(old, old + '''
d2v7 = res["law"]["competitor_d2v7"]; print("D2v7 frozen law: train rmse %.4f heldout rmse %.4f" % (res["law"]["d2v7_law_train_rmse"], res["law"]["d2v7_law_heldout_rmse"]))''')
f = f.replace('''rmse law %.3f nominal %.3f unity %.3f | jac''', '''rmse law %.3f nominal %.3f unity %.3f d2v7 %.3f | jac''')
f = f.replace('''rmse(law, rs), rmse(comp, rs), rmse(unity, rs), p["hub_jaccard_same_alpha_mean"]''', '''rmse(law, rs), rmse(comp, rs), rmse(unity, rs), rmse(d2v7, rs), p["hub_jaccard_same_alpha_mean"]''')
f = f.replace('''"pooled_unity": rmse(unity, all_rows), "FRAC_X"''', '''"pooled_unity": rmse(unity, all_rows), "pooled_d2v7_law": rmse(d2v7, all_rows), "FRAC_X"''')
wr("d2v8_fix_tols.py", f)

# configuration
c = json.load(open(os.path.join(SP, "d2v7_prereg_config.json"), encoding="utf-8"))
c["world"] = ("D2v7's world and target (the log Poisson hub excess) with full-dimensional clouds at d = 384 and 512 in the discovery set: the uniform cube and an isotropic Gaussian at d = 384, the cube and a Gaussian with covariance exponent 0.5 at d = 512 join the training worlds, bracketing an unseen cube at d = 448 and an unseen ball at d = 384 in dimension; the isotropic Gaussian at d = 512 stays unseen, and a cube at d = 640 sits one step beyond the set. Observers, k, budget cells, held-out worlds, heavy-tailed worlds, manifolds, real corpora (fresh slices: Wikipedia part 003 at 0 and 500,000, SIFT base at 8,000,000 and 9,000,000; the SIFT query file has 10,000 rows and its window overlaps earlier gates'; the scale Wikipedia cell on part 004 at 300,000) and scale cells as D2v7. Competitors: the nominal-only law on the same target, the chance level, and the frozen D2v7 law.")
c["seed_probe"] = 20261013; c["seed_pilot"] = 20261014; c["seed_run"] = 20261015
c["bars"] = "PREREG-D2V8.md Section 5; the law, its nominal-dimension competitor, the chance level and the frozen D2v7 law in law.json; REF the frozen law's RMS log-ratio error pooled over every pilot row; tolerances declared multiples of REF"
for w in c["worlds"]:
    w.pop("in_probe", None)
by = {w["name"]: w for w in c["worlds"]}
ins = c["worlds"].index(by["lap_d256"]) + 1
c["worlds"][ins:ins] = [{"name": "cube_d384", "group": "train", "family": "cube", "d": 384, "N": 4000, "seed_offset": 113, "in_probe": True},
                        {"name": "g_a0_d384", "group": "train", "family": "gauss", "d": 384, "N": 4000, "params": {"alpha_data": 0.0}, "seed_offset": 114},
                        {"name": "cube_d512", "group": "train", "family": "cube", "d": 512, "N": 4000, "seed_offset": 115},
                        {"name": "g_a05_d512", "group": "train", "family": "gauss", "d": 512, "N": 4000, "params": {"alpha_data": 0.5}, "seed_offset": 116, "in_probe": True}]
by["u_cube_d512"].update({"name": "u_cube_d448", "d": 448, "in_probe": True})
ins = c["worlds"].index(by["u_g_a0_d512"]) + 1
c["worlds"][ins:ins] = [{"name": "u_ball_d384", "group": "unseen", "family": "ball", "d": 384, "N": 4000, "seed_offset": 117},
                        {"name": "u_cube_d640", "group": "unseen", "family": "cube", "d": 640, "N": 4000, "seed_offset": 118}]
by["r_wiki1024"].update({"offset": 0, "path": "/archive/tqp_real/wiki1024/part_003.npy"})
by["r_wiki1024_b"].update({"offset": 500000, "path": "/archive/tqp_real/wiki1024/part_003.npy"})
by["r_sift128"].update({"offset": 8000000})
by["r_siftq128"].update({"offset": 6000})
by["s_wiki1024_N12000"].update({"offset": 300000, "path": "/archive/tqp_real/wiki1024/part_004.npy"})
by["s_sift128_N16000"].update({"offset": 9000000})
json.dump(c, open(os.path.join(SP, "d2v8_prereg_config.json"), "w", encoding="utf-8"), indent=1)
print("d2v8 files written; worlds", len(c["worlds"]), "probe", [w["name"] for w in c["worlds"] if w.get("in_probe")])
