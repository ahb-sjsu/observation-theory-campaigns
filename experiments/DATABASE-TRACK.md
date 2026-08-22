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

## 6. Roadmap

DB-2 (the alignment tax) pilots next; the step-dependence of
quantize-the-unread is a declared open question (own future seal, not
a retune); byte-realistic storage budgets a future refinement.
Boundary with XPROTO-GEO remains binding.
