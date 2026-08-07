#!/usr/bin/env python3
"""Normalize G1 packets into an arm-agnostic item list for scoring.

Strips everything that identifies which arm produced a packet, keeps
only the fields a scorer is entitled to see, and shuffles the items
under a declared seed so their order carries no signal either.

The normalizer cannot hide vocabulary. A packet from the kernel arm
will speak of substrates and consumers and a packet from the
comparator will not, and that limitation is recorded in
GENERATOR-DRYRUN.md rather than papered over here. What the
normalizer removes is the arm label, the packet scaffolding, the
operator tags, and the file provenance, so that no scorer is told
which arm is the hypothesis or even that arms exist.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402

KEEP = ("statement", "quantitative_test", "bars", "falsifier")


def normalize(packet, order_seed):
    items = []
    for raw in packet.get("items", []):
        items.append({k: raw.get(k, "") for k in KEEP})
    rng = random.Random(order_seed)
    rng.shuffle(items)
    for i, item in enumerate(items, start=1):
        item["id"] = f"N{i}"
    return items


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("packets", nargs="+")
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    bundles = []
    for path in args.packets:
        pk = json.loads(Path(path).read_text(encoding="utf-8"))
        items = normalize(pk, args.seed)
        bundles.append({
            "bundle_id": canonical_sha256(
                {"src": Path(path).name, "seed": args.seed})[:12],
            "domain_description": pk["domain_description"],
            "items": items,
            "source_file": Path(path).name,
        })
    # the bundle order is shuffled too, so position carries nothing
    rng = random.Random(args.seed ^ 0x5F5F)
    rng.shuffle(bundles)

    scorer_view = [
        {"bundle_id": b["bundle_id"],
         "domain_description": b["domain_description"],
         "items": b["items"]}
        for b in bundles
    ]
    key = {b["bundle_id"]: b["source_file"] for b in bundles}

    record = {
        "schema": "g1-normalized-v1",
        "label": "rehearsal",
        "order_seed": args.seed,
        "scorer_view": scorer_view,
        "unblinding_key": key,
        "note": "the unblinding key is kept in the record and is "
                "not given to any scorer; vocabulary may still "
                "identify an arm and that limit is declared in "
                "GENERATOR-DRYRUN.md",
        "runtime": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "platform": platform.platform(),
            "hostname": platform.node(),
            "code_commit": os.environ.get("CODE_COMMIT", "unknown"),
        },
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = root / "results" / args.out
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    for b in scorer_view:
        print(b["bundle_id"], len(b["items"]), "items")
    print("key", key)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
