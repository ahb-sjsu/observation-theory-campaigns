"""XPROTO-BEAM graded runner — bars per PREREG-XPROTO-BEAM.md. Coded
cooling-off (seal >= 1 day after family construction) + real-NR-substrate
guard (refuses the sim). Mirrors csi_check.py.

    python3 beam_check.py --check-family   # pre-seal record check
    python3 beam_check.py                   # graded run (needs seal + NR record)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-BEAM.md")
FAMILY_CONSTRUCTED = date(2026, 8, 22)
GRADED_SEEDS = [20260823, 20260824, 20260825]

# ---- sealed bars (must match the prereg verbatim) --------------------
B1_NAIVE_BLER = 0.25       # stale beam vacuous under angular aging
B2_BFR_BLER = 0.15         # beam-failure recovery holds near target
B3_DOMINANCE = 2.0         # bfr <= naive / 2
MC1_BEAM_LOSS_DB = 2.0     # misalignment is real (mean beamforming-gain loss)
MC2_FRESH_BLER = 0.15      # link sane with a fresh beam
MC3_MIN_SLOT = 5000
MC3_MIN_BEAM_VAR = 2       # beams actually switch (certificate active)


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-BEAM.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off — seal {d} not >= 1 day after "
                 f"family construction {FAMILY_CONSTRUCTED}.")
    return d


def grade(cell: dict) -> dict:
    nb, bb = cell["naive_bler"], cell["bfr_bler"]
    return {
        "B1": nb >= B1_NAIVE_BLER,
        "B2": bb <= B2_BFR_BLER,
        "B3": bb <= nb / B3_DOMINANCE,
        "MC1": cell["beam_loss_db"] >= MC1_BEAM_LOSS_DB,
        "MC2": cell["fresh_bler"] <= MC2_FRESH_BLER,
        "MC3": cell["n_slot"] >= MC3_MIN_SLOT and cell["beam_var"] >= MC3_MIN_BEAM_VAR,
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
        print(f"  seed {g['seed']}: naive_bler={g['naive_bler']} "
              f"bfr_bler={g['bfr_bler']} fresh_bler={g['fresh_bler']} "
              f"beam_loss={g['beam_loss_db']}dB -> "
              + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys), flush=True)
    print(f"{label}: {verdict} (B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; "
          f"MCs {mcs_ok})", flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record", default=os.path.join(HERE, "BEAMREP-family.json"))
    args = ap.parse_args()
    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec["cells"], "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)
    seal_date = require_seal()
    raw = os.path.join(HERE, "BEAMREP-graded-raw.json")
    if not os.path.exists(raw):
        sys.exit("REFUSED: BEAMREP-graded-raw.json missing — run on Atlas GPU "
                 "first: fam_beam.py --seeds 20260823 20260824 20260825 "
                 "--out BEAMREP-graded-raw.json.")
    rec = json.load(open(raw, encoding="utf-8"))
    cells = rec["cells"]
    seeds = sorted(c["seed"] for c in cells)
    if seeds != sorted(GRADED_SEEDS):
        sys.exit(f"REFUSED: graded seeds {seeds} != prereg {sorted(GRADED_SEEDS)}.")
    if any(c.get("mode") != "nrsionna_beam" for c in cells):
        sys.exit("REFUSED: sealed grading requires mode nrsionna_beam.")
    print(f"XPROTO-BEAM graded — sealed {seal_date}, seeds {GRADED_SEEDS}", flush=True)
    out = report(cells, "XPROTO-BEAM")
    out.update({"cell": "XPROTO-BEAM", "sealed": str(seal_date), "seeds": GRADED_SEEDS})
    json.dump(out, open(os.path.join(HERE, "XPROTO-BEAM-graded.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
