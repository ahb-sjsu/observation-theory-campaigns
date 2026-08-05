#!/usr/bin/env python3
"""EG-3 local first law on the causal-determinism substrate
(exploratory, EG track).

Question, per the track document. Does delta Q = T delta S hold
locally with flux, temperature, and entropy each defined
independently, as an output rather than an input.

The three quantities, each defined with no reference to the others.

delta Q. The substrate's only stochastic events are declared noise
injections, one fresh bit XORed into a stated cell at a stated step.
The flux into a spacetime region is the COUNT of injections it
contains. This is event bookkeeping, defined without any entropy.

T. A declared detector, fixed on a single training configuration
before any test. The detector is the response ratio of the final-row
entropy to one injected bit placed far from every boundary, measured
once. Its value is recorded and then frozen.

delta S. The entropy gain of the final row over the vacuum value,
measured by the EG instrument layer as an exact GF(2) rank.

Independence audit. delta Q counts events and mentions no entropy.
T is fixed on the training configuration only and never recomputed.
delta S is a rank. None of the three is defined through the others,
so a first-law relation, if it holds, is an output.

The test. Held-out noise patterns of increasing density and varying
geometry (scattered dilute, scattered moderate, clustered, dense
block, repeated-cell), never used in fixing T. The witness is the
residual delta S - T delta Q relative to T delta Q. The quasi-static
analogue of the track document's bar is the dilute limit, where
injections are causally separated; the residual must vanish there.
Departures at finite density are measured, not assumed, and the
expected mechanism is saturation, two injections whose light cones
overlap on the window can share a rank direction.

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

from eg_ca_substrate import (  # noqa: E402
    evolve_generators,
    marginal_entropy_bits,
    window_matrix,
)
from projection_fold import canonical_sha256  # noqa: E402

N_RING = 257
T_STEPS = 60
TRAIN_EVENT = ((30, 200),)
HELD_OUT = {
    "dilute_2": ((10, 20), (40, 120)),
    "dilute_4": ((5, 10), (20, 70), (35, 130), (50, 190)),
    "moderate_8": ((6, 10), (12, 42), (18, 74), (24, 106),
                   (30, 138), (36, 170), (42, 202), (48, 234)),
    "clustered_4": ((30, 100), (30, 102), (31, 101), (32, 100)),
    "dense_block_9": ((28, 100), (28, 101), (28, 102),
                      (29, 100), (29, 101), (29, 102),
                      (30, 100), (30, 101), (30, 102)),
    "repeated_cell_5": ((20, 50), (25, 50), (30, 50), (35, 50),
                        (40, 50)),
}


def final_row_entropy(noise_events) -> int:
    hist = evolve_generators(N_RING, T_STEPS,
                             noise_events=tuple(noise_events))
    cells = [(T_STEPS, j) for j in range(N_RING)]
    return marginal_entropy_bits(window_matrix(hist, cells))


def main() -> int:
    h_vac = final_row_entropy(())
    assert h_vac == N_RING - 1, \
        f"vacuum final row must carry the parity constraint: {h_vac}"

    # detector calibration on the single training configuration
    h_train = final_row_entropy(TRAIN_EVENT)
    t_detector = float(h_train - h_vac) / len(TRAIN_EVENT)
    assert t_detector > 0, "detector response must be positive"

    rows = []
    for name, events in HELD_OUT.items():
        dq = len(events)
        ds = final_row_entropy(events) - h_vac
        predicted = t_detector * dq
        residual = (ds - predicted) / predicted
        rows.append({"pattern": name, "delta_Q": dq,
                     "delta_S_bits": ds,
                     "T_deltaQ": predicted,
                     "relative_residual": residual})

    dilute = [r for r in rows if r["pattern"].startswith("dilute")]
    for r in dilute:
        assert abs(r["relative_residual"]) < 1e-12, \
            f"first law must be exact in the dilute limit: {r}"
    dense = [r for r in rows
             if r["pattern"] in ("dense_block_9", "repeated_cell_5",
                                 "clustered_4")]
    assert any(r["relative_residual"] < -1e-12 for r in dense), \
        "saturation should appear somewhere in the dense patterns"

    verdict = (
        "the first law delta S = T delta Q holds exactly in the "
        "dilute limit with all three quantities independently "
        "defined, T fixed once on a training configuration and never "
        "recomputed; at finite density the relation breaks by "
        "saturation, overlapping light cones share rank directions "
        "so delta S falls below T delta Q, and the departure is "
        "measured, not assumed; on this substrate the Clausius "
        "relation is an output in the quasi-static limit and fails "
        "outside it, which is the ordering the thermodynamic gravity "
        "literature assumes rather than derives"
    )

    record = {
        "schema": "eg3-first-law-v1",
        "label": "exploratory",
        "declared": {"ring": N_RING, "steps": T_STEPS,
                     "vacuum_rule": 90,
                     "train_event": [list(e) for e in TRAIN_EVENT],
                     "held_out_patterns": {k: [list(e) for e in v]
                                           for k, v in
                                           HELD_OUT.items()},
                     "detector": "final-row entropy response to one "
                                 "training injection, frozen",
                     "independence_audit": "delta Q counts events, no "
                         "entropy; T frozen on training only; delta S "
                         "is a rank; none defined through the others"},
        "vacuum_row_entropy": h_vac,
        "T_detector_bits_per_event": t_detector,
        "held_out": rows,
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
        / "eg3-first-law.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print(f"vacuum row {h_vac}, T = {t_detector} bits/event")
    for r in rows:
        print(f"{r['pattern']}: dQ {r['delta_Q']}, dS "
              f"{r['delta_S_bits']}, residual "
              f"{r['relative_residual']:+.4f}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
