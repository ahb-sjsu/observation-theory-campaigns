"""Grades OP2's sealed run (PREREG-OP2-RUN-DRAFT.md Sections 2, 4, 5 and 7): OP1's regime check, OP2's bars, READ-KE's test.
Usage: python op2_run_grade.py <op2 results.json> --op1 <op1 results.json> --tols tolerances.json [--out grade.json]
       python op2_run_grade.py --selftest

Inputs. OP2's merged results (op2_mz.py on OP1's trajectory files, READ_KE in every cell) and OP1's merged results of the
same role (submit_op1_nrp.py --collect), which carry the persistence forecast the regime check reads. The two must share the
role and the seed, and every OP2 world must name the trajectory file of OP1's seed.

Regime check (Section 4): op1_run_grade.regime_check on OP1's results, unchanged. A world it removes is reported and not
graded in OP2 either, so OP2's N1 is not graded at that viscosity; if it fails at both viscosities, OP2 is reported as unable
to test its claim. A world with no OP2 result (its trajectory file missing) is reported and not graded (Section 7).

Cells (Section 7). A cell whose graded quantities (the shares of READ, ENERGY, BALL, SENS and every RANDOM draw, and E_min of
READ, ENERGY and BALL) are not all present and finite enters the record and is not graded; the count is reported.

Primary claim (Section 2): op2_grade.grade, unchanged, on the kept worlds and graded cells, with the registered tolerances.

READ-KE (Section 5): over the graded cells, READ-KE's memory share against the better (lower) of ENERGY's and BALL's, a
one-sided sign test with ties dropped: p = P(Binomial(n, 1/2) >= below), n the untied cells, beats the control at p <= 0.05,
no correction. A cell where READ-KE's share or E_min is absent or not finite is dropped from the test and listed. READ-KE's
pooled advantage, its standing against READ cell by cell, and its best error with memory against the control's (L1E's form)
are reported beside the test, untested. A file of any role but "run" is labelled as not a verdict, and only a run file is held
to the registered tolerances.
"""
from __future__ import annotations

import copy
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "OP1"))
from op1_run_grade import regime_check, sign_test, threshold  # noqa: E402
from op2_grade import grade as op2_grade_fn  # noqa: E402

ALPHA = 0.05
REGISTERED_TOLS = {"M1": 0.01, "TOL1": 0.25, "TOL_N": 0.05}  # tolerances.json at d2f087f (Section 1)


def _ok(cell: dict, arm: str, key: str) -> bool:
    v = cell.get(arm, {}).get(key) if isinstance(cell.get(arm), dict) else None
    return isinstance(v, (int, float)) and math.isfinite(v)


def gradable(cell: dict) -> bool:
    """Every quantity op2_grade reads is present and finite."""
    arms = ("READ", "ENERGY", "BALL", "SENS") + tuple(k for k in cell if k.startswith("RANDOM"))
    return (any(k.startswith("RANDOM") for k in cell) and all(_ok(cell, a, "share") for a in arms)
            and all(_ok(cell, a, "E_min") for a in ("READ", "ENERGY", "BALL")))


def read_ke_test(res: dict) -> dict:
    """Section 5 on the cells of `res` (already reduced to the kept worlds and graded cells)."""
    rows, dropped = [], []
    for w in res["worlds"]:
        for kc, c in w["cutoffs"].items():
            for r, cell in c["cells"].items():
                tag = f"{w['name']}/kc{kc}/r{r}"
                if not (_ok(cell, "READ_KE", "share") and _ok(cell, "READ_KE", "E_min")): dropped.append(tag); continue
                rows.append({"cell": tag, "s": cell["READ_KE"]["share"], "ctrl": min(cell["ENERGY"]["share"], cell["BALL"]["share"]), "READ": cell["READ"]["share"],
                             "e": cell["READ_KE"]["E_min"], "ectrl": min(cell["ENERGY"]["E_min"], cell["BALL"]["E_min"])})
    below = sum(r["s"] < r["ctrl"] for r in rows); above = sum(r["s"] > r["ctrl"] for r in rows); tied = len(rows) - below - above
    p = sign_test(below, above) if rows else None
    rel = lambda a, b: (b - a) / b if b > 0 else 0.0
    mean = lambda xs: float(np.mean(xs)) if xs else None
    return {"cells": len(rows), "dropped_no_read_ke": dropped, "below": below, "above": above, "tied": tied, "untied": below + above,
            "needed": threshold(below + above) if rows else None, "p_one_sided": p, "alpha": ALPHA, "beats": p is not None and p <= ALPHA,
            "pooled_advantage": mean([rel(r["s"], r["ctrl"]) for r in rows]),
            "vs_read": {"below": sum(r["s"] < r["READ"] for r in rows), "above": sum(r["s"] > r["READ"] for r in rows),
                        "tied": sum(r["s"] == r["READ"] for r in rows), "pooled_relative": mean([rel(r["s"], r["READ"]) for r in rows])},
            "pooled_E_advantage": mean([rel(r["e"], r["ectrl"]) for r in rows]),
            "per_cell": {r["cell"]: {"READ_KE": r["s"], "ctrl": r["ctrl"], "READ": r["READ"], "E_min": r["e"], "E_min_ctrl": r["ectrl"]} for r in rows}}


def grade(res: dict, op1: dict, tols: dict) -> dict:
    role = res.get("seed_role", "run")
    if op1.get("seed_role", role) != role: raise SystemExit(f"OP2 file is role {role}, OP1 file is {op1.get('seed_role')}")
    if res.get("seed") != op1.get("seed"): raise SystemExit(f"OP2 seed {res.get('seed')} is not OP1's {op1.get('seed')}")
    for w in res["worlds"]:
        want = f"{w['name']}_seed{op1.get('seed')}.npz"
        if w.get("trajectory_cache") != want: raise SystemExit(f"{w['name']}: trajectory {w.get('trajectory_cache')}, not OP1's {want}")
    label = (lambda s: s) if role == "run" else (lambda s: f"{role.upper()} GRADE, NOT A VERDICT: {s}")
    if role == "run":
        got = {k: float(tols[k]) for k in REGISTERED_TOLS}
        if got != REGISTERED_TOLS: raise SystemExit(f"run tolerances {got} are not the registered {REGISTERED_TOLS}")
    group = op1.get("config", {}).get("groups_by_role", {}).get(role, [role])
    rc = regime_check(op1, [w["name"] for w in op1.get("config", {}).get("worlds", []) if w.get("group") in group])
    group2 = res.get("config", {}).get("groups_by_role", {}).get(role, [role])
    expected2 = [w["name"] for w in res.get("config", {}).get("worlds", []) if w.get("group") in group2]
    have = {w["name"] for w in res["worlds"] if not w.get("refused")}
    out = {"seed_role": role, "read_ke_in_file": bool(res.get("read_ke")),
           "regime_check": {**rc, "op2_missing": sorted(n for n in set(expected2) | set(rc["kept"]) if n not in have)}}
    stop = "UNABLE TO TEST: OP1's regime check failed at both viscosities" if rc["unable_to_test"] else None
    kept = copy.deepcopy(res); kept["worlds"] = [w for w in kept["worlds"] if w["name"] in rc["kept"] and not w.get("refused")]
    not_graded = []
    for w in kept["worlds"]:
        for kc, c in w["cutoffs"].items():
            for r in list(c["cells"]):
                if not gradable(c["cells"][r]): not_graded.append(f"{w['name']}/kc{kc}/r{r}"); del c["cells"][r]
    out["cells_not_graded"] = {"count": len(not_graded), "cells": not_graded}
    if stop is None and not any(c["cells"] for w in kept["worlds"] for c in w["cutoffs"].values()): stop = "NO CELLS GRADED"
    if stop:
        out["op2"] = {"gate": label(stop)}; out["read_ke"] = {"beats_control": label(stop)}
        return out
    g = op2_grade_fn(kept, tols); g["gate"] = label(g["gate"]); out["op2"] = g
    t = read_ke_test(kept); t["beats_control"] = label("BEATS THE CONTROL" if t.pop("beats") else "does not beat the control")
    out["read_ke"] = t
    return out


# ---------------------------------------------------------------- self-test on synthetic results

LADDER = [2, 4, 8, 16, 32]


def _op2_world(name, nu, n, seed, read=0.50, read_ke=0.52, ke=None, bad=None):
    """ENERGY's share 0.60, BALL's 0.55 everywhere. `ke` maps (kc, r) -> READ-KE's share (None drops it); `bad` lists the
    (kc, r) cells whose BALL share is NaN."""
    cut = {}
    for kc in ("3", "5"):
        cells = {}
        for r in LADDER:
            s_ke = ke.get((kc, r), read_ke) if ke is not None else read_ke
            cell = {"READ": {"share": read, "E_min": 0.30}, "ENERGY": {"share": 0.60, "E_min": 0.30}, "BALL": {"share": 0.55, "E_min": 0.31},
                    "SENS": {"share": 0.58, "E_min": 0.30}, **{f"RANDOM{j}": {"share": 0.70, "E_min": 0.33} for j in range(3)}}
            if s_ke is not None: cell["READ_KE"] = {"share": s_ke, "E_min": 0.29}
            if bad and (kc, r) in bad: cell["BALL"]["share"] = float("nan")
            cells[str(r)] = cell
        cut[kc] = {"ladder": LADDER, "cells": cells}
    return {"name": name, "nu": nu, "n": n, "trajectory_cache": f"{name}_seed{seed}.npz", "cutoffs": cut}


def _op1_world(name, nu, n, persist):
    L = {lift: {"PERSIST": {"E": persist}} for lift in ("rff", "tend")}
    return {"name": name, "nu": nu, "n": n, "cutoffs": {"3": {"lifts": L}, "5": {"lifts": L}}}


NAMES = (("a30", 0.03, 128), ("b30", 0.03, 192), ("a20", 0.02, 128), ("b20", 0.02, 192))


def _files(op2_kw=None, persist=None, role="run", seed=7, drop2=()):
    op2_kw = op2_kw or {}; persist = persist or {}
    cfg = {"groups_by_role": {role: [role]}, "worlds": [{"name": nm, "group": role} for nm, _, _ in NAMES]}
    op2 = {"seed_role": role, "seed": seed, "read_ke": True, "config": cfg,
           "worlds": [_op2_world(nm, nu, n, seed, **op2_kw.get(nm, {})) for nm, nu, n in NAMES if nm not in drop2]}
    op1 = {"seed_role": role, "seed": seed, "config": cfg, "worlds": [_op1_world(nm, nu, n, persist.get(nm, 0.3)) for nm, nu, n in NAMES]}
    return op2, op1


def selftest() -> int:
    fails = 0; tols = dict(REGISTERED_TOLS)

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"{label}: {detail}", "PASS" if ok else "FAIL"); fails += 0 if ok else 1

    # Section 5's thresholds: 26 of 40 untied p = 0.0403, 25 of 40 p = 0.0769
    check("sign test 26/40 and 25/40", abs(sign_test(26, 14) - 0.0403) < 5e-5 and abs(sign_test(25, 15) - 0.0769) < 5e-5 and threshold(40) == 26,
          f"{sign_test(26, 14):.4f} {sign_test(25, 15):.4f}, threshold {threshold(40)}")
    g = grade(*_files(), tols)
    check("four worlds kept: 40 cells, N1 at both viscosities", g["op2"]["n_cells"] == 40 and set(g["op2"]["bars"]["N1"]["by_nu"]) == {"0.02", "0.03"},
          f"{g['op2']['n_cells']} cells, gate {g['op2']['gate']}")
    g = grade(*_files(persist={"a30": 0.2, "b30": 0.31}), tols)
    check("OP1's check failing at nu 0.03 removes both OP2 worlds there; N1 at nu 0.02 only, on 20 cells",
          g["regime_check"]["removed"] == ["a30", "b30"] and g["op2"]["n_cells"] == 20 and set(g["op2"]["bars"]["N1"]["by_nu"]) == {"0.02"}, str(g["regime_check"]["removed"]))
    op2, op1 = _files(); kept = copy.deepcopy(op2); kept["worlds"] = kept["worlds"][2:]
    check("op2_grade is called unchanged on the kept worlds", json.dumps(grade(*_files(persist={"a30": 0.2, "b30": 0.31}), tols)["op2"], sort_keys=True)
          == json.dumps(op2_grade_fn(kept, tols), sort_keys=True))
    g = grade(*_files(persist={"a30": 0.2, "b30": 0.4, "a20": 0.4, "b20": 0.2}), tols)
    check("both viscosities fail: unable to test", g["op2"]["gate"].startswith("UNABLE TO TEST") and g["read_ke"]["beats_control"].startswith("UNABLE TO TEST"), g["op2"]["gate"])
    g = grade(*_files(drop2=("b20",)), tols)
    check("a world with no OP2 result is reported, and N1 skips its viscosity", g["regime_check"]["op2_missing"] == ["b20"] and g["op2"]["n_cells"] == 30
          and set(g["op2"]["bars"]["N1"]["by_nu"]) == {"0.03"}, str(g["regime_check"]["op2_missing"]))
    g = grade(*_files({"a20": {"bad": [("3", 2), ("5", 32)]}}), tols)
    check("a cell with a non-finite share is recorded and not graded", g["cells_not_graded"] == {"count": 2, "cells": ["a20/kc3/r2", "a20/kc5/r32"]} and g["op2"]["n_cells"] == 38,
          str(g["cells_not_graded"]))
    # READ-KE: 26 below the control (0.52 < 0.55), 13 above (0.57), 1 tied (0.55): 39 untied, needs 26 (p 0.0266)
    cells = [(kc, r) for kc in ("3", "5") for r in LADDER]; vals = iter([0.52] * 26 + [0.57] * 13 + [0.55])
    ke = {nm: {c: next(vals) for c in cells} for nm, _, _ in NAMES}
    t = grade(*_files({nm: {"ke": ke[nm]} for nm in ke}), tols)["read_ke"]
    check("READ-KE 26 below, 13 above, 1 tie dropped: beats the control", (t["below"], t["above"], t["tied"], t["needed"]) == (26, 13, 1, 26)
          and t["beats_control"] == "BEATS THE CONTROL", f"p {t['p_one_sided']:.4f}")
    vals = iter([0.52] * 25 + [0.57] * 15); ke = {nm: {c: next(vals) for c in cells} for nm, _, _ in NAMES}
    t = grade(*_files({nm: {"ke": ke[nm]} for nm in ke}), tols)["read_ke"]
    check("READ-KE 25 of 40: does not beat the control", t["below"] == 25 and t["beats_control"] == "does not beat the control", f"p {t['p_one_sided']:.4f}")
    check("READ-KE against READ (0.50) and L1E's form reported", t["vs_read"]["above"] == 40 and abs(t["pooled_E_advantage"] - (0.30 - 0.29) / 0.30) < 1e-12,
          f"{t['vs_read']} E adv {t['pooled_E_advantage']:.4f}")
    t = grade(*_files({"a30": {"ke": {("3", 2): None}}}), tols)["read_ke"]
    check("a cell without READ-KE is dropped from its test and listed", t["cells"] == 39 and t["dropped_no_read_ke"] == ["a30/kc3/r2"], str(t["dropped_no_read_ke"]))
    for label, mut in (("roles differ", lambda a, b: b.update(seed_role="pilot")), ("seeds differ", lambda a, b: b.update(seed=8)),
                       ("a trajectory of another seed", lambda a, b: a["worlds"][0].update(trajectory_cache="a30_seed8.npz"))):
        op2, op1 = _files(); mut(op2, op1)
        try: grade(op2, op1, tols); ok = False
        except SystemExit: ok = True
        check(f"refused: {label}", ok)
    try: grade(*_files(), {"M1": 0.02, "TOL1": 0.25, "TOL_N": 0.05}); ok = False
    except SystemExit: ok = True
    check("a run file with other tolerances is refused", ok)
    g = grade(*_files(role="smoke"), {"M1": 0.5, "TOL1": 1.0, "TOL_N": 0.5})
    check("a smoke file is labelled not a verdict, and is not held to the registered tolerances", g["op2"]["gate"].startswith("SMOKE GRADE, NOT A VERDICT")
          and g["read_ke"]["beats_control"].startswith("SMOKE GRADE, NOT A VERDICT"), g["op2"]["gate"])
    p2, p1 = HERE / "pilot.json", HERE.parent / "OP1" / "pilot.json"
    if p2.exists() and p1.exists():
        g = grade(json.loads(p2.read_text(encoding="utf-8")), json.loads(p1.read_text(encoding="utf-8")), json.loads((HERE / "tolerances.json").read_text(encoding="utf-8")))
        check("on the pilots, OP1's check removes OP2's nu 0.03 worlds: 20 cells graded, labelled not a verdict",
              g["regime_check"]["removed"] == ["p_nu030_n96", "p_nu030_n128"] and g["op2"]["n_cells"] == 20 and g["op2"]["gate"].startswith("PILOT GRADE, NOT A VERDICT"), g["op2"]["gate"])
    else:
        check("OP1's and OP2's pilot.json present for the real-data check", False)
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv: return 1 if selftest() else 0
    tols = json.load(open(argv[argv.index("--tols") + 1], encoding="utf-8-sig"))
    op1 = json.load(open(argv[argv.index("--op1") + 1], encoding="utf-8"))
    g = grade(json.load(open(argv[0], encoding="utf-8")), op1, tols); text = json.dumps(g, indent=1, default=float)
    if "--out" in argv: open(argv[argv.index("--out") + 1], "w", encoding="utf-8").write(text + "\n")
    print(text); return 0


if __name__ == "__main__":
    sys.exit(main())
