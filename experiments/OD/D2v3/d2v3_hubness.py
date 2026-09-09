"""D2v3: observer-relative hubness, the law with manifold worlds in the discovery set
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


Hub Relativity (Bond 2026, draft) reads hubness through an observer O = (C, G, B): a point's
k-occurrence H_k(x | O) is the number of other points whose k nearest neighbours, measured in the
observer's distance, include x. Here the observer is a linear map with a declared spectrum
applied after a random rotation, C = diag(i^-alpha) R, with G = I and the budget B a
quantization of the observed coordinates. The observed cloud has covariance
Sigma_obs = C Sigma_data C^T, and the candidate law says the hubness of a cloud under an
observer depends on the observer only through spectral summaries of Sigma_obs (an effective
dimension first) together with N and k.

Hubness statistics follow the program's instrument (openvector-bench, hubness.py): the
k-occurrence counts, their skewness (Radovanovic et al. 2010), the busiest point's count over the
Poisson ceiling (each point queries once with k slots, so the null mean is k), the share of slots
held by the busiest one percent, and the anti-hub fraction. Polarity: hub when the standardised
count is at least 2, anti-hub when the count is 0 (thresholds fixed here, before validation).

Modes. `--seed-role pilot` runs the training and held-out worlds and, with `--discover`, searches
the declared expression family for the law and its nominal-dimension competitor and freezes them
to `law.json`. `--seed-role run` evaluates the frozen law on fresh seeds, the unseen families, the
real corpora and the scale cells; it never refits.

    python d2_hubness.py --selftest
    python d2_hubness.py --config prereg_config.json --seed-role pilot --out pilot.json --discover law.json
    python d2_hubness.py --config prereg_config.json --seed-role run --out results.json --law law.json
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
import time

import numpy as np

# ----------------------------------------------------------------------------- hubness instrument (openvector-bench)


def _poisson_sf(lam: float, x: int) -> float:
    if x <= 0:
        return 1.0
    s = 0.0
    for i in range(x):
        s += math.exp(-lam + i * math.log(lam + 1e-300) - math.lgamma(i + 1))
    return max(0.0, 1.0 - s)


def poisson_null_max(lam: float, n_base: int, cap: int = 100_000) -> int:
    if lam <= 0 or n_base <= 0:
        return 0
    c = 1
    while c < cap and n_base * _poisson_sf(lam, c) >= 1.0:
        c += 1
    return c - 1


def tail_share(counts: np.ndarray, frac: float = 0.01) -> float:
    c = np.sort(np.asarray(counts, dtype=np.float64))[::-1]
    m = max(1, int(round(len(c) * frac)))
    total = c.sum()
    return float(c[:m].sum() / total) if total > 0 else 0.0


def skewness(v: np.ndarray) -> float:
    v = np.asarray(v, dtype=np.float64); m = v.mean(); s = v.std()
    return float(((v - m) ** 3).mean() / s ** 3) if s > 0 else 0.0


# ----------------------------------------------------------------------------- data


def gen_data(family: str, d: int, N: int, rng: np.random.Generator, params: dict) -> np.ndarray:
    if family == "gauss":
        sd = np.arange(1, d + 1, dtype=float) ** (-float(params.get("alpha_data", 0.0)) / 2.0)
        return rng.normal(size=(N, d)) * sd
    if family == "cube":
        return rng.uniform(-1, 1, size=(N, d))
    if family == "ball":
        z = rng.normal(size=(N, d)); z /= np.linalg.norm(z, axis=1, keepdims=True)
        r = rng.uniform(size=(N, 1)) ** (1.0 / d)
        return z * r
    if family == "student":
        nu = float(params.get("nu", 3.0)); z = rng.normal(size=(N, d))
        return z / np.sqrt(rng.chisquare(nu, size=(N, 1)) / nu)
    if family == "mixture":
        m = int(params.get("centres", 4)); centres = rng.normal(size=(m, d)) * float(params.get("spread", 2.0))
        lab = rng.integers(0, m, size=N)
        return centres[lab] + rng.normal(size=(N, d))
    if family == "aniso_cube":
        sd = np.arange(1, d + 1, dtype=float) ** (-float(params.get("alpha_data", 1.0)) / 2.0)
        return rng.uniform(-1, 1, size=(N, d)) * sd
    if family == "laplace":
        return rng.laplace(size=(N, d))
    if family == "lognormal":
        return np.exp(float(params.get("sigma", 0.5)) * rng.normal(size=(N, d)))
    if family == "shell":
        z = rng.normal(size=(N, d)); return z / np.linalg.norm(z, axis=1, keepdims=True)
    if family == "subspace":
        m = int(params["m"]); noise = float(params.get("noise", 0.05))
        Q, _ = np.linalg.qr(rng.normal(size=(d, m)))
        return rng.normal(size=(N, m)) @ Q.T + noise * rng.normal(size=(N, d))
    if family == "fourier":
        m = int(params["m"]); noise = float(params.get("noise", 0.05)); n_feat = int(params.get("features", 3 * d))
        z = rng.normal(size=(N, m)); W = rng.normal(size=(m, n_feat)) * float(params.get("bandwidth", 0.5)); b = rng.uniform(0, 2 * np.pi, size=n_feat)
        phi = np.cos(z @ W + b)
        A = rng.normal(size=(n_feat, d)) / np.sqrt(n_feat)
        x = phi @ A
        return x / x.std() + noise * rng.normal(size=(N, d))
    if family == "torus":
        # m angles (the intrinsic dimension); each angle contributes cos and sin of its first H harmonics,
        # so the cloud is a curved m-manifold whose spectral dimension grows with H, as real embeddings do
        m = int(params["m"]); noise = float(params.get("noise", 0.05)); H = max(1, min(int(params.get("harmonics", 1)), d // (2 * m)))
        th = rng.uniform(0, 2 * np.pi, size=(N, m))
        pts = np.concatenate([f(h * th) for h in range(1, H + 1) for f in (np.cos, np.sin)], axis=1) / np.sqrt(H)
        Q, _ = np.linalg.qr(rng.normal(size=(d, 2 * m * H)))
        return pts @ Q.T + noise * rng.normal(size=(N, d))
    if family == "swissroll":
        noise = float(params.get("noise", 0.05)); t = 1.5 * np.pi * (1 + 2 * rng.uniform(size=N)); h = 10 * rng.uniform(size=N)
        pts = np.stack([t * np.cos(t), h, t * np.sin(t)], axis=1); pts = (pts - pts.mean(0)) / pts.std()
        Q, _ = np.linalg.qr(rng.normal(size=(d, 3)))
        return pts @ Q.T + noise * rng.normal(size=(N, d))
    if family == "two_scale":
        m = int(params.get("centres", 4)); centres = rng.normal(size=(m, d)) * float(params.get("spread", 2.0))
        lab = rng.integers(0, m, size=N); scale = np.where(lab % 2 == 0, 1.0, float(params.get("ratio", 3.0)))[:, None]
        return centres[lab] + rng.normal(size=(N, d)) * scale
    raise ValueError(family)


def load_real(kind: str, N: int, offset: int, path: str) -> np.ndarray:
    if kind == "npy":
        a = np.load(path, mmap_mode="r")
        return np.array(a[offset: offset + N], dtype=np.float64)
    if kind == "u8bin":
        with open(path, "rb") as f:
            n, d = np.frombuffer(f.read(8), dtype=np.uint32)
            f.seek(8 + offset * int(d))
            x = np.frombuffer(f.read(N * int(d)), dtype=np.uint8).reshape(N, int(d))
        return np.array(x, dtype=np.float64)
    raise ValueError(kind)


# ----------------------------------------------------------------------------- observers and distances


def make_observer(d: int, alpha: float, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """C = diag(s) R with s_i = i^-alpha and R a Haar-random rotation."""
    Q, Rr = np.linalg.qr(rng.normal(size=(d, d)))
    Q = Q * np.sign(np.diag(Rr))
    s = np.arange(1, d + 1, dtype=float) ** (-alpha)
    return Q, s


def observe(x: np.ndarray, Q: np.ndarray, s: np.ndarray, budget: float = 0.0) -> np.ndarray:
    y = (x @ Q.T) * s
    if budget > 0:
        y = budget * np.round(y / budget)
    return y


def knn_search(y: np.ndarray, k: int, block: int = 1024) -> tuple[np.ndarray, np.ndarray]:
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
            "cv_knn": float(rk.std() / rk.mean()), "rc": float(mean_pair_dist / rk.mean())}


def occurrence_counts(idx: np.ndarray, N: int, k: int) -> np.ndarray:
    return np.bincount(idx[:, :k].ravel(), minlength=N)


def hub_stats(counts: np.ndarray, N: int, k: int) -> dict:
    z = (counts - counts.mean()) / (counts.std() + 1e-12)
    return {"skew": skewness(counts), "excess": float(counts.max() / max(poisson_null_max(float(k), N), 1)),
            "tail_share_1pct": tail_share(counts, 0.01), "antihub_frac": float((counts == 0).mean()),
            "count_max": int(counts.max()), "hub_frac": float((z >= 2.0).mean())}


def spectral_variables(y: np.ndarray, d_nom: int, N: int, rng: np.random.Generator) -> dict:
    """Spectral summaries of the observed covariance and the distance concentration of a sample."""
    yc = y - y.mean(0)
    lam = np.clip(np.linalg.eigvalsh(yc.T @ yc / (len(y) - 1)), 0, None); tr = lam.sum()
    p = lam / tr
    d_eff = float(tr ** 2 / (lam ** 2).sum())
    d_ent = float(np.exp(-(p[p > 0] * np.log(p[p > 0])).sum()))
    top_share = float(lam.max() / tr)
    m = min(512, len(y)); sub = y[rng.choice(len(y), m, replace=False)]
    sq = (sub * sub).sum(1); D = np.sqrt(np.maximum(sq[:, None] + sq[None, :] - 2.0 * (sub @ sub.T), 0))
    iu = np.triu_indices(m, 1); dist = D[iu]
    return {"d_eff": d_eff, "d_ent": d_ent, "top_share": top_share, "d_nom": float(d_nom), "N": float(N),
            "cv_d": float(dist.std() / dist.mean()), "mean_pair_dist": float(dist.mean()), "median_nn_dist": float(np.median(np.sort(D + np.eye(m) * 1e30, axis=1)[:, 0]))}


def effective_rank(H: np.ndarray) -> float:
    s = np.linalg.svd(H, compute_uv=False); s2 = s ** 2
    return float(s2.sum() ** 2 / (s2 ** 2).sum()) if s2.sum() > 0 else 0.0


# ----------------------------------------------------------------------------- law family


def _pos(x):
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
NOMINAL_ONLY = {"log_d_nom", "d_nom", "sqrt_d_nom", "inv_d_nom", "log_N", "N", "sqrt_N", "inv_N", "log_k", "k", "inv_k", "sqrt_k", "log_kN", "log_d_nom_x_log_k", "sqrt_d_nom_over_k"}
D2_FROZEN_LAW = {"target": "skew", "features": ["inv_cv_d", "sqrt_d_eff_over_k"], "coef": [-0.026165647256707177, 0.4206954447231824, 0.8172228220333909], "transform": "identity",
                 "note": "the law gate D2 froze on Gaussian clouds (observation-theory-campaigns/experiments/OD/D2/law.json), carried as a fixed competitor"}
D2V2_FROZEN_LAW = {"target": "skew", "features": ["d_ent", "inv_cv_d", "sqrt_top_share"], "coef": [2.8109594094123243, 0.004706131843131253, -0.09277311281123588, -2.461264557894105], "transform": "log1p",
                   "note": "the law gate D2v2 froze on seven full-dimensional families (observation-theory-campaigns/experiments/OD/D2v2/law.json), carried as a fixed competitor"}


def feature_matrix(rows: list[dict], names: list[str]) -> np.ndarray:
    if not names:
        return np.zeros((len(rows), 0))
    return np.stack([np.array([FEATURES[n](r["variables"]) for r in rows]) for n in names], axis=1)


def fwd(y, transform):
    return np.log1p(np.maximum(y, -0.99)) if transform == "log1p" else y


def back(y, transform):
    return np.expm1(y) if transform == "log1p" else y


def fit_law(rows: list[dict], names: list[str], target: str, transform: str = "identity") -> tuple[np.ndarray, float]:
    X = np.column_stack([np.ones(len(rows)), feature_matrix(rows, names)]); yv = np.array([r["targets"][target] for r in rows])
    coef, *_ = np.linalg.lstsq(X, fwd(yv, transform), rcond=None)
    return coef, float(np.sqrt(np.mean((back(X @ coef, transform) - yv) ** 2)))


def apply_law(law: dict, rows: list[dict]) -> np.ndarray:
    X = np.column_stack([np.ones(len(rows)), feature_matrix(rows, law["features"])])
    return back(X @ np.array(law["coef"]), law.get("transform", "identity"))


def rmse(law: dict, rows: list[dict]) -> float:
    pred = apply_law(law, rows); yv = np.array([r["targets"][law["target"]] for r in rows])
    return float(np.sqrt(np.mean((pred - yv) ** 2)))


def discover(train: list[dict], heldout: list[dict], target: str, max_terms: int = 2, pool: set | None = None, transforms=("identity", "log1p")) -> dict:
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
    return best


# ----------------------------------------------------------------------------- one world


def run_world(world: dict, cfg: dict, seed: int, log=print) -> dict:
    rng = np.random.default_rng(seed + int(world["seed_offset"]))
    N = int(world["N"]); ks = [int(k) for k in cfg["k_ladder"]]; kmax = max(ks)
    if world["family"] == "real":
        x = load_real(world["kind"], N, int(world["offset"]), world["path"])
    else:
        x = gen_data(world["family"], int(world["d"]), N, rng, world.get("params", {}))
    d = x.shape[1]
    obs_specs = [(float(a), r) for a in world.get("alphas", cfg["observer_alphas"]) for r in range(int(world.get("rotations", cfg["rotations_per_alpha"])))]
    rows = []; hub_sets = {}; anti_sets = {}; H_cols = []; t0 = time.time()
    for alpha, rot in obs_specs:
        Q, s = make_observer(d, alpha, rng)
        y = observe(x, Q, s)
        var = spectral_variables(y, d, N, rng)
        idx, kdist = knn_search(y, kmax)
        var.update(shape_variables(y, kdist, int(cfg["k_law"]), var["mean_pair_dist"]))
        oname = f"a{alpha}_r{rot}"
        for k in ks:
            counts = occurrence_counts(idx, N, k)
            st = hub_stats(counts, N, k)
            rows.append({"world": world["name"], "observer": oname, "alpha": alpha, "rotation": rot, "k": k,
                         "variables": {**var, "k": float(k)}, "targets": st})
            if k == int(cfg["k_law"]):
                z = (counts - counts.mean()) / (counts.std() + 1e-12)
                hub_sets[oname] = set(np.nonzero(z >= 2.0)[0].tolist()); anti_sets[oname] = set(np.nonzero(counts == 0)[0].tolist())
                H_cols.append(counts.astype(float))
        # budget sweep on the declared observers
        if world.get("budget_sweep") and rot == 0 and alpha in [float(a) for a in cfg["budget_alphas"]]:
            k = int(cfg["k_law"]); base_counts = occurrence_counts(idx, N, k)
            zb = (base_counts - base_counts.mean()) / (base_counts.std() + 1e-12)
            pol0 = np.where(zb >= 2.0, 1, np.where(base_counts == 0, -1, 0))
            for b in cfg["budget_ladder"]:
                B = float(b) * var["median_nn_dist"]
                cb = occurrence_counts(knn_indices(observe(x, Q, s, B), k), N, k)
                zq = (cb - cb.mean()) / (cb.std() + 1e-12); polq = np.where(zq >= 2.0, 1, np.where(cb == 0, -1, 0))
                rows.append({"world": world["name"], "observer": oname, "alpha": alpha, "rotation": rot, "k": k, "budget_rel": float(b),
                             "variables": {**var, "k": float(k)}, "targets": hub_stats(cb, N, k),
                             "polarity_changed_frac": float((polq != pol0).mean()), "reversal_frac": float(((polq * pol0) < 0).mean())})
    # cross-observer matrix at k_law
    H = np.stack(H_cols, axis=1); Hs = (H - H.mean(0)) / (H.std(0) + 1e-12)
    rng_null = np.random.default_rng(seed + 977 + int(world["seed_offset"]))
    Hn = np.stack([rng_null.permutation(c) for c in H.T], axis=1); Hns = (Hn - Hn.mean(0)) / (Hn.std(0) + 1e-12)
    matrix = {"M": H.shape[1], "N": N, "rank_eff": effective_rank(H), "rank_eff_standardised": effective_rank(Hs),
              "null_rank_eff": effective_rank(Hn), "null_rank_eff_standardised": effective_rank(Hns)}
    # polarity reversals: same alpha (rotation only) against different alpha
    names = list(hub_sets.keys()); same = []; diff = []; jac_same = []; jac_diff = []; ajac_same = []; ajac_diff = []
    def jaccard(A, B):
        return len(A & B) / len(A | B) if (A | B) else 1.0
    for a, b in itertools.combinations(names, 2):
        rev = len(hub_sets[a] & anti_sets[b]) + len(hub_sets[b] & anti_sets[a])
        is_same = a.split("_")[0] == b.split("_")[0]
        (same if is_same else diff).append(rev / N)
        (jac_same if is_same else jac_diff).append(jaccard(hub_sets[a], hub_sets[b]))
        (ajac_same if is_same else ajac_diff).append(jaccard(anti_sets[a], anti_sets[b]))
    polarity = {"reversal_frac_same_alpha_mean": float(np.mean(same)) if same else float("nan"),
                "reversal_frac_diff_alpha_mean": float(np.mean(diff)) if diff else float("nan"),
                "hub_jaccard_same_alpha_mean": float(np.mean(jac_same)) if jac_same else float("nan"),
                "hub_jaccard_diff_alpha_mean": float(np.mean(jac_diff)) if jac_diff else float("nan"),
                "antihub_jaccard_same_alpha_mean": float(np.mean(ajac_same)) if ajac_same else float("nan"),
                "antihub_jaccard_diff_alpha_mean": float(np.mean(ajac_diff)) if ajac_diff else float("nan"),
                "pairs_same": len(same), "pairs_diff": len(diff),
                "hub_frac_mean": float(np.mean([len(v) / N for v in hub_sets.values()])),
                "antihub_frac_mean": float(np.mean([len(v) / N for v in anti_sets.values()]))}
    log(json.dumps({"world": world["name"], "rows": len(rows), "rank_eff": round(matrix["rank_eff_standardised"], 2), "null": round(matrix["null_rank_eff_standardised"], 2),
                    "jac_same": round(polarity["hub_jaccard_same_alpha_mean"], 3), "jac_diff": round(polarity["hub_jaccard_diff_alpha_mean"], 3), "seconds": round(time.time() - t0, 1)}))
    return {"name": world["name"], "group": world["group"], "family": world["family"], "d": d, "N": N, "rows": rows, "matrix": matrix, "polarity": polarity, "seconds": time.time() - t0}


def run(cfg: dict, seed_role: str, out_path: str, discover_path: str | None, law_path: str | None) -> dict:
    seed = int(cfg[f"seed_{seed_role}"])
    groups = cfg["groups_by_role"][seed_role]
    result = {"config": cfg, "seed_role": seed_role, "seed": seed, "started": time.strftime("%Y-%m-%d %H:%M:%S"), "worlds": []}
    for world in cfg["worlds"]:
        if seed_role == "probe":
            if not world.get("in_probe"):
                continue
        elif world["group"] not in groups:
            continue
        result["worlds"].append(run_world(world, cfg, seed))
        json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1)
    target = cfg["law_target"]
    if discover_path:
        train = [r for w in result["worlds"] if w["group"] == "train" for r in w["rows"] if "budget_rel" not in r]
        held = [r for w in result["worlds"] if w["group"] == "heldout" for r in w["rows"] if "budget_rel" not in r]
        law = discover(train, held, target, int(cfg["law_max_terms"]))
        comp = discover(train, held, target, int(cfg["law_max_terms"]), NOMINAL_ONLY)
        frozen = {"law": law, "competitor_nominal": comp, "competitor_d2": D2_FROZEN_LAW, "competitor_d2v2": D2V2_FROZEN_LAW, "target": target, "frozen_from": seed_role, "seed": seed, "n_train": len(train), "n_heldout": len(held),
                  "d2_law_heldout_rmse": rmse(D2_FROZEN_LAW, held), "d2_law_train_rmse": rmse(D2_FROZEN_LAW, train),
                  "d2v2_law_heldout_rmse": rmse(D2V2_FROZEN_LAW, held), "d2v2_law_train_rmse": rmse(D2V2_FROZEN_LAW, train)}
        json.dump(frozen, open(discover_path, "w", encoding="utf-8"), indent=1)
        result["law"] = frozen
        print(json.dumps({"law": law, "competitor": comp}))
    if law_path:
        frozen = json.load(open(law_path, encoding="utf-8")); result["law"] = frozen; result["evaluation"] = {}
        for w in result["worlds"]:
            rs = [r for r in w["rows"] if "budget_rel" not in r]
            result["evaluation"][w["name"]] = {"group": w["group"], "rmse_law": rmse(frozen["law"], rs), "rmse_competitor": rmse(frozen["competitor_nominal"], rs), "rmse_d2_law": rmse(frozen["competitor_d2"], rs), "rmse_d2v2_law": rmse(frozen["competitor_d2v2"], rs), "n": len(rs)}
    result["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
    json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1)
    return result


# ----------------------------------------------------------------------------- self test


def selftest() -> int:
    fails = 0; rng = np.random.default_rng(0)
    # kNN against brute force
    y = rng.normal(size=(300, 5)); idx = knn_indices(y, 4, block=64)
    D = ((y[:, None] - y[None]) ** 2).sum(-1); np.fill_diagonal(D, np.inf); ref = np.argsort(D, axis=1)[:, :4]
    ok = np.array_equal(idx, ref); print("knn exact:", ok); fails += 0 if ok else 1
    # counts sum to N k; Poisson ceiling above the mean
    c = occurrence_counts(idx, 300, 4); ok = c.sum() == 1200 and poisson_null_max(4.0, 300) > 4; print("counts and ceiling:", ok, c.sum(), poisson_null_max(4.0, 300)); fails += 0 if ok else 1
    # an observer with alpha = 0 is a rotation: distances, hence counts, unchanged
    x = rng.normal(size=(400, 8)); Q, s = make_observer(8, 0.0, rng); c0 = occurrence_counts(knn_indices(x, 5), 400, 5); c1 = occurrence_counts(knn_indices(observe(x, Q, s), 5), 400, 5)
    ok = np.array_equal(c0, c1); print("rotation invariance:", ok); fails += 0 if ok else 1
    # effective dimension: isotropic data under alpha = 0 has d_eff near d; under alpha = 2 far below
    x = rng.normal(size=(2000, 32)); v0 = spectral_variables(observe(x, *make_observer(32, 0.0, rng)), 32, 2000, rng); v2 = spectral_variables(observe(x, *make_observer(32, 2.0, rng)), 32, 2000, rng)
    ok = v0["d_eff"] > 25 and v2["d_eff"] < 3; print("d_eff: iso %.1f, alpha=2 %.2f" % (v0["d_eff"], v2["d_eff"]), ok); fails += 0 if ok else 1
    # hubness rises with dimension on isotropic Gaussians (Radovanovic): skew at d = 4 below skew at d = 64
    s4 = hub_stats(occurrence_counts(knn_indices(rng.normal(size=(2000, 4)), 10), 2000, 10), 2000, 10)["skew"]
    s64 = hub_stats(occurrence_counts(knn_indices(rng.normal(size=(2000, 64)), 10), 2000, 10), 2000, 10)["skew"]
    ok = s64 > s4 + 0.3; print("skew d=4 %.2f, d=64 %.2f" % (s4, s64), ok); fails += 0 if ok else 1
    # law fitting recovers a planted linear law exactly
    rows = [{"variables": {"d_eff": float(de), "d_ent": 1.0, "d_nom": 1.0, "N": 1000.0, "k": 10.0, "top_share": 0.1, "cv_d": 0.3}, "targets": {"skew": 0.5 + 0.7 * np.log(de)}} for de in (2, 4, 8, 16, 32)]
    law = discover(rows, rows, "skew", 1, {"log_d_eff", "d_eff", "log_N"}); ok = law["features"] == ["log_d_eff"] and abs(law["coef"][1] - 0.7) < 1e-9; print("planted law recovered:", ok, law["features"], law["coef"]); fails += 0 if ok else 1
    # effective rank: a rank-one matrix gives 1, a random one about min(N, M)
    ok = abs(effective_rank(np.outer(np.arange(1, 50), np.arange(1, 9))) - 1.0) < 1e-9 and effective_rank(rng.normal(size=(500, 8))) > 6; print("effective rank:", ok); fails += 0 if ok else 1
    # shape variables: a Gaussian and a uniform ball at d = 32 differ in cv_r and kurt_1d as expected
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
    # manifold families: TwoNN dimension near m and far below d, while the spectral dimension is not
    for fam, prm in (("subspace", {"m": 8, "noise": 0.01}), ("fourier", {"m": 8, "noise": 0.01}), ("torus", {"m": 4, "noise": 0.01, "harmonics": 4}), ("swissroll", {"noise": 0.005})):
        x = gen_data(fam, 64, 3000, rng, prm); v = spectral_variables(x, 64, 3000, rng); i, dd = knn_search(x, 20); sh = shape_variables(x, dd, 10, v["mean_pair_dist"])
        target = prm.get("m", 2)
        # the manifold's TwoNN dimension must sit far below the ambient one and near its intrinsic one;
        # the sheet, whose density varies along the spiral, is held only to the first condition
        # TwoNN overestimates curved manifolds at this sample size (Facco et al. note the finite-sample bias), so the
        # curved families are held to a factor of 2.5 of their intrinsic dimension and the flat one to 1.6
        ok = sh["id_twonn"] < 0.25 * 64 and (fam == "swissroll" or sh["id_twonn"] < (1.6 if fam == "subspace" else 2.5) * target)
        print("%-9s id_twonn %5.1f (m = %d) d_eff %5.1f d_ent %5.1f" % (fam, sh["id_twonn"], target, v["d_eff"], v["d_ent"]), ok); fails += 0 if ok else 1
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--config"); ap.add_argument("--seed-role", default="pilot")
    ap.add_argument("--out", default="out.json"); ap.add_argument("--discover"); ap.add_argument("--law")
    a = ap.parse_args(argv)
    if a.selftest:
        return 1 if selftest() else 0
    run(json.load(open(a.config, encoding="utf-8")), a.seed_role, a.out, a.discover, a.law)
    return 0


if __name__ == "__main__":
    sys.exit(main())
