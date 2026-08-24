# Database-Freshness Track: replication & coordination staleness certificates

**Status:** re-homed 2026-08-24 from `network-governor`. Chip 🕒💾 DBF. Freshness
program ([FRESHNESS-PROGRAM.md](FRESHNESS-PROGRAM.md)). Distinct from the
[DATABASE-TRACK](DATABASE-TRACK.md) (precision/encoding allocation): this track is
consumer-relative **staleness** — `tr(P_C·Σ)` read as false-clear, not allocation.

## Question

A replica read is a **certificate** ("this replica is fresh enough"). Served under
write load it **false-clears**: the returned version lags the primary's committed
version, yet the read is served as current. Graded against a **watermark witness**
(WAL LSN / oplog ts / zxid), the naive lag certificate false-clears far above
target for a **hot footprint**, while a watermark-gated read (or `sync()`) holds it
at zero. The rate is **consumer-relative**: on the *same* replica a hot-footprint
reader is stale while a cold-footprint reader is fresh — no single "replica is
fresh enough" assumption serves both.

## Cells (all SEALED; see SEALS.md, provenance = network-governor commits)

| Cell | Substrate | Witness | Result (naive → witnessed) |
|---|---|---|---|
| **XPROTO-PG** (`analysis/pgrep`) | Postgres, `recovery_min_apply_delay` | WAL LSN | ~0.50 → ~0.06 |
| **XPROTO-MG** (`analysis/mongo`) | MongoDB delayed secondary | oplog ts | ~0.47 → ~0.03 |
| **XPROTO-PGX** (`analysis/pgx`) | production PG, netem lag | WAL LSN, `pg_stat_statements` footprint | ~0.47 → ~0.02 |
| **XPROTO-GEO** (`analysis/geofleet`) | geo-distributed PG fleet (NRP) | replay LSN | nearest-certified routing: cert fresher than nearest, more local than least-lag |
| **XPROTO-ZK** (`analysis/zk`) | ZooKeeper 3.9 ensemble | zxid, `sync()` | hot 0.99 / cold 0.01, witnessed 0.0 |

Consumer-relativity, starkest (ZK): on one follower at one instant, hot-footprint
reader 99% stale vs cold-footprint 1% — a 99× gap from *what the reader reads*.

## Discipline & provenance

Each cell: sealed prereg, coded cooling-off, disjoint graded seeds, kept FAILs,
real substrate (refuse-to-seal-on-sim). Sealed originally in `network-governor`;
seals preserved via SEALS.md rows citing the original NG sealing commit + SHA-256
(verify: `git -C network-governor show <commit>:<path> | sha256sum`). The
generalized `read_fresh` library (`analysis/freshread`, migrating with the radio
track's shared tooling) unifies the witness-gate across ZK/PG/Mongo.

## Collaboration

**Ben Reed** (SJSU; ZooKeeper/Zab co-creator) — XPROTO-ZK + the `read_fresh` fix
are the outreach asset (`outreach/ben-reed-intro.md`). **Suneuy Kim** (SJSU;
NoSQL) — the MongoDB/YCSB lineage.
