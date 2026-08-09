#!/usr/bin/env python3
"""PF-7b: the Bell ceiling, corrected instrument.

Bars in experiments/PF7B-BELL-DECLARATION.md. PF-7a's record stands as a VOID
with its two declaration errors named; this run does not replace it.

Corrections, both forced by the instrument study python/pf7_control_tuning.py:
  * anti-vacuity is barred per cell ONLY against a PR box, which is nonlocal by
    construction and carries no geometry, measured S = 4.000 in 16/16. The
    premise-break arms are barred in aggregate, because the study measured that
    the substrate varies their violation magnitude (post-selection fires 8-10/16,
    locality 10-12/16, whatever the coefficient).
  * the measurement dependence tilt is rescaled by d, since |L . q| falls as
    1/sqrt(d) and a fixed coefficient weakens with dimension.
  * the angular law is judged by the parent harness's own comparison, scaled
    sawtooth against quantum, not against an unscaled sawtooth.

Shared source and arm machinery is imported from pf7_bell_ceiling so the two
runs cannot drift apart.
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

from pf7_bell_ceiling import (  # noqa: E402
    DETECTOR_SHARP, DIMS, N_ANG, N_DRAW, N_ORIENT, SEED,
    angular_law, chsh, dirn, eta_align, fold_orientations, outcomes, plane,
)
from projection_fold import canonical_sha256  # noqa: E402

LEAK = 0.45
ZIGZAG = 0.35
B0_BAR = 2.0
B0B_MEDIAN = 2.0
B0B_MIN_FIRE = 10
B2_BAR = 0.99
B3_MIN_CELLS = 14
B4_BAR = 0.01


def run_arm(X, w, qA, qB, rng, arm, sharp=None, zigzag=0.0):
    """P0 / C1 postselect / C2 measurement dependence / C3 locality / C0 PR box."""
    eta = None if sharp is None else eta_align(sharp)
    d = X.shape[1]
    E_all, E_ps, marg, eff = {}, {}, {}, {}
    base = rng.choice(len(X), N_DRAW, p=w)
    blind = rng.random(N_DRAW) < zigzag if zigzag > 0 else None
    for x in (0, 1):
        for y in (0, 1):
            if arm == "C2":
                tilt = w * np.exp(1.2 * d * (X @ qA[x]) * (X @ qB[y]))
                tilt /= tilt.sum()
                idx = rng.choice(len(X), N_DRAW, p=tilt)
            else:
                idx = base
            L = X[idx]
            if arm == "C0":                       # PR box: a XOR b = x.y
                a = rng.integers(0, 2, N_DRAW)
                b = (a ^ (x * y)).astype(int)
                A, B = 1.0 - 2.0 * a, 1.0 - 2.0 * b
            else:
                sa = L @ qA[x]
                if arm == "C3":
                    sa = sa + LEAK * (L @ qB[y])
                A = np.where(sa >= 0, 1.0, -1.0)
                B = np.where((L @ qB[y]) >= 0, -1.0, 1.0)
                if eta is not None:
                    A = np.where(rng.random(N_DRAW) < eta(L, qA[x]), A, 0.0)
                    B = np.where(rng.random(N_DRAW) < eta(L, qB[y]), B, 0.0)
                if blind is not None:
                    B = np.where(blind, 0.0, B)
            E_all[(x, y)] = float((A * B).mean())
            both = (A != 0) & (B != 0)
            eff[(x, y)] = float(both.mean())
            E_ps[(x, y)] = float((A[both] * B[both]).mean()) if both.sum() > 50 else 0.0
            marg[(x, y)] = (float(A.mean()), float(B.mean()))
    ns = max(max(abs(marg[(x, 0)][0] - marg[(x, 1)][0]) for x in (0, 1)),
             max(abs(marg[(0, y)][1] - marg[(1, y)][1]) for y in (0, 1)))
    return dict(arm=arm, S_all_counted=chsh(E_all), S_postselected=chsh(E_ps),
                no_signalling_residual=float(ns),
                eff_mean=float(np.mean(list(eff.values()))), zigzag=zigzag)


def main() -> int:
    rng = np.random.default_rng(SEED)
    tol = 4.0 / np.sqrt(N_DRAW)
    print(f"PF-7b Bell ceiling (corrected instrument)  seed={SEED}")
    print("per-cell anti-vacuity on the PR box only; premise arms barred in aggregate\n",
          flush=True)

    grid = [dict(d=d, kappa=k, zipf_a=z)
            for d in DIMS for k in (0.0, 2.0) for z in (0.0, 1.5)]
    p0, c0, prem, blind, ang = [], [], [], [], []
    for g in grid:
        X, w = fold_orientations(N_ORIENT, g["d"], g["kappa"], g["zipf_a"], rng)
        e1, e2 = plane(g["d"], rng)
        qA = {0: dirn(e1, e2, 0.0), 1: dirn(e1, e2, np.pi / 2)}
        qB = {0: dirn(e1, e2, np.pi / 4), 1: dirn(e1, e2, -np.pi / 4)}

        for sharp in (None, DETECTOR_SHARP):
            r = run_arm(X, w, qA, qB, rng, "P0", sharp)
            r.update(g, sharp=(sharp or 0.0))
            p0.append(r)
        r = run_arm(X, w, qA, qB, rng, "C0")
        r.update(g)
        c0.append(r)
        for arm, sh in (("C1", DETECTOR_SHARP), ("C2", None), ("C3", None)):
            r = run_arm(X, w, qA, qB, rng, arm, sh)
            r.update(g)
            prem.append(r)
        r = run_arm(X, w, qA, qB, rng, "P0", DETECTOR_SHARP, zigzag=ZIGZAG)
        r.update(g)
        blind.append(r)
        ang.append(dict(**g, **angular_law(X, w, rng, g["d"], N_DRAW // 4, None)))
        print(f"  d={g['d']:3d} k={g['kappa']:.0f} z={g['zipf_a']:.1f} | "
              f"P0={p0[-2]['S_all_counted']:.4f} C0={c0[-1]['S_all_counted']:.3f} "
              f"C1ps={prem[-3]['S_postselected']:.3f} C2={prem[-2]['S_all_counted']:.3f} "
              f"C3={prem[-1]['S_all_counted']:.3f} | E(0)={ang[-1]['E_at_zero']:+.4f} "
              f"saw<qm={ang[-1]['rms_vs_scaled_sawtooth'] < ang[-1]['rms_vs_quantum']}",
              flush=True)

    s0 = np.array([r["S_all_counted"] for r in p0])
    ns0 = np.array([r["no_signalling_residual"] for r in p0])
    s_pr = np.array([r["S_all_counted"] for r in c0])
    field = {"C1": "S_postselected", "C2": "S_all_counted", "C3": "S_all_counted"}
    byarm = {k: np.array([r[field[k]] for r in prem if r["arm"] == k]) for k in field}
    e0 = np.array([a["E_at_zero"] for a in ang])
    saw_wins = int(sum(a["rms_vs_scaled_sawtooth"] < a["rms_vs_quantum"] for a in ang))
    gap = np.array([a["max_gap_vs_quantum"] for a in ang])
    b_all = np.array([r["S_all_counted"] for r in blind])
    b_ps = np.array([r["S_postselected"] for r in blind])

    bars = {
        "B0_prbox_fires_every_cell": bool(s_pr.min() > B0_BAR),
        "B0b_premise_arms_aggregate": bool(all(
            float(np.median(byarm[k])) > B0B_MEDIAN
            and int((byarm[k] > 2.0).sum()) >= B0B_MIN_FIRE for k in byarm)),
        "B1_ceiling_code_check": bool(s0.max() <= 2.0 + 3.0 * tol),
        "B2_conservation_signature": bool(np.abs(e0).min() >= B2_BAR),
        "B3_scaled_sawtooth_beats_quantum": bool(saw_wins >= B3_MIN_CELLS),
        "B4_no_signalling": bool(ns0.max() <= B4_BAR),
        "B5_blind_consumer_loophole": bool(
            b_ps.max() > 2.0 and b_all.max() <= 2.0 + 3.0 * tol),
    }
    verdict = "PASS" if all(bars.values()) else "FAIL"
    if not bars["B0_prbox_fires_every_cell"]:
        verdict = "VOID_INSTRUMENT_NOT_LIVE"

    record = {
        "schema": "pf7b-bell-ceiling-v1",
        "declaration": "experiments/PF7B-BELL-DECLARATION.md",
        "supersedes_bars_of": "experiments/PF7-BELL-DECLARATION.md",
        "does_not_supersede": "results/pf7a-bell-ceiling.json (VOID, kept)",
        "provenance": (
            "arm semantics from geometric-observation/experiments/"
            "bell_geometry_audit.py (GO-P-2026-057); corrections forced by "
            "python/pf7_control_tuning.py; fold specific content is signed "
            "count zero, per crossing independence, PF-8 1->3 zigzag"),
        "note_on_B1": "P0 null is a theorem for any source measure; B1 is a code check",
        "p0": p0, "prbox": c0, "premise_controls": prem,
        "blind_consumer": blind, "angular": ang,
        "summary": {
            "P0_S_max": float(s0.max()), "P0_S_values": sorted(set(np.round(s0, 6).tolist())),
            "PR_S_min": float(s_pr.min()),
            "premise_median": {k: float(np.median(byarm[k])) for k in byarm},
            "premise_fires": {k: int((byarm[k] > 2.0).sum()) for k in byarm},
            "E_at_zero_min_abs": float(np.abs(e0).min()),
            "scaled_sawtooth_wins": saw_wins,
            "max_gap_vs_quantum": {"min": float(gap.min()), "median": float(np.median(gap)),
                                   "max": float(gap.max())},
            "blind_S_all_max": float(b_all.max()),
            "blind_S_postselected_max": float(b_ps.max()),
            "no_signalling_max": float(ns0.max()),
            "finite_tolerance": float(tol)},
        "bars": bars,
        "verdict": {"value": verdict, "computed_from": sorted(bars)},
        "declared": {"seed": SEED, "dims": list(DIMS), "n_orient": N_ORIENT,
                     "n_draw": N_DRAW, "n_ang": N_ANG, "leak": LEAK,
                     "zigzag": ZIGZAG, "detector_sharp": DETECTOR_SHARP,
                     "B0_bar": B0_BAR, "B0b_median": B0B_MEDIAN,
                     "B0b_min_fire": B0B_MIN_FIRE, "B2_bar": B2_BAR,
                     "B3_min_cells": B3_MIN_CELLS, "B4_bar": B4_BAR},
        "runtime": {"generated_utc": datetime.now(timezone.utc).isoformat(),
                    "python": sys.version, "numpy": np.__version__,
                    "platform": platform.platform(), "hostname": platform.node(),
                    "code_commit": os.environ.get("CODE_COMMIT", "unknown")},
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" / "pf7b-bell-ceiling.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")

    print("\n" + "=" * 68)
    for k, v in bars.items():
        print(f"  {k:36s} {'PASS' if v else 'FAIL'}")
    print("=" * 68)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
