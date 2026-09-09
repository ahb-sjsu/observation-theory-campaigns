"""Builds the D2v5 files from the D2v4 ones: d2v5_hubness.py (tail variables measured on the
neighbour distances, the frozen D2v4 law as a fifth competitor), d2v5_grade.py, d2v5_fix_tols.py
and d2v5_prereg_config.json (heavy tails placed at the transfer dimensions, fresh real slices,
new seeds)."""
import json
import os

SP = r"C:\Users\abptl\AppData\Local\Temp\claude\C--source\f9dd774c-068a-466c-aa48-fbb6bdd82c75\scratchpad"


def rd(p):
    return open(os.path.join(SP, p), encoding="utf-8").read().replace("\r\n", "\n")


def wr(p, s):
    open(os.path.join(SP, p), "w", encoding="utf-8", newline="\n").write(s)


s = rd("d2v4_hubness.py")


def sub(a, b, count=1):
    global s
    assert s.count(a) == count, (s.count(a), a[:70])
    s = s.replace(a, b)


D2V4 = {"target": "skew", "features": ["cv_r_x_sqrt_d_eff", "log_d_nom_x_log_k", "log_id_twonn"], "coef": [-1.0937946857408793, 0.16852132160750913, -0.03188415704240788, 0.7013760762316192], "transform": "log1p"}

sub('"""D2v4: observer-relative hubness, the law with the discovery set widened to full-dimensional\nclouds at d = 256 and heavy tails (OD track, gate D2v4), built on the D2v3 workload.', '''"""D2v5: observer-relative hubness, the law with a tail variable measured on the neighbour
distances (OD track, gate D2v5), built on the D2v4 workload.

D2v4's law extrapolated to d = 512 and fitted the real corpora but missed heavier tails at higher
dimension than its discovery set held (Student t with 4 degrees at d = 256, Laplace at d = 192),
and the record named the reason: the feature family's only tail variable was the kurtosis of the
observed coordinates, which a rotation drives toward the Gaussian value (Laplace at d = 192 reads
0.04) and the search never chose. D2v5 measures the tail where the hubness mechanism lives, on
the distribution of neighbour distances in the observed space: the ratio of the 99th to the 50th
percentile of the k-th neighbour distance (tail_knn) and of the first (tail_r1), the excess
kurtosis of log r_k (kurt_lrk), and the Hill log-excess of r_k over its upper 5 percent (hill_rk);
each is scale-free, so the observer's rescaling is already inside it. The discovery set places
heavy tails at the transfer dimensions (Student t with 4 degrees at d = 192, Laplace at d = 128),
the unseen group keeps Student t with 4 degrees at d = 256 and Laplace at d = 192 one step beyond
them and adds Student t with 2.5 degrees at d = 128 and a log-normal at d = 192, and the frozen
D2, D2v2, D2v3 and D2v4 laws are carried as competitors.

D2v4 header follows.

(OD track, gate D2v4), built on the D2v3 workload.''')

# tail variables on the neighbour distances
sub('''    rk = knn_dist[:, k_law - 1]
    return {"cv_r": float(sd / m), "skew_r": float((z ** 3).mean()), "kurt_r": float((z ** 4).mean() - 3.0),
            "kurt_1d": float(np.mean(k1d)), "id_twonn": id_twonn,
            "cv_knn": float(rk.std() / rk.mean()), "rc": float(mean_pair_dist / rk.mean())}''',
    '''    rk = knn_dist[:, k_law - 1]
    out = {"cv_r": float(sd / m), "skew_r": float((z ** 3).mean()), "kurt_r": float((z ** 4).mean() - 3.0),
           "kurt_1d": float(np.mean(k1d)), "id_twonn": id_twonn,
           "cv_knn": float(rk.std() / rk.mean()), "rc": float(mean_pair_dist / rk.mean())}
    out.update(tail_variables(knn_dist, k_law))
    return out


def tail_variables(knn_dist: np.ndarray, k_law: int) -> dict:
    """Tail weight of the neighbour-distance distribution in the observed space, scale-free:
    the ratio of the 99th to the 50th percentile of the k-th neighbour distance and of the first,
    the excess kurtosis of log r_k, and the Hill log-excess of r_k over its upper 5 percent
    (the mean of log(r_(i) / r_(m)) over the m largest, the reciprocal of the Hill tail index)."""
    rk = np.maximum(knn_dist[:, k_law - 1], 1e-12); r1 = np.maximum(knn_dist[:, 0], 1e-12)
    q = np.quantile(rk, [0.5, 0.99]); q1 = np.quantile(r1, [0.5, 0.99])
    lr = np.log(rk); zl = (lr - lr.mean()) / (lr.std() + 1e-12)
    srt = np.sort(rk)[::-1]; m = max(20, int(0.05 * len(rk)))
    hill = float(np.mean(np.log(srt[:m] / srt[m]))) if len(rk) > m else float("nan")
    return {"tail_knn": float(q[1] / q[0]), "tail_r1": float(q1[1] / q1[0]), "kurt_lrk": float((zl ** 4).mean() - 3.0), "hill_rk": hill}''')

sub('''BASE = ["d_eff", "d_ent", "top_share", "cv_d", "cv_r", "kurt_r", "skew_r", "kurt_1d", "id_twonn", "cv_knn", "rc", "N", "k", "d_nom"]''',
    '''BASE = ["d_eff", "d_ent", "top_share", "cv_d", "cv_r", "kurt_r", "skew_r", "kurt_1d", "id_twonn", "cv_knn", "rc", "N", "k", "d_nom", "tail_knn", "tail_r1", "hill_rk", "kurt_lrk"]''')
sub('''    if _v not in ("kurt_r", "skew_r", "kurt_1d"):''', '''    if _v not in ("kurt_r", "skew_r", "kurt_1d", "kurt_lrk"):''')
sub('''    "log_d_nom_x_log_k": lambda v: np.log(v["d_nom"]) * np.log(v["k"]), "sqrt_d_nom_over_k": lambda v: np.sqrt(v["d_nom"]) / v["k"],
})''', '''    "log_d_nom_x_log_k": lambda v: np.log(v["d_nom"]) * np.log(v["k"]), "sqrt_d_nom_over_k": lambda v: np.sqrt(v["d_nom"]) / v["k"],
    "log_tail_knn_x_sqrt_d_eff": lambda v: np.log(_pos(v["tail_knn"])) * np.sqrt(v["d_eff"]), "log_tail_knn_x_log_id": lambda v: np.log(_pos(v["tail_knn"])) * np.log(_pos(v["id_twonn"])),
    "hill_rk_x_sqrt_d_eff": lambda v: v["hill_rk"] * np.sqrt(v["d_eff"]),
})''')
sub('''D2V3_FROZEN_LAW = {''', '''D2V4_FROZEN_LAW = {"target": "skew", "features": %s, "coef": %r, "transform": "log1p",
                   "note": "the law gate D2v4 froze with d = 256 clouds and heavy tails in the discovery set (observation-theory-campaigns/experiments/OD/D2v4/law.json), carried as a fixed competitor"}
D2V3_FROZEN_LAW = {''' % (json.dumps(D2V4["features"]), D2V4["coef"]))
sub('''"competitor_d2v3": D2V3_FROZEN_LAW, "target": target,''', '''"competitor_d2v3": D2V3_FROZEN_LAW, "competitor_d2v4": D2V4_FROZEN_LAW, "target": target,''')
sub('''                  "d2v3_law_heldout_rmse": rmse(D2V3_FROZEN_LAW, held), "d2v3_law_train_rmse": rmse(D2V3_FROZEN_LAW, train)}''',
    '''                  "d2v3_law_heldout_rmse": rmse(D2V3_FROZEN_LAW, held), "d2v3_law_train_rmse": rmse(D2V3_FROZEN_LAW, train),
                  "d2v4_law_heldout_rmse": rmse(D2V4_FROZEN_LAW, held), "d2v4_law_train_rmse": rmse(D2V4_FROZEN_LAW, train)}''')
sub('''"rmse_d2v3_law": rmse(frozen["competitor_d2v3"], rs), "n": len(rs)}''', '''"rmse_d2v3_law": rmse(frozen["competitor_d2v3"], rs), "rmse_d2v4_law": rmse(frozen["competitor_d2v4"], rs), "n": len(rs)}''')
# self-test: tail variables order ball < Gaussian < Student t, invariant to scale; the D2v4 law applies
sub('''    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails''', '''    # tail variables: a ball, a Gaussian and Student t with 3 degrees order by tail weight in every neighbour-distance
    # tail measure, and the measures do not change under a rescaling of the cloud (they read the observed space scale-free)
    tb, tg, tt = tail_variables(knn_search(b, 20)[1], 10), tail_variables(knn_search(g, 20)[1], 10), tail_variables(knn_search(t3, 20)[1], 10)
    ts = tail_variables(knn_search(3.7 * t3, 20)[1], 10)
    ok = all(tb[n] < tg[n] < tt[n] for n in ("tail_knn", "tail_r1", "hill_rk")) and tg["kurt_lrk"] < tt["kurt_lrk"] and all(abs(ts[n] - tt[n]) < 1e-6 * max(1.0, abs(tt[n])) for n in tt)
    print("tails: tail_knn ball %.3f gauss %.3f t3 %.3f | hill_rk %.3f %.3f %.3f | kurt_lrk %.2f %.2f %.2f | scale-free %s" % (tb["tail_knn"], tg["tail_knn"], tt["tail_knn"], tb["hill_rk"], tg["hill_rk"], tt["hill_rk"], tb["kurt_lrk"], tg["kurt_lrk"], tt["kurt_lrk"], all(abs(ts[n] - tt[n]) < 1e-6 * max(1.0, abs(tt[n])) for n in tt)), ok); fails += 0 if ok else 1
    # a Laplace cloud at d = 128 after a rotation: coordinate kurtosis near zero, neighbour-distance tail above the Gaussian's
    lp = gen_data("laplace", 128, 3000, rng, {}); g128 = rng.normal(size=(3000, 128)); Q, sc = make_observer(128, 0.0, rng)
    vl = spectral_variables(observe(lp, Q, sc), 128, 3000, rng); shl = shape_variables(observe(lp, Q, sc), knn_search(observe(lp, Q, sc), 20)[1], 10, vl["mean_pair_dist"])
    vg = spectral_variables(g128, 128, 3000, rng); shg = shape_variables(g128, knn_search(g128, 20)[1], 10, vg["mean_pair_dist"])
    ok = abs(shl["kurt_1d"]) < 0.5 and shl["tail_knn"] > shg["tail_knn"] and shl["hill_rk"] > shg["hill_rk"]
    print("laplace d=128 rotated: kurt_1d %.3f (gauss %.3f) tail_knn %.4f (gauss %.4f) hill_rk %.4f (gauss %.4f)" % (shl["kurt_1d"], shg["kurt_1d"], shl["tail_knn"], shg["tail_knn"], shl["hill_rk"], shg["hill_rk"]), ok); fails += 0 if ok else 1
    row = {"variables": {"cv_r": 0.12, "d_eff": 40.0, "d_nom": 64.0, "k": 10.0, "id_twonn": 20.0}, "targets": {"skew": 1.0}}
    pred = apply_law(D2V4_FROZEN_LAW, [row])[0]; c = D2V4_FROZEN_LAW["coef"]; exp = np.expm1(c[0] + c[1] * 0.12 * np.sqrt(40.0) + c[2] * np.log(64.0) * np.log(10.0) + c[3] * np.log(20.0))
    ok = abs(pred - exp) < 1e-9; print("D2v4 frozen law applies: %.3f" % pred, ok); fails += 0 if ok else 1
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails''')
sub("    python d2_hubness.py --selftest", "    python d2v5_hubness.py --selftest")
wr("d2v5_hubness.py", s)

# grader
g = rd("d2v4_grade.py")
g = g.replace("D2v4", "D2v5").replace("PREREG-D2V4", "PREREG-D2V5").replace("d2v2_grade.py", "d2v5_grade.py").replace("from d2v4_hubness import", "from d2v5_hubness import")
old = '''d2v3 = res["law"]["competitor_d2v3"]
    REF'''
assert g.count(old) == 1
g = g.replace(old, '''d2v3 = res["law"]["competitor_d2v3"]; d2v4 = res["law"]["competitor_d2v4"]
    REF''')
g = g.replace('"competitor_d2v3": d2v3, "groups"', '"competitor_d2v3": d2v3, "competitor_d2v4": d2v4, "groups"')
g = g.replace('"rmse_d2v3": rmse(d2v3, law_rows(w))} for w in res["worlds"]}', '"rmse_d2v3": rmse(d2v3, law_rows(w)), "rmse_d2v4": rmse(d2v4, law_rows(w))} for w in res["worlds"]}')
g = g.replace('"rmse_d2v3": rmse(d2v3, rs) if rs else None}', '"rmse_d2v3": rmse(d2v3, rs) if rs else None, "rmse_d2v4": rmse(d2v4, rs) if rs else None}')
old = '''        el, en, ed, ev, e3 = rmse(law, rs), rmse(comp, rs), rmse(d2, rs), rmse(d2v2, rs), rmse(d2v3, rs)
        per_group = {g: (out["groups"][g]["rmse_law"], out["groups"][g]["rmse_nominal"], out["groups"][g]["rmse_d2"], out["groups"][g]["rmse_d2v2"], out["groups"][g]["rmse_d2v3"]) for g in ("unseen", "real", "scale") if out["groups"][g]["n"]}
        l5 = el <= 0.8 * en and el <= 0.8 * ed and el <= 0.9 * ev and el <= 0.95 * e3 and all(a <= b and a <= c and a <= d and a <= e for a, b, c, d, e in per_group.values())
        if en < el or ed < el or ev < el or e3 < el:
            fail = True
    else:
        el = en = ed = ev = e3 = None; per_group = {}; l5 = None
    out["bars"]["L5_vs_competitors"] = {"rmse_law": el, "rmse_nominal": en, "rmse_d2": ed, "rmse_d2v2": ev, "rmse_d2v3": e3, "per_group_law_nominal_d2_d2v2_d2v3": per_group, "holds": l5}'''
assert g.count(old) == 1
g = g.replace(old, '''        el, en, ed, ev, e3, e4 = rmse(law, rs), rmse(comp, rs), rmse(d2, rs), rmse(d2v2, rs), rmse(d2v3, rs), rmse(d2v4, rs)
        per_group = {g: (out["groups"][g]["rmse_law"], out["groups"][g]["rmse_nominal"], out["groups"][g]["rmse_d2"], out["groups"][g]["rmse_d2v2"], out["groups"][g]["rmse_d2v3"], out["groups"][g]["rmse_d2v4"]) for g in ("unseen", "real", "scale") if out["groups"][g]["n"]}
        l5 = el <= 0.8 * en and el <= 0.8 * ed and el <= 0.9 * ev and el <= 0.95 * e3 and el <= 0.95 * e4 and all(a <= min(others) for a, *others in per_group.values())
        if min(en, ed, ev, e3, e4) < el:
            fail = True
    else:
        el = en = ed = ev = e3 = e4 = None; per_group = {}; l5 = None
    out["bars"]["L5_vs_competitors"] = {"rmse_law": el, "rmse_nominal": en, "rmse_d2": ed, "rmse_d2v2": ev, "rmse_d2v3": e3, "rmse_d2v4": e4, "per_group_law_nominal_d2_d2v2_d2v3_d2v4": per_group, "holds": l5}''')
wr("d2v5_grade.py", g)

# tolerance fixer
f = rd("d2v4_fix_tols.py").replace("D2V4", "D2V5").replace("from d2v4_hubness import", "from d2v5_hubness import")
old = '''d2v3 = res["law"]["competitor_d2v3"]; print("D2v3 frozen law: train rmse %.4f heldout rmse %.4f" % (res["law"]["d2v3_law_train_rmse"], res["law"]["d2v3_law_heldout_rmse"]))'''
assert f.count(old) == 1
f = f.replace(old, old + '''
d2v4 = res["law"]["competitor_d2v4"]; print("D2v4 frozen law: train rmse %.4f heldout rmse %.4f" % (res["law"]["d2v4_law_train_rmse"], res["law"]["d2v4_law_heldout_rmse"]))''')
f = f.replace('''rmse law %.3f nominal %.3f d2 %.3f d2v2 %.3f d2v3 %.3f | jac''', '''rmse law %.3f nominal %.3f d2 %.3f d2v2 %.3f d2v3 %.3f d2v4 %.3f | jac''')
f = f.replace('''rmse(d2v2, rs), rmse(d2v3, rs), p["hub_jaccard_same_alpha_mean"]''', '''rmse(d2v2, rs), rmse(d2v3, rs), rmse(d2v4, rs), p["hub_jaccard_same_alpha_mean"]''')
f = f.replace('''"pooled_d2v3_law": rmse(d2v3, all_rows), "FRAC_X"''', '''"pooled_d2v3_law": rmse(d2v3, all_rows), "pooled_d2v4_law": rmse(d2v4, all_rows), "FRAC_X"''')
old = '''print("pooled pilot RMSE of the frozen law over train + heldout rows (%d): %.4f (competitor %.4f)" % (len(all_rows), pooled, rmse(comp, all_rows)))'''
assert f.count(old) == 1
f = f.replace(old, old + '''
tail_rows = [r for w in res["worlds"] for r in w["rows"] if "budget_rel" not in r]
print("tail variable ranges: tail_knn %.3f..%.3f hill_rk %.4f..%.4f kurt_lrk %.2f..%.2f tail_r1 %.3f..%.3f" % (min(r["variables"]["tail_knn"] for r in tail_rows), max(r["variables"]["tail_knn"] for r in tail_rows), min(r["variables"]["hill_rk"] for r in tail_rows), max(r["variables"]["hill_rk"] for r in tail_rows), min(r["variables"]["kurt_lrk"] for r in tail_rows), max(r["variables"]["kurt_lrk"] for r in tail_rows), min(r["variables"]["tail_r1"] for r in tail_rows), max(r["variables"]["tail_r1"] for r in tail_rows)))''')
wr("d2v5_fix_tols.py", f)

# configuration
c = json.load(open(os.path.join(SP, "d2v4_prereg_config.json"), encoding="utf-8"))
c["world"] = ("D2v4's world with a tail variable measured on the neighbour distances in the feature pool (the 99th to 50th percentile ratio of the k-th and of the first neighbour distance, the excess kurtosis of log r_k, the Hill log-excess of r_k over its upper 5 percent) and heavy tails placed at the transfer dimensions in the discovery set (Student t with 4 degrees at d = 192 and Laplace at d = 128 join the training worlds). Observers, k, budget cells, held-out worlds as before. Unseen families keep Student t with 4 degrees at d = 256 and Laplace at d = 192, now one step beyond the training set, and add Student t with 2.5 degrees at d = 128 and a log-normal at d = 192; real corpora on fresh slices (Wikipedia part 002, SIFT base beyond 2,000,000; the SIFT query file has 10,000 rows and its window overlaps D2v2's by 3,000); scale cells add Laplace at d = 64 and N = 12000. The frozen D2, D2v2, D2v3 and D2v4 laws are carried as competitors.")
c["seed_probe"] = 20261004; c["seed_pilot"] = 20261005; c["seed_run"] = 20261006
c["bars"] = "PREREG-D2V5.md Section 5; the law, its nominal-dimension competitor, and the frozen D2, D2v2, D2v3 and D2v4 laws in law.json; REF the frozen law's error pooled over every pilot row; tolerances declared multiples of REF"
for w in c["worlds"]:
    w.pop("in_probe", None)
by = {w["name"]: w for w in c["worlds"]}
by["h_t3_d96"]["in_probe"] = True
ins = c["worlds"].index(by["lap_d64"]) + 1
c["worlds"][ins:ins] = [{"name": "t4_d192", "group": "train", "family": "student", "d": 192, "N": 4000, "params": {"nu": 4.0}, "seed_offset": 102, "in_probe": True},
                        {"name": "lap_d128", "group": "train", "family": "laplace", "d": 128, "N": 4000, "seed_offset": 103, "in_probe": True}]
ins = c["worlds"].index(by["u_laplace_d192"]) + 1
c["worlds"][ins:ins] = [{"name": "u_t25_d128", "group": "unseen", "family": "student", "d": 128, "N": 4000, "params": {"nu": 2.5}, "seed_offset": 104},
                        {"name": "u_lognormal_d192", "group": "unseen", "family": "lognormal", "d": 192, "N": 4000, "params": {"sigma": 0.5}, "seed_offset": 105}]
by["r_wiki1024"].update({"offset": 0, "path": "/archive/tqp_real/wiki1024/part_002.npy"})
by["r_wiki1024_b"].update({"offset": 500000, "path": "/archive/tqp_real/wiki1024/part_002.npy"})
by["r_sift128"].update({"offset": 2000000})
by["r_siftq128"].update({"offset": 0})
by["s_wiki1024_N12000"].update({"offset": 250000, "path": "/archive/tqp_real/wiki1024/part_003.npy"})
by["s_sift128_N16000"].update({"offset": 3000000})
c["worlds"].append({"name": "s_lap_d64_N12000", "group": "scale", "family": "laplace", "d": 64, "N": 12000, "seed_offset": 106, "rotations": 2})
json.dump(c, open(os.path.join(SP, "d2v5_prereg_config.json"), "w", encoding="utf-8"), indent=1)
print("d2v5 files written; worlds", len(c["worlds"]), "probe worlds", [w["name"] for w in c["worlds"] if w.get("in_probe")])
