#!/usr/bin/env python3
"""The smoke run's checks (PREREG-D8-RUN-DRAFT.md Section 9, item 7). Runs ON ATLAS after every smoke Job has succeeded.

The smoke role is the run's Jobs on the smoke world (n = 64, own seeds, K = 1), every graded observer and every variant arm
in ladder halves, with the run's NATS publish. This script checks, in order:
  1. transport: for every Job, the result in its log block and the copy collected from OD_RESULTS are byte-identical;
  2. collect: submit_d8_nrp.py --collect --role smoke writes smoke.json, the halves joined (m* on the merged flags), and
     submit_variants_nrp.py --collect --role smoke writes smoke_variants.json;
  3. the NATS fallback: the same collection from the stream alone (log path disabled) gives the same merged files;
  4. grade: d8_run_grade.py on the two files gives D8's gate, OP4's reading and the secondary arms, labelled smoke.
Writes smoke_record.json. A check that fails is reported and the rest still run.

    /home/claude/env/bin/python smoke_check.py
"""
from __future__ import annotations

import base64
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VAR = HERE.parents[1] / "OP" / "VARIANTS"
sys.path.insert(0, str(VAR))
import submit_d8_nrp as d8  # noqa: E402
import submit_variants_nrp as opv  # noqa: E402

PY = sys.executable


def log_block(name: str, begin: str, end: str) -> bytes | None:
    st = d8.kubectl("get", "job", name, "-o", "jsonpath={.status.succeeded}/{.status.failed}").stdout.strip()
    if not st.startswith("1/"): return None
    log = d8.kubectl("logs", f"job/{name}").stdout
    if begin not in log: return None
    return gzip.decompress(base64.b64decode(log.split(begin, 1)[1].split(end, 1)[0].strip()))


def sha(b: bytes | None) -> str | None:
    return hashlib.sha256(b).hexdigest() if b is not None else None


def run(args: list[str], cwd: Path) -> dict:
    p = subprocess.run([PY, *args], cwd=cwd, capture_output=True, text=True)
    return {"cmd": " ".join(args), "exit": p.returncode, "tail": p.stdout.splitlines()[-12:] + p.stderr.splitlines()[-6:]}


def main() -> int:
    rec = {"check": "PREREG-D8-RUN-DRAFT.md Section 9 item 7, the smoke run", "transport": [], "steps": {}}
    jobs = [("d8", d8.job_name(w, p, "smoke", t), d8.BEGIN, d8.END) for w, t, p in d8.units("smoke", False)]
    jobs += [("opv", opv.job_name(v, w, "smoke", t, h), opv.BEGIN, opv.END) for v, w, t, h in opv.units("smoke")]
    for track, name, b, e in jobs:
        lg = log_block(name, b, e); nt = d8.fetch_nats(d8.nats_subject(track, "smoke", name))
        rec["transport"].append({"job": name, "log_sha256": sha(lg), "nats_sha256": sha(nt), "bytes": len(lg) if lg else None, "identical": lg is not None and lg == nt})
    rec["steps"]["transport_all_identical"] = all(x["identical"] for x in rec["transport"]); print("transport:", rec["steps"]["transport_all_identical"], len(jobs), "Jobs")
    # 2. collect through the normal path
    rec["steps"]["d8_collect"] = run(["submit_d8_nrp.py", "--collect", "--role", "smoke"], HERE)
    rec["steps"]["opv_save"] = run(["submit_variants_nrp.py", "--save", "--role", "smoke"], VAR)
    rec["steps"]["opv_collect"] = run(["submit_variants_nrp.py", "--collect", "--role", "smoke"], VAR)
    d8_file, var_file = HERE / "smoke.json", VAR / "smoke_variants.json"
    # 3. the same D8 collection from the stream alone: fetch with the log path disabled
    real_kubectl = d8.kubectl
    def no_logs(*a):
        if a and a[0] == "logs": return subprocess.CompletedProcess(a, 1, "", "logs disabled for the NATS-only check")
        return real_kubectl(*a)
    d8.kubectl = no_logs
    try:
        pieces = {}
        for w, t, p in d8.units("smoke", False):
            jn = d8.job_name(w, p, "smoke", t); got, _ = d8.fetch(jn, d8.nats_subject("d8", "smoke", jn))
            if got: pieces[f"t{t}_{p}"] = got[0]
        nats_only = d8.merge_parts(d8.join_halves(pieces)) if pieces else None
    finally:
        d8.kubectl = real_kubectl
    if nats_only is not None and d8_file.exists():
        p = HERE / "smoke_nats_only.json"; p.write_text(json.dumps({**{k: v for k, v in nats_only.items() if k != "worlds"}, "worlds": nats_only["worlds"]}, indent=1), encoding="utf-8")
        a = json.loads(d8_file.read_text(encoding="utf-8")); b = nats_only
        same = json.dumps(a["worlds"], sort_keys=True) == json.dumps(b["worlds"], sort_keys=True)
        rec["steps"]["d8_nats_only_same_worlds"] = same; p.unlink()
    else:
        rec["steps"]["d8_nats_only_same_worlds"] = False
    print("NATS-only D8 collection equals the log collection:", rec["steps"]["d8_nats_only_same_worlds"])
    # 4. grade
    if d8_file.exists() and var_file.exists():
        rec["steps"]["grade"] = run(["d8_run_grade.py", str(d8_file), str(var_file), "--tols", "tolerances.json", "--out", "smoke_grade.json"], HERE)
        g = json.loads((HERE / "smoke_grade.json").read_text(encoding="utf-8")) if (HERE / "smoke_grade.json").exists() else {}
        rec["summary"] = {"d8_gate": g.get("d8", {}).get("gate"), "op4_reading": g.get("op4", {}).get("reading"),
                          "secondary": {k: v.get("beats_ball") for k, v in g.get("secondary", {}).items()}}
    w = json.loads(d8_file.read_text(encoding="utf-8"))["worlds"][0] if d8_file.exists() else None
    if w:
        t = w["tests"][0]; rec["budgets"] = {k: (o["m_star"] if "m_star" in o else "NO m* (an unmerged half)") for k, o in t["observers"].items()}
    if var_file.exists():
        v = json.loads(var_file.read_text(encoding="utf-8"))
        for arm, ws in v["arms"].items():
            for x in ws.values(): rec.setdefault("budgets", {})[arm] = x["tests"][0]["observers"][arm].get("m_star")
        rec["variants_missing"] = v["missing"]
    ok = rec["steps"]["transport_all_identical"] and rec["steps"]["d8_nats_only_same_worlds"] and all(s.get("exit") == 0 for k, s in rec["steps"].items() if isinstance(s, dict))
    rec["result"] = "PASS" if ok else "FAIL"
    (HERE / "smoke_record.json").write_text(json.dumps(rec, indent=1), encoding="utf-8"); print(json.dumps({k: rec.get(k) for k in ("result", "summary", "budgets")}, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
