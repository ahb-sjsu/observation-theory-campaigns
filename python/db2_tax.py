#!/usr/bin/env python3
"""DB-2: the multi-consumer alignment tax for shared precision budgets.

Track DB (DATABASE-TRACK.md), EC-6 transplanted to physical design.
Modes: pilotA | pilotB | governed (refuses until GATES frozen).
DuckDB-local, deterministic. Coordination boundary binding (track §0):
no routing/freshness/fleet claims.

Question: two consumers read a table through planted supports at
controlled OVERLAP (the discrete analogue of EC-6's principal angle).
One precision budget (4 of 8 columns fine) must serve both. The
alignment tax is

  tax(o) = max_i loss_i(shared-BEST) / max_i loss_i(utopia_i)

where shared-BEST is the exhaustively optimal single allocation for
the egalitarian worst-of-two (all C(8,4)=70 subsets evaluated — no
heuristic gap), and utopia_i gives consumer i the whole budget
(exhaustive best-for-i). Overlap levels: o = 4 (identical), 2, 1, 0
(disjoint); support_A = {0,1,2,3} fixed; support_B(o) = {0..o-1} ∪
{4..7-o+ ...} per the table in code.

Predictions (EC-6 shape): tax(4) ≈ 1 (sharing free when geometries
coincide); tax rises as overlap falls; tax(0) materially > 1; and the
consumer-AWARE shared allocation beats a task-blind shared baseline
(mean over 4 seed-drawn subsets distinct from shared-best and both
utopias) pooled on worst-of-two.

Design: n = 10,000 rows, d = 8, m = 150 query rows, k = 25; per
overlap level, N_INST = 5 seeded instances (fresh coefficient draws +
fresh targets); consumer i's target y_i = sum_{p in S_i} c_p x_p +
0.5 * x_{s0} x_{s1} + noise(0.5); loss = k-NN report MSE vs noiseless
truth (as DB-1).

Seeds: pilotA = 20261210; pilotB = 20261212; governed = 20261215.
"""
import itertools
import json
import pathlib
import sys

import duckdb
import numpy as np

N_ROWS = 10000
M_QUERY = 150
D = 8
K_NN = 25
F_FINE = 4
N_INST = 5
N_RAND = 4
NOISE = 0.5
OVERLAPS = [4, 2, 1, 0]
SUPPORT_A = [0, 1, 2, 3]
SUPPORT_B = {4: [0, 1, 2, 3], 2: [0, 1, 4, 5], 1: [0, 4, 5, 6], 0: [4, 5, 6, 7]}
SEEDS = {"pilotA": 20261210, "pilotB": 20261212, "governed": 20261215}

# Frozen only from >= 2 independent powered draws. GATE RESPEC after
# pilot A (disclosed): the EC-6 "monotone in angle" prediction used
# overlap COUNT as the angle measure, and pilot A refuted that
# parameterization on this substrate — partial overlaps price HIGHER
# (1.070/1.076) than disjoint (1.055) because both consumers'
# interaction terms contend for the same high-value columns at
# partial overlap. The tax tracks VALUE-WEIGHTED alignment, not
# set-overlap count (which is OT's own claim, sharpened). T2/T3 are
# respecified to pooled/min forms over non-identical overlaps; the
# non-monotonicity is reported as a disclosed finding, never gated.
# Frozen 2026-08-21 from the ACROSS-DRAW calibration of two powered
# draws (pilotA seed 20261210 / pilotB seed 20261212): T1 1.0000
# both (sharing exactly free at identity, both draws); T2 mean
# non-identical 1.0669/1.0705; T3 min non-identical 1.0550/1.0537;
# T4 0.2321/0.2169; determinism true; 2820 eval runs both. The
# non-monotonicity in overlap COUNT replicated across draws (o=1 >
# o=0 in both) — the value-weighted-alignment finding is stable and
# stays a reported diagnostic.
GATES = {
    "T1_tax_identical_max": 1.02,          # sharing free at identity
    "T2_tax_nonidentical_mean_min": 1.03,  # mean tax over o in {2,1,0}
    "T3_tax_nonidentical_min_min": 1.02,   # min cell-mean tax over o in {2,1,0}
    "T4_aware_vs_blind_pooled_min": 0.10,  # worst-of-two improvement
    "T5_determinism_bitwise": True,
    "T6_eval_runs_expected": 2820,
}


def _df(X, y, qid=False):
    import pandas as pd
    d = {f"x{i}": X[:, i] for i in range(D)}
    if qid:
        d["qid"] = np.arange(len(X))
    else:
        d["y"] = y
        d["rid"] = np.arange(len(X))
    return pd.DataFrame(d)


def knn_loss(con, cols_fine, Xs, Xq, y_store, y_true_q, ledger):
    mask = np.isin(np.arange(D), list(cols_fine))[None, :]
    enc_s = np.where(mask, Xs, np.round(Xs))
    enc_q = np.where(mask, Xq, np.round(Xq))
    con.execute("DROP TABLE IF EXISTS store; DROP TABLE IF EXISTS q")
    con.register("store_df", _df(enc_s, y_store))
    con.register("q_df", _df(enc_q, None, qid=True))
    con.execute("CREATE TABLE store AS SELECT * FROM store_df")
    con.execute("CREATE TABLE q AS SELECT * FROM q_df")
    dist = " + ".join(f"(q.x{i}-s.x{i})*(q.x{i}-s.x{i})" for i in range(D))
    sql = f"""
      SELECT qid, AVG(y) AS report FROM (
        SELECT q.qid, s.y,
               ROW_NUMBER() OVER (PARTITION BY q.qid ORDER BY {dist}, s.rid) AS rn
        FROM q CROSS JOIN store s)
      WHERE rn <= {K_NN} GROUP BY qid ORDER BY qid
    """
    rep = con.execute(sql).fetchnumpy()["report"]
    ledger["eval_runs"] += 1
    return float(np.mean((rep - y_true_q) ** 2))


def make_target(rng, support, Xs, Xq):
    c = rng.uniform(0.5, 1.5, size=len(support))
    def f(X):
        base = sum(ci * X[:, p] for ci, p in zip(c, support))
        return base + 0.5 * X[:, support[0]] * X[:, support[1]]
    y_store = f(Xs) + NOISE * rng.standard_normal(len(Xs))
    return y_store, f(Xq)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "pilotA"
    assert mode in SEEDS
    if mode == "governed" and any(v is None for v in GATES.values()):
        raise SystemExit("GATES not frozen; refusing to run governed mode before seal.")
    seed = SEEDS[mode]
    rng = np.random.default_rng(seed)
    rand_rng = np.random.default_rng(seed + 7)
    con = duckdb.connect(":memory:")
    ledger = {"eval_runs": 0}
    subsets = [tuple(sorted(s)) for s in itertools.combinations(range(D), F_FINE)]

    cells = {}
    for o in OVERLAPS:
        SB = SUPPORT_B[o]
        inst_rows = []
        for inst in range(N_INST):
            Xs = rng.standard_normal((N_ROWS, D))
            Xq = rng.standard_normal((M_QUERY, D))
            yA_s, yA_q = make_target(rng, SUPPORT_A, Xs, Xq)
            yB_s, yB_q = make_target(rng, SB, Xs, Xq)
            # exhaustive: every 4-subset's loss for each consumer
            LA, LB = {}, {}
            for s in subsets:
                LA[s] = knn_loss(con, set(s), Xs, Xq, yA_s, yA_q, ledger)
                LB[s] = knn_loss(con, set(s), Xs, Xq, yB_s, yB_q, ledger)
            utopiaA = min(LA.values())
            utopiaB = min(LB.values())
            shared_best_s = min(subsets, key=lambda s: max(LA[s], LB[s]))
            w_shared = max(LA[shared_best_s], LB[shared_best_s])
            w_utopia = max(utopiaA, utopiaB)
            tax = w_shared / w_utopia
            # task-blind baseline: 4 seed-drawn subsets distinct from
            # shared-best and both utopia argmins, pairwise distinct
            forbidden = {shared_best_s,
                         min(subsets, key=lambda s: LA[s]),
                         min(subsets, key=lambda s: LB[s])}
            blind = []
            while len(blind) < N_RAND:
                cand = tuple(sorted(rand_rng.choice(D, F_FINE, replace=False).tolist()))
                if cand not in forbidden:
                    forbidden.add(cand)
                    blind.append(cand)
            w_blind = float(np.mean([max(LA[s], LB[s]) for s in blind]))
            aware_vs_blind = 1.0 - w_shared / w_blind
            # determinism instrument on the shared-best cell
            redo = knn_loss(con, set(shared_best_s), Xs, Xq, yA_s, yA_q, ledger)
            det = (redo == LA[shared_best_s])
            inst_rows.append({"tax": tax, "w_shared": w_shared,
                              "w_utopia": w_utopia, "w_blind_mean4": w_blind,
                              "aware_vs_blind": aware_vs_blind,
                              "shared_best": list(shared_best_s),
                              "deterministic": bool(det)})
            print(f"[o={o} inst={inst}] tax {tax:.4f} aware_vs_blind "
                  f"{aware_vs_blind:+.4f} shared_best={list(shared_best_s)}",
                  flush=True)
        cells[str(o)] = {
            "mean_tax": round(float(np.mean([r["tax"] for r in inst_rows])), 4),
            "instances": inst_rows,
        }

    tax4 = cells["4"]["mean_tax"]
    nonid = [cells[str(o)]["mean_tax"] for o in OVERLAPS if o != 4]
    pooled_aware = float(np.mean(
        [r["aware_vs_blind"] for o in OVERLAPS for r in cells[str(o)]["instances"]]))
    agg = {
        "tax_by_overlap": {o: cells[str(o)]["mean_tax"] for o in OVERLAPS},
        "T1_tax_identical": tax4,
        "T2_tax_nonidentical_mean": round(float(np.mean(nonid)), 4),
        "T3_tax_nonidentical_min": round(float(np.min(nonid)), 4),
        "T4_aware_vs_blind_pooled": round(pooled_aware, 4),
        "monotonicity_in_overlap_count_DIAGNOSTIC": bool(
            cells["2"]["mean_tax"] <= cells["1"]["mean_tax"] <= cells["0"]["mean_tax"]),
        "deterministic_all": bool(all(r["deterministic"]
                                      for o in OVERLAPS for r in cells[str(o)]["instances"])),
    }
    verdicts = None
    if mode == "governed":
        verdicts = {
            "T1": agg["T1_tax_identical"] <= GATES["T1_tax_identical_max"],
            "T2": agg["T2_tax_nonidentical_mean"] >= GATES["T2_tax_nonidentical_mean_min"],
            "T3": agg["T3_tax_nonidentical_min"] >= GATES["T3_tax_nonidentical_min_min"],
            "T4": agg["T4_aware_vs_blind_pooled"] >= GATES["T4_aware_vs_blind_pooled_min"],
            "T5": agg["deterministic_all"] == GATES["T5_determinism_bitwise"],
            "T6": ledger["eval_runs"] == GATES["T6_eval_runs_expected"],
        }
        verdicts["ALL"] = bool(all(verdicts.values()))

    out = {"campaign": "DB-2 multi-consumer alignment tax for shared precision budgets",
           "mode": mode,
           "disclosure": ("DISCLOSED CALIBRATION PILOT" if mode != "governed"
                          else "GOVERNED RUN at the sealed seed"),
           "seed": int(seed),
           "config": {"n": N_ROWS, "m": M_QUERY, "d": D, "k": K_NN,
                      "f_fine": F_FINE, "n_inst": N_INST, "noise": NOISE,
                      "overlaps": OVERLAPS, "support_A": SUPPORT_A,
                      "support_B": SUPPORT_B},
           "cells": cells, "aggregate": agg,
           "gates": GATES if mode == "governed" else None,
           "verdicts": verdicts, "ledger": ledger}
    path = pathlib.Path(__file__).resolve().parent.parent / "results" / f"db2-{mode}.json"
    path.write_text(json.dumps(out, indent=2))
    print(json.dumps({"aggregate": agg, "verdicts": verdicts,
                      "ledger": ledger}, indent=2))
    print("written:", path)


if __name__ == "__main__":
    main()
