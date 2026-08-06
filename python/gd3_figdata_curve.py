#!/usr/bin/env python3
"""Auxiliary figure-data run for the games-decisions paper.

Recomputes only the GD-3 P2 weighting curve at the declared budget
sigma 1.0, under the declared symmetric environment and the declared
shifted environment, using the committed GD-3 instrument unchanged,
and writes the downsampled curve as a committed artifact so the paper
can plot it. No verdict, no bars, no new measurement. A consistency
item ties the artifact to the sealed GD-3 record, the recomputed
maximum deviation from the identity at sigma 1.0 must match the
parent record's value.

Exploratory label. No claim about human beings.
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

from gd3_prospect_signatures import channel_weight  # noqa: E402
from projection_fold import canonical_sha256  # noqa: E402

KEEP_EVERY = 10
SIGMA = 1.0
TAU2 = 1.5


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parent_path = root / "results" / "gd3-prospect-signatures.json"
    parent = json.loads(parent_path.read_text(encoding="utf-8"))

    lgrid = np.round(np.arange(-6.0, 6.0 + 1e-9, 0.01), 10)
    mgrid = np.round(np.arange(-9.0, 9.0 + 1e-9, 0.01), 10)
    prior = np.exp(-0.5 * lgrid ** 2 / TAU2)
    prior /= prior.sum()
    prior_shift = np.exp(-0.5 * (lgrid + 1.0) ** 2 / TAU2)
    prior_shift /= prior_shift.sum()
    pvals = 1.0 / (1.0 + np.exp(-lgrid))

    w_sym = channel_weight(lgrid, prior, pvals, SIGMA, mgrid)
    w_shift = channel_weight(lgrid, prior_shift, pvals, SIGMA, mgrid)

    max_dev = float(np.max(np.abs(w_sym - pvals)))
    parent_dev = float(parent["P2"]["max_dev_from_identity"][0])
    assert abs(max_dev - parent_dev) < 1e-12, \
        f"curve inconsistent with sealed record: {max_dev} vs {parent_dev}"

    keep = sorted(set(range(0, len(lgrid), KEEP_EVERY))
                  | {len(lgrid) - 1})
    points = [[float(pvals[i]), float(w_sym[i]), float(w_shift[i])]
              for i in keep]

    record: dict = {
        "schema": "gd3-figdata-curve-v1",
        "label": "exploratory",
        "purpose": "figure data only, the GD-3 P2 curve at sigma 1.0 "
                   "recomputed by the committed instrument for the "
                   "games-decisions paper, no verdict and no bar",
        "parent_record": "results/gd3-prospect-signatures.json",
        "parent_sha256": parent["record_sha256"],
        "declared": {"sigma": SIGMA, "tau2": TAU2,
                     "grid_step": 0.01, "keep_every": KEEP_EVERY,
                     "shifted_prior_mean_logodds": -1.0},
        "columns": ["p", "w_symmetric_env", "w_shifted_env"],
        "points": points,
        "consistency": {"max_dev_from_identity_sigma1": max_dev,
                        "parent_value": parent_dev},
    }
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = root / "results" / "gd3-figdata-curve.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print(f"points {len(points)} max_dev {max_dev}")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
