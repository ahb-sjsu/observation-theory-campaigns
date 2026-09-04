#!/usr/bin/env python3
"""Tier-1 HLS timing run for the EPU silicon cell -- PREPARED, NOT AUTO-RUN.

Submits ONE self-terminating CPU job (no FPGA requested) that unpacks the
epu_u55c sources (base64-embedded tar, sha-asserted), sources Vitis 2023.2,
runs run_hls_timing.sh, and emits hls_timing_summary.md between markers.

Policy notes (reference_nrp_job_policies scored line-by-line):
  * image gitlab-registry.nrp-nautilus.io/nrp/coder-images/vivado-vitis --
    owner-confirmed anonymously pullable ("worked before without any secret").
  * FIRST-RUN MEASUREMENT: no measured HLS footprint exists yet, so this run
    IS the measurement (wrapped in /usr/bin/time -v); requests are set to a
    modest 4 CPU / 8Gi with limits==requests and the log records true usage
    for footprints.json. csynth is largely single-threaded; usage floor risk
    is low (expected 1-2 cores ~ 25-50% of 4).
  * Self-terminating, no sleeps, backoff_limit=1, ephemeral 20Gi (Vitis tmp).

Run ON ATLAS, only on the owner's explicit go:
  python3 submit_tier1_hls.py --i-have-checked-nrp-policy
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import os
import sys
import tarfile

sys.path.insert(0, "/home/claude/step5")
from nats_bursting.client import Client                    # noqa: E402
from nats_bursting.descriptor import JobDescriptor, Resources  # noqa: E402

IMAGE = "gitlab-registry.nrp-nautilus.io/nrp/coder-images/vivado-vitis"
SRC = os.path.expanduser("~/epu_u55c.tgz")   # staged from the repo before run


def build_command(tar_b64: str, tar_sha: str) -> str:
    return f"""
set -euo pipefail
export PYTHONUNBUFFERED=1 HOME=/work
mkdir -p /work && cd /work
echo '{tar_b64}' | base64 -d > epu.tgz
echo "{tar_sha}  epu.tgz" | sha256sum -c - || exit 3
tar xzf epu.tgz
for V in 2023.2 2023.1 2021.2; do
  [ -f /tools/Xilinx/Vitis/$V/settings64.sh ] && {{ source /tools/Xilinx/Vitis/$V/settings64.sh; echo "VITIS=$V"; break; }}
done
which vitis_hls || which vivado_hls || {{ echo NO-HLS-TOOL; exit 4; }}
cd epu_u55c
/usr/bin/time -v ./run_hls_timing.sh . 2>&1 | tail -80
echo "----BEGIN summary----"
cat hls_timing_summary.md 2>/dev/null || echo "summary missing; see raw reports above"
echo "----END summary----"
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-have-checked-nrp-policy", action="store_true", dest="ack")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not a.ack and not a.dry_run:
        sys.exit("refusing without --i-have-checked-nrp-policy")
    raw = open(SRC, "rb").read()
    if len(raw) > 2_000_000:
        sys.exit(f"tar too large to embed ({len(raw)}B); use PVC staging instead")
    d = JobDescriptor(
        name="epu-tier1-hls",
        image=IMAGE,
        command=["/bin/bash", "-lc",
                 build_command(base64.b64encode(raw).decode(),
                               hashlib.sha256(raw).hexdigest())],
        resources=Resources(cpu="4", memory="8Gi", gpu=0,
                            ephemeral_storage="20Gi"),
        labels={"atlas.io/batch": "epu-silicon-cell", "atlas.io/role": "tier1-hls"},
        backoff_limit=1,
    )
    if a.dry_run:
        dd = d.to_dict(); dd["command"] = "<elided>"
        import json; print(json.dumps(dd, indent=1))
        return 0
    res = Client(nats_url="nats://localhost:4222").submit_and_wait(d, timeout=120)
    print(f"{d.name} -> {res.job_id} {getattr(res.status, 'phase', '')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
