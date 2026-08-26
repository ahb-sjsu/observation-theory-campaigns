# EXPLORATION — the Flip in coordination-service reads (kept, NOT registered)

**Date: 2026-08-26. Status: stopping rule fired at pilot 4; kept exploration; no
prereg, no seal. The pilot trail and stopping rule were declared in
DESIGN-ZK-FLIP.md before the final run.**

We tried to produce the two-consumer verdict inversion on a real ZooKeeper
ensemble with two staleness axes: write churn (hot znodes, one write per 12 ms)
and replication lag (a fast follower at 50 ms, a slow one at 400 then 1200 ms).
The H-fleet reads hot keys through the fast follower; the L-fleet reads a cold
key (one write per 3.6 s) through the slow follower. Policies allocate a matched
sync() budget by churn (A) or by lag (B).

The H-axis behaved from pilot 1: syncing hot readers cuts their stale rate from
about 0.2 to near zero, every seed, every pilot. The L-axis never produced a
registrable gap, for two different reasons at the two lag settings.

**At 400 ms lag the axis is too weak.** The stale fraction a cold reader can
accumulate is lag over write interval, about 0.11, diluted by znode choice and
sampling. After three disclosed fixes (paced reads, single cold znode) the
per-seed gaps were still 2 to 7 events out of 300, within noise.

**At 1200 ms lag the witness stops paying.** Pilot 4 was first contaminated by a
double launch (disclosed in DESIGN-ZK-FLIP.md; that data is quarantined and not
used). The clean re-execution, one process, n = 600, gave per-seed L-fleet rates
of 0.067/0.075/0.080 under the churn policy A (10 percent sync) against
0.065/0.058/0.055 under the lag policy B (90 percent sync). Nine times the sync
budget bought the cold readers gaps of 0.002, 0.017 and 0.025, every one under
the pre-declared 0.10 bar. The mechanism: sync() flushes the leader-to-follower
queue through the same delayed channel, so its round-trip is about the lag
itself, and during that round-trip a lag-over-interval fraction of cold writes
lands and is lagging again by the time the read executes. The sync re-opens part
of the window it closes. When replication lag approaches the consumer's write
interval, the witnessed correction converges too slowly to matter, and paying
more sync buys almost nothing. The H-fleet behaved throughout (0.027-0.047 under
its protecting policy against 0.218-0.255 without), which also confirms the
contaminated run's inflated H numbers were the double-writer artifact.

**An open observation, recorded not chased.** Across all pilots the measured
L-fleet stale rate runs about four times below the lag-over-write-interval
arithmetic (0.067-0.080 measured against about 0.30 expected at 1200 ms).
Something in Zab's commit pipelining makes the effective stale window smaller
than the injected netem delay. A future cell that sweeps lag against write
interval should measure this directly.

**What this cell established, none of it a flip:**
1. A witnessed correction has an operating region. sync() protects a reader only
   while lag is well under the read's write interval. Past that, the correction
   is self-defeating. This is the coordination-service twin of the WCNC result
   that above a mobility threshold no CSI reporting cadence suffices.
2. The witness cost scales with the lag (a sync round-trip is about the lag
   itself), so the correction is most expensive exactly where it is most needed,
   and then stops working where it is needed most.
3. The flip in this substrate would live only in a narrow band of lag relative
   to write interval. Our two lab settings bracket the band. Registering a cell
   whose effect exists only in a tuned sliver would be the opposite of the
   program's discipline, so we did not.

**Records** (all kept): ZKFLIPREP-family.json (pilot 3),
ZKFLIPREP-pilot4-clean.json (the clean final run), zkflip4_contaminated.log
(quarantined) and zkflip2.log through zkflip4.log on Atlas, DESIGN-ZK-FLIP.md
(pilot log, the pre-declared stopping rule, and the contamination disclosure).
Lab torn down 2026-08-26.

The sync-breakdown finding is worth a sealed cell of its own someday: sweep lag
against write interval and measure where witnessed reads stop converging. That
is a monotone threshold claim, not a flip, and it is exactly the kind of
question the Ben Reed collaboration could take up on a production workload.
