# PREREG-XPROTO-PG — replication-staleness cell (the taxonomy's first database entry)

**STATUS: SEALED 2026-08-20.** FAMILY-CONSTRUCTED: 2026-08-19. Construction +
family shakedown only; the earliest compliant seal is **2026-08-20**
(`pgrep_check.py` enforces the cooling-off in code and refuses to grade
before a dated seal). Graded on seeds {20260820, 20260821, 20260822},
disjoint from the shakedown's {0, 1, 2}. No evidential weight until
sealed and run.

**Disclosure gate (owner decision pending):** a possible provisional
patent filing on the witnessed consumer-relative certificate mechanism
precedes any *public* disclosure of this cell; the repo is private, and
this prereg records the gate so publication order is a decision, not an
accident.

## The claim

On a Postgres primary/replica pair with a real apply-delay window, the
standard replication monitor — `now() − pg_last_xact_replay_timestamp()`
against a threshold — is **two-sidedly vacuous for heterogeneous
consumers**: no threshold simultaneously avoids false-clears for a
bursty-footprint consumer and false-alarms for a quiet-footprint
consumer. A **WAL-witnessed, footprint-aware certificate**
(`tr(P_i · drift) = 0`: no change to consumer *i*'s footprint past the
replica's replay LSN) is simultaneously correct in both directions for
both consumers, dominating the naive monitor's entire threshold curve.

This is the vacuity taxonomy's first **database** cell (sealed cells so
far: BGP 0.351 / IS-IS 0.184 / OSPF 0.083 / BMP witness-grading), and
the consumer-relativity (P1/P2) claim measured on the C-leg's
staleness face.

## Family F-PG (constructed + shaken down 2026-08-19)

Lab: `postgres:16-alpine` primary (`wal_level=logical`) + streaming
replica (`recovery_min_apply_delay = 1000 ms`); setup/teardown in
`lab_up.sh` / `lab_down.sh`. Sealed constants (`fam_pgrep.py`):
thresholds {0.1, 0.5, 1, 2, 5} s; duration 120 s; tick 200 ms; truth
guard 200 ms; 20 s busy/quiet phases. The **seed** draws the busy-phase
write rate from [4, 6]/s and the quiet consumer's spacing from
[6, 10] s — the family dimension is the write schedule, and each seeded
cell rebuilds fresh tables and a fresh logical slot.

Consumers: A's footprint = `hot_a` (bursty), B's = `hot_b` (sparse).
Ground truth per tick is exact from the beacon schedule (writes carry
sequence + commit time). Witness = logical-decoding slot, per-table max
change LSN, compared to the replica's replay LSN.

## Bars (bind at seal; checked against the family record first)

Per the OT-18 practice, every bar below must hold on **each of the
three family seeds** in the committed `PGREP-family.json`
(`pgrep_check.py --check-family`) before the seal is applied; a bar the
family record cannot pass does not get sealed.

- **B1 — two-sided naive vacuity.** Per seed:
  `min over thresholds T of max(fcA, faA, fcB, faB)(T) ≥ 0.25` — the
  naive monitor's best achievable worst-error stays above one quarter;
  no threshold serves both consumers.
- **B2 — witness correctness.** Per seed: the certificate's worst error
  across both consumers and both directions `≤ 0.10`.
- **B3 — dominance.** Per seed: witness worst-error `≤ naive-minmax/3`.

**Manipulation checks (bars too, enforcement granularity):**
- **MC1** A's truth-stale fraction in [0.20, 0.80] (a real staleness
  regime, not degenerate) per seed.
- **MC2** B's truth-stale fraction < A's (the footprint asymmetry
  actually realized) per seed.
- **MC3** schedule + knob executed: ≥ 100 `hot_a` writes, ≥ 10 `hot_b`
  writes, and max busy-phase naive lag ≥ 0.8 s (the apply delay bit).

**Verdict rule:** any MC failure → VOID (instrument, not claim); all
MCs pass and all bars pass on every graded seed → PASS; otherwise FAIL,
kept as executed.

**Kills.** `naive-minmax < 0.15` on the graded seeds — the deployed
monitor is adequate for heterogeneous consumers and the PG vacuity
claim is refuted for this substrate; or witness worst-error `> 0.20` —
the witnessed certificate does not deliver, and the module case
collapses. Either is reported as the cell's result.

## Seal procedure

On 2026-08-20 or later: run `pgrep_check.py --check-family` (must
PASS), reread this prereg, replace the STATUS token with
`STATUS: SEALED <date>`, commit, bring the lab up, run
`pgrep_check.py`, commit `XPROTO-PG-graded.json` as executed.

## Scope

A lab cell: the apply delay is a controlled knob standing in for
geo-replication / apply-lag regimes, and consumers are synthetic
footprints. A PASS earns the mechanism and the taxonomy entry, not a
production claim; a production cell (real workload footprints from
`pg_stat_statements`, uncontrolled lag) is its own later campaign.
Exact-consistency mechanisms (`remote_apply`, LSN tokens) are
explicitly out of scope — the cell's regime is where they are
unaffordable. Prior-art positioning obligations (PBS, consistency
SLAs, CDC-driven invalidation) recorded in `NOTES.md` and owed before
any public claim.

## Provenance

- Exploration: `pgrep_shakedown.py` + `PGREP-shakedown.json`
  (2026-08-19, single-config, no weight) and issue #22.
- Family: `fam_pgrep.py` + `PGREP-family.json` (seeds {0,1,2}).
- Graded runner: `pgrep_check.py` (seal-guard + coded cooling-off +
  pre-seal record check).
