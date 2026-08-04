#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import statistics


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    records = []
    for path in sorted(Path(args.input).rglob("*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if value.get("schema") == "projection-fold-trial-v1":
            records.append(value)

    fold_counts = [r["outcome"].get("fold_count", 0) for r in records]
    energy_drifts = [
        r["outcome"]["max_relative_energy_drift"]
        for r in records
        if "max_relative_energy_drift" in r["outcome"]
    ]
    summary = {
        "schema": "projection-fold-summary-v1",
        "n_records": len(records),
        "total_folds": int(sum(fold_counts)),
        "mean_folds": statistics.fmean(fold_counts) if fold_counts else None,
        "max_energy_drift": max(energy_drifts) if energy_drifts else None,
        "record_hashes": [r.get("record_sha256") for r in records],
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
