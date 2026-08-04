#!/usr/bin/env python3
"""WM-1 reversible-CA entropy cycle (exploratory, WM track).

The PE-2 protocol transplanted to a cellular automaton. The system is
a second-order reversible elementary CA,

    a(t+1) = F(a(t)) XOR a(t-1),

invertible by construction for any elementary rule F (run the same
update with the last two configurations swapped). F is Rule 30, the
Wolfram program's flagship pseudorandomizer. From an ordered seed the
coarse-grained block entropy of the configuration rises toward the
maximum; reversing exactly retraces the trajectory bitwise, and the
initial microstate is recovered exactly. The observed entropy growth
is therefore observational, produced entirely by the declared
coarse-graining, with zero information loss in the dynamics, which is
the campaign's PE-2 conclusion verbatim and the concrete content of
any second-law claim for reversible computational systems.

Coarse-graining declared before the run: non-overlapping blocks of 8
cells read as bytes, Shannon entropy of the empirical byte histogram
in bits per block. Exploratory label.
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

RULE = 30
WIDTH = 4096
STEPS = 400
BLOCK = 8


def rule_table(rule: int) -> np.ndarray:
    return np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)


def step_elementary(state: np.ndarray, table: np.ndarray) -> np.ndarray:
    left = np.roll(state, 1)
    right = np.roll(state, -1)
    idx = (left << 2) | (state << 1) | right
    return table[idx]


def block_entropy_bits(state: np.ndarray) -> float:
    blocks = state.reshape(-1, BLOCK)
    weights = 1 << np.arange(BLOCK - 1, -1, -1, dtype=np.uint32)
    codes = (blocks * weights).sum(axis=1)
    counts = np.bincount(codes, minlength=1 << BLOCK)
    p = counts[counts > 0] / codes.size
    return float(-(p * np.log2(p)).sum())


def main() -> int:
    table = rule_table(RULE)
    prev = np.zeros(WIDTH, dtype=np.uint8)
    curr = np.zeros(WIDTH, dtype=np.uint8)
    curr[WIDTH // 2] = 1
    seed_prev, seed_curr = prev.copy(), curr.copy()

    forward = [block_entropy_bits(curr)]
    for _ in range(STEPS):
        prev, curr = curr, step_elementary(curr, table) ^ prev
        forward.append(block_entropy_bits(curr))

    rev_prev, rev_curr = curr.copy(), prev.copy()
    reverse = [block_entropy_bits(rev_curr)]
    for _ in range(STEPS):
        rev_prev, rev_curr = rev_curr, \
            step_elementary(rev_curr, table) ^ rev_prev
        reverse.append(block_entropy_bits(rev_curr))

    retrace = max(abs(a - b) for a, b in
                  zip(reverse, forward[::-1], strict=True))
    recovered = (np.array_equal(rev_curr, seed_prev)
                 and np.array_equal(rev_prev, seed_curr))
    assert retrace == 0.0, "entropy curve failed to retrace exactly"
    assert recovered, "microstate not recovered exactly"
    rise = forward[-1] - forward[0]
    assert rise > 4.0, "entropy failed to rise from the ordered seed"

    record = {
        "schema": "wm1-reversible-ca-v1",
        "label": "exploratory",
        "declared": {"rule": RULE, "second_order": True, "width": WIDTH,
                     "steps": STEPS, "block": BLOCK,
                     "seed": "single centered 1 over zeros"},
        "entropy_initial_bits": forward[0],
        "entropy_final_bits": forward[-1],
        "entropy_rise_bits": rise,
        "forward_curve_every_20": forward[::20],
        "retrace_defect": retrace,
        "microstate_recovered_exactly": bool(recovered),
        "statement": "coarse-grained entropy of a manifestly reversible "
            "second-order CA rises from an ordered seed and retraces "
            "exactly under reversal with exact microstate recovery; the "
            "growth is observational, the PE-2 conclusion verbatim",
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
        / "wm1-reversible-ca.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print(f"entropy {forward[0]:.3f} -> {forward[-1]:.3f} bits "
          f"(rise {rise:.3f}); retrace defect {retrace}; microstate "
          f"recovered {recovered}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
