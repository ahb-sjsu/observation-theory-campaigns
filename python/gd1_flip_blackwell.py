#!/usr/bin/env python3
"""GD-1 the flip meets Blackwell (exploratory, GD track).

Protocol declared in GAMES-DECISIONS-TRACK.md before this run. Binary
state, uniform prior. Seven f-divergences between the two conditional
signal rows are the declared scalar fidelity battery. The wedge is a
pair where every divergence orders A above B while a declared task
strictly prefers B, possible only in the Blackwell-incomparable
region. G1 verifies the declared rare-decisive-signal exhibit, G2 is
the data-processing control on declared garbles, G3 checks that every
wedge found in a random ensemble is incomparable, G4 measures wedge
prevalence. Verdict computed from the measured items, never written
first.

Exploratory label. No claim about human beings.
"""
from __future__ import annotations

import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gd0_instrument import FEAS_TOL, experiment_value  # noqa: E402
from projection_fold import canonical_sha256  # noqa: E402

INCOMP_TOL = 1e-2
WEDGE_TASK_TOL = 1e-6
DPI_TOL = 1e-10


def divergences(p, q) -> dict:
    """The declared battery of seven f-divergences."""
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    m = 0.5 * (p + q)
    return {
        "kl_pq": float(np.sum(p * np.log(p / q))),
        "kl_qp": float(np.sum(q * np.log(q / p))),
        "tv": float(0.5 * np.sum(np.abs(p - q))),
        "hellinger_sq": float(1.0 - np.sum(np.sqrt(p * q))),
        "chi2_pq": float(np.sum((p - q) ** 2 / q)),
        "chi2_qp": float(np.sum((p - q) ** 2 / p)),
        "js": float(0.5 * np.sum(p * np.log(p / m))
                    + 0.5 * np.sum(q * np.log(q / m))),
    }


DIV_KEYS = ["kl_pq", "kl_qp", "tv", "hellinger_sq",
            "chi2_pq", "chi2_qp", "js"]


def garbling_residual(a, b, iters=20_000, check=500):
    """GD-0 projected-gradient search with an early exit on residual
    convergence. The checked object is the residual, as in GD-0."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    ya, yb = a.shape[1], b.shape[1]
    m = np.full((ya, yb), 1.0 / yb)
    lam = float(np.linalg.eigvalsh(a.T @ a).max())
    step = 0.9 / max(lam, 1e-12)
    best = np.inf
    for it in range(iters):
        grad = a.T @ (a @ m - b)
        m = m - step * grad
        for r in range(ya):
            v = np.sort(m[r])[::-1]
            css = np.cumsum(v) - 1.0
            rho = np.nonzero(
                v - css / (np.arange(yb) + 1.0) > 0)[0][-1]
            theta = css[rho] / (rho + 1.0)
            m[r] = np.maximum(m[r] - theta, 0.0)
        if (it + 1) % check == 0:
            resid = float(np.max(np.abs(a @ m - b)))
            if resid < FEAS_TOL or best - resid < 1e-13:
                return resid
            best = min(best, resid)
    return float(np.max(np.abs(a @ m - b)))


def draw_experiment(rng, k=3, floor=0.005) -> np.ndarray:
    """2 by k Dirichlet rows, entries at least floor by rejection."""
    while True:
        e = rng.dirichlet(np.ones(k), size=2)
        if e.min() >= floor:
            return e


def battery(rng) -> list:
    tasks = [rng.uniform(-1, 1, size=(3, 2)) for _ in range(200)]
    for c in (2.0, 5.0, 10.0, 20.0, 50.0):
        tasks.append(np.array([[0.0, 0.0], [-c, 1.0]]))
    return tasks


def main() -> int:
    record: dict = {"schema": "gd1-flip-blackwell-v1",
                    "label": "exploratory"}
    rng = np.random.RandomState(20260807)
    prior = np.array([0.5, 0.5])
    tasks = battery(rng)

    # G1: the declared rare-decisive-signal exhibit
    a_ex = np.array([[0.90, 0.05, 0.05], [0.05, 0.05, 0.90]])
    b_ex = np.array([[0.98, 0.019, 0.001], [0.881, 0.02, 0.099]])
    task_ex = np.array([[0.0, 0.0], [-20.0, 1.0]])
    div_a = divergences(a_ex[0], a_ex[1])
    div_b = divergences(b_ex[0], b_ex[1])
    margins = {k: div_a[k] - div_b[k] for k in DIV_KEYS}
    v_a = experiment_value(prior, task_ex, a_ex)
    v_b = experiment_value(prior, task_ex, b_ex)
    task_margin = v_b - v_a
    r_ab = garbling_residual(a_ex, b_ex)
    r_ba = garbling_residual(b_ex, a_ex)
    g1_pass = (all(m > 0.01 for m in margins.values())
               and task_margin > 0.01
               and r_ab > INCOMP_TOL and r_ba > INCOMP_TOL)
    record["G1"] = {
        "divergences_A": div_a, "divergences_B": div_b,
        "divergence_margins_A_minus_B": margins,
        "value_A": v_a, "value_B": v_b,
        "task_margin_B_minus_A": float(task_margin),
        "residual_A_to_B": r_ab, "residual_B_to_A": r_ba,
        "pass": bool(g1_pass)}
    print("G1", "PASS" if g1_pass else "FAIL",
          f"task_margin={task_margin:.6f} r_ab={r_ab:.3e} "
          f"r_ba={r_ba:.3e} min_div_margin="
          f"{min(margins.values()):.4f}")

    # G2: data-processing control on declared garbles
    worst_div = np.inf
    worst_task = -np.inf
    for _ in range(500):
        a = draw_experiment(rng)
        m_g = rng.dirichlet(np.ones(3), size=3)
        b = a @ m_g
        da = divergences(a[0], a[1])
        db = divergences(b[0], b[1])
        worst_div = min(worst_div,
                        min(da[k] - db[k] for k in DIV_KEYS))
        for t in tasks:
            gain = (experiment_value(prior, t, b)
                    - experiment_value(prior, t, a))
            worst_task = max(worst_task, gain)
    g2_pass = worst_div > -DPI_TOL and worst_task < DPI_TOL
    record["G2"] = {"pairs": 500, "battery_size": len(tasks),
                    "worst_divergence_drop": float(worst_div),
                    "worst_task_gain_under_garbling":
                        float(worst_task),
                    "pass": bool(g2_pass)}
    print("G2", "PASS" if g2_pass else "FAIL",
          f"worst_div_margin={worst_div:.3e} "
          f"worst_task_gain={worst_task:.3e}")

    # G3 + G4: random-ensemble localization and prevalence
    n_pairs = 2000
    counts = {"comparable": 0, "incomparable": 0, "ambiguous": 0,
              "unanimous_incomparable": 0, "wedge_incomparable": 0,
              "wedge_comparable": 0, "wedge_ambiguous": 0}
    wedge_margins = []
    for i in range(n_pairs):
        a = draw_experiment(rng)
        b = draw_experiment(rng)
        da = divergences(a[0], a[1])
        db = divergences(b[0], b[1])
        signs = [np.sign(da[k] - db[k]) for k in DIV_KEYS]
        unanimous = all(s > 0 for s in signs) or \
            all(s < 0 for s in signs)
        top, bot = (a, b) if signs[0] > 0 else (b, a)
        best_rev = -np.inf
        if unanimous:
            for t in tasks:
                rev = (experiment_value(prior, t, bot)
                       - experiment_value(prior, t, top))
                best_rev = max(best_rev, rev)
        wedge = unanimous and best_rev > WEDGE_TASK_TOL
        r1 = garbling_residual(a, b)
        r2 = garbling_residual(b, a)
        if r1 < FEAS_TOL or r2 < FEAS_TOL:
            cls = "comparable"
        elif r1 > INCOMP_TOL and r2 > INCOMP_TOL:
            cls = "incomparable"
        else:
            cls = "ambiguous"
        counts[cls] += 1
        if unanimous and cls == "incomparable":
            counts["unanimous_incomparable"] += 1
        if wedge:
            counts[f"wedge_{cls}"] += 1
            if cls == "incomparable":
                wedge_margins.append(float(best_rev))
        if (i + 1) % 200 == 0:
            print(f"  ensemble {i + 1}/{n_pairs} {counts}",
                  flush=True)
    g3_pass = counts["wedge_comparable"] == 0
    record["G3"] = {"ensemble": n_pairs, "seed": 20260807,
                    "counts": {k: int(v) for k, v in counts.items()},
                    "pass": bool(g3_pass)}
    wm = np.array(wedge_margins) if wedge_margins else np.array([0.0])
    record["G4"] = {
        "incomparable_pairs": int(counts["incomparable"]),
        "unanimous_among_incomparable":
            int(counts["unanimous_incomparable"]),
        "wedge_among_incomparable":
            int(counts["wedge_incomparable"]),
        "wedge_margin_max": float(wm.max()),
        "wedge_margin_median": float(np.median(wm)),
        "note": "measurement, no bar"}
    print("G3", "PASS" if g3_pass else "FAIL", counts)

    verdict = ("PASS" if g1_pass and g2_pass and g3_pass
               else "FAIL")
    record["verdict"] = {
        "value": verdict,
        "computed_from": ["G1.pass", "G2.pass", "G3.pass"]}
    record["declared"] = {
        "divergence_battery": DIV_KEYS,
        "feasibility_tol": FEAS_TOL, "incomparable_tol": INCOMP_TOL,
        "wedge_task_tol": WEDGE_TASK_TOL, "dpi_tol": DPI_TOL}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "gd1-flip-blackwell.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
