# A footprint-scoped freshness fix for ZooKeeper local reads

*Design note, 2026-08-23. Motivated by the XPROTO-ZK result: a local follower
read false-clears ~99% for a hot footprint and ~1% for a cold footprint on the
**same** follower — staleness is a property of the reader's footprint, not the
replica. `sync()` repairs it but is a blunt, unconditional, leader-involving
barrier. This note proposes a cheaper, consumer-relative alternative.*

## Diagnosis

A ZooKeeper reader today chooses between two extremes:

- **Naive local read** — fast, but clears *every* read blindly. Its false-clear
  rate is whatever the reader's footprint dictates (measured: 0.99 hot / 0.01
  cold). It reads neither the footprint nor a witness.
- **`sync()` then read** — correct, but an *unconditional full barrier*: it
  forwards to the leader and pulls the follower up to the leader's **latest**
  zxid, on every freshness-sensitive read, regardless of how little the reader
  touches or how fresh it actually needs to be.

Neither is consumer-relative. Yet the witness ZooKeeper needs is already present.

## Principle: the zxid is a sufficient, local, per-footprint witness

Because Zab totally orders writes, a follower's single applied watermark
`lastZxid` certifies **every** footprint at once: if `lastZxid ≥ W`, the follower
holds all writes with zxid `≤ W`, including any to the reader's znodes. Freshness
therefore reduces to one number the *reader* supplies — the watermark `W` it
needs — checked against the follower's current zxid. The consumer-relativity is
entirely in `W`; the follower needs no per-znode tracking.

Every read reply already carries the server's current zxid (the client's
last-seen zxid). So the witness is delivered *by the read itself* — no extra
round-trip.

## Fix 1 — client-side, no server change (deployable today)

A thin read wrapper:

```
read_fresh(path, W):           # W = the zxid this reader requires
    data, stat = client.get(path)          # ordinary local read
    if client.last_zxid >= W:               # the reply's zxid is the witness
        return data, CERTIFIED_FRESH_AT(client.last_zxid)   # local fast path
    client.sync(path)                        # slow path only when actually behind
    data, stat = client.get(path)
    return data, REFRESHED
```

Plus a **causal-token** convention: a writer captures the zxid of its write
(`stat.mzxid` from the `set`/`create` reply) and hands it to readers that must
observe it. `W` is then the max zxid across the writes the reader depends on —
i.e. its footprint's required watermark, derived from causality, not guessed.

Effect: a hot reader carrying its token either reads locally (when the follower
is already at `W`) or waits/`sync()`s only when genuinely behind — it **never
false-clears**. A cold reader declares a low `W` (or `W=0`) and pays nothing.
Each reader gets exactly the freshness it declares, witnessed by the zxid, for
the cost of one integer comparison on the common path.

## Fix 2 — server-side enhancement (a native bounded-staleness read)

Expose `W` as a first-class read parameter: `get(path, min_zxid=W)`. The follower
serves it **locally** iff `lastZxid ≥ W`; otherwise it waits until it applies up
to `W` (a bounded wait, timeout-guarded) before replying — and only forwards a
`sync` to the leader if it cannot make progress. This removes the leader
round-trip on the fast path (the common case for a well-chosen `W`) and moves
`sync()` from an *unconditional* barrier to a *conditional* one. It reuses the
zxid-watermark comparison ZooKeeper already performs at session (re)connect to
preserve monotonic reads — the machinery exists; this surfaces it per read.

## What it costs, and what it does not fix

- **Cost:** one comparison per read on the fast path; a bounded wait (Fix 2) or a
  `sync` (Fix 1) only when the follower is behind `W`. Cold/relaxed readers pay
  nothing; hot readers pay far less than an unconditional `sync` per read.
- **Honest limits:** a reader that needs the *latest global* state (a
  linearizable read) still requires leader contact — that is inherent, and this
  proposal does not remove it. It removes the tax on the far more common case:
  readers that need "at least as fresh as some causal event," whose watermark is
  a known zxid. `W` must come from somewhere (a causal token or an app-level
  freshness requirement); the proposal makes that requirement explicit and
  per-consumer instead of the current all-or-nothing.

## Relation to the measured result

The fix attacks the 99% false-clear directly and asymmetrically: it is
consumer-relative (each reader declares `W`) and witnessed (graded against the
zxid) by construction — the two grammar words the naive certificate was missing.

## Measured (2026-08-23, `zk_fix.py`, jittered ${\sim}200$ ms lag)

Sweeping the reader's declared tolerance $\tau$ (its watermark $W$ = the leader
zxid as of $\text{now}-\tau$) on the same lab, with the two degenerate baselines
for reference:

| policy | cost (sync rate) | false-clear |
|---|---|---|
| naive local read | 0.00 | **0.989** (vs latest) |
| `sync()`-always | 1.00 | 0.000 |
| `read_fresh` $\tau{=}0$ (needs latest) | 1.00 | **0.000 vs $W$** |
| `read_fresh` $\tau{=}100$ ms | 0.675 | **0.000 vs $W$** |
| `read_fresh` $\tau{=}200$ ms (${=}$lag) | **0.11** | **0.000 vs $W$** |
| `read_fresh` $\tau{=}300$ ms | 0.00 | **0.000 vs $W$** |

Two facts carry the proposal. First, `false_clear_vs_W = 0` at **every** point:
the zxid is a *sound* witness — a certified-local read never violates the
freshness it promised (verified against a per-znode write log). Second, the cost
is exactly the probability that the follower's lag exceeds $\tau$ (the lag CDF):
`read_fresh` traces a smooth curve from `sync()`-always cost (need latest) to
zero cost (tolerate the lag), **correct at every point**, where naive (free,
$0.99$ wrong) and `sync()`-always ($1.0$ cost, correct) are the two blind
endpoints. At a tolerance equal to the follower's own lag, a reader gets
guaranteed freshness for a sync on only ${\sim}11\%$ of reads. See `ZK-FIX.png`.
