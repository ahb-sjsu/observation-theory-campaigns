#!/usr/bin/env python3
"""DB-3: directional optimizer-statistics refresh (advanced-DB survey flagship F3).

Runs ON Atlas against the project-owned PostgreSQL 16 cluster
(localhost:5544, autovacuum off, data /home/claude/db3_pg — system
cluster on 5432 untouched).

Question: when ANALYZE budget is scarce (k=1 table/epoch), does
allocating it by a probed plan-sensitivity signal (which tables'
refresh would actually change the optimizer's plans for the live
workload) beat the industrial churn baseline (modification counters),
age, and random at matched count — and beat even a DOUBLE-budget
churn arm (churn2, k=2), which settles probe-cost accounting under
any charging scheme?

Substrate (v2, 200k rows — the 20k v1 pilots were INVALID: fully
cached tiny tables execute misestimated nested loops faster than the
"fresh" hash plans, the none-arm beat the referee in both draws, and
the endpoint measured cost-model miscalibration, not staleness):
  12 tables x 200k rows.
  t00..t03  workload-relevant, drifting predicate column `a`
            (~10%/epoch churn that SHIFTS the distribution)
  t04..t07  workload-relevant, churning but distribution-stable
            (~5%/epoch, `a` redrawn from the SAME distribution)
  t08..t11  not in the workload, LOUDEST churn (~20%/epoch pad only)
So modification counters rank t08..t11 first — the churn baseline is
fooled exactly where counters and plan-impact diverge.

Endpoint (v2): DIRECT total workload latency per arm per epoch
(median-of-5 per query, summed) under CRN — identical data trajectory
per seed for every arm. No referee in the endpoint: v1's
regret-vs-fresh-referee assumed the cost model ranks plans correctly
in wall time, which 20k-scale falsified. A budget-unlimited `fresh`
arm (ANALYZE all, every epoch) is the reference ceiling and `none`
the floor; staleness-matters is a GATE (none materially worse), not
an assumption.

Probe (directional arm, cost logged per epoch; churn2 dominates any
charging dispute):
  per footprint table: BEGIN; SET LOCAL default_statistics_target=10;
  ANALYZE t_i; canonical per-predicate count(*) re-EXPLAIN; score =
  sum |log row-estimate shift| on the probed table's own scan nodes;
  ROLLBACK. (Probing the workload queries themselves is an artifact
  trap — coarse stats spuriously flip join plans; shakedown v1.)

Executed latency on a live host -> logged-response posture (LM-track
precedent): raw per-rep timings are the artifact; instrument gate =
per-query repeat spread. ANALYZE at FULL_TARGET samples >= N_ROWS
rows (full read), so refresh stats are deterministic.

Modes:
  shakedown            mechanics + regime validation (no arms)
  pilot <seed>         full multi-arm run, disclosed
  governed <seed>      identical code path; run only after seal
Output: /home/claude/db3_results/db3_<mode>_<seed>.json
"""

import hashlib
import json
import os
import sys
import time
from io import StringIO

import numpy as np
import psycopg2

DSN = dict(host="localhost", port=5544, user="claude", dbname="db3")

N_TABLES = 12
N_ROWS = 200_000
B_RANGE = N_ROWS // 10        # join-key fanout ~10: the NL/hash flip zone
DRIFT = [0, 1, 2, 3]          # relevant + distribution-shifting
STABLE = [4, 5, 6, 7]         # relevant, churn without shift
IRRELEVANT = [8, 9, 10, 11]   # not queried, loud churn
EPOCHS = 30
# v4 (final design): k=1 — REAL scarcity. The v3 pilots (k=3 vs 4
# relevant tables) showed +12% staleness cost but no separation among
# refresh policies: any policy touched the drift tables often enough.
# Scarcity is what the hypothesis is about. churn2 (k=2) is the
# double-budget control that closes the probe-cost accounting: if
# directional-k1 (+probes) beats churn-k2, it wins under any charging.
K_BASE = 1                    # refreshes/epoch: churn, age, random
K_DIR = 1                     # directional: matched count, probe cost logged
K_CHURN2 = 2                  # churn2: double-budget control
PROBE_TARGET = 10
FULL_TARGET = 1000            # 300*1000 >= 200k -> full-read, deterministic
TIMED_REPS = 5
MODE_START = 650.0
MODE_STEP = (-35.0, 12.0)     # mean, sd of the seeded mode walk
PAD = "x" * 240
ARMS = ["directional", "churn", "churn2", "age", "random", "none", "fresh"]

# Predicate window the drift mode walks THROUGH (~epochs 11-16)
WIN = "a BETWEEN 180 AND 240"      # 6% under the initial uniform

# Workload: one-side-filtered joins only. Both-sides-filtered joins
# (the v2 QD family) are EXCLUDED as uncalibratable: two rpc sweeps
# (db3_calibration.json) showed no random_page_cost at which the
# planner given correct statistics picks the actually-fastest plan
# for both join shapes (QJ truth-unbiased at rpc>=0.9, QD only at
# rpc<=0.8) — a planner cost-model limitation, documented in
# DATABASE-TRACK.md s8.3. At rpc=1.1 the QJ family is verified
# truth-unbiased (fresh beats stale +39..+61 ms at transit).
QUERIES = {}  # name -> (sql, tables touched)
for i in DRIFT:
    QUERIES[f"QJ{i}"] = (
        f"SELECT count(*), COALESCE(sum(y.b),0) FROM t{i:02d} x "
        f"JOIN t{i+4:02d} y ON x.b = y.b WHERE x.{WIN}",
        [i, i + 4],
    )
    QUERIES[f"QS{i}"] = (
        f"SELECT COALESCE(sum(b),0) FROM t{i:02d} WHERE {WIN}",
        [i],
    )
QUERIES["QC4"] = (f"SELECT count(*) FROM t04 WHERE {WIN}", [4])
# Cross-pair joins onto different stable partners: more flip-capable
# load-bearing forms in the calibrated one-side-filtered shape.
for qa, qb in [(0, 5), (1, 6), (2, 7), (3, 4)]:
    QUERIES[f"QX{qa}{qb}"] = (
        f"SELECT count(*), COALESCE(sum(y.b),0) FROM t{qa:02d} x "
        f"JOIN t{qb:02d} y ON x.b = y.b WHERE x.{WIN}",
        [qa, qb],
    )

# Consumer footprint for the directional probe: the workload's
# predicates on each table. Tables carrying no workload predicate have
# zero consumer footprint — the directional arm never probes them.
PROBE_PREDS = {0: [WIN], 1: [WIN], 2: [WIN], 3: [WIN], 4: [WIN]}


def connect():
    conn = psycopg2.connect(**DSN)
    conn.autocommit = True
    return conn


def build(conn, seed):
    """Deterministic rebuild: identical data for every arm (CRN)."""
    rng = np.random.default_rng(seed)
    cur = conn.cursor()
    # SSD-realistic planner costing (default random_page_cost=4 never
    # flips plans at these selectivities); roomy work_mem so hash joins
    # don't batch-spill and timing stays clean.
    cur.execute("ALTER SYSTEM SET random_page_cost = 1.1")
    cur.execute("ALTER SYSTEM SET work_mem = '64MB'")
    cur.execute("SELECT pg_reload_conf()")
    for i in range(N_TABLES):
        t = f"t{i:02d}"
        cur.execute(f"DROP TABLE IF EXISTS {t}")
        cur.execute(
            f"CREATE TABLE {t} (id int PRIMARY KEY, a int NOT NULL, "
            f"b int NOT NULL, pad text NOT NULL)"
        )
        a = rng.integers(0, 1000, N_ROWS)
        b = rng.integers(0, B_RANGE, N_ROWS)
        rows = "\n".join(
            f"{j}\t{a[j]}\t{b[j]}\t{PAD}" for j in range(N_ROWS)
        )
        cur.copy_expert(f"COPY {t} FROM STDIN", StringIO(rows))
        cur.execute(f"CREATE INDEX ON {t} (a)")
        # b-index everywhere: gives the planner the nested-loop path,
        # whose misuse under stale estimates is the regret mechanism
        cur.execute(f"CREATE INDEX ON {t} (b)")
        cur.execute(f"SET default_statistics_target = {FULL_TARGET}")
        cur.execute(f"ANALYZE {t}")  # all arms start with fresh stats
    cur.close()


def bulk_update(cur, table, col, ids, vals):
    """Set col=val for id in ids via a COPYed temp table (a VALUES list
    with tens of thousands of tuples is slow to parse at 200k scale)."""
    cur.execute("DROP TABLE IF EXISTS upd_tmp")
    cur.execute("CREATE TEMP TABLE upd_tmp (id int, v int)")
    payload = "\n".join(f"{int(i)}\t{int(v)}" for i, v in zip(ids, vals))
    cur.copy_expert("COPY upd_tmp FROM STDIN", StringIO(payload))
    cur.execute(
        f"UPDATE {table} t SET {col} = u.v FROM upd_tmp u WHERE t.id = u.id")


def drift_step(conn, rng, modes):
    """One epoch of seeded churn. Returns rows modified per table.
    Update-set sizes are binomial: exact constant sizes create
    artificial ties in the churn ranking; real counters jitter."""
    cur = conn.cursor()
    nmod = {}
    for i in DRIFT:  # ~10% of rows, values pulled toward the walking mode
        modes[i] = float(np.clip(modes[i] + rng.normal(*MODE_STEP), 40, 950))
        n = int(rng.binomial(N_ROWS, 0.10))
        ids = rng.choice(N_ROWS, n, replace=False)
        vals = np.clip(rng.normal(modes[i], 45, n), 0, 999).astype(int)
        bulk_update(cur, f"t{i:02d}", "a", ids, vals)
        nmod[i] = n
    for i in STABLE:  # ~5% churn, a redrawn from the ORIGINAL distribution
        n = int(rng.binomial(N_ROWS, 0.05))
        ids = rng.choice(N_ROWS, n, replace=False)
        vals = rng.integers(0, 1000, n)
        bulk_update(cur, f"t{i:02d}", "a", ids, vals)
        nmod[i] = n
    for i in IRRELEVANT:  # ~20% churn, pad only — loud counters, no plan impact
        n = int(rng.binomial(N_ROWS, 0.20))
        lo = int(rng.integers(0, N_ROWS - n))
        cur.execute(
            f"UPDATE t{i:02d} SET pad = pad WHERE id BETWEEN {lo} "
            f"AND {lo + n - 1}")
        nmod[i] = n
    cur.execute("SELECT pg_stat_force_next_flush()")
    cur.close()
    return nmod


def plan_hash_cost(cur, sql):
    """Returns (structure hash, total cost, {relation: est scan rows})."""
    cur.execute("EXPLAIN (FORMAT JSON) " + sql)
    plan = cur.fetchone()[0][0]["Plan"]
    rows_by_rel = {}

    def skel(n):
        rel = n.get("Relation Name")
        if rel:
            rows_by_rel[rel] = rows_by_rel.get(rel, 0.0) + float(
                n.get("Plan Rows", 0))
        keep = {k: n.get(k) for k in
                ("Node Type", "Relation Name", "Index Name", "Join Type",
                 "Parent Relationship", "Scan Direction")}
        keep["children"] = [skel(c) for c in n.get("Plans", [])]
        return keep

    h = hashlib.sha256(
        json.dumps(skel(plan), sort_keys=True).encode()
    ).hexdigest()[:16]
    return h, float(plan["Total Cost"]), rows_by_rel


def timed_exec(cur, sql, reps=TIMED_REPS):
    cur.execute(sql)
    cur.fetchall()  # warm
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter()
        cur.execute(sql)
        cur.fetchall()
        ts.append((time.perf_counter() - t0) * 1000.0)
    return float(np.median(ts)), ts


def probe_scores(conn):
    """Canonical-selectivity rollback probes on the consumer footprint."""
    scores = {i: 0.0 for i in range(N_TABLES)}
    t0 = time.perf_counter()
    with connect() as c2:
        c2.autocommit = False
        cur = c2.cursor()
        for i, preds in PROBE_PREDS.items():
            t = f"t{i:02d}"
            probes = [f"SELECT count(*) FROM {t} WHERE {p}" for p in preds]
            before = []
            for sql in probes:
                _, _, rows = plan_hash_cost(cur, sql)
                before.append(rows.get(t, 0.0))
            cur.execute(f"SET LOCAL default_statistics_target = {PROBE_TARGET}")
            cur.execute(f"ANALYZE {t}")
            s = 0.0
            for sql, b in zip(probes, before):
                _, _, rows = plan_hash_cost(cur, sql)
                s += abs(np.log((rows.get(t, 0.0) + 1.0) / (b + 1.0)))
            scores[i] = float(s)
            c2.rollback()
        cur.close()
    return scores, (time.perf_counter() - t0) * 1000.0


def choose_tables(arm, epoch, conn, rng_arm, last_analyzed, mod_acc):
    """mod_acc mirrors n_mod_since_analyze arm-side (rows modified since
    this arm's last ANALYZE) — exact and immune to pg's build-time
    COPY/ANALYZE flush race; verified against pg_stat in shakedown."""
    probe_ms = 0.0
    if arm == "none":
        return [], probe_ms, None
    if arm == "fresh":
        return list(range(N_TABLES)), probe_ms, None
    if arm == "directional":
        scores, probe_ms = probe_scores(conn)
        order = sorted(scores, key=lambda i: (-scores[i], i))
        return order[:K_DIR], probe_ms, scores
    if arm == "churn":
        order = sorted(range(N_TABLES), key=lambda i: (-mod_acc[i], i))
        return order[:K_BASE], probe_ms, dict(mod_acc)
    if arm == "churn2":
        order = sorted(range(N_TABLES), key=lambda i: (-mod_acc[i], i))
        return order[:K_CHURN2], probe_ms, dict(mod_acc)
    if arm == "age":
        order = sorted(range(N_TABLES), key=lambda i: (last_analyzed[i], i))
        return order[:K_BASE], probe_ms, dict(last_analyzed)
    if arm == "random":
        return [int(x) for x in
                rng_arm.choice(N_TABLES, K_BASE, replace=False)], probe_ms, None
    raise ValueError(arm)


def measure_epoch(conn):
    """Execute the full workload under the arm's current stats."""
    cur = conn.cursor()
    out = {}
    for q, (sql, _) in QUERIES.items():
        h, cost, _rows = plan_hash_cost(cur, sql)
        med, raw = timed_exec(cur, sql)
        out[q] = dict(hash=h, cost=cost, med=med, raw=raw)
    cur.close()
    return out


def run_arm(arm, seed, epochs):
    conn = connect()
    build(conn, seed)  # CRN: identical data trajectory for every arm
    rng_drift = np.random.default_rng(seed + 1)   # shared across arms (CRN)
    rng_arm = np.random.default_rng(seed + 1000 + ARMS.index(arm))
    modes = {i: MODE_START for i in DRIFT}
    last_analyzed = {i: 0 for i in range(N_TABLES)}
    mod_acc = {i: 0 for i in range(N_TABLES)}
    cur = conn.cursor()
    log = []
    for e in range(1, epochs + 1):
        nmod = drift_step(conn, rng_drift, modes)
        for i, v in nmod.items():
            mod_acc[i] += v
        chosen, probe_ms, diag = choose_tables(arm, e, conn, rng_arm,
                                               last_analyzed, mod_acc)
        t0 = time.perf_counter()
        for i in chosen:
            cur.execute(f"SET default_statistics_target = {FULL_TARGET}")
            cur.execute(f"ANALYZE t{i:02d}")
            last_analyzed[i] = e
            mod_acc[i] = 0
        analyze_ms = (time.perf_counter() - t0) * 1000.0
        qrec = measure_epoch(conn)
        true_win = {}
        for i in DRIFT:  # ground-truth in-window selectivity (diagnostic)
            cur.execute(f"SELECT count(*) FROM t{i:02d} WHERE {WIN}")
            true_win[i] = cur.fetchone()[0] / N_ROWS
        epoch_ms = sum(r["med"] for r in qrec.values())
        log.append(dict(
            epoch=e, chosen=chosen, probe_ms=probe_ms, analyze_ms=analyze_ms,
            diag=diag, modes=dict(modes), true_win=true_win,
            queries=qrec, epoch_ms=epoch_ms,
        ))
        print(f"[{arm}] epoch {e:02d} chose={chosen} "
              f"workload={epoch_ms:.1f}ms", flush=True)
    cur.close()
    conn.close()
    return log


def shakedown():
    """Mechanics + REGIME validation, no arms: a 20-epoch no-refresh
    trajectory. The regime gate that killed substrate v1: at flip
    epochs, plans from fresh stats must actually EXECUTE faster than
    the stale plans — else the premise of refresh scheduling is absent
    at this scale and no arm comparison is meaningful."""
    seed = 20261218
    conn = connect()
    build(conn, seed)
    rng = np.random.default_rng(seed + 1)
    modes = {i: MODE_START for i in DRIFT}
    report = {"mode": "shakedown", "seed": seed, "checks": {}}

    mod_acc = {i: 0 for i in range(N_TABLES)}
    cur = conn.cursor()
    traj, regime = [], []
    for e in range(1, 21):
        nmod = drift_step(conn, rng, modes)
        for i, v in nmod.items():
            mod_acc[i] += v
        if e == 1:
            # pg counters vs the Python mirror BEFORE any rollback-
            # ANALYZE machinery has run. Build's COPY-then-ANALYZE
            # flush race can leave an N_ROWS residual on the pg side.
            cur.execute("SELECT relname, n_mod_since_analyze "
                        "FROM pg_stat_user_tables WHERE relname LIKE 't%'")
            pg_nmod = {int(r[0][1:]): int(r[1]) for r in cur.fetchall()}
            report["checks"]["pg_nmod_epoch1"] = pg_nmod
            report["checks"]["mirror_matches_pg_mod_buildrace"] = all(
                pg_nmod.get(i, -1) - mod_acc[i] in (0, N_ROWS)
                for i in range(N_TABLES))
        cur.execute(f"SELECT count(*) FROM t00 WHERE {WIN}")
        true_win = cur.fetchone()[0] / N_ROWS
        stale = {q: plan_hash_cost(cur, sql) for q, (sql, _) in QUERIES.items()}
        with connect() as c2:
            c2.autocommit = False
            k = c2.cursor()
            k.execute(f"SET LOCAL default_statistics_target = {FULL_TARGET}")
            for i in range(N_TABLES):
                k.execute(f"ANALYZE t{i:02d}")
            fresh = {q: plan_hash_cost(k, sql) for q, (sql, _) in QUERIES.items()}
            flips = [q for q in QUERIES if stale[q][0] != fresh[q][0]]
            # REGIME CHECK at every flip epoch: executed stale vs fresh
            for q in flips:
                sql = QUERIES[q][0]
                mf, _ = timed_exec(k, sql, reps=3)
                ms, _ = timed_exec(cur, sql, reps=3)
                regime.append(dict(epoch=e, q=q, stale_ms=ms, fresh_ms=mf,
                                   regret_ms=ms - mf))
            c2.rollback()
        if e == 1:
            post = {q: plan_hash_cost(cur, sql)[0]
                    for q, (sql, _) in QUERIES.items()}
            report["checks"]["rollback_restores_stale"] = all(
                post[q] == stale[q][0] for q in QUERIES)
        traj.append(dict(
            epoch=e, mode0=round(modes[0], 1), true_win_t00=round(true_win, 3),
            flips=flips))
    report["checks"]["trajectory"] = traj
    report["checks"]["regime"] = regime
    tot = sum(r["regret_ms"] for r in regime)
    pos = sum(1 for r in regime if r["regret_ms"] > 0)
    report["checks"]["regime_total_regret_ms"] = tot
    report["checks"]["regime_positive_fraction"] = (
        pos / len(regime) if regime else None)
    report["checks"]["any_flips"] = any(t["flips"] for t in traj)
    report["checks"]["flip_epochs"] = [t["epoch"] for t in traj if t["flips"]]
    report["checks"]["churn_ranks_irrelevant_first"] = (
        min(mod_acc[i] for i in IRRELEVANT)
        > max(mod_acc[i] for i in DRIFT + STABLE))

    # probe mechanics (after 20 epochs of drift)
    scores, probe_ms = probe_scores(conn)
    report["checks"]["probe_scores"] = {str(k): v for k, v in scores.items()}
    report["checks"]["probe_ms"] = probe_ms
    order = sorted(scores, key=lambda i: (-scores[i], i))
    report["checks"]["probe_top4"] = order[:4]
    report["checks"]["probe_top2_are_drift"] = set(order[:K_DIR]) <= set(DRIFT)
    report["checks"]["stable_below_all_drift"] = (
        scores[4] < min(scores[i] for i in DRIFT))
    cur.close()
    conn.close()
    return report


def main():
    mode = sys.argv[1]
    os.makedirs("/home/claude/db3_results", exist_ok=True)
    if mode == "shakedown":
        rep = shakedown()
        seed = rep["seed"]
    else:
        seed = int(sys.argv[2])
        t0 = time.time()
        arms = {arm: run_arm(arm, seed, EPOCHS) for arm in ARMS}
        summary = {}
        for arm, log in arms.items():
            ms = [ep["epoch_ms"] for ep in log]
            summary[arm] = dict(
                total_workload_ms=float(np.sum(ms)),
                mean_epoch_ms=float(np.mean(ms)),
                probe_ms_total=float(np.sum([ep["probe_ms"] for ep in log])),
                analyze_ms_total=float(np.sum([ep["analyze_ms"] for ep in log])),
            )
        rep = dict(mode=mode, seed=seed, epochs=EPOCHS, n_rows=N_ROWS,
                   k_base=K_BASE, k_dir=K_DIR, arms=ARMS, summary=summary,
                   log=arms, wall_s=time.time() - t0)
    path = f"/home/claude/db3_results/db3_{mode}_{seed}.json"
    with open(path, "w") as f:
        json.dump(rep, f, indent=1, default=str)
    print("WROTE", path)


if __name__ == "__main__":
    main()
