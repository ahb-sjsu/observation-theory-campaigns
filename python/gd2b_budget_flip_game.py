#!/usr/bin/env python3
"""GD-2b the budget flip in a game, corrected declaration.

Identical to GD-2 in every declared object, bar, seed, and ensemble.
The one correction is C4's declared count of tied fidelity-optimal
2-cell partitions, three, not six, GD-2's declaration tallied each
two-cell partition once from each of its cells. Verdict computed
from the measured items.

Exploratory label. No claim about human beings.
"""
from __future__ import annotations

import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gd2_budget_flip_game import (  # noqa: E402
    CLOSED_TOL, FLIP_TOL, MONO_TOL, TIE_TOL, analyze,
    set_partitions)
from projection_fold import canonical_sha256  # noqa: E402

DECLARED_MI_TIES_K2 = 3


def main() -> int:
    record: dict = {"schema": "gd2b-budget-flip-game-v1",
                    "label": "exploratory"}
    parts = list(set_partitions(list(range(6))))
    assert len(parts) == 203

    prior = np.array([4, 4, 4, 1, 1, 1], dtype=float) / 15.0
    b = np.array([0, 0, 0, 1, 1, 1])
    stakes = np.array([1.0, 3.0])
    payoff = np.zeros((6, 2, 2))
    for s in range(6):
        for a1 in range(2):
            for a2 in range(2):
                payoff[s, a1, a2] = stakes[a2] * \
                    (1.0 if a1 == b[s] else -2.0)

    ex, values, finest_v = analyze(prior, payoff, parts,
                                   budgets=range(1, 7))
    v_ladder = [ex[k]["v_task"] for k in range(1, 7)]
    h_ladder = [ex[k]["h_max_bits"] for k in range(1, 7)]

    h1 = ex[2]["flip"] >= 0.5
    h2 = (abs(ex[6]["v_fid_best"] - ex[6]["v_task"]) <= MONO_TOL
          and abs(ex[6]["v_task"] - finest_v) <= MONO_TOL)
    c1 = all(v_ladder[i + 1] >= v_ladder[i] - MONO_TOL
             for i in range(5))
    c2 = all(h_ladder[i + 1] >= h_ladder[i] - MONO_TOL
             for i in range(5))
    c3 = max(values) <= finest_v + MONO_TOL
    closed = {"v_task_k2": (ex[2]["v_task"], 1.0),
              "v_fid_k2": (ex[2]["v_fid_best"], 0.4),
              "v_task_k1": (ex[1]["v_task"], 0.4),
              "v_finest": (finest_v, 1.0)}
    c4 = (all(abs(m - c) <= CLOSED_TOL
              for m, c in closed.values())
          and ex[2]["n_mi_ties"] == DECLARED_MI_TIES_K2)
    record["exhibit"] = {
        "per_budget": {str(k): {kk: (float(vv) if not
                                     isinstance(vv, int) else vv)
                                for kk, vv in ex[k].items()}
                       for k in ex},
        "closed_forms": {k: {"measured": float(m), "declared": c}
                         for k, (m, c) in closed.items()},
        "flip_k2": float(ex[2]["flip"]),
        "declared_mi_ties_k2": DECLARED_MI_TIES_K2,
        "items": {"H1": bool(h1), "H2": bool(h2), "C1": bool(c1),
                  "C2": bool(c2), "C3": bool(c3), "C4": bool(c4)}}
    print("exhibit flip", ex[2]["flip"], "ties", ex[2]["n_mi_ties"],
          record["exhibit"]["items"])

    rng = np.random.RandomState(20260808)
    n_games = 200
    c3_ok = True
    flips = {2: [], 3: []}
    for g in range(n_games):
        pr = rng.dirichlet(np.ones(6))
        pay = rng.uniform(-1, 1, size=(6, 3, 2))
        res, vals, fin = analyze(pr, pay, parts, budgets=(2, 3, 6))
        if max(vals) > fin + MONO_TOL:
            c3_ok = False
        for k in (2, 3):
            flips[k].append(res[k]["flip"])
    c3 = c3 and c3_ok
    record["exhibit"]["items"]["C3"] = bool(c3)
    ens = {}
    for k in (2, 3):
        f = np.array(flips[k])
        ens[str(k)] = {
            "games": n_games,
            "flip_count": int(np.sum(f > FLIP_TOL)),
            "flip_fraction": float(np.mean(f > FLIP_TOL)),
            "flip_max": float(f.max()),
            "flip_median_over_flips":
                float(np.median(f[f > FLIP_TOL]))
                if np.any(f > FLIP_TOL) else 0.0}
    record["ensemble"] = {"seed": 20260808, "note":
                          "measurement, no bar", **ens}

    items = record["exhibit"]["items"]
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["declared"] = {"tie_tol": TIE_TOL, "mono_tol": MONO_TOL,
                          "closed_tol": CLOSED_TOL,
                          "flip_tol": FLIP_TOL,
                          "bars": {"H1_flip_k2": 0.5},
                          "correction":
                              "declared MI tie count 3, GD-2's 6 "
                              "double-counted each 2-cell "
                              "partition from both cells"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "gd2b-budget-flip-game.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("ensemble", ens)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
