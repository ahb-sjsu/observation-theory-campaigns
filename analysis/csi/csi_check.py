"""XPROTO-CSI graded runner — bars per PREREG-XPROTO-CSI.md. Refuses to
grade unless the prereg is SEALED >= 1 day after family construction
(cooling-off is a code guard) AND the run is RFsim, not the simulator
(the sim validates code, not the phenomenon).

    python3 csi_check.py --check-family   # pre-seal record check (RFsim family)
    python3 csi_check.py                    # graded run (needs seal + RFsim logs)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

PREREG = os.path.join(HERE, "PREREG-XPROTO-CSI.md")
FAMILY_CONSTRUCTED = date(2026, 8, 22)
GRADED_SEEDS = [20260823, 20260824, 20260825]

# ---- the sealed bars (must match the prereg verbatim) ----------------
B1_NAIVE_BLER = 0.25       # raw CQI vacuous under aging
B2_OLLA_BLER = 0.15        # HARQ-witnessed holds near target
B3_DOMINANCE = 2.0         # olla <= naive / 2
MC1_CQI_ERR_DB = 2.0       # aging is real
MC2_FRESH_BLER = 0.15      # link sane with fresh CSI
MC3_MIN_TTI = 5000
MC3_MIN_MCS_VAR = 2


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-CSI.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off — seal {d} not >= 1 day after "
                 f"family construction {FAMILY_CONSTRUCTED}.")
    return d


def grade(cell: dict) -> dict:
    nb, ob = cell["naive_bler"], cell["olla_bler"]
    return {
        "B1": nb >= B1_NAIVE_BLER,
        "B2": ob <= B2_OLLA_BLER,
        "B3": ob <= nb / B3_DOMINANCE,
        "MC1": cell["cqi_err_db"] >= MC1_CQI_ERR_DB,
        "MC2": cell["fresh_bler"] <= MC2_FRESH_BLER,
        "MC3": cell["n_tti"] >= MC3_MIN_TTI and cell["mcs_var"] >= MC3_MIN_MCS_VAR,
    }


def report(cells: list[dict], label: str) -> dict:
    if any(c.get("mode") == "sim" for c in cells):
        sys.exit("REFUSED: sealed grading requires RFsim runs; the sim "
                 "validates code only and carries no evidential weight.")
    graded = [{**c, "grade": grade(c)} for c in cells]
    keys = ("B1", "B2", "B3", "MC1", "MC2", "MC3")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}
    mcs = all(agg[k] for k in ("MC1", "MC2", "MC3"))
    bars = agg["B1"] and agg["B2"] and agg["B3"]
    verdict = "VOID" if not mcs else ("PASS" if bars else "FAIL")
    for g in graded:
        gr = g["grade"]
        print(f"  seed {g['seed']}: naive_bler={g['naive_bler']} "
              f"olla_bler={g['olla_bler']} fresh_bler={g['fresh_bler']} -> "
              + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys), flush=True)
    print(f"{label}: {verdict} (B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; "
          f"MCs {mcs})", flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record",
                    default=os.path.join(HERE, "CSIREP-family.json"))
    args = ap.parse_args()
    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec["cells"], "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)
    seal_date = require_seal()
    raw = os.path.join(HERE, "CSIREP-graded-raw.json")
    if not os.path.exists(raw):
        sys.exit("REFUSED: CSIREP-graded-raw.json missing — run on Atlas GPU "
                 "first: csi_sionna.py --seeds 20260823 20260824 20260825 "
                 "--out CSIREP-graded-raw.json (real NR substrate).")
    rec = json.load(open(raw, encoding="utf-8"))
    cells = rec["cells"]
    seeds = sorted(c["seed"] for c in cells)
    if seeds != sorted(GRADED_SEEDS):
        sys.exit(f"REFUSED: graded seeds {seeds} != prereg {sorted(GRADED_SEEDS)}.")
    if any(c.get("mode") not in ("nrsionna", "rfsim") for c in cells):
        sys.exit("REFUSED: sealed grading requires a real NR substrate "
                 "(mode nrsionna or rfsim).")
    print(f"XPROTO-CSI graded — sealed {seal_date}, seeds {GRADED_SEEDS} "
          f"(mode {cells[0].get('mode')})", flush=True)
    out = report(cells, "XPROTO-CSI")
    out.update({"cell": "XPROTO-CSI", "sealed": str(seal_date),
                "seeds": GRADED_SEEDS})
    json.dump(out, open(os.path.join(HERE, "XPROTO-CSI-graded.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
