# DB Track: Database Physical Design Under Consumer Geometry

**Status:** design draft, unsealed, non-claim-bearing. Chip 💾 DB.
No bar in this document is calibrated yet; thresholds are PENDING
PILOT until disclosed powered draws fix them (PROTOCOL §5.1; bars
from the ACROSS-DRAW distribution per the LM1-002 lesson).

## 0. Coordination boundary (binding)

The owner's concurrent program (`network-governor`,
PREREG-XPROTO-GEO, 2026-08-21) occupies consumer-relative FRESHNESS
for replica READ-ROUTING (footprint-certified replica selection on a
live geo-distributed Postgres fleet). This track therefore:
- claims NOTHING about replica routing, read placement, witnessed
  freshness certificates, replication lag, or fleet substrates;
- treats freshness/refresh questions generally as ceded or
  coordination-required territory (survey Area C note);
- works the orthogonal axis only: PRECISION/ENCODING allocation at
  matched storage budgets (DB-1) and the multi-workload alignment
  tax for shared physical design (DB-2).

## 1. Question (DB-1, the first campaign)

Survey headline cell A ([`../paper/OT-DATABASES-SURVEY.md` in
geometric-observation]): can per-column storage precision be
allocated by a QUERY-ONLY probed sensitivity of the downstream
consumer's answer quality — beating task-blind allocation at matched
precision budgets — and does the quantize-the-unread effect
(coarsening columns outside the consumer's read geometry actively
IMPROVING its answers) exist as a physical-design phenomenon?

Prior-art posture (recon-grade, from the survey; quote-verification
owed pre-seal): SPARTAN (declared tolerances), QoI-preserving
compression (closed-form downstream functions), compression-aware
physical design (lossless, cost-only) conceded; the probed-sensitivity
allocation and the coarsening-helps effect unoccupied.

## 2. Design (DB-1 pilot family)

Substrate: DuckDB (local, deterministic, seeded — EC-grade bitwise
reproducibility; no gateway, no owned-GPU, negligible power).

- **Data:** n = 20,000 rows, d = 8 numeric columns x1..x8 ~ seeded
  prior; external targets y_A = f_A(planted subset A) + noise,
  y_B = f_B(planted subset B) + noise materialized alongside.
- **Consumers (black boxes to the probe):** similarity/report
  programs run via SQL + a thin scorer: consumer i answers m = 200
  held-out query rows by k-NN over the STORED (encoded) columns
  (k = 25), reporting the neighbour-mean target; loss = MSE against
  the TRUE targets (external ground truth — the loss an owner cares
  about, and the honest frame in which coarsening CAN help: for
  similarity consumers, quantizing noisy unread columns is implicit
  feature selection).
- **Encoding ladder:** per column fine (full float) vs coarse
  (rounded to step 1.0; quantization std ≈ 0.29 of the unit-scaled
  prior); budget = exactly F = 4 of 8 columns fine (the LM-2 ladder;
  storage-byte realism is a declared future refinement).
- **Probe (query-only):** per column, re-run each consumer with that
  column alone coarsened; Δloss vs all-fine = the probed sensitivity
  diag P̂. Probe cost = the probe runs, logged in the artifact.
- **Arms (matched budget, CRN — identical stored rows, identical
  query rows):** aligned (top-4 by P̂), oracle (planted subset padded
  by P̂), anti (bottom-4), mean-4 distinct task-blind baseline
  (LM2-002 degeneracy-proof construction: four seed-drawn subsets,
  none equal to aligned/oracle, pairwise distinct), references
  all-coarse / all-fine.
- **Instrument:** full determinism check (same seed twice, bitwise);
  the endpoint is deterministic so the repeat gate is exact.

Candidate gates (freeze ONLY from ≥ 2 independent powered draws):
Q1 pooled aligned-vs-baseline improvement; Q1b per-consumer floors;
Q2 blind capture of oracle; Q3 anti not meaningfully better than
baseline (pooled); **Q4 the headline: aligned-at-budget beats
ALL-FINE pooled** (quantize-the-unread as a gated claim this time —
pilots decide whether it gates or reports); Q5 determinism bitwise;
Q6 probe-cost ledger present.

## 3. DB-2 (design-stage): the alignment tax

Two consumers at controlled read-geometry angles sharing one encoding
budget: egalitarian best-shared-over-utopia tax vs angle (EC-6
transplanted to physical design). Not before DB-1 resolves.

## 4. Inherited discipline (binding)

Sealed preregs, frozen gates, single governed runs reported
regardless of sign; bars from the across-draw distribution at final
power (≥ 2 draws); pooled load-bearing forms with per-cell noise
documented; degeneracy-proof baselines; anti-controls pooled;
instrument gates interpreted first (EC-7); `git commit -F` for
messages with quotes; numpy bools cast before json.dump.

## 5. DB-1 pilots, seal, and governed run: **ALL PASS 6/6 — promoted
on the first seal** (class [predicted])

Two disclosed powered draws (seeds 20261201/20261203: pooled Q1
0.2228/0.1809, capture 1.0000 all cells, anti −0.20/−0.42; Q4
quantize-the-unread ≈ 0 — the SCOPED NEGATIVE, demoted to an ungated
diagnostic rather than retuning the coarseness step to chase it).
Sealed [`PREREG-DB1-001`](PREREG-DB1-001.md) at `cecb0e9` (SEALS
`ed2ff61`); single governed run at seed 20261205
([`results/db1-governed.json`](../results/db1-governed.json)):

- **Q1 pooled +16.8%** over the degeneracy-proof mean-4 task-blind
  baseline (bar 0.10); floors 0.212/0.123 (bar 0.05).
- **Q2 capture 1.000**: the query-only probe recovered the planted
  read supports EXACTLY in all cells (aligned ≡ oracle) — noted as
  making the gate near-vacuous; the informative gates carried.
- **Q3 anti −36.0%** (bar ≤ +0.10); **Q5** bitwise-deterministic;
  **Q6** probe ledger exact (16 runs).
- **Q4 diagnostic −0.087**: the quantize-the-unread effect remains
  absent at step-1.0 on similarity consumers — the scoped negative
  holds in the governed run and stays on the record as the track's
  first finding.

The claim licensed at `[predicted]`: per-column storage precision
allocated by query-only probed consumer sensitivity beats task-blind
allocation at matched budgets on a real database engine — the
tr(P̂ Σ) allocation consequence as physical design. First first-seal
promotion of the program's applied tracks: the accumulated design
lessons (degeneracy-proof baseline, across-draw bars, pooled forms,
instrument gates, no bar-shopping) were all inherited, and none was
re-learned the hard way.

## 6. DB-2 pilots, seal, and governed run: **ALL PASS 6/6 — promoted
on the first seal** (class [predicted])

Two powered draws (seeds 20261210/20261212; 2,820 exhaustive
evaluations each — all 70 budget subsets per consumer per instance,
so shared-best and utopia are exact optima and the tax cannot be an
optimizer artifact): tax exactly 1.0000 at identical supports in both
draws; non-identical band 1.054–1.084; aware-vs-blind +23%/+22%.
**Disclosed respec, replicated across draws:** the tax is NOT
monotone in overlap COUNT (partial overlap priced above disjoint in
both pilots — the consumers' interaction terms contend for the same
high-value columns), so the tax tracks VALUE-WEIGHTED geometric
alignment, not set arithmetic; T2/T3 respecified to pooled/min forms,
monotonicity demoted to a diagnostic. Sealed
[`PREREG-DB2-001`](PREREG-DB2-001.md) at `9ba55bc` (SEALS `d08982c`);
governed seed 20261215
([`results/db2-governed.json`](../results/db2-governed.json)):

- **T1 1.0115** ≤ 1.02 (sharing near-free at coincident geometry);
- **T2 mean non-identical 1.0732** ≥ 1.03; **T3 min 1.0292** ≥ 1.02;
- **T4 aware-vs-blind +24.5%** ≥ 0.10; **T5/T6** instrument clean.
- Diagnostic epilogue: the governed draw WAS count-monotone
  (1.029 ≤ 1.094 ≤ 1.097) after both pilots were not — confirming
  count-monotonicity is draw-luck, exactly why it was demoted.

The claim licensed at `[predicted]`: one precision budget serving two
consumers carries a geometric tax — free at coincident read
structures, material otherwise — and consumer-aware sharing beats
task-blind sharing. Both survey headline cells (A: precision
allocation; B: the alignment tax) are now claimed; the DB track opened
with two first-seal promotions. Declared follow-on (not claimed): a
value-weighted alignment index that predicts the tax ordering.

## 7. Roadmap

Next candidates from the advanced survey: F3 directional
optimizer-stats refresh (fastest seal), F1 consumer-probed
vector-index quantization (the big bet, window closing). The
quantize-the-unread step-dependence and byte-realistic budgets remain
declared open questions. Boundary with XPROTO-GEO remains binding.

## 8. DB-3 (design frozen pre-pilot): directional optimizer-statistics
refresh (advanced-survey flagship F3)

**Boundary check (§0):** DB-3 is SINGLE-NODE optimizer-statistics
scheduling — which tables get scarce ANALYZE budget so the query
planner's estimates track drifting data. No replicas, no routing, no
replication lag, no freshness certificates, no fleet: outside
XPROTO-GEO's territory (the survey's F3 vetting, reaffirmed here).

**Question:** at matched refresh budgets, does allocating ANALYZE by a
probed plan-sensitivity signal (would refreshing this table's stats
change the optimizer's plans for the live workload?) beat the
industrial baseline (modification counters), age, and random — even
at a count HANDICAP (directional refreshes k=2 tables/epoch and pays
its probe cost; baselines refresh k=3)?

**Substrate:** PostgreSQL 16.15 on Atlas (project-owned cluster,
localhost:5544, data `/home/claude/db3_pg`, autovacuum off,
`random_page_cost=1.1`; system cluster on 5432 untouched). Harness
[`../python/db3_stats_refresh.py`](../python/db3_stats_refresh.py),
runs on Atlas per the owner's substrate directive (2026-08-22).

**Design (frozen through shakedown 20261218 rev7 before any pilot):**
12 tables x 20k rows. t00–t03 drift (a-values pulled toward a seeded
walking mode that transits the workload's predicate windows); t04–t07
churn WITHOUT distribution shift (a redrawn from the original
uniform); t08–t11 not queried, LOUDEST churn (~20 %/epoch pad
rewrites) — modification counters rank exactly the tables whose
refresh is worthless. Workload: 4 drifting-pair joins (`QD*`, narrow
3 % windows — the flip-capable, load-bearing forms: the nested-loop /
hash / join-order choice turns on the product of two drifting
misestimates), 4 drift-stable joins (`QJ*`), 4 window aggregates
(`QS*`), 1 stable control (`QC4`). b-indexes on all tables (without
them only near-tie hash orders can flip — shakedown rev5 lesson).

**Referee (regret zero point), one cluster, no twin DB:** per epoch,
`BEGIN; ANALYZE` all 12 at full target (full-row read at 20k rows →
deterministic stats); EXPLAIN each query → fresh plan; execute
fresh-plan queries timed inside the txn; `ROLLBACK` (ANALYZE is
transactional in PostgreSQL — pg_statistic reverts). Arm-plan
executions run outside on identical data. regret_q = median-of-5
latency(arm plan) − latency(fresh plan), measured only when plan
hashes differ. Arms run the full 30-epoch horizon sequentially with a
seeded identical rebuild + drift replay (CRN).

**Probe (charged):** per footprint table, rollback mini-ANALYZE at
statistics target 10 + canonical single-table `count(*)` re-EXPLAIN
per workload predicate; score = Σ|log row-estimate shift|. Probing
the workload queries themselves is an ARTIFACT TRAP (coarse probe
stats spuriously flip join plans and change Plan-Rows semantics —
shakedown rev1/rev2 both ranked stable tables above drifted ones);
canonical probes fixed it (rev3+: top-4 = the four drift tables,
stable below all, ~70 ms/epoch, vs k=1 full ANALYZE ~150 ms).

**Arms:** directional (probe + top-k=2), churn (top-k=3 by rows
modified since that arm's last ANALYZE — mirrored arm-side because
cumulative-stats reports are NON-transactional, so the rolled-back
referee ANALYZE zeroes the real `n_mod_since_analyze` every epoch;
mirror verified against pg_stat pre-referee in shakedown), age
(oldest-first k=3), random (seeded k=3), none (floor). Update-set
sizes drawn binomially (exact constant sizes make the churn ranking
tie-degenerate).

**Instrument posture:** executed-latency endpoint on a live host →
logged-response discipline (LM track precedent): raw per-rep timings
in the artifact; repeat gate on median spread (shakedown: ~1 % typical,
one 52 % transient outlier — medians-of-5 pooled over 4+ forms carry
it). Plan hashes and stats are deterministic given the seed.

**Shakedown record (all rev7 checks PASS):** flips in 11/20 no-refresh
epochs concentrated at the mode transit; first-flip regret +0.79 ms on
~2 ms queries; counter mirror exact modulo the build-time COPY/ANALYZE
flush race (pg residual +N_ROWS on a random subset of tables — the
mirror, not pg, is the clean signal); rollback restores stale plans;
churn ranks irrelevant tables first.

**Pilot protocol:** two disclosed powered draws (seeds 20261220,
20261222), 30 epochs x 5 arms each; candidate gates to be frozen ONLY
from the across-draw distribution (LM1-002 lesson): S1 staleness is
real (none-arm pooled regret > 0, materially); S2 directional beats
churn (THE load-bearing gate); S3 directional beats age and random;
S4 probe cost ledger (probe+ANALYZE ms within budget envelope); S5
instrument repeat gate; S6 run-integrity count. Exact bars PENDING
PILOT. Governed seed 20261225 after seal.

### 8.1 v1 pilots INVALID — substrate failure, disclosed respec
(2026-08-22, pre-seal)

Both v1 draws ran to completion and are on the record
(`db3_pilot_20261220/20261222.json`, 20k rows, referee-relative
regret): the **`none` arm produced NEGATIVE total regret in both
draws** (−67 ms, −85 ms) — fully-stale plans EXECUTED faster than the
fresh-stats referee plans. At 20k fully-cached rows the planner's
cost model does not rank plans by wall time (misestimated nested
loops stay fast), so the referee is not a valid zero point and the
substrate lacks the regime the question is about. The
directional-beats-churn ordering appeared in both draws (44 vs 66 ms;
22 vs 101 ms) but is unclaimable on an invalid substrate. Per
protocol this is a disclosed pre-seal respec, not bar-shopping: no
gate existed yet, and the failure is of the S1 SUBSTRATE gate the
design planned to freeze.

**v2 redesign (harness rewritten before any v2 pilot):**
- 200k rows/table, join fanout ~10 (`b` in [0, 20k)), work_mem 64MB —
  the scale where a wrong join choice costs real time;
- **endpoint respecified to DIRECT total workload latency per arm**
  (median-of-5 per query, summed per epoch, CRN across arms) — what
  an operator pays, with no cost-model-calibrated referee inside the
  endpoint; `fresh` (ANALYZE-all every epoch) joins as reference
  ceiling and `none` as floor;
- staleness-matters becomes GATE S1 (none materially worse than
  fresh), not an assumption; **S2 (load-bearing) respecified:
  directional total workload latency < churn's** at the k=2-vs-k=3
  handicap;
- v2 shakedown adds a REGIME check: at every no-refresh flip epoch,
  executed stale-vs-fresh latency on the flipped queries must show
  fresh materially faster on net — the check v1 lacked;
- referee-txn counter clobbering is gone with the referee, so real
  `n_mod_since_analyze` semantics hold; the verified arm-side mirror
  is kept for exactness across the build-time flush race.
v2 pilots re-run the same seeds (20261220/20261222); v1 artifacts
retained.

### 8.2 v2 shakedown regime finding: planner biased at TRUTH on one
query family — disclosed instrument calibration (2026-08-22)

The v2 regime check (executed stale-vs-fresh at every no-refresh flip
epoch, 57 instances) split cleanly by family: **QJ (one-side-filtered
joins): fresh stats win +60..+96 ms** at transit — the classic
staleness harm (underestimate → wrong join strategy). **QD
(both-sides-filtered joins): fresh stats LOSE −50..−89 ms** — with
both sides filtered, the indexed nested loop is truly optimal on
cached data even at true cardinalities, but random_page_cost=1.1
over-costs ~150k cached index probes and the planner given CORRECT
estimates picks a hash join needing two full seq scans (3x slower).
Net regime regret −130 ms, positive fraction 0.56.

No refresh policy is evaluable on a substrate where giving the
planner the truth makes it slower: the defect is planner-calibration
bias at true cardinalities, an INSTRUMENT fault (EC-7 lesson: gate
the instrument first, interpret before touching hypotheses).
Response, disclosed pre-seal: calibrate random_page_cost by an
empirical sweep (1.1/0.5/0.25/0.1/0.05 at a mid-transit drift state,
`db3_calibrate.py`) selecting the value where fresh-chosen plans are
the fastest-executing plans for BOTH families; then re-run the full
shakedown regime gate (require net-positive regret and a high
positive fraction across families) before any v2 pilot. The
calibration criterion is planner-unbiasedness-at-truth — it does not
look at any arm comparison, so it cannot tune the S2 contest.

### 8.3 Calibration outcome: the window is EMPTY — QD family excluded
(2026-08-22)

Two sweeps (rpc 1.1/0.5/0.25/0.1/0.05, then 0.6–1.0 in 0.1 steps;
`db3_calibration.json`): the one-side-filtered QJ family is
truth-unbiased only at rpc ≥ 0.9 (fresh +39..+61 ms), while the
both-sides-filtered QD family is truth-unbiased only at rpc ≤ 0.8
(at 0.9–1.1 the planner given correct estimates picks a hash join
with two full seq scans over the truly-optimal indexed nested loop,
−52..−62 ms). NO random_page_cost calibrates both join shapes on this
cached substrate — a real PostgreSQL cost-model observation
(one scalar page-cost cannot represent cached-probe economics),
recorded here as a finding of the shakedown, not a claim of the
campaign. Resolution per the pre-declared branch: the QD family is
EXCLUDED from the workload (scoped exclusion, documented), replaced
by four cross-pair one-side-filtered joins (QX: drift × different
stable partner) — 8 flip-capable load-bearing forms, all in the
regime where the planner rewards correct statistics; rpc stays 1.1.
Full shakedown regime gate re-runs before the v2 pilots. Sweep
caveat noted for the record: no-flip queries showed ±15 ms
stale-vs-fresh deltas (cache-state bias between the two measurement
paths) — the arm endpoint is immune (identical procedure every arm,
CRN), but cross-txn regime numbers carry that floor.

### 8.4 v3 pilots: S1 robust, refresh policies NOT separated at k=3 —
final design iteration to the scarcity regime (2026-08-22)

v3 regime gate had passed perfectly (35/35 flip instances
fresh-faster, net +2.72 s). Both v3 pilot draws completed
(`db3-v3-pilot-*.json`): **S1 replicated — none costs +12.1 %/+12.5 %
over fresh in both draws.** But the refresh policies did NOT separate:
draw-1 ordering age < churn < random < directional(k=2), draw-2
random < age < directional < churn, differences 1–7 % at the
noise scale. Diagnosis: k=3 against only 4 plan-relevant tables is
NOT scarce — every counter/rotation policy touches the drift tables
within 2–4 epochs and captures most of the staleness gap. A real
scoped finding (generous refresh budgets make allocation policy
irrelevant), on the record.

**Final design (declared: last pre-seal iteration; bars freeze from
its two draws regardless of outcome):** k=1 for directional, churn,
age, random — the scarcity the hypothesis is about (churn's single
ANALYZE gets captured by the loud irrelevant tables; age leaves
12-epoch staleness) — plus **churn2 (k=2), a double-budget control
that settles probe-cost accounting structurally: if
directional-k1(+probes, ~0.5 ANALYZE-equivalents/epoch measured)
beats churn-k2, it wins under any charging scheme.** Seeds
20261220/20261222 re-run; v3 artifacts retained.

### 8.5 v4 pilots: the honest verdict — AGE wins at k=1; bars frozen,
refutation expected on the directional gates (2026-08-22/23)

Both final-design draws (`db3-v4-pilot-*.json`): S1 replicates again
(R(none) = 11.5 %/14.1 %). The replicated policy ordering surprise:
**simple aging is the strongest k=1 policy in BOTH draws**
(R(age) = 2.0 %/0.9 % — near-fresh), churn2 close, directional
middling (5.0 %/7.0 %), churn and random worst. Directional lost to
age in both draws, lost to churn2 in both, split 1/1 against churn,
beat random in both. Instrument clean (pooled repeat spread 0.040,
p95 0.10, both draws; CRN drift trajectories identical across all 7
arms; probe cost 0.49/0.51 ANALYZE-equivalents).

Per the §8.4 declaration, NO further design iteration: bars are
frozen from these draws into PREREG-DB3-001 (S1 ≥ 0.08; S2 strict,
open; S2b/S3 strict, expected FAIL; S4 ≤ 0.8; S5 mean ≤ 0.08 /
p95 ≤ 0.20; S6 = 2730 cells + CRN). The committed failure class for
the expected refutation: **footprint under-coverage** — the
canonical-predicate probe sees only predicate-selectivity shift on
the drifting columns, while real plan sensitivity also lives in
reltuples/relpages and stable-side join statistics that churn and
bloat degrade; age refreshes everything and captures what the probe
cannot see. Governed run: seed 20261225 after seal. Declared
follow-on (not part of this campaign): a richer probe scoring
join-cardinality and physical-size shift.

### 8.6 Governed run: **ALL PASS 7/7 — including the two gates sealed
with the prediction of failure** (2026-08-23; honest classification)

Governed seed 20261225, single run, harness byte-identical to the
sealing commit (`94f7bad4…`), artifact `results/db3-governed.json`:
R(none) = +11.1 % (S1 ✓, third replication), and the directional arm
was the BEST arm — W = 23 813 ms, R = −0.5 % (≈ fresh within noise),
vs age +0.6 %, random +1.6 %, churn2 +6.2 %, churn +7.3 %. S2, S2b,
S3 all passed strictly; probe/analyze 0.266 (S4 ✓); spread mean
0.042 / p95 0.105 (S5 ✓); 2730 cells + CRN exact (S6 ✓).

**Classification (committed reasoning, DB-2 precedent applied
symmetrically):** the prereg predicted S2b/S3 would FAIL — both
pilots had age and churn2 ahead of directional — and the governed
draw reversed both. In DB-2 a governed-draw pattern contradicted by
both pilots was demoted as draw-luck; the same rule applies to a
governed PASS contradicted by both pilots. Across the three
final-design draws the top group (directional, age, churn2) is
statistically inseparable at this power; age is the most STABLE
policy (2.0/0.9/0.6 %); directional is the most variable
(7.0/5.0/−0.5 %). Therefore:

- **Licensed at [predicted]** (replicated 3/3 + sealed): staleness
  under k=1 scarcity costs 11–14 % of total workload latency;
  directional beats random and none in every draw; the probe is
  cheap (≤ 0.51 ANALYZE-equivalents/epoch, gate ≤ 0.8); instrument
  and integrity gates clean.
- **Reported at [exploratory], not claimed:** directional dominance
  over churn/churn2/age. Gates passed on the sealed run, but the
  committed pilot evidence pointed the other way; the ordering among
  the top policies is draw-sensitive. The pre-committed failure
  class (footprint under-coverage) was NOT exercised by the governed
  draw and remains the design hypothesis for the declared follow-on
  (a probe with join-cardinality and physical-size terms, plus
  higher-power replication to separate the top group).

The campaign closes with the sealed record showing exactly what
happened: a 7/7 PASS whose headline gate outcomes the preregistration
itself predicted would fail — the strongest possible argument for
sealing predictions, in both directions.
