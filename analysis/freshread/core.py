"""freshread -- consumer-relative bounded-staleness reads over a monotonic
witness.

The generalization of the ZooKeeper read_fresh fix. A reader declares the
watermark W it requires (the position of the writes it causally depends on). A
local replica read is certified fresh iff the replica's applied watermark >= W;
otherwise a substrate-specific refresh forces catch-up to >= W. Because the
witness is a total order, one scalar -- the replica's applied watermark --
certifies every footprint at once, so the consumer-relativity lives entirely in
W. This is one core with per-substrate adapters (see adapters.py):

    substrate     witness (applied watermark)     refresh (force >= W)
    ---------     ---------------------------     --------------------
    ZooKeeper     session zxid (lastZxid)         sync(path)
    PostgreSQL    WAL replay LSN                   read primary / wait for replay
    MongoDB       oplog cluster time               afterClusterTime read

Correctness (sound witness): if applied >= W then, by total order, the replica
holds every write with position <= W, so a certified-local read never violates
the freshness it promised. Cost (fraction needing a refresh) equals the
probability the replica's lag exceeds the reader's tolerance -- the lag CDF.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Tuple


@dataclass
class Result:
    value: Any
    mode: str            # "LOCAL" (certified locally) or "REFRESHED" (slow path)
    applied: int         # the replica's applied watermark at read time
    required: int        # W

    @property
    def certified(self) -> bool:
        return self.applied >= self.required


@dataclass
class FreshRead:
    """A substrate-generic bounded-staleness reader.

    read(path)      -> (value, applied_watermark): a local replica read plus the
                       replica's applied watermark (the witness).
    refresh(path,W) -> (value, applied_watermark): force the read to reflect >= W
                       (sync / primary route / afterClusterTime), returning the
                       refreshed value and the now-applied watermark.
    """
    read: Callable[[str], Tuple[Any, int]]
    refresh: Callable[[str, int], Tuple[Any, int]]

    def get(self, path: str, W: int = 0) -> Result:
        value, applied = self.read(path)
        if applied >= W:                       # certified fresh vs W, locally
            return Result(value, "LOCAL", applied, W)
        value, applied = self.refresh(path, W)  # slow path only when behind W
        return Result(value, "REFRESHED", applied, W)
