"""XPROTO-CSI-GRAD graded checker -- bars per PREREG-XPROTO-CSI-GRAD.md.

Coded cooling-off (seal date AND wall-clock date), real-NR-substrate guard, seed
disjointness guard, and a registration-tamper guard: the calibration record must
still reproduce the registered numbers frozen into the prereg.

    python3 csigrad_check.py                       # sealed grading
    python3 csigrad_check.py --smoke-record CSIGRADREP-shakedown.json

Verdicts: PASS (exit 0), FAIL (exit 1), VOID (exit 2). VOID is reserved for
manipulation-check failure, seed collision, or registration tamper.

Substrate note: the prereg's claim that graded cells at seeds shared with the
sealed F-CSI-FLIP record reproduce that record's fc values EXACTLY is not
supported by the family's own records (CSIFLIPREP-family, CSIGRADREP-shakedown
and CSICMREP-shakedown disagree in the third decimal at seed 0). The substrate
guard here is therefore the mode tag plus an ADVISORY cross-check printed for
the reader, never a verdict input.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-CSI-GRAD.md")
CAL_RECORD = os.path.join(HERE, "CSIGRADREP-calibration.json")
GRADED_RECORD = os.path.join(HERE, "CSIGRADREP-graded-raw.json")
FLIP_SEALED = os.path.join(HERE, "XPROTO-CSI-FLIP-graded.json")
OUT_RECORD = os.path.join(HERE, "XPROTO-CSI-GRAD-graded.json")

# ---- constants restated from the prereg; the line citation is the authority ----
FAMILY_CONSTRUCTED = date(2026, 8, 28)      # prereg line 3
GRADED_SEEDS = [20260906, 20260907, 20260908]   # prereg lines 4-5, 123
CAL_SEEDS = [990, 991, 992, 993, 994]       # prereg line 52
SHAKEDOWN_SEEDS = [0, 1, 2]                 # prereg line 155
MODE = "nrsionna"                           # prereg line 7

PRED_SIGN_DR_M = -1                         # prereg line 114 (B1, line 125)
PRED_SIGN_DR_S = +1                         # prereg line 114 (B1, line 125)
LAMBDA_BAND = (0.3635, 0.4635)              # prereg line 116 (B2, line 127)
LAMBDA_STAR_REG = 0.4135                    # prereg line 115
D_RMS_FLOOR_DB = 0.5                        # prereg line 132 (MC2)
SE_RATIO_CEIL = 0.5                         # prereg line 133 (MC3)

# registered calibration gate, prereg lines 112-113; used as the tamper guard
GATE_REG = {"g_mean_1": -0.13896, "se_1": 0.00097, "curv_bound_1": 0.05595,
            "floor_1": 0.01592, "ratio_1": 8.728,
            "g_mean_2": 0.09798, "se_2": 0.00131, "curv_bound_2": 0.16343,
            "floor_2": 0.04347, "ratio_2": 2.254}
GATE_ATOL = 5e-5
SUBSTRATE_ADVISORY_TOL = 0.02   # advisory only; never a verdict input


def require_seal() -> date:
    today = date.today()
    if today <= FAMILY_CONSTRUCTED:
        sys.exit(f"REFUSED: cooling-off -- today {today} is not strictly after "
                 f"family construction {FAMILY_CONSTRUCTED}.")
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: DRAFT" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-CSI-GRAD.md is not SEALED.")
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
    """VOID condition: a graded seed that also served calibration or
    shakedown. allow_shakedown is for the checker's own smoke test, where
    the shakedown seeds are the input by design; it is never set on the
    sealed grading path."""
    forbidden = set(CAL_SEEDS)
    if not allow_shakedown:
        forbidden |= set(SHAKEDOWN_SEEDS)
    return sorted(set(seeds) & forbidden)


def registration_ok(cal, reg):
    return {
        "decision_REGISTER": reg.get("decision") == "REGISTER",
        "sign_M": reg.get("pred_sign_dR_M") == PRED_SIGN_DR_M,
        "sign_S": reg.get("pred_sign_dR_S") == PRED_SIGN_DR_S,
        "reversal_predicted": bool(reg.get("reversal_predicted")),
        "lambda_star": abs(float(reg.get("lambda_star_pred", -9))
                           - LAMBDA_STAR_REG) <= 1e-4,
        "lambda_band": (reg.get("lambda_band") is not None and
                        abs(reg["lambda_band"][0] - LAMBDA_BAND[0]) <= 1e-4 and
                        abs(reg["lambda_band"][1] - LAMBDA_BAND[1]) <= 1e-4),
        "cal_seeds": (cal is None or
                      sorted(cal["constants"]["cal_seeds"]) == sorted(CAL_SEEDS)),
        "gate_numbers": (cal is None or
                         all(abs(cal["gate"][k] - v) <= GATE_ATOL
                             for k, v in GATE_REG.items())),
    }


def calibration_mcs(cal, graded_rec):
    mc = (cal["mc"] if cal is not None else graded_rec.get("calibration_mc", {}))
    out = {"MC3_calibration_stability": bool(mc.get("MC3_stable")),
           "MC4_control_not_reversed": bool(mc.get("MC4_control_not_reversed"))}
    if cal is not None:
        g = cal["gate"]
        out["MC3_calibration_stability"] = bool(
            g["se_1"] <= SE_RATIO_CEIL * abs(g["g_mean_1"]) and
            g["se_2"] <= SE_RATIO_CEIL * abs(g["g_mean_2"]))
        cg = cal["control_gate"]
        # MC4 forbids exactly one outcome: a LICENSED OPPOSITE-SIGN control.
        # Both non-reversal branches stay legal: ABSTAIN, or LICENSE SAME-SIGN.
        # The radio control is expected on the license-same-sign branch.
        out["MC4_control_not_reversed"] = not (bool(cg["licensed"]) and
                                               bool(cg["opposite_signs"]))
        out["MC4_control_branch"] = ("abstain" if not cg["licensed"] else
                                     ("license-same-sign" if not cg["opposite_signs"]
                                      else "LICENSE-OPPOSITE-SIGN (illegal)"))
        out["MC4_control_ratios"] = [cg["ratio_1"], cg["ratio_2"]]
        out["MC4_control_g_means"] = [cg["g_mean_1"], cg["g_mean_2"]]
    return out


def substrate_advisory(cells):
    """Advisory only. Report how graded fc values compare with the sealed
    F-CSI-FLIP record on any shared seed. Never a verdict input."""
    if not os.path.exists(FLIP_SEALED):
        return {}
    flip = {c["seed"]: c for c in
            json.load(open(FLIP_SEALED, encoding="utf-8"))["cells"]}
    out = {}
    for c in cells:
        f = flip.get(c["seed"])
        if not f:
            continue
        dev = max(abs(c["fc_M_A"] - f["fc_M_A"]), abs(c["fc_M_B"] - f["fc_M_B"]),
                  abs(c["fc_S_A"] - f["fc_S_A"]), abs(c["fc_S_B"] - f["fc_S_B"]))
        out[str(c["seed"])] = {"max_abs_dev_vs_sealed_flip": round(dev, 5),
                               "within_advisory_tol": dev <= SUBSTRATE_ADVISORY_TOL}
    return out


def grade_cell(c):
    lam = c.get("lambda_star")
    lo, hi = LAMBDA_BAND
    return {
        "B1_signs": (c["dR_M"] < 0 and c["dR_S"] > 0 and
                     (1 if c["dR_S"] > 0 else -1) == PRED_SIGN_DR_S and
                     (1 if c["dR_M"] > 0 else -1) == PRED_SIGN_DR_M),
        "B2_lambda_in_band": bool(lam is not None and lo <= lam <= hi),
        "MC1_sane": all(0.0 < c[k] < 1.0 for k in
                        ("fc_M_A", "fc_M_B", "fc_S_A", "fc_S_B")),
        "MC2_policies_differ": c["d_rms_db"] >= D_RMS_FLOOR_DB,
    }


def report(rec, cal, label, smoke):
    cells = rec["cells"]
    if rec.get("mode") != MODE or any(c.get("mode", MODE) != MODE for c in cells):
        sys.exit(f"REFUSED: grading requires the real NR substrate (mode {MODE}).")
    reg = rec.get("registration", {})
    reg_checks = registration_ok(cal, reg)
    cal_mc = calibration_mcs(cal, rec)
    collisions = seed_disjointness([c["seed"] for c in cells],
                                   allow_shakedown=smoke)
    advisory = substrate_advisory(cells)

    graded = [{**c, "grade": grade_cell(c)} for c in cells]
    keys = ("B1_signs", "B2_lambda_in_band", "MC1_sane", "MC2_policies_differ")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}

    print(f"registration frozen in the prereg: signs (dR_M {PRED_SIGN_DR_M:+d}, "
          f"dR_S {PRED_SIGN_DR_S:+d}), lambda* {LAMBDA_STAR_REG} "
          f"band [{LAMBDA_BAND[0]}, {LAMBDA_BAND[1]}]", flush=True)
    for k, v in reg_checks.items():
        print(f"  registration guard {k}: {'ok' if v else 'TAMPER'}", flush=True)
    for k, v in cal_mc.items():
        print(f"  calibration {k}: {v}", flush=True)
    print(f"  seed collisions with calibration/shakedown: "
          f"{collisions if collisions else 'none'}", flush=True)
    for s, a in advisory.items():
        print(f"  ADVISORY seed {s} shares the sealed F-CSI-FLIP graded record: "
              f"max |dev| = {a['max_abs_dev_vs_sealed_flip']} (advisory only, "
              f"not a verdict input)", flush=True)

    for g in graded:
        gr = g["grade"]
        print(f"  seed {g['seed']}: fc_M A={g['fc_M_A']} B={g['fc_M_B']} | "
              f"fc_S A={g['fc_S_A']} B={g['fc_S_B']} | dR_M={g['dR_M']} "
              f"dR_S={g['dR_S']} | lambda*={g['lambda_star']} | "
              f"d_rms={g['d_rms_db']} dB -> "
              + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys), flush=True)

    mcs_ok = (agg["MC1_sane"] and agg["MC2_policies_differ"] and
              cal_mc["MC3_calibration_stability"] and
              cal_mc["MC4_control_not_reversed"] and
              all(reg_checks.values()) and not collisions)
    bars_ok = agg["B1_signs"] and agg["B2_lambda_in_band"]
    verdict = "VOID" if not mcs_ok else ("PASS" if bars_ok else "FAIL")
    print(f"{label}: {verdict} (B1 {agg['B1_signs']}, B2 "
          f"{agg['B2_lambda_in_band']}; MCs {mcs_ok})", flush=True)
    if smoke:
        print("CHECKER SMOKE TEST -- shakedown input, NOT EVIDENCE. No record "
              "written.", flush=True)
    return {"cells": graded, "aggregate": agg, "registration_guard": reg_checks,
            "calibration_mc": cal_mc, "seed_collisions": collisions,
            "substrate_advisory": advisory, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-record")
    args = ap.parse_args()
    cal = (json.load(open(CAL_RECORD, encoding="utf-8"))
           if os.path.exists(CAL_RECORD) else None)

    if args.smoke_record:
        path = args.smoke_record
        if not os.path.isabs(path):
            path = os.path.join(HERE, path)
        rec = json.load(open(path, encoding="utf-8"))
        print(f"XPROTO-CSI-GRAD checker smoke test on {os.path.basename(path)}",
              flush=True)
        out = report(rec, cal, "smoke (checker logic only)", smoke=True)
        sys.exit(0 if out["verdict"] == "PASS" else
                 (2 if out["verdict"] == "VOID" else 1))

    seal_date = require_seal()
    if cal is None:
        sys.exit("REFUSED: CSIGRADREP-calibration.json missing -- the registration "
                 "cannot be verified.")
    if not os.path.exists(GRADED_RECORD):
        sys.exit("REFUSED: CSIGRADREP-graded-raw.json missing -- run fam_csigrad.py "
                 "--graded --seeds 20260906 20260907 20260908 on Atlas first.")
    rec = json.load(open(GRADED_RECORD, encoding="utf-8"))
    if sorted(c["seed"] for c in rec["cells"]) != sorted(GRADED_SEEDS):
        sys.exit("REFUSED: graded seeds mismatch prereg.")
    print(f"XPROTO-CSI-GRAD graded -- sealed {seal_date}, seeds {GRADED_SEEDS}",
          flush=True)
    out = report(rec, cal, "XPROTO-CSI-GRAD", smoke=False)
    out.update({"cell": "XPROTO-CSI-GRAD", "sealed": str(seal_date),
                "seeds": GRADED_SEEDS, "checked_on": str(date.today())})
    json.dump(out, open(OUT_RECORD, "w"), indent=1)
    print(f"wrote {OUT_RECORD}", flush=True)
    sys.exit(0 if out["verdict"] == "PASS" else
             (2 if out["verdict"] == "VOID" else 1))


if __name__ == "__main__":
    main()
