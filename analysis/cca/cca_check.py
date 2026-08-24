"""XPROTO-CCA graded runner — bars per PREREG-XPROTO-CCA.md. Reuses the
family grading (fam_cca.grade_condition via run_cell) unchanged. Runs on
bench seeds DISJOINT from the sim validation's {0,1,2}. Refuses to grade
unless (a) the prereg is SEALED with a date >= one day after family
construction (2026-08-21) — the cooling-off is a code guard — and (b) the
run is on HARDWARE, not the simulator (sim is code validation, not
evidence).

    python3 cca_check.py                  # graded run (needs seal + bench)
    python3 cca_check.py --check-family   # pre-seal record check (hw family)
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

PREREG = os.path.join(HERE, "PREREG-XPROTO-CCA.md")
FAMILY_CONSTRUCTED = date(2026, 8, 21)
GRADED_SEEDS = [20260822, 20260823, 20260824]

# ---- the sealed bars (must match the prereg verbatim) ----------------
B1_FC_CCA = 0.15         # CCA-alone false-clear >= this (CCA vacuity)
B2_FC_RTSCTS = 0.05      # RTS/CTS false-clear <= this (witness helps)
B3_DOMINANCE = 3.0       # fc_cca >= 3x fc_rtscts
MC1_A_CLEAR_DURING_C = 0.80   # A cannot sense C (hidden realized)
MC2_WITNESS_DETECT = 0.80     # witness sees C at Rx
MC3_MIN = (1000, 200)         # n_clear, n_concurrent
MC3_CLEAN_DECODE = 0.90       # link sane absent interferer


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-CCA.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off — seal {d} not >= 1 day after "
                 f"family construction {FAMILY_CONSTRUCTED}.")
    return d


def grade(cell: dict) -> dict:
    fcc, fcr = cell["fc_cca"], cell["fc_rtscts"]
    return {
        "B1": fcc >= B1_FC_CCA,
        "B2": fcr <= B2_FC_RTSCTS,
        "B3": fcc >= B3_DOMINANCE * fcr,
        "MC1": cell["a_clear_during_c"] >= MC1_A_CLEAR_DURING_C,
        "MC2": cell["witness_detect"] >= MC2_WITNESS_DETECT,
        "MC3": (cell["n_clear"] >= MC3_MIN[0]
                and cell["n_concurrent"] >= MC3_MIN[1]
                and cell["clean_decode_rate"] >= MC3_CLEAN_DECODE),
        "MC4": bool(cell.get("witness_aligned")),
    }


def report(cells: list[dict], label: str) -> dict:
    if any(c.get("mode") == "sim" for c in cells):
        sys.exit("REFUSED: sealed grading requires HARDWARE runs; the sim "
                 "validates code only and carries no evidential weight.")
    graded = [{**c, "grade": grade(c)} for c in cells]
    keys = ("B1", "B2", "B3", "MC1", "MC2", "MC3", "MC4")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}
    mcs_ok = all(agg[k] for k in ("MC1", "MC2", "MC3", "MC4"))
    bars_ok = agg["B1"] and agg["B2"] and agg["B3"]
    verdict = "VOID" if not mcs_ok else ("PASS" if bars_ok else "FAIL")
    for g in graded:
        gr = g["grade"]
        print(f"  seed {g['seed']}: fc_cca={g['fc_cca']} "
              f"fc_rtscts={g['fc_rtscts']} -> "
              + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys),
              flush=True)
    print(f"{label}: {verdict} "
          f"(B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; MCs {mcs_ok})",
          flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record",
                    default=os.path.join(HERE, "CCAREP-family.json"))
    args = ap.parse_args()

    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec["cells"], "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)

    seal_date = require_seal()
    import fam_cca as fam
    print(f"XPROTO-CCA graded — sealed {seal_date}, seeds {GRADED_SEEDS} (hw)",
          flush=True)
    cells = [fam.run_cell(seed, mode="hw") for seed in GRADED_SEEDS]
    out = report(cells, "XPROTO-CCA")
    out.update({"cell": "XPROTO-CCA", "sealed": str(seal_date),
                "seeds": GRADED_SEEDS, "constants_from": "fam_cca.py"})
    path = os.path.join(HERE, "XPROTO-CCA-graded.json")
    json.dump(out, open(path, "w"), indent=1)
    print(f"-> {path}", flush=True)


if __name__ == "__main__":
    main()
