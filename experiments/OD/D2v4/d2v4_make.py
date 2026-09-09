"""Builds d2v4_hubness.py from d2v3_hubness.py: the frozen D2v3 law as a fourth competitor. The
world changes (full-dimensional clouds at d = 256 and heavy-tailed clouds in the discovery set)
live in the configuration."""
import os

SP = r"C:\Users\abptl\AppData\Local\Temp\claude\C--source\f9dd774c-068a-466c-aa48-fbb6bdd82c75\scratchpad"
s = open(os.path.join(SP, "d2v3_hubness.py"), encoding="utf-8").read().replace("\r\n", "\n")


def sub(a, b, count=1):
    global s
    assert s.count(a) == count, (s.count(a), a[:60])
    s = s.replace(a, b)


sub('"""D2v3: observer-relative hubness, the law with manifold worlds in the discovery set', '''"""D2v4: observer-relative hubness, the law with the discovery set widened to full-dimensional
clouds at d = 256 and heavy tails (OD track, gate D2v4), built on the D2v3 workload.

D2v3's law, discovered with manifold worlds in the set, fitted every real corpus but missed the
per-world limit on a full-dimensional cube at d = 256, where the TwoNN estimator leaves the regime
the discovery set had shown it, and on heavy tails at N = 16000. D2v4 puts Gaussian and cube clouds
at d = 256 and Student t clouds with 3 degrees of freedom into the discovery families, keeps the
same feature family and search, and carries the frozen D2, D2v2 and D2v3 laws as competitors.

D2v3 header follows.
''')
sub('''D2V2_FROZEN_LAW = {''', '''D2V3_FROZEN_LAW = {"target": "skew", "features": ["inv_cv_knn", "log_id_twonn", "sqrt_d_eff"], "coef": [-1.462907521326016, -0.013182421393936017, 0.7474954718371633, 0.06855322431693047], "transform": "log1p",
                   "note": "the law gate D2v3 froze with manifold worlds in the discovery set (observation-theory-campaigns/experiments/OD/D2v3/law.json), carried as a fixed competitor"}
D2V2_FROZEN_LAW = {''')
sub('''        frozen = {"law": law, "competitor_nominal": comp, "competitor_d2": D2_FROZEN_LAW, "competitor_d2v2": D2V2_FROZEN_LAW, "target": target, "frozen_from": seed_role, "seed": seed, "n_train": len(train), "n_heldout": len(held),
                  "d2_law_heldout_rmse": rmse(D2_FROZEN_LAW, held), "d2_law_train_rmse": rmse(D2_FROZEN_LAW, train),
                  "d2v2_law_heldout_rmse": rmse(D2V2_FROZEN_LAW, held), "d2v2_law_train_rmse": rmse(D2V2_FROZEN_LAW, train)}''',
    '''        frozen = {"law": law, "competitor_nominal": comp, "competitor_d2": D2_FROZEN_LAW, "competitor_d2v2": D2V2_FROZEN_LAW, "competitor_d2v3": D2V3_FROZEN_LAW, "target": target, "frozen_from": seed_role, "seed": seed, "n_train": len(train), "n_heldout": len(held),
                  "d2_law_heldout_rmse": rmse(D2_FROZEN_LAW, held), "d2_law_train_rmse": rmse(D2_FROZEN_LAW, train),
                  "d2v2_law_heldout_rmse": rmse(D2V2_FROZEN_LAW, held), "d2v2_law_train_rmse": rmse(D2V2_FROZEN_LAW, train),
                  "d2v3_law_heldout_rmse": rmse(D2V3_FROZEN_LAW, held), "d2v3_law_train_rmse": rmse(D2V3_FROZEN_LAW, train)}''')
sub('''            result["evaluation"][w["name"]] = {"group": w["group"], "rmse_law": rmse(frozen["law"], rs), "rmse_competitor": rmse(frozen["competitor_nominal"], rs), "rmse_d2_law": rmse(frozen["competitor_d2"], rs), "rmse_d2v2_law": rmse(frozen["competitor_d2v2"], rs), "n": len(rs)}''',
    '''            result["evaluation"][w["name"]] = {"group": w["group"], "rmse_law": rmse(frozen["law"], rs), "rmse_competitor": rmse(frozen["competitor_nominal"], rs), "rmse_d2_law": rmse(frozen["competitor_d2"], rs), "rmse_d2v2_law": rmse(frozen["competitor_d2v2"], rs), "rmse_d2v3_law": rmse(frozen["competitor_d2v3"], rs), "n": len(rs)}''')
# self-test: the frozen D2v3 law applies with its published coefficients on a D2v3 row shape
sub('''    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails''', '''    row = {"variables": {"cv_knn": 0.167, "id_twonn": 11.8, "d_eff": 32.4}, "targets": {"skew": 0.24}}
    pred = apply_law(D2V3_FROZEN_LAW, [row])[0]; exp = np.expm1(-1.462907521326016 - 0.013182421393936017 / 0.167 + 0.7474954718371633 * np.log(11.8) + 0.06855322431693047 * np.sqrt(32.4))
    ok = abs(pred - exp) < 1e-9; print("D2v3 frozen law applies: %.3f (probe row measured 0.24)" % pred, ok); fails += 0 if ok else 1
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails''')
open(os.path.join(SP, "d2v4_hubness.py"), "w", encoding="utf-8", newline="\n").write(s)
print("d2v4_hubness.py written")
