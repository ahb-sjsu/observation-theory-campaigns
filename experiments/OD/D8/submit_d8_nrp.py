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
  * Self-contained: no PVC, no ConfigMap. d5_burgers.py, d8_sync.py and prereg_config.json ride in gzip-compressed as
    base64 and their sha256 is asserted after decode; the code's own self-test runs in the pod before the probe. No exec
    argument may exceed ARG_LIMIT (Linux refuses one over 128 KiB; the variant probe's first 12 Jobs died of it).
  * Submitted through burst.submit with a status subscription opened BEFORE publishing (submit errors are published to
    burst.status.<job_id> and never logged); names checked absent before submit; creationTimestamp checked fresh after.
  * Results come back in the Job log between markers (gzip + base64), no PVC round trip. A role with "nats" also
    publishes the result file into the hub's OD_RESULTS stream (nats_results.py, through the in-cluster leaf) before the
    log block, so a lost log does not lose the result; a failed publish is logged and the log block still follows.
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
# Shipped only to roles with "nats": the results transport of PREREG-D8-RUN-DRAFT.md Section 8, round trip tested from an
# NRP Job (nats_roundtrip_test.json); nats-py pinned to Atlas's version, the leaf at its in-cluster service
NATS_FILES = {"OD/D8/nats_results.py": HERE / "nats_results.py"}
NATS_PIN, NATS_URL, NATS_TIMEOUT = "nats-py==2.14.0", "nats://atlas-nats:4222", "10m"
# Per role: the Job parts (d8_sync.py --parts), whether each test trajectory is its own Job, the timeout, the batch label.
# Probe round 3 at n = 96 measured 2.4 to 3.0 h per core or dt/2 part. The pilot at n = 128 is estimated at about 12 h for
# its core part (four graded observers with the observer and block exponents, the instrument group and training), so each
# pilot Job is one (world, test trajectory, part) and the bound is 20 h.
ROLES = {
    "probe": {"parts": {"core": "instrument,graded", "others": "others", "dthalf": "dthalf"}, "per_test": False, "timeout": "16h", "batch": "od-d8-probe"},
    "pilot": {"parts": {"core": "instrument,graded", "others": "others", "mu4": "murecord"}, "per_test": True, "timeout": "20h", "batch": "od-d8-pilot",
              "split_parts": {"inst": ("instrument", None), "read": ("graded", "READ"), "enstrophy": ("graded", "ENSTROPHY"), "ke": ("graded", "KE"), "ball": ("graded", "BALL")}},
    # The run (PREREG-D8-RUN-DRAFT.md Section 4): every Job is one (world, trajectory, arm), from the start. Measured on NRP in
    # the pilot at n = 128: one graded observer with both tangents 9.3 to 13.4 h, the six other observers together 7 to 17 h,
    # training 0.3 to 0.8 h, peak RSS 360 MiB. n = 192 is ESTIMATED at about 3.7 times n = 128 (n^2 log n per step, steps
    # proportional to n; not measured), and the run carries the observer tangent only, so a graded observer at n = 192 is
    # about 20 h or more whole and is split into ladder halves (halves_min_n); one other observer is about 4 to 10 h and runs
    # whole. Memory at n = 192 is estimated at about 0.8 GiB. MEASURED 2026-10-14 by the timing role (timing_n192_read_h0.json,
    # on k8s-haosu-11): the lower half of READ at n = 192 took 8.6 h (training 2.0 h, 7 rungs 6.6 h), peak RSS 760 MiB, so the
    # estimate above was high; an unsplit observer is about 14 h by equal cost per rung. The owner kept the halves
    # (2026-10-14, PREREG-D8-RUN-DRAFT.md Section 9, item 4).
    "run": {"parts": {}, "per_test": True, "per_arm": True, "timeout": "20h", "batch": "od-d8-run", "halves_min_n": 192, "nats": True,
            "split_parts": {"inst": ("instrument", None), "read": ("graded", "READ"), "enstrophy": ("graded", "ENSTROPHY"), "ke": ("graded", "KE"), "ball": ("graded", "BALL"),
                            "sens": ("others", "SENS"), **{f"random{j}": ("others", f"RANDOM{j}") for j in range(5)}}},
    # The timing measurement (PREREG-D8-RUN-DRAFT.md Section 9, owner 2026-10-14): one run-shaped Job at n = 192 on the timing
    # world's own seeds, submitted with --only for the lower half (7 of 13 rungs, the larger) of one graded observer; the role
    # carries the run's tangents (observer only), so its footprint is a run Job's
    "timing": {"parts": {}, "per_test": True, "per_arm": True, "timeout": "20h", "batch": "od-d8-timing", "halves_min_n": 192,
               "split_parts": {"read": ("graded", "READ")}},
}
# The smoke run (PREREG-D8-RUN-DRAFT.md Section 9, item 7): the run's Jobs exactly, on the smoke world (n = 64, its own seeds,
# K = 1), with halves_min_n lowered to 64 so that every graded observer goes through the ladder-half split and merge, and
# the run's NATS publish; the bound is lower since an n = 64 half is minutes per rung (test_ladder_split.py on Atlas)
ROLES["smoke"] = {**ROLES["run"], "timeout": "6h", "batch": "od-d8-smoke", "halves_min_n": 64}
# split_parts: a core part cut into five Jobs (the instrument group, then one graded observer each), submitted only when named
# with --only. Added 2026-10-11 after d8-pilot-p-nu020-n128-t0-core timed out at 20 h with READ alone finished; each
# graded observer at n = 128 takes about 4 h. Every Job repeats the deterministic training, so the pieces merge by index.
JOB_PARTS = ROLES["probe"]["parts"]  # kept for the probe rounds' collections and for importers
TIMEOUT = ROLES["probe"]["timeout"]
CPU, MEM, EPH = "1", "2Gi", "2Gi"
BEGIN, END = "----BEGIN d8 result gz-b64----", "----END d8 result----"
ARG_LIMIT = 120_000  # bytes per exec argument, under MAX_ARG_STRLEN (131072) with margin
HALVES = ("-h0", "-h1")  # a part name ending in one of these is that ladder half of the part


def nats_subject(track: str, role: str, name: str) -> str:
    """The OD_RESULTS subject of one Job's result: od.results.<track>.<role>.<Job name>."""
    return f"od.results.{track}.{role}.{name}"


def nats_lines(path: str, subject: str) -> list[str]:
    """Publish the result file, bounded; a failure is logged and never fails the Job, whose log block follows."""
    return [f"timeout {NATS_TIMEOUT} python -u /work/OD/D8/nats_results.py publish {path} {subject} || echo \"NATS-PUBLISH-EXIT $? {subject}\""]


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


def role_parts(role: str, world: str) -> list[str]:
    """The run's parts for one world and trajectory: the instrument and one per observer, each graded observer as two ladder
    halves (part + '-h0', '-h1') when the world's n is at least the role's halves_min_n."""
    R = ROLES[role]; n = next(int(w["n"]) for w in config()["worlds"] if w["name"] == world); out = []
    for p, (part, _) in R["split_parts"].items():
        out += [p + h for h in HALVES] if part == "graded" and n >= R.get("halves_min_n", 10 ** 9) else [p]
    return out


def units(role: str, split: bool, with_split_parts: bool = False) -> list[tuple[str, int | None, str | None]]:
    """(world, test trajectory or None, part or None) for every Job of the role; the split parts only on request, except in
    the run, whose Jobs are always the split parts (role_parts)."""
    R = ROLES[role]; K = int(config()["K_by_role"][role])
    tests = list(range(K)) if R["per_test"] else [None]
    if R.get("per_arm"):
        return [(w, t, p) for w in role_worlds(role) for t in tests for p in role_parts(role, w)]
    parts = list(R["parts"]) if (split or role != "probe") else [None]
    if with_split_parts: parts += list(R.get("split_parts", {}))
    return [(w, t, p) for w in role_worlds(role) for t in tests for p in parts]


def command(world: str, blobs: dict[str, tuple[str, str]], part: str | None = None, role: str = "probe", test: int | None = None) -> str:
    R = ROLES[role]
    tag = "_".join(x for x in (world, f"t{test}" if test is not None else "", part or "") if x)
    base, half = (part[:-3], int(part[-1])) if part and part.endswith(HALVES) else (part, None)
    if base in R.get("split_parts", {}):
        p, obs = R["split_parts"][base]; extra = f" --parts {p}" + (f" --observers {obs}" if obs else "")
    else:
        extra = f" --parts {R['parts'][base]}" if base else ""
    extra += f" --tests {test}" if test is not None else ""
    extra += f" --ladder-half {half}" if half is not None else ""
    lines = ["set -euo pipefail", "export PYTHONUNBUFFERED=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PIP_ROOT_USER_ACTION=ignore HOME=/work",
             "mkdir -p /work/OD/D5 /work/OD/D8"]
    for rel, (b64, sha) in blobs.items():
        lines += [f"echo '{b64}' | base64 -d | gunzip > /work/{rel}", f"echo '{sha}  /work/{rel}' | sha256sum -c - || exit 3"]
    pins = f"numpy=={NUMPY}" + (f" {NATS_PIN}" if R.get("nats") else "")
    lines += [f"pip install -q --no-cache-dir {pins} 2>&1 | tail -1 || true",
              "python -c \"import numpy, sys; print('numpy', numpy.__version__, 'python', sys.version.split()[0])\"",
              "cd /work/OD/D8", "python -u d8_sync.py --selftest",
              f"timeout {R['timeout']} python -u d8_sync.py --config prereg_config.json --seed-role {role} --world {world}{extra} --out {role}_{tag}.json"]
    if R.get("nats"): lines += nats_lines(f"{role}_{tag}.json", nats_subject("d8", role, job_name(world, part, role, test)))
    lines += [f"echo '{BEGIN}'", f"gzip -c {role}_{tag}.json | base64 -w0", "echo", f"echo '{END}'"]
    return "\n".join(lines) + "\n"


def descriptor(world: str, blobs, head: str, part: str | None = None, role: str = "probe", test: int | None = None) -> JobDescriptor:
    return JobDescriptor(name=job_name(world, part, role, test), image=IMAGE, command=["/bin/bash", "-c", command(world, blobs, part, role, test)],
                         env={"D8_WORLD": world, "D8_HEAD": head, "D8_PART": part or "all", "D8_ROLE": role, "D8_TEST": "all" if test is None else str(test)}
                         | ({"NATS_URL": NATS_URL} if ROLES[role].get("nats") else {}),
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
    if len(d.name) > 63: problems.append(f"name longer than 63 characters ({len(d.name)})")
    if ROLES[role].get("nats") and (f"timeout {NATS_TIMEOUT} python -u /work/OD/D8/nats_results.py publish" not in body or d.env.get("NATS_URL") != NATS_URL):
        problems.append("a nats role without a bounded publish or without NATS_URL")
    big = max(len(a.encode()) for a in d.command)
    if big > ARG_LIMIT: problems.append(f"command argument {big} bytes exceeds {ARG_LIMIT} (MAX_ARG_STRLEN is 131072)")
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


def submit(dry: bool, split: bool = False, role: str = "probe", only: list[str] | None = None) -> int:
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=HERE).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", *[str(p) for p in (FILES | NATS_FILES).values()]], capture_output=True, text=True, cwd=HERE).stdout.strip()
    if dirty: raise SystemExit(f"PREFLIGHT VETO: shipped files differ from HEAD {head}:\n{dirty}")
    if role not in ROLES: raise SystemExit(f"PREFLIGHT VETO: unknown role {role}")
    if role == "run" and not dry and subprocess.run(["git", "cat-file", "-e", "HEAD:experiments/OD/D8/PREREG-D8-RUN.md"], cwd=HERE, capture_output=True).returncode != 0:
        raise SystemExit("PREFLIGHT VETO: the run is submittable only once PREREG-D8-RUN.md is sealed in HEAD (a draft is not a registration); --dry-run works")
    blobs = {}
    for rel, p in (FILES | (NATS_FILES if ROLES[role].get("nats") else {})).items():
        raw = p.read_bytes(); blobs[rel] = (base64.b64encode(gzip.compress(raw, mtime=0)).decode(), hashlib.sha256(raw).hexdigest())
    us = units(role, split, with_split_parts=bool(only))
    if only:  # resubmit named Jobs only (e.g. a part whose result block was lost); every other Job is left alone
        us = [u for u in us if job_name(u[0], u[2], role, u[1]) in only]
        missing = set(only) - {job_name(w, p, role, t) for w, t, p in us}
        if missing: raise SystemExit(f"--only names not in role {role}: {sorted(missing)}")
    descs = [descriptor(w, blobs, head, p, role, t) for w, t, p in us]
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


def fetch_nats(subject: str) -> bytes | None:
    """The result a Job published to OD_RESULTS (nats_results.collect verifies the sha256 and length), or None."""
    import tempfile
    from nats_results import collect as nr_collect
    with tempfile.TemporaryDirectory() as d:
        r = asyncio.run(nr_collect(subject, str(Path(d) / "r.json")))
        return (Path(d) / "r.json").read_bytes() if r.get("ok") else None


def fetch(name: str, subject: str | None = None):
    """A Job's result from its log block; for a role that publishes (subject given), from the stream when the Job is gone,
    has no log, or has no result block."""
    st = kubectl("get", "job", name, "-o", "jsonpath={.status.succeeded}/{.status.failed}").stdout.strip()
    log = ""
    if st.startswith("1/"):  # never read logs of a Job that has not succeeded: a dead node makes kubectl logs hang
        log = kubectl("logs", f"job/{name}").stdout
        if BEGIN in log:
            blob = log.split(BEGIN, 1)[1].split(END, 1)[0].strip()
            return (json.loads(gzip.decompress(base64.b64decode(blob))), log.split(BEGIN, 1)[0]), st
    if subject:
        raw = fetch_nats(subject)
        if raw is not None:
            print(f"{name}: status {st or 'absent'}, result taken from {subject}")
            return (json.loads(raw), f"(log unavailable; result from NATS {subject})\n"), st or "absent"
    if st.startswith("1/"):
        print(f"{name}: status {st}, no result block; last lines:\n" + "\n".join(log.splitlines()[-8:]))
    else:
        print(f"{name}: status {st or 'absent'}, not collected")
    return None, st


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


def join_halves(pieces: dict) -> dict:
    """Ladder-half pieces (keys ending -h0 and -h1) -> one piece each, joined by d8_sync.merge_world_halves, which takes m*
    on the merged flags. A half without its partner is left out with a note: a half carries no m* and is never graded alone."""
    from d8_sync import merge_world_halves
    out = {k: v for k, v in pieces.items() if not k.endswith(HALVES)}
    for k in sorted(k for k in pieces if k.endswith(HALVES)):
        base = k[:-3]; lo, hi = pieces.get(base + HALVES[0]), pieces.get(base + HALVES[1])
        if lo is None or hi is None:
            print(f"{k}: its other ladder half is missing, not merged"); continue
        if k.endswith(HALVES[0]):
            out[base] = {**lo, "worlds": [merge_world_halves(lo["worlds"][0], hi["worlds"][0])], "footprint": {"h0": lo.get("footprint"), "h1": hi.get("footprint")}}
    return out


def collect(worlds: list[str] | None = None, tag: str = "", split: bool = False, role: str = "probe") -> int:
    merged = None
    R = ROLES[role]; K = int(config()["K_by_role"][role])
    for w in worlds or role_worlds(role):
        name = job_name(w, None, role)
        if split or role != "probe":
            pieces = {}; logs = []
            for t in (range(K) if R["per_test"] else [None]):
                for part in (role_parts(role, w) if R.get("per_arm") else [*R["parts"], *R.get("split_parts", {})]):
                    key = "_".join(x for x in (f"t{t}" if t is not None else "", part) if x)
                    if not R.get("per_arm") and part in R.get("split_parts", {}) and kubectl("get", "job", job_name(w, part, role, t), "-o", "name").returncode != 0: continue
                    jn = job_name(w, part, role, t); got, st = fetch(jn, nats_subject("d8", role, jn) if R.get("nats") else None)
                    if got: pieces[key] = got[0]; logs.append(f"===== {key}\n" + got[1])
            pieces = join_halves(pieces)
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
    if R.get("per_arm"):
        names = [job_name(w, p, role, t) for w, t, p in units(role, split) if worlds is None or w in worlds]
    else:
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
    cmd = command("p_nu020_n128", {}, "ball", "pilot", 0)
    ok = ok and "--parts graded --observers BALL --tests 0" in cmd and "--parts instrument --tests 0 " in command("p_nu020_n128", {}, "inst", "pilot", 0)
    ok = ok and "--observers" not in command("p_nu020_n128", {}, "core", "pilot", 0) and all(p not in ROLES["pilot"]["parts"] for p in ROLES["pilot"]["split_parts"])
    print("merge by trajectory index, job names, split-part commands:", "PASS" if ok else "FAIL", names)
    # the run role: K = 8, one Job per (world, trajectory, arm), n = 192 graded observers in ladder halves, unique short names
    cfg = config(); nw = {w["name"]: int(w["n"]) for w in cfg["worlds"]}; K = int(cfg["K_by_role"]["run"]); ru = units("run", False)
    per = {n: sum(1 for u in ru if nw[u[0]] == n) for n in (128, 192)}; rn = [job_name(w, p, "run", t) for w, t, p in ru]
    ok2 = K == 8 and per == {128: 2 * K * 11, 192: 2 * K * 15} and len(set(rn)) == len(rn) and max(map(len, rn)) <= 63
    ok2 = ok2 and int(cfg["random_draws"]) == sum(1 for p in ROLES["run"]["split_parts"] if p.startswith("random"))
    c192 = command("r_nu020_n192", {}, "read-h1", "run", 7); c128 = command("r_nu020_n128", {}, "read", "run", 7)
    ok2 = ok2 and "--seed-role run --world r_nu020_n192 --parts graded --observers READ --tests 7 --ladder-half 1 " in c192 and "--ladder-half" not in c128
    ok2 = ok2 and "--parts others --observers RANDOM4 --tests 0 " in command("r_nu030_n192", {}, "random4", "run", 0) and "sens-h0" not in role_parts("run", "r_nu030_n192")
    su = units("smoke", False); sn = [job_name(w, p, "smoke", t) for w, t, p in su]
    ok2 = ok2 and len(su) == 15 and sum(n.endswith(HALVES) for n in sn) == 8 and "--seed-role smoke --world s_nu030_n64 --parts graded --observers KE --tests 0 --ladder-half 0 " in command("s_nu030_n64", {}, "ke-h0", "smoke", 0)
    ok2 = ok2 and "od.results.d8.smoke.d8-smoke-s-nu030-n64-t0-ke-h0 " in command("s_nu030_n64", {}, "ke-h0", "smoke", 0) and "timeout 6h " in command("s_nu030_n64", {}, "inst", "smoke", 0)
    pub = "nats_results.py publish run_r_nu020_n192_t7_read-h1.json od.results.d8.run.d8-run-r-nu020-n192-t7-read-h1 || echo"
    ok2 = ok2 and pub in c192 and c192.index(pub) < c192.index(BEGIN) and NATS_PIN in c192 and "nats_results" not in command("p_nu020_n128", {}, "ball", "pilot", 0)
    print(f"run role: K = {K}, {len(ru)} Jobs ({per[128]} at n = 128, {per[192]} at n = 192), longest name {max(map(len, rn))}; smoke role {len(su)} Jobs; NATS publish:", "PASS" if ok2 else "FAIL")

    # join_halves: two constructed halves join into the whole ladder's record with m* taken on the merged flags; a lone half is left out
    def half(h, part, flags, rows):
        rec = {"ladder_half": h, "ladder_part": part, "synced": flags, "slope_hold": [0.0] * len(part), "delta_final": rows[-1], "delta_series": rows, "times": [0.0, 1.0],
               "initial_spreading_rate": [1.0] * len(part)}
        w = {"name": "x", "n": 192, "ladder": [4, 8, 16], "parts": ["graded"], "observers_run": ["READ"], "rankings": {"READ": [[1, 0]]}, "ladder_half": h, "seconds": 1.0,
             "tests": [{"index": 0, "spectrum_tail": 0.1, "observers": {"READ": rec}, "mu_record": {}, "dt_half": {}, "seconds": 1.0}]}
        return {"worlds": [w], "footprint": {"h": h}}
    lo = half(0, [4, 8], [False, True], [[1.0, 1.0], [1.0, 1e-5]]); hi = half(1, [16], [True], [[1.0], [1e-6]])
    j = join_halves({"t0_read-h0": lo, "t0_read-h1": hi, "t1_read-h0": lo}); r = j["t0_read"]["worlds"][0]["tests"][0]["observers"]["READ"]
    ok3 = sorted(j) == ["t0_read"] and r["m_star"] == 8 and r["synced"] == [False, True, True] and r["delta_series"] == [[1.0, 1.0, 1.0], [1.0, 1e-5, 1e-6]]
    print("join_halves: halves joined with m* on the merged flags, a lone half left out:", "PASS" if ok3 else "FAIL")
    return 0 if ok and ok2 and ok3 else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-have-checked-nrp-policy", action="store_true", dest="ack")
    ap.add_argument("--role", default="probe", choices=list(ROLES))
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--collect", action="store_true"); ap.add_argument("--cleanup", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--worlds", default=None, help="comma-separated world names for --collect/--cleanup (e.g. an earlier probe round)")
    ap.add_argument("--tag", default="", help="suffix for the merged file, <role><tag>.json")
    ap.add_argument("--split", action="store_true", help="probe only: three Jobs per world (core, others, dthalf); the pilot is always split per trajectory and part")
    ap.add_argument("--only", default=None, help="comma-separated Job names: submit only these")
    a = ap.parse_args(); ws = a.worlds.split(",") if a.worlds else None
    if a.selftest: return selftest()
    if a.collect: return collect(ws, a.tag, a.split, a.role)
    if a.cleanup: return cleanup(ws, a.split, a.role)
    if not a.ack and not a.dry_run:
        sys.exit("refusing without --i-have-checked-nrp-policy (read reference_nrp_job_policies first)")
    return submit(a.dry_run, a.split, a.role, a.only.split(",") if a.only else None)


if __name__ == "__main__":
    sys.exit(main())
