#!/usr/bin/env python3
"""Governed run of PREREG-QO2-001. Every constant is from the sealed
document; the machinery is the sealed-commit code path in qo2_flip."""
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
from qo0_instrument import ising_hamiltonian_jh, partial_trace, thermal_state  # noqa: E402
from qo2_flip import FLUX_QUBIT, N_FULL, OUTSIDE, run_budget, scenario_states  # noqa: E402

BETA = 0.5
COUPLING_POINTS = [(1.0, 2.0), (0.8, 1.8), (1.2, 2.2)]
PRIMARY_POINT = (1.0, 2.0)
TRAIN_STRONG = [0.55, 0.85, 1.15]
TRAIN_WEAK = [0.12, 0.22, 0.32]
HELD_STRONG = [0.70, 1.00, 1.30]
HELD_WEAK = [0.08, 0.18, 0.28]
TASK_MARGIN = 0.01
FIDELITY_MARGIN = 0.01
BUDGETS = [1, 2, 3]

EXPLORATORY_ANGLES = {0.6, 0.9, 1.2, 0.1, 0.2, 0.3, 0.75, 1.05, 0.15, 0.25}
for angle in TRAIN_STRONG + TRAIN_WEAK + HELD_STRONG + HELD_WEAK:
    assert angle not in EXPLORATORY_ANGLES, "grid overlaps exploratory run"


def evaluate_point(j: float, h: float) -> dict:
    sigma_full = thermal_state(ising_hamiltonian_jh(N_FULL, j, h), BETA)
    vacuum = partial_trace(sigma_full, OUTSIDE, N_FULL)
    train_states = scenario_states(vacuum, TRAIN_STRONG, TRAIN_WEAK)
    held_states = scenario_states(vacuum, HELD_STRONG, HELD_WEAK)

    budgets = [run_budget(k, train_states, held_states, vacuum)
               for k in BUDGETS]
    for entry in budgets:
        held = entry["held_out"]
        for arm in ("F", "T", "anti"):
            assert np.isfinite(held[arm]["task_distortion"])
            assert np.isfinite(held[arm]["infidelity"])
        assert entry["anti_arm_interpretable"], \
            f"anti-arm not worst at (J={j}, h={h}, k={entry['budget_qubits']})"

    k_star = None
    for entry in budgets:
        if FLUX_QUBIT not in entry["f_arm_keeps"]:
            k_star = entry["budget_qubits"]
            break
    if k_star is None:
        return {"J": j, "h": h, "scope_failure": True, "budgets": budgets}

    star = next(b for b in budgets if b["budget_qubits"] == k_star)
    held = star["held_out"]
    task_pass = (held["T"]["task_distortion"]
                 < held["F"]["task_distortion"] - TASK_MARGIN)
    fidelity_pass = (held["T"]["infidelity"]
                     > held["F"]["infidelity"] + FIDELITY_MARGIN)
    return {
        "J": j, "h": h, "scope_failure": False, "k_star": k_star,
        "primary_task_margin_pass": bool(task_pass),
        "primary_fidelity_margin_pass": bool(fidelity_pass),
        "flip_at_k_star": bool(task_pass and fidelity_pass),
        "budgets": budgets,
    }


def main() -> int:
    points = {}
    for j, h in COUPLING_POINTS:
        points[f"{j},{h}"] = evaluate_point(j, h)

    primary = points[f"{PRIMARY_POINT[0]},{PRIMARY_POINT[1]}"]
    if primary.get("scope_failure"):
        outcome = "scope failure at the primary point: the fidelity-optimal "\
                  "subset contained the flux site at every budget"
        claim = "unevaluable"
    elif primary["flip_at_k_star"]:
        outcome = "primary claim PASSES at the sealed margins"
        claim = "demonstrated-in-model"
    else:
        outcome = "primary claim REFUTED at the sealed margins"
        claim = "refuted"

    secondary = {
        key: (p.get("scope_failure") and "scope-failure"
              or ("flip" if p.get("flip_at_k_star") else "no-flip"))
        for key, p in points.items()
        if key != f"{PRIMARY_POINT[0]},{PRIMARY_POINT[1]}"
    }

    record = {
        "schema": "prereg-qo2-001-run-v1",
        "registration_id": "PREREG-QO2-001",
        "label": claim,
        "outcome": outcome,
        "secondary_outcomes": secondary,
        "points": points,
        "declared": {
            "beta": BETA, "coupling_points": COUPLING_POINTS,
            "primary_point": PRIMARY_POINT,
            "train": [TRAIN_STRONG, TRAIN_WEAK],
            "held": [HELD_STRONG, HELD_WEAK],
            "task_margin": TASK_MARGIN, "fidelity_margin": FIDELITY_MARGIN,
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
    output = Path(__file__).resolve().parents[1] / "results" / "prereg-qo2-001.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    for key, p in points.items():
        if p.get("scope_failure"):
            print(f"({key}): SCOPE FAILURE")
            continue
        star = next(b for b in p["budgets"]
                    if b["budget_qubits"] == p["k_star"])
        held = star["held_out"]
        print(f"({key}) k*={p['k_star']}: "
              f"T task {held['T']['task_distortion']:.4f} vs "
              f"F task {held['F']['task_distortion']:.4f}; "
              f"T infid {held['T']['infidelity']:.4f} vs "
              f"F infid {held['F']['infidelity']:.4f}; "
              f"anti {held['anti']['task_distortion']:.4f}; "
              f"flip={p['flip_at_k_star']}")
    print(outcome)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
