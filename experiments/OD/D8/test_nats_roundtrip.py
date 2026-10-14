#!/usr/bin/env python3
"""Round trip of nats_results.py from an NRP Job (PREREG-D8-RUN-DRAFT.md Section 9, item 5). Runs ON ATLAS.

One exempt-class Job generates a payload from a seed (incompressible, about 2.2 MB, so it travels as three chunks under
the 1 MiB payload limit), publishes it with nats_results.py through the in-cluster leaf, and prints its sha256. Atlas then
collects the subject from the OD_RESULTS stream and checks the copy against the sha256 it computes from the same seed,
independently of the Job.

    /home/claude/env/bin/python test_nats_roundtrip.py local          # Atlas-only check: publish to the hub and collect
    /home/claude/env/bin/python test_nats_roundtrip.py submit --i-have-checked-nrp-policy
    /home/claude/env/bin/python test_nats_roundtrip.py collect        # after the Job succeeds; writes nats_roundtrip_test.json
"""
from __future__ import annotations

import asyncio
import base64
import datetime as dt
import gzip
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

from nats_bursting.descriptor import JobDescriptor, Resources

from nats_results import collect as nr_collect
from nats_results import ensure_stream
from nats_results import publish as nr_publish
from submit_d8_nrp import ARG_LIMIT, IMAGE, created, kubectl, publish

HERE = Path(__file__).resolve().parent
NAME = "d8-nats-roundtrip"
SUBJECT = "od.results.test.roundtrip"
SEED, N = "nats-roundtrip-2026-10-14", 70_000  # N sha256 digests of 32 bytes each: 2.24 MB that gzip cannot shrink
PIN = "nats-py==2.14.0"  # the version on Atlas
TIMEOUT = "20m"


def payload() -> bytes:
    return b"".join(hashlib.sha256(f"{SEED}-{i}".encode()).digest() for i in range(N))


GEN = f"import hashlib; open('payload.bin','wb').write(b''.join(hashlib.sha256(f'{SEED}-{{i}}'.encode()).digest() for i in range({N})))"


def command(b64: str, sha: str) -> str:
    lines = ["set -euo pipefail", "export PYTHONUNBUFFERED=1 PIP_ROOT_USER_ACTION=ignore HOME=/work", "mkdir -p /work && cd /work",
             f"echo '{b64}' | base64 -d | gunzip > nats_results.py", f"echo '{sha}  nats_results.py' | sha256sum -c - || exit 3",
             f"pip install -q --no-cache-dir {PIN} 2>&1 | tail -1 || true", f"python -c \"{GEN}\"", "sha256sum payload.bin",
             f"timeout {TIMEOUT} python -u nats_results.py publish payload.bin {SUBJECT}"]
    return "\n".join(lines) + "\n"


def descriptor() -> JobDescriptor:
    raw = (HERE / "nats_results.py").read_bytes()
    cmd = command(base64.b64encode(gzip.compress(raw, mtime=0)).decode(), hashlib.sha256(raw).hexdigest())
    return JobDescriptor(name=NAME, image=IMAGE, command=["/bin/bash", "-c", cmd], env={"NATS_URL": "nats://atlas-nats:4222"},
                         resources=Resources(cpu="1", memory="2Gi", gpu=0, ephemeral_storage="2Gi"),
                         labels={"atlas.io/batch": "od-d8-nats-test", "atlas.io/role": "test", "app": "od-d8"}, backoff_limit=0)


def preflight(d: JobDescriptor) -> None:
    """The PREFLIGHT as code, as in submit_d8_nrp.py: exempt class, no sleep, bounded, backoff 0, name absent and short."""
    r = d.resources; body = " ".join(d.command); problems = []
    if r.gpu != 0 or float(r.cpu) > 1 or float(r.memory[:-2]) > 2 or not r.ephemeral_storage: problems.append("outside the exempt class")
    if "sleep" in body: problems.append("command contains sleep")
    if f"timeout {TIMEOUT}" not in body: problems.append("not bounded by timeout")
    if d.backoff_limit != 0: problems.append("backoff_limit must be 0")
    if len(d.name) > 63: problems.append("name too long")
    if max(len(a.encode()) for a in d.command) > ARG_LIMIT: problems.append("command argument over ARG_LIMIT")
    got = kubectl("get", "job", d.name, "-o", "name")
    if got.returncode == 0 and got.stdout.strip(): problems.append(f"Job {d.name} already exists (delete the finished one first)")
    dirty = subprocess.run(["git", "status", "--porcelain", "--", "nats_results.py", "test_nats_roundtrip.py"], capture_output=True, text=True, cwd=HERE).stdout.strip()
    if dirty: problems.append(f"shipped files differ from HEAD:\n{dirty}")
    if problems: raise SystemExit(f"PREFLIGHT VETO {d.name}: " + "; ".join(problems))


def main() -> int:
    a = sys.argv[1:]; expect = hashlib.sha256(payload()).hexdigest()
    if a[:1] == ["local"]:
        print(json.dumps(asyncio.run(ensure_stream())))
        tmp = HERE / "nats_roundtrip_local.bin"; tmp.write_bytes(payload())
        seqs = asyncio.run(nr_publish(str(tmp), "od.results.test.local", url="nats://localhost:4222"))
        r = asyncio.run(nr_collect("od.results.test.local", str(HERE / "nats_roundtrip_local.out")))
        ok = r.get("ok") and r.get("sha256") == expect
        print(json.dumps({"local": "PASS" if ok else "FAIL", "chunks_acked": len(seqs), "collect": r, "expected_sha256": expect}))
        tmp.unlink(); (HERE / "nats_roundtrip_local.out").unlink(missing_ok=True); return 0 if ok else 1
    if a[:1] == ["submit"]:
        if "--i-have-checked-nrp-policy" not in a: sys.exit("refusing without --i-have-checked-nrp-policy")
        print(json.dumps(asyncio.run(ensure_stream())))
        d = descriptor(); preflight(d); t_sub = dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=5)
        ev = asyncio.run(publish(d)); c = None
        for _ in range(12):
            c = created(d.name)
            if c: break
            time.sleep(5)
        print(json.dumps({"job": d.name, "status_events": ev, "creationTimestamp": c.isoformat() if c else None, "fresh": c is not None and c >= t_sub}))
        return 0
    if a[:1] == ["collect"]:
        st = kubectl("get", "job", NAME, "-o", "jsonpath={.status.succeeded}/{.status.failed}").stdout.strip()
        log = kubectl("logs", f"job/{NAME}").stdout if st.startswith("1/") else ""
        pod_sha = next((ln.split()[0] for ln in log.splitlines() if ln.endswith("payload.bin")), None)
        published = next((ln for ln in log.splitlines() if ln.startswith("NATS-PUBLISH")), None)
        out = HERE / "nats_roundtrip.bin"; r = asyncio.run(nr_collect(SUBJECT, str(out)))
        ok = bool(r.get("ok")) and r.get("sha256") == expect == pod_sha and published is not None and published.startswith("NATS-PUBLISHED")
        res = {"test": "nats_results.py round trip from an NRP Job, PREREG-D8-RUN-DRAFT.md Section 9 item 5", "job": NAME, "job_status": st,
               "subject": SUBJECT, "payload_bytes": len(payload()), "expected_sha256": expect, "pod_sha256": pod_sha, "pod_publish_line": published,
               "collect": r, "result": "PASS" if ok else "FAIL"}
        out.unlink(missing_ok=True); (HERE / "nats_roundtrip_test.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(json.dumps(res, indent=1)); return 0 if ok else 1
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main())
