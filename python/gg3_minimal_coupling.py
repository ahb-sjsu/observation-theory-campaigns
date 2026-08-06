#!/usr/bin/env python3
"""GG-3 the minimal-coupling audit (exploratory).

Protocol declared in GAUGE-TRACK.md before this run. Z2 matter
minimally coupled to Z2 links. The unitary-gauge identity maps the
coupled model onto the GG-2 deformed ensemble, verified exactly on
the small torus, Elitzur for matter holds, only dressed
observables exist, and the observer family's bare readings are
fiber coordinates. Verdict computed from the measured items.

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

from gg0_instrument import all_configs, plaquette_links  # noqa: E402
from projection_fold import canonical_sha256  # noqa: E402

KG = 0.4
J = 0.1


def small_torus():
    """2x2 torus, 4 sites, 8 links, 4 plaquettes."""
    def li(kind, i, j):
        return kind * 4 + i * 2 + j
    links = []
    for i in range(2):
        for j in range(2):
            links.append((li(0, i, j), (i, j), (i, (j + 1) % 2)))
            links.append((li(1, i, j), (i, j), ((i + 1) % 2, j)))
    plaqs = []
    for i in range(2):
        for j in range(2):
            plaqs.append([li(0, i, j), li(1, i, (j + 1) % 2),
                          li(0, (i + 1) % 2, j), li(1, i, j)])
    return links, plaqs


def main() -> int:
    record: dict = {"schema": "gg3-minimal-coupling-v1",
                    "label": "exploratory"}
    items = {}
    links, plaqs = small_torus()
    site_id = {(i, j): i * 2 + j for i in range(2)
               for j in range(2)}

    # full enumeration over 2^8 links x 2^4 matter
    lu = np.arange(2 ** 8)
    u = (1 - 2 * ((lu[:, None] >> np.arange(8)) & 1)).astype(
        np.int8)
    ls = np.arange(2 ** 4)
    sig = (1 - 2 * ((ls[:, None] >> np.arange(4)) & 1)).astype(
        np.int8)
    plaq_sum = np.zeros(2 ** 8)
    for p in plaqs:
        plaq_sum += (u[:, p[0]] * u[:, p[1]] * u[:, p[2]]
                     * u[:, p[3]]).astype(np.float64)
    coup = np.zeros((2 ** 8, 2 ** 4))
    for idx, a, b in links:
        coup += (u[:, idx].astype(np.float64)[:, None]
                 * (sig[:, site_id[a]]
                    * sig[:, site_id[b]]).astype(
                     np.float64)[None, :])
    w_full = np.exp(KG * plaq_sum[:, None] + J * coup)
    z_full = math.fsum(w_full.ravel())

    # unitary-gauge route, the deformed pure-link ensemble
    w_def = np.exp(KG * plaq_sum
                   + J * u.sum(axis=1, dtype=np.float64))
    z_def = math.fsum(w_def)
    dev_z = abs(z_full / (16.0 * z_def) - 1.0)

    l0, a0, b0 = links[0]
    s_a, s_b = site_id[a0], site_id[b0]
    dressed_full = math.fsum(
        (w_full * (u[:, l0].astype(np.float64)[:, None]
                   * (sig[:, s_a] * sig[:, s_b]).astype(
                       np.float64)[None, :])).ravel()) / z_full
    dressed_def = math.fsum(w_def * u[:, l0]) / z_def
    items["N1_unitary_gauge_identity"] = (
        dev_z <= 1e-12
        and abs(dressed_full - dressed_def) <= 1e-12)

    bare_full = math.fsum(
        (w_full * (sig[:, s_a] * sig[:, s_b]).astype(
            np.float64)[None, :]).ravel()) / z_full

    # 3x3 torus through the unitary-gauge identity
    cfgs9 = all_configs()
    plaqs9 = plaquette_links()
    ps9 = np.zeros(cfgs9.shape[0])
    for a, b, c, d in plaqs9:
        ps9 += (cfgs9[:, a] * cfgs9[:, b] * cfgs9[:, c]
                * cfgs9[:, d]).astype(np.float64)
    w9 = np.exp(KG * ps9 + J * cfgs9.sum(axis=1,
                                         dtype=np.float64))
    z9 = math.fsum(w9)
    dressed_3x3 = math.fsum(w9 * cfgs9[:, 0]) / z9
    items["N2_elitzur_for_matter"] = (
        abs(bare_full) <= 1e-13
        and dressed_full >= 0.01 and dressed_3x3 >= 0.01)

    # N3 observer family on the small torus
    # unitary observer, slice sigma identically +1
    w_unit = w_full[:, 0]
    z_unit = math.fsum(w_unit)
    bare_unit = 1.0
    dressed_unit = math.fsum(w_unit * u[:, l0]) / z_unit
    # tree observer, fix a spanning tree of links to +1, sigma free
    # h(0,0): (0,0)-(0,1); v(0,0): (0,0)-(1,0); v(0,1): (0,1)-(1,1)
    tree = [links[0][0], links[1][0], links[3][0]]
    mask = np.ones(2 ** 8, dtype=bool)
    for tl in tree:
        mask &= u[:, tl] == 1
    w_tree = w_full[mask]
    z_tree = math.fsum(w_tree.ravel())
    bare_tree = math.fsum(
        (w_tree * (sig[:, s_a] * sig[:, s_b]).astype(
            np.float64)[None, :]).ravel()) / z_tree
    dressed_tree = math.fsum(
        (w_tree * (u[mask][:, l0].astype(np.float64)[:, None]
                   * (sig[:, s_a] * sig[:, s_b]).astype(
                       np.float64)[None, :])).ravel()) / z_tree
    spread = abs(bare_unit - bare_tree)
    dev_dressed = max(abs(dressed_unit - dressed_full),
                      abs(dressed_tree - dressed_full))
    items["N3_observer_family"] = (spread >= 0.1
                                   and dev_dressed <= 1e-12)

    record["measured"] = {
        "z_ratio_dev": float(dev_z),
        "dressed_full_2x2": float(dressed_full),
        "dressed_def_2x2": float(dressed_def),
        "bare_full_2x2": float(bare_full),
        "dressed_3x3": float(dressed_3x3),
        "bare_unit_observer": float(bare_unit),
        "bare_tree_observer": float(bare_tree),
        "observer_bare_spread": float(spread),
        "dressed_agreement_dev": float(dev_dressed),
        "reading": "matter coupled to gauge carries no "
                   "observer-independent bare identity, every "
                   "invariant fact about charge is a statement "
                   "about lines, the observers' bare readings are "
                   "their fiber coordinates"}
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
        / "gg3-minimal-coupling.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("dressed", dressed_full, dressed_3x3,
          "bare spread", spread)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
