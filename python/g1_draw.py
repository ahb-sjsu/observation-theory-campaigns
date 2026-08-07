#!/usr/bin/env python3
"""Execute the G1 domain draw exactly as sealed.

Implements GENERATOR-DOMAIN-POOL-V2.md section 3. Run with
--rehearse and a past timestamp to exercise the machinery without
touching the sealed pulse. Run with no arguments on or after the
sealed instant to perform the real draw.

The rehearsal writes to a rehearsal path and refuses to overwrite
the real record, so a dry run cannot be mistaken for the draw.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import random
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402

SEALED_TIMESTAMP = "2026-08-14T00:00:00Z"
SUBSET_TIMESTAMP = "2026-08-21T00:00:00Z"
BEACON = "https://beacon.nist.gov/beacon/2.0/pulse/time/{ms}"
STRATUM_ORDER = ["N", "F", "A"]
PER_STRATUM = 4


def iso_to_ms(stamp):
    dt = datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)


def fetch_pulse(stamp):
    url = BEACON.format(ms=iso_to_ms(stamp))
    req = urllib.request.Request(
        url, headers={"User-Agent": "g1-draw"})
    with urllib.request.urlopen(req, timeout=60) as fh:
        data = json.load(fh)["pulse"]
    return {"uri": data["uri"], "timeStamp": data["timeStamp"],
            "pulseIndex": data["pulseIndex"],
            "outputValue": data["outputValue"]}


def draw(pool_strata, seed_hex):
    """The sealed algorithm, verbatim."""
    seed = int(seed_hex, 16)
    rng = random.Random(seed)
    out = {}
    for name in STRATUM_ORDER:
        items = sorted(pool_strata[name])
        rng.shuffle(items)
        out[name] = items[:PER_STRATUM]
    return seed, out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rehearse", metavar="ISO8601",
                    help="a past pulse timestamp, writes to the "
                         "rehearsal path and never to the record")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    pool = json.loads((root / "results" / "g1-domain-pool.json")
                      .read_text(encoding="utf-8"))
    strata = pool["strata"]

    rehearsing = args.rehearse is not None
    stamp = args.rehearse if rehearsing else SEALED_TIMESTAMP
    if not rehearsing:
        now = datetime.now(timezone.utc)
        if now < datetime.strptime(
                SEALED_TIMESTAMP, "%Y-%m-%dT%H:%M:%SZ").replace(
                    tzinfo=timezone.utc):
            print("the sealed pulse does not exist yet, refusing")
            return 2

    pulse = fetch_pulse(stamp)
    seed, drawn = draw(strata, pulse["outputValue"])
    twelve = [c for name in STRATUM_ORDER for c in drawn[name]]

    record = {
        "schema": "g1-domain-draw-v1",
        "label": "rehearsal" if rehearsing else "sealed-draw",
        "protocol": "experiments/GENERATOR-DOMAIN-POOL-V2.md",
        "pool_record_sha256": pool["record_sha256"],
        "requested_timestamp": stamp,
        "pulse": pulse,
        "derived_seed": str(seed),
        "drawn_by_stratum": drawn,
        "drawn_twelve": twelve,
        "stratum_sizes": {k: len(strata[k])
                          for k in STRATUM_ORDER},
        "runtime": {
            "generated_utc": datetime.now(
                timezone.utc).isoformat(),
            "python": sys.version,
            "platform": platform.platform(),
            "hostname": platform.node(),
            "code_commit": os.environ.get("CODE_COMMIT",
                                          "unknown")},
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    name = ("g1-domain-draw-rehearsal.json" if rehearsing
            else "g1-domain-draw.json")
    out = root / "results" / name
    if not rehearsing and out.exists():
        print("the draw record already exists, refusing to redraw")
        return 3
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("pulse", pulse["timeStamp"], "index",
          pulse["pulseIndex"])
    for k in STRATUM_ORDER:
        print(f"  {k}: {' '.join(drawn[k])}")
    print("record", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
