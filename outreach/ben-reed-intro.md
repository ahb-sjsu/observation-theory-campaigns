# Intro note to Ben Reed (SJSU Computer Engineering; ZooKeeper/Zab)

Draft 2026-08-23. Hook: XPROTO-ZK — his own system is the cleanest cell in the
freshness series; DB mechanism now public (ot-replication-freshness paper).
Low-friction ask: 20–30 min. Repo: https://github.com/ahb-sjsu/geometric-observation

---

**Subject:** ZooKeeper's sync(), measured — a freshness result I'd value your read on

Hi Ben,

I'm Andrew Bond, over in Computer Engineering here at SJSU — I teach the database
course. I've spent the last stretch building a measurement discipline around one
question: when a system reports that a read is "fresh enough," how often is it
wrong, and for whom?

The short version of the thesis is that freshness isn't a property of a replica —
it's a relation between the replica's drift and *what a particular consumer
reads* — and any honest freshness claim needs an independent witness rather than
an inferred lag bound. I've been measuring this across substrates (PostgreSQL,
MongoDB, a geo-distributed fleet), each under a sealed pre-registration so the
pass/fail bars are committed in code before the runs.

ZooKeeper turned out to be the cleanest case in the whole series — and it's the
one I most wanted your eyes on, since you built it. On a 3-node ensemble, a local
follower read of a hot znode false-clears ~99% of the time under write load,
while a cold znode on the *same* follower reads ~1% stale: the staleness is
entirely a property of the reader's footprint, not of the replica. Graded against
the zxid, `sync()` drives the false-clear to zero. The framing I landed on is
that the certificate that matters isn't "follower lag < T," it's "has this
consumer's footprint caught up" — and `sync()`/the zxid is exactly the witness
that answers it.

I'm certain I'm being naive about corners of ZooKeeper's read semantics, which is
honestly why I'm writing — I'd value 20–30 minutes (coffee on campus?) to hear
where the framing holds and where it doesn't. The work is public if you'd like a
look first: github.com/ahb-sjsu/geometric-observation — the databases paper
carries the ZooKeeper cell as its coordination-service case.

Either way, it's a genuine pleasure to have ZooKeeper's designer down the hall.

Best,
Andrew

Andrew H. Bond · Dept. of Computer Engineering, SJSU
