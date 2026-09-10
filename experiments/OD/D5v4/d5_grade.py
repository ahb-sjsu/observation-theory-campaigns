"""Grades a D5 results.json against the sealed bars of PREREG-D5.md.
Usage: python d5_grade.py results.json --tols tolerances.json [--out grade.json]
tolerances.json carries TOL_N (convergence in resolution), TOL_C (collapse scatter) and MARGIN_L (lead).
The collapse variable is x = B / B_c(t) with B_c = max|u_x| / max|u|, the collapsed quantity y = f_B(t) / f_B(0),
on samples after the front has begun to steepen (B_c(t) >= STEEP x B_c(0)); the null is the same with x = B."""
from __future__ import annotations

import json
import sys

import numpy as np

BINS = np.arange(-3.0, 4.51, 0.5)   # bins in log2 x
STEEP = 1.2


def points(w: dict, scaled: bool) -> list[tuple[float, float]]:
    rec = w["record"]; ts = np.array(rec["t"]); mg = np.array(rec["max_grad"]); mu = np.array(rec["max_u"]); Bc = mg / mu
    out = []
    for B in [b for b in rec["geom"][0] if b != "total_energy"]:
        f = np.array([g[B]["read_fraction"] for g in rec["geom"]]); f0 = f[0]
        for i in range(len(ts)):
            if Bc[i] >= STEEP * Bc[0]:
                x = float(B) / Bc[i] if scaled else float(B); out.append((np.log2(x), f[i] / f0))
    return out


def scatter(pts: list[tuple[float, float]]) -> dict:
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts]); iqrs = []
    for lo, hi in zip(BINS[:-1], BINS[1:]):
        sel = (xs >= lo) & (xs < hi)
        if sel.sum() >= 8:
            q = np.percentile(ys[sel], [25, 75]); iqrs.append(float(q[1] - q[0]))
    return {"n_bins": len(iqrs), "median_iqr": float(np.median(iqrs)) if iqrs else None, "max_iqr": float(max(iqrs)) if iqrs else None, "n_points": len(pts)}


def grade(res: dict, tols: dict) -> dict:
    TOL_N = float(tols["TOL_N"]); TOL_C = float(tols["TOL_C"]); MARGIN_L = float(tols["MARGIN_L"])
    out = {"tolerances": tols, "bars": {}, "gate": None}; fail = False
    burg = [w for w in res["worlds"] if w.get("t_star") is not None]; ctrl = [w for w in res["worlds"] if w.get("t_star") is None]
    # E1 exact: read fractions nested in B and at most 1, every sample of every world
    e1 = True
    for w in res["worlds"]:
        for g in w["record"]["geom"]:
            bs = sorted([int(b) for b in g if b != "total_energy"]); fs = [g[str(b)]["read_fraction"] for b in bs]
            e1 = e1 and all(a <= b + 1e-9 for a, b in zip(fs, fs[1:])) and fs[-1] <= 1.0 + 1e-9
    out["bars"]["E1_nested"] = {"holds": bool(e1)}
    # N1 convergence: pairs (same ic seed_offset and nu, N and 2N), max |f_B^N - f_B^2N| over t <= 0.9 t* and shared budgets
    pairs = []; diffs = {}
    for a in burg:
        for b in burg:
            if a["ic_seed"] == b["ic_seed"] and a["nu"] == b["nu"] and b["N"] == 2 * a["N"]:
                ta = np.array(a["record"]["t"]); tb = np.array(b["record"]["t"]); n = min(len(ta), len(tb)); keep = ta[:n] <= 0.9 * a["t_star"]
                shared = [bb for bb in a["record"]["geom"][0] if bb != "total_energy" and bb in b["record"]["geom"][0]]
                d = max(float(np.max(np.abs(np.array([g[bb]["read_fraction"] for g in a["record"]["geom"][:n]])[keep] - np.array([g[bb]["read_fraction"] for g in b["record"]["geom"][:n]])[keep]))) for bb in shared)
                pairs.append((a["name"], b["name"])); diffs[f"{a['name']}|{b['name']}"] = d
    n1 = (all(d <= TOL_N for d in diffs.values())) if diffs else None
    out["bars"]["N1_convergence"] = {"pairs": diffs, "max_diff": max(diffs.values()) if diffs else None, "limit": TOL_N, "holds": n1}
    if diffs and max(diffs.values()) > 3 * TOL_N:
        fail = True
    # C1 collapse per viscosity, and C2 the scaled collapse tighter than the unscaled null
    c1 = True; c2 = True; coll = {}
    for nu in sorted(set(w["nu"] for w in burg)):
        ws = [w for w in burg if w["nu"] == nu]
        if len(ws) < 2: continue
        sc = scatter(sum((points(w, True) for w in ws), [])); un = scatter(sum((points(w, False) for w in ws), []))
        coll[str(nu)] = {"scaled": sc, "unscaled": un}
        if sc["median_iqr"] is None: c1 = False; continue
        c1 = c1 and sc["median_iqr"] <= TOL_C and sc["max_iqr"] <= 2 * TOL_C
        c2 = c2 and (un["median_iqr"] is not None and sc["median_iqr"] <= 0.8 * un["median_iqr"])
        if sc["median_iqr"] > 3 * TOL_C:
            fail = True
    out["bars"]["C1_collapse"] = {"by_nu": coll, "limit_median": TOL_C, "limit_max": 2 * TOL_C, "holds": bool(c1) if coll else None}
    out["bars"]["C2_scaled_beats_null"] = {"holds": bool(c2) if coll else None}
    # L1 lead over the classical alarm: per Burgers world, the earliest observational alarm across budgets against the classical alarm
    leads = {}
    for w in burg:
        obs = [v for v in w["alarms_obs"].values() if v is not None]; cl = w["alarm_classical"]
        if cl is not None:
            leads[w["name"]] = (cl - min(obs)) if obs else -float("inf")
    fin = [v for v in leads.values() if np.isfinite(v)]
    l1 = (len(fin) == len(leads) and len(leads) > 0 and float(np.median(fin)) >= MARGIN_L) if leads else None
    out["bars"]["L1_lead"] = {"leads": {k: (v if np.isfinite(v) else None) for k, v in leads.items()}, "n_no_obs_alarm": sum(1 for v in leads.values() if not np.isfinite(v)), "median_lead": float(np.median(fin)) if fin else None, "margin": MARGIN_L, "holds": l1}
    # X1 control: no observational alarm on any control world at any budget
    x1 = all(v is None for w in ctrl for v in w["alarms_obs"].values()) if ctrl else None
    out["bars"]["X1_control"] = {"alarms": {w["name"]: w["alarms_obs"] for w in ctrl}, "max_grad_ratio": {w["name"]: w["max_grad_ratio"] for w in ctrl}, "holds": x1}
    if ctrl and sum(v is not None for w in ctrl for v in w["alarms_obs"].values()) > 0.5 * sum(len(w["alarms_obs"]) for w in ctrl):
        fail = True
    bars = [out["bars"][k]["holds"] for k in ("E1_nested", "N1_convergence", "C1_collapse", "C2_scaled_beats_null", "L1_lead", "X1_control")]
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
