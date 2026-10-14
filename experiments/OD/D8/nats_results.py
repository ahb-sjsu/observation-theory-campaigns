"""Durable result transport for OD Jobs on NRP: publish a result file over NATS into a JetStream stream on the Atlas hub,
and collect it back on Atlas. The Job's log stays as the fallback path.

Why: on 2026-10-11 a pilot Job succeeded but its container log could not be retrieved, and the result block travels only
in the log, so the result was lost. Results must not depend on the node that ran the Job.

How it travels. Pods reach the Atlas NATS hub through the in-cluster leaf (nats://atlas-nats:4222). JetStream's own API
does not federate across the leaf link (atlas-burst fleet-coordinator notes), so the pod does a CORE request to a subject
that a stream on the hub captures (OD_RESULTS, subjects od.results.>). The stream answers a captured message with a PubAck
on the request's reply inbox, which core request/reply carries back across the leaf, so the pod learns the result is
stored. The file is gzipped and split into chunks under the 1 MiB payload limit; every chunk carries the whole file's
sha256 and its index, and a Nats-Msg-Id so that a retried chunk is not stored twice.

    python nats_results.py publish <file> <subject>      # in the pod; exit 0 only if every chunk was acknowledged
    python nats_results.py ensure-stream                 # on Atlas, once
    python nats_results.py collect <subject> <out-file>  # on Atlas; exit 0 if a complete, verified copy was written
"""
from __future__ import annotations

import asyncio
import gzip
import hashlib
import json
import os
import sys

STREAM = "OD_RESULTS"
SUBJECTS = ["od.results.>"]
CHUNK = 800_000  # under the hub's 1 MiB max_payload with headers to spare
HUB_URL = "nats://localhost:4222"


async def publish(path: str, subject: str, url: str | None = None, tries: int = 6) -> list[int]:
    import nats
    url = url or os.environ.get("NATS_URL", "nats://atlas-nats:4222")
    raw = open(path, "rb").read(); sha = hashlib.sha256(raw).hexdigest(); blob = gzip.compress(raw)
    chunks = [blob[i:i + CHUNK] for i in range(0, len(blob), CHUNK)] or [b""]
    nc = await nats.connect(url, connect_timeout=10, max_reconnect_attempts=5); seqs = []
    try:
        for i, part in enumerate(chunks):
            hdr = {"Nats-Msg-Id": f"{subject}.{sha[:16]}.{i}", "OD-Sha256": sha, "OD-Chunk": str(i), "OD-Chunks": str(len(chunks)), "OD-Bytes": str(len(raw))}
            for attempt in range(tries):
                try:
                    ack = json.loads((await nc.request(f"{subject}.{i}", part, timeout=15, headers=hdr)).data)
                    if "error" in ack: raise RuntimeError(f"stream error {ack['error']}")
                    seqs.append(int(ack["seq"])); break
                except Exception as e:  # bounded retry with backoff inside a computing Job, not an idle wait
                    if attempt == tries - 1: raise RuntimeError(f"chunk {i} of {len(chunks)} not acknowledged: {e}")
                    await asyncio.sleep(2 ** attempt)
    finally:
        await nc.close()
    return seqs


async def ensure_stream(url: str = HUB_URL) -> dict:
    import nats
    from nats.js.api import DiscardPolicy, RetentionPolicy, StorageType, StreamConfig
    nc = await nats.connect(url); js = nc.jetstream()
    try:
        info = await js.stream_info(STREAM); created = False
    except Exception:
        info = await js.add_stream(StreamConfig(name=STREAM, subjects=SUBJECTS, storage=StorageType.FILE, retention=RetentionPolicy.LIMITS,
                                                discard=DiscardPolicy.OLD, max_age=90 * 24 * 3600, max_bytes=5 * 1024 ** 3,
                                                max_msg_size=1024 ** 2, duplicate_window=600))
        created = True
    out = {"stream": info.config.name, "subjects": info.config.subjects, "created": created, "messages": info.state.messages, "bytes": info.state.bytes}
    await nc.close(); return out


async def collect(subject: str, out_path: str, url: str = HUB_URL) -> dict:
    """Read every chunk stored under <subject>.*, keep the newest complete set (by file sha256), verify it, write it."""
    import nats
    from nats.js.api import ConsumerConfig, DeliverPolicy
    nc = await nats.connect(url); js = nc.jetstream(); sets: dict[str, dict] = {}
    try:
        sub = await js.pull_subscribe(f"{subject}.*", durable=None, stream=STREAM, config=ConsumerConfig(deliver_policy=DeliverPolicy.ALL))
        while True:
            try:
                msgs = await sub.fetch(64, timeout=3)
            except Exception:
                break
            if not msgs: break
            for m in msgs:
                h = m.headers or {}; s = sets.setdefault(h["OD-Sha256"], {"n": int(h["OD-Chunks"]), "bytes": int(h["OD-Bytes"]), "parts": {}, "seq": 0})
                s["parts"][int(h["OD-Chunk"])] = m.data; s["seq"] = max(s["seq"], m.metadata.sequence.stream); await m.ack()
    finally:
        await nc.close()
    complete = {k: v for k, v in sets.items() if len(v["parts"]) == v["n"]}
    if not complete: return {"ok": False, "reason": f"no complete set under {subject} ({len(sets)} partial)"}
    sha, s = max(complete.items(), key=lambda kv: kv[1]["seq"])
    raw = gzip.decompress(b"".join(s["parts"][i] for i in range(s["n"])))
    if hashlib.sha256(raw).hexdigest() != sha or len(raw) != s["bytes"]: return {"ok": False, "reason": "sha256 or length mismatch"}
    open(out_path, "wb").write(raw)
    return {"ok": True, "sha256": sha, "bytes": len(raw), "chunks": s["n"], "sets_seen": len(sets)}


def main(argv=None) -> int:
    a = sys.argv[1:] if argv is None else argv
    if a[:1] == ["publish"]:
        try:
            seqs = asyncio.run(publish(a[1], a[2]))
            print(f"NATS-PUBLISHED {a[2]} chunks={len(seqs)} seqs={seqs}", flush=True); return 0
        except Exception as e:
            print(f"NATS-PUBLISH-FAILED {a[2]}: {e}", flush=True); return 1
    if a[:1] == ["ensure-stream"]:
        print(json.dumps(asyncio.run(ensure_stream()))); return 0
    if a[:1] == ["collect"]:
        r = asyncio.run(collect(a[1], a[2])); print(json.dumps(r)); return 0 if r["ok"] else 1
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main())
