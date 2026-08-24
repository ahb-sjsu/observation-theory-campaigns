"""Per-substrate adapters for freshread. Each turns already-connected clients
into a FreshRead by supplying the witness (applied watermark) and the refresh;
the application supplies `read_value(path) -> value`. The witness is a monotonic
integer in every case, which is the whole point.
"""
from __future__ import annotations

from typing import Any, Callable

from .core import FreshRead


def zk_adapter(client, read_value: Callable[[str], Any]) -> FreshRead:
    """ZooKeeper. `client`: a kazoo KazooClient connected to a follower.
    Witness = the session's last-seen zxid (carried on every reply). Refresh =
    sync(path), ZooKeeper's freshness barrier."""
    def read(path):
        return read_value(path), int(getattr(client, "last_zxid", 0) or 0)

    def refresh(path, W):
        client.sync(path)
        return read_value(path), int(getattr(client, "last_zxid", 0) or 0)

    return FreshRead(read, refresh)


def _lsn_to_int(lsn: str) -> int:
    """PostgreSQL LSN 'XXXX/YYYY' (hex) -> monotonic int."""
    hi, lo = lsn.split("/")
    return (int(hi, 16) << 32) | int(lo, 16)


def pg_adapter(replica, primary, read_value: Callable[[Any, str], Any]) -> FreshRead:
    """PostgreSQL streaming replication. `replica`/`primary`: DB-API connections.
    Witness = the replica's WAL replay LSN. Refresh (slow path) = read the
    primary, which is by definition at or ahead of any required LSN."""
    def read(path):
        v = read_value(replica, path)
        cur = replica.cursor(); cur.execute("SELECT pg_last_wal_replay_lsn()")
        return v, _lsn_to_int(cur.fetchone()[0])

    def refresh(path, W):
        v = read_value(primary, path)
        cur = primary.cursor(); cur.execute("SELECT pg_current_wal_lsn()")
        return v, _lsn_to_int(cur.fetchone()[0])

    return FreshRead(read, refresh)


def mongo_adapter(secondary_db, primary_db, coll: str,
                  read_value: Callable[[Any, str], Any]) -> FreshRead:
    """MongoDB replica set. Witness = the secondary's applied optime cluster
    time (as an int: seconds<<32 | increment). Refresh = a causal read
    (afterClusterTime = W), MongoDB's native watermark read, served so it
    reflects >= W. `*_db`: pymongo Database handles."""
    def _applied(db) -> int:
        st = db.command("replSetGetStatus")
        me = next(m for m in st["members"] if m.get("self"))
        ts = me["optime"]["ts"] if isinstance(me.get("optime"), dict) else me["optime"]
        return (ts.time << 32) | ts.inc

    def read(path):
        return read_value(secondary_db, path), _applied(secondary_db)

    def refresh(path, W):
        # a causal read forces the server to reflect at least W before answering
        sec, inc = W >> 32, W & 0xFFFFFFFF
        from bson.timestamp import Timestamp
        s = secondary_db.client.start_session()
        s.advance_cluster_time({"clusterTime": Timestamp(sec, inc)})
        v = read_value(secondary_db, path)      # read within the causal session
        return v, _applied(secondary_db)

    return FreshRead(read, refresh)
