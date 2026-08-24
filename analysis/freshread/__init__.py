"""freshread -- consumer-relative bounded-staleness reads over a monotonic
witness. One core, per-substrate adapters (ZooKeeper zxid / PostgreSQL WAL LSN /
MongoDB cluster time). See core.py and FIX-PROPOSAL / the XPROTO-ZK cell."""
from .core import FreshRead, Result
from .adapters import zk_adapter, pg_adapter, mongo_adapter

__all__ = ["FreshRead", "Result", "zk_adapter", "pg_adapter", "mongo_adapter"]
