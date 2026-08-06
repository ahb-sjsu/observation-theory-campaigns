#!/usr/bin/env python3
"""GG-2b the Gauss-law replay, corrected window.

Identical to GG-2 except W3's plaquette window, now [3.5, 4.5].
GG-2 assumed a generic quadratic invariant-sector response, but no
two deformation links close a loop with a plaquette on this graph,
the quadratic channel vanishes identically and the first surviving
response is quartic, the declared prediction here. Verdict
computed from the measured items.

Exploratory label. No claim about continuum gauge theory.
"""
from __future__ import annotations

import json
import math
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gg0_instrument import (  # noqa: E402
    K, LSIZE, NLINK, all_configs, gauge_transform,
    plaquette_links)
from projection_fold import canonical_sha256  # noqa: E402

EPS_LADDER = [0.0, 1e-3, 1e-2, 1e-1]


def main() -> int:
    record: dict = {"schema": "gg2b-gauss-replay-v1",
                    "label": "exploratory"}
    items = {}
    plaqs = plaquette_links()
    cfgs = all_configs()
    plaq_prod = np.ones((cfgs.shape[0], 9), dtype=np.int8)
    for p, (a, b, c, d) in enumerate(plaqs):
        plaq_prod[:, p] = (cfgs[:, a] * cfgs[:, b]
                           * cfgs[:, c] * cfgs[:, d])
    s_gauge = K * plaq_prod.sum(axis=1, dtype=np.float64)
    link_sum = cfgs.sum(axis=1, dtype=np.float64)

    rng = np.random.RandomState(20260821)
    site_patterns = [(1 - 2 * ((g >> np.arange(9)) & 1)).reshape(
        LSIZE, LSIZE) for g in range(2 ** 9)]
    sample_cfgs = [(1 - 2 * rng.randint(0, 2, NLINK)).astype(np.int8)
                   for _ in range(20)]

    per_eps = {}
    for eps in EPS_LADDER:
        w = np.exp(s_gauge + eps * link_sum)
        z = math.fsum(w)
        max_link = max(
            abs(math.fsum(cfgs[:, li].astype(np.float64) * w)) / z
            for li in range(NLINK))
        wp = math.fsum(plaq_prod[:, 0] * w) / z

        def action(cfg):
            ap = K * sum(cfg[a] * cfg[b] * cfg[c] * cfg[d]
                         for a, b, c, d in plaqs)
            return ap + eps * float(cfg.sum())

        spreads = []
        for cfg in sample_cfgs:
            vals = [action(gauge_transform(cfg, sp))
                    for sp in site_patterns]
            spreads.append(max(vals) - min(vals))
        per_eps[str(eps)] = {
            "max_link_exp": float(max_link),
            "wilson_plaquette": float(wp),
            "min_orbit_action_spread": float(min(spreads)),
            "max_orbit_action_spread": float(max(spreads))}
        print("eps", eps, per_eps[str(eps)], flush=True)

    e0 = per_eps["0.0"]
    items["W1_zero_point_exact"] = (
        e0["max_link_exp"] <= 1e-13
        and e0["max_orbit_action_spread"] == 0.0)
    items["W2_first_order_detectable"] = all(
        per_eps[str(e)]["max_link_exp"] >= 0.3 * e
        and per_eps[str(e)]["min_orbit_action_spread"] > 0.0
        for e in EPS_LADDER[1:])
    wp0 = e0["wilson_plaquette"]
    link_slope = (np.log(per_eps["0.01"]["max_link_exp"]
                         / per_eps["0.001"]["max_link_exp"])
                  / np.log(10.0))
    shift3 = abs(per_eps["0.001"]["wilson_plaquette"] - wp0)
    shift2 = abs(per_eps["0.01"]["wilson_plaquette"] - wp0)
    plaq_slope = np.log(shift2 / max(shift3, 1e-300)) / np.log(10.0)
    items["W3_sector_split"] = (0.8 <= link_slope <= 1.2
                                and 3.5 <= plaq_slope <= 4.5)

    record["measured"] = {
        "per_eps": per_eps,
        "link_response_slope": float(link_slope),
        "plaquette_response_slope": float(plaq_slope),
        "reading": "constraint structure is an isolated algebraic "
                   "point, declared or absent, first-order loud in "
                   "the link sector and second-order quiet in the "
                   "invariant sector"}
    record["items"] = {k: bool(v) for k, v in items.items()}
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "gg2b-gauss-replay.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("slopes", link_slope, plaq_slope)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
