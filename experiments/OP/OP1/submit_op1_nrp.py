#!/usr/bin/env python3
"""Submit OP1's run to NRP via nats-bursting, one Job per world, and collect each world's result and trajectory file.
Runs ON ATLAS from the repository checkout (it needs the NATS hub and kubectl). PREREG-OP1-RUN-DRAFT.md Section 8.

Every Job runs `op1_edmd.py --read-ke` on one world: the run's rankings, READ-KE included, its lifts and its ladder. Two
files come back. The result JSON travels in the Job log between markers and over NATS into the hub's OD_RESULTS stream
(D8's nats_results.py, imported). The world's trajectory file (`traj/<world>_seed<seed>.npz`, which OP2 reads) travels
over NATS only, under its own subject: at about 10 MB it is too large for a container log, whose kubelet rotation
(10 MiB by default) would cut it. It is seed-deterministic, so a lost one can be simulated again.

The transport is D8's, imported and not copied: `publish` (status subscription opened before publishing), `created`
(fresh creationTimestamp after submit), `kubectl`, `fetch_nats` and `nats_lines`. The preflight is scored against the
PREFLIGHT of reference_nrp_job_policies line by line:
  * CPU-only (gpu = 0): numpy pseudo-spectral solver and ridge EDMD; no GPU rule can apply.
  * Exempt class: cpu = 1, memory = 2Gi, ephemeral-storage 2Gi declared, requests == limits (the renderer sets them
    equal). The utilization bands do not apply in this class. OMP_NUM_THREADS = 1.
  * Sized by a MEASUREMENT, never an estimate. The run role is vetoed unless the timing Job's collected record
    (`timing.json`, world t_nu030_n192, n = 192, the run's largest n) carries a measured footprint whose peak RSS times
    1.25 fits 2 GiB and whose wall time times 1.25 fits the run's timeout. The timing and smoke roles are the
    measurements themselves; their only risk in the exempt class is OOM, which their own footprint shows.
  * Self-terminating: the run is bounded by `timeout`; no sleep anywhere in the Job; backoff_limit = 0.
  * Self-contained: no PVC, no ConfigMap. The code and config ride in gzip + base64 with sha256 asserted; numpy is pinned
    to the version the self-tests passed on; op1_edmd.py's self-test runs in the pod first. No exec argument may exceed
    ARG_LIMIT.
  * Names checked absent before submit, creationTimestamp checked fresh after; logs read only from Jobs that
    succeeded; nothing saved is ever overwritten.
  * No deletes here except `--cleanup`, which refuses any Job that has not finished.

Usage (on Atlas, from experiments/OP/OP1):
  /home/claude/env/bin/python submit_op1_nrp.py --selftest
  /home/claude/env/bin/python submit_op1_nrp.py --role timing --dry-run
  /home/claude/env/bin/python submit_op1_nrp.py --role timing --i-have-checked-nrp-policy
  /home/claude/env/bin/python submit_op1_nrp.py --role timing --collect   # <role>_<world>.json, traj/, <role>.json
  /home/claude/env/bin/python submit_op1_nrp.py --role timing --cleanup   # finished Jobs only
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import datetime as dt
import gzip
import hashlib
import io
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from nats_bursting.descriptor import JobDescriptor, Resources

HERE = Path(__file__).resolve().parent
EXP = HERE.parents[1]
sys.path.insert(0, str(EXP / "OD" / "D8"))
from submit_d8_nrp import NATS_FILES, NATS_PIN, NATS_TIMEOUT, NATS_URL, created, fetch_nats, kubectl, nats_lines, nats_subject, publish  # noqa: E402

IMAGE = "python:3.12-slim"
PINS = "numpy==2.2.6"  # the version op1_edmd.py's self-test passed on at Atlas
FILES = {"OD/D5/d5_burgers.py": EXP / "OD" / "D5" / "d5_burgers.py", "OD/D8/d8_sync.py": EXP / "OD" / "D8" / "d8_sync.py",
         "OP/OP1/op1_edmd.py": HERE / "op1_edmd.py", "OP/OP1/prereg_config.json": HERE / "prereg_config.json"}
CFG = json.loads(FILES["OP/OP1/prereg_config.json"].read_text(encoding="utf-8"))
# Sizing. The pilot ran each world on one Atlas core in 3.5 to 5.2 h at n = 96 and 128 (pilot.json), 1.9 to 2.4 h of it the
# trajectories at n = 128; peak RSS 154 to 198 MiB in the probe and pilot footprints. Nothing at n = 192 is measured:
# the timing role measures it, and the run is vetoed until it has (measured_ok). The timeouts are bounds, not sizes.
ROLES = {"timing": {"timeout": "20h", "batch": "op1-timing"},
         "smoke": {"timeout": "6h", "batch": "op1-smoke"},
         "run": {"timeout": "20h", "batch": "op1-run", "needs_measurement": "timing"}}
CPU, MEM, EPH = "1", "2Gi", "2Gi"
MEM_MIB = 2048
MARGIN = 1.25  # request = measured peak x 1.25 (reference_nrp_job_policies); the same margin on wall time against the bound
BEGIN, END = "----BEGIN op1 result gz-b64----", "----END op1 result----"
ARG_LIMIT = 120_000  # bytes per exec argument, under MAX_ARG_STRLEN (131072) with margin


def role_worlds(role: str) -> list[str]:
    return [w["name"] for w in CFG["worlds"] if w["group"] in CFG["groups_by_role"][role]]


def seed(role: str) -> int:
    return int(CFG[f"seed_{role}"])


def job_name(world: str, role: str) -> str:
    return f"op1-{role}-" + world.replace("_", "-").lower()


def traj_name(world: str, role: str) -> str:
    return f"{world}_seed{seed(role)}.npz"  # op1_edmd.run_world's trajectory file name


def subjects(world: str, role: str) -> tuple[str, str]:
    """(result, trajectory) subjects in OD_RESULTS: od.results.op1.<role>.<Job> and od.results.op1traj.<role>.<Job>."""
    n = job_name(world, role); return nats_subject("op1", role, n), nats_subject("op1traj", role, n)


def seconds(bound: str) -> float:
    return float(bound[:-1]) * {"s": 1, "m": 60, "h": 3600}[bound[-1]]


def command(world: str, role: str, blobs: dict[str, tuple[str, str]]) -> str:
    R = ROLES[role]; out = f"{role}_{world}.json"; s_res, s_traj = subjects(world, role)
    lines = ["set -euo pipefail", "export PYTHONUNBUFFERED=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PIP_ROOT_USER_ACTION=ignore HOME=/work",
             "mkdir -p /work/OD/D5 /work/OD/D8 /work/OP/OP1/traj"]
    for rel, (b64, sha) in blobs.items():
        lines += [f"echo '{b64}' | base64 -d | gunzip > /work/{rel}", f"echo '{sha}  /work/{rel}' | sha256sum -c - || exit 3"]
    lines += [f"pip install -q --no-cache-dir {PINS} {NATS_PIN} 2>&1 | tail -1 || true",
              "python -c \"import numpy, sys; print('numpy', numpy.__version__, 'python', sys.version.split()[0])\"",
              "cd /work/OP/OP1", "python -u op1_edmd.py --selftest",
              f"timeout {R['timeout']} python -u op1_edmd.py --config prereg_config.json --seed-role {role} --world {world} --traj-dir traj --read-ke --out {out}"]
    lines += nats_lines(out, s_res) + nats_lines(f"traj/{traj_name(world, role)}", s_traj)
    lines += [f"echo '{BEGIN}'", f"gzip -c {out} | base64 -w0", "echo", f"echo '{END}'"]
    return "\n".join(lines) + "\n"


def descriptor(world: str, role: str, blobs, head: str) -> JobDescriptor:
    return JobDescriptor(name=job_name(world, role), image=IMAGE, command=["/bin/bash", "-c", command(world, role, blobs)],
                         env={"OP1_WORLD": world, "OP1_ROLE": role, "OP1_HEAD": head, "NATS_URL": NATS_URL},
                         resources=Resources(cpu=CPU, memory=MEM, gpu=0, ephemeral_storage=EPH),
                         labels={"atlas.io/batch": ROLES[role]["batch"], "atlas.io/role": role, "app": "op-op1"}, backoff_limit=0)


def measured_ok(rec: dict | None, timeout: str) -> list[str]:
    """Problems with a collected measurement record (<role>.json) as the size of a run Job; [] when it fits. Every world
    in it must carry a measured footprint (op1_edmd.footprint: peak_rss_mib, wall_seconds)."""
    if not rec or not rec.get("worlds"): return ["no measurement collected"]
    fp = rec.get("footprints") or {}; out = []
    for w in rec["worlds"]:
        f = fp.get(w["name"]) or {}
        if "peak_rss_mib" not in f or "wall_seconds" not in f: out.append(f"{w['name']}: no measured footprint"); continue
        if f["peak_rss_mib"] * MARGIN > MEM_MIB: out.append(f"{w['name']}: peak {f['peak_rss_mib']:.0f} MiB x {MARGIN} exceeds {MEM_MIB} MiB")
        if f["wall_seconds"] * MARGIN > seconds(timeout): out.append(f"{w['name']}: wall {f['wall_seconds'] / 3600:.1f} h x {MARGIN} exceeds the bound {timeout}")
    return out


def preflight(d: JobDescriptor, role: str) -> None:
    """The PREFLIGHT as code; the exempt class is the only class this submitter may use."""
    r = d.resources; problems = []
    if r.gpu != 0: problems.append("GPU requested for a CPU workload")
    if float(r.cpu) > 1: problems.append(f"cpu {r.cpu} outside the exempt class (<= 1)")
    if not r.memory.endswith("Gi") or float(r.memory[:-2]) > 2: problems.append(f"memory {r.memory} outside the exempt class (<= 2Gi)")
    if not r.ephemeral_storage: problems.append("ephemeral-storage not declared")
    body = " ".join(d.command)
    if "sleep" in body: problems.append("command contains sleep")
    if f"timeout {ROLES[role]['timeout']} python -u op1_edmd.py" not in body: problems.append("run not bounded by timeout")
    if d.backoff_limit != 0: problems.append("backoff_limit must be 0")
    if len(d.name) > 63: problems.append(f"name longer than 63 characters ({len(d.name)})")
    if body.count(f"timeout {NATS_TIMEOUT} python -u /work/OD/D8/nats_results.py publish") != 2 or d.env.get("NATS_URL") != NATS_URL:
        problems.append("the result and the trajectory need a bounded publish each, and NATS_URL")
    if "--read-ke" not in body: problems.append("the run's secondary arm READ-KE is not requested")
    big = max(len(a.encode()) for a in d.command)
    if big > ARG_LIMIT: problems.append(f"command argument {big} bytes exceeds {ARG_LIMIT} (MAX_ARG_STRLEN is 131072)")
    got = kubectl("get", "job", d.name, "-o", "name")
    if got.returncode == 0 and got.stdout.strip(): problems.append(f"Job {d.name} already exists (delete the finished one first)")
    if problems:
        raise SystemExit(f"PREFLIGHT VETO {d.name}: " + "; ".join(problems))


def submit(role: str, dry: bool) -> int:
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=HERE).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", *[str(p) for p in (FILES | NATS_FILES).values()]], capture_output=True, text=True, cwd=HERE).stdout.strip()
    if dirty: raise SystemExit(f"PREFLIGHT VETO: shipped files differ from HEAD {head}:\n{dirty}")
    R = ROLES[role]
    if role == "run" and not dry and subprocess.run(["git", "cat-file", "-e", "HEAD:experiments/OP/OP1/PREREG-OP1-RUN.md"], cwd=HERE, capture_output=True).returncode != 0:
        raise SystemExit("PREFLIGHT VETO: the run is submittable only once PREREG-OP1-RUN.md is sealed in HEAD (a draft is not a registration); --dry-run works")
    if R.get("needs_measurement"):
        p = HERE / f"{R['needs_measurement']}.json"; rec = json.loads(p.read_text(encoding="utf-8")) if p.exists() else None
        bad = measured_ok(rec, R["timeout"])
        if bad:
            if not dry: raise SystemExit(f"PREFLIGHT VETO: no measured size for the run ({p.name}): " + "; ".join(bad))
            print(f"DRY RUN WITHOUT A MEASURED SIZE (a submission would be vetoed): {'; '.join(bad)}")
    blobs = {}
    for rel, p in (FILES | NATS_FILES).items():
        raw = p.read_bytes(); blobs[rel] = (base64.b64encode(gzip.compress(raw, mtime=0)).decode(), hashlib.sha256(raw).hexdigest())
    descs = [descriptor(w, role, blobs, head) for w in role_worlds(role)]
    for d in descs: preflight(d, role)
    print(json.dumps({"head": head, "role": role, "seed": seed(role), "n_jobs": len(descs), "jobs": [d.name for d in descs], "sha256": {k: v[1] for k, v in blobs.items()},
                      "resources": {"cpu": CPU, "memory": MEM, "ephemeral_storage": EPH}, "timeout": R["timeout"], "pins": f"{PINS} {NATS_PIN}"}, indent=1))
    if dry:
        print(command(role_worlds(role)[0], role, {k: ("<b64>", s) for k, (_, s) in blobs.items()})); return 0
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


def check_traj(raw: bytes, world: str) -> str | None:
    """Why a trajectory file is unusable by OP2's --read-ke, or None: it must load and carry the run's arrays and S_ke."""
    import numpy as np
    try:
        z = np.load(io.BytesIO(raw))
        missing = [k for k in ("Xtr", "S", "S_at", "Xte", "keep", "meta", "S_ke") if k not in z.files]
        if missing: return f"{world}: trajectory file lacks {missing}"
        if z["S_ke"].shape != z["S"].shape: return f"{world}: S_ke {z['S_ke'].shape} differs from S {z['S'].shape}"
    except Exception as e:
        return f"{world}: trajectory file does not load ({e})"
    return None


def write_once(path: Path, raw: bytes) -> bool:
    if path.exists(): return False
    tmp = path.with_name(path.name + ".tmp"); tmp.write_bytes(raw); os.replace(tmp, path); return True


def collect(role: str) -> int:
    """Each finished world's result (log block, else the stream) -> <role>_<world>.json and .log, and its trajectory (the
    stream) -> traj/<world>_seed<seed>.npz, each written once and never overwritten; then <role>.json merges the saved
    worlds with their footprints, in the pilot's format."""
    (HERE / "traj").mkdir(exist_ok=True); merged = None
    for w in role_worlds(role):
        name = job_name(w, role); s_res, s_traj = subjects(w, role); res_path = HERE / f"{role}_{w}.json"
        st = kubectl("get", "job", name, "-o", "jsonpath={.status.succeeded}/{.status.failed}").stdout.strip()
        if not res_path.exists():
            raw, log = None, ""
            if st.startswith("1/"):  # never read logs of a Job that has not succeeded: a dead node makes kubectl logs hang
                log = kubectl("logs", f"job/{name}").stdout
                if BEGIN in log: raw = gzip.decompress(base64.b64decode(log.split(BEGIN, 1)[1].split(END, 1)[0].strip())); log = log.split(BEGIN, 1)[0]
            if raw is None and (st.startswith("1/") or not st):  # succeeded without a block, or the Job is gone
                raw = fetch_nats(s_res); log = f"(log unavailable; result from NATS {s_res})\n"
            if raw is None:
                print(f"{name}: status {st or 'absent'}, no result yet"); continue
            write_once(res_path, raw); (HERE / f"{role}_{w}.log").write_text(log, encoding="utf-8"); print(f"{name}: wrote {res_path.name}")
        tp = HERE / "traj" / traj_name(w, role)
        if not tp.exists():
            raw = fetch_nats(s_traj)
            why = "not in the stream" if raw is None else check_traj(raw, w)
            if why: print(f"{name}: TRAJECTORY NOT SAVED: {why}")
            else: write_once(tp, raw); print(f"{name}: wrote traj/{tp.name} ({len(raw)} bytes)")
        res = json.loads(res_path.read_text(encoding="utf-8"))
        if merged is None: merged = {k: v for k, v in res.items() if k not in ("worlds", "footprint")} | {"worlds": [], "footprints": {}}
        merged["worlds"] += res["worlds"]; merged["footprints"][w] = res.get("footprint")
    if merged:
        (HERE / f"{role}.json").write_text(json.dumps(merged, indent=1), encoding="utf-8"); print(f"merged {role}.json:", len(merged["worlds"]), "worlds")
    return 0


def cleanup(role: str) -> int:
    for w in role_worlds(role):
        name = job_name(w, role); got = kubectl("get", "job", name, "-o", "jsonpath={.status.succeeded}/{.status.failed}/{.status.active}")
        if got.returncode != 0: print(f"{name}: absent"); continue
        s, f, a = (got.stdout.strip().split("/") + ["", "", ""])[:3]
        if a not in ("", "0") or (s in ("", "0") and f in ("", "0")):
            print(f"{name}: NOT finished (succeeded={s} failed={f} active={a}); refusing to delete a running Job"); continue
        print(name, kubectl("delete", "job", name).stdout.strip())
    return 0


def selftest() -> int:
    """Roles, names, commands, the measurement guard and the trajectory check, on constructed inputs (no cluster call)."""
    import numpy as np
    fails = 0

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"{label}: {detail}", "PASS" if ok else "FAIL"); fails += 0 if ok else 1

    ws = {r: role_worlds(r) for r in ROLES}
    check("one Job per world: four run worlds, one timing world at n = 192, one smoke world",
          ws == {"timing": ["t_nu030_n192"], "smoke": ["s_nu030_n64"], "run": ["r_nu030_n128", "r_nu030_n192", "r_nu020_n128", "r_nu020_n192"]}, str(ws))
    seeds = {r: seed(r) for r in ("probe", "pilot", "run", "timing", "smoke")}
    check("each role has its own seed", len(set(seeds.values())) == len(seeds), str(seeds))
    names = [job_name(w, r) for r in ROLES for w in ws[r]]
    check("Job names unique and short", len(set(names)) == len(names) and max(map(len, names)) <= 63, f"longest {max(names, key=len)}")
    c = command("r_nu020_n192", "run", {}); s_res, s_traj = subjects("r_nu020_n192", "run")
    run_line = "timeout 20h python -u op1_edmd.py --config prereg_config.json --seed-role run --world r_nu020_n192 --traj-dir traj --read-ke --out run_r_nu020_n192.json"
    p_res = f"nats_results.py publish run_r_nu020_n192.json {s_res} ||"; p_traj = f"nats_results.py publish traj/r_nu020_n192_seed20261113.npz {s_traj} ||"
    check("run command: self-test first, then the bounded run with READ-KE, both publishes before the log block",
          c.index("op1_edmd.py --selftest") < c.index(run_line) < c.index(p_res) < c.index(p_traj) < c.index(BEGIN) and "sleep" not in c,
          f"{s_res} | {s_traj}")
    check("the two subjects never overlap in the stream (collect reads <subject>.*)", not s_traj.startswith(s_res + ".") and not s_res.startswith(s_traj + "."), "")
    fp = lambda rss, wall: {"worlds": [{"name": "t_nu030_n192"}], "footprints": {"t_nu030_n192": {"peak_rss_mib": rss, "wall_seconds": wall}}}
    cases = [measured_ok(None, "20h"), measured_ok({"worlds": [{"name": "t"}], "footprints": {}}, "20h"), measured_ok(fp(900, 11 * 3600), "20h"),
             measured_ok(fp(1700, 11 * 3600), "20h"), measured_ok(fp(900, 17 * 3600), "20h")]
    check("the run is sized only by a measurement: none, no footprint, fits, too much memory, too long",
          bool(cases[0]) and bool(cases[1]) and cases[2] == [] and "MiB" in cases[3][0] and "bound" in cases[4][0], str([len(x) for x in cases]))
    good = io.BytesIO(); a = np.zeros((3, 4)); np.savez_compressed(good, Xtr=a, S=a, S_at=np.arange(3), Xte=a, keep=np.arange(2), meta="{}", S_ke=a)
    bare = io.BytesIO(); np.savez_compressed(bare, Xtr=a, S=a, S_at=np.arange(3), Xte=a, keep=np.arange(2), meta="{}")
    check("a trajectory file is saved only with S_ke and loadable", check_traj(good.getvalue(), "w") is None and "S_ke" in check_traj(bare.getvalue(), "w")
          and "does not load" in check_traj(b"junk", "w"), "")
    check("timeouts parse and the run's bound is the timing role's", seconds("20h") == 72000 and seconds("6h") == 21600 and ROLES["run"]["timeout"] == ROLES["timing"]["timeout"], "")
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-have-checked-nrp-policy", action="store_true", dest="ack"); ap.add_argument("--role", default="timing", choices=list(ROLES))
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--collect", action="store_true"); ap.add_argument("--cleanup", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: return 1 if selftest() else 0
    if a.collect: return collect(a.role)
    if a.cleanup: return cleanup(a.role)
    if not a.ack and not a.dry_run:
        sys.exit("refusing without --i-have-checked-nrp-policy (read reference_nrp_job_policies first)")
    return submit(a.role, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
