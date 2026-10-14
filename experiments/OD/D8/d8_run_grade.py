"""Grades the joint D8 and OP4 run (PREREG-D8-RUN-DRAFT.md Sections 2 to 5): D8's gate, OP4's reading, the secondary arms.
Usage: python d8_run_grade.py <d8 results.json> <variants.json> --tols tolerances.json [--out grade.json]
       python d8_run_grade.py --selftest

Inputs. The D8 results are the merged file of submit_d8_nrp.py --collect (every world, the graded and recorded observers,
the instrument fields). The variants file is submit_variants_nrp.py --collect (GRAM, READ_KE, GRAM_UN and SV per world,
test trajectories by index, ladder halves already joined). A cell is (world, test trajectory) of a world the stability
guard did not refuse. An arm's m* is read as its ladder index, a censored arm at len(ladder), as in d8_grade.py.

D8 (Section 2): d8_grade.grade on the D8 results, unchanged.

OP4 (Section 2): over the cells where GRAM, BALL and READ are all present, the pooled advantage of GRAM over BALL in ladder
steps, mean(i_BALL - i_GRAM). "instrument" if it is at least 0 (GRAM ahead of or level with BALL); otherwise "both" if the
pooled advantage over READ, mean(i_READ - i_GRAM), is above 0 (GRAM ahead of READ); otherwise "system".

Secondary arms (Section 5): READ_KE, GRAM_UN and SV, each against BALL by a one-sided sign test over its cells, ties
dropped (an arm is ahead in a cell when its index is below BALL's); p = P(Binomial(n, 1/2) >= ahead), n the untied cells.
Holm's correction across the three arms at family-wise 0.05: sorted by p, the j-th smallest is compared with
0.05 / (3 - j + 1), and an arm beats BALL only if it and every smaller p pass. A cell missing an arm or BALL is dropped from
that arm's test (Section 7), and the test runs on the cells left. Margins in ladder steps against BALL, READ and the best of
the graded controls per cell are reported beside the test, untested. A file of any role but "run" is labelled as not a
verdict.
"""
from __future__ import annotations

import json
import math
import sys

import numpy as np

from d8_grade import CONTROLS, grade as d8_grade_fn, index

ARMS = ("READ_KE", "GRAM_UN", "SV")
FWER = 0.05


def d8_cells(d8: dict) -> dict:
    """(world, test index) -> {"ladder", "idx": ladder index per D8 observer}, for every world that was not refused."""
    out = {}
    for w in d8["worlds"]:
        if w.get("refused"): continue
        for t in w["tests"]:
            out[(w["name"], t["index"])] = {"ladder": w["ladder"], "n": w["n"], "nu": w["nu"], "idx": {k: index(o, w["ladder"]) for k, o in t["observers"].items()}}
    return out


def arm_indices(var: dict, cells: dict) -> dict:
    """arm -> {(world, test): ladder index}, on D8's ladder for that world (the ladders must agree)."""
    out = {}
    for arm, ws in var["arms"].items():
        for wn, rec in ws.items():
            for t in rec["tests"]:
                key = (wn, t["index"])
                if key not in cells: continue
                if rec["ladder"] != cells[key]["ladder"]: raise SystemExit(f"{arm} {wn}: ladder differs from D8's")
                out.setdefault(arm, {})[key] = index(t["observers"][arm], rec["ladder"])
    return out


def sign_test(ahead: int, behind: int) -> float:
    n = ahead + behind
    if n == 0: return 1.0
    return sum(math.comb(n, k) for k in range(ahead, n + 1)) / 2 ** n


def holm(ps: dict, alpha: float = FWER) -> dict:
    """arm -> (threshold, rejected) by Holm's step-down; an arm with p None is not tested and counts as not rejected."""
    tested = sorted((p, a) for a, p in ps.items() if p is not None); m = len(tested); out = {a: (None, False) for a in ps}; go = True
    for j, (p, a) in enumerate(tested, 1):
        thr = alpha / (m - j + 1); go = go and p <= thr; out[a] = (thr, go)
    return out


def margins(cs, arm_idx, ref) -> dict:
    d = [ref(c) - arm_idx[k] for k, c in cs]
    return {"cells": len(d), "pooled_steps": float(np.mean(d)) if d else None, "ahead": sum(x > 0 for x in d), "level": sum(x == 0 for x in d), "behind": sum(x < 0 for x in d),
            "per_cell": {f"{k[0]}/t{k[1]}": x for (k, _), x in zip(cs, d)}}


def grade(d8: dict, var: dict, tols: dict) -> dict:
    role = d8.get("seed_role", "run")
    if var.get("seed_role", role) != role: raise SystemExit(f"D8 file is role {role}, variants file is {var.get('seed_role')}")
    label = (lambda s: s) if role == "run" else (lambda s: f"{role.upper()} GRADE, NOT A VERDICT: {s}")
    cells = d8_cells(d8); idx = arm_indices(var, cells)
    out = {"seed_role": role, "d8": d8_grade_fn(d8, tols), "op4": {}, "secondary": {}}
    # OP4
    g = idx.get("GRAM", {}); cs = [(k, c) for k, c in sorted(cells.items()) if k in g and "BALL" in c["idx"] and "READ" in c["idx"]]
    if cs:
        vb = margins(cs, g, lambda c: c["idx"]["BALL"]); vr = margins(cs, g, lambda c: c["idx"]["READ"])
        reading = "instrument" if vb["pooled_steps"] >= 0 else ("both" if vr["pooled_steps"] > 0 else "system")
        out["op4"] = {"cells": len(cs), "missing_cells": sorted(f"{k[0]}/t{k[1]}" for k in cells if k not in g), "gram_vs_ball": vb, "gram_vs_read": vr, "reading": label(reading)}
    else:
        out["op4"] = {"cells": 0, "reading": label("NO CELLS (GRAM missing)")}
    # secondary arms
    ps = {}
    for arm in ARMS:
        a = idx.get(arm, {}); cs = [(k, c) for k, c in sorted(cells.items()) if k in a and "BALL" in c["idx"]]
        vb = margins(cs, a, lambda c: c["idx"]["BALL"])
        ps[arm] = sign_test(vb["ahead"], vb["behind"]) if cs else None
        out["secondary"][arm] = {"cells": len(cs), "missing_cells": sorted(f"{k[0]}/t{k[1]}" for k in cells if k not in a), "untied": vb["ahead"] + vb["behind"],
                                 "ahead_of_ball": vb["ahead"], "behind_ball": vb["behind"], "p_one_sided": ps[arm], "vs_ball": vb,
                                 "vs_read": margins([x for x in cs if "READ" in x[1]["idx"]], a, lambda c: c["idx"]["READ"]),
                                 "vs_best_control": margins([x for x in cs if all(k in x[1]["idx"] for k in CONTROLS)], a, lambda c: min(c["idx"][k] for k in CONTROLS))}
    for arm, (thr, rej) in holm(ps).items():
        out["secondary"][arm]["holm_threshold"] = thr
        out["secondary"][arm]["beats_ball"] = label("BEATS BALL" if rej else "does not beat BALL")
    return out


# ---------------------------------------------------------------- self-test on synthetic results

def _rec(m, L):
    return {"m_star": m, "synced": [m is not None and x >= m for x in L], "initial_spreading_rate": [1.0] * len(L)}


def _files(spec, role="run", ladder=(4, 8, 16, 32, 64)):
    """spec: list of cells, each {observer or arm: m* or None}; one world per 8 cells."""
    L = list(ladder); worlds = []; arms = {}
    for wi in range(0, len(spec), 8):
        wn = f"w{wi // 8}"; tests = []
        for j, c in enumerate(spec[wi:wi + 8]):
            obs = {k: _rec(c[k], L) for k in ("READ", "BALL", "ENSTROPHY", "KE", "SENS")}
            obs.update({f"RANDOM{r}": _rec(None, L) for r in range(3)})
            tests.append({"index": j, "observers": obs, "all_hold_max": 1e-12, "none_final": 0.9, "mu_record": {}, "dt_half": {}})
            for arm in ("GRAM",) + ARMS:
                if arm in c: arms.setdefault(arm, {}).setdefault(wn, {"ladder": L, "tests": []})["tests"].append({"index": j, "observers": {arm: _rec(c[arm], L)}})
        worlds.append({"name": wn, "n": 64 * (1 + wi // 8), "nu": 0.03, "ladder": L, "tests": tests, "rankings": {k: [[1, 0]] * 64 for k in ("READ", "BALL", "ENSTROPHY", "KE", "SENS")},
                       "theorem_checks": [{"T1_ratio": 1e-16, "first_octave_max_read": 1.0, "T2_ratio": 0.02}]})
    return {"seed_role": role, "worlds": worlds}, {"seed_role": role, "arms": arms}


def selftest() -> int:
    fails = 0; tols = {"M1": 0.5, "TOL1": 1.0, "TOL_N": 0.5}

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"{label}: {detail}", "PASS" if ok else "FAIL"); fails += 0 if ok else 1

    base = {"READ": 16, "BALL": 8, "ENSTROPHY": 32, "KE": 16, "SENS": 16}
    # exact binomial thresholds at 32 untied cells (Section 5): 23 ahead p = 0.0100, 22 ahead p = 0.0251, 21 ahead p = 0.0551
    check("sign test 23/32, 22/32, 21/32", abs(sign_test(23, 9) - 0.0100) < 5e-5 and abs(sign_test(22, 10) - 0.0251) < 5e-5 and abs(sign_test(21, 11) - 0.0551) < 5e-5,
          f"{sign_test(23, 9):.4f} {sign_test(22, 10):.4f} {sign_test(21, 11):.4f}")
    h = holm({"A": 0.0100, "B": 0.0100, "C": 0.0251})
    check("Holm: 23, 23 and 22 cells ahead all pass", all(v[1] for v in h.values()) and [round(h[k][0], 4) for k in "ABC"] == [0.0167, 0.025, 0.05], str(h))
    h = holm({"A": 0.0251, "B": 0.0100, "C": 0.0100})
    check("Holm orders by p, not by arm: the same three p values in another order all pass", all(v[1] for v in h.values()) and round(h["A"][0], 4) == 0.05, str(h))
    h = holm({"A": 0.0251, "B": 0.0251, "C": 0.0100})
    check("Holm: the second smallest p 0.0251 > 0.025 stops the rest", h["C"][1] and not h["A"][1] and not h["B"][1], str(h))
    # 32 cells: READ_KE 23 ahead of BALL (4 vs 8) and 9 behind; GRAM_UN level everywhere; SV 22 ahead and 10 behind
    spec = []
    for i in range(32):
        spec.append({**base, "GRAM": 16 if i < 16 else 4, "READ_KE": 4 if i < 23 else 16, "GRAM_UN": 8, "SV": 4 if i < 22 else 16})
    d8, var = _files(spec); g = grade(d8, var, tols); s = g["secondary"]
    check("READ_KE 23/32 beats BALL", s["READ_KE"]["ahead_of_ball"] == 23 and s["READ_KE"]["beats_ball"] == "BEATS BALL", s["READ_KE"]["beats_ball"])
    check("GRAM_UN level everywhere: no untied cells, not tested", s["GRAM_UN"]["untied"] == 0 and s["GRAM_UN"]["p_one_sided"] == 1.0 and s["GRAM_UN"]["beats_ball"] == "does not beat BALL", s["GRAM_UN"]["beats_ball"])
    check("SV 22/32 at the second Holm step (0.0251 > 0.025) does not beat BALL", s["SV"]["ahead_of_ball"] == 22 and s["SV"]["beats_ball"] == "does not beat BALL", f"{s['SV']['p_one_sided']:.4f} thr {s['SV']['holm_threshold']}")
    check("OP4: GRAM level with BALL pooled (one step ahead in half the cells, behind in half) reads instrument",
          g["op4"]["reading"] == "instrument" and g["op4"]["gram_vs_ball"]["pooled_steps"] == 0.0, str(g["op4"]["gram_vs_ball"]["pooled_steps"]))
    d8, var = _files([{**base, "GRAM": 16} for _ in range(8)])
    r = grade(d8, var, tols)["op4"]
    check("OP4: GRAM one step behind BALL and level with READ reads system", r["reading"] == "system", f"{r['gram_vs_ball']['pooled_steps']} {r['gram_vs_read']['pooled_steps']} {r['reading']}")
    d8, var = _files([{**base, "GRAM": 32} for _ in range(8)])
    r = grade(d8, var, tols)["op4"]
    check("OP4: GRAM behind BALL and behind READ reads system", r["reading"] == "system", f"{r['gram_vs_ball']['pooled_steps']} {r['gram_vs_read']['pooled_steps']} {r['reading']}")
    d8, var = _files([{**base, "GRAM": 8} for _ in range(4)] + [{**base, "GRAM": 16} for _ in range(4)])
    r = grade(d8, var, tols)["op4"]
    check("OP4: GRAM behind BALL (-0.5) and ahead of READ (+0.5) reads both", r["reading"] == "both", f"{r['gram_vs_ball']['pooled_steps']} {r['gram_vs_read']['pooled_steps']} {r['reading']}")
    spec = [{**base, "GRAM": 8, "READ_KE": 4, "GRAM_UN": 8, "SV": 8} for _ in range(8)]; del spec[3]["READ_KE"]
    d8, var = _files(spec); s = grade(d8, var, tols)["secondary"]["READ_KE"]
    check("a cell missing an arm is dropped from that arm's test", s["cells"] == 7 and s["missing_cells"] == ["w0/t3"] and abs(s["p_one_sided"] - 1 / 128) < 1e-12, f"{s['cells']} cells, p {s['p_one_sided']}")
    d8, var = _files([{**base, "GRAM": None, "READ_KE": None, "GRAM_UN": 4, "SV": 8, "BALL": None} for _ in range(8)])
    s = grade(d8, var, tols)
    check("censored arms sit one step past the top", s["op4"]["gram_vs_ball"]["level"] == 8 and s["secondary"]["GRAM_UN"]["ahead_of_ball"] == 8, str(s["secondary"]["GRAM_UN"]["vs_ball"]["pooled_steps"]))
    d8, var = _files([{**base, "GRAM": 8, "READ_KE": 4, "GRAM_UN": 8, "SV": 8} for _ in range(8)], role="smoke")
    g = grade(d8, var, tols)
    check("a smoke file is labelled not a verdict", g["op4"]["reading"].startswith("SMOKE GRADE, NOT A VERDICT") and g["secondary"]["READ_KE"]["beats_ball"].startswith("SMOKE GRADE")
          and g["d8"]["gate"].startswith("SMOKE GRADE"), g["op4"]["reading"])
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv: return 1 if selftest() else 0
    tols = json.load(open(argv[argv.index("--tols") + 1], encoding="utf-8-sig"))
    g = grade(json.load(open(argv[0], encoding="utf-8")), json.load(open(argv[1], encoding="utf-8")), tols); text = json.dumps(g, indent=1, default=float)
    if "--out" in argv: open(argv[argv.index("--out") + 1], "w", encoding="utf-8").write(text + "\n")
    print(text); return 0


if __name__ == "__main__":
    sys.exit(main())
