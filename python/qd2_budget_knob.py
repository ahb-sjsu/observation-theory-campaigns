#!/usr/bin/env python3
"""QD-2 the budget knob (exploratory).

Protocol declared in QUANTUM-DARWINISM-TRACK.md before this run.
The symmetric consumer's budget curve f*(theta) against the
branching closed form, and the portfolio consumer with declared
unequal angles where every subset has its own closed form and
fragments of equal size are no longer equivalent. Verdict computed
from the measured items.

Exploratory label. No claim about laboratory classicality.
"""
from __future__ import annotations

import itertools
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402
from qd0_instrument import (  # noqa: E402
    NENV, NQ, entropy_bits, h2, mi_sf, reduced)
from qd1_emergence import (  # noqa: E402
    apply_two_qubit, controlled_ry, initial_state)


def closed_i(c_frag, c_rest, c_tot):
    return (h2((1 + c_tot) / 2) + h2((1 + c_frag) / 2)
            - h2((1 + c_rest) / 2))


def main() -> int:
    record: dict = {"schema": "qd2-budget-knob-v1",
                    "label": "exploratory"}
    items = {}

    # symmetric consumer, the budget curve
    grid = [k * np.pi / 32 for k in range(1, 17)]
    dev_k1 = 0.0
    fstars = []
    curve = {}
    for theta in grid:
        psi = initial_state()
        u = controlled_ry(theta)
        for j in range(1, NQ):
            psi = apply_two_qubit(psi, u, 0, j)
        c = float(np.cos(theta / 2.0))
        ss = entropy_bits(reduced(psi, [0]))
        fstar_meas = 0
        fstar_pred = 0
        for f in range(1, NENV + 1):
            meas = mi_sf(psi, list(range(1, 1 + f)))
            pred = closed_i(c ** f, c ** (NENV - f), c ** NENV)
            dev_k1 = max(dev_k1, abs(meas - pred))
            if fstar_meas == 0 and meas >= 0.9 * ss - 1e-12:
                fstar_meas = f
            if fstar_pred == 0 and pred >= 0.9 * h2(
                    (1 + c ** NENV) / 2) - 1e-12:
                fstar_pred = f
        fstars.append(fstar_meas if fstar_meas else 7)
        curve[f"{theta:.6f}"] = {
            "fstar": int(fstar_meas) if fstar_meas else None,
            "system_entropy_bits": float(ss)}
        if fstar_meas != fstar_pred:
            dev_k1 = max(dev_k1, 1.0)
    items["K1_closed_form_and_fstar"] = dev_k1 <= 1e-10
    items["K2_fstar_monotone"] = all(
        fstars[i + 1] <= fstars[i] for i in range(len(grid) - 1))
    onset = next((grid[i] for i in range(len(grid))
                  if fstars[i] <= 6), None)

    # portfolio consumer
    angles = [np.pi / 16, np.pi / 16, np.pi / 8, np.pi / 4,
              np.pi / 2, 3 * np.pi / 4]
    psi = initial_state()
    for j, th in enumerate(angles, start=1):
        psi = apply_two_qubit(psi, controlled_ry(th), 0, j)
    cos_half = [float(np.cos(t / 2)) for t in angles]
    c_tot = float(np.prod(cos_half))
    dev_k3 = 0.0
    size2 = {}
    for r in range(1, NENV):
        for sub in itertools.combinations(range(NENV), r):
            c_f = float(np.prod([cos_half[j] for j in sub]))
            c_r = c_tot / c_f
            meas = mi_sf(psi, [j + 1 for j in sub])
            pred = closed_i(c_f, c_r, c_tot)
            dev_k3 = max(dev_k3, abs(meas - pred))
            if r == 2:
                size2[str(sub)] = float(meas)
    items["K3_portfolio_closed_form"] = dev_k3 <= 1e-10
    best2 = max(size2.values())
    worst2 = min(size2.values())

    record["measured"] = {
        "k1_max_dev": float(dev_k1),
        "budget_curve": curve,
        "onset_angle": float(onset) if onset else None,
        "k3_max_dev": float(dev_k3),
        "size2_best_bits": float(best2),
        "size2_worst_bits": float(worst2),
        "size2_ratio": float(best2 / max(worst2, 1e-300)),
        "reading": "the consumer's budget is a portfolio, not a "
                   "number, equal fragment counts differ by the "
                   "measured ratio"}
    record["items"] = {k: bool(v) for k, v in items.items()}
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "qd2-budget-knob.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("fstars", fstars, "onset", onset,
          "size2 ratio", best2 / max(worst2, 1e-300))
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
