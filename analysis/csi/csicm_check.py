"""XPROTO-CSI-CM graded checker -- bars per PREREG-XPROTO-CSI-CM.md.

Coded cooling-off (seal date AND wall-clock date), real-NR-substrate guard, seed
disjointness guard, cost-match residual guard, and the kept-negative rule: a
cost-matched sign death is FAIL and is reported, never discarded.

    python3 csicm_check.py                     # sealed grading
    python3 csicm_check.py --smoke-record CSICMREP-shakedown.json

Verdicts: PASS (exit 0), FAIL (exit 1), VOID (exit 2). VOID is reserved for
manipulation-check failure or seed collision.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-CSI-CM.md")
GRADED_RECORD = os.path.join(HERE, "CSICMREP-graded-raw.json")
OUT_RECORD = os.path.join(HERE, "XPROTO-CSI-CM-graded.json")

# ---- constants restated from the prereg; the line citation is the authority ----
FAMILY_CONSTRUCTED = date(2026, 8, 28)      # prereg line 3
GRADED_SEEDS = [20260906, 20260907, 20260908]   # prereg lines 4-5, 66
SHAKEDOWN_SEEDS = [0, 1, 2]                 # prereg lines 5, 92
# The fleets are shared with F-CSI-GRAD, so that cell's calibration seeds are
# forbidden here too (PREREG-XPROTO-CSI-GRAD.md line 52).
SIBLING_CAL_SEEDS = [990, 991, 992, 993, 994]
MODE = "nrsionna"                           # prereg line 6

LAMBDA_SHIFT_TOL = 0.10                     # prereg line 70 (B2)
D_RMS_FLOOR_DB = 0.5                        # prereg line 78 (MC2)
COST_RTOL = 1e-9                            # prereg line 79 (MC3), line 61
S_LO, S_HI = 0.25, 4.0                      # prereg line 60 (solver bracket)
N_BISECT = 200                              # prereg line 61
S_REGISTERED = 1.24128                      # prereg line 63 (fleet constant)
S_ATOL = 1e-4


def require_seal() -> date:
    today = date.today()
    if today <= FAMILY_CONSTRUCTED:
        sys.exit(f"REFUSED: cooling-off -- today {today} is not strictly after "
                 f"family construction {FAMILY_CONSTRUCTED}.")
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: DRAFT" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-CSI-CM.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off -- seal {d} not >= 1 day after "
                 f"{FAMILY_CONSTRUCTED}.")
    if d > today:
        sys.exit(f"REFUSED: seal date {d} is in the future (today {today}).")
    return d


def seed_disjointness(seeds, allow_shakedown=False):
    """VOID condition: a graded seed that also served shakedown or the
    sibling GRAD calibration. allow_shakedown is for the checker's own
    smoke test only; it is never set on the sealed grading path."""
    forbidden = set(SIBLING_CAL_SEEDS)
    if not allow_shakedown:
        forbidden |= set(SHAKEDOWN_SEEDS)
    return sorted(set(seeds) & forbidden)


def solver_guard(rec):
    c = rec.get("constants", {})
    return {
        "cost_rtol_declared": abs(float(c.get("cost_rtol", -1)) - COST_RTOL) < 1e-18,
        "lambda_shift_tol_declared": abs(float(c.get("lambda_shift_tol", -1))
                                         - LAMBDA_SHIFT_TOL) < 1e-12,
        "rebalanced_policy_B": str(c.get("rebalanced_policy", "")).startswith("B"),
        "solver_bracket": (f"[{S_LO},{S_HI}]" in str(c.get("solver", "")) and
                           str(N_BISECT) in str(c.get("solver", ""))),
    }


def sign(x):
    return 0 if x == 0 else (1 if x > 0 else -1)


def grade_cell(c):
    shift = c.get("lambda_shift")
    return {
        # B1 (prereg line 68): signs survive cost matching and match the
        # nominal pair in the same run.
        "B1_signs_survive": bool(
            c["dR_M_cm"] < 0 < c["dR_S_cm"] and
            sign(c["dR_M_cm"]) == sign(c["dR_M_nom"]) != 0 and
            sign(c["dR_S_cm"]) == sign(c["dR_S_nom"]) != 0),
        # B2 (prereg line 70): lambda* stability under the declared tolerance.
        "B2_lambda_shift": bool(shift is not None and shift <= LAMBDA_SHIFT_TOL),
        "MC1_sane": all(0.0 < c[k] < 1.0 for k in
                        ("fc_M_A", "fc_S_A", "fc_M_B_cm", "fc_S_B_cm")),
        "MC2_policies_differ": c["d_rms_cm_db"] >= D_RMS_FLOOR_DB,
        "MC3_cost_matched": float(c["cost_match_resid_rel"]) <= COST_RTOL,
        "MC4_nominal_flip_holds": bool(c["flip_nom"]),
    }


def report(rec, label, smoke):
    cells = rec["cells"]
    if rec.get("mode") != MODE or any(c.get("mode", MODE) != MODE for c in cells):
        sys.exit(f"REFUSED: grading requires the real NR substrate (mode {MODE}).")
    sg = solver_guard(rec)
    collisions = seed_disjointness([c["seed"] for c in cells],
                                   allow_shakedown=smoke)
    graded = [{**c, "grade": grade_cell(c)} for c in cells]
    keys = ("B1_signs_survive", "B2_lambda_shift", "MC1_sane",
            "MC2_policies_differ", "MC3_cost_matched", "MC4_nominal_flip_holds")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}

    print(f"declared tolerances: cost residual <= {COST_RTOL}, "
          f"|lambda* shift| <= {LAMBDA_SHIFT_TOL}, RMS(d) >= {D_RMS_FLOOR_DB} dB",
          flush=True)
    for k, v in sg.items():
        print(f"  solver guard {k}: {'ok' if v else 'MISMATCH'}", flush=True)
    print(f"  seed collisions with shakedown/sibling calibration: "
          f"{collisions if collisions else 'none'}", flush=True)
    # Advisory only: the prereg registers s as one seed-independent fleet
    # constant (line 63). A departure is informative, not a verdict input.
    for c in cells:
        if abs(float(c["s_rebalance"]) - S_REGISTERED) > S_ATOL:
            print(f"  ADVISORY seed {c['seed']}: s={c['s_rebalance']} departs from "
                  f"the registered fleet constant {S_REGISTERED} (advisory only)",
                  flush=True)

    for g in graded:
        gr = g["grade"]
        print(f"  seed {g['seed']}: s={g['s_rebalance']} "
              f"cost_A={g['cost_A_se']} cost_B_nom={g['cost_B_nominal_se']} "
              f"gap={g['cost_gap_nominal_rel']} resid={g['cost_match_resid_rel']:.3e} "
              f"| mean margin B_cm={g['mean_margin_B_cm_db']} dB "
              f"d_rms={g['d_rms_cm_db']} dB", flush=True)
        print(f"          nom dR_M={g['dR_M_nom']} dR_S={g['dR_S_nom']} "
              f"lam*={g['lambda_star_nom']} | cm dR_M={g['dR_M_cm']} "
              f"dR_S={g['dR_S_cm']} lam*={g['lambda_star_cm']} "
              f"| shift={g['lambda_shift']} -> "
              + " ".join(f"{k.split('_')[0]}:{'ok' if gr[k] else 'X'}"
                         for k in keys), flush=True)

    mcs_ok = (agg["MC1_sane"] and agg["MC2_policies_differ"] and
              agg["MC3_cost_matched"] and agg["MC4_nominal_flip_holds"] and
              all(sg.values()) and not collisions)
    bars_ok = agg["B1_signs_survive"] and agg["B2_lambda_shift"]
    verdict = "VOID" if not mcs_ok else ("PASS" if bars_ok else "FAIL")
    print(f"{label}: {verdict} (B1 {agg['B1_signs_survive']}, B2 "
          f"{agg['B2_lambda_shift']}; MCs {mcs_ok})", flush=True)
    if verdict == "FAIL":
        print("KEPT NEGATIVE: the reversal did not survive exact cost matching. "
              "Per the prereg this is a reportable result, not a discard.",
              flush=True)
    if smoke:
        print("CHECKER SMOKE TEST -- shakedown input, NOT EVIDENCE. No record "
              "written.", flush=True)
    return {"cells": graded, "aggregate": agg, "solver_guard": sg,
            "seed_collisions": collisions, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-record")
    args = ap.parse_args()

    if args.smoke_record:
        path = args.smoke_record
        if not os.path.isabs(path):
            path = os.path.join(HERE, path)
        rec = json.load(open(path, encoding="utf-8"))
        print(f"XPROTO-CSI-CM checker smoke test on {os.path.basename(path)}",
              flush=True)
        out = report(rec, "smoke (checker logic only)", smoke=True)
        sys.exit(0 if out["verdict"] == "PASS" else
                 (2 if out["verdict"] == "VOID" else 1))

    seal_date = require_seal()
    if not os.path.exists(GRADED_RECORD):
        sys.exit("REFUSED: CSICMREP-graded-raw.json missing -- run fam_csicm.py "
                 "--graded --seeds 20260906 20260907 20260908 on Atlas first.")
    rec = json.load(open(GRADED_RECORD, encoding="utf-8"))
    if rec.get("phase") != "graded":
        sys.exit("REFUSED: record is not a graded-phase record.")
    if sorted(c["seed"] for c in rec["cells"]) != sorted(GRADED_SEEDS):
        sys.exit("REFUSED: graded seeds mismatch prereg.")
    print(f"XPROTO-CSI-CM graded -- sealed {seal_date}, seeds {GRADED_SEEDS}",
          flush=True)
    out = report(rec, "XPROTO-CSI-CM", smoke=False)
    out.update({"cell": "XPROTO-CSI-CM", "sealed": str(seal_date),
                "seeds": GRADED_SEEDS, "checked_on": str(date.today())})
    json.dump(out, open(OUT_RECORD, "w"), indent=1)
    print(f"wrote {OUT_RECORD}", flush=True)
    sys.exit(0 if out["verdict"] == "PASS" else
             (2 if out["verdict"] == "VOID" else 1))


if __name__ == "__main__":
    main()
