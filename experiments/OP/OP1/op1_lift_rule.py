"""OP1's rule for which lifts are graded (PREREG-OP1-DRAFT.md Section 7, fixed before probe round 2 ran), applied to the
probe's results. A lift is graded only if the best error over every arm computed under it (READ, ENERGY, BALL, SENS,
each RANDOM draw, POD and GREEDY where run), at the top of the ladder, pooled over the probe's worlds and cutoffs, is at
least 5 percent below the consumer alone (NONE). The script prints only that comparison; it never reports READ's
standing against the controls.

    python op1_lift_rule.py probe2_pr_nu020_n96.json probe2_pr_nu030_n96.json
"""
import json
import sys

import numpy as np

THRESHOLD = 0.05


def main(paths: list[str]) -> int:
    worlds = [w for p in paths for w in json.load(open(p, encoding="utf-8"))["worlds"]]
    lifts = sorted({l for w in worlds for c in w["cutoffs"].values() for l in c["lifts"]})
    out = {}
    for lift in lifts:
        best, none = [], []
        for w in worlds:
            for kc, c in w["cutoffs"].items():
                if lift not in c["lifts"]: continue
                L = c["lifts"][lift]; top = L[str(max(c["ladder"]))]
                arms = [top[k]["E"] for k in ("READ", "ENERGY", "BALL", "SENS", "POD", "GREEDY") if top.get(k)] + list(top["RANDOM_E"])
                best.append(min(arms)); none.append(L["NONE"]["E"])
        b, n = float(np.mean(best)), float(np.mean(none)); gain = 1.0 - b / n
        out[lift] = {"cells": len(best), "best_of_all_arms_at_top_r": round(b, 4), "none": round(n, 4), "gain": round(gain, 4), "graded": gain >= THRESHOLD}
    print(json.dumps({"rule": "graded if pooled best-of-all-arms at top r is >= 5% below NONE (READ-blind)", "lifts": out}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
