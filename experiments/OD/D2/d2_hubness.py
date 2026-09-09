"""D2: observer-relative hubness, the law (OD track, gate D2).

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


def knn_indices(y: np.ndarray, k: int, block: int = 1024) -> np.ndarray:
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
    return out


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
            "cv_d": float(dist.std() / dist.mean()), "median_nn_dist": float(np.median(np.sort(D + np.eye(m) * 1e30, axis=1)[:, 0]))}


def effective_rank(H: np.ndarray) -> float:
    s = np.linalg.svd(H, compute_uv=False); s2 = s ** 2
    return float(s2.sum() ** 2 / (s2 ** 2).sum()) if s2.sum() > 0 else 0.0


# ----------------------------------------------------------------------------- law family


FEATURES = {
    "log_d_eff": lambda v: np.log(v["d_eff"]), "d_eff": lambda v: v["d_eff"], "sqrt_d_eff": lambda v: np.sqrt(v["d_eff"]), "inv_d_eff": lambda v: 1.0 / v["d_eff"],
    "log_d_ent": lambda v: np.log(v["d_ent"]), "d_ent": lambda v: v["d_ent"], "sqrt_d_ent": lambda v: np.sqrt(v["d_ent"]),
    "log_d_nom": lambda v: np.log(v["d_nom"]), "d_nom": lambda v: v["d_nom"], "sqrt_d_nom": lambda v: np.sqrt(v["d_nom"]),
    "log_N": lambda v: np.log(v["N"]), "log_k": lambda v: np.log(v["k"]), "k": lambda v: v["k"], "inv_k": lambda v: 1.0 / v["k"], "sqrt_k": lambda v: np.sqrt(v["k"]),
    "log_kN": lambda v: np.log(v["k"] / v["N"]), "top_share": lambda v: v["top_share"], "log_top_share": lambda v: np.log(v["top_share"]),
    "cv_d": lambda v: v["cv_d"], "inv_cv_d": lambda v: 1.0 / v["cv_d"], "log_cv_d": lambda v: np.log(v["cv_d"]),
    "log_d_eff_x_log_k": lambda v: np.log(v["d_eff"]) * np.log(v["k"]), "log_d_eff_over_log_N": lambda v: np.log(v["d_eff"]) / np.log(v["N"]),
    "sqrt_d_eff_over_k": lambda v: np.sqrt(v["d_eff"]) / v["k"], "d_eff_over_log_N": lambda v: v["d_eff"] / np.log(v["N"]),
    "log_d_nom_x_log_k": lambda v: np.log(v["d_nom"]) * np.log(v["k"]), "log_d_nom_over_log_N": lambda v: np.log(v["d_nom"]) / np.log(v["N"]),
}
NOMINAL_ONLY = {"log_d_nom", "d_nom", "sqrt_d_nom", "log_N", "log_k", "k", "inv_k", "sqrt_k", "log_kN", "log_d_nom_x_log_k", "log_d_nom_over_log_N"}


def feature_matrix(rows: list[dict], names: list[str]) -> np.ndarray:
    if not names:
        return np.zeros((len(rows), 0))
    return np.stack([np.array([FEATURES[n](r["variables"]) for r in rows]) for n in names], axis=1)


def fit_law(rows: list[dict], names: list[str], target: str) -> tuple[np.ndarray, float]:
    X = np.column_stack([np.ones(len(rows)), feature_matrix(rows, names)]); yv = np.array([r["targets"][target] for r in rows])
    coef, *_ = np.linalg.lstsq(X, yv, rcond=None)
    return coef, float(np.sqrt(np.mean((X @ coef - yv) ** 2)))


def apply_law(law: dict, rows: list[dict]) -> np.ndarray:
    X = np.column_stack([np.ones(len(rows)), feature_matrix(rows, law["features"])])
    return X @ np.array(law["coef"])


def rmse(law: dict, rows: list[dict]) -> float:
    pred = apply_law(law, rows); yv = np.array([r["targets"][law["target"]] for r in rows])
    return float(np.sqrt(np.mean((pred - yv) ** 2)))


def discover(train: list[dict], heldout: list[dict], target: str, max_terms: int = 2, pool: set | None = None) -> dict:
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
        idx = knn_indices(y, kmax)
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
        frozen = {"law": law, "competitor_nominal": comp, "target": target, "frozen_from": seed_role, "seed": seed, "n_train": len(train), "n_heldout": len(held)}
        json.dump(frozen, open(discover_path, "w", encoding="utf-8"), indent=1)
        result["law"] = frozen
        print(json.dumps({"law": law, "competitor": comp}))
    if law_path:
        frozen = json.load(open(law_path, encoding="utf-8")); result["law"] = frozen; result["evaluation"] = {}
        for w in result["worlds"]:
            rs = [r for r in w["rows"] if "budget_rel" not in r]
            result["evaluation"][w["name"]] = {"group": w["group"], "rmse_law": rmse(frozen["law"], rs), "rmse_competitor": rmse(frozen["competitor_nominal"], rs), "n": len(rs)}
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
