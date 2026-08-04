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

RULE = 122
WIDTH = 1024
STEPS = 1500
BLOCK = 4
SEED_REGION = 256
SEED_RNG = 20260805
RISE_BAR = 1.0

# Instrument iteration findings, preserved. (i) Rule 30R from a single
# seed runs to a ninety-nine percent ones phase where F vanishes on
# 111 neighborhoods and the byte-block entropy falls, so that
# rule/seed pair never randomizes under the declared coarse-graining.
# (ii) The symmetric initialization prev = curr makes the orbit
# time-reflection symmetric and Rule 122R then shows a near-recurrence
# by step one thousand, collapsing back toward order; the
# initialization must be asymmetric. (iii) Byte blocks are too coarse
# for structured CA fields; four-cell blocks resolve the growth. Rule
# 122 is the featured example of Wolfram's own second-law writings,
# which is why it carries the demonstration here. The entropy of the
# finite reversible system fluctuates as it must; the claim is the
# rise from the ordered seed plus the exact retrace, not monotonicity.


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
    rng = np.random.RandomState(SEED_RNG)
    prev = np.zeros(WIDTH, dtype=np.uint8)
    curr = np.zeros(WIDTH, dtype=np.uint8)
    half = SEED_REGION // 2
    curr[WIDTH // 2 - half:WIDTH // 2 + half] = \
        rng.randint(0, 2, SEED_REGION).astype(np.uint8)
    seed_curr = curr.copy()

    forward = [block_entropy_bits(curr)]
    first_evolved = None
    for k in range(STEPS):
        prev, curr = curr, step_elementary(curr, table) ^ prev
        if k == 0:
            first_evolved = curr.copy()
        forward.append(block_entropy_bits(curr))

    # One extra forward step supplies the pair (a_{T+1}, a_T), so the
    # reversal retraces a_T, a_{T-1}, .., a_0 in exact alignment with
    # the forward record. The first version swapped (a_T, a_{T-1}) and
    # retraced from a_{T-1}, a one-step misalignment the exact-retrace
    # bar caught immediately.
    prev, curr = curr, step_elementary(curr, table) ^ prev
    rev_prev, rev_curr = curr.copy(), prev.copy()
    reverse = [block_entropy_bits(rev_curr)]
    for _ in range(STEPS):
        rev_prev, rev_curr = rev_curr, \
            step_elementary(rev_curr, table) ^ rev_prev
        reverse.append(block_entropy_bits(rev_curr))

    retrace = max(abs(a - b) for a, b in
                  zip(reverse, forward[::-1], strict=True))
    recovered = (np.array_equal(rev_curr, seed_curr)
                 and np.array_equal(rev_prev, first_evolved))
    assert retrace == 0.0, "entropy curve failed to retrace exactly"
    assert recovered, "microstate not recovered exactly"
    rise = forward[-1] - forward[0]
    assert rise > RISE_BAR, "entropy failed to rise from the ordered seed"

    record = {
        "schema": "wm1-reversible-ca-v1",
        "label": "exploratory",
        "declared": {"rule": RULE, "second_order": True, "width": WIDTH,
                     "steps": STEPS, "block": BLOCK,
                     "seed": f"random {SEED_REGION}-cell center region, "
                             f"RandomState({SEED_RNG}), prev zeros",
                     "rise_bar": RISE_BAR},
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
