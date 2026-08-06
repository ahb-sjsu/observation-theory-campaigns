#!/usr/bin/env python3
"""GD-2 the budget flip in a game (exploratory, GD track).

Protocol declared in GAMES-DECISIONS-TRACK.md before this run. A
player buys a deterministic coarsening of six hidden states under a
cell budget, publicly, then plays a simultaneous zero-sum game
against an uninformed adversary with two actions. The game value is
exact, best response to the adversary's mixture is per-cell greedy,
so the value is the minimum over q in [0, 1] of a convex
piecewise-linear function, found by enumerating line crossings. The
stake-game exhibit has declared rational closed forms, the
fidelity-optimal budget spend buys exactly nothing. Verdict computed
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

from projection_fold import canonical_sha256  # noqa: E402

TIE_TOL = 1e-12
MONO_TOL = 1e-10
CLOSED_TOL = 1e-12
FLIP_TOL = 1e-6


def set_partitions(elems):
    if not elems:
        yield []
        return
    first, rest = elems[0], elems[1:]
    for p in set_partitions(rest):
        for i in range(len(p)):
            yield p[:i] + [p[i] + [first]] + p[i + 1:]
        yield [[first]] + p


def game_value(prior, payoff, partition) -> float:
    """Exact zero-sum value, player two mixes over two actions."""
    m1 = payoff.shape[1]
    cells = []
    qs = {0.0, 1.0}
    for cell in partition:
        c = np.zeros((m1, 2))
        for s in cell:
            c += prior[s] * payoff[s]
        # line for action a: L(q) = c[a,1] + q (c[a,0] - c[a,1])
        d = c[:, 0] - c[:, 1]
        for a in range(m1):
            for a2 in range(a + 1, m1):
                den = d[a] - d[a2]
                if abs(den) > 1e-15:
                    q = (c[a2, 1] - c[a, 1]) / den
                    if 0.0 < q < 1.0:
                        qs.add(float(q))
        cells.append(c)
    best = np.inf
    for q in qs:
        f = sum(float(np.max(c[:, 1] + q * (c[:, 0] - c[:, 1])))
                for c in cells)
        best = min(best, f)
    return best


def cell_entropy_bits(prior, partition) -> float:
    masses = [sum(prior[s] for s in cell) for cell in partition]
    return float(-sum(m * np.log2(m) for m in masses if m > 0))


def analyze(prior, payoff, parts, budgets):
    """Per budget, task-optimal value and best-valued MI-argmax."""
    values = [game_value(prior, payoff, p) for p in parts]
    ents = [cell_entropy_bits(prior, p) for p in parts]
    ncells = [len(p) for p in parts]
    finest_v = values[ncells.index(max(ncells))]
    out = {}
    for k in budgets:
        idx = [i for i in range(len(parts)) if ncells[i] <= k]
        v_task = max(values[i] for i in idx)
        h_max = max(ents[i] for i in idx)
        mi_arg = [i for i in idx if ents[i] > h_max - TIE_TOL]
        v_fid = max(values[i] for i in mi_arg)
        out[k] = {"v_task": v_task, "v_fid_best": v_fid,
                  "h_max_bits": h_max, "n_mi_ties": len(mi_arg),
                  "flip": v_task - v_fid}
    return out, values, finest_v


def main() -> int:
    record: dict = {"schema": "gd2-budget-flip-game-v1",
                    "label": "exploratory"}
    parts = list(set_partitions(list(range(6))))
    assert len(parts) == 203

    # the stake game exhibit
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
          and ex[2]["n_mi_ties"] == 6)
    record["exhibit"] = {
        "per_budget": {str(k): {kk: (float(vv) if not
                                     isinstance(vv, int) else vv)
                                for kk, vv in ex[k].items()}
                       for k in ex},
        "closed_forms": {k: {"measured": float(m), "declared": c}
                         for k, (m, c) in closed.items()},
        "flip_k2": float(ex[2]["flip"]),
        "items": {"H1": bool(h1), "H2": bool(h2), "C1": bool(c1),
                  "C2": bool(c2), "C3": bool(c3), "C4": bool(c4)}}
    print("exhibit flip", ex[2]["flip"], "ties", ex[2]["n_mi_ties"],
          {k: v for k, v in record["exhibit"]["items"].items()})

    # ensemble
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
        if (g + 1) % 50 == 0:
            print(f"  ensemble {g + 1}/{n_games}", flush=True)
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
    print("ensemble", ens)

    items = record["exhibit"]["items"]
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["declared"] = {"tie_tol": TIE_TOL, "mono_tol": MONO_TOL,
                          "closed_tol": CLOSED_TOL,
                          "flip_tol": FLIP_TOL,
                          "bars": {"H1_flip_k2": 0.5}}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "gd2-budget-flip-game.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
