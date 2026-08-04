#!/usr/bin/env python3
"""Governed run of PREREG-QO3-001. Every constant is from the sealed
document; the machinery is the sealed-commit code path in qo3_family,
with only the declared grids substituted, exactly as the estimator
section licenses."""
from __future__ import annotations

import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402
import qo3_family  # noqa: E402
from qo3_family import CUTS, WINDOWS_B, coupling_point, spread  # noqa: E402

J_GRID = [0.7, 0.9, 1.1, 1.3]
H_GRID = [1.7, 1.9, 2.1, 2.3]
THETAS = [0.06, 0.11, 0.16, 0.21]
EPSILON = 0.05
DELTA = 0.05
LOOSE = 0.15

EXPLORATORY_J = {0.6, 0.8, 1.0, 1.2}
EXPLORATORY_H = {1.6, 1.8, 2.0, 2.2}
EXPLORATORY_THETA = {0.05, 0.10, 0.15, 0.20}
assert not set(J_GRID) & EXPLORATORY_J, "J grid overlaps exploratory"
assert not set(H_GRID) & EXPLORATORY_H, "h grid overlaps exploratory"
assert not set(THETAS) & EXPLORATORY_THETA, "theta grid overlaps exploratory"

qo3_family.THETAS = THETAS  # declared-grid substitution, per the estimator


def main() -> int:
    window_keys = ["".join(str(q) for q in w) for w in WINDOWS_B]
    points = []
    for j in J_GRID:
        for h in H_GRID:
            lambdas, residuals, lambdas_b, residuals_b = coupling_point(j, h)
            points.append({
                "J": j, "h": h,
                "residual_by_cut": {str(c): residuals[c] for c in CUTS},
                "lambda_by_cut": {str(c): lambdas[c] for c in CUTS},
                "family_b_lambda_by_window": lambdas_b,
                "family_b_residual_by_window": residuals_b,
            })
    n_points = len(points)

    def summarize(eps, delta):
        single_a = {
            str(c): sum(p["residual_by_cut"][str(c)] < eps for p in points)
            / n_points for c in CUTS
        }
        lam_a = [{c: p["lambda_by_cut"][str(c)] for c in CUTS}
                 for p in points]
        joint_a = sum(
            all(p["residual_by_cut"][str(c)] < eps for c in CUTS)
            and spread(lam, CUTS) < delta
            for p, lam in zip(points, lam_a, strict=True)
        ) / n_points
        single_b = {
            key: sum(p["family_b_residual_by_window"][key] < eps
                     for p in points) / n_points
            for key in window_keys
        }
        joint_b = sum(
            all(p["family_b_residual_by_window"][key] < eps
                for key in window_keys)
            and spread(p["family_b_lambda_by_window"], window_keys) < delta
            for p in points
        ) / n_points
        return single_a, joint_a, single_b, joint_b

    single_a, joint_a, single_b, joint_b = summarize(EPSILON, DELTA)
    loose = summarize(LOOSE, LOOSE)

    min_single_a = min(single_a.values())
    min_single_b = min(single_b.values())
    claim1_pass = joint_b < min_single_b
    claim2_pass = joint_a == min_single_a
    unevaluable = loose[3] == 0.0

    if unevaluable:
        label = "unevaluable"
        outcome = "declaration fails: no coupling point satisfies the "\
                  "family-B requirement even at loose thresholds"
    else:
        label = ("demonstrated-in-model"
                 if claim1_pass and claim2_pass else "refuted")
        outcome = (f"claim 1 (activation) "
                   f"{'PASSES' if claim1_pass else 'REFUTED'}: joint(B) = "
                   f"{joint_b:.4f} vs min single(B) = {min_single_b:.4f}; "
                   f"claim 2 (inertness) "
                   f"{'PASSES' if claim2_pass else 'REFUTED'}: joint(A) = "
                   f"{joint_a:.4f} vs min single(A) = {min_single_a:.4f}")

    surviving_b = [
        (p["J"], p["h"]) for p in points
        if all(p["family_b_residual_by_window"][key] < EPSILON
               for key in window_keys)
        and spread(p["family_b_lambda_by_window"], window_keys) < DELTA
    ]

    record = {
        "schema": "prereg-qo3-001-run-v1",
        "registration_id": "PREREG-QO3-001",
        "label": label,
        "outcome": outcome,
        "claim1_activation_pass": bool(claim1_pass),
        "claim2_inertness_pass": bool(claim2_pass),
        "strict": {
            "single_a": single_a, "joint_a": joint_a,
            "single_b": single_b, "joint_b": joint_b,
        },
        "loose_descriptive": {
            "joint_a": loose[1], "joint_b": loose[3],
        },
        "surviving_b_points": surviving_b,
        "coupling_points": points,
        "declared": {
            "J_grid": J_GRID, "h_grid": H_GRID, "thetas": THETAS,
            "epsilon": EPSILON, "delta": DELTA, "loose": LOOSE,
        },
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
    output = Path(__file__).resolve().parents[1] / "results" / "prereg-qo3-001.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print(outcome)
    print(f"surviving family-B points: {surviving_b}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
