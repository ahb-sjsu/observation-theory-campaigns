# PREREG-DB2-001 — DB-2: the multi-consumer alignment tax for shared precision budgets

**SEALED at the commit ledgered in `SEALS.md`.** The governed run executes
ONCE after the sealing commit, on the governed seed below, and is reported
regardless of sign in the track document and README status ledger.

## Coordination boundary (binding)

Per [`DATABASE-TRACK.md`](DATABASE-TRACK.md) §0: no claims about replica
routing, freshness certificates, replication, or fleets (ceded to the
concurrent network-governor XPROTO-GEO program). The decision variable
is one shared per-column PRECISION budget serving two consumers.

## Claim under test

Survey headline cell B (OT×Databases survey): when one precision budget
must serve two consumers, sharing carries a **geometric tax** — exactly
free when the consumers' read structures coincide, materially positive
when they do not — and consumer-AWARE shared allocation beats
task-blind shared allocation on the egalitarian worst-of-two. EC-6's
result transplanted from sensor schedules to database physical design,
with exhaustive optimization (all C(8,4) = 70 budget subsets evaluated
per consumer per instance) so shared-best and utopia are EXACT optima
and the tax cannot be an optimizer artifact.

**Disclosed respecification (pilot A, replicated in pilot B):** the
naive EC-6 transplant predicted the tax monotone in support-overlap
COUNT. Both pilot draws refute that parameterization on this
substrate: partial overlaps price HIGHER than disjoint supports (o = 1
above o = 0 in both draws), because at partial overlap both consumers'
interaction terms contend for the same high-value columns. **The tax
tracks value-weighted geometric alignment, not set arithmetic** — a
sharpening of OT's own claim, and the reason the sealed gates use
pooled/min forms over non-identical overlaps while monotonicity-in-
count is a reported diagnostic, never gated.

## Design (frozen; harness `python/db2_tax.py`)

DuckDB in-memory, fully deterministic at the seed. n = 10,000 rows,
d = 8 ~ N(0,1); m = 150 query rows; consumers = SQL k-NN (k = 25)
reports vs noiseless external truth (as DB-1); per-consumer target
y_i = Σ_{p∈S_i} c_p x_p + 0.5·x_{s0}x_{s1} + ε(0.5), coefficients
seeded per instance. Support_A = {1,2,3,4}; Support_B at overlap o ∈
{4,2,1,0} per the harness table. Budget = exactly 4 of 8 columns fine
(fine = raw double; coarse = ROUND(x)). Per overlap, N = 5 seeded
instances. Per instance: all 70 subsets evaluated for both consumers;
tax = max_i loss_i(shared-best) / max_i loss_i(utopia_i); task-blind
baseline = mean worst-of-two over 4 seed-drawn subsets distinct from
shared-best and both utopia argmins (LM2-002 degeneracy-proof
construction). Instrument: bitwise recompute; exact eval-run ledger.

## Two disclosed powered calibration draws

| | pilotA (20261210) | pilotB (20261212) |
|---|---|---|
| tax at identical supports | **1.0000** | **1.0000** |
| tax by overlap 2/1/0 | 1.0695 / 1.0761 / 1.0550 | 1.0537 / 1.0841 / 1.0738 |
| mean non-identical | 1.0669 | 1.0705 |
| min non-identical | 1.0550 | 1.0537 |
| aware-vs-blind pooled | +0.2321 | +0.2169 |
| deterministic / eval runs | true / 2,820 | true / 2,820 |

```yaml
id: PREREG-DB2-001
date: 2026-08-21
retrospective: false
kind: multi-consumer alignment tax for one shared per-column precision
      budget (DB-2; EC-6 transplanted to physical design; exhaustive
      shared-best and utopia)
harness: python/db2_tax.py
code_hash: sha256:a9e14f3d5ba3a02b8203c7ac0a4d712c3a4083a4ed40a4ab7cfb69a0c532d534
governed_seed: 20261215
calibration_seeds: [20261210, 20261212]
frozen_config:
  n_rows: 10000
  m_query: 150
  d: 8
  k_nn: 25
  f_fine: 4
  n_inst: 5
  n_rand_baseline: 4
  noise: 0.5
  overlaps: [4, 2, 1, 0]
sealed_gates:
  T1: tax at identical supports <= 1.02 - sharing exactly free when
      geometries coincide (cal 1.0000 / 1.0000)
  T2: mean tax over non-identical overlaps >= 1.03 (cal 1.0669/1.0705)
  T3: min cell-mean tax over non-identical overlaps >= 1.02
      (cal 1.0550 / 1.0537)
  T4: consumer-aware shared allocation beats task-blind shared
      allocation, pooled worst-of-two improvement >= 0.10
      (cal 0.2321 / 0.2169)
  T5: bitwise determinism of the recompute instrument (cal true both)
  T6: eval-run ledger == 2820 (cal 2820 both)
ungated_diagnostics: [monotonicity-in-overlap-count (REFUTED in both
      pilots - the value-weighted-alignment finding), per-instance tax
      tables, shared-best allocations]
stopping: fixed-n, single governed run
falsification: T1 fail -> sharing costs even at coincident geometry
  (the tax is not geometric). T2/T3 fail -> no material tax exists at
  this budget - the survey's headline cell B claim fails, reported as
  the campaign's answer. T4 fail -> awareness adds nothing over blind
  sharing. T5/T6 fail -> instrument broken, no other gate interpreted
  (EC-7 discipline). All reported at equal prominence.
amendments: []
```

## Scope and non-claims

Two consumers, equal weights, egalitarian endpoint; synthetic data and
planted similarity consumers on one engine; overlap-count is the
CONSTRUCTION variable, not the claimed alignment measure (the pilots
showed value-weighted alignment governs — formalizing that index is a
declared follow-on, not claimed here); m > 2 consumers and asymmetric
priorities are future work; no optimality claim beyond the exhaustive
search within the declared subset family. Class on pass: `[predicted]`.
