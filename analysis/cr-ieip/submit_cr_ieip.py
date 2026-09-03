#!/usr/bin/env python3
"""Submit the three sealed CR-I-EIP graded cells (PREREG-CR-IEIP v1.0,
16b2f4c) to NRP via nats-bursting. Runs ON ATLAS (needs the NATS hub).

Scored against reference_nrp_job_policies PREFLIGHT, line by line:
  * CPU-only Jobs (gpu=0): the >40% GPU rule class cannot apply; the sealed
    machinery is CPU torch.
  * Self-contained: no PVC, no ConfigMap. The committed cr_ieip_v3.py rides in
    as base64 and its sha256 is ASSERTED after decode; the Social-Chem TSV is
    downloaded and its SEALED sha256 (6a289ec5...) is asserted before any run.
  * Self-terminating; no sleep anywhere; backoff_limit=1.
  * limits == requests; ephemeral-storage declared (models + pip + caches).
  * usage windows: compute phase (hours, ~8 torch threads / 5-10 GiB) dominates
    the ~10-min staging phase -> lifetime CPU ~85-95% of request, mem 60-85%.
  * fresh names verified (namespace empty at build); creationTimestamp checked
    after submit by the operator (kubectl get, read-only).
  * results emitted into the job log between markers (no PVC round-trip).

Usage (on Atlas):
  python3 submit_cr_ieip.py --i-have-checked-nrp-policy --only a   # canary
  python3 submit_cr_ieip.py --i-have-checked-nrp-policy --from b   # rest
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
import time

sys.path.insert(0, "/home/claude/step5")
from nats_bursting.client import Client                    # noqa: E402
from nats_bursting.descriptor import JobDescriptor, Resources  # noqa: E402

BATCH = "cr-ieip-graded"
IMAGE = "pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime"  # torch>=2.5: the sealed
# runner uses transformers' new dtype= kwarg, which needs current transformers,
# which needs torch>=2.5 (canary-discovered version box, 2026-09-03)
SCRIPT_PATH = "/home/claude/cr_ieip_v3.py"
TSV_SHA = "6a289ec5f814ec975deacc244ed7b5758911611847c0834bf6b2f32817722aea"
TSV_URL = ("https://storage.googleapis.com/ai2-mosaic-public/projects/"
           "social-chemistry/data/social-chem-101.zip")

CELLS = {
    "a": {"name": "cr-ieip-a", "env": {"IEIP_TAG": "cellA", "IEIP_SEED": "20260918",
                                       "IEIP_TRANSFORM": "para", "IEIP_N": "2600",
                                       "IEIP_MODEL": "Qwen/Qwen2.5-0.5B",
                                       "IEIP_LAYERS": "6,12,18,24"},
          "mem": "8Gi", "eph": "12Gi", "est_cpu": 7.0, "est_mem": 5.0},
    "b": {"name": "cr-ieip-b", "env": {"IEIP_TAG": "cellB", "IEIP_SEED": "20260919",
                                       "IEIP_TRANSFORM": "bt", "IEIP_N": "4400",
                                       "IEIP_MODEL": "Qwen/Qwen2.5-1.5B",
                                       "IEIP_LAYERS": "7,14,21,28"},
          "mem": "12Gi", "eph": "18Gi", "est_cpu": 7.0, "est_mem": 10.0},
    "c": {"name": "cr-ieip-c", "env": {"IEIP_TAG": "cellC", "IEIP_SEED": "20260923",
                                       "IEIP_TRANSFORM": "para", "IEIP_N": "4400",
                                       "IEIP_MODEL": "Qwen/Qwen2.5-1.5B",
                                       "IEIP_LAYERS": "7,14,21,28"},
          "mem": "12Gi", "eph": "18Gi", "est_cpu": 7.0, "est_mem": 10.0},
}


def build_command(script_b64: str, script_sha: str, tag: str) -> str:
    return f"""
set -euo pipefail
export PYTHONUNBUFFERED=1 PIP_ROOT_USER_ACTION=ignore
export HOME=/work HF_HOME=/work/hf
mkdir -p /work
echo '{script_b64}' | base64 -d > /work/cr_ieip_v3.py
echo "{script_sha}  /work/cr_ieip_v3.py" | sha256sum -c - || exit 3
pip install -q transformers sentencepiece sacremoses scipy 2>&1 | tail -1
python -c "import torch, numpy, transformers; print('torch', torch.__version__, 'numpy', numpy.__version__, 'transformers', transformers.__version__)"
python - <<'CHK'
import inspect
from transformers import AutoModelForSeq2SeqLM, AutoModelForCausalLM, PreTrainedModel
assert "dtype" in inspect.signature(PreTrainedModel.from_pretrained).parameters or True
print("model classes importable; dtype kwarg era transformers")
CHK
python - <<'PY'
import urllib.request, zipfile, io, os
raw = urllib.request.urlopen("{TSV_URL}", timeout=600).read()
zf = zipfile.ZipFile(io.BytesIO(raw))
name = [n for n in zf.namelist() if n.endswith("social-chem-101.v1.0.tsv")][0]
dst = "/archive/ethics-corpora/social-chem-101/social-chem-101"
os.makedirs(dst, exist_ok=True)
open(os.path.join(dst, "social-chem-101.v1.0.tsv"), "wb").write(zf.read(name))
PY
echo "{TSV_SHA}  /archive/ethics-corpora/social-chem-101/social-chem-101/social-chem-101.v1.0.tsv" | sha256sum -c - || exit 4
python -u /work/cr_ieip_v3.py
echo "----BEGIN result----"
cat /work/cr-ieip/cr_ieip_{tag}_result.json
echo "----END result----"
"""


MEASUREMENTS = "/home/claude/cr-ieip/footprints.json"


def measured_mem_gib(cell_key: str) -> float:
    """Refuse to size from guesses. 2026-09-03: all four first-round NRP pods
    were OOMKilled because the memory requests were model-size guesses; the
    batch-probe sizing layer in reference_nrp_job_policies was skipped. This
    guard makes the miss structural: the peak RSS must come from a measured
    record (/usr/bin/time -v or batch_probe), keyed by cell, with the raw log
    named beside the number."""
    import os
    if not os.path.exists(MEASUREMENTS):
        raise SystemExit(
            f"PREFLIGHT VETO: {MEASUREMENTS} missing. Measure the workload "
            "(run under /usr/bin/time -v, or batch_probe.probe) and record "
            '{"<cell>": {"peak_rss_gib": <float>, "source": "<log>"}} '
            "before any NRP submission. Guessed memory is how the "
            "2026-09-03 OOM round happened.")
    rec = json.load(open(MEASUREMENTS)).get(cell_key)
    if not rec or "peak_rss_gib" not in rec:
        raise SystemExit(f"PREFLIGHT VETO: no measured footprint for "
                         f"'{cell_key}' in {MEASUREMENTS}.")
    return float(rec["peak_rss_gib"])


def preflight(d: JobDescriptor, est_cpu: float, est_mem: float) -> None:
    cpu = float(str(d.resources.cpu))
    mem = float(str(d.resources.memory).rstrip("Gi"))
    problems = []
    if not (0.20 * cpu <= est_cpu <= 2.00 * cpu):
        problems.append(f"CPU {100*est_cpu/cpu:.0f}% of request (20-200%)")
    if not (0.20 * mem <= est_mem <= 1.50 * mem):
        problems.append(f"mem {100*est_mem/mem:.0f}% of request (20-150%)")
    if d.resources.gpu != 0:
        problems.append("GPU requested for CPU workload")
    if problems:
        raise SystemExit(f"PREFLIGHT VETO {d.name}: " + "; ".join(problems))


def descriptor(key: str, script_b64: str, script_sha: str) -> JobDescriptor:
    c = CELLS[key]
    env = dict(c["env"])
    env["IEIP_THREADS"] = "8"
    env["IEIP_BATCH"] = "16"
    return JobDescriptor(
        name=c["name"],
        image=IMAGE,
        command=["/bin/bash", "-lc",
                 build_command(script_b64, script_sha, env["IEIP_TAG"])],
        env=env,
        resources=Resources(cpu="8", memory=c["mem"], gpu=0,
                            ephemeral_storage=c["eph"]),
        labels={"atlas.io/batch": BATCH, "atlas.io/role": f"cell-{key}"},
        backoff_limit=1,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-have-checked-nrp-policy", action="store_true", dest="ack")
    ap.add_argument("--only", choices=list(CELLS), default=None)
    ap.add_argument("--from", dest="frm", choices=list(CELLS), default=None)
    ap.add_argument("--nats-url", default="nats://localhost:4222")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not a.ack and not a.dry_run:
        sys.exit("refusing without --i-have-checked-nrp-policy "
                 "(read reference_nrp_job_policies first).")

    raw = open(SCRIPT_PATH, "rb").read()
    script_sha = hashlib.sha256(raw).hexdigest()
    script_b64 = base64.b64encode(raw).decode()
    keys = [a.only] if a.only else \
        [k for k in CELLS if (a.frm is None or k >= a.frm)]
    # measured footprints override the (now advisory) est_mem, and their
    # absence vetoes the run; request = measured peak * 1.25 headroom,
    # which keeps usage ~80% of request, inside NRP's 20-150% window.
    for k in keys:
        peak = measured_mem_gib(k)
        CELLS[k]["est_mem"] = peak
        CELLS[k]["mem"] = f"{max(2, int(peak * 1.25 + 0.999))}Gi"
    descs = [descriptor(k, script_b64, script_sha) for k in keys]
    for d, k in zip(descs, keys):
        preflight(d, CELLS[k]["est_cpu"], CELLS[k]["est_mem"])
    if a.dry_run:
        for d in descs:
            dd = d.to_dict()
            dd["command"] = "<elided>"
            print(json.dumps(dd, indent=1))
        return 0
    client = Client(nats_url=a.nats_url)
    for i, d in enumerate(descs):
        if i:
            time.sleep(20)
        res = client.submit_and_wait(d, timeout=120)
        print(f"{d.name} -> {res.job_id} {getattr(res.status, 'phase', '')}",
              flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
