#!/usr/bin/env python3
"""EG-4c round three: the long statics run (exploratory, EG track).

Round two established the exact Gaussian instrument, measurable
fields from a strong-contrast scatterer, isotropy within spread, and
superposition deviations decaying with source separation, distance
acting as the weak-field knob. What it could not reach at times 48
and 96 is the static regime, because two-dimensional waves relax
with slow algebraic tails and the profiles were still
transient-dominated. This runner is the long-time batch, the axis
profile at doubling times 256 and 512 on lattices too large for any
wrap, with convergence, gradedness, monotone decay, and Poisson
localization evaluated on the late pair. Verdicts computed from the
numbers.

Exploratory label. No physics claim.
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

from eg4c2_wave import DEFECT_HALF, field_at  # noqa: E402
from projection_fold import canonical_sha256  # noqa: E402

T_LONG = (256, 512)
AXIS_RS = list(range(4, 61, 4))


def main() -> int:
    profiles = {}
    for t_steps in T_LONG:
        side = 2 * t_steps + 64
        c = side // 2
        src = tuple((c + a, c + b)
                    for a in range(-DEFECT_HALF, DEFECT_HALF + 1)
                    for b in range(-DEFECT_HALF, DEFECT_HALF + 1))
        d_far = field_at(side, t_steps,
                         (c + t_steps + DEFECT_HALF + 10, c), src)
        assert d_far == 0.0, f"causality violated at T={t_steps}"
        axis = []
        for r in AXIS_RS:
            axis.append({"r": r, "phi_bits":
                         field_at(side, t_steps, (c, c + r), src)})
            print(f"T={t_steps} r={r}: {axis[-1]['phi_bits']:.6g}",
                  flush=True)
        profiles[str(t_steps)] = axis

    p1 = np.array([row["phi_bits"] for row in profiles[str(T_LONG[0])]])
    p2 = np.array([row["phi_bits"] for row in profiles[str(T_LONG[1])]])
    scale = float(max(p2.max(), 1e-300))
    conv = float(np.max(np.abs(p2 - p1))) / scale
    spread = float((p2.max() - p2.min()) / scale) if p2.max() > 0 else 0.0
    monotone = bool(np.all(np.diff(p2) <= 1e-12))
    lap = [p2[i + 1] - 2 * p2[i] + p2[i - 1]
           for i in range(1, len(p2) - 1)]
    lap_near = max(abs(v) for i, v in enumerate(lap)
                   if AXIS_RS[i + 1] <= 12)
    lap_mid = max((abs(v) for i, v in enumerate(lap)
                   if 16 <= AXIS_RS[i + 1] <= 48), default=0.0)
    items = {
        "causality_null": True,
        "static_converged": bool(conv < 0.05),
        "static_graded": bool(spread > 0.1),
        "monotone_decay": monotone,
        "poisson_source_localized":
            bool(lap_near > 5.0 * lap_mid) if lap_mid > 0
            else bool(lap_near > 0),
    }
    passed = sum(1 for v in items.values() if v)
    verdict = (
        f"long statics at T {T_LONG[0]} and {T_LONG[1]}: convergence "
        f"{conv:.3g}, spread {spread:.3g}, monotone {monotone}, "
        f"laplacian near/mid {lap_near:.3g}/{lap_mid:.3g}; "
        f"{passed} of {len(items)} items pass"
        + (", the statics portion of the EG-4 bar is met on the wave "
           "substrate." if passed == len(items) else
           ", the static regime "
           + ("is reached but the profile shape fails the remaining "
              "items." if items["static_converged"] else
              "is still not reached at these times.")))

    record = {
        "schema": "eg4c3-statics-v1",
        "label": "exploratory",
        "declared": {"times": list(T_LONG), "axis_rs": AXIS_RS,
                     "substrate": "as eg4c2-wave round 2c, strong "
                                  "contrast scatterer kappa 0.05"},
        "profiles": profiles,
        "convergence_relative": conv,
        "spread": spread,
        "monotone_decay": monotone,
        "laplacian_near": float(lap_near),
        "laplacian_mid": float(lap_mid),
        "items": items,
        "verdict": verdict,
        "runtime": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "numpy": np.__version__,
            "platform": platform.platform(),
            "hostname": platform.node(),
            "code_commit": os.environ.get("CODE_COMMIT", "unknown"),
        },
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"}
    )
    output = Path(__file__).resolve().parents[1] / "results" \
        / "eg4c3-statics.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")
    print(verdict)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
