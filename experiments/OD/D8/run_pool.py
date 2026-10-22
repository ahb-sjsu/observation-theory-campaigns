#!/usr/bin/env python3
"""The pool that runs the sealed D8 and OP4 run on NRP (PREREG-D8-RUN.md Sections 7 and 8). Runs ON ATLAS in a screen, from
experiments/OD/D8, with /home/claude/env/bin/python.

It sends exactly the Jobs the two submitters would (submit_d8_nrp.build and submit_variants_nrp.build, each preflighted), and
adds what 608 Jobs on a shared cluster need:
  * A cap: at most CAP Jobs of the run in flight (created and not finished) at once, 48 by the owner's word (2026-10-19).
    NRP has no fair queue, so the run never holds more than the cap. Submissions are spaced SPACING seconds apart.
  * Longest first: the n = 192 Jobs go out before the n = 128 ones, so the tail of the run is short.
  * Section 7: a Job that fails, or whose Job object vanishes, is recorded (attempts/<job>_attempt<k>.json) and, after its
    first attempt only, deleted (it has finished) and resubmitted once with the same seeds. After a second failure it is
    recorded and left; the collection reports its cell missing from that arm.
  * Every succeeded Job's result block is saved at once (pieces/<job>.json and .log, never overwritten), and its copy in
    OD_RESULTS is compared with it byte for byte; the variant Jobs' pieces go where submit_variants_nrp.py --collect reads them.
  * A brake: new submissions pause (state "paused", an ALERT line) when more than BRAKE Jobs fail within an hour, or when
    a submission does not show a fresh Job. Nothing is deleted while paused; the pool keeps saving results.
  * No Job is ever deleted except a failed one before its single resubmission; succeeded Jobs are left for --cleanup.
  * Each poll notes the node of every pod of the run (a NODE line when first seen), so a lost attempt's record names the
    node its pod last ran on even when the pod is gone by the time the loss is seen (the losses of 2026-10-20).
  * Nodes listed in exclude_nodes.json are kept out: every Job is sent with nats-bursting's exclude_nodes (a required
    NotIn node affinity on kubernetes.io/hostname), the file is reread before each send so a node can be added while
    the pool runs, and a Job created without the exclusion pauses the pool (a controller that ignores the field).
    The exclusion is scheduling only: the Job's command, image, resources and env are unchanged.
State is in run_pool_state.json, so a restarted pool adopts the Jobs already out and never resubmits a saved one. A restart
at a later HEAD is allowed only when no file the Jobs carry or are built from changed between the state's HEAD and this one
(`git diff`), and when the Jobs built now are the ones the state was written for (a fingerprint of every Job, its HEAD label
aside); the state keeps the launch HEAD and lists every HEAD the pool has run at.

  /home/claude/env/bin/python run_pool.py --selftest
  /home/claude/env/bin/python run_pool.py --dry-run          # builds and preflights all Jobs, submits nothing
  /home/claude/env/bin/python run_pool.py --i-have-checked-nrp-policy   # in a screen
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import datetime as dt
import gzip
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
VAR = HERE.parents[1] / "OP" / "VARIANTS"
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(VAR))

CAP = 48
SPACING = 20  # seconds between submissions, as in the submitters
TICK = 120  # seconds between polls of the cluster
BRAKE = 6  # failures within an hour that pause new submissions
STATE = HERE / "run_pool_state.json"; LOG = HERE / "run_pool.log"
PIECES_D8 = HERE / "pieces"; PIECES_VAR = VAR / "pieces"; ATTEMPTS = HERE / "attempts"
EXCLUDE = HERE / "exclude_nodes.json"  # {"exclude_nodes": [hostname, ...], "why": "..."}


def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def say(msg: str) -> None:
    line = f"{now().strftime('%Y-%m-%dT%H:%M:%SZ')} {msg}"; print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f: f.write(line + "\n")


def order_key(n: int, i: int) -> tuple[int, int]:
    """Longest first: larger n first, then the submitters' own order."""
    return (-n, i)


class Pool:
    """The scheduler. `cluster` returns {name: 'active' | 'succeeded' | 'failed'} for the run's Jobs that exist; `send`
    submits one Job and returns True when a fresh Job was seen, False when none was, or a reason (a str) when the Job was
    created but the pool must pause after it; `delete`, `save` and `record` act on one Job. All five are injected, so the
    self-test drives the same code on a fake cluster."""

    def __init__(self, jobs: list[str], cluster, send, delete, save, record, state: dict | None = None, cap: int = CAP, brake: int = BRAKE):
        self.jobs = jobs; self.cluster, self.send, self.delete, self.save, self.record = cluster, send, delete, save, record
        self.cap, self.brake = cap, brake
        s = state or {}
        self.attempts: dict[str, int] = s.get("attempts", {}); self.done: dict[str, str] = s.get("done", {})
        self.failures: list[str] = s.get("failures", []); self.paused: str | None = s.get("paused")
        self.sent_at: dict[str, str] = s.get("sent_at", {})

    def state(self) -> dict:
        return {"attempts": self.attempts, "done": self.done, "failures": self.failures, "paused": self.paused, "sent_at": self.sent_at}

    def tick(self, t: dt.datetime) -> list[str]:
        st = self.cluster(); events = []
        for name in self.jobs:
            if name in self.done or self.attempts.get(name, 0) == 0: continue  # done, never sent, or queued for its resubmission
            s = st.get(name)
            if s == "succeeded":
                ok = self.save(name)
                if ok: self.done[name] = "saved"; events.append(f"SAVED {name} (attempt {self.attempts[name]})")
                else: events.append(f"SAVE-PENDING {name}")
            elif s == "failed" or (s is None and t - dt.datetime.fromisoformat(self.sent_at.get(name, t.isoformat())) >= dt.timedelta(minutes=10)):
                why = "failed" if s == "failed" else "vanished"  # absent 10 min after sending, not a listing that lags a fresh Job
                self.record(name, self.attempts[name], why); self.failures.append(t.isoformat())
                if self.attempts[name] == 1:
                    if s == "failed": self.delete(name)
                    self.attempts[name] = 0  # back in the queue for its one resubmission
                    events.append(f"LOST {name} ({why}, attempt 1): recorded, queued for its one resubmission")
                else:
                    self.done[name] = f"missing after 2 attempts ({why})"
                    events.append(f"MISSING {name} ({why} at attempt 2): recorded, reported and not resubmitted")
        hour = (t - dt.timedelta(hours=1)).isoformat()
        recent = [x for x in self.failures if x >= hour]
        if len(recent) > self.brake and not self.paused:
            self.paused = f"{len(recent)} failures within an hour"; events.append(f"ALERT paused: {self.paused}")
        inflight = sum(1 for n in self.jobs if n not in self.done and self.attempts.get(n, 0) > 0)
        for name in self.jobs:
            if self.paused or inflight >= self.cap: break
            if name in self.done or self.attempts.get(name, 0) > 0: continue
            k = 2 if name in self.attempts and self.attempts[name] == 0 else 1
            r = self.send(name)
            if r:
                self.attempts[name] = k; self.sent_at[name] = t.isoformat(); inflight += 1; events.append(f"SUBMITTED {name} (attempt {k}, {inflight} in flight)")
                if isinstance(r, str): self.paused = r; events.append(f"ALERT paused: {self.paused}")  # sent, but stop after it
            else:
                self.paused = f"no fresh Job after submitting {name}"; events.append(f"ALERT paused: {self.paused}")
        if all(n in self.done for n in self.jobs): events.append("POOL DONE")
        return events


# ---------------------------------------------------------------- the cluster side (Atlas)

class names_absent:
    """While building at a restart, the submitters' preflight is told every run Job's name is absent: the Jobs already out
    are the ones being adopted, not sent. Every other check of the preflight runs as written, and send() runs the whole
    preflight, the name's absence included, against the real cluster before each Job is sent."""

    def __init__(self, on: bool):
        self.on = on

    def __enter__(self):
        import subprocess
        import submit_d8_nrp as S8
        import submit_variants_nrp as SV
        self.mods, self.real = (S8, SV), (S8.kubectl, SV.kubectl)
        if self.on:
            def kc(*args):
                if len(args) == 5 and args[:2] == ("get", "job") and args[3:] == ("-o", "name"):  # the preflight's name check
                    return subprocess.CompletedProcess(args, 1, "", "adopting at a restart: the name check runs at send time")
                return self.real[0](*args)
            S8.kubectl = SV.kubectl = kc
        return self

    def __exit__(self, *exc):
        self.mods[0].kubectl, self.mods[1].kubectl = self.real
        return False


def build_all(dry: bool, adopting: bool = False):
    import submit_d8_nrp as S8
    import submit_variants_nrp as SV
    with names_absent(adopting):
        h8, _, us8, d8 = S8.build(dry, False, "run")
        hv, _, _, dv = SV.build("run", dry)
    if h8 != hv: raise SystemExit(f"the two submitters see different HEADs: {h8} {hv}")
    n_of = {w["name"]: int(w["n"]) for w in S8.config()["worlds"]}
    items = [(d, "d8", n_of[d.env["D8_WORLD"]]) for d in d8] + [(d, "opv", n_of[d.env["OPV_WORLD"]]) for d in dv]
    items = [x for _, x in sorted(enumerate(items), key=lambda p: order_key(p[1][2], p[0]))]
    return h8, {d.name: (d, kind) for d, kind, _ in items}, [d.name for d, _, _ in items]


def built_from() -> list[Path]:
    """Every file a run Job carries or is built from: both submitters' shipped files, the variant caches of the run worlds,
    and the two submitters themselves (they write the command, resources and env)."""
    import submit_d8_nrp as S8
    import submit_variants_nrp as SV
    ps = {*S8.FILES.values(), *S8.NATS_FILES.values(), *SV.FILES.values(), Path(S8.__file__), Path(SV.__file__)}
    for w in SV.ROLES["run"]["worlds"]: ps |= set(SV.cache_files(w, SV.ROLES["run"]["seed_role"]).values())
    return sorted(Path(p).resolve() for p in ps)


def git_changed(old: str, new: str, paths: list[Path]) -> list[str] | None:
    """The files among `paths` that differ between commits old and new, or None when git cannot tell."""
    import subprocess
    got = subprocess.run(["git", "diff", "--name-only", old, new, "--", *map(str, paths)], capture_output=True, text=True, cwd=HERE)
    return None if got.returncode != 0 else [x for x in got.stdout.splitlines() if x.strip()]


def restart_problem(state_head: str, head: str, paths: list[Path], changed=git_changed) -> str | None:
    """Why a pool whose state was written at state_head must not restart at head, or None when it may."""
    if state_head == head: return None
    got = changed(state_head, head, paths)
    if got is None: return f"git cannot compare {state_head} with {head}"
    if got: return f"files the Jobs carry or are built from changed between {state_head} and {head}: {got}"
    return None


def fingerprint(descs: dict) -> str:
    """sha256 over every Job as it would be sent, its HEAD label left out (D8_HEAD, OPV_HEAD name the commit, not the Job)."""
    import dataclasses
    import hashlib
    rows = []
    for name in sorted(descs):
        d = dataclasses.asdict(descs[name][0]); d["env"] = {k: v for k, v in d["env"].items() if not k.endswith("_HEAD")}
        rows.append(d)
    return hashlib.sha256(json.dumps(rows, sort_keys=True, default=str).encode()).hexdigest()


def kubectl(*args: str, timeout: int = 120):
    """kubectl in the namespace, bounded: a Job's log on a dead node can hang an unbounded call. A timeout comes back as a
    failed call (returncode 124), never as an empty success."""
    import subprocess
    import submit_d8_nrp as S8
    try:
        return subprocess.run(["kubectl", "-n", S8.NS, *args], capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(args, 124, "", f"kubectl {' '.join(args[:2])} timed out after {timeout} s")


def excluded_nodes(path: Path | None = None) -> list[str]:
    """The nodes to keep the run's pods off, reread before each send. No file means no exclusion; a malformed file is an
    error (RuntimeError, which the loop reports as a WARN and retries), never a silent empty list."""
    p = path or EXCLUDE
    if not p.exists(): return []
    try:
        got = json.loads(p.read_text(encoding="utf-8"))["exclude_nodes"]
    except (ValueError, KeyError, TypeError) as e:
        raise RuntimeError(f"{p.name} is malformed ({e}); nothing sent") from None
    if not isinstance(got, list) or not all(isinstance(x, str) and x.strip() for x in got):
        raise RuntimeError(f"{p.name}: exclude_nodes must be a list of non-empty hostnames; nothing sent")
    return sorted({x.strip() for x in got})


class Excluding:
    """A submitter's JobDescriptor sent with exclude_nodes added to its payload. The nats-bursting client on Atlas predates
    the field, so it is added to the dict the submitters publish; everything else is the descriptor as built."""

    def __init__(self, d, nodes: list[str]):
        self._d, self._nodes = d, list(nodes)

    def __getattr__(self, k):
        return getattr(self._d, k)

    def to_dict(self) -> dict:
        x = self._d.to_dict()
        if self._nodes: x["exclude_nodes"] = list(self._nodes)
        return x


AFFINITY = "jsonpath={.spec.template.spec.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[*].matchExpressions[?(@.key=='kubernetes.io/hostname')].values[*]}"


def make_cluster(descs: dict, kc=None, note=None, attempts_dir: Path | None = None, exclude_path: Path | None = None):
    import submit_d8_nrp as S8
    import submit_variants_nrp as SV
    kubectl_ = kc or kubectl; note = note or say; attempts = attempts_dir or ATTEMPTS
    seen: dict[str, dict] = {}  # Job name -> the pod of its current attempt last seen: pod, node, phase, time

    def cluster() -> dict:
        got = kubectl_("get", "jobs", "-o", "json")
        if got.returncode != 0: raise RuntimeError(f"kubectl get jobs failed: {got.stderr.strip()[:200]}")
        out = {}
        for j in json.loads(got.stdout)["items"]:
            n = j["metadata"]["name"]
            if n not in descs: continue
            s = j.get("status", {})
            out[n] = "succeeded" if s.get("succeeded") else "failed" if s.get("failed") else "active"
        pods = kubectl_("get", "pods", "-l", "job-name", "-o", "json")
        if pods.returncode != 0: note(f"WARN kubectl get pods failed, nodes not noted this poll: {pods.stderr.strip()[:200]}")
        else:
            for pod in json.loads(pods.stdout).get("items", []):
                n = pod["metadata"].get("labels", {}).get("job-name"); node = pod.get("spec", {}).get("nodeName")
                if n not in out or out[n] != "active" or not node: continue  # only pods of the run's Jobs in flight
                p = pod["metadata"]["name"]
                if seen.get(n, {}).get("pod") != p or seen[n].get("node") != node: note(f"NODE {n} pod {p} on {node}")
                seen[n] = {"pod": p, "node": node, "phase": pod.get("status", {}).get("phase"), "seen": now().isoformat()}
        return out

    def send(name: str):
        d, kind = descs[name]; M = S8 if kind == "d8" else SV
        ex = excluded_nodes(exclude_path)  # reread each time; a malformed file raises before anything is sent
        M.preflight(d, "run")  # the name is absent and the Job is the sealed shape, checked again at send time
        t_sub = now() - dt.timedelta(seconds=5); ev = asyncio.run(M.publish(Excluding(d, ex))); c = None
        for _ in range(12):
            c = M.created(name)
            if c: break
            time.sleep(5)  # the pool on Atlas waiting for the controller, not a Job
        rendered = None
        if c is not None and ex:
            got = kubectl_("get", "job", name, "-o", AFFINITY)
            rendered = sorted(got.stdout.split()) if got.returncode == 0 else None
        note(json.dumps({"job": name, "status_events": ev, "creationTimestamp": c.isoformat() if c else None,
                         "exclude_nodes": ex, "exclusion_on_job": rendered}))
        time.sleep(SPACING)
        if c is None or c < t_sub: return False
        if ex and rendered != ex:
            return f"{name} was created without its node exclusion (on the Job: {rendered}); the controller may predate exclude_nodes"
        return True

    def delete(name: str) -> None:
        got = kubectl_("get", "job", name, "-o", "jsonpath={.status.succeeded}/{.status.failed}/{.status.active}")
        s, f, a = (got.stdout.strip().split("/") + ["", "", ""])[:3]
        if got.returncode != 0 or a not in ("", "0") or f in ("", "0"):
            raise SystemExit(f"{name}: not a failed, finished Job (succeeded={s} failed={f} active={a}); refusing to delete")
        say(f"DELETE {name}: " + kubectl_("delete", "job", name, "--wait=true", timeout=300).stdout.strip())
        if kubectl_("get", "job", name, "-o", "name").returncode == 0: raise SystemExit(f"{name}: still present after delete; its name cannot be reused yet")

    def save(name: str) -> bool:
        d, kind = descs[name]; out = PIECES_D8 if kind == "d8" else PIECES_VAR; out.mkdir(exist_ok=True)
        path = out / f"{name}.json"
        if path.exists(): return True
        got = kubectl_("logs", f"job/{name}"); log = got.stdout if got.returncode == 0 else ""; raw = None
        begin, end = (S8.BEGIN, S8.END) if kind == "d8" else (SV.BEGIN, SV.END)
        if begin in log: raw = gzip.decompress(base64.b64decode(log.split(begin, 1)[1].split(end, 1)[0].strip()))
        subject = S8.nats_subject(kind, "run", name); streamed = S8.fetch_nats(subject)
        if raw is None and streamed is None: return False
        same = "no log copy" if raw is None else "no stream copy" if streamed is None else ("SAME" if raw == streamed else "DIFFERENT")
        body = raw if raw is not None else streamed
        tmp = path.with_suffix(".tmp"); tmp.write_bytes(body); os.replace(tmp, path)
        (out / f"{name}.log").write_text(log.split(begin, 1)[0] if begin in log else f"(log unavailable; result from NATS {subject})\n", encoding="utf-8")
        if same != "SAME": say(f"ALERT {name}: log and stream copies {same}")
        return True

    def record(name: str, attempt: int, why: str) -> None:
        attempts.mkdir(exist_ok=True); p = attempts / f"{name}_attempt{attempt}.json"
        got = kubectl_("get", "job", name, "-o", "json")
        ev = kubectl_("get", "events", "--field-selector", f"involvedObject.name={name}", "-o", "json")
        pods = kubectl_("get", "pods", "-l", f"job-name={name}", "-o", "json")
        pev = []
        if pods.returncode == 0:
            for pod in json.loads(pods.stdout).get("items", []):
                e = kubectl_("get", "events", "--field-selector", f"involvedObject.name={pod['metadata']['name']}", "-o", "json")
                if e.returncode == 0: pev += [{"reason": x.get("reason"), "message": x.get("message"), "last": x.get("lastTimestamp")} for x in json.loads(e.stdout).get("items", [])]
        rec = {"job": name, "attempt": attempt, "why": why, "recorded": now().isoformat(),
               "status": json.loads(got.stdout).get("status") if got.returncode == 0 else None,
               "job_events": [{"reason": x.get("reason"), "message": x.get("message"), "last": x.get("lastTimestamp")} for x in json.loads(ev.stdout).get("items", [])] if ev.returncode == 0 else [],
               "pod_events": pev, "pod_last_seen": seen.pop(name, None)}  # popped: the next attempt's pod is noted afresh
        if not p.exists(): p.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")

    return cluster, send, delete, save, record


def run(ack: bool) -> int:
    if not ack: sys.exit("refusing without --i-have-checked-nrp-policy (read reference_nrp_job_policies first)")
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    head, descs, jobs = build_all(False, adopting=bool(state))
    launch = state.get("head", head); heads = state.get("heads", [launch]); fp = fingerprint(descs)
    why = restart_problem(heads[-1], head, built_from())
    if why: raise SystemExit(f"state was written at {heads[-1]}, HEAD is {head}, and {why}: stop and look")
    if state.get("fingerprint", fp) != fp: raise SystemExit(f"the Jobs built at {head} are not the ones the state was written for: stop and look")
    if head not in heads: heads.append(head)
    pool = Pool(jobs, *make_cluster(descs), state=state)
    say(f"POOL START head {head} (launched at {launch}), {len(jobs)} Jobs, cap {CAP}, {sum(1 for n in jobs if n in pool.done)} already done"
        + (f", paused: {pool.paused}" if pool.paused else ""))
    while True:
        try:
            events = pool.tick(now())
        except RuntimeError as e:
            events = [f"WARN {e}"]
        for e in events: say(e)
        tmp = STATE.with_suffix(".tmp"); tmp.write_text(json.dumps({"head": launch, "heads": heads, "fingerprint": fp, **pool.state()}, indent=1), encoding="utf-8"); os.replace(tmp, STATE)
        if "POOL DONE" in events: return 0
        time.sleep(TICK)  # the pool's poll interval on Atlas, not a Job


def dry() -> int:
    head, descs, jobs = build_all(True)
    from collections import Counter
    print(json.dumps({"head": head, "n_jobs": len(jobs), "by_kind": Counter(k for _, k in descs.values()), "cap": CAP,
                      "first": jobs[:3], "last": jobs[-3:]}, indent=1))
    return 0


# ---------------------------------------------------------------- self-test on a fake cluster

def selftest() -> int:
    fails = 0

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"{label}: {detail}", "PASS" if ok else "FAIL"); fails += 0 if ok else 1

    def fake(jobs, script):
        """script: {name: [outcome of attempt 1, outcome of attempt 2]}, outcomes 'ok', 'fail', 'vanish'."""
        cl = {}; att = {n: 0 for n in jobs}; log = {"sent": [], "deleted": [], "saved": [], "recorded": []}

        def cluster():
            return dict(cl)

        def send(n):
            if n in cl: raise SystemExit(f"sent {n} while its Job exists")
            att[n] += 1; log["sent"].append(n); cl[n] = "active"; return True

        def delete(n):
            if cl.get(n) != "failed": raise SystemExit(f"deleted {n} in state {cl.get(n)}")
            log["deleted"].append(n); del cl[n]

        def save(n):
            log["saved"].append(n); return True

        def record(n, k, why):
            log["recorded"].append((n, k, why))

        def finish():
            for n, s in list(cl.items()):
                if s != "active": continue
                o = script.get(n, ["ok", "ok"])[att[n] - 1]
                if o == "ok": cl[n] = "succeeded"
                elif o == "fail": cl[n] = "failed"
                else: del cl[n]
        return cluster, send, delete, save, record, finish, log, cl

    jobs = [f"j{i}" for i in range(10)]
    cluster, send, delete, save, record, finish, log, cl = fake(jobs, {"j1": ["fail", "ok"], "j2": ["vanish", "fail"], "j3": ["fail", "vanish"]})
    p = Pool(jobs, cluster, send, delete, save, record, cap=3, brake=100); t = dt.datetime(2026, 10, 19, tzinfo=dt.timezone.utc); peak = 0
    for i in range(40):
        ev = p.tick(t + dt.timedelta(minutes=2 * i)); peak = max(peak, sum(1 for s in cl.values() if s == "active"))
        if "POOL DONE" in ev: break
        finish()
    check("the cap holds: never more than 3 Jobs in flight", peak <= 3, f"peak {peak}")
    check("every Job ends saved or missing", all(n in p.done for n in jobs), str(p.done))
    check("a Job failing once is resubmitted once and saved", log["sent"].count("j1") == 2 and p.done["j1"] == "saved", "")
    check("failing twice: two attempts, reported missing, never a third", log["sent"].count("j2") == 2 and log["sent"].count("j3") == 2 and p.done["j2"].startswith("missing") and p.done["j3"].startswith("missing"), "")
    check("only failed Jobs are deleted, and only before their one resubmission", sorted(log["deleted"]) == ["j1", "j3"], str(log["deleted"]))
    check("every lost attempt is recorded", sorted(log["recorded"]) == [("j1", 1, "failed"), ("j2", 1, "vanished"), ("j2", 2, "failed"), ("j3", 1, "failed"), ("j3", 2, "vanished")], str(sorted(log["recorded"])))
    check("every succeeded Job is saved, and none is deleted (the fake refuses to delete any Job not failed)",
          set(log["saved"]) == {n for n in jobs if p.done[n] == "saved"} and len(log["saved"]) == len(set(log["saved"])), "")
    st = p.state(); cluster2, send2, *_rest = fake(jobs, {})
    p2 = Pool(jobs, lambda: {}, lambda n: (_ for _ in ()).throw(SystemExit("resubmitted a finished Job")), delete, save, record, state=json.loads(json.dumps(st)))
    check("a restarted pool resubmits nothing that is done", "POOL DONE" in p2.tick(t), "")
    jobs = [f"k{i}" for i in range(12)]
    cluster, send, delete, save, record, finish, log, cl = fake(jobs, {n: ["fail", "fail"] for n in jobs})
    p = Pool(jobs, cluster, send, delete, save, record, cap=12, brake=6)
    for i in range(6):
        p.tick(t + dt.timedelta(minutes=i)); finish()
    check("the brake pauses new submissions after more than 6 failures within an hour", p.paused is not None and len(log["sent"]) < 24, f"{p.paused}, {len(log['sent'])} sent")
    cluster, send, delete, save, record, finish, log, cl = fake(["a", "b"], {})
    p = Pool(["a", "b"], cluster, lambda n: False, delete, save, record)
    ev = p.tick(t)
    check("a submission without a fresh Job pauses the pool", p.paused is not None and any("ALERT" in e for e in ev), str(ev))
    cluster, send, delete, save, record, finish, log, cl = fake(["x"], {})
    p = Pool(["x"], lambda: {}, send, delete, save, record)
    p.tick(t); p.tick(t + dt.timedelta(minutes=2))
    check("a Job missing from a lagging listing just after its send is not counted lost", not log["recorded"] and p.attempts["x"] == 1 and log["sent"] == ["x"], str(log["recorded"]))
    cl.clear(); p.tick(t + dt.timedelta(minutes=12))
    check("and it is counted lost once it has been absent 10 minutes, then sent once more", log["recorded"] == [("x", 1, "vanished")] and log["sent"] == ["x", "x"], str(log["recorded"]))
    check("longest first: n = 192 before n = 128, the submitters' order kept within", sorted([(128, 0), (192, 1), (128, 2), (192, 3)], key=lambda x: order_key(*x)) == [(192, 1), (192, 3), (128, 0), (128, 2)], "")
    # the restart check and the fingerprint
    ps = [Path("a.py")]
    check("a restart at the same HEAD is allowed without asking git", restart_problem("h1", "h1", ps, changed=lambda *a: (_ for _ in ()).throw(SystemExit("asked git"))) is None, "")
    check("a restart at a later HEAD with no built-from file changed is allowed", restart_problem("h1", "h2", ps, changed=lambda *a: []) is None, "")
    check("and refused when one changed, or when git cannot tell", restart_problem("h1", "h2", ps, changed=lambda *a: ["OD/D8/d8_sync.py"]) is not None
          and restart_problem("h1", "h2", ps, changed=lambda *a: None) is not None, "")
    import dataclasses

    @dataclasses.dataclass
    class D:
        name: str; command: list; env: dict
    f0 = fingerprint({"a": (D("a", ["x"], {"D8_WORLD": "w", "D8_HEAD": "h1"}), "d8")})
    check("the fingerprint ignores the HEAD label", f0 == fingerprint({"a": (D("a", ["x"], {"D8_WORLD": "w", "D8_HEAD": "h2"}), "d8")}), "")
    check("and catches a changed command or env", f0 != fingerprint({"a": (D("a", ["y"], {"D8_WORLD": "w", "D8_HEAD": "h1"}), "d8")})
          and f0 != fingerprint({"a": (D("a", ["x"], {"D8_WORLD": "v", "D8_HEAD": "h1"}), "d8")}), "")
    # the node noted while the pod lives reaches the record of a loss seen after the pod is gone
    import subprocess
    import tempfile
    world = {"jobs": [{"metadata": {"name": "j"}, "status": {"active": 1}}],
             "pods": [{"metadata": {"name": "j-abc", "labels": {"job-name": "j"}}, "spec": {"nodeName": "node-7"}, "status": {"phase": "Running"}},
                      {"metadata": {"name": "z-1", "labels": {"job-name": "other"}}, "spec": {"nodeName": "node-9"}, "status": {"phase": "Running"}}]}

    def kc(*args, timeout=120):
        if args[:2] == ("get", "jobs"): return subprocess.CompletedProcess(args, 0, json.dumps({"items": world["jobs"]}), "")
        if args[:2] == ("get", "pods") and args[3] == "job-name": return subprocess.CompletedProcess(args, 0, json.dumps({"items": world["pods"]}), "")
        if args[:2] == ("get", "pods"): return subprocess.CompletedProcess(args, 0, json.dumps({"items": []}), "")
        return subprocess.CompletedProcess(args, 1, "", "NotFound")
    notes = []
    with tempfile.TemporaryDirectory() as td:
        cl, _s, _d, _sv, rec = make_cluster({"j": (None, "d8")}, kc=kc, note=notes.append, attempts_dir=Path(td))
        st1 = cl(); cl()
        world["jobs"], world["pods"] = [], []  # the Job and its pod gone, as on 2026-10-20
        rec("j", 1, "vanished"); r = json.loads((Path(td) / "j_attempt1.json").read_text(encoding="utf-8"))
        rec("j", 2, "vanished"); r2 = json.loads((Path(td) / "j_attempt2.json").read_text(encoding="utf-8"))
    check("a running pod's node is noted once, and only for the run's Jobs", st1 == {"j": "active"} and notes == ["NODE j pod j-abc on node-7"], str(notes))
    check("a lost attempt's record names the node its pod last ran on", (r.get("pod_last_seen") or {}).get("node") == "node-7", str(r.get("pod_last_seen")))
    check("and the next attempt's record does not inherit it", r2.get("pod_last_seen") is None, str(r2.get("pod_last_seen")))
    # building at a restart: only the preflight's name check is answered "absent", and only inside the block
    import submit_d8_nrp as S8
    import submit_variants_nrp as SV
    orig = (S8.kubectl, SV.kubectl); calls = []
    S8.kubectl = SV.kubectl = lambda *a: (calls.append(a), subprocess.CompletedProcess(a, 0, "job.batch/x\n", ""))[1]
    try:
        stub = S8.kubectl
        with names_absent(True):
            gone = S8.kubectl("get", "job", "x", "-o", "name").returncode == 1 and SV.kubectl("get", "job", "y", "-o", "name").returncode == 1
            S8.kubectl("get", "job", "x", "-o", "json")
        with names_absent(False):
            kept = S8.kubectl is stub
        check("at a restart the name check reads absent, every other call reaches kubectl, and both are restored after",
              gone and calls == [("get", "job", "x", "-o", "json")] and kept and S8.kubectl is stub and SV.kubectl is stub, str(calls))
    finally:
        S8.kubectl, SV.kubectl = orig
    # node exclusion: the list file, the payload, and a Job created without the exclusion
    with tempfile.TemporaryDirectory() as td:
        ep = Path(td) / "exclude_nodes.json"
        none = excluded_nodes(ep)
        ep.write_text(json.dumps({"exclude_nodes": ["n-b", "n-a", "n-a"]}), encoding="utf-8")
        listed = excluded_nodes(ep)
        bad = []
        for text in ("{not json", json.dumps({"nodes": []}), json.dumps({"exclude_nodes": ["ok", ""]})):
            ep.write_text(text, encoding="utf-8")
            try:
                excluded_nodes(ep)
            except RuntimeError:
                bad.append(text)
        check("exclude list: no file is none, a list is sorted and deduplicated, a malformed file is an error",
              none == [] and listed == ["n-a", "n-b"] and len(bad) == 3, f"{none} {listed} {len(bad)}")

        class FD:
            name = "j"

            def to_dict(self):
                return {"name": "j", "image": "alpine"}
        check("the payload carries exclude_nodes only when the list is non-empty",
              Excluding(FD(), ["n-a"]).to_dict() == {"name": "j", "image": "alpine", "exclude_nodes": ["n-a"]}
              and "exclude_nodes" not in Excluding(FD(), []).to_dict() and Excluding(FD(), []).name == "j", "")

        ep.write_text(json.dumps({"exclude_nodes": ["n-a", "n-b"]}), encoding="utf-8")
        sent, on_job = [], {"values": "n-b n-a"}
        saved = (S8.preflight, S8.publish, S8.created, globals()["SPACING"])

        async def fake_publish(d, listen_s=15.0):
            sent.append(d.to_dict()); return [{"state": "submitted"}]

        def kc2(*args, timeout=120):
            if args[:2] == ("get", "job") and args[3:4] == ("-o",) and args[4].startswith("jsonpath={.spec.template.spec.affinity"):
                return subprocess.CompletedProcess(args, 0, on_job["values"], "")
            return subprocess.CompletedProcess(args, 1, "", "NotFound")
        try:
            S8.preflight = lambda d, role: None; S8.publish = fake_publish
            S8.created = lambda n: now() + dt.timedelta(seconds=1); globals()["SPACING"] = 0
            _c, snd, *_r = make_cluster({"j": (FD(), "d8")}, kc=kc2, note=lambda m: None, attempts_dir=Path(td), exclude_path=ep)
            ok_send = snd("j"); on_job["values"] = ""; bare_send = snd("j")
        finally:
            S8.preflight, S8.publish, S8.created, globals()["SPACING"] = saved
        check("a Job sent with the exclusion on it counts as sent; one created without it returns a pause reason",
              ok_send is True and isinstance(bare_send, str) and sent[0].get("exclude_nodes") == ["n-a", "n-b"], f"{ok_send!r} {bare_send!r}")
    cluster, send, delete, save, record, finish, log, cl = fake(["a", "b"], {})
    p = Pool(["a", "b"], cluster, lambda n: (send(n), "exclusion missing")[1], delete, save, record)
    ev = p.tick(t)
    check("a send that returns a reason is counted in flight and pauses the pool after it",
          p.attempts.get("a") == 1 and "b" not in p.attempts and p.paused == "exclusion missing" and log["sent"] == ["a"], str(ev))
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--i-have-checked-nrp-policy", action="store_true", dest="ack")
    a = ap.parse_args()
    if a.selftest: return 1 if selftest() else 0
    if a.dry_run: return dry()
    return run(a.ack)


if __name__ == "__main__":
    sys.exit(main())
