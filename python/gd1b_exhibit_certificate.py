#!/usr/bin/env python3
"""GD-1b exhibit certificate (exploratory, GD track).

Redeclared run after GD-1's G1 failed its residual-threshold bar.
The exhibit and task are unchanged. Incomparability is now proved,
not thresholded. A garbled experiment's joint columns are conic
combinations of the garbler's joint columns, so for a binary state
any target column (t0, t1) with t0 below r times t1, where r is the
garbler's minimum joint-column ratio, forces an L-infinity residual
of at least (r t1 - t0)/(1 + r). Total variation is an f-divergence,
so a garbling cannot raise it, which settles the other direction.
Verdict computed from the declared items.

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

from gd0_instrument import experiment_value  # noqa: E402
from gd1_flip_blackwell import (  # noqa: E402
    DIV_KEYS, divergences, garbling_residual)
from projection_fold import canonical_sha256  # noqa: E402


def conic_lower_bound(a, b, prior) -> float:
    """Exact lower bound on max|A M - B| over row-stochastic M, from
    the conic-hull constraint on joint columns, binary state."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    ja = prior[:, None] * a
    jb = prior[:, None] * b
    ratios = ja[0] / ja[1]
    r_min, r_max = float(ratios.min()), float(ratios.max())
    best = 0.0
    for y in range(jb.shape[1]):
        t0, t1 = float(jb[0, y]), float(jb[1, y])
        if t0 < r_min * t1:
            best = max(best, (r_min * t1 - t0) / (1.0 + r_min))
        if t1 < t0 / r_max:
            best = max(best, (t0 / r_max - t1) / (1.0 + 1.0 / r_max))
    # the bound is on the joint-column residual; the certificate
    # search works on likelihood columns, joint = prior * likelihood,
    # so rescale by the smaller prior weight to stay a valid bound
    return best / float(prior.max())


def main() -> int:
    record: dict = {"schema": "gd1b-exhibit-certificate-v1",
                    "label": "exploratory"}
    prior = np.array([0.5, 0.5])
    a_ex = np.array([[0.90, 0.05, 0.05], [0.05, 0.05, 0.90]])
    b_ex = np.array([[0.98, 0.019, 0.001], [0.881, 0.02, 0.099]])
    task_ex = np.array([[0.0, 0.0], [-20.0, 1.0]])

    div_a = divergences(a_ex[0], a_ex[1])
    div_b = divergences(b_ex[0], b_ex[1])
    margins = {k: div_a[k] - div_b[k] for k in DIV_KEYS}
    ok_div = all(m > 0.01 for m in margins.values())

    v_a = experiment_value(prior, task_ex, a_ex)
    v_b = experiment_value(prior, task_ex, b_ex)
    task_margin = float(v_b - v_a)
    ok_task = task_margin > 0.01

    bound = conic_lower_bound(a_ex, b_ex, prior)
    ok_bound = bound > 1e-3

    tv_gap = div_a["tv"] - div_b["tv"]
    ok_tv = tv_gap > 0.01

    resid = garbling_residual(a_ex, b_ex)
    ok_consistent = resid >= bound

    items = {"divergence_margins": ok_div, "task_margin": ok_task,
             "conic_bound": ok_bound, "tv_gap": ok_tv,
             "search_consistency": ok_consistent}
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["G1b"] = {
        "divergence_margins_A_minus_B": margins,
        "min_divergence_margin": float(min(margins.values())),
        "value_A": v_a, "value_B": v_b,
        "task_margin_B_minus_A": task_margin,
        "conic_lower_bound_B_from_A": float(bound),
        "tv_gap_A_minus_B": float(tv_gap),
        "search_residual_B_from_A": float(resid),
        "items": {k: bool(v) for k, v in items.items()}}
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["declared"] = {
        "bars": {"divergence_margin": 0.01, "task_margin": 0.01,
                 "conic_bound": 1e-3, "tv_gap": 0.01},
        "g2_g3_g4": "stand as measured in GD-1, not rerun"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "gd1b-exhibit-certificate.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("bound", bound, "resid", resid, "tv_gap", tv_gap,
          "task_margin", task_margin)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
