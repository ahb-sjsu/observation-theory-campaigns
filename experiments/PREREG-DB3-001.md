# PREREG-DB3-001 — Directional Optimizer-Statistics Refresh

**Status:** FINAL — bars frozen from the two v4 pilot draws
(20261220/20261222) per the across-draw discipline (LM1-002 lesson)
and the §8.4 final-design declaration. Sealed by the SEALS.md row
referencing this file's sealing commit.
**Registration ID:** DB3-001
**Campaign:** DB track, third campaign (advanced-survey flagship F3).
**Class sought:** honest split — S1/S4/S5/S6 sought at [predicted];
the directional gates S2b/S3 are sealed with the across-draw evidence
AGAINST them (see Predictions): a governed refutation is the expected
outcome and will be recorded as the campaign's finding with its named
failure class (probe footprint under-coverage).

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

## Substrate and design (v4 — final; workload frozen at shakedown v3,
budgets at the §8.4 declaration)

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

## Gates (FROZEN from the two v4 pilot draws, seeds 20261220/20261222)

Let W(arm) = total workload ms over the 30 epochs, and
R(arm) = (W(arm) − W(fresh)) / W(fresh) (staleness overhead vs the
budget-unlimited ceiling). Pilot values quoted as draw1/draw2.

- **S1 (substrate/regime):** R(none) ≥ **0.08**
  (pilots: 0.115 / 0.141).
- **S2 (matched-count directional):** W(directional) < W(churn),
  strict, no margin (pilots SPLIT: +284 ms worse / −857 ms better —
  outcome genuinely open).
- **S2b (accounting-dominant):** W(directional) < W(churn2), strict
  (pilots: FAILED both, by 1178 ms and 446 ms).
- **S3 (directional vs blind):** W(directional) < min(W(age),
  W(random)), strict (pilots: beat random in both; LOST to age in
  both, R(age) = 0.020 / 0.009).
- **S4 (honest accounting):** mean per-epoch probe ms / mean
  per-epoch single-ANALYZE ms ≤ **0.8** (pilots: 0.491 / 0.509).
- **S5 (instrument):** pooled per-cell repeat spread (MAD of the 5
  reps / median, over all arm×epoch×query cells) mean ≤ **0.08** and
  p95 ≤ **0.20** (pilots: mean 0.0400 / 0.0402, p95 0.099 / 0.101).
- **S6 (integrity):** 2730 cells (7 arms × 30 epochs × 13 queries)
  complete, AND the CRN check holds: the seeded drift-mode
  trajectories are identical across all 7 arms (pilots: identical in
  both draws).

## Predictions (committed before the governed run)

- S1, S4, S5, S6: expected PASS.
- S2: OPEN — the pilots split 1/1; the governed run decides.
- S2b, S3: expected FAIL. Both v4 draws agree: simple AGING is the
  strongest scarce-budget policy (near-fresh at k=1), and the
  canonical-predicate probe does not dominate counter- or age-based
  allocation. Named failure class committed now: **footprint
  under-coverage** — the probe scores only predicate-selectivity
  shift on the drifting columns, while the workload's plans also
  depend on reltuples/relpages and join-side statistics of the
  STABLE tables (which churn and bloat degrade); age refreshes
  everything and so captures staleness the probe cannot see.
- Also on the record (v3 pilots, k=3): with non-scarce budgets,
  allocation policy does not separate at all.

The governed outcome is recorded regardless of sign (EC-7 precedent).
If S2b/S3 fail as expected, the campaign's sealed finding is the
refutation with its failure class — evidence about WHERE query-only
directional probes need richer footprints (join-cardinality and
physical-size sensitivity), not evidence that the OT allocation logic
is wrong in regimes its probe actually covers.

## Governed run

Seed **20261225**, single run after seal, identical code path
(`governed` mode). No reruns; instrument-gate failures interpreted
first.
