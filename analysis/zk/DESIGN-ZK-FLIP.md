# DESIGN — the Flip in coordination-service reads (staged, lab not yet built)

**Date: 2026-08-26. Status: designed; blocked on a two-axis lab; no run, no prereg.**

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
