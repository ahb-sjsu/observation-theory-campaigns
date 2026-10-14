"""Ladder-half splitting on a real world (PREREG-D8-RUN-DRAFT.md Section 9, item 3). The whole ladder and its two halves,
merged by merge_world_halves, must give the same m* and the same synchronization flags for every observer; the delta
series and the tangent exponents are compared and recorded beside them. The world is a test world (n = 64, nu = 0.03,
the probe seeds at a seed offset no gate uses), so no trajectory of the run is touched.

    python test_ladder_split.py run full     # the whole ladder
    python test_ladder_split.py run 0        # the lower half      (run the three in parallel)
    python test_ladder_split.py run 1        # the upper half
    python test_ladder_split.py compare      # merge the halves, compare, write ladder_split_test.json
"""
import json
import sys

import numpy as np

from d8_sync import merge_world_halves, run_world

WORLD = {"name": "split_test_nu030_n64", "group": "test", "n": 64, "nu": 0.03, "seed_offset": 31}
OBSERVERS = ["BALL", "READ"]
ROLE = "probe"  # the probe role carries both tangents (observer and block), so both draws are exercised


def max_diff(a, b) -> float:
    return float(np.max(np.abs(np.asarray(a, float) - np.asarray(b, float))))


def main() -> int:
    cfg = json.load(open("prereg_config.json", encoding="utf-8")); seed_train = int(cfg["seed_probe"]); seed_test = seed_train + 5000
    if sys.argv[1] == "run":
        tag = sys.argv[2]; half = None if tag == "full" else int(tag)
        out = run_world(WORLD, cfg, seed_train, seed_test, 1, ROLE, parts=["graded"], tests=[0], observers=OBSERVERS, ladder_half=half)
        json.dump(out, open(f"split_test_{tag}.json", "w", encoding="utf-8"), default=float)
        return 0
    whole, lo, hi = (json.load(open(f"split_test_{t}.json", encoding="utf-8")) for t in ("full", "0", "1"))
    merged = merge_world_halves(lo, hi); rows = {}
    for name in OBSERVERS:
        a = whole["tests"][0]["observers"][name]; b = merged["tests"][0]["observers"][name]
        rows[name] = {"m_star_whole": a["m_star"], "m_star_merged": b["m_star"], "nonmonotone_whole": a["nonmonotone"], "nonmonotone_merged": b["nonmonotone"],
                      "flags_whole": "".join("1" if f else "0" for f in a["synced"]), "flags_merged": "".join("1" if f else "0" for f in b["synced"]),
                      "delta_series_max_abs_diff": max_diff(a["delta_series"], b["delta_series"]),
                      "lyap_obs_max_abs_diff": max_diff(a["lyap_obs"], b["lyap_obs"]), "lyap_block_max_abs_diff": max_diff(a["lyap_block"], b["lyap_block"])}
    passed = all(r["m_star_whole"] == r["m_star_merged"] and r["flags_whole"] == r["flags_merged"] and r["nonmonotone_whole"] == r["nonmonotone_merged"] for r in rows.values())
    res = {"test": "ladder-half splitting, PREREG-D8-RUN-DRAFT.md Section 9 item 3", "world": WORLD, "role": ROLE, "ladder": whole["ladder"],
           "halves": [lo["tests"][0]["observers"][OBSERVERS[0]]["ladder_part"], hi["tests"][0]["observers"][OBSERVERS[0]]["ladder_part"]],
           "observers": rows, "seconds": {"whole": whole["seconds"], "half_0": lo["seconds"], "half_1": hi["seconds"]},
           "criterion": "m*, nonmonotone and every flag equal for each observer", "result": "PASS" if passed else "FAIL"}
    json.dump(res, open("ladder_split_test.json", "w", encoding="utf-8"), indent=1)
    print(json.dumps(res, indent=1))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
