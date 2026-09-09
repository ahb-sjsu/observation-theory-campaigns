"""Exploratory annotation for the D2v5 registration (not a bar): the best model of the declared family
that contains at least one neighbour-distance tail variable, against the frozen law, on the pilot rows."""
import json
import sys

sys.path.insert(0, "/archive/ahb-sjsu/observation-theory-campaigns/experiments/OD/D2v5")
import numpy as np  # noqa: E402
from d2v5_hubness import FEATURES, discover, rmse  # noqa: E402

res = json.load(open(sys.argv[1], encoding="utf-8"))
train = [r for w in res["worlds"] if w["group"] == "train" for r in w["rows"] if "budget_rel" not in r]
held = [r for w in res["worlds"] if w["group"] == "heldout" for r in w["rows"] if "budget_rel" not in r]
TAIL = [n for n in FEATURES if any(t in n for t in ("tail_knn", "tail_r1", "hill_rk", "kurt_lrk"))]
print("tail features", len(TAIL))
# rank every model with at least one tail feature: run discover on the full pool but keep the best that uses a tail feature
best_tail = None
for tf in TAIL:
    others = [n for n in FEATURES if n != tf]
    # models = tf plus up to two others: discover with max_terms 2 on a pool, forcing tf in by adding it as a fixed column is not
    # supported, so enumerate directly
    import itertools
    Xtr = {n: np.array([FEATURES[n](r["variables"]) for r in train]) for n in FEATURES}
    Xho = {n: np.array([FEATURES[n](r["variables"]) for r in held]) for n in FEATURES}
    ok = [n for n in others if np.all(np.isfinite(Xtr[n])) and np.all(np.isfinite(Xho[n]))]
    if not (np.all(np.isfinite(Xtr[tf])) and np.all(np.isfinite(Xho[tf]))):
        continue
    ytr = np.array([r["targets"]["skew"] for r in train]); yho = np.array([r["targets"]["skew"] for r in held])
    for transform in ("identity", "log1p"):
        ytr_t = np.log1p(np.maximum(ytr, -0.99)) if transform == "log1p" else ytr
        for m in range(0, 3):
            for combo in itertools.combinations(ok, m):
                names = (tf,) + combo
                X = np.column_stack([np.ones(len(train))] + [Xtr[n] for n in names])
                coef, *_ = np.linalg.lstsq(X, ytr_t, rcond=None)
                Xh = np.column_stack([np.ones(len(held))] + [Xho[n] for n in names])
                ph = Xh @ coef; ph = np.expm1(ph) if transform == "log1p" else ph
                ho = float(np.sqrt(np.mean((ph - yho) ** 2)))
                if np.isfinite(ho) and (best_tail is None or ho < best_tail["heldout_rmse"]):
                    pt = X @ coef; pt = np.expm1(pt) if transform == "log1p" else pt
                    best_tail = {"target": "skew", "features": list(names), "coef": [float(c) for c in coef], "transform": transform, "heldout_rmse": ho, "train_rmse": float(np.sqrt(np.mean((pt - ytr) ** 2)))}
law = res["law"]["law"]
allrows = train + held
out = {"frozen_law": law, "frozen_pooled": rmse(law, allrows), "best_with_tail": best_tail, "best_with_tail_pooled": rmse(best_tail, allrows),
       "per_world_heavy": {w["name"]: {"frozen": rmse(law, [r for r in w["rows"] if "budget_rel" not in r]), "with_tail": rmse(best_tail, [r for r in w["rows"] if "budget_rel" not in r])} for w in res["worlds"] if w["family"] in ("student", "laplace")}}
print(json.dumps(out, indent=1))
json.dump(out, open(sys.argv[2], "w"), indent=1)
