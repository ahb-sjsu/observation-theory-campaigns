# PREREG-DB3-001 — Directional Optimizer-Statistics Refresh

**Status:** DRAFT — bars PENDING PILOT; do not seal until both v2
pilot draws are on the record and every `⟨PENDING⟩` below is frozen
from the ACROSS-DRAW distribution (LM1-002 lesson).
**Registration ID:** DB3-001
**Campaign:** DB track, third campaign (advanced-survey flagship F3).
**Class sought:** [predicted].

## Coordination boundary (binding)

Single-node optimizer-statistics scheduling only. No replicas, no
read routing, no replication lag, no freshness certificates, no
fleet claims — that territory is XPROTO-GEO's
(`C:\source\network-governor\analysis\geofleet\PREREG-XPROTO-GEO.md`).

## Hypothesis

When ANALYZE budget is scarce under drift (k=1 table/epoch against
12 tables of which 4 are plan-relevant), allocating it by a
query-only probed plan-sensitivity signal (rollback mini-ANALYZE +
canonical predicate re-EXPLAIN per footprint table) yields lower
total workload latency than allocating it by modification counters
(the industrial baseline), age, or random at matched count — and
lower even than a DOUBLE-budget churn arm (k=2), which settles the
probe-cost accounting under any charging scheme (measured probe cost
~0.5 ANALYZE-equivalents/epoch, logged per epoch).

This is the OT allocation consequence (budget to the directions
where the consumer's observation geometry is sensitive, tr(P̂ Σ)
logic) transplanted to optimizer statistics: modification counters
measure Σ (change) alone; the probe measures P̂ (plan sensitivity)
composed with change.

## Substrate and design (v2 — frozen at shakedown v2)

PostgreSQL 16.15, project-owned cluster localhost:5544 on Atlas
(autovacuum off, random_page_cost 1.1, work_mem 64MB,
default_statistics_target 1000 for real refreshes = full-row read at
200k rows → deterministic stats; probe target 10).
12 tables × 200k rows (drift t00–t03 / stable-churn t04–t07 /
loud-irrelevant t08–t11), 13-query workload — all joins in the
one-side-filtered shape where the planner is verified truth-unbiased
at rpc 1.1: 4 drift×stable joins QJ*, 4 cross-pair joins QX*, 4
window aggregates QS*, 1 stable control QC4. Both-sides-filtered
joins are a documented scoped EXCLUSION (no page-cost value
calibrates both join shapes — `DATABASE-TRACK.md` §8.3). b-indexes
everywhere, seeded mode-walk drift transiting the predicate window.
Regime validation (v3 shakedown): 35/35 flip instances fresh-faster,
net +2.72 s, flips at transit epochs 13–19 across all 8 flip-capable
queries. Harness `python/db3_stats_refresh.py` at the sealing
commit; full design rationale and shakedown history in
`DATABASE-TRACK.md` §8–8.3 (including the v1 20k-row substrate
invalidation and endpoint respec, disclosed pre-seal).

**Endpoint:** per arm, total workload latency per epoch = Σ over the
13 queries of the median of 5 timed executions (1 warm-up discarded),
pooled over 30 epochs; CRN (identical seeded data trajectory) across
arms. Logged-response posture: raw per-rep timings in the artifact.

**Arms:** directional (k=1 + logged probes), churn (k=1 by
rows-modified-since-last-arm-ANALYZE, verified arm-side mirror),
churn2 (k=2 double-budget control), age (k=1 oldest-first), random
(k=1 seeded), none (floor), fresh (ANALYZE-all ceiling).

## Gates (ALL must pass; bars frozen from the two v4 pilot draws)

Let W(arm) = total workload ms over the 30 epochs, and
R(arm) = (W(arm) − W(fresh)) / W(fresh) (staleness overhead vs the
budget-unlimited ceiling).

- **S1 (substrate/regime):** R(none) ≥ ⟨PENDING⟩ — staleness is
  materially costly in this regime (v3 pilots: +12.1 %/+12.5 %).
- **S2 (load-bearing):** W(directional) < W(churn) by margin
  ⟨PENDING⟩ at matched k=1.
- **S2b (accounting-dominant):** W(directional) < W(churn2) by
  ⟨PENDING⟩ — beating double budget closes probe-cost charging.
- **S3:** W(directional) < min(W(age), W(random)) by ⟨PENDING⟩.
- **S4 (honest accounting):** directional probe cost reported per
  epoch; mean probe ms / mean single-ANALYZE ms ≤ ⟨PENDING⟩.
- **S5 (instrument):** pooled per-query repeat spread (median
  absolute deviation of the 5 reps / median) ≤ ⟨PENDING⟩; queries
  exceeding it documented, endpoint recomputed excluding them as a
  sensitivity note.
- **S6 (integrity):** 7 arms × 30 epochs × 13 queries complete;
  seeded reproduction of all non-timing quantities (plans chosen,
  tables chosen, drift trajectory) exact on re-run.

## Prediction

Directional < churn/age/random and < churn2 on W; churn's single
ANALYZE is captured by the loud irrelevant tables most epochs; age
leaves 12-epoch staleness; none pays the largest R. Outcome recorded
regardless of sign; misses stay on the record (EC-7 precedent). The
v3 finding stands alongside: at k=3 (non-scarce), allocation policy
does not matter — scarcity is the regime of the claim.

## Governed run

Seed **20261225**, single run after seal, identical code path
(`governed` mode). No reruns; instrument-gate failures interpreted
first.
