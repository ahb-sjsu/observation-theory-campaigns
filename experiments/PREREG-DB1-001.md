# PREREG-DB1-001 — DB-1: per-column precision allocation by probed consumer sensitivity

**SEALED at the commit ledgered in `SEALS.md`.** The governed run executes
ONCE after the sealing commit, on the governed seed below, and is reported
regardless of sign in the track document and README status ledger.

## Coordination boundary (binding)

Per [`DATABASE-TRACK.md`](DATABASE-TRACK.md) §0: this campaign claims
nothing about replica routing, read placement, freshness certificates,
replication lag, or fleet substrates — that cell belongs to the owner's
concurrent `network-governor` program (PREREG-XPROTO-GEO). The decision
variable here is per-column STORAGE PRECISION at a matched budget.

## Claim under test

Survey headline cell A (OT×Databases survey, geometric-observation
@95fd920): per-column storage precision allocated by a QUERY-ONLY
probed sensitivity of downstream consumers' answer quality beats
task-blind allocation at a matched precision budget, with the blind
allocation capturing the planted-oracle advantage and the anti-aligned
allocation not meaningfully better than task-blind. Consumers are SQL
k-NN report programs over a DuckDB store, judged against EXTERNAL
ground truth. On pass, class `[predicted]`: the tr(P̂ Σ) allocation
consequence instantiated on a database physical-design decision.

**Explicit scoped negative carried as a finding, never gated:** the
quantize-the-unread effect (coarsening unread columns actively
HELPING) measured ≈ 0 at step-1.0 coarsening in both pilot draws
(pooled +0.001/−0.027, sign-varying) — at this design point coarse is
FREE, not prophylactic, for similarity consumers. The coarseness step
was NOT retuned to chase the effect; whether a helps-regime exists at
coarser steps is a declared open question (Q4 reported ungated).

**Prior-art posture (recon-grade, sealed as-is; quote-verification of
the named works is owed before any publication citing them):**
SPARTAN (declared per-column tolerances), QoI-preserving compression
(closed-form downstream functions), compression-aware physical design
(lossless, cost-only), self-tuning histograms (access-pattern-driven)
conceded; probed-sensitivity precision allocation unoccupied per the
2026-08-21 recon.

## Design (frozen; harness `python/db1_precision.py`)

DuckDB in-memory, fully deterministic at the seed. n = 20,000 rows,
d = 8 columns ~ N(0,1); external targets y_A = x1 + x2² − x3 + ε,
y_B = x5·x6 + ε (ε ~ N(0, 0.5²)); consumers = SQL k-NN (k = 25)
neighbour-mean reports over ALL stored encoded columns for m = 200
query rows; loss = MSE vs the noiseless true target. Encoding: fine =
raw double, coarse = ROUND(x) (step 1.0); budget = exactly 4 of 8
fine. Probe: coarsen one column at a time, Δloss vs all-fine (16 runs,
ledger-checked). Arms at matched budget, CRN exact: aligned (top-4 by
Δ), oracle (planted support padded by Δ), anti (bottom-4), mean-4
degeneracy-proof task-blind baseline (LM2-002 construction),
all-coarse/all-fine references. Instrument: bitwise recompute of the
aligned arm; probe-run ledger.

## Two disclosed powered calibration draws

| | pilotA (20261201) | pilotB (20261203) |
|---|---|---|
| pooled Q1 (aligned vs baseline) | +0.2228 | +0.1809 |
| per-consumer | 0.3026 / 0.1431 | 0.1590 / 0.2028 |
| capture | 1.0000 (all cells) | 1.0000 (all cells) |
| pooled anti | −0.2031 | −0.4178 |
| Q4 diagnostic (vs all-fine) | +0.0009 | −0.0272 |

Note recorded honestly: the probe recovered the planted supports
EXACTLY in all four cells, making aligned ≡ oracle and the capture
gate near-vacuous at this problem size; the informative gates are
Q1/Q1b/Q3. Bars below across-draw minimums with margin (the LM1-002
lesson).

```yaml
id: PREREG-DB1-001
date: 2026-08-21
retrospective: false
kind: per-column precision allocation by probed consumer sensitivity
      (DB-1; DuckDB-local; coordination boundary with XPROTO-GEO
      recorded)
harness: python/db1_precision.py
code_hash: sha256:309334e4bd1964f7ca3fc44ced4e15a13b835660df99772098a0334b1f0a643c
governed_seed: 20261205
calibration_seeds: [20261201, 20261203]
frozen_config:
  n_rows: 20000
  m_query: 200
  d: 8
  k_nn: 25
  f_fine: 4
  n_rand_baseline: 4
  noise: 0.5
  coarse_step: 1.0
sealed_gates:
  Q1: pooled aligned-vs-mean4-baseline improvement >= 0.10
      (across-draw cal 0.2228 / 0.1809)
  Q1b: per-consumer floor >= 0.05 (cal min 0.1431)
  Q2: pooled capture of the oracle advantage >= 0.60 (cal 1.0000 both
      draws; near-vacuous here since aligned == oracle, retained at the
      program-standard bar)
  Q3: pooled anti improvement <= +0.10 (cal -0.2031 / -0.4178)
  Q5: bitwise determinism of the recompute instrument (cal true both)
  Q6: probe-run ledger == 16 (cal 16 both)
ungated_diagnostics: [Q4 aligned-vs-allfine (the quantize-the-unread
      scoped negative), probed deltas, arm allocations, loss tables]
stopping: fixed-n, single governed run
falsification: Q1/Q1b fail -> probed-sensitivity allocation does not
  pay on a database precision budget; the survey's headline cell A
  claim fails at this design point, reported as the campaign's answer.
  Q3 fail -> the advantage is not geometry-borne. Q5/Q6 fail ->
  instrument broken, no other gate interpreted (EC-7 discipline). All
  reported at equal prominence.
amendments: []
```

## Scope and non-claims

Synthetic data and planted similarity consumers on one engine; no
storage-byte realism claim (the ladder is a precision budget, byte
accounting is future work); no claim about routing, freshness, or
replication (boundary above); no optimality claim for top-k
allocation; the quantize-the-unread negative is scoped to step-1.0
coarsening and similarity consumers. Class on pass: `[predicted]`.
