#!/usr/bin/env python3
"""Submit the D9 barrier probe to NRP via nats-bursting, one CPU Job per world, and collect the results. Runs ON ATLAS from
the repository checkout (it needs the NATS hub and kubectl).

The transport is D8's, imported and not copied: `publish` (status subscription opened BEFORE publishing, since submit
errors go to burst.status.<job_id> and are never logged), `created` (fresh creationTimestamp after submit) and `kubectl`.
The preflight is D9's own, scored against the PREFLIGHT of reference_nrp_job_policies line by line:
  * CPU-only (gpu = 0): stiff ODE systems of at most 2 x 40 unknowns; no GPU rule can apply.
  * Exempt class: cpu = 1, memory = 2Gi, requests == limits, ephemeral-storage 2Gi declared. The working set is a few
    tens of MiB (40 x 2001 samples per run); the only risk the class leaves is OOM, and the job's own footprint is
    recorded. OMP_NUM_THREADS = 1.
  * Self-terminating: bounded by `timeout`; no sleep anywhere in the Job; backoff_limit = 0.
  * Self-contained: d9_barrier.py and prereg_config.json ride in as base64 with sha256 asserted; numpy and scipy are
    pinned to the versions the self-test passed on at Atlas; the self-test runs in the pod before the probe.
  * Names checked absent before submit; logs read only from Jobs that succeeded (a dead node makes kubectl logs hang).
  * No deletes here except `--cleanup`, which refuses any Job that has not finished.

Usage (on Atlas, from experiments/OD/D9):
  /home/claude/env/bin/python submit_d9_nrp.py --dry-run
  /home/claude/env/bin/python submit_d9_nrp.py --i-have-checked-nrp-policy
  /home/claude/env/bin/python submit_d9_nrp.py --collect        # writes probe_<world>.json and .log, merges into probe.json
  /home/claude/env/bin/python submit_d9_nrp.py --cleanup        # deletes finished D9 probe Jobs only
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
from pathlib import Path

from nats_bursting.descriptor import JobDescriptor, Resources

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "D8"))
from submit_d8_nrp import created, kubectl, publish  # noqa: E402

BATCH = "od-d9-probe"
IMAGE = "python:3.12-slim"
PINS = "numpy==2.2.6 scipy==1.17.1"  # the versions the D9 self-test passed on at Atlas (2026-10-10, 2d004ec)
FILES = {"OD/D9/d9_barrier.py": HERE / "d9_barrier.py", "OD/D9/prereg_config.json": HERE / "prereg_config.json"}
TIMEOUT = "12h"  # cost unmeasured: C2 runs one stiff nudged integration per observer and shell count, up to J = 40
CPU, MEM, EPH = "1", "2Gi", "2Gi"
BEGIN, END = "----BEGIN d9 result gz-b64----", "----END d9 result----"


def config() -> dict:
    return json.loads(FILES["OD/D9/prereg_config.json"].read_text(encoding="utf-8"))


def worlds_for(role: str) -> list[str]:
    cfg = config(); return [w["name"] for w in cfg["worlds"] if w.get("group") in cfg["groups_by_role"][role]]


def job_name(world: str, role: str) -> str:
    return f"d9-{role}-" + world.replace("_", "-").lower()


def command(world: str, role: str, blobs: dict[str, tuple[str, str]]) -> str:
    out = "results.json" if role == "run" else f"{role}_{world}.json"
    lines = ["set -euo pipefail", "export PYTHONUNBUFFERED=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PIP_ROOT_USER_ACTION=ignore HOME=/work",
             "mkdir -p /work/OD/D9"]
    for rel, (b64, sha) in blobs.items():
        lines += [f"echo '{b64}' | base64 -d > /work/{rel}", f"echo '{sha}  /work/{rel}' | sha256sum -c - || exit 3"]
    lines += [f"pip install -q --no-cache-dir {PINS} 2>&1 | tail -1 || true",
              "python -c \"import numpy, scipy, sys; print('numpy', numpy.__version__, 'scipy', scipy.__version__, 'python', sys.version.split()[0])\"",
              "cd /work/OD/D9", "python -u d9_barrier.py --selftest",
              f"timeout {TIMEOUT} python -u d9_barrier.py --config prereg_config.json --seed-role {role} --world {world} --out {out}",
              f"echo '{BEGIN}'", f"gzip -c {out} | base64 -w0", "echo", f"echo '{END}'"]
    return "\n".join(lines) + "\n"


def descriptor(world: str, role: str, blobs, head: str) -> JobDescriptor:
    return JobDescriptor(name=job_name(world, role), image=IMAGE, command=["/bin/bash", "-c", command(world, role, blobs)],
                         env={"D9_WORLD": world, "D9_ROLE": role, "D9_HEAD": head}, resources=Resources(cpu=CPU, memory=MEM, gpu=0, ephemeral_storage=EPH),
                         labels={"atlas.io/batch": BATCH if role == "probe" else f"od-d9-{role}", "atlas.io/role": role, "app": "od-d9"}, backoff_limit=0)


def preflight(d: JobDescriptor) -> None:
    """The PREFLIGHT as code; the exempt class is the only class this submitter may use."""
    r = d.resources; problems = []
    if r.gpu != 0: problems.append("GPU requested for a CPU workload")
    if float(r.cpu) > 1: problems.append(f"cpu {r.cpu} outside the exempt class (<= 1)")
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


def submit(role: str, dry: bool) -> int:
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=HERE).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", *[str(p) for p in FILES.values()]], capture_output=True, text=True, cwd=HERE).stdout.strip()
    if dirty: raise SystemExit(f"PREFLIGHT VETO: shipped files differ from HEAD {head}:\n{dirty}")
    if role == "run" and not (HERE / "PREREG-D9.md").exists(): raise SystemExit("PREFLIGHT VETO: the run role needs the sealed PREREG-D9.md")
    blobs = {}
    for rel, p in FILES.items():
        raw = p.read_bytes(); blobs[rel] = (base64.b64encode(raw).decode(), hashlib.sha256(raw).hexdigest())
    worlds = worlds_for(role); descs = [descriptor(w, role, blobs, head) for w in worlds]
    for d in descs: preflight(d)
    print(json.dumps({"head": head, "role": role, "jobs": [d.name for d in descs], "sha256": {k: v[1] for k, v in blobs.items()},
                      "resources": {"cpu": CPU, "memory": MEM, "ephemeral_storage": EPH}, "timeout": TIMEOUT, "pins": PINS}, indent=1))
    if dry:
        print(command(worlds[0], role, {k: ("<b64>", v[1]) for k, v in blobs.items()})); return 0
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


def collect(role: str) -> int:
    merged = None
    for w in worlds_for(role):
        name = job_name(w, role); st = kubectl("get", "job", name, "-o", "jsonpath={.status.succeeded}/{.status.failed}").stdout.strip()
        if not st.startswith("1/"):  # never read logs of a Job that has not succeeded: a dead node makes kubectl logs hang
            print(f"{name}: status {st or 'absent'}, not collected"); continue
        log = kubectl("logs", f"job/{name}").stdout
        if BEGIN not in log:
            print(f"{name}: succeeded but no result block; last lines:\n" + "\n".join(log.splitlines()[-8:])); continue
        res = json.loads(gzip.decompress(base64.b64decode(log.split(BEGIN, 1)[1].split(END, 1)[0].strip())))
        out = HERE / f"{role}_{w}.json"; out.write_text(json.dumps(res, indent=1), encoding="utf-8")
        (HERE / f"{role}_{w}.log").write_text(log.split(BEGIN, 1)[0], encoding="utf-8")
        print(f"{name}: wrote {out.name} and {out.stem}.log")
        if merged is None: merged = {k: v for k, v in res.items() if k != "worlds"} | {"worlds": []}
        merged["worlds"] += res["worlds"]
    if merged:
        (HERE / f"{role}.json").write_text(json.dumps(merged, indent=1), encoding="utf-8"); print(f"merged {role}.json:", len(merged["worlds"]), "worlds")
    return 0


def cleanup(role: str) -> int:
    for w in worlds_for(role):
        name = job_name(w, role); got = kubectl("get", "job", name, "-o", "jsonpath={.status.succeeded}/{.status.failed}/{.status.active}")
        if got.returncode != 0: print(f"{name}: absent"); continue
        s, f, a = (got.stdout.strip().split("/") + ["", "", ""])[:3]
        if a not in ("", "0") or (s in ("", "0") and f in ("", "0")):
            print(f"{name}: NOT finished (succeeded={s} failed={f} active={a}); refusing to delete a running Job"); continue
        print(name, kubectl("delete", "job", name).stdout.strip())
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-have-checked-nrp-policy", action="store_true", dest="ack")
    ap.add_argument("--role", default="probe", choices=["probe", "pilot", "run"])
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--collect", action="store_true"); ap.add_argument("--cleanup", action="store_true")
    a = ap.parse_args()
    if a.collect: return collect(a.role)
    if a.cleanup: return cleanup(a.role)
    if not a.ack and not a.dry_run:
        sys.exit("refusing without --i-have-checked-nrp-policy (read reference_nrp_job_policies first)")
    return submit(a.role, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
