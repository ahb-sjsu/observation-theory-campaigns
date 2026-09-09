"""Builds d2v2_hubness.py from d2_hubness.py: four more families, shape variables measured on the
observed cloud (centroid-distance spread, skewness and kurtosis, coordinate kurtosis, TwoNN
intrinsic dimension, neighbour-distance concentration and relative contrast), a wider feature
pool with up to three terms and an optional log1p target transform, and the frozen D2 law as a
second competitor."""
import os

SP = r"C:\Users\abptl\AppData\Local\Temp\claude\C--source\f9dd774c-068a-466c-aa48-fbb6bdd82c75\scratchpad"
s = open(os.path.join(SP, "d2_hubness.py"), encoding="utf-8").read().replace("\r\n", "\n")


def sub(a, b, count=1):
    global s
    assert s.count(a) == count, (s.count(a), a[:60])
    s = s.replace(a, b)


sub('"""D2: observer-relative hubness, the law (OD track, gate D2).', '''"""D2v2: observer-relative hubness, the law with a shape variable and multi-family discovery
(OD track, gate D2v2), built on the D2 workload.

D2 froze a law on Gaussian clouds in the spectral summaries of the observed covariance and the
concentration of pairwise distances, and it did not transfer: it over-predicted hubness on round
clouds (uniform balls, Wikipedia embeddings) and under-predicted it on heavy tails. D2v2 adds
variables that separate shape from spectrum, all measured on the observed cloud with no knowledge
of its family: the coefficient of variation, skewness and excess kurtosis of the distances to the
centroid; the mean excess kurtosis of the observed coordinates; the TwoNN intrinsic dimension
(Facco et al., as the program's corpus_geometry uses it); the coefficient of variation of the
k-th neighbour distance over points; and the relative contrast of neighbour to pairwise
distances. Discovery runs on seven families at once, and the frozen D2 law is carried as a
second competitor the new law must beat on the transfer groups.

Original D2 header follows.
''')

# families
sub('''    if family == "aniso_cube":
        sd = np.arange(1, d + 1, dtype=float) ** (-float(params.get("alpha_data", 1.0)) / 2.0)
        return rng.uniform(-1, 1, size=(N, d)) * sd
    raise ValueError(family)''', '''    if family == "aniso_cube":
        sd = np.arange(1, d + 1, dtype=float) ** (-float(params.get("alpha_data", 1.0)) / 2.0)
        return rng.uniform(-1, 1, size=(N, d)) * sd
    if family == "laplace":
        return rng.laplace(size=(N, d))
    if family == "lognormal":
        return np.exp(float(params.get("sigma", 0.5)) * rng.normal(size=(N, d)))
    if family == "shell":
        z = rng.normal(size=(N, d)); return z / np.linalg.norm(z, axis=1, keepdims=True)
    if family == "two_scale":
        m = int(params.get("centres", 4)); centres = rng.normal(size=(m, d)) * float(params.get("spread", 2.0))
        lab = rng.integers(0, m, size=N); scale = np.where(lab % 2 == 0, 1.0, float(params.get("ratio", 3.0)))[:, None]
        return centres[lab] + rng.normal(size=(N, d)) * scale
    raise ValueError(family)''')

# neighbour distances alongside indices
sub('''def knn_indices(y: np.ndarray, k: int, block: int = 1024) -> np.ndarray:
    """Indices of the k nearest neighbours of every row (self excluded), by blocked exact search."""
    N = len(y); y32 = y.astype(np.float32); sq = (y32 * y32).sum(1)
    out = np.empty((N, k), dtype=np.int64)
    for i0 in range(0, N, block):
        i1 = min(N, i0 + block)
        d2 = sq[i0:i1, None] + sq[None, :] - 2.0 * (y32[i0:i1] @ y32.T)
        d2[np.arange(i1 - i0), np.arange(i0, i1)] = np.inf
        part = np.argpartition(d2, k, axis=1)[:, :k]
        dd = np.take_along_axis(d2, part, axis=1)
        order = np.argsort(dd, axis=1)
        out[i0:i1] = np.take_along_axis(part, order, axis=1)
    return out''', '''def knn_search(y: np.ndarray, k: int, block: int = 1024) -> tuple[np.ndarray, np.ndarray]:
    """Indices and distances of the k nearest neighbours of every row (self excluded), by blocked
    exact search."""
    N = len(y); y32 = y.astype(np.float32); sq = (y32 * y32).sum(1)
    out = np.empty((N, k), dtype=np.int64); dist = np.empty((N, k), dtype=np.float64)
    for i0 in range(0, N, block):
        i1 = min(N, i0 + block)
        d2 = sq[i0:i1, None] + sq[None, :] - 2.0 * (y32[i0:i1] @ y32.T)
        d2[np.arange(i1 - i0), np.arange(i0, i1)] = np.inf
        part = np.argpartition(d2, k, axis=1)[:, :k]
        dd = np.take_along_axis(d2, part, axis=1)
        order = np.argsort(dd, axis=1)
        out[i0:i1] = np.take_along_axis(part, order, axis=1)
        dist[i0:i1] = np.sqrt(np.maximum(np.take_along_axis(dd, order, axis=1), 0.0))
    return out, dist


def knn_indices(y: np.ndarray, k: int, block: int = 1024) -> np.ndarray:
    return knn_search(y, k, block)[0]


def shape_variables(y: np.ndarray, knn_dist: np.ndarray, k_law: int, mean_pair_dist: float) -> dict:
    """Shape of the observed cloud, family-blind: distances to the centroid (coefficient of
    variation, skewness, excess kurtosis), mean excess kurtosis of the observed coordinates,
    TwoNN intrinsic dimension (Facco et al. 2017, trimmed at the 90th percentile as in the
    program's corpus_geometry), concentration of the k-th neighbour distance, relative contrast."""
    r = np.linalg.norm(y - y.mean(0), axis=1); m = r.mean(); sd = r.std()
    z = (r - m) / (sd + 1e-12)
    yc = y - y.mean(0); v = yc.var(0) + 1e-12; k1d = ((yc ** 4).mean(0) / v ** 2 - 3.0)
    r1, r2 = knn_dist[:, 0], knn_dist[:, 1]
    mu = r2[r1 > 0] / np.maximum(r1[r1 > 0], 1e-12); mu = mu[mu > 1.0]
    if len(mu) >= 100:
        mu = mu[mu <= np.quantile(mu, 0.9)]; id_twonn = float(len(mu) / np.sum(np.log(mu)))
    else:
        id_twonn = float("nan")
    rk = knn_dist[:, k_law - 1]
    return {"cv_r": float(sd / m), "skew_r": float((z ** 3).mean()), "kurt_r": float((z ** 4).mean() - 3.0),
            "kurt_1d": float(np.mean(k1d)), "id_twonn": id_twonn,
            "cv_knn": float(rk.std() / rk.mean()), "rc": float(mean_pair_dist / rk.mean())}''')

# spectral_variables: return the mean pairwise distance too
sub('''            "cv_d": float(dist.std() / dist.mean()), "median_nn_dist": float(np.median(np.sort(D + np.eye(m) * 1e30, axis=1)[:, 0]))}''',
    '''            "cv_d": float(dist.std() / dist.mean()), "mean_pair_dist": float(dist.mean()), "median_nn_dist": float(np.median(np.sort(D + np.eye(m) * 1e30, axis=1)[:, 0]))}''')

# feature pool
start = s.index("FEATURES = {"); end = s.index("NOMINAL_ONLY = {")
s = s[:start] + '''def _pos(x):
    return np.maximum(x, 1e-9)


BASE = ["d_eff", "d_ent", "top_share", "cv_d", "cv_r", "kurt_r", "skew_r", "kurt_1d", "id_twonn", "cv_knn", "rc", "N", "k", "d_nom"]
FEATURES = {}
for _v in BASE:
    FEATURES[_v] = (lambda name: (lambda v: v[name]))(_v)
    if _v not in ("kurt_r", "skew_r", "kurt_1d"):
        FEATURES["log_" + _v] = (lambda name: (lambda v: np.log(_pos(v[name]))))(_v)
        FEATURES["sqrt_" + _v] = (lambda name: (lambda v: np.sqrt(_pos(v[name]))))(_v)
        FEATURES["inv_" + _v] = (lambda name: (lambda v: 1.0 / _pos(v[name])))(_v)
    else:
        FEATURES["log3_" + _v] = (lambda name: (lambda v: np.log(_pos(v[name] + 3.0))))(_v)
FEATURES.update({
    "log_kN": lambda v: np.log(v["k"] / v["N"]),
    "sqrt_d_eff_over_k": lambda v: np.sqrt(v["d_eff"]) / v["k"], "sqrt_id_over_k": lambda v: np.sqrt(_pos(v["id_twonn"])) / v["k"],
    "log_d_eff_x_log_k": lambda v: np.log(v["d_eff"]) * np.log(v["k"]), "log_id_x_log_k": lambda v: np.log(_pos(v["id_twonn"])) * np.log(v["k"]),
    "cv_r_x_sqrt_d_eff": lambda v: v["cv_r"] * np.sqrt(v["d_eff"]), "inv_cv_d_over_k": lambda v: 1.0 / (_pos(v["cv_d"]) * v["k"]),
    "kurt_r_over_k": lambda v: v["kurt_r"] / v["k"], "rc_over_k": lambda v: v["rc"] / v["k"], "cv_knn_x_sqrt_d_eff": lambda v: v["cv_knn"] * np.sqrt(v["d_eff"]),
    "log_d_nom_x_log_k": lambda v: np.log(v["d_nom"]) * np.log(v["k"]), "sqrt_d_nom_over_k": lambda v: np.sqrt(v["d_nom"]) / v["k"],
})
''' + s[end:]
sub('''NOMINAL_ONLY = {"log_d_nom", "d_nom", "sqrt_d_nom", "log_N", "log_k", "k", "inv_k", "sqrt_k", "log_kN", "log_d_nom_x_log_k", "log_d_nom_over_log_N"}''',
    '''NOMINAL_ONLY = {"log_d_nom", "d_nom", "sqrt_d_nom", "inv_d_nom", "log_N", "N", "sqrt_N", "inv_N", "log_k", "k", "inv_k", "sqrt_k", "log_kN", "log_d_nom_x_log_k", "sqrt_d_nom_over_k"}
D2_FROZEN_LAW = {"target": "skew", "features": ["inv_cv_d", "sqrt_d_eff_over_k"], "coef": [-0.026165647256707177, 0.4206954447231824, 0.8172228220333909], "transform": "identity",
                 "note": "the law gate D2 froze on Gaussian clouds (observation-theory-campaigns/experiments/OD/D2/law.json), carried as a fixed competitor"}''')

# target transform in fit / apply / rmse / discover
sub('''def fit_law(rows: list[dict], names: list[str], target: str) -> tuple[np.ndarray, float]:
    X = np.column_stack([np.ones(len(rows)), feature_matrix(rows, names)]); yv = np.array([r["targets"][target] for r in rows])
    coef, *_ = np.linalg.lstsq(X, yv, rcond=None)
    return coef, float(np.sqrt(np.mean((X @ coef - yv) ** 2)))''', '''def fwd(y, transform):
    return np.log1p(np.maximum(y, -0.99)) if transform == "log1p" else y


def back(y, transform):
    return np.expm1(y) if transform == "log1p" else y


def fit_law(rows: list[dict], names: list[str], target: str, transform: str = "identity") -> tuple[np.ndarray, float]:
    X = np.column_stack([np.ones(len(rows)), feature_matrix(rows, names)]); yv = np.array([r["targets"][target] for r in rows])
    coef, *_ = np.linalg.lstsq(X, fwd(yv, transform), rcond=None)
    return coef, float(np.sqrt(np.mean((back(X @ coef, transform) - yv) ** 2)))''')
sub('''def apply_law(law: dict, rows: list[dict]) -> np.ndarray:
    X = np.column_stack([np.ones(len(rows)), feature_matrix(rows, law["features"])])
    return X @ np.array(law["coef"])''', '''def apply_law(law: dict, rows: list[dict]) -> np.ndarray:
    X = np.column_stack([np.ones(len(rows)), feature_matrix(rows, law["features"])])
    return back(X @ np.array(law["coef"]), law.get("transform", "identity"))''')
sub('''def discover(train: list[dict], heldout: list[dict], target: str, max_terms: int = 2, pool: set | None = None) -> dict:
    """Every model with up to max_terms features from the pool, fitted on train, ranked by held-out RMSE."""
    names = sorted(pool if pool is not None else FEATURES.keys())
    best = None
    for m in range(0, max_terms + 1):
        for combo in itertools.combinations(names, m):
            coef, tr_rmse = fit_law(train, list(combo), target)
            law = {"target": target, "features": list(combo), "coef": [float(c) for c in coef]}
            ho = rmse(law, heldout)
            if not np.isfinite(ho):
                continue
            if best is None or ho < best["heldout_rmse"] - 1e-12:
                best = {**law, "train_rmse": tr_rmse, "heldout_rmse": ho, "n_terms": m}
    return best''', '''def discover(train: list[dict], heldout: list[dict], target: str, max_terms: int = 2, pool: set | None = None, transforms=("identity", "log1p")) -> dict:
    """Every model with up to max_terms features from the pool under each target transform, fitted
    on train, ranked by held-out RMSE on the untransformed target."""
    names = sorted(pool if pool is not None else FEATURES.keys())
    Xtr_all = {n: np.array([FEATURES[n](r["variables"]) for r in train]) for n in names}
    Xho_all = {n: np.array([FEATURES[n](r["variables"]) for r in heldout]) for n in names}
    ytr = np.array([r["targets"][target] for r in train]); yho = np.array([r["targets"][target] for r in heldout])
    ok = [n for n in names if np.all(np.isfinite(Xtr_all[n])) and np.all(np.isfinite(Xho_all[n]))]
    best = None
    for transform in transforms:
        ytr_t = fwd(ytr, transform)
        for m in range(0, max_terms + 1):
            for combo in itertools.combinations(ok, m):
                X = np.column_stack([np.ones(len(train))] + [Xtr_all[n] for n in combo])
                coef, *_ = np.linalg.lstsq(X, ytr_t, rcond=None)
                Xh = np.column_stack([np.ones(len(heldout))] + [Xho_all[n] for n in combo])
                ho = float(np.sqrt(np.mean((back(Xh @ coef, transform) - yho) ** 2)))
                if not np.isfinite(ho):
                    continue
                if best is None or ho < best["heldout_rmse"] - 1e-12:
                    tr = float(np.sqrt(np.mean((back(X @ coef, transform) - ytr) ** 2)))
                    best = {"target": target, "features": list(combo), "coef": [float(c) for c in coef], "transform": transform, "train_rmse": tr, "heldout_rmse": ho, "n_terms": m}
    return best''')

# run_world: shape variables from the neighbour search
sub('''        var = spectral_variables(y, d, N, rng)
        idx = knn_indices(y, kmax)''', '''        var = spectral_variables(y, d, N, rng)
        idx, kdist = knn_search(y, kmax)
        var.update(shape_variables(y, kdist, int(cfg["k_law"]), var["mean_pair_dist"]))''')
# competitors in run()
sub('''        law = discover(train, held, target, int(cfg["law_max_terms"]))
        comp = discover(train, held, target, int(cfg["law_max_terms"]), NOMINAL_ONLY)
        frozen = {"law": law, "competitor_nominal": comp, "target": target, "frozen_from": seed_role, "seed": seed, "n_train": len(train), "n_heldout": len(held)}''',
    '''        law = discover(train, held, target, int(cfg["law_max_terms"]))
        comp = discover(train, held, target, int(cfg["law_max_terms"]), NOMINAL_ONLY)
        frozen = {"law": law, "competitor_nominal": comp, "competitor_d2": D2_FROZEN_LAW, "target": target, "frozen_from": seed_role, "seed": seed, "n_train": len(train), "n_heldout": len(held),
                  "d2_law_heldout_rmse": rmse(D2_FROZEN_LAW, held), "d2_law_train_rmse": rmse(D2_FROZEN_LAW, train)}''')
sub('''            result["evaluation"][w["name"]] = {"group": w["group"], "rmse_law": rmse(frozen["law"], rs), "rmse_competitor": rmse(frozen["competitor_nominal"], rs), "n": len(rs)}''',
    '''            result["evaluation"][w["name"]] = {"group": w["group"], "rmse_law": rmse(frozen["law"], rs), "rmse_competitor": rmse(frozen["competitor_nominal"], rs), "rmse_d2_law": rmse(frozen["competitor_d2"], rs), "n": len(rs)}''')
# self test additions
sub('''    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails''', '''    # shape variables: a Gaussian and a uniform ball at d = 32 differ in cv_r and kurt_1d as expected
    g = rng.normal(size=(3000, 32)); b = gen_data("ball", 32, 3000, rng, {}); t3 = gen_data("student", 32, 3000, rng, {"nu": 3.0})
    def shp(x):
        v = spectral_variables(x, 32, 3000, rng); i, dd = knn_search(x, 20); return shape_variables(x, dd, 10, v["mean_pair_dist"])
    sg, sb, st = shp(g), shp(b), shp(t3)
    ok = sb["cv_r"] < sg["cv_r"] < st["cv_r"] and sb["kurt_1d"] < sg["kurt_1d"] < st["kurt_1d"] and 20 < sg["id_twonn"] < 40
    print("shape: cv_r ball %.3f gauss %.3f t3 %.3f | kurt_1d %.2f %.2f %.2f | id_twonn gauss %.1f" % (sb["cv_r"], sg["cv_r"], st["cv_r"], sb["kurt_1d"], sg["kurt_1d"], st["kurt_1d"], sg["id_twonn"]), ok); fails += 0 if ok else 1
    # the frozen D2 law reproduces D2's held-out error on a D2 row shape
    row = {"variables": {"d_eff": 9.8, "cv_d": 0.216, "k": 10.0}, "targets": {"skew": 2.70}}
    pred = apply_law(D2_FROZEN_LAW, [row])[0]; ok = abs(pred - (-0.0262 + 0.4207 / 0.216 + 0.8172 * np.sqrt(9.8) / 10)) < 1e-3
    print("D2 frozen law applies: %.3f" % pred, ok); fails += 0 if ok else 1
    # log1p transform round trip in discovery
    rows2 = [{"variables": {**{k: 1.0 for k in BASE}, "d_eff": float(de), "k": 10.0, "N": 1000.0}, "targets": {"skew": np.expm1(0.2 + 0.5 * np.log(de))}} for de in (2, 4, 8, 16, 32, 64)]
    law2 = discover(rows2, rows2, "skew", 1, {"log_d_eff", "d_eff"}); ok = law2["transform"] == "log1p" and law2["features"] == ["log_d_eff"] and abs(law2["coef"][1] - 0.5) < 1e-6
    print("planted log1p law recovered:", ok, law2["transform"], law2["features"]); fails += 0 if ok else 1
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails''')
open(os.path.join(SP, "d2v2_hubness.py"), "w", encoding="utf-8", newline="\n").write(s)
print("d2v2_hubness.py written")
