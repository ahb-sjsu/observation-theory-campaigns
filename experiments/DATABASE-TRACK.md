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

## 5. Roadmap

Pilot draws A/B (powered) → freeze → seal PREREG-DB1-001 → single
governed run → DB-2 pilots. Nothing here is claim-bearing.
