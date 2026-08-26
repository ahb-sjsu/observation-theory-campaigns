# DESIGN — the Flip in coordination-service reads

**Date: 2026-08-26. Status: lab LIVE (two netem profiles); pilots 1-4 run today;
registration decision bound to pilot 4's declared stopping rule.**

## Pilot log (all kept)

1. **Pilot 1** (50/400 ms, 300 back-to-back reads): H-axis clean (0.00 vs
   0.18-0.21 every seed); L-axis under-sampled, the read block spanned less than
   one cold-write cycle. Fix: pace reads at 50 ms.
2. **Pilot 2** (paced): flip on 2 of 3 seeds; L-gaps 2-4 events out of 300,
   noise. Cause found by arithmetic: a cold write lands on one of three cold
   znodes, so a random cold reader sees a third of the stale windows. Fix: one
   cold znode.
3. **Pilot 3** (single cold znode): flip on 3 of 3 seeds, null holds on all,
   but L-gaps still thin (0.007-0.023) against a 0.09 expectation. Remaining
   shortfall unexplained by the dilution model alone.
4. **Pilot 4** (slow lag 400 -> 1200 ms, n = 600, DECLARED FINAL): a priori
   expectation L_A ~ 0.30 vs L_B ~ 0.03. **Stopping rule written before the
   run:** any seed's L-gap under 0.10 sends this cell to a kept exploration,
   not a registration. No pilot 5.

**Found along the way:** sync() cost scales with the follower's lag. Against the
1200 ms follower a sync round-trip takes about 1.2 s, which stretched the
high-sync read blocks from 30 s to 11 minutes. The witnessed correction is most
expensive exactly where it is most needed. That asymmetry belongs in any paper
this cell feeds.

The two-consumer verdict inversion needs consumers that read different axes of
the staleness state. The sealed XPROTO-ZK cell has one axis (write churn on a hot
key behind one delayed follower), so it can show relativity but not inversion.
The two axes for a coordination service are write churn and replication lag, and
they need to vary independently.

**Lab.** A 3-follower ensemble with two netem profiles: follower F1 at 50 ms
commit-stream delay, follower F2 at 400 ms. Two key populations: hot keys
(~30 writes/s) and cold keys (~0.3 writes/s). Two reader fleets with misaligned
reads: the H-fleet reads hot keys through the fast follower (staleness driven by
churn), and the L-fleet reads cold keys through the slow follower (staleness
driven by lag).

**Policies.** A fixed sync() budget per window (the freshness currency), allocated
two ways at matched totals: policy A syncs in proportion to key write rate,
policy B in proportion to follower lag. The H-fleet should do better under A and
the L-fleet under B, with the fleet-mean stale-read rate unable to order the pair.

**Null.** The same fleet read at two staleness tolerances (zxid gap 5 versus 20).
A tolerance shift leaves both consumers reading the same projection, so no
inversion is expected. (Lesson from the grid attempt: the null must be a
threshold pair, not a re-run with the drivers coupled.)

**Why staged.** The current lab (`lab_up.sh`) builds one delayed follower. The
two-profile lab is a real change to a live Atlas deployment, and Atlas work is
ask-first. Estimated effort: half a day including calibration pilots. Ben Reed's
out-of-band framing (see `outreach/ben-reed-reply.md`) makes this cell a natural
joint experiment for the PaPoC direction.
