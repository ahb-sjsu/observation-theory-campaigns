"""Grades a D5v2 results.json against the sealed bars of PREREG-D5V2.md.
Usage: python d5v2_grade.py results.json --tols tolerances.json [--out grade.json]
The claim is the observer-relative transition as a law: the read fraction of carried perturbations, per spectral
budget B, converges in resolution and collapses on x = B / B_c(t) (B_c the front wavenumber) more tightly than on
the unscaled null, inside a declared viscosity scope (nu at most NU_MAX = 0.005, where a front forms); the control,
decaying two-dimensional turbulence, must NOT collapse more tightly on the scaled variable than on the null. No
alarm and no lead bar: D5 showed and said in advance that the budgeted reader is not early. tolerances.json carries
TOL_N (convergence), TOL_C (collapse scatter) and RATIO (the scaled-over-unscaled ratio the collapse must beat)."""
from __future__ import annotations

import json
import sys

import numpy as np

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from d5_grade import points, scatter  # noqa: E402

NU_MAX = 0.005


def control_points(w: dict, scaled: bool) -> list[tuple[float, float]]:
    """The control's points: B over its own front wavenumber max |grad u| / max |u| (recorded by the D5v2 workload),
    or unscaled B; y = f_B(t) / f_B(0)."""
    rec = w["record"]; ts = np.array(rec["t"]); mg = np.array(rec["max_grad"]); Bc = (mg / np.array(rec["max_u"])) if "max_u" in rec else 2.0 * mg / mg[0]; out = []
    for B in [b for b in rec["geom"][0] if b != "total_energy"]:
        f = np.array([g[B]["read_fraction"] for g in rec["geom"]]); f0 = f[0]
        for i in range(len(ts)):
            x = float(B) / Bc[i] if scaled else float(B); out.append((np.log2(x), f[i] / f0))
    return out


def grade(res: dict, tols: dict) -> dict:
    TOL_N = float(tols["TOL_N"]); TOL_C = float(tols["TOL_C"]); RATIO = float(tols["RATIO"])
    out = {"tolerances": tols, "scope_nu_max": NU_MAX, "bars": {}, "gate": None}; fail = False
    burg = [w for w in res["worlds"] if w.get("t_star") is not None]; ins = [w for w in burg if w["nu"] <= NU_MAX + 1e-12]; outs = [w for w in burg if w["nu"] > NU_MAX + 1e-12]
    ctrl = [w for w in res["worlds"] if w.get("t_star") is None]
    e1 = True
    for w in res["worlds"]:
        for g in w["record"]["geom"]:
            bs = sorted([int(b) for b in g if b != "total_energy"]); fs = [g[str(b)]["read_fraction"] for b in bs]
            e1 = e1 and all(a <= b + 1e-9 for a, b in zip(fs, fs[1:])) and fs[-1] <= 1.0 + 1e-9
    out["bars"]["E1_nested"] = {"holds": bool(e1)}
    diffs = {}
    for a in ins:
        for b in ins:
            if a["ic_seed"] == b["ic_seed"] and a["nu"] == b["nu"] and b["N"] == 2 * a["N"]:
                ta = np.array(a["record"]["t"]); tb = np.array(b["record"]["t"]); n = min(len(ta), len(tb)); keep = ta[:n] <= 0.9 * a["t_star"]
                shared = [bb for bb in a["record"]["geom"][0] if bb != "total_energy" and bb in b["record"]["geom"][0]]
                diffs[f"{a['name']}|{b['name']}"] = max(float(np.max(np.abs(np.array([g[bb]["read_fraction"] for g in a["record"]["geom"][:n]])[keep] - np.array([g[bb]["read_fraction"] for g in b["record"]["geom"][:n]])[keep]))) for bb in shared)
    n1 = all(d <= TOL_N for d in diffs.values()) if diffs else None
    out["bars"]["N1_convergence_in_scope"] = {"pairs": diffs, "max_diff": max(diffs.values()) if diffs else None, "limit": TOL_N, "holds": n1}
    if diffs and max(diffs.values()) > 3 * TOL_N: fail = True
    c1 = True; c2 = True; coll = {}
    for nu in sorted(set(w["nu"] for w in ins)):
        ws = [w for w in ins if w["nu"] == nu]
        if len(ws) < 2: continue
        sc = scatter(sum((points(w, True) for w in ws), [])); un = scatter(sum((points(w, False) for w in ws), [])); coll[str(nu)] = {"scaled": sc, "unscaled": un}
        if sc["median_iqr"] is None: c1 = False; continue
        c1 = c1 and sc["median_iqr"] <= TOL_C and sc["max_iqr"] <= 2 * TOL_C
        c2 = c2 and un["median_iqr"] is not None and sc["median_iqr"] <= RATIO * un["median_iqr"]
        if sc["median_iqr"] > 3 * TOL_C: fail = True
    out["bars"]["C1_collapse_in_scope"] = {"by_nu": coll, "limit_median": TOL_C, "limit_max": 2 * TOL_C, "holds": bool(c1) if coll else None}
    out["bars"]["C2_scaled_beats_null_in_scope"] = {"ratio": RATIO, "holds": bool(c2) if coll else None}
    # outside the scope: reported, not claimed
    rep = {}
    for nu in sorted(set(w["nu"] for w in outs)):
        ws = [w for w in outs if w["nu"] == nu]
        if len(ws) >= 2:
            sc = scatter(sum((points(w, True) for w in ws), [])); un = scatter(sum((points(w, False) for w in ws), [])); rep[str(nu)] = {"scaled_median_iqr": sc["median_iqr"], "unscaled_median_iqr": un["median_iqr"]}
    out["bars"]["R1_outside_scope"] = rep
    # C3 the control: the scaled variable must not organise the control's read fractions (scaled median IQR at least the unscaled)
    if len(ctrl) >= 1:
        sc = scatter(sum((control_points(w, True) for w in ctrl), [])); un = scatter(sum((control_points(w, False) for w in ctrl), []))
        c3 = (sc["median_iqr"] is not None and un["median_iqr"] is not None and sc["median_iqr"] >= RATIO * un["median_iqr"])
        out["bars"]["C3_control_does_not_collapse"] = {"scaled": sc, "unscaled": un, "holds": bool(c3)}
        if sc["median_iqr"] is not None and un["median_iqr"] is not None and sc["median_iqr"] < 0.5 * un["median_iqr"]: fail = True
    else:
        c3 = None; out["bars"]["C3_control_does_not_collapse"] = {"holds": None}
    bars = [e1, n1, out["bars"]["C1_collapse_in_scope"]["holds"], out["bars"]["C2_scaled_beats_null_in_scope"]["holds"], c3]
    if any(b is None for b in bars):
        out["gate"] = "NOT ALL GROUPS RUN (pilot or probe): " + ("all run bars hold" if all(b for b in bars if b is not None) else "a run bar fails")
        return out
    out["gate"] = "PASS" if all(bars) else ("FAIL" if fail else "INDETERMINATE")
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0]; tols = json.load(open(argv[argv.index("--tols") + 1], encoding="utf-8-sig"))
    outp = argv[argv.index("--out") + 1] if "--out" in argv else None
    g = grade(json.load(open(path, encoding="utf-8-sig")), tols); text = json.dumps(g, indent=1)
    if outp:
        open(outp, "w", encoding="utf-8").write(text + "\n")
    print(text); return 0


if __name__ == "__main__":
    sys.exit(main())
