"""Grades OP1's sealed run (PREREG-OP1-RUN-DRAFT.md Sections 2, 4, 5 and 7): the regime check, OP1's bars, READ-KE's test.
Usage: python op1_run_grade.py <results.json> --tols tolerances.json [--out grade.json]
       python op1_run_grade.py --selftest

Input. The merged file of submit_op1_nrp.py --collect (<role>.json, the pilot's format, READ_KE in every cell).

Regime check (Section 4), before any bar. A world's number is PERSIST's graded value E (the mean over the horizons of
min(e_h, cap)) averaged over the two cutoffs; PERSIST does not depend on the lift, and a file where it differs between lifts
is refused. At each viscosity with both resolutions present the check fails when the larger number exceeds 1.5 times the
smaller, and then both worlds of that viscosity are reported and not graded, so N1 is not graded there. If both viscosities
fail, OP1 is reported as unable to test its claim on the run worlds. A world that is missing or refused by the stability
guard is reported and not graded (Section 7); its partner cannot be checked, is graded, and is recorded as unchecked.

Primary claim (Section 2): op1_grade.grade, unchanged, on the worlds the check keeps, with the registered tolerances.

READ-KE (Section 5): over the graded cells of the kept worlds, READ-KE against the better of ENERGY and BALL (lower E is
ahead), a one-sided sign test with ties dropped: p = P(Binomial(n, 1/2) >= ahead), n the untied cells, beats the control at
p <= 0.05, no correction. A cell without READ_KE is dropped from the test and listed. READ-KE's pooled advantage, and its
standing against READ cell by cell, are reported beside the test, untested. A file of any role but "run" is labelled as not a
verdict, and only a run file is held to the registered tolerances.
"""
from __future__ import annotations

import copy
import json
import math
import sys
from pathlib import Path

import numpy as np

from op1_grade import cells as op1_cells, grade as op1_grade_fn

RATIO = 1.5
ALPHA = 0.05
REGISTERED_TOLS = {"M1": 0.01, "TOL1": 0.25, "TOL_N": 0.05}  # tolerances.json at 321cb46 (Section 1)


def persist_number(w: dict) -> float:
    """PERSIST's E averaged over the cutoffs; refuses a world whose PERSIST differs between lifts."""
    per_kc = []
    for kc, c in w["cutoffs"].items():
        es = {lift: L["PERSIST"]["E"] for lift, L in c["lifts"].items()}
        if len(set(es.values())) != 1: raise SystemExit(f"{w['name']} k_c {kc}: PERSIST differs between lifts {es}")
        per_kc.append(next(iter(es.values())))
    return float(np.mean(per_kc))


def regime_check(res: dict, expected: list[str]) -> dict:
    """Section 4: per viscosity, the two resolutions' PERSIST numbers and whether their ratio passes; the worlds removed."""
    present = {w["name"]: w for w in res["worlds"]}
    missing = [n for n in expected if n not in present]
    refused = sorted(n for n, w in present.items() if w.get("refused"))
    usable = [w for w in res["worlds"] if not w.get("refused")]
    by_nu, removed = {}, []
    for nu in sorted({w["nu"] for w in usable}):
        ws = sorted((w for w in usable if w["nu"] == nu), key=lambda w: w["n"])
        if len(ws) > 2: raise SystemExit(f"nu {nu}: {len(ws)} resolutions; the check is defined for a pair")
        nums = {w["name"]: persist_number(w) for w in ws}
        if len(ws) < 2:
            by_nu[str(nu)] = {"persist": nums, "ratio": None, "passes": None, "note": "pair incomplete: not checked, graded"}
            continue
        lo, hi = min(nums.values()), max(nums.values()); fails = hi > RATIO * lo
        by_nu[str(nu)] = {"persist": nums, "ratio": hi / lo, "passes": not fails}
        if fails: removed += [w["name"] for w in ws]
    kept = [w["name"] for w in usable if w["name"] not in removed]
    failed = [nu for nu, v in by_nu.items() if v["passes"] is False]
    return {"limit": RATIO, "by_nu": by_nu, "removed": removed, "missing": missing, "refused": refused, "kept": kept,
            "unable_to_test": len(failed) >= 2 or bool(failed and not kept)}


def sign_test(ahead: int, behind: int) -> float:
    n = ahead + behind
    if n == 0: return 1.0
    return sum(math.comb(n, k) for k in range(ahead, n + 1)) / 2 ** n


def threshold(n: int, alpha: float = ALPHA) -> int:
    """The fewest cells ahead, of n untied, with p <= alpha."""
    return next(k for k in range(n + 2) if k > n or sign_test(k, n - k) <= alpha)


def read_ke_test(res: dict) -> dict:
    """Section 5 on the graded cells of `res` (already reduced to the kept worlds)."""
    graded = res.get("config", {}).get("graded_lifts"); rows, dropped = [], []
    lookup = {w["name"]: w for w in res["worlds"]}
    for c in op1_cells(res):
        x = lookup[c["world"]]["cutoffs"][c["kc"]]["lifts"][c["lift"]][str(c["r"])]
        tag = f"{c['world']}/kc{c['kc']}/{c['lift']}/r{c['r']}"
        if not x.get("READ_KE"): dropped.append(tag); continue
        rows.append({"cell": tag, "E": x["READ_KE"]["E"], "ctrl": c["ctrl"], "READ": c["READ"]})
    ahead = sum(r["E"] < r["ctrl"] for r in rows); behind = sum(r["E"] > r["ctrl"] for r in rows); tied = len(rows) - ahead - behind
    p = sign_test(ahead, behind) if rows else None
    adv = [(r["ctrl"] - r["E"]) / r["ctrl"] if r["ctrl"] > 0 else 0.0 for r in rows]
    vr = [(r["READ"] - r["E"]) / r["READ"] if r["READ"] > 0 else 0.0 for r in rows]
    return {"graded_lifts": graded, "cells": len(rows), "dropped_no_read_ke": dropped, "ahead": ahead, "behind": behind, "tied": tied,
            "untied": ahead + behind, "needed": threshold(ahead + behind) if rows else None, "p_one_sided": p, "alpha": ALPHA,
            "beats": p is not None and p <= ALPHA,
            "pooled_advantage": float(np.mean(adv)) if adv else None,
            "vs_read": {"ahead": sum(r["E"] < r["READ"] for r in rows), "behind": sum(r["E"] > r["READ"] for r in rows),
                        "tied": sum(r["E"] == r["READ"] for r in rows), "pooled_relative": float(np.mean(vr)) if vr else None},
            "per_cell": {r["cell"]: {"READ_KE": r["E"], "ctrl": r["ctrl"], "READ": r["READ"]} for r in rows}}


def grade(res: dict, tols: dict) -> dict:
    role = res.get("seed_role", "run")
    label = (lambda s: s) if role == "run" else (lambda s: f"{role.upper()} GRADE, NOT A VERDICT: {s}")
    if role == "run":
        got = {k: float(tols[k]) for k in REGISTERED_TOLS}
        if got != REGISTERED_TOLS: raise SystemExit(f"run tolerances {got} are not the registered {REGISTERED_TOLS}")
    group = res.get("config", {}).get("groups_by_role", {}).get(role, [role])
    expected = [w["name"] for w in res.get("config", {}).get("worlds", []) if w.get("group") in group]
    rc = regime_check(res, expected)
    out = {"seed_role": role, "read_ke_in_file": bool(res.get("read_ke")), "regime_check": rc}
    if rc["unable_to_test"]:
        out["op1"] = {"gate": label("UNABLE TO TEST: the regime check failed at both viscosities")}
        out["read_ke"] = {"beats_control": label("UNABLE TO TEST: the regime check failed at both viscosities")}
        return out
    if not rc["kept"]:
        out["op1"] = {"gate": label("NO WORLDS GRADED")}; out["read_ke"] = {"beats_control": label("NO WORLDS GRADED")}
        return out
    kept = copy.deepcopy(res); kept["worlds"] = [w for w in res["worlds"] if w["name"] in rc["kept"]]
    g = op1_grade_fn(kept, tols); g["gate"] = label(g["gate"]); out["op1"] = g
    t = read_ke_test(kept); t["beats_control"] = label("BEATS THE CONTROL" if t.pop("beats") else "does not beat the control")
    out["read_ke"] = t
    return out


# ---------------------------------------------------------------- self-test on synthetic results

LADDER = [2, 4, 8, 16, 32]


def _world(name, nu, n, read=0.54, read_ke=0.55, persist=(0.3, 0.3), ke=None, lifts=("rff", "tend")):
    """One world with cutoffs 3 and 5; ENERGY 0.6 and BALL 0.7 everywhere. `ke`, if given, maps (kc, lift, r) -> READ_KE's E
    (None drops the arm from that cell)."""
    cut = {}
    for kc, pe in zip(("3", "5"), persist):
        L = {}
        for lift in lifts:
            cl = {"NONE": {"E": 1.0}, "PERSIST": {"E": pe}}
            for r in LADDER:
                e_ke = ke.get((kc, lift, r), read_ke) if ke is not None else read_ke
                cl[str(r)] = {"READ": {"E": read}, "ENERGY": {"E": 0.6}, "BALL": {"E": 0.7}, "SENS": {"E": 0.65}, "RANDOM_median_E": 0.8}
                if e_ke is not None: cl[str(r)]["READ_KE"] = {"E": e_ke}
            L[lift] = cl
        cut[kc] = {"ladder": LADDER, "lifts": L}
    return {"name": name, "nu": nu, "n": n, "cutoffs": cut}


def _file(worlds, role="run"):
    cfg_worlds = [{"name": w["name"], "group": role} for w in worlds]
    return {"seed_role": role, "read_ke": True, "config": {"graded_lifts": ["rff", "tend"], "groups_by_role": {role: [role]}, "worlds": cfg_worlds},
            "worlds": worlds}


def selftest() -> int:
    fails = 0; tols = dict(REGISTERED_TOLS)

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"{label}: {detail}", "PASS" if ok else "FAIL"); fails += 0 if ok else 1

    # Section 5's thresholds: 48 of 80 untied p = 0.0465, 47 of 80 p = 0.0728
    check("sign test 48/80 and 47/80", abs(sign_test(48, 32) - 0.0465) < 5e-5 and abs(sign_test(47, 33) - 0.0728) < 5e-5 and threshold(80) == 48,
          f"{sign_test(48, 32):.4f} {sign_test(47, 33):.4f}, threshold {threshold(80)}")
    four = lambda **kw: [_world("a30", 0.03, 128, **kw.get("a30", {})), _world("b30", 0.03, 192, **kw.get("b30", {})),
                         _world("a20", 0.02, 128, **kw.get("a20", {})), _world("b20", 0.02, 192, **kw.get("b20", {}))]
    g = grade(_file(four()), tols)
    check("four worlds pass the check: 80 cells, both viscosities in N1", g["regime_check"]["removed"] == [] and g["op1"]["n_cells"] == 80
          and set(g["op1"]["bars"]["N1"]["by_nu"]) == {"0.02", "0.03"}, f"{g['op1']['n_cells']} cells, gate {g['op1']['gate']}")
    # the quantity: the mean over cutoffs. Cutoff by cutoff the ratios are 2.0 and 1.33, the means 0.25 and 0.375 give 1.5
    # exactly (binary fractions, no rounding): kept, since only a ratio above 1.5 fails
    g = grade(_file(four(a30={"persist": (0.125, 0.375)}, b30={"persist": (0.25, 0.5)})), tols)
    check("the check reads the mean over the cutoffs (ratio 1.5 exactly is kept)", g["regime_check"]["by_nu"]["0.03"]["passes"] and g["regime_check"]["by_nu"]["0.03"]["ratio"] == 1.5,
          repr(g["regime_check"]["by_nu"]["0.03"]["ratio"]))
    g = grade(_file(four(a30={"persist": (0.2, 0.2)}, b30={"persist": (0.31, 0.31)})), tols); rc = g["regime_check"]
    check("ratio 1.55 removes both worlds of that viscosity, either way round", rc["removed"] == ["a30", "b30"] and rc["kept"] == ["a20", "b20"], str(rc["removed"]))
    check("then N1 is graded at the other viscosity only, on 40 cells", set(g["op1"]["bars"]["N1"]["by_nu"]) == {"0.02"} and g["op1"]["n_cells"] == 40,
          str(g["op1"]["bars"]["N1"]["by_nu"].keys()))
    g2 = grade(_file(four(a30={"persist": (0.31, 0.31)}, b30={"persist": (0.2, 0.2)})), tols)
    check("the ratio is symmetric", g2["regime_check"]["removed"] == ["a30", "b30"], str(g2["regime_check"]["by_nu"]["0.03"]["ratio"]))
    kept = _file(four()); kept["worlds"] = kept["worlds"][2:]
    check("op1_grade is called unchanged on the kept worlds", json.dumps(g["op1"], sort_keys=True) == json.dumps(op1_grade_fn(kept, tols), sort_keys=True))
    g = grade(_file(four(a30={"persist": (0.2, 0.2)}, b30={"persist": (0.4, 0.4)}, a20={"persist": (0.4, 0.4)}, b20={"persist": (0.2, 0.2)})), tols)
    check("both viscosities fail: unable to test", g["op1"]["gate"].startswith("UNABLE TO TEST") and g["read_ke"]["beats_control"].startswith("UNABLE TO TEST"), g["op1"]["gate"])
    ws = four(); del ws[1]; g = grade(_file(four()) | {"worlds": ws}, tols); rc = g["regime_check"]
    check("a missing world is reported; its partner is graded unchecked and N1 skips that viscosity",
          rc["missing"] == ["b30"] and rc["by_nu"]["0.03"]["passes"] is None and "a30" in rc["kept"] and set(g["op1"]["bars"]["N1"]["by_nu"]) == {"0.02"}, str(rc["by_nu"]["0.03"]))
    ws = four(); ws[3] = {"name": "b20", "nu": 0.02, "n": 192, "refused": "unstable"}; rc = grade(_file(four()) | {"worlds": ws}, tols)["regime_check"]
    check("a refused world is reported and not graded", rc["refused"] == ["b20"] and "b20" not in rc["kept"] and rc["by_nu"]["0.02"]["passes"] is None, str(rc["refused"]))
    w = _world("x", 0.03, 128); w["cutoffs"]["3"]["lifts"]["tend"]["PERSIST"]["E"] = 0.31
    try: persist_number(w); ok = False
    except SystemExit: ok = True
    check("PERSIST differing between lifts is refused", ok)
    # READ-KE: 48 of 80 ahead of the control (0.55 < 0.6), 31 behind (0.65), 1 tied (0.6): 79 untied, needs 48 (p 0.0347)
    cells = [(kc, lift, r) for kc in ("3", "5") for lift in ("rff", "tend") for r in LADDER]
    vals = iter([0.55] * 48 + [0.65] * 31 + [0.6])
    ke = {}
    for wn in ("a30", "b30", "a20", "b20"): ke[wn] = {c: next(vals) for c in cells}
    t = grade(_file(four(**{wn: {"ke": ke[wn]} for wn in ke})), tols)["read_ke"]
    check("READ-KE 48 ahead, 31 behind, 1 tie dropped: beats the control", (t["ahead"], t["behind"], t["tied"], t["needed"]) == (48, 31, 1, 48)
          and t["beats_control"] == "BEATS THE CONTROL", f"p {t['p_one_sided']:.4f}")
    vals = iter([0.55] * 47 + [0.65] * 33); ke = {wn: {c: next(vals) for c in cells} for wn in ("a30", "b30", "a20", "b20")}
    t = grade(_file(four(**{wn: {"ke": ke[wn]} for wn in ke})), tols)["read_ke"]
    check("READ-KE 47 of 80: does not beat the control", t["ahead"] == 47 and t["beats_control"] == "does not beat the control", f"p {t['p_one_sided']:.4f}")
    check("READ-KE against READ (0.54) reported: behind in every cell", t["vs_read"]["behind"] == 80, str(t["vs_read"]))
    t = grade(_file(four(a30={"ke": {("3", "rff", 2): None}})), tols)["read_ke"]
    check("a cell without READ-KE is dropped and listed", t["cells"] == 79 and t["dropped_no_read_ke"] == ["a30/kc3/rff/r2"], str(t["dropped_no_read_ke"]))
    t = grade(_file([_world(w, 0.03, 128, lifts=("lin", "rff", "tend")) for w in ("a",)]), tols)["read_ke"]
    check("the ungraded lift LIN is not in the test", t["cells"] == 20, str(t["cells"]))
    g = grade(_file([_world("s", 0.03, 64)], role="smoke"), {"M1": 0.5, "TOL1": 1.0, "TOL_N": 0.5})
    check("a smoke file is labelled not a verdict, and is not held to the registered tolerances", g["op1"]["gate"].startswith("SMOKE GRADE, NOT A VERDICT")
          and g["read_ke"]["beats_control"].startswith("SMOKE GRADE, NOT A VERDICT"), g["op1"]["gate"])
    try: grade(_file(four()), {"M1": 0.02, "TOL1": 0.25, "TOL_N": 0.05}); ok = False
    except SystemExit: ok = True
    check("a run file with other tolerances is refused", ok)
    pilot = Path(__file__).with_name("pilot.json")
    if pilot.exists():
        rc = regime_check(json.loads(pilot.read_text(encoding="utf-8")), [])
        r30, r20 = rc["by_nu"]["0.03"]["ratio"], rc["by_nu"]["0.02"]["ratio"]
        check("on the pilot's worlds the check removes nu 0.03 (the case it was fixed from) and keeps nu 0.02",
              rc["removed"] == ["p_nu030_n96", "p_nu030_n128"] and 1.0 < r20 < 1.5 < r30, f"ratios {r30:.3f} and {r20:.3f}")
    else:
        check("pilot.json present for the real-data check", False)
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv: return 1 if selftest() else 0
    tols = json.load(open(argv[argv.index("--tols") + 1], encoding="utf-8-sig"))
    g = grade(json.load(open(argv[0], encoding="utf-8")), tols); text = json.dumps(g, indent=1, default=float)
    if "--out" in argv: open(argv[argv.index("--out") + 1], "w", encoding="utf-8").write(text + "\n")
    print(text); return 0


if __name__ == "__main__":
    sys.exit(main())
