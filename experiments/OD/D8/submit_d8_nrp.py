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
IMAGE = "python:3.12-slim"
NUMPY = "2.2.6"  # the version the self-test passed on at Atlas
HERE = Path(__file__).resolve().parent
FILES = {"OD/D5/d5_burgers.py": HERE.parent / "D5" / "d5_burgers.py", "OD/D8/d8_sync.py": HERE / "d8_sync.py", "OD/D8/prereg_config.json": HERE / "prereg_config.json"}
# Per role: the Job parts (d8_sync.py --parts), whether each test trajectory is its own Job, the timeout, the batch label.
# Probe round 3 at n = 96 measured 2.4 to 3.0 h per core or dt/2 part. The pilot at n = 128 is estimated at about 12 h for
# its core part (four graded observers with the observer and block exponents, the instrument group and training), so each
# pilot Job is one (world, test trajectory, part) and the bound is 20 h.
ROLES = {
    "probe": {"parts": {"core": "instrument,graded", "others": "others", "dthalf": "dthalf"}, "per_test": False, "timeout": "16h", "batch": "od-d8-probe"},
    "pilot": {"parts": {"core": "instrument,graded", "others": "others", "mu4": "murecord"}, "per_test": True, "timeout": "20h", "batch": "od-d8-pilot"},
}
JOB_PARTS = ROLES["probe"]["parts"]  # kept for the probe rounds' collections and for importers
TIMEOUT = ROLES["probe"]["timeout"]
CPU, MEM, EPH = "1", "2Gi", "2Gi"
BEGIN, END = "----BEGIN d8 result gz-b64----", "----END d8 result----"


def kubectl(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["kubectl", "-n", NS, *args], capture_output=True, text=True)


def config() -> dict:
    return json.loads(FILES["OD/D8/prereg_config.json"].read_text(encoding="utf-8"))


def role_worlds(role: str = "probe") -> list[str]:
    cfg = config(); return [w["name"] for w in cfg["worlds"] if w["group"] in cfg["groups_by_role"][role]]


def probe_worlds() -> list[str]:
    return role_worlds("probe")


def job_name(world: str, part: str | None = None, role: str = "probe", test: int | None = None) -> str:
    return f"d8-{role}-" + world.replace("_", "-").lower() + (f"-t{test}" if test is not None else "") + (f"-{part}" if part else "")


def units(role: str, split: bool) -> list[tuple[str, int | None, str | None]]:
    """(world, test trajectory or None, part or None) for every Job of the role."""
    R = ROLES[role]; K = int(config()["K_by_role"][role])
    tests = list(range(K)) if R["per_test"] else [None]
    parts = list(R["parts"]) if (split or role != "probe") else [None]
    return [(w, t, p) for w in role_worlds(role) for t in tests for p in parts]


def command(world: str, blobs: dict[str, tuple[str, str]], part: str | None = None, role: str = "probe", test: int | None = None) -> str:
    R = ROLES[role]
    tag = "_".join(x for x in (world, f"t{test}" if test is not None else "", part or "") if x)
    extra = (f" --parts {R['parts'][part]}" if part else "") + (f" --tests {test}" if test is not None else "")
    lines = ["set -euo pipefail", "export PYTHONUNBUFFERED=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PIP_ROOT_USER_ACTION=ignore HOME=/work",
             "mkdir -p /work/OD/D5 /work/OD/D8"]
    for rel, (b64, sha) in blobs.items():
        lines += [f"echo '{b64}' | base64 -d > /work/{rel}", f"echo '{sha}  /work/{rel}' | sha256sum -c - || exit 3"]
    lines += [f"pip install -q --no-cache-dir numpy=={NUMPY} 2>&1 | tail -1 || true",
              "python -c \"import numpy, sys; print('numpy', numpy.__version__, 'python', sys.version.split()[0])\"",
              "cd /work/OD/D8", "python -u d8_sync.py --selftest",
              f"timeout {R['timeout']} python -u d8_sync.py --config prereg_config.json --seed-role {role} --world {world}{extra} --out {role}_{tag}.json",
              f"echo '{BEGIN}'", f"gzip -c {role}_{tag}.json | base64 -w0", "echo", f"echo '{END}'"]
    return "\n".join(lines) + "\n"


def descriptor(world: str, blobs, head: str, part: str | None = None, role: str = "probe", test: int | None = None) -> JobDescriptor:
    return JobDescriptor(name=job_name(world, part, role, test), image=IMAGE, command=["/bin/bash", "-c", command(world, blobs, part, role, test)],
                         env={"D8_WORLD": world, "D8_HEAD": head, "D8_PART": part or "all", "D8_ROLE": role, "D8_TEST": "all" if test is None else str(test)},
                         resources=Resources(cpu=CPU, memory=MEM, gpu=0, ephemeral_storage=EPH),
                         labels={"atlas.io/batch": ROLES[role]["batch"], "atlas.io/role": role, "app": "od-d8"}, backoff_limit=0)


def preflight(d: JobDescriptor, role: str = "probe") -> None:
    """The PREFLIGHT as code. The exempt class is the only class this submitter may use. The footprints measured on the
    probe (about 220 MiB at n = 96, one core) keep the pilot well inside it; the pilot's n = 128 parts record their own."""
    r = d.resources; problems = []
    if r.gpu != 0: problems.append("GPU requested for a CPU workload")
    if float(r.cpu) > 1: problems.append(f"cpu {r.cpu} outside the exempt class (<= 1)")
    if not r.memory.endswith("Gi") or float(r.memory[:-2]) > 2: problems.append(f"memory {r.memory} outside the exempt class (<= 2Gi)")
    if not r.ephemeral_storage: problems.append("ephemeral-storage not declared")
    body = " ".join(d.command)
    if "sleep" in body: problems.append("command contains sleep")
    if f"timeout {ROLES[role]['timeout']}" not in body: problems.append("run not bounded by timeout")
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


def submit(dry: bool, split: bool = False, role: str = "probe") -> int:
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=HERE).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", *[str(p) for p in FILES.values()]], capture_output=True, text=True, cwd=HERE).stdout.strip()
    if dirty: raise SystemExit(f"PREFLIGHT VETO: shipped files differ from HEAD {head}:\n{dirty}")
    if role == "run" or role not in ROLES: raise SystemExit(f"PREFLIGHT VETO: role {role} is not submittable here (the run needs the sealed PREREG-D8.md and its own entry)")
    blobs = {}
    for rel, p in FILES.items():
        raw = p.read_bytes(); blobs[rel] = (base64.b64encode(raw).decode(), hashlib.sha256(raw).hexdigest())
    us = units(role, split); descs = [descriptor(w, blobs, head, p, role, t) for w, t, p in us]
    for d in descs: preflight(d, role)
    print(json.dumps({"head": head, "role": role, "n_jobs": len(descs), "jobs": [d.name for d in descs], "sha256": {k: v[1] for k, v in blobs.items()},
                      "resources": {"cpu": CPU, "memory": MEM, "ephemeral_storage": EPH}, "timeout": ROLES[role]["timeout"]}, indent=1))
    if dry:
        w, t, p = us[0]; print(command(w, {k: ("<b64>", v[1]) for k, v in blobs.items()}, p, role, t)); return 0
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


def fetch(name: str):
    st = kubectl("get", "job", name, "-o", "jsonpath={.status.succeeded}/{.status.failed}").stdout.strip()
    if not st.startswith("1/"):  # never read logs of a Job that has not succeeded: a dead node makes kubectl logs hang
        print(f"{name}: status {st or 'absent'}, not collected"); return None, st
    log = kubectl("logs", f"job/{name}").stdout
    if BEGIN not in log:
        print(f"{name}: status {st}, no result block; last lines:\n" + "\n".join(log.splitlines()[-8:])); return None, st
    blob = log.split(BEGIN, 1)[1].split(END, 1)[0].strip()
    return (json.loads(gzip.decompress(base64.b64decode(blob))), log.split(BEGIN, 1)[0]), st


def merge_parts(pieces: dict) -> dict:
    """Merge one world's results from several Jobs (parts and/or test trajectories). Training and every test trajectory's
    u0 are seed-deterministic, so all pieces share rankings, and a test trajectory is identified by its index; observers,
    dt_half, mu_record and the instrument fields are unioned per index, and test trajectories are sorted by index."""
    first = next(iter(pieces.values())); base = json.loads(json.dumps(first))
    w0 = base["worlds"][0]; w0["parts"] = sorted({p for r in pieces.values() for p in r["worlds"][0]["parts"]}); base["footprints_by_part"] = {}
    tests = {}
    for key, r in pieces.items():
        base["footprints_by_part"][key] = r.get("footprint")
        w = r["worlds"][0]
        if w["rankings"] != w0["rankings"]: raise SystemExit(f"piece {key} has different rankings: the pieces are not the same world")
        for t in w["tests"]:
            t0 = tests.setdefault(t["index"], {"index": t["index"], "spectrum_tail": t["spectrum_tail"], "observers": {}, "mu_record": {}, "dt_half": {}})
            t0["observers"].update(t["observers"]); t0["dt_half"].update(t["dt_half"])
            for mu, d in t["mu_record"].items():
                t0["mu_record"].setdefault(mu, {}).update(d)
            for k in ("lyapunov", "none_final", "all_final", "all_hold_max"):
                if k in t: t0[k] = t[k]
    w0["tests"] = [tests[i] for i in sorted(tests)]
    return base


def collect(worlds: list[str] | None = None, tag: str = "", split: bool = False, role: str = "probe") -> int:
    merged = None
    R = ROLES[role]; K = int(config()["K_by_role"][role])
    for w in worlds or role_worlds(role):
        name = job_name(w, None, role)
        if split or role != "probe":
            pieces = {}; logs = []
            for t in (range(K) if R["per_test"] else [None]):
                for part in R["parts"]:
                    key = "_".join(x for x in (f"t{t}" if t is not None else "", part) if x)
                    got, st = fetch(job_name(w, part, role, t))
                    if got: pieces[key] = got[0]; logs.append(f"===== {key}\n" + got[1])
            if not pieces: continue
            res = merge_parts(pieces); log = "\n".join(logs) + "\n"; st = "pieces " + ",".join(sorted(pieces))
        else:
            got, st = fetch(name)
            if not got: continue
            res, log = got
        out = HERE / f"{role}_{w}.json"; out.write_text(json.dumps(res, indent=1), encoding="utf-8")
        (HERE / f"{role}_{w}.log").write_text(log, encoding="utf-8")
        print(f"{name}: status {st}, wrote {out.name} and {out.stem}.log")
        if merged is None: merged = {k: v for k, v in res.items() if k != "worlds"} | {"worlds": [], "footprints": {}}
        merged["worlds"] += res["worlds"]; merged["footprints"][w] = res.get("footprints_by_part", res.get("footprint"))
    if merged:
        (HERE / f"{role}{tag}.json").write_text(json.dumps(merged, indent=1), encoding="utf-8"); print(f"merged {role}{tag}.json:", len(merged["worlds"]), "worlds")
    return 0


def cleanup(worlds: list[str] | None = None, split: bool = False, role: str = "probe") -> int:
    R = ROLES[role]; K = int(config()["K_by_role"][role])
    names = [job_name(w, p, role, t) for w in (worlds or role_worlds(role)) for t in (range(K) if R["per_test"] else [None])
             for p in (R["parts"] if (split or role != "probe") else [None])]
    for name in names:
        got = kubectl("get", "job", name, "-o", "jsonpath={.status.succeeded}/{.status.failed}/{.status.active}")
        if got.returncode != 0: print(f"{name}: absent"); continue
        s, f, a = (got.stdout.strip().split("/") + ["", "", ""])[:3]
        if a not in ("", "0") or (s in ("", "0") and f in ("", "0")):
            print(f"{name}: NOT finished (succeeded={s} failed={f} active={a}); refusing to delete a running Job"); continue
        print(name, kubectl("delete", "job", name).stdout.strip())
    return 0


def selftest() -> int:
    """Checks merge_parts on constructed pieces: two test trajectories split across parts merge by index."""
    def piece(parts, tests):
        return {"worlds": [{"parts": parts, "rankings": {"READ": [[1, 0]]}, "tests": tests}], "footprint": {"x": 1}}
    a = piece(["instrument", "graded"], [{"index": 1, "spectrum_tail": 0.1, "observers": {"READ": {"m_star": 8}}, "mu_record": {}, "dt_half": {}, "lyapunov": 0.2, "none_final": 1, "all_final": 0, "all_hold_max": 0}])
    b = piece(["others"], [{"index": 1, "spectrum_tail": 0.1, "observers": {"SENS": {"m_star": None}}, "mu_record": {}, "dt_half": {}}])
    c = piece(["instrument", "graded"], [{"index": 0, "spectrum_tail": 0.2, "observers": {"READ": {"m_star": 16}}, "mu_record": {"12.5": {"READ": {"m_star": 24}}}, "dt_half": {}, "lyapunov": 0.3, "none_final": 1, "all_final": 0, "all_hold_max": 0}])
    m = merge_parts({"t1_core": a, "t1_others": b, "t0_core": c}); t = m["worlds"][0]["tests"]
    ok = [x["index"] for x in t] == [0, 1] and sorted(t[1]["observers"]) == ["READ", "SENS"] and t[0]["mu_record"]["12.5"]["READ"]["m_star"] == 24 and t[1]["lyapunov"] == 0.2
    names = [job_name("p_nu030_n128", "core", "pilot", 1), job_name("pr3_nu020_n96", "others")]
    ok = ok and names == ["d8-pilot-p-nu030-n128-t1-core", "d8-probe-pr3-nu020-n96-others"] and all(len(n) <= 63 for n in names)
    print("merge by trajectory index and job names:", "PASS" if ok else "FAIL", names)
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-have-checked-nrp-policy", action="store_true", dest="ack")
    ap.add_argument("--role", default="probe", choices=["probe", "pilot"])
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--collect", action="store_true"); ap.add_argument("--cleanup", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--worlds", default=None, help="comma-separated world names for --collect/--cleanup (e.g. an earlier probe round)")
    ap.add_argument("--tag", default="", help="suffix for the merged file, <role><tag>.json")
    ap.add_argument("--split", action="store_true", help="probe only: three Jobs per world (core, others, dthalf); the pilot is always split per trajectory and part")
    a = ap.parse_args(); ws = a.worlds.split(",") if a.worlds else None
    if a.selftest: return selftest()
    if a.collect: return collect(ws, a.tag, a.split, a.role)
    if a.cleanup: return cleanup(ws, a.split, a.role)
    if not a.ack and not a.dry_run:
        sys.exit("refusing without --i-have-checked-nrp-policy (read reference_nrp_job_policies first)")
    return submit(a.dry_run, a.split, a.role)


if __name__ == "__main__":
    sys.exit(main())
