#!/usr/bin/env python3
"""Submit the variants' nudging Jobs to NRP via nats-bursting, save each result as it lands, and collect them. Runs ON
ATLAS from the repository checkout (it needs the NATS hub and kubectl). SEALED-RUN-PLAN.md Sections 4 and 6.

Two stages. The ranking and Gramian parts (`op_variants.py --part rank|gram`) run first and cache each world's orderings
in `cache/`. Every nudging Job then carries its world's cached orderings inside it (gzip + base64 in one environment
variable per file, sha256 asserted), so no Job depends on another and none reads a shared volume. One Job per (variant,
world, test trajectory).

The transport is D8's, imported and not copied: `publish` (status subscription opened before publishing), `created`
(fresh creationTimestamp after submit) and `kubectl`. The preflight is scored against the PREFLIGHT of
reference_nrp_job_policies line by line:
  * CPU-only (gpu = 0). Exempt class: cpu = 1, memory = 2Gi, ephemeral-storage 2Gi declared; D8's footprint at n = 96
    is about 220 MiB on one core. OMP_NUM_THREADS = 1.
  * Self-terminating: bounded by `timeout`; no sleep anywhere in the Job; backoff_limit = 0.
  * Self-contained: the code, configs and cache ride in as environment variables (gzip + base64, one per file) with
    sha256 asserted, decoded and unset before anything runs; numpy is pinned to the version
    the self-tests passed on; the variants' self-test runs in the pod first.
  * Names checked absent before submit, creationTimestamp checked fresh after; logs read only from Jobs that
    succeeded; `--save` keeps each result block the moment its Job succeeds (three D8 pilot logs were lost when it
    did not), and never overwrites a saved piece. A role with "nats" also publishes its result file into the hub's
    OD_RESULTS stream through D8's nats_results.py before the log block, so a lost log does not lose the result.
  * No deletes here except `--cleanup`, which refuses any Job that has not finished.

Usage (on Atlas, from experiments/OP/VARIANTS):
  /home/claude/env/bin/python submit_variants_nrp.py --role probe --dry-run
  /home/claude/env/bin/python submit_variants_nrp.py --role probe --i-have-checked-nrp-policy
  /home/claude/env/bin/python submit_variants_nrp.py --role probe --save      # run on every watcher poll
  /home/claude/env/bin/python submit_variants_nrp.py --role probe --cleanup   # finished Jobs only
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import datetime as dt
import gzip
import hashlib
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
from submit_d8_nrp import NATS_FILES, NATS_PIN, NATS_TIMEOUT, NATS_URL, created, kubectl, nats_lines, nats_subject, publish  # noqa: E402

IMAGE = "python:3.12-slim"
PINS = "numpy==2.2.6"  # the version D8's and the variants' self-tests passed on at Atlas
FILES = {"OD/D5/d5_burgers.py": EXP / "OD" / "D5" / "d5_burgers.py", "OD/D8/d8_sync.py": EXP / "OD" / "D8" / "d8_sync.py",
         "OD/D8/prereg_config.json": EXP / "OD" / "D8" / "prereg_config.json", "OP/OP4/op4_gram.py": EXP / "OP" / "OP4" / "op4_gram.py",
         "OP/VARIANTS/op_variants.py": HERE / "op_variants.py", "OP/VARIANTS/variants_config.json": HERE / "variants_config.json"}
CFG8 = json.loads(FILES["OD/D8/prereg_config.json"].read_text(encoding="utf-8"))
WORLD_N = {w["name"]: int(w["n"]) for w in CFG8["worlds"]}
ROLES = {"probe": {"worlds": ["p_nu030_n96", "p_nu020_n96"], "seed_role": "pilot", "tests": [0, 1], "timeout": "16h", "batch": "op-var-probe"},
         # the run (PREREG-D8-RUN-DRAFT.md Sections 3 and 4): OP4's GRAM and the three secondary arms on the run worlds, K from
         # the config; every arm carries the observer tangent like a graded D8 observer, so at n = 192 it is split into ladder
         # halves (the same sizing as submit_d8_nrp.py's run role, measured there 2026-10-14: 8.6 h and 760 MiB for READ's lower
         # half at n = 192; the owner kept the halves, 2026-10-14); ESA was dropped
         # before the seal when its sample-count rule failed (PREREG-D8-RUN-DRAFT.md Section 3, owner 2026-10-14)
         "run": {"worlds": [w["name"] for w in CFG8["worlds"] if w["group"] in CFG8["groups_by_role"]["run"]], "seed_role": "run",
                 "tests": list(range(int(CFG8["K_by_role"]["run"]))), "timeout": "20h", "batch": "op-var-run",
                 "variants": ("GRAM", "READ_KE", "GRAM_UN", "SV"), "halves_min_n": 192, "nats": True}}
# the smoke run (PREREG-D8-RUN-DRAFT.md Section 9, item 7): the run's Jobs on the smoke world, split by halves at n = 64
ROLES["smoke"] = {**ROLES["run"], "worlds": [w["name"] for w in CFG8["worlds"] if w["group"] in CFG8["groups_by_role"]["smoke"]], "seed_role": "smoke",
                  "tests": list(range(int(CFG8["K_by_role"]["smoke"]))), "timeout": "6h", "batch": "op-var-smoke", "halves_min_n": 64}
VARIANTS = ("READ_KE", "ESA", "GRAM_UN", "SV")  # the probe's arms; a role may name its own
CPU, MEM, EPH = "1", "2Gi", "2Gi"
BEGIN, END = "----BEGIN opv result gz-b64----", "----END opv result----"
ARG_LIMIT = 120_000  # bytes per exec argument or environment string, under MAX_ARG_STRLEN (131072) with margin
# The files ship in environment variables, one per file, so each sits under ARG_LIMIT on its own (the n = 192 caches put
# 157536 bytes into one command argument, vetoed 2026-10-15). Two totals bound the Job as a whole, both measured on Atlas
# 2026-10-16: the burst.submit message under the hub's max_payload (1048576, from :8222/varz, nats-server 2.10.24), and the
# command plus environment under ARG_MAX (2097152 at the 8 MiB default stack, getconf ARG_MAX). The pod's own stack limit
# is not measured; the smoke run is the check.
TOTAL_LIMIT = 1_000_000
FILE_ENV = "OPV_FILE_"


def file_env(blobs: dict[str, tuple[str, str]]) -> dict[str, str]:
    """One environment variable per shipped file, in the order of `blobs`."""
    return {f"{FILE_ENV}{i}": b64 for i, (b64, _) in enumerate(blobs.values())}


def job_name(variant: str, world: str, role: str, test: int, half: int | None = None) -> str:
    return f"opv-{role}-{variant.replace('_', '-').lower()}-{world.replace('_', '-').lower()}-t{test}" + (f"-h{half}" if half is not None else "")


def units(role: str, variants=None) -> list[tuple[str, str, int, int | None]]:
    """(variant, world, test trajectory, ladder half or None) for every Job of the role; a world at or above the role's
    halves_min_n runs each (variant, trajectory) as two ladder halves."""
    R = ROLES[role]; allv = R.get("variants", VARIANTS); vs = allv if variants is None else [v for v in allv if v in variants]
    out = []
    for w in R["worlds"]:
        hs = (0, 1) if WORLD_N[w] >= R.get("halves_min_n", 10 ** 9) else (None,)
        out += [(v, w, t, h) for v in vs for t in R["tests"] for h in hs]
    return out


def cache_files(world: str, seed_role: str) -> dict[str, Path]:
    return {f"OP/VARIANTS/cache/{p}_{world}_{seed_role}.json": HERE / "cache" / f"{p}_{world}_{seed_role}.json" for p in ("rank", "gram")}


def command(variant: str, world: str, role: str, test: int, blobs: dict[str, tuple[str, str]], half: int | None = None) -> str:
    R = ROLES[role]; out = f"{role}_{variant}_{world}_t{test}" + (f"_h{half}" if half is not None else "") + ".json"
    lines = ["set -euo pipefail", "export PYTHONUNBUFFERED=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PIP_ROOT_USER_ACTION=ignore HOME=/work",
             "mkdir -p /work/OD/D5 /work/OD/D8 /work/OP/OP4 /work/OP/VARIANTS/cache"]
    for i, (rel, (_, sha)) in enumerate(blobs.items()):
        lines += [f"printf '%s' \"${FILE_ENV}{i}\" | base64 -d | gunzip > /work/{rel}", f"echo '{sha}  /work/{rel}' | sha256sum -c - || exit 3"]
    lines += ["unset " + " ".join(f"{FILE_ENV}{i}" for i in range(len(blobs)))]
    pins = PINS + (f" {NATS_PIN}" if R.get("nats") else "")
    lines += [f"pip install -q --no-cache-dir {pins} 2>&1 | tail -1 || true",
              "python -c \"import numpy, sys; print('numpy', numpy.__version__, 'python', sys.version.split()[0])\"",
              "cd /work/OP/VARIANTS", "python -u op_variants.py --selftest",
              f"timeout {R['timeout']} python -u op_variants.py --config ../../OD/D8/prereg_config.json --vcfg variants_config.json --seed-role {R['seed_role']} "
              f"--world {world} --part nudge --variant {variant} --tests {test} --cache cache --out {out}" + (f" --ladder-half {half}" if half is not None else "")]
    if R.get("nats"): lines += nats_lines(out, nats_subject("opv", role, job_name(variant, world, role, test, half)))
    lines += [f"echo '{BEGIN}'", f"gzip -c {out} | base64 -w0", "echo", f"echo '{END}'"]
    return "\n".join(lines) + "\n"


def descriptor(variant, world, role, test, blobs, head, half=None) -> JobDescriptor:
    return JobDescriptor(name=job_name(variant, world, role, test, half), image=IMAGE, command=["/bin/bash", "-c", command(variant, world, role, test, blobs, half)],
                         env={"OPV_VARIANT": variant, "OPV_WORLD": world, "OPV_ROLE": role, "OPV_TEST": str(test), "OPV_HALF": "all" if half is None else str(half), "OPV_HEAD": head}
                         | ({"NATS_URL": NATS_URL} if ROLES[role].get("nats") else {}) | file_env(blobs),
                         resources=Resources(cpu=CPU, memory=MEM, gpu=0, ephemeral_storage=EPH),
                         labels={"atlas.io/batch": ROLES[role]["batch"], "atlas.io/role": role, "app": "op-variants"}, backoff_limit=0)


def preflight(d: JobDescriptor, role: str) -> None:
    """The PREFLIGHT as code; the exempt class is the only class this submitter may use."""
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
    # Linux refuses any single exec argument over MAX_ARG_STRLEN (128 KiB): the first probe's 12 Jobs died at
    # "exec /bin/bash: argument list too long" with ~200 KB of uncompressed base64 in the command
    big = max(len(a.encode()) for a in d.command)
    if big > ARG_LIMIT: problems.append(f"command argument {big} bytes exceeds {ARG_LIMIT} (MAX_ARG_STRLEN is 131072)")
    env_big = max((len(f"{k}={v}".encode()), k) for k, v in d.env.items())
    if env_big[0] > ARG_LIMIT: problems.append(f"environment string {env_big[1]} {env_big[0]} bytes exceeds {ARG_LIMIT} (MAX_ARG_STRLEN is 131072)")
    total = sum(len(a.encode()) + 1 for a in d.command) + sum(len(f"{k}={v}".encode()) + 1 for k, v in d.env.items())
    if total > TOTAL_LIMIT: problems.append(f"command plus environment {total} bytes exceeds {TOTAL_LIMIT} (ARG_MAX 2097152 on Atlas)")
    msg = len(json.dumps({"job_id": f"{d.name}-00000000", "descriptor": d.to_dict()}).encode())  # the message publish() sends
    if msg > TOTAL_LIMIT: problems.append(f"burst.submit message {msg} bytes exceeds {TOTAL_LIMIT} (hub max_payload 1048576)")
    shipped = sorted(k for k in d.env if k.startswith(FILE_ENV)); cmd = d.command[-1]; cut = cmd.find("\nunset ")
    if shipped and (cut < 0 or any(f"\"${k}\" | base64 -d" not in cmd[:cut] for k in shipped)):
        problems.append("a shipped-file variable is not decoded before the unset")
    got = kubectl("get", "job", d.name, "-o", "name")
    if got.returncode == 0 and got.stdout.strip(): problems.append(f"Job {d.name} already exists (delete the finished one first)")
    if problems:
        raise SystemExit(f"PREFLIGHT VETO {d.name}: " + "; ".join(problems))


def build(role: str, dry: bool, variants=None):
    """The checks before any submission and the role's Jobs, each preflighted: (head, base blobs, cache sha256, descriptors).
    Used by submit() and by OD/D8/run_pool.py, so the pool sends exactly the Jobs this submitter would."""
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=HERE).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", *[str(p) for p in (FILES | NATS_FILES).values()]], capture_output=True, text=True, cwd=HERE).stdout.strip()
    if dirty: raise SystemExit(f"PREFLIGHT VETO: shipped files differ from HEAD {head}:\n{dirty}")
    if role == "run" and not dry and subprocess.run(["git", "cat-file", "-e", "HEAD:experiments/OD/D8/PREREG-D8-RUN.md"], cwd=HERE, capture_output=True).returncode != 0:
        raise SystemExit("PREFLIGHT VETO: the run is submittable only once PREREG-D8-RUN.md is sealed in HEAD (a draft is not a registration); --dry-run works")
    R = ROLES[role]; base = {}
    for rel, p in (FILES | (NATS_FILES if R.get("nats") else {})).items():
        raw = p.read_bytes(); base[rel] = (base64.b64encode(gzip.compress(raw, mtime=0)).decode(), hashlib.sha256(raw).hexdigest())
    descs = []; cache_sha = {}
    missing = set()
    for v, w, t, h in units(role, variants):
        blobs = dict(base)
        for rel, p in cache_files(w, R["seed_role"]).items():
            if not p.exists():
                if not dry: raise SystemExit(f"PREFLIGHT VETO: {p} missing; run op_variants.py --part rank and --part gram for {w} first")
                missing.add(p.name); continue
            raw = p.read_bytes(); blobs[rel] = (base64.b64encode(gzip.compress(raw, mtime=0)).decode(), hashlib.sha256(raw).hexdigest()); cache_sha[rel] = blobs[rel][1]
        descs.append(descriptor(v, w, role, t, blobs, head, h))
    if missing: print(f"DRY RUN WITHOUT CACHES (a submission would be vetoed): {sorted(missing)}")
    for d in descs: preflight(d, role)
    return head, base, cache_sha, descs


def submit(role: str, dry: bool, variants=None) -> int:
    head, base, cache_sha, descs = build(role, dry, variants); R = ROLES[role]
    print(json.dumps({"head": head, "role": role, "n_jobs": len(descs), "jobs": [d.name for d in descs], "sha256": {k: v[1] for k, v in base.items()} | cache_sha,
                      "resources": {"cpu": CPU, "memory": MEM, "ephemeral_storage": EPH}, "timeout": R["timeout"], "pins": PINS + (f" {NATS_PIN}" if R.get("nats") else "")}, indent=1))
    if dry:
        v, w, t, h = units(role, variants)[-1]; print(command(v, w, role, t, {k: ("<b64>", s) for k, (_, s) in base.items()}, h)); return 0
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


def save(role: str) -> int:
    """Save every succeeded Job's result block to pieces/<job>.json, once, atomically; never overwrite. For a role that
    publishes, a Job that succeeded without a readable result block is saved from the stream instead."""
    from submit_d8_nrp import fetch_nats
    out = HERE / "pieces"; out.mkdir(exist_ok=True)
    for v, w, t, h in units(role):
        name = job_name(v, w, role, t, h); path = out / f"{name}.json"
        if path.exists(): continue
        st = kubectl("get", "job", name, "-o", "jsonpath={.status.succeeded}/{.status.failed}").stdout.strip()
        raw, log = None, ""
        if st.startswith("1/"):  # never read logs of a Job that has not succeeded
            log = kubectl("logs", f"job/{name}").stdout
            if BEGIN in log: raw = gzip.decompress(base64.b64decode(log.split(BEGIN, 1)[1].split(END, 1)[0].strip())); log = log.split(BEGIN, 1)[0]
        if raw is None and ROLES[role].get("nats") and st.startswith("1/"):  # only finished Jobs: the saver runs on every poll
            raw = fetch_nats(nats_subject("opv", role, name)); log = f"(log unavailable; result from NATS {nats_subject('opv', role, name)})\n"
        if raw is None:
            if st.startswith("1/"): print(f"SAVE-UNAVAILABLE {name}")
            continue
        tmp = path.with_suffix(".tmp"); tmp.write_bytes(raw); os.replace(tmp, path)
        (out / f"{name}.log").write_text(log, encoding="utf-8"); print(f"SAVED {name} {len(raw)} bytes")
    return 0


def collect(role: str) -> int:
    """The saved pieces of the role -> <role>_variants.json: one record per (variant, world), test trajectories by index, the
    ladder halves joined by op_variants.merge_variant_halves (m* on the merged flags). A half without its partner is left out
    and reported; a half is never graded alone."""
    sys.path.insert(0, str(HERE)); from op_variants import merge_variant_halves
    pieces = HERE / "pieces"; res = {"role": role, "seed_role": ROLES[role]["seed_role"], "arms": {}, "missing": [], "footprints": {}}
    for v in ROLES[role].get("variants", VARIANTS):
        for w in ROLES[role]["worlds"]:
            tests = {}
            for t in ROLES[role]["tests"]:
                hs = [h for (v2, w2, t2, h) in units(role) if (v2, w2, t2) == (v, w, t)]
                got = {h: pieces / f"{job_name(v, w, role, t, h)}.json" for h in hs}
                if not all(p.exists() for p in got.values()):
                    res["missing"] += [p.stem for p in got.values() if not p.exists()]; continue
                parts = {h: json.loads(p.read_text(encoding="utf-8")) for h, p in got.items()}
                for h, p in got.items(): res["footprints"][p.stem] = parts[h].get("footprint")
                r = merge_variant_halves(parts[0], parts[1]) if hs == [0, 1] else parts[None]
                for x in r["tests"]: tests[x["index"]] = x
                ladder = r["ladder"]
            if tests: res["arms"].setdefault(v, {})[w] = {"ladder": ladder, "tests": [tests[i] for i in sorted(tests)]}
    out = HERE / f"{role}_variants.json"; out.write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps({"wrote": out.name, "arms": {v: {w: len(x["tests"]) for w, x in ws.items()} for v, ws in res["arms"].items()}, "missing": res["missing"]}))
    return 0


def cleanup(role: str) -> int:
    for v, w, t, h in units(role):
        name = job_name(v, w, role, t, h); got = kubectl("get", "job", name, "-o", "jsonpath={.status.succeeded}/{.status.failed}/{.status.active}")
        if got.returncode != 0: print(f"{name}: absent"); continue
        s, f, a = (got.stdout.strip().split("/") + ["", "", ""])[:3]
        if a not in ("", "0") or (s in ("", "0") and f in ("", "0")):
            print(f"{name}: NOT finished (succeeded={s} failed={f} active={a}); refusing to delete a running Job"); continue
        print(name, kubectl("delete", "job", name).stdout.strip())
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-have-checked-nrp-policy", action="store_true", dest="ack"); ap.add_argument("--role", default="probe", choices=list(ROLES))
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--save", action="store_true"); ap.add_argument("--cleanup", action="store_true")
    ap.add_argument("--collect", action="store_true", help="merge the saved pieces into <role>_variants.json")
    ap.add_argument("--variants", default=None, help="comma-separated subset of the variants to submit (all by default)")
    a = ap.parse_args()
    if a.save: return save(a.role)
    if a.collect: return collect(a.role)
    if a.cleanup: return cleanup(a.role)
    if not a.ack and not a.dry_run:
        sys.exit("refusing without --i-have-checked-nrp-policy (read reference_nrp_job_policies first)")
    return submit(a.role, a.dry_run, a.variants.split(",") if a.variants else None)


if __name__ == "__main__":
    sys.exit(main())
