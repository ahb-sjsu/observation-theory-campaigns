"""Third exploration for the D2v9 registration: the family without divergent terms. The pure reciprocals
of the concentration and tail variables (1 / cv_knn, 1 / hill_rk, 1 / cv_d, 1 / cv_r, 1 / tail_knn,
1 / tail_r1) leave the pool; the softened reciprocals 1 / (x + c) at declared c replace them. Same
protocol as d2v9_explore.py; optionally the held-out set gains an over-concentrated world by moving
a named training world into it (the ranking then sees the regime the transfer asks about).

    python d2v9_explore3.py <train pilot.json> <eval results.json> <out.json> <max_terms> [world-to-hold-out,...]
"""
import json
import sys

sys.path.insert(0, "/home/claude")
import d2v9_explore as E  # noqa: E402
import d2v9_explore2 as E2  # noqa: E402
from d2v8_hubness import FEATURES  # noqa: E402

DIVERGENT = {"inv_cv_knn", "inv_hill_rk", "inv_cv_d", "inv_cv_r", "inv_tail_knn", "inv_tail_r1", "inv_cv_d_over_k"}


def main():
    pilot = json.load(open(sys.argv[1])); run = json.load(open(sys.argv[2])); mt = int(sys.argv[4])
    move = set(sys.argv[5].split(",")) if len(sys.argv) > 5 else set()
    train = [r for w in pilot["worlds"] if w["group"] == "train" and w["name"] not in move for r in w["rows"] if "budget_rel" not in r]
    held = [r for w in pilot["worlds"] if (w["group"] == "heldout" or w["name"] in move) for r in w["rows"] if "budget_rel" not in r]
    names = sorted((set(FEATURES.keys()) - DIVERGENT) | set(E2.SOFT.keys()))
    law = E.search(train, held, names, mt)
    gr = E.grade(law, pilot, run)
    tag = "nodiv_%d%s" % (mt, ("_held+" + "+".join(sorted(move))) if move else "")
    print(json.dumps({"config": tag, "features": law["features"], "coef": [round(c, 4) for c in law["coef"]], "heldout": round(law["heldout_rmse"], 4), "REF": round(gr["REF"], 4),
                      "bars": gr["bars"], "misses": gr["misses"], "seconds": round(law["seconds"], 1), "models": law["models"]}), flush=True)
    worst = sorted(((n, v[1]) for n, v in gr["worlds"].items() if v[0] in ("unseen", "scale", "real")), key=lambda t: -t[1])[:6]
    print(json.dumps({"worst_transfer_worlds": [(n, round(e, 3)) for n, e in worst], "groups": {k: {a: round(b, 3) for a, b in v.items()} for k, v in gr["groups"].items() if v}}), flush=True)
    json.dump({"law": law, "grade": gr, "held_out_added": sorted(move)}, open(sys.argv[3], "w"), indent=1)
    print("EXPLORE3_DONE")


if __name__ == "__main__":
    main()
