#!/usr/bin/env python3
"""EG-3 local first law on the causal-determinism substrate
(exploratory, EG track).

Question, per the track document. Does delta Q = T delta S hold
locally with flux, temperature, and entropy each defined
independently, as an output rather than an input.

The observation region is a spacetime patch, the natural region of
this substrate per the EG-1b corollary decision. A first structural
fact, proved en route and asserted, shapes the whole experiment. With
a full uniform initial ensemble, an injection BEFORE the patch's time
span is absorbed exactly. The evolved ensemble is already maximal on
every reachable set, so the perturbed marginal coincides with the
vacuum one and the entropy response is zero. A time-slice detector is
therefore blind, and the flux entering the first law must count the
stochastic events INSIDE the observation region, not all events. This
is measured, not assumed, and it is the substrate's version of the
statement that only heat crossing into the region drives its entropy.

The three quantities, each defined with no reference to the others.

delta Q. The count of declared noise injections inside the patch.
Event bookkeeping, no entropy anywhere.

T. A declared detector, the patch-entropy response to one training
injection placed inside the patch, measured once and frozen.

delta S. The patch entropy gain over vacuum, an exact GF(2) rank
difference from the instrument layer.

Held-out tests, never used in fixing T. Scattered dilute and moderate
interior patterns, where the law must be exact. Past patterns, all
events before the patch, where delta S must be exactly zero although
the naive all-events flux is positive. A mixed pattern, where the law
must hold with the inside-only accounting and fail with the naive
one. A stacked-column stress pattern probing rank alignment, with the
universal bound delta S <= number of events asserted throughout.

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
PATCH_T0 = 20
PATCH_COLS = range(0, 40)
TRAIN_EVENT = ((40, 20),)
HELD_OUT = {
    "dilute_2": ((25, 5), (50, 30)),
    "dilute_4": ((24, 4), (32, 14), (44, 26), (54, 36)),
    "moderate_8": ((22, 2), (27, 8), (32, 14), (37, 20),
                   (42, 26), (47, 32), (52, 36), (57, 10)),
    "past_4": ((5, 10), (8, 20), (12, 30), (15, 5)),
    "mixed_2in_2past": ((30, 10), (45, 25), (6, 15), (10, 33)),
    "stacked_column_12": tuple((t, 12) for t in range(25, 49, 2)),
}


def inside(event) -> bool:
    t, j = event
    return t >= PATCH_T0 and (j % N_RING) in PATCH_COLS


def patch_entropy(noise_events) -> int:
    hist = evolve_generators(N_RING, T_STEPS,
                             noise_events=tuple(noise_events))
    cells = [(t, j) for t in range(PATCH_T0, T_STEPS + 1)
             for j in PATCH_COLS]
    return marginal_entropy_bits(window_matrix(hist, cells))


def main() -> int:
    h_vac = patch_entropy(())

    h_train = patch_entropy(TRAIN_EVENT)
    t_detector = float(h_train - h_vac) / len(TRAIN_EVENT)
    assert t_detector > 0, "detector response must be positive"

    rows = []
    for name, events in HELD_OUT.items():
        dq_inside = sum(1 for e in events if inside(e))
        dq_naive = len(events)
        ds = patch_entropy(events) - h_vac
        assert ds <= dq_naive, "rank gain cannot exceed event count"
        predicted = t_detector * dq_inside
        residual = ((ds - predicted) / predicted if predicted > 0
                    else float(ds))
        rows.append({"pattern": name,
                     "delta_Q_inside": dq_inside,
                     "delta_Q_naive": dq_naive,
                     "delta_S_bits": ds,
                     "relative_residual_inside_accounting": residual})

    by_name = {r["pattern"]: r for r in rows}
    for name in ("dilute_2", "dilute_4", "moderate_8"):
        assert abs(by_name[name]
                   ["relative_residual_inside_accounting"]) < 1e-12, \
            f"first law must be exact for {name}"
    assert by_name["past_4"]["delta_S_bits"] == 0, \
        "past injections must be absorbed exactly"
    assert abs(by_name["mixed_2in_2past"]
               ["relative_residual_inside_accounting"]) < 1e-12, \
        "mixed pattern must satisfy inside-only accounting"
    assert by_name["mixed_2in_2past"]["delta_S_bits"] \
        < t_detector * by_name["mixed_2in_2past"]["delta_Q_naive"], \
        "naive all-events accounting must overpredict"

    verdict = (
        "the first law delta S = T delta Q holds exactly on held-out "
        "interior patterns with all three quantities independently "
        "defined, T frozen on one training injection; the flux that "
        "makes it hold is the events inside the spacetime region, "
        "because injections in the region's causal past are absorbed "
        "exactly by the maximal ensemble, delta S = 0 against a "
        "positive naive flux; the Clausius relation is an output on "
        "this substrate once the flux is the one crossing into the "
        "region, and a time-slice reading of the same relation is "
        "blind by the same absorption"
    )

    record = {
        "schema": "eg3-first-law-v2",
        "label": "exploratory",
        "declared": {"ring": N_RING, "steps": T_STEPS,
                     "patch": {"t_from": PATCH_T0, "t_to": T_STEPS,
                               "cols": [PATCH_COLS.start,
                                        PATCH_COLS.stop]},
                     "vacuum_rule": 90,
                     "train_event": [list(e) for e in TRAIN_EVENT],
                     "held_out_patterns": {k: [list(e) for e in v]
                                           for k, v in
                                           HELD_OUT.items()},
                     "detector": "patch-entropy response to one "
                                 "training injection, frozen",
                     "independence_audit": "delta Q counts events, no "
                         "entropy; T frozen on training only; delta S "
                         "is a rank; none defined through the others"},
        "vacuum_patch_entropy": h_vac,
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

    print(f"vacuum patch {h_vac} bits, T = {t_detector} bits/event")
    for r in rows:
        print(f"{r['pattern']}: dQ_in {r['delta_Q_inside']}, "
              f"dQ_naive {r['delta_Q_naive']}, dS "
              f"{r['delta_S_bits']}, residual "
              f"{r['relative_residual_inside_accounting']:+.4f}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
