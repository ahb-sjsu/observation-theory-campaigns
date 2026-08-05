#!/usr/bin/env python3
"""PE-5 classical consumer hierarchy (exploratory, PE track).

Consumers read the double-fold projection t = tau^3 - tau with
increasing access: binned observed time only; time plus the branch
orientation sign(dt/dtau); time plus the full branch label. The
double fold is the right system because its three branches carry only
two orientations (the outer branches share sign), so the three rungs
are genuinely distinct. With the hidden state uniform on a declared
tau grid (resolution delta) and observed time binned at epsilon, all
conditional entropies are exact finite sums, and the lawful ordering

  H(Z | pos) >= H(Z | pos, orient) >= H(Z | pos, branch) >= 0

is the classical shadow of the QO-1 degradation chain. The gaps
measure what each additional observable is worth, and the branch rung
does not reach zero because a branch is an interval of hidden states,
not a point, which is the finite-resolution residual the QO paper's
classical reduction cites.

Exploratory label.
"""
from __future__ import annotations

import json
import math
import os
import platform
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402

TAU_LIM = 1.6
DELTA = 1e-4
EPSILON = 0.05


def branch_label(tau: float) -> int:
    third = 1.0 / math.sqrt(3.0)
    if tau < -third:
        return 0
    if tau <= third:
        return 1
    return 2


def main() -> int:
    taus = np.arange(-TAU_LIM, TAU_LIM + DELTA / 2, DELTA)
    ts = taus**3 - taus
    orients = np.sign(3.0 * taus**2 - 1.0).astype(int)
    branches = np.array([branch_label(x) for x in taus])
    bins = np.floor(ts / EPSILON).astype(int)

    def conditional_entropy(keys) -> float:
        groups = defaultdict(int)
        for k in keys:
            groups[k] += 1
        n = len(keys)
        h = 0.0
        for count in groups.values():
            h += (count / n) * math.log2(count)
        return h  # sum p(group) * log2 |group|, uniform within groups

    h_pos = conditional_entropy(list(bins))
    h_orient = conditional_entropy(list(zip(bins, orients, strict=True)))
    h_branch = conditional_entropy(list(zip(bins, branches, strict=True)))
    h_full = 0.0

    assert h_pos >= h_orient - 1e-12, "ordering violated: pos vs orient"
    assert h_orient >= h_branch - 1e-12, "ordering violated: orient vs branch"
    assert h_branch > h_full, "branch rung should not reach zero"
    gap_orient = h_pos - h_orient
    gap_branch = h_orient - h_branch
    assert gap_orient > 0.01, "orientation should carry information here"
    assert gap_branch > 0.01, \
        "branch label should exceed orientation (outer branches share sign)"

    record = {
        "schema": "pe5-hierarchy-v1",
        "label": "exploratory",
        "declared": {"map": "t = tau^3 - tau", "tau_limit": TAU_LIM,
                     "delta": DELTA, "epsilon": EPSILON,
                     "hidden_measure": "uniform on the tau grid"},
        "chain_bits": {"H_given_pos": h_pos,
                       "H_given_pos_orient": h_orient,
                       "H_given_pos_branch": h_branch,
                       "H_given_full": h_full},
        "gaps_bits": {"orientation_worth": gap_orient,
                      "branch_worth_beyond_orientation": gap_branch,
                      "finite_resolution_residual": h_branch},
        "statement": "the lawful ordering holds with strictly positive "
            "gaps at every rung; orientation resolves the middle branch "
            "but not the outer pair, the branch label resolves all "
            "three, and the residual is the within-branch positional "
            "uncertainty set by delta and epsilon, the classical shadow "
            "of the QO-1 chain",
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
        / "pe5-hierarchy.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print(f"H(Z|pos) {h_pos:.4f} >= H(Z|pos,orient) {h_orient:.4f} >= "
          f"H(Z|pos,branch) {h_branch:.4f} >= 0 bits")
    print(f"gaps: orientation worth {gap_orient:.4f}, branch beyond "
          f"orientation {gap_branch:.4f}, residual {h_branch:.4f}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
