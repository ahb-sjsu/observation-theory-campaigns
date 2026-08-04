#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()

    fields = [0.25, 0.5, 1.0, 2.0]
    couplings = [0.1, 0.25, 0.5]
    omega_t = [0.75, 1.0, 1.5]
    scenarios = []
    sequence = 0
    for field, g, wt, seed_index in itertools.product(
        fields, couplings, omega_t, range(args.seeds)
    ):
        sequence += 1
        scenarios.append(
            {
                "scenario_id": f"PF2-{sequence:05d}",
                "model": "toy_hamiltonian",
                "seed": 2026080300 + seed_index,
                "dt": 0.001,
                "tau_max": 40.0,
                "omega_t": wt,
                "omega_u": 1.2,
                "lambda": 0.1,
                "g": g,
                "field": field,
                "t0": 0.0,
                "pt0": 1.0,
                "x0": 0.0,
                "px0": 0.2,
                "u0": 0.1,
                "pu0": 0.0,
            }
        )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for scenario in scenarios:
            handle.write(json.dumps(scenario, sort_keys=True) + "\n")
    print(f"wrote {len(scenarios)} scenarios to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
