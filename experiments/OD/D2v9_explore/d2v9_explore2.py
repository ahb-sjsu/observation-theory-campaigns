"""Second exploration for the D2v9 registration: the shape repair is a saturating concentration term.
The reciprocal 1 / cv_knn (and 1 / hill_rk) diverges on over-concentrated worlds (the ball at d = 384
reads cv_knn 0.003 under the isotropic reader, six times below the Gaussian's) and predicts an excess
near zero where the truth is 1.4. Softened reciprocals 1 / (x + c) at declared c join the pool; the
search chooses among them. Same protocol as d2v9_explore.py.

    python d2v9_explore2.py <train pilot.json> <eval results.json> <out.json> <max_terms>
"""
import json
import sys

import numpy as np

sys.path.insert(0, "/home/claude")
import d2v9_explore as E  # noqa: E402
from d2v8_hubness import FEATURES, _pos  # noqa: E402

SOFT = {}
for c in (0.01, 0.02, 0.05, 0.1):
    SOFT["inv_cv_knn_c%g" % c] = (lambda cc: (lambda v: 1.0 / (_pos(v["cv_knn"]) + cc)))(c)
for c in (0.005, 0.01, 0.02, 0.05):
    SOFT["inv_hill_rk_c%g" % c] = (lambda cc: (lambda v: 1.0 / (_pos(v["hill_rk"]) + cc)))(c)
for c in (0.01, 0.03, 0.1):
    SOFT["inv_cv_d_c%g" % c] = (lambda cc: (lambda v: 1.0 / (_pos(v["cv_d"]) + cc)))(c)
    SOFT["inv_cv_r_c%g" % c] = (lambda cc: (lambda v: 1.0 / (_pos(v["cv_r"]) + cc)))(c)
E.POOL.update(SOFT)


def main():
    pilot = json.load(open(sys.argv[1])); run = json.load(open(sys.argv[2])); mt = int(sys.argv[4])
    train = E.rows_of(pilot, {"train"}); held = E.rows_of(pilot, {"heldout"})
    names = sorted(set(FEATURES.keys()) | set(SOFT.keys()))
    law = E.search(train, held, names, mt)
    gr = E.grade(law, pilot, run)
    print(json.dumps({"config": "soft_%d" % mt, "features": law["features"], "coef": [round(c, 4) for c in law["coef"]], "heldout": round(law["heldout_rmse"], 4), "REF": round(gr["REF"], 4),
                      "bars": gr["bars"], "misses": gr["misses"], "seconds": round(law["seconds"], 1), "models": law["models"]}), flush=True)
    worst = sorted(((n, v[1]) for n, v in gr["worlds"].items() if v[0] in ("unseen", "scale", "real")), key=lambda t: -t[1])[:6]
    print(json.dumps({"worst_transfer_worlds": [(n, round(e, 3)) for n, e in worst], "groups": {k: {a: round(b, 3) for a, b in v.items()} for k, v in gr["groups"].items() if v}}), flush=True)
    json.dump({"law": law, "grade": gr}, open(sys.argv[3], "w"), indent=1)
    print("EXPLORE2_DONE")


if __name__ == "__main__":
    main()
