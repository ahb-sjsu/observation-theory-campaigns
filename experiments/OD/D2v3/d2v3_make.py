"""Builds d2v3_hubness.py from d2v2_hubness.py: manifold families whose intrinsic dimension sits far
below the ambient one (a linear subspace with noise, a random smooth nonlinear embedding of a
low-dimensional Gaussian, a product of circles, a swiss-roll sheet), so that the intrinsic
dimension becomes informative in the discovery set; the frozen D2v2 law carried as a third
competitor."""
import os

SP = r"C:\Users\abptl\AppData\Local\Temp\claude\C--source\f9dd774c-068a-466c-aa48-fbb6bdd82c75\scratchpad"
s = open(os.path.join(SP, "d2v2_hubness.py"), encoding="utf-8").read().replace("\r\n", "\n")


def sub(a, b, count=1):
    global s
    assert s.count(a) == count, (s.count(a), a[:60])
    s = s.replace(a, b)


sub('"""D2v2: observer-relative hubness, the law with a shape variable and multi-family discovery', '''"""D2v3: observer-relative hubness, the law with manifold worlds in the discovery set
(OD track, gate D2v3), built on the D2v2 workload.

D2v2's law transferred to every unseen full-dimensional family and to SIFT but not to Wikipedia
embeddings, whose TwoNN intrinsic dimension (8 to 20) sits far below their spectral dimension (up
to 320); the intrinsic dimension was in the pool and the search dropped it, because on
full-dimensional discovery families it duplicates the spectral dimension. D2v3 puts clouds on
embedded manifolds into the discovery families: an m-dimensional Gaussian in an m-dimensional
random subspace of R^d with small isotropic noise; a random smooth nonlinear embedding of an
m-dimensional Gaussian (random Fourier features) with noise; a product of m/2 circles; and a
two-dimensional swiss-roll sheet; at intrinsic dimension m on 4, 8, 16 and ambient d on 64, 128.
The frozen D2v2 law is carried as a third competitor.

D2v2 header follows.
''')

sub('''    if family == "two_scale":''', '''    if family == "subspace":
        m = int(params["m"]); noise = float(params.get("noise", 0.05))
        Q, _ = np.linalg.qr(rng.normal(size=(d, m)))
        return rng.normal(size=(N, m)) @ Q.T + noise * rng.normal(size=(N, d))
    if family == "fourier":
        m = int(params["m"]); noise = float(params.get("noise", 0.05)); n_feat = int(params.get("features", 3 * d))
        z = rng.normal(size=(N, m)); W = rng.normal(size=(m, n_feat)) * float(params.get("bandwidth", 1.0)); b = rng.uniform(0, 2 * np.pi, size=n_feat)
        phi = np.cos(z @ W + b)
        A = rng.normal(size=(n_feat, d)) / np.sqrt(n_feat)
        x = phi @ A
        return x / x.std() + noise * rng.normal(size=(N, d))
    if family == "torus":
        m = int(params["m"]); noise = float(params.get("noise", 0.05)); k2 = m // 2
        th = rng.uniform(0, 2 * np.pi, size=(N, k2)); pts = np.concatenate([np.cos(th), np.sin(th)], axis=1)
        Q, _ = np.linalg.qr(rng.normal(size=(d, 2 * k2)))
        return pts @ Q.T + noise * rng.normal(size=(N, d))
    if family == "swissroll":
        noise = float(params.get("noise", 0.05)); t = 1.5 * np.pi * (1 + 2 * rng.uniform(size=N)); h = 10 * rng.uniform(size=N)
        pts = np.stack([t * np.cos(t), h, t * np.sin(t)], axis=1); pts = (pts - pts.mean(0)) / pts.std()
        Q, _ = np.linalg.qr(rng.normal(size=(d, 3)))
        return pts @ Q.T + noise * rng.normal(size=(N, d))
    if family == "two_scale":''')

sub('''D2_FROZEN_LAW = {"target": "skew", "features": ["inv_cv_d", "sqrt_d_eff_over_k"], "coef": [-0.026165647256707177, 0.4206954447231824, 0.8172228220333909], "transform": "identity",
                 "note": "the law gate D2 froze on Gaussian clouds (observation-theory-campaigns/experiments/OD/D2/law.json), carried as a fixed competitor"}''',
    '''D2_FROZEN_LAW = {"target": "skew", "features": ["inv_cv_d", "sqrt_d_eff_over_k"], "coef": [-0.026165647256707177, 0.4206954447231824, 0.8172228220333909], "transform": "identity",
                 "note": "the law gate D2 froze on Gaussian clouds (observation-theory-campaigns/experiments/OD/D2/law.json), carried as a fixed competitor"}
D2V2_FROZEN_LAW = {"target": "skew", "features": ["d_ent", "inv_cv_d", "sqrt_top_share"], "coef": [2.8109594094123243, 0.004706131843131253, -0.09277311281123588, -2.461264557894105], "transform": "log1p",
                   "note": "the law gate D2v2 froze on seven full-dimensional families (observation-theory-campaigns/experiments/OD/D2v2/law.json), carried as a fixed competitor"}''')
sub('''        frozen = {"law": law, "competitor_nominal": comp, "competitor_d2": D2_FROZEN_LAW, "target": target, "frozen_from": seed_role, "seed": seed, "n_train": len(train), "n_heldout": len(held),
                  "d2_law_heldout_rmse": rmse(D2_FROZEN_LAW, held), "d2_law_train_rmse": rmse(D2_FROZEN_LAW, train)}''',
    '''        frozen = {"law": law, "competitor_nominal": comp, "competitor_d2": D2_FROZEN_LAW, "competitor_d2v2": D2V2_FROZEN_LAW, "target": target, "frozen_from": seed_role, "seed": seed, "n_train": len(train), "n_heldout": len(held),
                  "d2_law_heldout_rmse": rmse(D2_FROZEN_LAW, held), "d2_law_train_rmse": rmse(D2_FROZEN_LAW, train),
                  "d2v2_law_heldout_rmse": rmse(D2V2_FROZEN_LAW, held), "d2v2_law_train_rmse": rmse(D2V2_FROZEN_LAW, train)}''')
sub('''            result["evaluation"][w["name"]] = {"group": w["group"], "rmse_law": rmse(frozen["law"], rs), "rmse_competitor": rmse(frozen["competitor_nominal"], rs), "rmse_d2_law": rmse(frozen["competitor_d2"], rs), "n": len(rs)}''',
    '''            result["evaluation"][w["name"]] = {"group": w["group"], "rmse_law": rmse(frozen["law"], rs), "rmse_competitor": rmse(frozen["competitor_nominal"], rs), "rmse_d2_law": rmse(frozen["competitor_d2"], rs), "rmse_d2v2_law": rmse(frozen["competitor_d2v2"], rs), "n": len(rs)}''')
# self test: manifold families have intrinsic dimension far below the ambient one
sub('''    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails''', '''    # manifold families: TwoNN dimension near m and far below d, while the spectral dimension is not
    for fam, prm in (("subspace", {"m": 8}), ("fourier", {"m": 8}), ("torus", {"m": 8}), ("swissroll", {})):
        x = gen_data(fam, 64, 3000, rng, prm); v = spectral_variables(x, 64, 3000, rng); i, dd = knn_search(x, 20); sh = shape_variables(x, dd, 10, v["mean_pair_dist"])
        target = prm.get("m", 2); ok = sh["id_twonn"] < 0.5 * 64 and abs(sh["id_twonn"] - target) < max(3.0, 0.6 * target)
        print("%-9s id_twonn %5.1f (m = %d) d_eff %5.1f d_ent %5.1f" % (fam, sh["id_twonn"], target, v["d_eff"], v["d_ent"]), ok); fails += 0 if ok else 1
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails''')
open(os.path.join(SP, "d2v3_hubness.py"), "w", encoding="utf-8", newline="\n").write(s)
print("d2v3_hubness.py written")
