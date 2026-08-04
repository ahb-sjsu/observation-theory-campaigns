#!/usr/bin/env python3
"""WM-2 prescription-pair audit (exploratory, WM track).

Update order is a prescription, and the Cayley-pole lesson says
physics must not live in the prescription. This instance runs the
audit on string substitution systems, the Wolfram program's simpler
model class, with three declared prescriptions (leftmost match,
rightmost match, seeded random match) and three declared systems.

1. The sorting rule BA -> AB, the canonical causal-invariant example.
   It terminates (each event removes one inversion) and is locally
   confluent, so every prescription must reach the identical sorted
   string in the identical number of events. Exact agreement is the
   pass bar for the instrument.
2. The planted trap {AB -> B, BA -> A}, non-confluent by critical
   pair (on ABA, leftmost yields A while rightmost yields AA). The
   pipeline must flag its prescription dependence or the audit is
   void. This is the WM transplant of the PF-4 Cayley trap.
3. The growth rule A -> AB, non-terminating, measured at a fixed
   event budget. Its letter counts are conserved-charge witnesses
   that must agree across prescriptions, while the arrangement is
   prescription-borne, and the audit's job is to measure and report
   the split rather than to average it away. This is the
   signed-versus-unsigned lesson in rewriting form.

Exploratory label. The hypergraph version of this audit is designed
in the track document and not implemented here.
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

from projection_fold import canonical_sha256  # noqa: E402

SEED = 20260805
RANDOM_STRING_LENGTH = 60
GROWTH_EVENTS = 200


def matches(state: str, rules) -> list:
    found = []
    for lhs, rhs in rules:
        start = 0
        while True:
            i = state.find(lhs, start)
            if i < 0:
                break
            found.append((i, lhs, rhs))
            start = i + 1
    return found


def evolve(state: str, rules, prescription: str, *, max_events: int,
           rng=None):
    events = 0
    while events < max_events:
        found = matches(state, rules)
        if not found:
            break
        found.sort(key=lambda m: (m[0], m[1]))
        if prescription == "leftmost":
            pick = found[0]
        elif prescription == "rightmost":
            pick = found[-1]
        elif prescription == "random":
            pick = found[rng.randint(len(found))]
        else:
            raise ValueError(prescription)
        i, lhs, rhs = pick
        state = state[:i] + rhs + state[i + len(lhs):]
        events += 1
    return state, events


def letter_counts(state: str) -> dict:
    return {c: state.count(c) for c in sorted(set(state))}


def main() -> int:
    rng = np.random.RandomState(SEED)
    prescriptions = ["leftmost", "rightmost", "random"]

    initial = "".join(rng.choice(["A", "B"], RANDOM_STRING_LENGTH))
    inversions = sum(1 for i in range(len(initial))
                     for j in range(i + 1, len(initial))
                     if initial[i] == "B" and initial[j] == "A")
    sorting = {}
    for p in prescriptions:
        final, events = evolve(initial, [("BA", "AB")], p,
                               max_events=10_000,
                               rng=np.random.RandomState(SEED + 1))
        sorting[p] = {"final": final, "events": events}
    finals = {v["final"] for v in sorting.values()}
    event_counts = {v["events"] for v in sorting.values()}
    assert len(finals) == 1, "sorting rule disagreed across prescriptions"
    assert finals == {"".join(sorted(initial))}, "sorted string wrong"
    assert event_counts == {inversions}, \
        "event count is the inversion number, an exact invariant"

    trap = {}
    for p in prescriptions:
        final, events = evolve("ABABABAB", [("AB", "B"), ("BA", "A")], p,
                               max_events=10_000,
                               rng=np.random.RandomState(SEED + 2))
        trap[p] = {"final": final, "events": events}
    trap_finals = {v["final"] for v in trap.values()}
    trap_flagged = len(trap_finals) > 1
    assert trap_flagged, \
        "planted non-confluent rule not flagged: audit pipeline void"

    growth = {}
    for p in prescriptions:
        final, events = evolve("ABA", [("A", "AB")], p,
                               max_events=GROWTH_EVENTS,
                               rng=np.random.RandomState(SEED + 3))
        growth[p] = {"final_length": len(final),
                     "letter_counts": letter_counts(final),
                     "final_prefix": final[:40]}
    counts = [tuple(sorted(v["letter_counts"].items()))
              for v in growth.values()]
    assert len(set(counts)) == 1, \
        "conserved letter counts disagreed across prescriptions"
    arrangements = {v["final_prefix"] for v in growth.values()}
    arrangement_borne = len(arrangements) > 1

    record = {
        "schema": "wm2-prescription-v1",
        "label": "exploratory",
        "declared": {"seed": SEED, "prescriptions": prescriptions,
                     "string_length": RANDOM_STRING_LENGTH,
                     "growth_events": GROWTH_EVENTS},
        "sorting_rule": {
            "initial": initial, "inversions": inversions,
            "per_prescription": sorting,
            "exact_agreement": True,
            "statement": "the causal-invariant control agrees exactly, "
                "final string and event count, under every prescription",
        },
        "planted_trap": {
            "per_prescription": trap,
            "distinct_terminals": sorted(trap_finals),
            "flagged": trap_flagged,
            "statement": "the non-confluent rule's physics is "
                "prescription-borne and the pipeline flags it, the "
                "Cayley-trap obligation discharged",
        },
        "growth_rule": {
            "per_prescription": growth,
            "conserved_counts_agree": True,
            "arrangement_prescription_borne": bool(arrangement_borne),
            "statement": "conserved charges are prescription-invariant "
                "while the arrangement is prescription-borne, the "
                "signed-versus-unsigned split measured in rewriting form",
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
    output = Path(__file__).resolve().parents[1] / "results" \
        / "wm2-prescription.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print(f"sorting: exact agreement, {inversions} events "
          f"(= inversion number) under all prescriptions")
    print(f"trap: flagged, terminals {sorted(trap_finals)}")
    print(f"growth: counts agree {counts[0]}, arrangement "
          f"prescription-borne {arrangement_borne}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
