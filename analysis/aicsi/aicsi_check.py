"""XPROTO-AICSI graded runner — bars per PREREG-XPROTO-AICSI.md. Coded
cooling-off + real-NR-substrate guard. Mirrors csi_check / beam_check.

    python3 aicsi_check.py --check-family   # pre-seal record check
    python3 aicsi_check.py                    # graded run (needs seal + NR record)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-AICSI.md")
FAMILY_CONSTRUCTED = date(2026, 8, 22)
GRADED_SEEDS = [20260823, 20260824, 20260825]

# ---- sealed bars (must match the prereg verbatim) --------------------
# Certificate = reconstruction fidelity; consumer = precoder gain; witness = HARQ.
B1_NMSE_FC = 0.22          # NMSE-optimal codec false-clears at the consumer
B2_AWARE_FC = 0.18         # consumer-aware codec holds well below it
B3_DOMINANCE = 1.7         # aware_fc <= nmse_fc / 1.7
MC1_PARADOX_MARGIN = 0.20  # the vacuity: NMSE codec WINS reconstruction (its
                           # recon NMSE lower than the aware codec's) by >= 0.20
MC2_PERFECT_FC = 0.15      # link sane with perfect CSI -> failures are feedback
MC3_NMSE_RECON_MAX = 0.90  # the NMSE codec actually learned to reconstruct


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-AICSI.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off — seal {d} not >= 1 day after "
                 f"family construction {FAMILY_CONSTRUCTED}.")
    return d


def grade(c: dict) -> dict:
    nf, af = c["nmse_false_clear"], c["aware_false_clear"]
    return {
        "B1": nf >= B1_NMSE_FC,
        "B2": af <= B2_AWARE_FC,
        "B3": af <= nf / B3_DOMINANCE,
        "MC1": c["nmse_recon_aware"] - c["nmse_recon_nmse"] >= MC1_PARADOX_MARGIN,
        "MC2": c["perfect_false_clear"] <= MC2_PERFECT_FC,
        "MC3": c["nmse_recon_nmse"] <= MC3_NMSE_RECON_MAX
        and c["aware_gain_frac"] >= c["nmse_gain_frac"],
    }


def report(cells: list[dict], label: str) -> dict:
    if any(c.get("mode") == "sim" for c in cells):
        sys.exit("REFUSED: sealed grading requires the real NR substrate.")
    graded = [{**c, "grade": grade(c)} for c in cells]
    keys = ("B1", "B2", "B3", "MC1", "MC2", "MC3")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}
    mcs_ok = all(agg[k] for k in ("MC1", "MC2", "MC3"))
    bars = agg["B1"] and agg["B2"] and agg["B3"]
    verdict = "VOID" if not mcs_ok else ("PASS" if bars else "FAIL")
    for g in graded:
        gr = g["grade"]
        print(f"  seed {g['seed']}: nmse_fc={g['nmse_false_clear']} "
              f"aware_fc={g['aware_false_clear']} | recon nmse={g['nmse_recon_nmse']} "
              f"aware={g['nmse_recon_aware']} -> "
              + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys), flush=True)
    print(f"{label}: {verdict} (B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; "
          f"MCs {mcs_ok})", flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record", default=os.path.join(HERE, "AICSIREP-family.json"))
    args = ap.parse_args()
    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec["cells"], "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)
    seal_date = require_seal()
    raw = os.path.join(HERE, "AICSIREP-graded-raw.json")
    if not os.path.exists(raw):
        sys.exit("REFUSED: AICSIREP-graded-raw.json missing — run on Atlas GPU "
                 "first: aicsi.py --seeds 20260823 20260824 20260825 "
                 "--out AICSIREP-graded-raw.json.")
    rec = json.load(open(raw, encoding="utf-8"))
    cells = rec["cells"]
    seeds = sorted(c["seed"] for c in cells)
    if seeds != sorted(GRADED_SEEDS):
        sys.exit(f"REFUSED: graded seeds {seeds} != prereg {sorted(GRADED_SEEDS)}.")
    if any(c.get("mode") != "nrsionna_aicsi" for c in cells):
        sys.exit("REFUSED: sealed grading requires mode nrsionna_aicsi.")
    print(f"XPROTO-AICSI graded — sealed {seal_date}, seeds {GRADED_SEEDS}", flush=True)
    out = report(cells, "XPROTO-AICSI")
    out.update({"cell": "XPROTO-AICSI", "sealed": str(seal_date), "seeds": GRADED_SEEDS})
    json.dump(out, open(os.path.join(HERE, "XPROTO-AICSI-graded.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
