#!/usr/bin/env python3
"""Consensus and the primary endpoint for a G1 scoring round.

Applies GENERATOR-G1.md sections 7.2 and 9.1. The consensus level
is the median of the scorers. An item whose levels span more than
one level is flagged for adjudication rather than silently
averaged. The five validity conditions take a majority.

The primary endpoint counts, per bundle, the items satisfying all
five conditions by consensus, and compares bundles pairwise. In a
rehearsal the comparison is reported and then discarded, because
the rehearsal measures the harness and not the generator.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402

CONDITIONS = ("commits_before_answer", "names_counting_outcome",
              "domain_native_quantity", "counterfactual_leverage",
              "not_settled_by_setup")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scores", nargs="+", required=True)
    ap.add_argument("--normalized", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--rehearsal", action="store_true")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    norm = json.loads((root / "results" / args.normalized)
                      .read_text(encoding="utf-8"))
    key = norm["unblinding_key"]

    per_item = defaultdict(list)
    scorers = []
    for path in args.scores:
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
        scorers.append(doc.get("scorer", Path(path).stem))
        for row in doc["scores"]:
            per_item[(row["bundle_id"], row["item_id"])].append(row)

    consensus = {}
    adjudicate = []
    for (bundle, item), rows in sorted(per_item.items()):
        levels = [int(r["level"]) for r in rows]
        spread = max(levels) - min(levels)
        med = int(statistics.median_low(levels))
        conds = {}
        for c in CONDITIONS:
            votes = [bool(r.get(c)) for r in rows]
            conds[c] = sum(votes) > len(votes) / 2
        rep = sum(bool(r.get("replication_grade"))
                  for r in rows) > len(rows) / 2
        all_five = all(conds.values())
        consensus[f"{bundle}/{item}"] = {
            "levels": levels, "level_spread": spread,
            "consensus_level": med, "conditions": conds,
            "all_five_conditions": all_five,
            "replication_grade": rep}
        if spread > 1:
            adjudicate.append({"bundle": bundle, "item": item,
                               "levels": levels})

    counts = defaultdict(int)
    level3plus = defaultdict(int)
    repcount = defaultdict(int)
    for k, v in consensus.items():
        bundle = k.split("/")[0]
        if v["all_five_conditions"]:
            counts[bundle] += 1
        if v["consensus_level"] >= 3:
            level3plus[bundle] += 1
        if v["replication_grade"]:
            repcount[bundle] += 1

    bundles = sorted(counts.keys() | set(key.keys()))
    record = {
        "schema": "g1-consensus-v1",
        "label": "rehearsal" if args.rehearsal else "scored-round",
        "scorers": scorers,
        "n_items": len(consensus),
        "consensus": consensus,
        "adjudication_queue": adjudicate,
        "adjudication_rate": (len(adjudicate) / len(consensus)
                              if consensus else 0.0),
        "per_bundle_all_five": {b: counts[b] for b in bundles},
        "per_bundle_level_ge_3": {b: level3plus[b] for b in bundles},
        "per_bundle_replication_grade": {b: repcount[b]
                                         for b in bundles},
        "unblinding_key": key,
        "note": ("rehearsal numbers are discarded and count for "
                 "nothing" if args.rehearsal else ""),
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
    print("items", len(consensus), "adjudication rate",
          round(record["adjudication_rate"], 4))
    for b in bundles:
        print(f"  {b} ({key.get(b,'?')}): all-five {counts[b]}, "
              f"level>=3 {level3plus[b]}, replication {repcount[b]}")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
