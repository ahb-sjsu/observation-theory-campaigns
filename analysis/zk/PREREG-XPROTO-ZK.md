# PREREG-XPROTO-ZK — ZooKeeper local-read staleness cell (the coordination-service twin)

**STATUS: SEALED 2026-08-24.** FAMILY-CONSTRUCTED: 2026-08-23. Earliest compliant
seal **2026-08-24** (`zk_check.py` enforces the cooling-off in code). The
**sealed graded run is on the real substrate** (mode="zk": a 3-node ZooKeeper
ensemble on Atlas, `lab_up.sh` + `fam_zk.py`). Graded on seeds {20260824,
20260825, 20260826}, disjoint from the shakedown's {0,1,2}. No evidential
weight until sealed and run on the real ensemble.

**IP posture:** public methodology; the coordination-service entry in the
replication survey. Nothing gated. **Collaborator relevance:** ZooKeeper's
`sync()` local-read staleness is Ben Reed's system (SJSU; ZooKeeper/Zab
co-creator) measured in the taxonomy.

## The claim

ZooKeeper serves reads **locally** from whatever server a client is connected
to; a follower answers from its own applied state, which may lag the leader's
committed state (writes are linearizable through the leader via Zab, but local
reads are not). A naive local read is therefore a **certificate**---an implicit
claim that the follower is fresh enough---that **false-clears under write load**:
the returned znode version is older than the leader's committed version, yet the
read is served as if current. Graded against the **zxid witness** (each znode's
modification zxid, `mzxid`; the leader's committed `mzxid` is the ground truth,
the follower's is what the local read sees), the naive local read has a
false-clear (stale) rate far above target for a **hot footprint**, while ZooKeeper's
own **`sync()`** barrier (flush leader$\to$follower before the read) holds it at
zero. The false-clear rate is **consumer-relative**: on the *same* follower a
hot-footprint reader reads stale while a cold-footprint reader reads fresh, so no
single "the follower is fresh enough" assumption serves both. `sync()` is the
deployed witnessed correction; OT's delta is the *measured, consumer-relative,
calibrated* false-clear rate.

## Family F-ZK (constructed + shaken down 2026-08-23)

A 3-node ensemble (1 leader, 2 followers). Staleness on the reader's follower is
induced by a **200 ms netem delay on the Zab commit stream** (leader egress
$\to$ that follower's IP), the coordination-service analog of PostgreSQL
`recovery_min_apply_delay` / a MongoDB delayed secondary / the geo-fleet Pauser
(disclosed; client reads to the follower's client port are NOT delayed, so they
stay prompt while the follower's applied state lags). A writer (on the leader)
writes `HOT`={0,1,2} every ~12 ms and `COLD`={7,8,9} every ~3.6 s over 10 znodes.
Two policies over the same run: **naive** (trust the local follower read) and
**witnessed** (`sync()` the path, then read). Truth (leader `mzxid`) is read
**before** the follower read, so a write committing during the read is not
counted stale (in-flight writes do not disqualify the follower --- the
guard-consistency lesson from XPROTO-GEO/PGX). A read is stale iff the follower's
`mzxid` is behind the leader's `mzxid` captured before it.

## Bars (bind at seal; checked against the family record first)

*Demonstrated on seeds {0,1,2}: naive_hot ≈ 0.99, naive_cold ≈ 0.01,
witnessed = 0.00, mean zxid gap ≈ 12.*

- **B1 — local-read certificate vacuity.** Per seed: `naive_hot ≥ 0.25` (the
  hot-footprint local read false-clears ≥ 2.5× the 0.10 target).
- **B2 — witness holds.** Per seed: `witnessed ≤ 0.10` (the `sync()` barrier
  keeps stale reads at/near zero).
- **B3 — dominance.** Per seed: `witnessed ≤ naive_hot / 2`.

**Manipulation checks (bars too):**
- **MC1 — staleness is real.** `mean_zxid_gap ≥ 2.0` (the follower genuinely
  lags the leader; if there is no lag there is no story).
- **MC2 — follower sane, staleness consumer-relative.** `naive_cold ≤ 0.10`
  (a cold footprint on the SAME delayed follower reads fresh --- the follower is
  not simply broken; the staleness is set by *what the consumer reads*).
- **MC3 — non-degenerate.** `n_reads ≥ 500` and `n_writes ≥ 200`.

**Verdict rule:** any MC failure → VOID; all MCs + B1–B3 pass on every graded
seed → PASS; otherwise FAIL, kept as executed.

**Kills.** `naive_hot < 0.15` — no local-read vacuity in this regime; or
`witnessed > 0.20` — `sync()` does not hold.

## Seal procedure

On 2026-08-24 or later: confirm `ZKREP-family.json` (mode "zk") PASSes
`zk_check.py --check-family`, reread this prereg, flip STATUS to `SEALED <date>`,
commit. Then on Atlas: `bash lab_up.sh 200` (fresh ensemble + netem), `fam_zk.py
--seeds 20260824 20260825 20260826 --out ZKREP-graded-raw.json`, pull it,
`zk_check.py` (seal-guarded) → commit `XPROTO-ZK-graded.json` as executed, then
`bash lab_down.sh`.

## Scope

Link-level to the coordination service: real ZooKeeper 3.9, real Zab, real
`mzxid` witness, real `sync()`; staleness induced by a disclosed netem delay
(mobility/geography stand-in). A production trace, observer/watch-based reads, a
larger ensemble, and read-scaling with observers are external-validity
graduations. `sync()` is credited ZooKeeper behavior; the delta is the measured,
consumer-relative false-clear rate and the demonstration that it is a footprint
property, not a replica property --- the same grammar as the WAL/oplog-witnessed
database cells and the HARQ-witnessed radio cells.

## Provenance

- Exploration: the replication survey (ZooKeeper `sync()` local-read staleness
  flagged as a candidate cell; Ben Reed collaborator fit).
- Substrate: `lab_up.sh` (3-node ensemble + Zab-stream netem), `topology.json`.
- Family + grading: `fam_zk.py`; graded runner `zk_check.py` (seal-guard +
  coded cooling-off + real-substrate-only sealed grading + pre-seal record check).
