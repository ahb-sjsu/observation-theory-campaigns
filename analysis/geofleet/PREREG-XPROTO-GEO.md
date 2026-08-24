# PREREG-XPROTO-GEO — the geo-fleet cell (nearest-CERTIFIED routing)

**STATUS: SEALED 2026-08-22.** FAMILY-CONSTRUCTED: 2026-08-21. Earliest compliant
seal **2026-08-22** (`geo_check.py` enforces the cooling-off in code).
Graded on seeds {20260822, 20260823, 20260824}, disjoint from the
shakedown's {0,1,2}. No evidential weight until sealed and run on the
graded seeds against a live fleet.

**IP posture:** public methodology (companion to the replication survey +
the 802.11 RFC's consumer-relative-routing idea); nothing gated. Repo
private for now per the owner's stance.

## The claim — dominance on two orthogonal axes

On a real geo-distributed Postgres fleet (primary + N streaming replicas
across distinct NRP sites), three routers place each consumer on one
replica. A consumer is a **footprint** (the relation it reads). Two axes:

- **freshness** — false-clear = routed to a replica **stale for that
  footprint** (the consumer reads stale data);
- **locality** — mean RTT of the chosen replica from the consumer vantage.

The routers: **nearest** (lowest RTT — ignores freshness; the
dynamic-snitch heuristic), **leastlag** (lowest *global* replication lag —
ignores the specific footprint and locality), and **cert** (the
consumer-relative witnessed certificate: the nearest replica CERTIFIED
fresh for the footprint; else the primary).

**Claim:** the certificate is **fresher than nearest** and **more local
than leastlag** — it beats each naive router on the very axis that router
optimizes, and is correct in absolute terms. This is the survey's
geo-fleet cell realized on real infrastructure; it needs genuine
geographic diversity (which the pilot has: CSU Bakersfield / SD School of
Mines / SDSC-UCSD) so that the nearest replica is sometimes stale while a
farther one is fresh.

## Family F-GEO (constructed + shaken down 2026-08-21)

Substrate: the live Phase-2 pilot fleet (`geofleet_pilot.sh`) — primary +
3 zone-spread streaming replicas in `ssu-atlas-ai`. The cell runs as an
in-cluster Job (`fam_geofleet.py`, reaching the primary + every replica),
orchestrated from Atlas. Per tick, per replica: RTT (median SELECT-1
round-trip), global replication lag, replay LSN, and per-relation visible
seq. **Witness** (no logical decoding): the writer captures
`pg_current_wal_lsn()` per footprint write; certified(replica, F) iff
replay LSN ≥ F's last-write LSN. **Ground truth**: beacon seq per relation
on each replica vs the primary's committed seq (guarded 200 ms) —
independent of the LSN witness. Consumers: HOT (footprint `orders`,
heavily written) and COLD (footprint `catalog`, rarely written). The seed
draws the write schedule; each seeded cell rebuilds fresh relations.

**Staleness induction (disclosed).** The NRP backbone is fast: natural
inter-zone replication lag (~ms) is below the 200 ms truth guard, so no
replica is ever stale and the routing decision is degenerate (the
2026-08-21 shakedown VOIDed on MC1/MC4 for exactly this reason). The cell
therefore *induces* the freshness axis: a `Pauser` rotates
`pg_wal_replay_pause()` across the replicas one at a time (period 6 s,
seeded order), so at any moment one replica is behind on the hot
footprint. This is a controlled, disclosed stand-in for maintenance /
load / network-lag events (cf. the roaming trial's replay-pause). The
**locality axis stays real** — RTT is the measured inter-zone network
latency (rtt_spread ~8× on the pilot); only the **freshness axis** is
induced. The certificate, witness, and routing logic are unchanged; the
pause only guarantees there is staleness to route around.

## Bars (bind at seal; checked against the family record first)

The bars encode the two-axis dominance. HOT is where routing is
contested (COLD is usually fresh everywhere). Every bar must hold on each
graded seed (`geo_check.py --check-family`) before the seal.

- **B1 — certificate correct.** HOT: `cert.fc ≤ 0.05`.
- **B2 — fresher than nearest.** HOT: `cert.fc ≤ nearest.fc / 3` (the
  certificate dominates the nearest-RTT router on the freshness axis).
- **B3 — more local than leastlag, near-optimal locality.** HOT:
  `cert.mean_rtt ≤ leastlag.mean_rtt` AND `cert.mean_rtt ≤ 1.3 ×
  nearest.mean_rtt` (the certificate is more local than the lag-blind
  router, and pays only a small locality tax over pure-nearest to gain
  freshness).

**Manipulation checks (bars too):**
- **MC1 — nearest can fail.** HOT `nearest.fc ≥ 0.15`: the nearest replica
  is materially stale for the footprint (a non-degenerate regime; if the
  nearest replica is always fresh there is no story). *(Kill if < 0.05.)*
- **MC2 — real geographic locality.** `rtt_spread ≥ 1.5` (the farthest
  replica's mean RTT is ≥ 1.5× the nearest's — genuine geo differences;
  if all RTTs are equal, "nearest" is meaningless).
- **MC3 — fleet healthy + activity.** `n_replicas ≥ 3`, all converged to
  the fresh generation, `hot_writes ≥ 300`.
- **MC4 — consumer-relativity realized.** `footprint_dependence ≥ 0.05`
  (on ≥ 5% of ticks the certificate routes HOT and COLD to *different*
  replicas — the decision is footprint-relative, not a global choice).

**Verdict rule:** any MC failure → VOID (instrument, not claim); all MCs
pass and B1–B3 pass on every graded seed → PASS; otherwise FAIL, kept as
executed.

**Kills.** HOT `cert.fc > 0.20` (the certificate does not deliver) — or
HOT `nearest.fc < 0.05` (no geo-vacuity on this fleet: the nearest replica
is always fresh, so consumer-relative routing buys nothing here — the
claim is refuted for this substrate). Either is reported.

## Seal procedure

On 2026-08-22 or later, with a live fleet: run the shakedown → commit
`GEOREP-family.json`; `geo_check.py --check-family` (must PASS); reread
this prereg; flip STATUS to `SEALED <date>`; commit; run the graded Job
(seeds {20260822-24}); commit `XPROTO-GEO-graded.json` as executed.

## Scope

The fleet is real (distinct NRP sites, genuine inter-site latency), the
workload synthetic (seeded beacons), the consumer vantage the Job pod's
zone. A PASS earns the nearest-CERTIFIED routing result on a real geo
fleet — the certificate dominating both naive routers — not a
production-traffic claim. The lag is emergent (real inter-zone network),
so there is no netem here; this is the external-validity graduation of the
netem-lab XPROTO-PGX. Prior art (Cassandra dynamic snitch = the nearest
router; PBS; session guarantees) positioned in the replication survey.

## Provenance

- Substrate: `geofleet_pilot.sh` (Phase-2 pilot, live).
- Measurement: `fam_geofleet.py`; shakedown `GEOREP-family.json` (seeds
  {0,1,2}) — no evidential weight.
- Graded runner: `geo_check.py` (seal-guard + coded cooling-off +
  pre-seal record check).
- Driver: `run_geofleet.sh` (Atlas-side: discover replicas → ConfigMap →
  submit the measurement Job → collect the result).
