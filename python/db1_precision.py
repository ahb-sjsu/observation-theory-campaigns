#!/usr/bin/env python3
"""DB-1: per-column precision allocation by probed consumer sensitivity
(quantize-the-unread as physical design). Track DB, design-draft stage.

Modes: pilotA | pilotB (disclosed powered calibration draws) | governed
(sealed seed; refuses until GATES frozen). Substrate: DuckDB, local,
fully deterministic at the seed (EC-grade reproducibility; negligible
power; no gateway).

Coordination boundary (binding, see DATABASE-TRACK.md §0): this
campaign claims nothing about replica routing, freshness certificates,
replication, or fleets (ceded to the concurrent network-governor
XPROTO-GEO program). The decision variable here is per-column STORAGE
PRECISION at a matched budget; the only "staleness" is quantization
error.

Design:
  n = 20,000 rows, d = 8 columns x1..x8 ~ N(0,1) seeded. External
  targets (never stored coarsely; the ground truth an owner cares
  about): y_A = x1 + x2^2 - x3 + noise(0.5), reading subset {1,2,3};
  y_B = x5 * x6 + noise(0.5), reading subset {5,6}.
  Consumers: SQL k-NN report programs (k = 25) over ALL stored encoded
  columns — irrelevant columns dilute the similarity metric, which is
  exactly why coarsening them can HELP. For each of m = 200 held-out
  query rows, the consumer reports the neighbour-mean target; loss =
  MSE against the true target.
  Encoding ladder: fine = raw double; coarse = ROUND(x) (step 1.0,
  quantization std ~0.29). Budget = exactly F = 4 of 8 columns fine.
  Probe (query-only, cost logged): coarsen ONE column, re-run each
  consumer, delta-loss vs all-fine = probed sensitivity diag.
  Arms at matched budget (CRN exact — same rows, same queries):
  aligned (top-4 by probed delta), oracle (planted subset padded by
  probed delta), anti (bottom-4), random1..4 (LM2-002 degeneracy-proof
  task-blind baseline: seed-drawn, none equal to aligned/oracle,
  pairwise distinct), references all-coarse / all-fine.

Seeds: pilotA = 20261201; pilotB = 20261203; governed = 20261205.
"""
import json
import pathlib
import sys

import duckdb
import numpy as np

N_ROWS = 20000
M_QUERY = 200
D = 8
K_NN = 25
F_FINE = 4
N_RAND = 4
NOISE = 0.5
SEEDS = {"pilotA": 20261201, "pilotB": 20261203, "governed": 20261205}

# Frozen 2026-08-21 from two independent powered draws (pilotA seed
# 20261201: pooled Q1 0.2228, cells 0.3026/0.1431, anti -0.2031;
# pilotB seed 20261203: pooled Q1 0.1809, cells 0.1590/0.2028, anti
# -0.4178; capture 1.0000 in all four cells — the probe recovered the
# planted supports EXACTLY, so aligned == oracle and Q2 is
# near-vacuous, retained at the program-standard bar). Q4
# (quantize-the-unread) is DEMOTED to an ungated diagnostic: pooled
# +0.0009/-0.0272, sign-varying per cell — at step-1.0 coarsening the
# effect is a SCOPED NEGATIVE (coarse ~ free, not prophylactic); the
# step is NOT retuned to chase the headline (bar-shopping).
GATES = {
    "Q1_aligned_vs_baseline_pooled_min": 0.10,
    "Q1b_per_consumer_floor": 0.05,
    "Q2_capture_pooled_min": 0.60,
    "Q3_anti_vs_baseline_pooled_max": 0.10,
    "Q5_determinism_bitwise": True,
    "Q6_probe_runs_expected": 16,
}

CONSUMERS = {
    "A": {"support": [0, 1, 2],
          "f": lambda X: X[:, 0] + X[:, 1] ** 2 - X[:, 2]},
    "B": {"support": [4, 5],
          "f": lambda X: X[:, 4] * X[:, 5]},
}


def knn_loss(con, cols_fine, Xs, Xq, y_store, y_true_q):
    """Run the consumer as a SQL program over the encoded store; return
    MSE of the k-NN neighbour-mean report against the true targets."""
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
    return float(np.mean((rep - y_true_q) ** 2))


def _df(X, y, qid=False):
    import pandas as pd
    d = {f"x{i}": X[:, i] for i in range(D)}
    if qid:
        d["qid"] = np.arange(len(X))
    else:
        d["y"] = y
        d["rid"] = np.arange(len(X))
    return pd.DataFrame(d)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "pilotA"
    assert mode in SEEDS
    if mode == "governed" and any(v is None for v in GATES.values()):
        raise SystemExit("GATES not frozen; refusing to run governed mode before seal.")
    seed = SEEDS[mode]
    rng = np.random.default_rng(seed)
    Xs = rng.standard_normal((N_ROWS, D))
    Xq = rng.standard_normal((M_QUERY, D))
    rand_rng = np.random.default_rng(seed + 7)

    con = duckdb.connect(":memory:")
    out = {"campaign": "DB-1 precision allocation by probed consumer sensitivity",
           "mode": mode,
           "disclosure": ("DISCLOSED CALIBRATION PILOT" if mode != "governed"
                          else "GOVERNED RUN at the sealed seed"),
           "seed": int(seed), "config": {"n": N_ROWS, "m": M_QUERY, "d": D,
                                         "k": K_NN, "f_fine": F_FINE,
                                         "noise": NOISE, "coarse_step": 1.0},
           "consumers": {}, "ledger": {"probe_runs": 0, "eval_runs": 0}}

    metrics = {}
    for cid, spec in CONSUMERS.items():
        y_store = spec["f"](Xs) + NOISE * rng.standard_normal(N_ROWS)
        y_true_q = spec["f"](Xq)  # the noiseless truth at the query rows

        allfine = set(range(D))
        loss_allfine = knn_loss(con, allfine, Xs, Xq, y_store, y_true_q)
        out["ledger"]["eval_runs"] += 1
        # probe: coarsen one column at a time (query-only; cost logged)
        deltas = []
        for i in range(D):
            li = knn_loss(con, allfine - {i}, Xs, Xq, y_store, y_true_q)
            out["ledger"]["probe_runs"] += 1
            deltas.append(li - loss_allfine)
        order = sorted(range(D), key=lambda i: -deltas[i])
        aligned = sorted(order[:F_FINE])
        anti = sorted(order[-F_FINE:])
        osup = list(spec["support"])
        osup += [i for i in order if i not in osup][: F_FINE - len(osup)]
        oracle = sorted(osup[:F_FINE])
        forbidden = {tuple(aligned), tuple(oracle)}
        rand_sets = []
        while len(rand_sets) < N_RAND:
            cand = tuple(sorted(rand_rng.choice(D, F_FINE, replace=False).tolist()))
            if cand not in forbidden:
                forbidden.add(cand)
                rand_sets.append(list(cand))

        arms = {"aligned": aligned, "oracle": oracle, "anti": anti,
                "allcoarse": [], "allfine": list(range(D))}
        for ri, rs in enumerate(rand_sets):
            arms[f"random{ri+1}"] = rs
        losses = {}
        for arm, fine in arms.items():
            losses[arm] = knn_loss(con, set(fine), Xs, Xq, y_store, y_true_q)
            out["ledger"]["eval_runs"] += 1
        # determinism instrument: recompute the aligned arm, must be bitwise
        redo = knn_loss(con, set(aligned), Xs, Xq, y_store, y_true_q)
        deterministic = (redo == losses["aligned"])

        base = float(np.mean([losses[f"random{r+1}"] for r in range(N_RAND)]))
        impr_aligned = 1.0 - losses["aligned"] / base
        impr_anti = 1.0 - losses["anti"] / base
        gap_oracle = base - losses["oracle"]
        capture = ((base - losses["aligned"]) / gap_oracle) if gap_oracle > 0 else None
        impr_vs_allfine = 1.0 - losses["aligned"] / losses["allfine"]

        metrics[cid] = {
            "probed_deltas": [round(x, 6) for x in deltas],
            "arms": {k: v for k, v in arms.items()},
            "loss_by_arm": {k: round(v, 6) for k, v in losses.items()},
            "baseline_mean4": round(base, 6),
            "impr_aligned_vs_baseline": round(impr_aligned, 4),
            "impr_anti_vs_baseline": round(impr_anti, 4),
            "capture_of_oracle": (round(capture, 4) if capture is not None else None),
            "impr_aligned_vs_allfine": round(impr_vs_allfine, 4),
            "deterministic_recompute": bool(deterministic),
        }
        print(f"[{cid}] aligned={aligned} oracle={oracle} anti={anti} "
              f"| impr {impr_aligned:+.4f} capture "
              f"{capture if capture is not None else float('nan'):.4f} "
              f"vs-allfine {impr_vs_allfine:+.4f}", flush=True)

    pooled = {
        "Q1_aligned_vs_baseline": round(float(np.mean(
            [metrics[c]["impr_aligned_vs_baseline"] for c in metrics])), 4),
        "Q2_capture": round(float(np.mean(
            [metrics[c]["capture_of_oracle"] for c in metrics
             if metrics[c]["capture_of_oracle"] is not None])), 4),
        "Q3_anti_vs_baseline": round(float(np.mean(
            [metrics[c]["impr_anti_vs_baseline"] for c in metrics])), 4),
        "Q4_aligned_vs_allfine": round(float(np.mean(
            [metrics[c]["impr_aligned_vs_allfine"] for c in metrics])), 4),
    }
    verdicts = None
    if mode == "governed":
        verdicts = {
            "Q1": pooled["Q1_aligned_vs_baseline"] >= GATES["Q1_aligned_vs_baseline_pooled_min"],
            "Q1b": all(metrics[c]["impr_aligned_vs_baseline"] >= GATES["Q1b_per_consumer_floor"] for c in metrics),
            "Q2": pooled["Q2_capture"] >= GATES["Q2_capture_pooled_min"],
            "Q3": pooled["Q3_anti_vs_baseline"] <= GATES["Q3_anti_vs_baseline_pooled_max"],
            "Q5": all(metrics[c]["deterministic_recompute"] for c in metrics) == GATES["Q5_determinism_bitwise"],
            "Q6": out["ledger"]["probe_runs"] == GATES["Q6_probe_runs_expected"],
        }
        verdicts["ALL"] = bool(all(verdicts.values()))
        # Q4 (quantize-the-unread) is reported in pooled/diagnostics,
        # never gated — pilot-calibrated scoped negative at this step.

    out["consumers"] = metrics
    out["pooled"] = pooled
    out["gates"] = GATES if mode == "governed" else None
    out["verdicts"] = verdicts
    path = pathlib.Path(__file__).resolve().parent.parent / "results" / f"db1-{mode}.json"
    path.write_text(json.dumps(out, indent=2))
    print(json.dumps({"pooled": pooled, "verdicts": verdicts,
                      "ledger": out["ledger"]}, indent=2))
    print("written:", path)


if __name__ == "__main__":
    main()
