# Reply to Ben Reed (2026-08-25) — DRAFT, owner sends

Context: Ben replied to the replication-vacuity survey with a precise account of
ZooKeeper's consistency model and a DB-master staleness example. Goal: nurture toward
collaboration on the ZK/freshness write-up. Keep it peer-level, credit `sync()`,
absorb his refinement, ask one empirical question, propose coffee. Do NOT oversell.

---

**Subject:** Re: nice survey!

Ben — thanks, and yes, we did trade a few notes a while back; good to pick it up.

Your DB-master example is exactly the case we ended up measuring, so it was a bit
uncanny to read. On a 3-node ensemble we hold a znode hot under write load and read
it from a lagging follower: the naive local read false-clears — returns a stale
version served as if current — about **99%** of the time on that hot key, while a
**cold** key on the *same* follower stays fresh (~1%). ZooKeeper's own `sync()`
barrier drives it to zero, as you'd expect. So we're not proposing a detection
mechanism — `sync()` is the mechanism; what we add is the *measured, consumer-relative*
false-clear rate (and a refresh horizon: how much write churn a read can tolerate
before it needs a `sync()`), as a first-class number that turns out to recur
identically in Postgres/Mongo replicas, optical margins, grid state estimation, etc.

The part of your note I want to sit with is this: *if machines interact only through
ZooKeeper, the total order means they can't detect the stale read — it only bites out
of band.* That's a sharper statement of what we've been calling "consumer-relative":
the false-clear isn't a property of the read, it's a property of the read **plus a
consumer whose channel differs from the certificate's**. Same-channel (in-band)
consumers are protected by the total order for free; the exposure is exactly the
out-of-band actor (your client walking over to server A). I'd like to state it that
way in the write-up — may I attribute the framing to you?

The empirical question I can't answer from a lab and you probably can from scars: in
practice, how often does a stale read actually *bite* — i.e., the state changes
between the client getting the result and acting on it — versus staying benign because
nothing acts on it before the next `sync()`? And is there a canonical workload where
it bites hardest (leader/master handoff is my guess)?

If you're up for it, I'd love to buy you a coffee on campus and walk through the ZK
measurements — 30–40 minutes, whenever suits. I think your read on where this matters
(and where it doesn't) would shape the paper for the better.

Best,
Andrew
