# PREREG-XPROTO-MG — replication-staleness cell, MongoDB (the taxonomy's second database entry)

**STATUS: SEALED 2026-08-21.** FAMILY-CONSTRUCTED: 2026-08-20. Construction +
family shakedown only; the earliest compliant seal is **2026-08-21**
(`mongo_check.py` enforces the cooling-off in code and refuses to grade
before a dated seal). Graded on seeds {20260821, 20260822, 20260823},
disjoint from the shakedown's {0, 1, 2}. No evidential weight until
sealed and run.

**Disclosure gate (owner decision pending):** same gate as XPROTO-PG —
a possible provisional patent on the witnessed consumer-relative
certificate mechanism precedes any *public* disclosure of this cell. The
repo is private; this prereg records the gate so publication order is a
decision, not an accident.

## Why this cell exists — the twin

XPROTO-PG (sealed 2026-08-20, PASS) measured the vacuity of the naive
replica-lag monitor on **Postgres streaming replication**. XPROTO-MG is
its deliberate **twin** on **MongoDB replica-set replication**: same
claim, same bar shape, same stimulus schedule, a *different substrate
and a different witness* (the oplog rather than the WAL). The point is
generalization under the survey's organizing claim — a total-order log
(the oplog `ts`, like the WAL LSN) yields a scalar witness certificate —
and, per the replication survey, MongoDB is the strongest structural
twin because it *already ships* the consumer-relative knob (causal
sessions / `afterClusterTime`) yet publishes no measured false-clear
rate. This cell measures that rate.

## The claim

On a MongoDB primary / delayed-secondary pair, the standard replication
monitor — `now − secondary.optimeDate` (replica lag) against a threshold
— is **two-sidedly vacuous for heterogeneous consumers**: no threshold
simultaneously avoids false-clears for a bursty-footprint consumer and
false-alarms for a quiet-footprint consumer. An **oplog-witnessed,
footprint-aware certificate** (consumer *i* CERTIFIED iff no oplog entry
touching *i*'s footprint has `ts` past the secondary's applied optime
`ts`) is simultaneously correct in both directions for both consumers,
dominating the naive monitor's entire threshold curve.

Sealed cells so far: BGP 0.351 / IS-IS 0.184 / OSPF 0.083 / BMP
witness-grading / **XPROTO-PG** (Postgres). This is the second database
cell and the consumer-relativity (P1/P2) claim measured on a second
substrate's staleness face.

## Family F-MG (constructed + shaken down 2026-08-20)

Lab (`lab_up.sh` / `lab_down.sh`): `mongo:7` replica set `rs0` with a
primary and a **delayed secondary** (`secondaryDelaySecs = 1`,
`priority: 0`) — the analog of the PG cell's
`recovery_min_apply_delay = 1000 ms`. Sealed constants (`fam_mongo.py`):
thresholds {0.1, 0.5, 1, 2, 5} s; duration 120 s; tick 200 ms; truth
guard 200 ms; 20 s busy/quiet phases. The **seed** draws the busy-phase
write rate from [4, 6]/s and the quiet consumer's spacing from [6, 10] s
— identical to F-PG, so the two cells differ only in substrate. Each
seeded cell rebuilds fresh collections and re-baselines the oplog cursor.

Consumers: A's footprint = `hot_a` (bursty), B's = `hot_b` (sparse).
Ground truth per tick is exact from the beacon schedule (writes carry
sequence + commit time), read on the secondary. Witness = the oplog
(`local.oplog.rs`), per-collection max change `ts`, compared to the
secondary's applied optime `ts` from `replSetGetStatus`.

## Bars (bind at seal; checked against the family record first)

Bound **identical to the XPROTO-PG twin**. Every bar must hold on each of
the three family seeds in the committed `MGREP-family.json`
(`mongo_check.py --check-family`) before the seal is applied; a bar the
family record cannot pass does not get sealed. (Binding the same bars is
a stronger commitment than re-tuning: if the substrate does not deliver
the same regime, the pre-seal check fails and the seal does not happen.)

- **B1 — two-sided naive vacuity.** Per seed:
  `min over thresholds T of max(fcA, faA, fcB, faB)(T) ≥ 0.25`.
- **B2 — witness correctness.** Per seed: certificate worst error across
  both consumers and both directions `≤ 0.10`.
- **B3 — dominance.** Per seed: witness worst-error `≤ naive-minmax / 3`.

**Manipulation checks (bars too):**
- **MC1** A's truth-stale fraction in [0.20, 0.80] per seed.
- **MC2** B's truth-stale fraction < A's per seed.
- **MC3** ≥ 100 `hot_a` writes, ≥ 10 `hot_b` writes, and max busy-phase
  naive lag ≥ 0.8 s (the delay realized) per seed.

**Verdict rule:** any MC failure → VOID (instrument, not claim); all MCs
pass and all bars pass on every graded seed → PASS; otherwise FAIL, kept
as executed.

**Kills.** `naive-minmax < 0.15` on the graded seeds — the deployed
monitor is adequate for heterogeneous consumers and the MongoDB vacuity
claim is refuted for this substrate; or witness worst-error `> 0.20` —
the oplog certificate does not deliver. Either is reported as the result.

## Seal procedure

On 2026-08-21 or later: run `mongo_check.py --check-family` (must PASS),
reread this prereg, replace the STATUS token with `STATUS: SEALED
<date>`, commit, bring the lab up, run `mongo_check.py`, commit
`XPROTO-MG-graded.json` as executed.

## Scope

A lab cell: `secondaryDelaySecs` is a controlled knob standing in for
geo-replication / apply-lag regimes, and consumers are synthetic
footprints. A PASS earns the mechanism and the taxonomy entry on a second
substrate, not a production claim; a production cell (real workload
footprints, uncontrolled lag, `readConcern`/causal-session comparison) is
its own later campaign. Exact-consistency mechanisms
(`writeConcern:majority` + `readConcern:linearizable`, causal sessions
with `afterClusterTime`) are the natural production comparison and are
explicitly out of scope here — this cell's regime is default
`secondary` + `local` reads, where those are unused or unaffordable.
Prior-art positioning (PBS, PNUTS per-record timeline, Cosmos session
level, MongoDB's own causal sessions) recorded in the replication survey
(`geometric-observation/docs/replication-vacuity-survey.md`) and owed
before any public claim.

## Provenance

- Twin of the sealed `PREREG-XPROTO-PG.md` (network-governor
  analysis/pgrep, 2026-08-20 PASS).
- Motivated by the replication survey's coverage map (top candidate
  cell: MongoDB `secondary`+`local` vs causal vs majority).
- Family: `fam_mongo.py` + `MGREP-family.json` (seeds {0,1,2}).
- Graded runner: `mongo_check.py` (seal-guard + coded cooling-off +
  pre-seal record check).
