#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

from projection_fold import (
    analytic_fold_branches,
    canonical_sha256,
    schwinger_optimum,
    signed_branch_count,
    simulate_toy_hamiltonian,
)


def run_scenario(scenario: dict) -> dict:
    model = scenario.get("model")
    if model == "analytic_fold":
        branches = analytic_fold_branches(
            float(scenario.get("t_obs", 1.0)),
            t0=float(scenario.get("t0", 0.0)),
            tau0=float(scenario.get("tau0", 0.0)),
            a=float(scenario.get("a", 1.0)),
            x0=float(scenario.get("x0", 0.0)),
            velocity=float(scenario.get("velocity", 1.0)),
        )
        return {
            "branch_count": len(branches),
            "signed_branch_count": signed_branch_count(branches),
            "branches": [branch.__dict__ for branch in branches],
        }
    if model == "schwinger_action":
        radius, action = schwinger_optimum(
            float(scenario["mass"]), float(scenario["charge_field"])
        )
        return {"optimal_radius": radius, "optimal_action": action}
    if model == "toy_hamiltonian":
        params = {
            "omega_t": float(scenario["omega_t"]),
            "omega_u": float(scenario["omega_u"]),
            "lambda": float(scenario["lambda"]),
            "g": float(scenario["g"]),
            "field": float(scenario["field"]),
        }
        initial_state = [
            float(scenario.get("t0", 0.0)),
            float(scenario.get("pt0", 1.0)),
            float(scenario.get("x0", 0.0)),
            float(scenario.get("px0", 0.0)),
            float(scenario.get("u0", 0.1)),
            float(scenario.get("pu0", 0.0)),
        ]
        result = simulate_toy_hamiltonian(
            initial_state,
            params,
            dt=float(scenario.get("dt", 1e-3)),
            tau_max=float(scenario.get("tau_max", 40.0)),
        )
        return result.to_dict()
    raise ValueError(f"unsupported model: {model!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--scenario-json")
    source.add_argument("--scenario-file")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    if args.scenario_json:
        scenario = json.loads(args.scenario_json)
    else:
        scenario = json.loads(Path(args.scenario_file).read_text(encoding="utf-8"))

    input_hash = canonical_sha256(scenario)
    started = datetime.now(timezone.utc)
    outcome = run_scenario(scenario)
    ended = datetime.now(timezone.utc)
    record = {
        "schema": "projection-fold-trial-v1",
        "scenario": scenario,
        "scenario_sha256": input_hash,
        "outcome": outcome,
        "outcome_sha256": canonical_sha256(outcome),
        "runtime": {
            "started_utc": started.isoformat(),
            "ended_utc": ended.isoformat(),
            "elapsed_seconds": (ended - started).total_seconds(),
            "python": sys.version,
            "platform": platform.platform(),
            "hostname": platform.node(),
            "container_image": os.environ.get("CONTAINER_IMAGE_DIGEST", "unknown"),
            "code_commit": os.environ.get("CODE_COMMIT", "unknown"),
        },
    }
    record["record_sha256"] = canonical_sha256(record)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
