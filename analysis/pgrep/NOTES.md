# XPROTO-PG — consumer-relative replication staleness (design notes)

Shakedown-stage exploration of the first **non-routing** cell of the
vacuity taxonomy: Postgres streaming replication. No evidential weight;
a sealed cell would follow the usual discipline (family, bars committed
before the run, fresh configuration).

## The claim being explored

The standard replication monitor — `now() -
pg_last_xact_replay_timestamp()` against a threshold — is a **global,
consumer-blind** certificate, and it is wrong in both directions
depending on regime:

- **false-clear** (the dangerous one): global lag under threshold while
  a row some consumer actually reads is stale on the replica;
- **false-alarm** (the availability tax): on a quiet primary the replay
  timestamp stops advancing, the metric grows without bound, and the
  monitor reports staleness while the replica is perfectly current —
  needlessly forcing reads to the primary.

The consumer-relative alternative: a **witness** (logical-decoding
stream = the WAL as ground-truth churn feed) tracks last-change LSN per
relation; consumer *i*'s certificate is CLEAR iff nothing in its
footprint changed past the replica's replay LSN — `tr(P_i · drift) = 0`
with `P_i` the footprint operator. Postgres is the cheapest substrate
the program has met: the witness channel (WAL) is native, and the
beacon methodology (known writes at known times) needs no lab
construction beyond two containers.

## CAP/PACELC positioning (owner's framing, 2026-08-19)

- **P leg:** CAP treats partition as a binary endpoint; systems live on
  the continuum of degraded observation (delay, loss, asymmetry). OT
  quantifies that interior — SC-2's delay-decorrelation law is the
  P-leg's interior law, and a full partition is the observation-age →
  ∞ limit where estimates revert to the prior. PACELC named this
  regime (Else: latency vs consistency); OT's delta is
  **consumer-relative weighting + witnessed (not modeled) staleness +
  derivable margins**.
- **C leg:** linearizability is a global, consumer-blind predicate.
  The **staleness/divergence face** of C becomes per-consumer:
  `tr(P_i · divergence) ≤ ε` certificates (this lab). The **ordering
  face** (causal/sequential/session semantics) is an algebra over
  histories — whether read operators generalize there is open
  research, and we do not claim it.
- **A leg:** touched via the false-alarm tax — consumer-blind monitors
  spend availability where no consumer needed it.

## Prior art to position against (before any sealed claim)

- **PBS** (Bailis et al., probabilistically bounded staleness): global
  and model-based; here staleness is consumer-weighted and measured
  against WAL ground truth.
- Bounded-staleness / session-guarantee literature and consistency
  SLAs (e.g. Pileus): guarantee lattices, not witnessed vacuity of the
  deployed monitor.
- Exact mechanisms (`synchronous_commit=remote_apply`, LSN-token
  read-your-writes): where consistency can be bought exactly, this
  module adds nothing — scope is the regimes where you can't afford
  them (geo-replicas, analytics offload, matviews, planner stats).

## The shakedown (pgrep_shakedown.py)

Primary (wal_level=logical) + replica with
`recovery_min_apply_delay=1000ms` (a controlled, honest staleness
window). Consumer A reads `hot_a` (bursty: 5 writes/s in alternating
20 s phases); consumer B reads `hot_b` (sparse: 1 write / 8 s). Beacon
writes carry (seq, commit time), so ground truth per consumer per tick
is exact. Sampled at 5 Hz: naive lag vs thresholds {0.1..5 s}, the
witness certificate per consumer, truth per consumer.

Expected shape (to be measured, not asserted): naive false-clear > 0
for A at large thresholds during churn; naive false-alarm ≈ 1 during
quiet phases (the idle-timestamp pathology); witness certificate ≈
correct in both directions, bounded by witness poll latency.

## Shakedown outcome (2026-08-19, run on the Atlas lab — no weight)

600 samples @5 Hz over 120 s; 296 writes to `hot_a`, 15 to `hot_b`;
apply delay 1000 ms. Truth-stale fraction: A 0.513, B 0.097.

| monitor | A false-clear | A false-alarm | B false-clear | B false-alarm |
|---|---|---|---|---|
| naive T=0.1–1.0 s | 0.000 | 0.487 | 0.000 | **0.903** |
| naive T=2 s | **0.498** | 0.400 | 0.052 | 0.370 |
| naive T=5 s | **0.500** | 0.178 | 0.062 | 0.157 |
| **witness cert** | **0.005** | **0.000** | 0.037 | 0.015 |

The shape is exactly the consumer-relativity claim, measured:

- **No naive threshold serves both consumers.** Below the apply delay
  the monitor is "safe" only by crying wolf — B pays a 90 % false-alarm
  availability tax (quiet table + idle-timestamp pathology + A's churn
  polluting the global metric). Above the apply delay the dangerous
  direction opens: **half of all samples are false-clears for the hot
  consumer** — essentially every truly-stale read passes as clear.
  min-max error over all thresholds ≈ 0.4.
- **The witness certificate beats the entire naive ROC at once**:
  ~100× less false-clear for A with zero false-alarm, both consumers
  served correctly from the same replica. Residuals are poll-granularity
  effects (200 ms witness tick vs 200 ms truth guard), stated.

Caveats: shakedown, not sealed — thresholds not preregistered, single
run, apply delay is a chosen lab knob, B's sample is small (15 writes).
A sealed cell needs the family/bars discipline and a fresh
configuration. But as a candidate headline: **the standard Postgres
lag monitor has no threshold that serves heterogeneous consumers; a
WAL-witnessed, footprint-aware certificate removes both error
directions simultaneously.**

## If it becomes a module

`governor.pg`: witness feed (logical slot), footprint extraction
(pg_stat_statements per role/app), certificates via the EXISTING
tooltip model (substrate-agnostic by design), vacuity audit runner,
OP4-style refresh-floor advice for matviews/ANALYZE. Tier-0 posture
first (read-only measurement), consumer-aware read routing as the
earned-authority endgame. Dogfood target: the program's own #2/#4
Postgres backend.
