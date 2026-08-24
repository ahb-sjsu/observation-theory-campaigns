# freshread

Consumer-relative bounded-staleness reads over a monotonic witness -- the
generalization of the ZooKeeper `read_fresh` fix (see `../zk/FIX-PROPOSAL.md`)
across replicated substrates.

## The idea

A reader declares the watermark `W` it requires -- the position of the writes it
causally depends on. A local replica read is **certified fresh** iff the
replica's applied watermark `>= W`; otherwise a substrate-specific **refresh**
forces catch-up to `>= W`. Because the witness is a total order, the replica's
single applied watermark certifies *every* footprint at once, so the
consumer-relativity is entirely in `W`.

| substrate  | witness (applied watermark)   | refresh (force `>= W`)          |
|------------|-------------------------------|---------------------------------|
| ZooKeeper  | session `zxid` (`lastZxid`)   | `sync(path)`                    |
| PostgreSQL | WAL replay LSN                | read primary / wait for replay  |
| MongoDB    | oplog cluster time            | `afterClusterTime` causal read  |

## Guarantees (measured)

- **Sound witness:** a certified-local read never violates the freshness it
  promised -- if `applied >= W`, total order guarantees every write `<= W` is
  present. (`false_clear_vs_W = 0` at every tolerance in the XPROTO-ZK
  measurement and in `test_cost_curve_generic`.)
- **Cost = the lag CDF:** the fraction of reads needing a refresh equals the
  probability the replica's lag exceeds the reader's tolerance. `read_fresh`
  interpolates between the two blind endpoints -- naive local reads (free,
  stale) and refresh-always (correct, maximal cost) -- *correct at every point*.

## Usage

```python
from freshread import FreshRead, zk_adapter

fr = zk_adapter(follower_client, read_value=lambda p: follower_client.get(p)[0])
r = fr.get("/service/config", W=my_causal_zxid)
#  r.mode == "LOCAL"     -> served from the follower, certified fresh vs W
#  r.mode == "REFRESHED" -> follower was behind W, sync()'d then served
```

`W` is a causal token: capture a write's position (zxid / LSN / cluster time)
and hand it to readers that must observe it; a reader tolerant of staleness
passes a `W` from `tau` ago (or `0`).

## Tests

`python test_freshread.py` -- core logic plus a substrate-agnostic reproduction
of the cost curve (no cluster needed). PG/MongoDB adapters are exercised live in
the respective XPROTO cells.
