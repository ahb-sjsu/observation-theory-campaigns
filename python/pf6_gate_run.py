#!/usr/bin/env python3
"""PF6-001 governed gate run. Sealed under PREREG-PF6-001.

Applies the frozen PF-6 covariance and observer audits to the
PF4-002 Sauter-slab family on the cells bound by PREREG-PF5-002.
Every constant is from the sealed document. The verdict is computed
from the bars.
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

import pf4_pilot as pilot  # noqa: E402
from pf6_covariance import (  # noqa: E402
    ALPHA_GRID, boost, first_fold_worldpoint, flow, fold_count,
    integrate)
from projection_fold import canonical_sha256  # noqa: E402

CELLS = [(0.60, 0.8957885742187499),
         (0.70, 1.0448364257812501),
         (0.80, 1.2020141601562502),
         (0.90, 1.3605468750000003)]
SHIFTS = [-2.0, -0.5, 0.5, 2.0]
N_STEPS = 20_000
PU0 = 0.1
ALPHA_REPARAM = 2.0


def main() -> int:
    record: dict = {"schema": "prereg-pf6-001-v1",
                    "registration_id": "PREREG-PF6-001",
                    "label": "sealed-gate-run"}
    cells = {}
    b1_ok = b2_ok = b5_ok = b6_ok = True
    worst_shift_dev = 0.0
    worst_wp_dev = 0.0
    worst_rate_dev = 0.0
    for p, e in CELLS:
        base = integrate(p, e, n_steps=N_STEPS, pu0=PU0)
        n_base = fold_count(base[1])
        wp_b = first_fold_worldpoint(base[0], base[1], base[2])
        if n_base < 1:
            b6_ok = False

        # bar 1, translation covariance
        for t0 in SHIFTS:
            mv = integrate(p, e, t0=t0, n_steps=N_STEPS, pu0=PU0)
            dev = float(np.max(np.abs(mv[0] - base[0] - t0)))
            worst_shift_dev = max(worst_shift_dev, dev)
            if dev >= 1e-6 or fold_count(mv[1]) != n_base:
                b1_ok = False
            wp_m = first_fold_worldpoint(mv[0], mv[1], mv[2])
            if wp_b is not None and wp_m is not None:
                d_t = abs(wp_m[0] - wp_b[0] - t0)
                d_u = abs(wp_m[1] - wp_b[1])
                worst_wp_dev = max(worst_wp_dev, d_t, d_u)
                if d_t >= 1e-6 or d_u >= 1e-6:
                    b1_ok = False
            elif (wp_b is None) != (wp_m is None):
                b1_ok = False

        # bar 2, reparametrization at alpha = 2 on the same segment
        sc = integrate(p, e, alpha=ALPHA_REPARAM, n_steps=N_STEPS,
                       pu0=PU0)
        n_sc = fold_count(sc[1])
        span_b = N_STEPS * pilot.DT
        span_s = N_STEPS * pilot.DT / ALPHA_REPARAM
        if n_base > 0:
            ratio = (n_sc / span_s) / (n_base / span_b)
            worst_rate_dev = max(worst_rate_dev,
                                 abs(ratio - ALPHA_REPARAM))
            if n_sc != n_base or abs(ratio - ALPHA_REPARAM) >= 1e-12:
                b2_ok = False
        else:
            # post-seal repair, named in CAMPAIGN.md: the sealing
            # commit's runner wrote a bare nan here and could not
            # serialize its own record. No bar is changed.
            ratio = None

        # bar 5, observer and detector audit
        curve = {}
        for a in ALPHA_GRID:
            slope = np.diff(base[0]) / pilot.DT + a
            obs = int(np.sum(slope[:-1] * slope[1:] < 0.0))
            shifted = base[1] + a
            det = int(np.sum(shifted[:-1] * shifted[1:] < 0.0))
            if obs != det:
                b5_ok = False
            curve[f"{a:g}"] = obs

        cells[f"P{p}_E{e:.6f}"] = {
            "fold_count": int(n_base),
            "first_fold_worldpoint": wp_b,
            "reparam_count": int(n_sc),
            "rate_ratio": (float(ratio) if ratio is not None
                           else None),
            "observer_curve": curve}
        print(f"P={p} E={e:.6f} folds={n_base} reparam={n_sc} "
              f"ratio={ratio} obs={curve}", flush=True)

    # bar 3, boost audit on the declared hyperbolic control
    worst_comm = worst_inv = 0.0
    min_cone = float("inf")
    for tdot in (1.02, 1.29, 2.0):
        for w0 in (-0.8, 0.0, 0.5):
            state = (tdot + 1.0, w0)
            inv0 = state[0] ** 2 - state[1] ** 2
            if inv0 <= 0 or state[0] <= abs(state[1]):
                continue
            for chi in (-2.0, -0.7, 0.7, 2.0):
                for ge in (0.5, 1.9, 2.1, 5.0):
                    a1 = flow(boost(state, chi), ge)
                    b1 = boost(flow(state, ge), chi)
                    worst_comm = max(worst_comm, abs(a1[0] - b1[0]),
                                     abs(a1[1] - b1[1]))
                    inv1 = a1[0] ** 2 - a1[1] ** 2
                    worst_inv = max(worst_inv,
                                    abs(inv1 - inv0) / abs(inv0))
                    for s in np.linspace(0.0, 1.0, 21):
                        c = flow(boost(state, chi), ge, s)
                        min_cone = min(min_cone, c[0] - abs(c[1]))
    b3_ok = (worst_comm < 1e-10 and worst_inv < 1e-10
             and min_cone > 0.0)

    verdict = ("PASS" if (b1_ok and b2_ok and b3_ok and b5_ok
                          and b6_ok)
               else ("vacuous" if not b6_ok else "FAIL"))
    record["cells"] = cells
    record["bars"] = {
        "b1_translation": bool(b1_ok),
        "b2_reparametrization": bool(b2_ok),
        "b3_boost": bool(b3_ok),
        "b4_gauge": "not-applicable, Sauter tilt declared "
                    "non-electromagnetic",
        "b5_observer_detector": bool(b5_ok),
        "b6_anti_vacuity": bool(b6_ok)}
    record["measured"] = {
        "worst_translation_worldline_dev": float(worst_shift_dev),
        "worst_worldpoint_dev": float(worst_wp_dev),
        "worst_rate_ratio_dev": float(worst_rate_dev),
        "cells_without_folds": int(sum(
            1 for v in cells.values() if v["fold_count"] < 1)),
        "boost_worst_commutation": float(worst_comm),
        "boost_worst_invariant_drift": float(worst_inv),
        "boost_min_future_cone_margin": float(min_cone)}
    record["verdict"] = {
        "value": verdict,
        "computed_from": ["b1", "b2", "b3", "b5", "b6"]}
    record["declared"] = {"cells": CELLS, "shifts": SHIFTS,
                          "n_steps": N_STEPS, "pu0": PU0,
                          "alpha_reparam": ALPHA_REPARAM,
                          "alpha_grid": list(ALPHA_GRID)}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "prereg-pf6-001.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("bars", record["bars"])
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
