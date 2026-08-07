#!/usr/bin/env python3
"""UN-1, the removability discriminator.

Governed by PREREG-UN1-001.md, sealed at commit b549a29, blob
3c22bc0d0ed56369acae9b5da816a46381768c6b589ccbd799d006112e5ae317.

Every object here is fixed by that document. Nothing is fitted,
sampled, or optimized. The type II family is enumerated in full and
its conditional entropies are computed by exact summation over the
whole record space.
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

# prereg section 3
A_ANG = math.pi / 5.0
B_ANG = math.pi / 7.0
# prereg section 5
LADDER = [1, 2, 3, 4, 5, 6]
# prereg section 4, type II angle grid
NTHETA = 24
TINY = 1e-12
MU_BITS = 1.0            # -log2(1/2) for the declared incompatible pair

I2 = np.eye(2)
Z1 = np.diag([1.0, -1.0])
X1 = np.array([[0.0, 1.0], [1.0, 0.0]])


def qubit(angle):
    return np.array([math.cos(angle), math.sin(angle)])


def state_vector():
    return np.kron(qubit(A_ANG), qubit(B_ANG))


def shannon(ps):
    out = 0.0
    for p in ps:
        if p > 1e-15:
            out -= p * math.log2(p)
    return out


def basis_at(theta):
    """Orthonormal qubit basis on the great circle through Z and X.

    theta = 0 gives the Z eigenbasis, theta = pi/4 the X eigenbasis,
    which is the convention the grid of the prereg refers to.
    """
    c, s = math.cos(theta), math.sin(theta)
    return [np.array([c, s]), np.array([-s, c])]


def projs(basis):
    return [np.outer(v, v.conj()) for v in basis]


# ----------------------------------------------------------------- type I

def variance(op, psi):
    ev = float(psi @ (op @ psi))
    ev2 = float(psi @ (op @ op @ psi))
    return ev2 - ev * ev


def type1_cell(var_a, var_b, n, commuting):
    """Enumerate the declared split-fraction family and, for a
    commuting pair, the joint member. Returns (best, member, errs)."""
    members = []
    for k in range(0, n + 1):
        na, nb = k, n - k
        if na == 0 or nb == 0:
            err = float("inf")
        else:
            err = var_a / na + var_b / nb
        members.append(("split k=%d" % k, err))
    if commuting:
        members.append(("joint", var_a / n + var_b / n))
    best_name, best = min(members, key=lambda m: m[1])
    return best, best_name, members


# ---------------------------------------------------------------- type II

def sqrtm_psd(m):
    w, v = np.linalg.eigh(m)
    return (v * np.sqrt(np.clip(w.real, 0.0, None))) @ v.conj().T


def copy_instrument(theta):
    """Projective measurement of one two-qubit copy at a single
    declared angle.

    The sealed family gives one angle per copy, so the copy's basis
    is the product basis built from that angle on both qubits.
    Returns the four rank-one projectors on the 4-dimensional copy.
    """
    p = projs(basis_at(theta))
    return [np.kron(u, v) for u in p for v in p]


def type2_error(theta_first, theta_rest, n, pair_ops, rho1):
    """Sum of the two conditional entropies of the referee's outcome
    on copy one, given the full record of all n copies.

    The other copies are measured too and their outcomes are part of
    the record. Their contribution is summed over explicitly rather
    than argued away.
    """
    povm_first = copy_instrument(theta_first)
    povm_rest = copy_instrument(theta_rest)
    ref_a = pair_ops[0]
    ref_b = pair_ops[1]

    # post-measurement branches of copy one under the Lueders rule
    branches = []
    for m in povm_first:
        root = sqrtm_psd(m)
        post = root @ rho1 @ root
        p = float(np.real(np.trace(post)))
        if p <= 1e-15:
            branches.append((0.0, None))
            continue
        branches.append((p, post / p))

    # probabilities of the other copies' outcomes, on the same state
    rest_probs = [float(np.real(np.trace(m @ rho1))) for m in povm_rest]

    ha = hb = 0.0
    n_rest = n - 1
    seen_records = 0
    for idx, (p1, post) in enumerate(branches):
        if p1 <= 1e-15:
            continue
        ea = shannon([float(np.real(np.trace(post @ q))) for q in ref_a])
        eb = shannon([float(np.real(np.trace(post @ q))) for q in ref_b])
        # every combination of the remaining copies' outcomes
        for combo in itertools.product(range(4), repeat=n_rest):
            w = p1
            for c in combo:
                w *= rest_probs[c]
            if w <= 1e-15:
                continue
            seen_records += 1
            ha += w * ea
            hb += w * eb
    return ha + hb, seen_records


def type2_cell(n, pair_ops, rho1):
    grid = [j * math.pi / NTHETA for j in range(NTHETA + 1)]
    members = []
    # the trivial member reads nothing from any copy
    triv = [np.eye(4)]
    ha = hb = 0.0
    for m in triv:
        root = sqrtm_psd(m)
        post = root @ rho1 @ root
        p = float(np.real(np.trace(post)))
        post = post / p
        ha += p * shannon([float(np.real(np.trace(post @ q)))
                           for q in pair_ops[0]])
        hb += p * shannon([float(np.real(np.trace(post @ q)))
                           for q in pair_ops[1]])
    members.append(("trivial", ha + hb, 1))

    # one angle on copy one, a second on every other copy, both
    # ranging over the declared grid
    for tf in grid:
        for tr in grid:
            err, nrec = type2_error(tf, tr, n, pair_ops, rho1)
            members.append(("theta_first=%.6f,theta_rest=%.6f"
                            % (tf, tr), err, nrec))
    best = min(members, key=lambda m: m[1])
    # the record count that matters is the attaining member's
    return best[1], best[0], members, best[2]


def main() -> int:
    psi = state_vector()
    rho1 = np.outer(psi, psi)

    ZI = np.kron(Z1, I2)
    IZ = np.kron(I2, Z1)
    XI = np.kron(X1, I2)

    pairs = {
        "compatible_ZI_IZ": {"ops": (ZI, IZ), "commuting": True},
        "incompatible_ZI_XI": {"ops": (ZI, XI), "commuting": False},
    }
    # referee projectors for the type II task
    ref = {
        "compatible_ZI_IZ": (
            [np.kron(p, I2) for p in projs(basis_at(0.0))],
            [np.kron(I2, p) for p in projs(basis_at(0.0))]),
        "incompatible_ZI_XI": (
            [np.kron(p, I2) for p in projs(basis_at(0.0))],
            [np.kron(p, I2) for p in projs(basis_at(math.pi / 4))]),
    }

    cells = []
    for pname, pdef in pairs.items():
        va = variance(pdef["ops"][0], psi)
        vb = variance(pdef["ops"][1], psi)
        for n in LADDER:
            best, member, members = type1_cell(va, vb, n,
                                               pdef["commuting"])
            finite = sorted({round(m[1], 15) for m in members
                             if math.isfinite(m[1])})
            cells.append({
                "pair": pname, "task": "I_estimation", "N": n,
                "frontier": best, "attaining_member": member,
                "distinct_finite_members": len(finite),
                "records_nondegenerate": None,
                "variances": [va, vb]})

    for pname, pdef in pairs.items():
        for n in LADDER:
            best, member, members, nrec = type2_cell(n, ref[pname],
                                                     rho1)
            finite = sorted({round(m[1], 12) for m in members
                             if math.isfinite(m[1])})
            cells.append({
                "pair": pname, "task": "II_prediction", "N": n,
                "frontier": best, "attaining_member": member,
                "distinct_finite_members": len(finite),
                "records_nondegenerate": bool(nrec >= 2)})

    def cell(pair, task, n):
        for c in cells:
            if c["pair"] == pair and c["task"] == task and c["N"] == n:
                return c
        return None

    bars = {}
    detail = {}

    # bar 1, type I frontier times N constant across the ladder
    b1 = True
    b1_rows = []
    for pname in pairs:
        prods = [cell(pname, "I_estimation", n)["frontier"] * n
                 for n in LADDER]
        spread = max(prods) - min(prods)
        b1_rows.append({"pair": pname, "err_times_N": prods,
                        "spread": spread})
        if spread > TINY:
            b1 = False
    bars["bar1_type1_reciprocal"] = b1
    detail["bar1"] = b1_rows

    # bar 2, type I ratio finite and constant
    ratios = []
    for n in LADDER:
        ci = cell("incompatible_ZI_XI", "I_estimation", n)["frontier"]
        cc = cell("compatible_ZI_IZ", "I_estimation", n)["frontier"]
        ratios.append(ci / cc)
    r_spread = max(ratios) - min(ratios)
    bars["bar2_type1_ratio_constant"] = bool(
        all(math.isfinite(r) for r in ratios) and r_spread <= TINY)
    detail["bar2"] = {"ratios": ratios, "spread": r_spread}

    # bar 3, type II compatible reaches zero
    comp2 = [cell("compatible_ZI_IZ", "II_prediction", n)["frontier"]
             for n in LADDER]
    bars["bar3_type2_compatible_zero"] = bool(max(comp2) <= TINY)
    detail["bar3"] = {"frontiers": comp2, "max": max(comp2)}

    # bar 4, type II incompatible immobile and above the bound
    inc2 = [cell("incompatible_ZI_XI", "II_prediction", n)["frontier"]
            for n in LADDER]
    i_spread = max(inc2) - min(inc2)
    bars["bar4_type2_incompatible_immobile"] = bool(
        i_spread <= TINY and min(inc2) >= MU_BITS - 1e-9)
    detail["bar4"] = {"frontiers": inc2, "spread": i_spread,
                      "maassen_uffink": MU_BITS,
                      "gap_above_bound": min(inc2) - MU_BITS}

    # bar 5, anti-vacuity at every cell
    vac = []
    for c in cells:
        ok = (c["distinct_finite_members"] >= 3
              and c["attaining_member"] is not None
              and math.isfinite(c["frontier"]))
        if c["task"] == "II_prediction":
            ok = ok and bool(c["records_nondegenerate"])
        if not ok:
            vac.append({"pair": c["pair"], "task": c["task"],
                        "N": c["N"],
                        "distinct": c["distinct_finite_members"],
                        "records_nondegenerate":
                            c["records_nondegenerate"]})
    bars["bar5_anti_vacuity"] = bool(not vac)
    detail["bar5"] = {"failed_cells": vac,
                      "min_distinct_members": min(
                          c["distinct_finite_members"] for c in cells)}

    # bar 6, census
    expect = len(pairs) * 2 * len(LADDER)
    complete = all(math.isfinite(c["frontier"])
                   and c["attaining_member"] for c in cells)
    bars["bar6_census"] = bool(len(cells) == expect and complete)
    detail["bar6"] = {"expected_cells": expect, "found": len(cells)}

    verdict = "PASS" if all(bars.values()) else "FAIL"
    record = {
        "schema": "un1-discriminator-v1",
        "governed_by": {
            "prereg": "experiments/PREREG-UN1-001.md",
            "sealing_commit": "b549a29",
            "sealed_blob_sha256":
                "3c22bc0d0ed56369acae9b5da816a46381768c6b589ccbd7"
                "99d006112e5ae317"},
        "declared": {
            "state_angles": [A_ANG, B_ANG], "ladder": LADDER,
            "theta_grid_points": NTHETA + 1, "tolerance": TINY,
            "admissible_class": "the family of PREREG-UN1-001 "
                                "section 4, enumerated in full; every "
                                "floor below is a floor across that "
                                "family and nothing wider"},
        "cells": cells, "bar_detail": detail,
        "bars": {k: bool(v) for k, v in bars.items()},
        "verdict": {"value": verdict, "computed_from": sorted(bars)},
    }
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(), "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})

    out = Path(__file__).resolve().parents[1] / "results" \
        / "un1-discriminator.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")

    for k in sorted(bars):
        print("%-40s %s" % (k, "PASS" if bars[k] else "FAIL"))
    print("type I  err*N   ", [round(r["err_times_N"][0], 9)
                               for r in b1_rows])
    print("type II compat  ", [round(v, 15) for v in comp2])
    print("type II incompat", [round(v, 15) for v in inc2])
    print("VERDICT", verdict)
    print("record_sha256", record["record_sha256"][:16])
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
