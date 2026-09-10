"""Exploration for the D2v9 registration, on rows already collected (disclosed in the registration; the
D2v9 pilot and run use fresh seeds). For each candidate family shape, discover a law on a pilot's
training/held-out rows exactly as the pilot would, then score it on a run's rows the way the sealed
grader would (REF = pooled pilot error; L1 1.5 REF; L2 2 REF per world, 1.5 pooled; L3 3 REF; L4 2 REF;
L5 against the frozen D2v7 law at 0.95 pooled and within every group).

    python d2v9_explore.py <train pilot.json> <eval results.json> <out.json>
"""
import itertools
import json
import sys
import time

import numpy as np

sys.path.insert(0, "/archive/ahb-sjsu/observation-theory-campaigns/experiments/OD/D2v8")
from d2v8_hubness import FEATURES, D2V7_FROZEN_LAW, UNITY_LAW, _pos, rmse  # noqa: E402

# the shape change: products of a neighbour-distance tail with a dimension, and a dimension with the concentration
EXTRA = {
    "hill_rk_x_log_d_eff": lambda v: v["hill_rk"] * np.log(_pos(v["d_eff"])),
    "hill_rk_x_sqrt_id": lambda v: v["hill_rk"] * np.sqrt(_pos(v["id_twonn"])),
    "hill_rk_x_log_id": lambda v: v["hill_rk"] * np.log(_pos(v["id_twonn"])),
    "log_hill_x_sqrt_id": lambda v: np.log(_pos(v["hill_rk"])) * np.sqrt(_pos(v["id_twonn"])),
    "log_tail_knn_x_log_d_eff": lambda v: np.log(_pos(v["tail_knn"])) * np.log(_pos(v["d_eff"])),
    "log_tail_knn_x_sqrt_id": lambda v: np.log(_pos(v["tail_knn"])) * np.sqrt(_pos(v["id_twonn"])),
    "inv_cv_knn_x_log_id": lambda v: np.log(_pos(v["id_twonn"])) / _pos(v["cv_knn"]),
    "log_cv_knn_x_sqrt_id": lambda v: np.log(_pos(v["cv_knn"])) * np.sqrt(_pos(v["id_twonn"])),
    "sqrt_id_x_log_d_eff": lambda v: np.sqrt(_pos(v["id_twonn"])) * np.log(_pos(v["d_eff"])),
    "log_id_over_log_d_eff": lambda v: np.log(_pos(v["id_twonn"])) / np.log(_pos(v["d_eff"]) + 1.0),
    "sqrt_id_x_kurt_lrk3": lambda v: np.sqrt(_pos(v["id_twonn"])) * np.log(_pos(v["kurt_lrk"] + 3.0)),
    "log_rc_x_sqrt_id": lambda v: np.log(_pos(v["rc"])) * np.sqrt(_pos(v["id_twonn"])),
}
POOL = dict(FEATURES); POOL.update(EXTRA)


def rows_of(res, groups):
    return [r for w in res["worlds"] if w["group"] in groups for r in w["rows"] if "budget_rel" not in r]


def search(train, held, names, max_terms, target="log_excess"):
    Xtr = {n: np.array([POOL[n](r["variables"]) for r in train]) for n in names}
    Xho = {n: np.array([POOL[n](r["variables"]) for r in held]) for n in names}
    ok = [n for n in names if np.all(np.isfinite(Xtr[n])) and np.all(np.isfinite(Xho[n]))]
    ytr = np.array([r["targets"][target] for r in train]); yho = np.array([r["targets"][target] for r in held])
    best = None; t0 = time.time(); n_models = 0
    ones_tr = np.ones(len(train)); ones_ho = np.ones(len(held))
    for m in range(1, max_terms + 1):
        for combo in itertools.combinations(ok, m):
            X = np.column_stack([ones_tr] + [Xtr[n] for n in combo])
            coef, *_ = np.linalg.lstsq(X, ytr, rcond=None)
            Xh = np.column_stack([ones_ho] + [Xho[n] for n in combo])
            ho = float(np.sqrt(np.mean((Xh @ coef - yho) ** 2))); n_models += 1
            if np.isfinite(ho) and (best is None or ho < best["heldout_rmse"] - 1e-12):
                best = {"target": target, "features": list(combo), "coef": [float(c) for c in coef], "transform": "identity", "heldout_rmse": ho,
                        "train_rmse": float(np.sqrt(np.mean((X @ coef - ytr) ** 2))), "n_terms": m}
    best["seconds"] = time.time() - t0; best["models"] = n_models
    return best


def apply(law, rows):
    X = np.column_stack([np.ones(len(rows))] + [np.array([POOL[n](r["variables"]) for r in rows]) for n in law["features"]])
    return X @ np.array(law["coef"])


def err(law, rows):
    return float(np.sqrt(np.mean((apply(law, rows) - np.array([r["targets"][law["target"]] for r in rows])) ** 2)))


def grade(law, pilot, run):
    REF = err(law, rows_of(pilot, {"train", "heldout"}))
    out = {"REF": REF, "limits": {"L1": 1.5 * REF, "L2_world": 2 * REF, "L2_pooled": 1.5 * REF, "L3": 3 * REF, "L4": 2 * REF}}
    per = {w["name"]: (w["group"], err(law, [r for r in w["rows"] if "budget_rel" not in r]), err(D2V7_FROZEN_LAW, [r for r in w["rows"] if "budget_rel" not in r])) for w in run["worlds"]}
    out["worlds"] = per
    g = {}
    for grp in ("train", "heldout", "unseen", "real", "scale"):
        rs = rows_of(run, {grp}); g[grp] = {"law": err(law, rs), "d2v7": err(D2V7_FROZEN_LAW, rs), "unity": err(UNITY_LAW, rs)} if rs else None
    out["groups"] = g
    l1 = err(law, rows_of(run, {"train", "heldout"})) <= 1.5 * REF
    uns = [v for v in per.values() if v[0] == "unseen"]
    l2 = all(v[1] <= 2 * REF for v in uns) and g["unseen"]["law"] <= 1.5 * REF
    l3 = all(v[1] <= 3 * REF for v in per.values() if v[0] == "real")
    l4 = all(v[1] <= 2 * REF for v in per.values() if v[0] == "scale")
    tr = rows_of(run, {"unseen", "real", "scale"}); el, e7, eu = err(law, tr), err(D2V7_FROZEN_LAW, tr), err(UNITY_LAW, tr)
    l5 = el <= 0.95 * e7 and el <= 0.8 * eu and all(g[k]["law"] <= min(g[k]["d2v7"], g[k]["unity"]) for k in ("unseen", "real", "scale"))
    out["bars"] = {"L1": l1, "L2": l2, "L3": l3, "L4": l4, "L5": l5, "transfer_pooled": {"law": el, "d2v7": e7, "unity": eu}}
    out["misses"] = {n: round(v[1], 3) for n, v in per.items() if (v[0] == "unseen" and v[1] > 2 * REF) or (v[0] == "scale" and v[1] > 2 * REF) or (v[0] == "real" and v[1] > 3 * REF)}
    out["verdict"] = "PASS" if all([l1, l2, l3, l4, l5]) else "no"
    return out


def main():
    pilot = json.load(open(sys.argv[1])); run = json.load(open(sys.argv[2]))
    train = rows_of(pilot, {"train"}); held = rows_of(pilot, {"heldout"})
    base = sorted(FEATURES.keys()); ext = sorted(POOL.keys())
    configs = [("base_3", base, 3), ("ext_3", ext, 3), ("ext_4", ext, 4)]
    results = {"train_from": sys.argv[1], "eval_on": sys.argv[2], "configs": {}}
    for name, names, mt in configs:
        law = search(train, held, names, mt)
        gr = grade(law, pilot, run)
        results["configs"][name] = {"law": law, "grade": gr}
        print(json.dumps({"config": name, "features": law["features"], "coef": [round(c, 4) for c in law["coef"]], "heldout": round(law["heldout_rmse"], 4), "REF": round(gr["REF"], 4),
                          "bars": gr["bars"], "misses": gr["misses"], "seconds": round(law["seconds"], 1), "models": law["models"]}), flush=True)
        json.dump(results, open(sys.argv[3], "w"), indent=1)
    # the frozen D2v7 law under the same bars, for reference
    gr7 = grade(D2V7_FROZEN_LAW, pilot, run); results["d2v7_reference"] = gr7
    print(json.dumps({"config": "d2v7_frozen", "REF": round(gr7["REF"], 4), "bars": gr7["bars"], "misses": gr7["misses"]}), flush=True)
    json.dump(results, open(sys.argv[3], "w"), indent=1)
    print("EXPLORE_DONE")


if __name__ == "__main__":
    main()
