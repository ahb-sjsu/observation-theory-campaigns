#!/usr/bin/env python3
"""UN-1b, the removability discriminator, corrected.

Governed by PREREG-UN1-002.md, sealed at commit ce0b05a, blob
f1e1ac999210f42b2820243d976ae16c3fba135bc64ab9120328abb659b7c25d.

Supersedes un1_discriminator.py, whose record stays committed at
results/un1-discriminator.json with its four failed bars. Writes a
new path, per the campaign's rule that a rerun never overwrites a
committed record.
"""
from __future__ import annotations

import itertools
import json
import math
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402

# prereg section 4
A_ANG = math.pi / 5.0
B_ANG = math.pi / 7.0
# prereg section 6, two ladders and the boundary case
LADDER_I = [4, 8, 16, 32, 64, 128]
LADDER_II = [1, 2, 3, 4, 5, 6]
BOUNDARY_N = 1
ANCHOR_N = 4
# prereg section 5
NTHETA = 24
# prereg section 7
TOL_ZERO = 1e-12
TOL_DRIFT = 1e-11
MU_BITS = 1.0

I2 = np.eye(2)
Z1 = np.diag([1.0, -1.0])
X1 = np.array([[0.0, 1.0], [1.0, 0.0]])


def qubit(a):
    return np.array([math.cos(a), math.sin(a)])


def shannon(ps):
    out = 0.0
    for p in ps:
        if p > 1e-15:
            out -= p * math.log2(p)
    return out


def basis_at(theta):
    c, s = math.cos(theta), math.sin(theta)
    return [np.array([c, s]), np.array([-s, c])]


def projs(basis):
    return [np.outer(v, v.conj()) for v in basis]


def sqrtm_psd(m):
    w, v = np.linalg.eigh(m)
    return (v * np.sqrt(np.clip(w.real, 0.0, None))) @ v.conj().T


def variance(op, psi):
    ev = float(psi @ (op @ psi))
    ev2 = float(psi @ (op @ op @ psi))
    return ev2 - ev * ev


# ----------------------------------------------------------------- type I

def type1_cell(var_a, var_b, n, commuting):
    members = []
    for k in range(0, n + 1):
        na, nb = k, n - k
        err = (float("inf") if na == 0 or nb == 0
               else var_a / na + var_b / nb)
        members.append(("split k=%d" % k, err))
    if commuting:
        members.append(("joint", var_a / n + var_b / n))
    name, best = min(members, key=lambda m: m[1])
    finite = sorted({round(m[1], 15) for m in members
                     if math.isfinite(m[1])})
    return best, name, len(finite)


# ---------------------------------------------------------------- type II

def copy_instrument(theta):
    p = projs(basis_at(theta))
    return [np.kron(u, v) for u in p for v in p]


def type2_error(theta_first, theta_rest, n, ref, rho1):
    """Sum of the two conditional entropies of the referee's outcome
    on copy one given the full record over all n copies. The other
    copies' outcomes are summed over explicitly."""
    povm_first = copy_instrument(theta_first)
    rest_probs = [float(np.real(np.trace(m @ rho1)))
                  for m in copy_instrument(theta_rest)]

    branches = []
    for m in povm_first:
        root = sqrtm_psd(m)
        post = root @ rho1 @ root
        p = float(np.real(np.trace(post)))
        branches.append((p, None if p <= 1e-15 else post / p))

    total = 0.0
    live_records = 0
    for p1, post in branches:
        if p1 <= 1e-15:
            continue
        ea = shannon([float(np.real(np.trace(post @ q)))
                      for q in ref[0]])
        eb = shannon([float(np.real(np.trace(post @ q)))
                      for q in ref[1]])
        for combo in itertools.product(range(4), repeat=n - 1):
            w = p1
            for c in combo:
                w *= rest_probs[c]
            if w <= TOL_ZERO:
                continue
            live_records += 1
            total += w * (ea + eb)
    return total, live_records


def type2_cell(n, ref, rho1):
    grid = [j * math.pi / NTHETA for j in range(NTHETA + 1)]
    members = []

    root = sqrtm_psd(np.eye(4))
    post = root @ rho1 @ root
    p = float(np.real(np.trace(post)))
    post = post / p
    triv = (shannon([float(np.real(np.trace(post @ q)))
                     for q in ref[0]])
            + shannon([float(np.real(np.trace(post @ q)))
                       for q in ref[1]]))
    members.append(("trivial", triv, 1))

    for tf in grid:
        for tr in grid:
            err, live = type2_error(tf, tr, n, ref, rho1)
            members.append(("theta_first=%.6f,theta_rest=%.6f"
                            % (tf, tr), err, live))
    name, best, live = min(members, key=lambda m: m[1])
    finite = sorted({round(m[1], 12) for m in members
                     if math.isfinite(m[1])})
    return best, name, len(finite), live


def main() -> int:
    psi = np.kron(qubit(A_ANG), qubit(B_ANG))
    rho1 = np.outer(psi, psi)
    ZI, IZ, XI = (np.kron(Z1, I2), np.kron(I2, Z1), np.kron(X1, I2))

    pairs = {
        "compatible_ZI_IZ": {"ops": (ZI, IZ), "commuting": True},
        "incompatible_ZI_XI": {"ops": (ZI, XI), "commuting": False},
    }
    ref = {
        "compatible_ZI_IZ": (
            [np.kron(q, I2) for q in projs(basis_at(0.0))],
            [np.kron(I2, q) for q in projs(basis_at(0.0))]),
        "incompatible_ZI_XI": (
            [np.kron(q, I2) for q in projs(basis_at(0.0))],
            [np.kron(q, I2) for q in projs(basis_at(math.pi / 4))]),
    }

    var = {}
    cont = {}
    for pn, pd in pairs.items():
        va, vb = (variance(pd["ops"][0], psi),
                  variance(pd["ops"][1], psi))
        var[pn] = (va, vb)
        # prereg section 7, the continuum optima
        cont[pn] = (va + vb if pd["commuting"]
                    else (math.sqrt(va) + math.sqrt(vb)) ** 2)

    cells = []
    for pn, pd in pairs.items():
        for n in LADDER_I:
            best, name, ndist = type1_cell(*var[pn], n,
                                           pd["commuting"])
            cells.append({"pair": pn, "task": "I_estimation", "N": n,
                          "frontier": best, "attaining_member": name,
                          "distinct_finite_members": ndist,
                          "records_live": None})
    for pn in pairs:
        for n in LADDER_II:
            best, name, ndist, live = type2_cell(n, ref[pn], rho1)
            cells.append({"pair": pn, "task": "II_prediction",
                          "N": n, "frontier": best,
                          "attaining_member": name,
                          "distinct_finite_members": ndist,
                          "records_live": live})

    boundary = {}
    for pn, pd in pairs.items():
        best, name, ndist = type1_cell(*var[pn], BOUNDARY_N,
                                       pd["commuting"])
        boundary[pn] = {"frontier": best, "attaining_member": name,
                        "finite": bool(math.isfinite(best))}

    def cell(pair, task, n):
        for c in cells:
            if (c["pair"] == pair and c["task"] == task
                    and c["N"] == n):
                return c
        return None

    bars, detail = {}, {}

    # bar 1
    b1_ok, rows = True, []
    for pn in pairs:
        C = cont[pn]
        row = []
        for n in LADDER_I:
            v = cell(pn, "I_estimation", n)["frontier"] * n
            lo, hi = C, C * (1.0 + 2.0 / n)
            ok = (v >= lo - 1e-15) and (v <= hi + 1e-15)
            row.append({"N": n, "err_times_N": v, "lo": lo, "hi": hi,
                        "in_band": bool(ok)})
            if not ok:
                b1_ok = False
        rows.append({"pair": pn, "continuum_optimum": C,
                     "rungs": row})
    bars["bar1_type1_reciprocal_band"] = b1_ok
    detail["bar1"] = rows

    # bar 2
    ratios = []
    for n in LADDER_I:
        ci = cell("incompatible_ZI_XI", "I_estimation", n)["frontier"]
        cc = cell("compatible_ZI_IZ", "I_estimation", n)["frontier"]
        ratios.append({"N": n, "ratio": ci / cc})
    target = cont["incompatible_ZI_XI"] / cont["compatible_ZI_IZ"]
    top = ratios[-1]["ratio"]
    rel = abs(top - target) / target
    bars["bar2_type1_ratio_bounded"] = bool(
        all(math.isfinite(r["ratio"]) for r in ratios)
        and all(r["ratio"] <= 1.5 for r in ratios if r["N"] >= 8)
        and rel <= 0.02)
    detail["bar2"] = {"ratios": ratios, "asymptotic_target": target,
                      "top_rung_relative_gap": rel}

    # bar 3
    comp2 = [cell("compatible_ZI_IZ", "II_prediction", n)["frontier"]
             for n in LADDER_II]
    bars["bar3_type2_compatible_zero"] = bool(max(comp2) <= TOL_ZERO)
    detail["bar3"] = {"frontiers": comp2, "max": max(comp2)}

    # bar 4
    inc2 = [cell("incompatible_ZI_XI", "II_prediction",
                 n)["frontier"] for n in LADDER_II]
    spread = max(inc2) - min(inc2)
    bars["bar4_type2_incompatible_immobile"] = bool(
        spread <= TOL_DRIFT and min(inc2) >= MU_BITS - 1e-9)
    detail["bar4"] = {"frontiers": inc2, "spread": spread,
                      "tolerance": TOL_DRIFT,
                      "maassen_uffink": MU_BITS,
                      "gap_above_bound": min(inc2) - MU_BITS}

    # bar 5
    vac = []
    for c in cells:
        ok = (c["distinct_finite_members"] >= 3
              and c["attaining_member"] is not None
              and math.isfinite(c["frontier"]))
        if c["task"] == "II_prediction":
            ok = ok and (c["records_live"] or 0) >= 2
        if not ok:
            vac.append({k: c[k] for k in
                        ("pair", "task", "N",
                         "distinct_finite_members", "records_live")})
    bars["bar5_anti_vacuity"] = bool(not vac)
    detail["bar5"] = {"failed_cells": vac,
                      "min_distinct_members":
                          min(c["distinct_finite_members"]
                              for c in cells),
                      "min_live_records":
                          min(c["records_live"] for c in cells
                              if c["records_live"] is not None)}

    # bar 6
    expect = len(pairs) * (len(LADDER_I) + len(LADDER_II))
    bars["bar6_census"] = bool(
        len(cells) == expect
        and all(math.isfinite(c["frontier"]) and c["attaining_member"]
                for c in cells)
        and len(boundary) == len(pairs))
    detail["bar6"] = {"expected_cells": expect, "found": len(cells),
                      "boundary_cells": len(boundary)}

    # bar 7
    bars["bar7_boundary"] = bool(
        boundary["compatible_ZI_IZ"]["finite"]
        and not boundary["incompatible_ZI_XI"]["finite"])
    detail["bar7"] = {
        "compatible_finite": boundary["compatible_ZI_IZ"]["finite"],
        "incompatible_finite":
            boundary["incompatible_ZI_XI"]["finite"],
        "reading": "at one copy the declared family cannot serve two "
                   "non-commuting estimation tasks at all"}

    # the anchor rung, reported not barred
    detail["anchor"] = {
        "N": ANCHOR_N,
        "cells": [{k: c[k] for k in ("pair", "task", "frontier")}
                  for c in cells if c["N"] == ANCHOR_N]}

    verdict = "PASS" if all(bars.values()) else "FAIL"
    record = {
        "schema": "un1b-discriminator-v1",
        "governed_by": {
            "prereg": "experiments/PREREG-UN1-002.md",
            "sealing_commit": "ce0b05a",
            "sealed_blob_sha256":
                "f1e1ac999210f42b2820243d976ae16c3fba135bc64ab912"
                "0328abb659b7c25d",
            "supersedes": "results/un1-discriminator.json"},
        "declared": {
            "state_angles": [A_ANG, B_ANG],
            "ladder_type1": LADDER_I, "ladder_type2": LADDER_II,
            "boundary_N": BOUNDARY_N, "anchor_N": ANCHOR_N,
            "theta_grid_points": NTHETA + 1,
            "variances": {k: list(v) for k, v in var.items()},
            "continuum_optima": cont,
            "admissible_class": "the family of PREREG-UN1-002 "
                                "section 5, enumerated in full; every "
                                "floor here is a floor across that "
                                "family and nothing wider"},
        "cells": cells, "boundary": boundary, "bar_detail": detail,
        "bars": {k: bool(v) for k, v in bars.items()},
        "verdict": {"value": verdict, "computed_from": sorted(bars)},
    }

    def jsonsafe(v):
        if isinstance(v, float):
            if math.isinf(v):
                return {"__nonfinite__": "inf" if v > 0 else "-inf"}
            if math.isnan(v):
                return {"__nonfinite__": "nan"}
            return v
        if isinstance(v, dict):
            return {k: jsonsafe(x) for k, x in v.items()}
        if isinstance(v, list):
            return [jsonsafe(x) for x in v]
        return v

    record = jsonsafe(record)
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(), "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})

    out = Path(__file__).resolve().parents[1] / "results" \
        / "un1b-discriminator.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")

    for k in sorted(bars):
        print("%-42s %s" % (k, "PASS" if bars[k] else "FAIL"))
    for r in detail["bar1"]:
        print("  %s  err*N %s" % (
            r["pair"][:20],
            [round(x["err_times_N"], 9) for x in r["rungs"]]))
    print("  ratios      ", [round(r["ratio"], 9) for r in ratios])
    print("  type II comp", [round(v, 15) for v in comp2])
    print("  type II inc ", [round(v, 15) for v in inc2])
    print("  boundary N=1", {k: v["finite"]
                             for k, v in boundary.items()})
    print("VERDICT", verdict)
    print("record_sha256", record["record_sha256"][:16])
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
