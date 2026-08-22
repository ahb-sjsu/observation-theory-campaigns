#!/usr/bin/env python3
"""DB-3: directional optimizer-statistics refresh (advanced-DB survey flagship F3).

Runs ON Atlas against the project-owned PostgreSQL 16 cluster
(localhost:5544, autovacuum off, data /home/claude/db3_pg — system
cluster on 5432 untouched).

Question: when ANALYZE budget is scarce, does allocating it by a
probed plan-sensitivity signal (which tables' refresh would actually
change the optimizer's plans for the live workload) beat the
industrial churn baseline (n_mod_since_analyze), age, and random —
at a count handicap (directional refreshes k=2 tables/epoch and pays
for its probes; baselines refresh k=3)?

Substrate: 12 tables x 20k rows.
  t00..t03  workload-relevant, drifting predicate column `a`
            (moderate churn that SHIFTS the distribution)
  t04..t07  workload-relevant, churning but distribution-stable
            (`a` redrawn from the SAME distribution: churn w/o impact)
  t08..t11  not in the workload, HIGH churn (pad rewrites)
So modification counters rank t08..t11 first — the churn baseline is
fooled exactly where the theory says counters and plan-impact diverge.

Referee (regret zero point), per epoch, no twin database needed:
  BEGIN; ANALYZE all tables (full target); EXPLAIN each query ->
  fresh plan; execute fresh-plan queries timed; ROLLBACK  (ANALYZE is
  transactional in PostgreSQL; the rollback restores the arm's stale
  pg_statistic). Arm-plan executions run outside the txn on identical
  data. regret_q = median latency(arm plan) - median latency(fresh
  plan), measured only when the plan hashes differ (else 0).

Probe (directional arm, charged by the k=2 handicap + logged ms):
  per table: BEGIN; SET LOCAL default_statistics_target=10;
  ANALYZE t_i; re-EXPLAIN the queries touching t_i; score =
  sum |est-cost delta| + FLIP_W * plan-flips; ROLLBACK.

Endpoint is executed latency -> nondeterministic: logged-response
posture (LM-track precedent). Raw timings are the artifact;
instrument gate = repeat spread of medians. Full-target ANALYZE
(300*100 = 30000 sampled rows > 20000) reads every row, so referee
stats are deterministic; probe stats (target 10) are sampled and
noisy by design — that noise is part of the probed method.

Modes:
  shakedown            mechanics validation (flips, rollback, counters, timing CV)
  pilot <seed>         full multi-arm run, disclosed
  governed <seed>      identical code path; run only after seal
Output: /home/claude/db3_results/db3_<mode>_<seed>.json
"""

import hashlib
import json
import os
import sys
import time

import numpy as np
import psycopg2

DSN = dict(host="localhost", port=5544, user="claude", dbname="db3")

N_TABLES = 12
N_ROWS = 20000
DRIFT = [0, 1, 2, 3]          # relevant + distribution-shifting
STABLE = [4, 5, 6, 7]         # relevant, churn without shift
IRRELEVANT = [8, 9, 10, 11]   # not queried, high churn
EPOCHS = 30
K_BASE = 3                    # refreshes/epoch for churn, age, random
K_DIR = 2                     # directional handicap: fewer refreshes, pays probes
PROBE_TARGET = 10
FULL_TARGET = 100
TIMED_REPS = 5
MODE_START = 650.0
MODE_STEP = (-35.0, 12.0)     # mean, sd of the seeded mode walk
DRIFT_FRAC = 10               # DRIFT tables churn N_ROWS//10 per epoch
ARMS = ["directional", "churn", "age", "random", "none"]

# Narrow predicate windows the drift mode walks THROUGH (~epochs 11-14):
# selectivity starts ~6% (index/bitmap territory), spikes as the mode
# transits the window (seq/hash territory), then decays — real plan
# flips in both directions. Shakedown 20261218 rev1 showed wide
# predicates (a<120, 80..220) never cross a plan boundary.
WIN = "a BETWEEN 180 AND 240"      # 6% under the initial uniform
NARROW = "a BETWEEN 195 AND 225"   # 3% — the nested-loop trap window

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
# Drifting-pair joins: the flip-capable, load-bearing forms (join
# method/order turns on the product of two drifting misestimates —
# shakedown rev4 showed this is the mechanism that actually flips).
# Four of them so regret pools instead of hanging off one query.
for qa, qb in [(0, 1), (2, 3), (0, 2), (1, 3)]:
    QUERIES[f"QD{qa}{qb}"] = (
        f"SELECT count(*), COALESCE(sum(x.b),0) FROM t{qa:02d} x "
        f"JOIN t{qb:02d} z ON x.b = z.b WHERE x.{NARROW} AND z.{NARROW}",
        [qa, qb],
    )

# Consumer footprint for the directional probe: the workload's
# predicates on each table. Tables carrying no workload predicate have
# zero consumer footprint — the directional arm never probes them.
PROBE_PREDS = {0: [WIN, NARROW], 1: [WIN, NARROW], 2: [WIN, NARROW],
               3: [WIN, NARROW], 4: [WIN]}


def connect():
    conn = psycopg2.connect(**DSN)
    conn.autocommit = True
    return conn


def build(conn, seed):
    """Deterministic rebuild: identical data for every arm (CRN)."""
    rng = np.random.default_rng(seed)
    cur = conn.cursor()
    # SSD-realistic planner costing: with the default random_page_cost=4
    # the planner picks seq scans on both sides of realistic selectivity
    # shifts and plans never flip (shakedown 20261218 rev1-3).
    cur.execute("ALTER SYSTEM SET random_page_cost = 1.1")
    cur.execute("SELECT pg_reload_conf()")
    for i in range(N_TABLES):
        t = f"t{i:02d}"
        cur.execute(f"DROP TABLE IF EXISTS {t}")
        cur.execute(
            f"CREATE TABLE {t} (id int PRIMARY KEY, a int NOT NULL, "
            f"b int NOT NULL, pad text NOT NULL)"
        )
        a = rng.integers(0, 1000, N_ROWS)
        b = rng.integers(0, 500, N_ROWS)
        rows = "\n".join(
            f"{j}\t{a[j]}\t{b[j]}\t{'x' * 240}" for j in range(N_ROWS)
        )
        from io import StringIO
        cur.copy_expert(f"COPY {t} FROM STDIN", StringIO(rows))
        cur.execute(f"CREATE INDEX ON {t} (a)")
        # b-index on every table: gives the planner the nested-loop
        # path, whose misuse under stale estimates is the real regret
        # mechanism (without it only near-tie hash orders can flip)
        cur.execute(f"CREATE INDEX ON {t} (b)")
        cur.execute(f"SET default_statistics_target = {FULL_TARGET}")
        cur.execute(f"ANALYZE {t}")  # all arms start with fresh stats
    cur.close()


def drift_step(conn, rng, modes):
    """One epoch of seeded churn. Returns rows modified per table."""
    cur = conn.cursor()
    nmod = {}
    # Update-set sizes are drawn binomially: exact constant sizes create
    # artificial ties in the churn arm's counter ranking that the
    # tie-break would resolve arbitrarily; real counters jitter.
    for i in DRIFT:  # ~10% of rows, values pulled toward the walking mode
        modes[i] = float(np.clip(modes[i] + rng.normal(*MODE_STEP), 40, 950))
        n = int(rng.binomial(N_ROWS, 1.0 / DRIFT_FRAC))
        ids = rng.choice(N_ROWS, n, replace=False)
        vals = np.clip(rng.normal(modes[i], 45, ids.size), 0, 999).astype(int)
        args = ",".join(f"({int(j)},{int(v)})" for j, v in zip(ids, vals))
        cur.execute(
            f"UPDATE t{i:02d} t SET a = v.a FROM (VALUES {args}) AS v(id,a) "
            f"WHERE t.id = v.id"
        )
        nmod[i] = ids.size
    for i in STABLE:  # ~5% churn, a redrawn from the ORIGINAL distribution
        ids = rng.choice(N_ROWS, int(rng.binomial(N_ROWS, 0.05)), replace=False)
        vals = rng.integers(0, 1000, ids.size)
        args = ",".join(f"({int(j)},{int(v)})" for j, v in zip(ids, vals))
        cur.execute(
            f"UPDATE t{i:02d} t SET a = v.a FROM (VALUES {args}) AS v(id,a) "
            f"WHERE t.id = v.id"
        )
        nmod[i] = ids.size
    for i in IRRELEVANT:  # ~20% churn, pad only — loud counters, no plan impact
        n = int(rng.binomial(N_ROWS, 0.20))
        lo = int(rng.integers(0, N_ROWS - n))
        cur.execute(
            f"UPDATE t{i:02d} SET pad = pad WHERE id BETWEEN {lo} "
            f"AND {lo + n - 1}"
        )
        nmod[i] = n
    # PG15+ cumulative stats: the writer's pending counters are invisible
    # to pg_stat_user_tables until flushed — force it before any arm reads.
    cur.execute("SELECT pg_stat_force_next_flush()")
    cur.execute("SELECT 1")
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
    cur.execute(sql)  # warm
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter()
        cur.execute(sql)
        cur.fetchall()
        ts.append((time.perf_counter() - t0) * 1000.0)
    return float(np.median(ts)), ts


def probe_scores(conn):
    """Canonical-selectivity rollback probes on the consumer footprint.

    For each table with workload predicates: EXPLAIN the predicate's
    row estimate under current stats, mini-ANALYZE (target 10) inside
    a txn, re-EXPLAIN, ROLLBACK. Score = sum |log estimate shift|.
    Probing the workload queries themselves is an artifact trap:
    coarse probe stats spuriously flip join plans and change Plan Rows
    semantics (per-loop rows) — shakedown 20261218 rev1/rev2 both
    ranked stable tables above drifted ones that way. Single-table
    count(*) probes have plan-shape-independent row estimates.
    """
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
    this arm's last ANALYZE of the table). The live pg_stat counter is
    unusable here: cumulative-stats reports are NON-transactional, so
    the referee's rolled-back ANALYZE-all still zeroes the real counter
    every epoch (verified in shakedown 20261218). The mirror is exact —
    shakedown checks it against pg_stat before any referee txn runs."""
    probe_ms = 0.0
    if arm == "none":
        return [], probe_ms, None
    if arm == "directional":
        scores, probe_ms = probe_scores(conn)
        order = sorted(scores, key=lambda i: (-scores[i], i))
        return order[:K_DIR], probe_ms, scores
    if arm == "churn":
        order = sorted(range(N_TABLES), key=lambda i: (-mod_acc[i], i))
        return order[:K_BASE], probe_ms, dict(mod_acc)
    if arm == "age":
        order = sorted(range(N_TABLES), key=lambda i: (last_analyzed[i], i))
        return order[:K_BASE], probe_ms, dict(last_analyzed)
    if arm == "random":
        return [int(x) for x in
                rng_arm.choice(N_TABLES, K_BASE, replace=False)], probe_ms, None
    raise ValueError(arm)


def measure_epoch(conn):
    """Arm plans + referee (fresh-stats) plans/latencies + arm latencies."""
    cur = conn.cursor()
    arm_plans = {q: plan_hash_cost(cur, sql) for q, (sql, _) in QUERIES.items()}
    cur.close()

    fresh, t0 = {}, time.perf_counter()
    with connect() as c2:
        c2.autocommit = False
        cur = c2.cursor()
        cur.execute(f"SET LOCAL default_statistics_target = {FULL_TARGET}")
        for i in range(N_TABLES):
            cur.execute(f"ANALYZE t{i:02d}")
        for q, (sql, _) in QUERIES.items():
            h, cost, _rows = plan_hash_cost(cur, sql)
            med = raw = None
            if h != arm_plans[q][0]:
                med, raw = timed_exec(cur, sql)
            fresh[q] = dict(hash=h, cost=cost, med=med, raw=raw)
        c2.rollback()
        cur.close()
    referee_ms = (time.perf_counter() - t0) * 1000.0

    out = {}
    cur = conn.cursor()
    for q, (sql, _) in QUERIES.items():
        fh = fresh[q]
        flip = fh["hash"] != arm_plans[q][0]
        rec = dict(arm_hash=arm_plans[q][0], arm_cost=arm_plans[q][1],
                   fresh_hash=fh["hash"], fresh_cost=fh["cost"], flip=flip,
                   regret_ms=0.0, arm_med=None, fresh_med=fh["med"],
                   arm_raw=None, fresh_raw=fh["raw"])
        if flip:
            med, raw = timed_exec(cur, sql)
            rec["arm_med"], rec["arm_raw"] = med, raw
            rec["regret_ms"] = med - fh["med"]
        out[q] = rec
    cur.close()
    return out, referee_ms


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
        qrec, referee_ms = measure_epoch(conn)
        true_win = {}
        for i in DRIFT:  # ground-truth in-window selectivity (diagnostic)
            cur.execute(f"SELECT count(*) FROM t{i:02d} WHERE {WIN}")
            true_win[i] = cur.fetchone()[0] / N_ROWS
        log.append(dict(
            epoch=e, chosen=chosen, probe_ms=probe_ms, analyze_ms=analyze_ms,
            referee_ms=referee_ms, diag=diag, modes=dict(modes),
            true_win=true_win,
            queries=qrec,
            epoch_regret=sum(r["regret_ms"] for r in qrec.values()),
            flips=sum(r["flip"] for r in qrec.values()),
        ))
        print(f"[{arm}] epoch {e:02d} chose={chosen} "
              f"flips={log[-1]['flips']} regret={log[-1]['epoch_regret']:.1f}ms",
              flush=True)
    cur.close()
    conn.close()
    return log


def shakedown():
    """Mechanics validation, no arms: a 20-epoch NO-refresh drift
    trajectory with per-epoch stale-vs-fresh plan comparison, so the
    flip dynamics are visible instead of guessed."""
    seed = 20261218
    conn = connect()
    build(conn, seed)
    rng = np.random.default_rng(seed + 1)
    modes = {i: MODE_START for i in DRIFT}
    report = {"mode": "shakedown", "seed": seed, "checks": {}}

    mod_acc = {i: 0 for i in range(N_TABLES)}
    cur = conn.cursor()
    traj, lat_done = [], False
    for e in range(1, 21):
        nmod = drift_step(conn, rng, modes)
        for i, v in nmod.items():
            mod_acc[i] += v
        if e == 1:
            # BEFORE any referee txn: pg counters vs the Python mirror.
            # Build's COPY-then-ANALYZE flush race can leave an N_ROWS
            # residual on the pg side; the mirror is the clean signal.
            cur.execute("SELECT relname, n_mod_since_analyze "
                        "FROM pg_stat_user_tables WHERE relname LIKE 't%'")
            pg_nmod = {int(r[0][1:]): int(r[1]) for r in cur.fetchall()}
            report["checks"]["pg_nmod_epoch1"] = pg_nmod
            report["checks"]["mirror_matches_pg_mod_buildrace"] = all(
                pg_nmod.get(i, -1) - mod_acc[i] in (0, N_ROWS)
                for i in range(N_TABLES))
        # ground-truth in-window selectivity on the fastest-drifting table
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
            if flips and not lat_done:
                # regret magnitude + repeatability at the first flip epoch
                lat = {}
                for q in flips[:4]:
                    sql = QUERIES[q][0]
                    mf, _ = timed_exec(k, sql)
                    m1, _ = timed_exec(cur, sql)
                    m2, _ = timed_exec(cur, sql)
                    lat[q] = dict(
                        stale_meds=[m1, m2], fresh_med=mf,
                        repeat_rel_spread=abs(m1 - m2) / max(m1, m2),
                        regret_ms=float(np.mean([m1, m2]) - mf))
                report["checks"]["latency_first_flips"] = dict(epoch=e, lat=lat)
                lat_done = True
            c2.rollback()
        if e == 1:
            post = {q: plan_hash_cost(cur, sql)[0]
                    for q, (sql, _) in QUERIES.items()}
            report["checks"]["rollback_restores_stale"] = all(
                post[q] == stale[q][0] for q in QUERIES)
        traj.append(dict(
            epoch=e, mode0=round(modes[0], 1), true_win_t00=round(true_win, 3),
            flips=flips,
            qs0_est_stale=stale["QS0"][2].get("t00"),
            qs0_est_fresh=fresh["QS0"][2].get("t00")))
    report["checks"]["trajectory"] = traj
    report["checks"]["any_flips"] = any(t["flips"] for t in traj)
    report["checks"]["flip_epochs"] = [t["epoch"] for t in traj if t["flips"]]
    report["checks"]["churn_ranks_irrelevant_first"] = (
        min(mod_acc[i] for i in IRRELEVANT)
        > max(mod_acc[i] for i in DRIFT + STABLE))

    # referee side effect: rolled-back ANALYZE resets the real counters
    cur.execute("SELECT relname, n_mod_since_analyze FROM pg_stat_user_tables "
                "WHERE relname LIKE 't%'")
    post_nmod = {int(r[0][1:]): int(r[1]) for r in cur.fetchall()}
    report["checks"]["referee_resets_pg_counters"] = all(
        v == 0 for v in post_nmod.values())

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
            reg = [ep["epoch_regret"] for ep in log]
            summary[arm] = dict(
                total_regret_ms=float(np.sum(reg)),
                mean_epoch_regret_ms=float(np.mean(reg)),
                total_flips=int(np.sum([ep["flips"] for ep in log])),
                probe_ms_total=float(np.sum([ep["probe_ms"] for ep in log])),
                analyze_ms_total=float(np.sum([ep["analyze_ms"] for ep in log])),
            )
        rep = dict(mode=mode, seed=seed, epochs=EPOCHS, k_base=K_BASE,
                   k_dir=K_DIR, arms=ARMS, summary=summary, log=arms,
                   wall_s=time.time() - t0)
    path = f"/home/claude/db3_results/db3_{mode}_{seed}.json"
    with open(path, "w") as f:
        json.dump(rep, f, indent=1, default=str)
    print("WROTE", path)
    if mode == "shakedown":
        print(json.dumps(rep["checks"], indent=1, default=str))


if __name__ == "__main__":
    main()
