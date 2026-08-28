# Intro note to Ben Reed (SJSU Computer Engineering; ZooKeeper/Zab)

Draft 2026-08-23. Hook: XPROTO-ZK. His own system is the cleanest case in the
freshness series; DB mechanism now public (ot-replication-freshness paper).
Low-friction ask: 20 to 30 min. Repo: https://github.com/ahb-sjsu/geometric-observation

---

Subject: ZooKeeper's sync(), measured. A freshness result I'd value your read on

Hi Ben,

I'm Andrew Bond, over in Computer Engineering here at SJSU. I teach the
database course. I've spent the last stretch building a measurement
discipline around one question: when a system reports that a read is "fresh
enough," how often is it wrong, and for whom?

The short version of the thesis is that freshness is not a property of a
replica. It is a relation between the replica's drift and what a particular
consumer actually reads. Any honest freshness claim needs an independent
check on the true state rather than an inferred lag bound. I've been
measuring this across PostgreSQL, MongoDB, and a geo-distributed fleet, each
under a pre-registration that commits the pass and fail bars in code before
the runs.

ZooKeeper turned out to be the cleanest case in the whole series, and it's
the one I most wanted your eyes on, since you built it. On a 3-node
ensemble, a local follower read of a hot znode returns stale data while
reporting success about 99% of the time under write load. A cold znode on
that same follower reads stale about 1% of the time. The staleness is entirely
a property of which znodes the reader touches, not of the replica. Checked
against the zxid, `sync()` drives that error rate to zero. The framing I
landed on is that the certificate that matters is not "follower lag < T." It
is "have the znodes this consumer reads caught up," and `sync()` with the
zxid is exactly the check that answers it.

I'm certain I'm being naive about corners of ZooKeeper's read semantics,
which is honestly why I'm writing. I'd value 20 to 30 minutes (coffee on
campus?) to hear where the framing holds and where it doesn't. The work is
public if you'd like a look first: github.com/ahb-sjsu/geometric-observation.
The databases paper carries the ZooKeeper measurements as its
coordination-service case.

Either way, it's a genuine pleasure to have ZooKeeper's designer down the hall.

Best,
Andrew

Andrew H. Bond, Dept. of Computer Engineering, SJSU
