"""XPROTO-GEO graded runner — bars per PREREG-XPROTO-GEO.md. Grades the
two-axis dominance of the consumer-relative certificate router over the
naive nearest / least-lag routers. Refuses to grade unless the prereg is
SEALED >= 1 day after family construction (cooling-off is a code guard).

    python3 geo_check.py --check-family   # pre-seal record check
    python3 geo_check.py                   # graded (needs seal + live fleet)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-GEO.md")
FAMILY_CONSTRUCTED = date(2026, 8, 21)
GRADED_SEEDS = [20260822, 20260823, 20260824]

# ---- the sealed bars (must match the prereg verbatim) ----------------
B1_CERT_FC = 0.05          # certificate correct
B2_DOMINANCE = 3.0         # cert.fc <= nearest.fc / 3  (freshness axis)
B3_LOCALITY_TAX = 1.3      # cert.rtt <= 1.3 * nearest.rtt  (near-optimal locality)
MC1_NEAREST_FC = 0.15      # nearest materially stale (non-degenerate)
MC2_RTT_SPREAD = 1.5       # real geographic locality
MC3_MIN_WRITES = 300       # hot activity
MC4_FP_DEP = 0.05          # consumer-relativity realized


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-GEO.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off — seal {d} not >= 1 day after "
                 f"family construction {FAMILY_CONSTRUCTED}.")
    return d


def grade(cell: dict) -> dict:
    h = cell["agg"]["HOT"]
    cert_fc, near_fc = h["cert"]["fc"], h["nearest"]["fc"]
    cert_rtt = h["cert"]["mean_rtt_ms"]
    near_rtt, ll_rtt = h["nearest"]["mean_rtt_ms"], h["leastlag"]["mean_rtt_ms"]
    return {
        "B1": cert_fc <= B1_CERT_FC,
        "B2": cert_fc <= near_fc / B2_DOMINANCE,
        "B3": cert_rtt <= ll_rtt and cert_rtt <= B3_LOCALITY_TAX * near_rtt,
        "MC1": near_fc >= MC1_NEAREST_FC,
        "MC2": cell["rtt_spread"] >= MC2_RTT_SPREAD,
        "MC3": cell["n_replicas"] >= 3 and cell["hot_writes"] >= MC3_MIN_WRITES,
        "MC4": cell["footprint_dependence"] >= MC4_FP_DEP,
    }


def report(cells: list[dict], label: str) -> dict:
    graded = [{**c, "grade": grade(c)} for c in cells]
    keys = ("B1", "B2", "B3", "MC1", "MC2", "MC3", "MC4")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}
    mcs = all(agg[k] for k in ("MC1", "MC2", "MC3", "MC4"))
    bars = agg["B1"] and agg["B2"] and agg["B3"]
    verdict = "VOID" if not mcs else ("PASS" if bars else "FAIL")
    for g in graded:
        h, gr = g["agg"]["HOT"], g["grade"]
        print(f"  seed {g['seed']}: HOT cert_fc={h['cert']['fc']} "
              f"nearest_fc={h['nearest']['fc']} | rtt_ms cert={h['cert']['mean_rtt_ms']} "
              f"nearest={h['nearest']['mean_rtt_ms']} leastlag={h['leastlag']['mean_rtt_ms']} "
              f"-> " + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys),
              flush=True)
    print(f"{label}: {verdict} (B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; "
          f"MCs {mcs})", flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record",
                    default=os.path.join(HERE, "GEOREP-family.json"))
    args = ap.parse_args()
    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec["cells"], "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)
    seal_date = require_seal()
    print(f"XPROTO-GEO graded — sealed {seal_date}. Run the graded Job "
          f"(seeds {GRADED_SEEDS}) via run_geofleet.sh, then grade its record:",
          flush=True)
    rec = json.load(open(os.path.join(HERE, "GEOREP-graded-raw.json")))
    out = report(rec["cells"], "XPROTO-GEO")
    out.update({"cell": "XPROTO-GEO", "sealed": str(seal_date), "seeds": GRADED_SEEDS})
    json.dump(out, open(os.path.join(HERE, "XPROTO-GEO-graded.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
