#!/usr/bin/env python3
"""Submit the D8 probe to NRP via nats-bursting, one Job per probe world, and collect the results. Runs ON ATLAS from the
repository checkout (it needs the NATS hub and kubectl).

Scored against the PREFLIGHT of reference_nrp_job_policies, line by line, and enforced in preflight() below:
  * CPU-only (gpu = 0): numpy pseudo-spectral solver; no GPU rule can apply.
  * Exempt class: cpu = 1, memory = 2Gi, requests == limits (the renderer sets them equal), ephemeral-storage 2Gi
    declared. The utilization bands do not apply in this class; the solver is single-threaded (OMP_NUM_THREADS = 1)
    and its working set at n = 64 is a few hundred MiB, so the only risk the class leaves is OOM, which the job's
    self-measured peak RSS (footprint in its output) will show. That measurement sizes the pilot's n = 96 Jobs.
  * Self-terminating: the run is bounded by `timeout`; no sleep anywhere; backoff_limit = 0.
  * Self-contained: no PVC, no ConfigMap. d5_burgers.py, d8_sync.py and prereg_config.json ride in as base64 and their
    sha256 is asserted after decode; the code's own self-test runs in the pod before the probe.
  * Submitted through burst.submit with a status subscription opened BEFORE publishing (submit errors are published to
    burst.status.<job_id> and never logged); names checked absent before submit; creationTimestamp checked fresh after.
  * Results come back in the Job log between markers (gzip + base64), no PVC round trip.
  * No deletes of any Job here; completed Jobs are cleaned by `--cleanup`, which refuses a Job that has not finished.

Usage (on Atlas, from experiments/OD/D8):
  /home/claude/env/bin/python submit_d8_nrp.py --dry-run
  /home/claude/env/bin/python submit_d8_nrp.py --i-have-checked-nrp-policy
  /home/claude/env/bin/python submit_d8_nrp.py --collect        # writes probe_<world>.json, merges into probe.json
  /home/claude/env/bin/python submit_d8_nrp.py --cleanup        # deletes finished d8 probe Jobs only
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import datetime as dt
import gzip
import hashlib
import json
import subprocess
import sys
import time
import uuid
from pathlib import Path

from nats_bursting.descriptor import JobDescriptor, Resources

NS = "ssu-atlas-ai"
BATCH = "od-d8-probe"
IMAGE = "python:3.12-slim"
NUMPY = "2.2.6"  # the version the self-test passed on at Atlas
HERE = Path(__file__).resolve().parent
FILES = {"OD/D5/d5_burgers.py": HERE.parent / "D5" / "d5_burgers.py", "OD/D8/d8_sync.py": HERE / "d8_sync.py", "OD/D8/prereg_config.json": HERE / "prereg_config.json"}
TIMEOUT = "4h"
CPU, MEM, EPH = "1", "2Gi", "2Gi"
BEGIN, END = "----BEGIN d8 result gz-b64----", "----END d8 result----"


def kubectl(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["kubectl", "-n", NS, *args], capture_output=True, text=True)


def probe_worlds() -> list[str]:
    cfg = json.loads(FILES["OD/D8/prereg_config.json"].read_text(encoding="utf-8"))
    return [w["name"] for w in cfg["worlds"] if w["group"] in cfg["groups_by_role"]["probe"]]


def job_name(world: str) -> str:
    return "d8-probe-" + world.replace("_", "-").lower()


def command(world: str, blobs: dict[str, tuple[str, str]]) -> str:
    lines = ["set -euo pipefail", "export PYTHONUNBUFFERED=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PIP_ROOT_USER_ACTION=ignore HOME=/work",
             "mkdir -p /work/OD/D5 /work/OD/D8"]
    for rel, (b64, sha) in blobs.items():
        lines += [f"echo '{b64}' | base64 -d > /work/{rel}", f"echo '{sha}  /work/{rel}' | sha256sum -c - || exit 3"]
    lines += [f"pip install -q --no-cache-dir numpy=={NUMPY} 2>&1 | tail -1 || true",
              "python -c \"import numpy, sys; print('numpy', numpy.__version__, 'python', sys.version.split()[0])\"",
              "cd /work/OD/D8", "python -u d8_sync.py --selftest",
              f"timeout {TIMEOUT} python -u d8_sync.py --config prereg_config.json --seed-role probe --world {world} --out probe_{world}.json",
              f"echo '{BEGIN}'", f"gzip -c probe_{world}.json | base64 -w0", "echo", f"echo '{END}'"]
    return "\n".join(lines) + "\n"


def descriptor(world: str, blobs, head: str) -> JobDescriptor:
    return JobDescriptor(name=job_name(world), image=IMAGE, command=["/bin/bash", "-c", command(world, blobs)],
                         env={"D8_WORLD": world, "D8_HEAD": head}, resources=Resources(cpu=CPU, memory=MEM, gpu=0, ephemeral_storage=EPH),
                         labels={"atlas.io/batch": BATCH, "atlas.io/role": "probe", "app": "od-d8"}, backoff_limit=0)


def preflight(d: JobDescriptor) -> None:
    """The PREFLIGHT as code. The exempt class is the only class this submitter may use: anything larger would need a
    measured footprint, and none exists yet."""
    r = d.resources; problems = []
    if r.gpu != 0: problems.append("GPU requested for a CPU workload")
    if float(r.cpu) > 1: problems.append(f"cpu {r.cpu} outside the exempt class (<= 1) with no measured footprint")
    if not r.memory.endswith("Gi") or float(r.memory[:-2]) > 2: problems.append(f"memory {r.memory} outside the exempt class (<= 2Gi)")
    if not r.ephemeral_storage: problems.append("ephemeral-storage not declared")
    body = " ".join(d.command)
    if "sleep" in body: problems.append("command contains sleep")
    if f"timeout {TIMEOUT}" not in body: problems.append("run not bounded by timeout")
    if d.backoff_limit != 0: problems.append("backoff_limit must be 0")
    got = kubectl("get", "job", d.name, "-o", "name")
    if got.returncode == 0 and got.stdout.strip(): problems.append(f"Job {d.name} already exists (delete the finished one first)")
    if problems:
        raise SystemExit(f"PREFLIGHT VETO {d.name}: " + "; ".join(problems))


async def publish(d: JobDescriptor, listen_s: float = 15.0) -> list[dict]:
    import nats
    nc = await nats.connect("nats://localhost:4222"); seen = []; jid = f"{d.name}-{uuid.uuid4().hex[:8]}"

    async def on_msg(msg):
        try:
            ev = json.loads(msg.data.decode())
        except Exception:
            ev = {"raw": msg.data.decode(errors="replace")}
        if msg.subject.endswith(jid): seen.append(ev)

    await nc.subscribe("burst.status.>", cb=on_msg); await nc.flush()
    await nc.publish("burst.submit", json.dumps({"job_id": jid, "descriptor": d.to_dict()}).encode()); await nc.flush()
    t0 = time.time()
    while time.time() - t0 < listen_s and not any(e.get("state") in ("submitted", "error") for e in seen):
        await asyncio.sleep(0.5)  # local event-loop wait on Atlas while listening for the status reply, not in any Job
    await nc.close()
    return seen


def created(name: str) -> dt.datetime | None:
    got = kubectl("get", "job", name, "-o", "jsonpath={.metadata.creationTimestamp}")
    if got.returncode != 0 or not got.stdout.strip(): return None
    return dt.datetime.fromisoformat(got.stdout.strip().replace("Z", "+00:00"))


def submit(dry: bool) -> int:
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=HERE).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", *[str(p) for p in FILES.values()]], capture_output=True, text=True, cwd=HERE).stdout.strip()
    if dirty: raise SystemExit(f"PREFLIGHT VETO: shipped files differ from HEAD {head}:\n{dirty}")
    blobs = {}
    for rel, p in FILES.items():
        raw = p.read_bytes(); blobs[rel] = (base64.b64encode(raw).decode(), hashlib.sha256(raw).hexdigest())
    worlds = probe_worlds(); descs = [descriptor(w, blobs, head) for w in worlds]
    for d in descs: preflight(d)
    print(json.dumps({"head": head, "jobs": [d.name for d in descs], "sha256": {k: v[1] for k, v in blobs.items()},
                      "resources": {"cpu": CPU, "memory": MEM, "ephemeral_storage": EPH}, "timeout": TIMEOUT}, indent=1))
    if dry:
        print(command(worlds[0], {k: ("<b64>", v[1]) for k, v in blobs.items()})); return 0
    for i, d in enumerate(descs):
        if i: time.sleep(20)  # space submissions apart on Atlas (no churn); this is the submitter, not a Job
        t_sub = dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=5)
        ev = asyncio.run(publish(d)); c = None
        for _ in range(12):
            c = created(d.name)
            if c: break
            time.sleep(5)
        fresh = c is not None and c >= t_sub
        print(json.dumps({"job": d.name, "status_events": ev, "creationTimestamp": c.isoformat() if c else None, "fresh": fresh}), flush=True)
        if not fresh:
            raise SystemExit(f"{d.name}: no fresh Job after submit; read the status events above before anything else")
    return 0


def collect() -> int:
    merged = None
    for w in probe_worlds():
        name = job_name(w); st = kubectl("get", "job", name, "-o", "jsonpath={.status.succeeded}/{.status.failed}").stdout.strip()
        log = kubectl("logs", f"job/{name}").stdout
        if BEGIN not in log:
            print(f"{name}: status {st}, no result block yet; last lines:\n" + "\n".join(log.splitlines()[-8:])); continue
        blob = log.split(BEGIN, 1)[1].split(END, 1)[0].strip(); res = json.loads(gzip.decompress(base64.b64decode(blob)))
        out = HERE / f"probe_{w}.json"; out.write_text(json.dumps(res, indent=1), encoding="utf-8")
        (HERE / f"probe_{w}.log").write_text(log.split(BEGIN, 1)[0], encoding="utf-8")
        print(f"{name}: status {st}, wrote {out.name} and {out.stem}.log; footprint {res.get('footprint')}")
        if merged is None: merged = {k: v for k, v in res.items() if k != "worlds"} | {"worlds": [], "footprints": {}}
        merged["worlds"] += res["worlds"]; merged["footprints"][w] = res.get("footprint")
    if merged:
        (HERE / "probe.json").write_text(json.dumps(merged, indent=1), encoding="utf-8"); print("merged probe.json:", len(merged["worlds"]), "worlds")
    return 0


def cleanup() -> int:
    for w in probe_worlds():
        name = job_name(w); got = kubectl("get", "job", name, "-o", "jsonpath={.status.succeeded}/{.status.failed}/{.status.active}")
        if got.returncode != 0: print(f"{name}: absent"); continue
        s, f, a = (got.stdout.strip().split("/") + ["", "", ""])[:3]
        if a not in ("", "0") or (s in ("", "0") and f in ("", "0")):
            print(f"{name}: NOT finished (succeeded={s} failed={f} active={a}); refusing to delete a running Job"); continue
        print(name, kubectl("delete", "job", name).stdout.strip())
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-have-checked-nrp-policy", action="store_true", dest="ack")
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--collect", action="store_true"); ap.add_argument("--cleanup", action="store_true")
    a = ap.parse_args()
    if a.collect: return collect()
    if a.cleanup: return cleanup()
    if not a.ack and not a.dry_run:
        sys.exit("refusing without --i-have-checked-nrp-policy (read reference_nrp_job_policies first)")
    return submit(a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
