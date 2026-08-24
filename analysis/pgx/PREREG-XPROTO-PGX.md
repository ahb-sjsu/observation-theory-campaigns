# PREREG-XPROTO-PGX — production Postgres replication-staleness cell

**STATUS: SEALED 2026-08-21.** FAMILY-CONSTRUCTED: 2026-08-20. Construction +
family shakedown only; the earliest compliant seal is **2026-08-21**
(`pgx_check.py` enforces the cooling-off in code). Graded on seeds
{20260821, 20260822, 20260823}, disjoint from the shakedown's {0, 1, 2}.
No evidential weight until sealed and run.

**IP posture:** repo is private and stays private for now (owner
decision 2026-08-20; the owner does not regard the mechanism IP as
worth gating disclosure — see the project IP-stance note — but the repo
stays private pending a deliberate release moment). No provisional-patent
hold on this cell.

## Why this cell exists — the production graduation

XPROTO-PG (sealed 2026-08-20, PASS) earned the consumer-relative
staleness mechanism in a **lab**: it *declared* the two consumer
footprints (`hot_a`/`hot_b`) and *dialed* the replication lag with a
clean deterministic `recovery_min_apply_delay = 1000 ms`. Its own scope
section deferred the production cell as a later campaign. This is that
cell. It relaxes exactly the two controlled things:

1. **Footprint is MEASURED, not declared.** Each consumer's footprint is
   *derived from the replica's `pg_stat_statements`* — the tool learns
   what the consumer actually reads from its query stats — over a
   multi-relation join workload where the answer is non-obvious. This is
   the production footprint mechanism (the same path pg-governor uses),
   and it gets its own manipulation check (MC4): if the derivation does
   not recover the intended relations, the cell VOIDs.
2. **Lag is EMERGENT, not dialed.** The replica sits behind a WAN-style
   `netem` delay+jitter (`lab_up.sh`, ~300 ms ± 120 ms) under a real
   write load, so the naive monitor faces a fluctuating lag
   *distribution* that arises from link × load rather than a fixed hold.
   MC3 requires that variation to be realized (a lag-std floor) — a cell
   with a suspiciously constant lag is not a production regime and VOIDs.

## The claim

On a Postgres primary/replica pair under emergent WAN-style lag, the
standard replication monitor — `now() − pg_last_xact_replay_timestamp()`
against a threshold — is **two-sidedly vacuous for heterogeneous
consumers whose footprints are measured, not declared**: no threshold
simultaneously avoids false-clears for a consumer reading heavily-written
relations and false-alarms for a consumer reading rarely-written ones. A
**WAL-witnessed certificate over the measured footprint** (no change to
consumer *i*'s derived footprint past the replica's replay LSN) is
correct in both directions for both consumers, dominating the naive
monitor's entire threshold curve.

## Family F-PGX (constructed + shaken down 2026-08-20)

Lab (`lab_up.sh`/`lab_down.sh`): `postgres:16` primary
(`wal_level=logical`, `shared_preload_libraries=pg_stat_statements`) +
async streaming replica (**no apply-delay**) whose link carries a
`netem` WAN delay+jitter; two login roles `consumer_hot`/`consumer_cold`.
Schema: hot relations `orders`, `order_items` (written together every hot
event); cold relations `catalog`, `category` (written together, rarely).
Sealed constants (`fam_pgx.py`): thresholds {0.1, 0.5, 1, 2, 5} s;
duration 120 s; 20 s busy/quiet phases; hot rate [4,6]/s; cold spacing
[6,10] s. The seed draws the schedule. **Sampling + guard are DERIVED per
cell** (shakedown-corrected 2026-08-20): the substrate's minimum
replication latency is measured by probing, `tick = clamp(0.3·min_lat,
[0.01, 0.03])` (fine relative to the transit), and the beacon `guard =
2·tick` — the guard covers only the measurement sampling skew (a write
enters `last_change` at the next slot pull, ≤ tick later), NOT the
replication latency; the false-alarm band is (0, guard), so a small guard
is correct. This rule generalizes to real geo (tens-of-ms lag → ~10 ms
ticks).

Consumers: HOT reads `orders ⋈ order_items` (intended footprint
{orders, order_items}); COLD reads `catalog ⋈ category` (intended
{catalog, category}). Each runs its query on the replica; the footprint
is **derived from `pg_stat_statements`** and must match the intended set.
Witness = logical-decoding slot, per-relation max change LSN vs the
replica's replay LSN. Ground truth per tick is exact from the beacon
schedule (writes carry per-relation sequence + commit time).

## Bars (bind at seal; checked against the family record first)

Set slightly looser than the XPROTO-PG lab twin (0.25 / 0.10 / 3×)
because measured footprints and emergent lag add real noise the clean lab
did not have — each loosening is a deliberate, justified concession, not
a fit to the data, and every bar is validated against the committed
`PGXREP-family.json` (`pgx_check.py --check-family`) before the seal.

- **B1 — two-sided naive vacuity.** Per seed:
  `min over thresholds T of max(fc, fa over both consumers)(T) ≥ 0.20`.
- **B2 — witness correctness.** Per seed: certificate worst error across
  both consumers and both directions `≤ 0.12`.
- **B3 — dominance.** Per seed: witness worst-error `≤ naive-minmax / 2.5`.

**Manipulation checks (bars too):**
- **MC1** HOT truth-stale fraction in [0.15, 0.85] per seed.
- **MC2** COLD truth-stale fraction < HOT per seed.
- **MC3** ≥ 100 `orders` writes, ≥ 8 `catalog` writes, max busy-phase lag
  ≥ 0.5 s, **and lag-std ≥ 0.10 s** (emergent variation realized) per seed.
- **MC4 — footprint-derivation fidelity.** The footprints derived from
  `pg_stat_statements` must equal the intended sets for BOTH consumers
  per seed. This guards the production mechanism itself; a derivation
  miss is an instrument failure, not a claim.

**Verdict rule:** any MC failure → VOID (instrument, not claim); all MCs
pass and all bars pass on every graded seed → PASS; otherwise FAIL, kept
as executed.

**Kills.** `naive-minmax < 0.12` on the graded seeds — the deployed
monitor is adequate under production lag and the claim is refuted for
this substrate; or witness worst-error `> 0.25` — the witnessed
certificate does not survive production noise. Either is reported.

## Seal procedure

On 2026-08-21 or later: `pgx_check.py --check-family` (must PASS), reread
this prereg, flip STATUS to `SEALED <date>`, commit, bring the lab up,
run `pgx_check.py`, commit `XPROTO-PGX-graded.json` as executed.

## Scope

Still a lab: `netem` stands in for WAN geo-replication (the lag is now a
fluctuating *distribution* from link × load rather than a deterministic
hold — a genuine graduation from the lab knob, but a lab nonetheless),
and the workload is synthetic. What is *no longer* controlled: the
footprint (measured from `pg_stat_statements`, not declared) and the lag
shape (emergent, must vary). A PASS earns the production footprint
mechanism and turns the taxonomy's PG entry from "mechanism in a clean
lab" into "mechanism under measured footprints and uncontrolled lag." A
fully-uncontrolled cell (real application workload, real geo link, e.g.
the roaming trial's data) is the next graduation after this one.
Exact-consistency mechanisms (`remote_apply`, LSN tokens) remain out of
scope. Prior-art positioning (PBS, PNUTS, consistency SLAs) per the
replication survey.

## Provenance

- Graduation of the sealed `PREREG-XPROTO-PG.md` (2026-08-20 PASS).
- Family: `fam_pgx.py` + `PGXREP-family.json` (seeds {0,1,2}).
- Graded runner: `pgx_check.py` (seal-guard + coded cooling-off +
  pre-seal record check + MC4 footprint-fidelity guard).
