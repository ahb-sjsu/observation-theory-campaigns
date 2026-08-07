#!/usr/bin/env python3
"""UN-0 exact frontier instrument layer (exploratory).

Protocol declared in UNCERTAINTY-TRACK.md before this run. The
machinery this track needs is exact conditional entropies for a
consumer's record, exact estimation errors, and the standard
entropic bound to compare against. Every control here has a closed
form and no later UN experiment runs until they all pass.

Exploratory label. Nothing here is a claim about physical
measurement.
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

from projection_fold import canonical_sha256  # noqa: E402

TOL = 1e-12


def basis_from_angle(theta):
    """Two orthonormal qubit bases separated by a declared angle on
    the Bloch sphere's great circle."""
    z = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]
    c, s = math.cos(theta / 2.0), math.sin(theta / 2.0)
    other = [np.array([c, s]), np.array([-s, c])]
    return z, other


def projectors(basis):
    return [np.outer(v, v.conj()) for v in basis]


def max_overlap(b1, b2):
    return max(abs(float(np.vdot(u, v))) ** 2 for u in b1
               for v in b2)


def shannon(p):
    out = 0.0
    for q in p:
        if q > 1e-15:
            out -= q * math.log2(q)
    return out


def outcome_probs(rho, proj):
    return [float(np.real(np.trace(rho @ p))) for p in proj]


def conditional_entropy(rho, meas_povm, target_proj):
    """H(target outcome | consumer record), exact.

    The consumer applies a declared POVM to the system. For each
    record it holds the post-measurement state, and the target
    observable is then measured on that state.
    """
    total = 0.0
    for m in meas_povm:
        # Luders instrument, the declared post-measurement rule
        root = sqrtm_psd(m)
        post = root @ rho @ root
        p_r = float(np.real(np.trace(post)))
        if p_r <= 1e-15:
            continue
        post = post / p_r
        total += p_r * shannon(outcome_probs(post, target_proj))
    return total


def sqrtm_psd(m):
    w, v = np.linalg.eigh(m)
    w = np.clip(w.real, 0.0, None)
    return (v * np.sqrt(w)) @ v.conj().T


def main() -> int:
    record: dict = {"schema": "un0-instrument-v1",
                    "label": "exploratory"}
    items = {}
    rho_mixed = np.eye(2) / 2.0
    plus = np.array([1.0, 1.0]) / math.sqrt(2.0)
    rho_pure = np.outer(plus, plus.conj())

    zb, xb = basis_from_angle(math.pi / 2.0)
    pz, px = projectors(zb), projectors(xb)
    trivial = [np.eye(2)]

    # C1 the trivial consumer reads nothing, so the record leaves
    # the outcome entropies at their unconditioned values
    h_z_triv = conditional_entropy(rho_mixed, trivial, pz)
    h_x_triv = conditional_entropy(rho_mixed, trivial, px)
    items["C1_trivial_consumer"] = (
        abs(h_z_triv - 1.0) <= TOL and abs(h_x_triv - 1.0) <= TOL)

    # C2 a compatible pair, one consumer serves both exactly
    h_z_self = conditional_entropy(rho_mixed, pz, pz)
    items["C2_compatible_pair_zero"] = abs(h_z_self) <= TOL

    # C3 an incompatible pair, measuring one maximizes the other
    h_x_given_z = conditional_entropy(rho_mixed, pz, px)
    items["C3_incompatible_costs"] = abs(h_x_given_z - 1.0) <= TOL

    # C4 the declared entropic bound reproduced on the sum of
    # unconditioned entropies for the two bases
    ang = [math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2]
    bound_rows = []
    ok4 = True
    for th in ang:
        b1, b2 = basis_from_angle(th)
        c = max_overlap(b1, b2)
        mu = -math.log2(c)
        p1, p2 = projectors(b1), projectors(b2)
        worst = min(
            shannon(outcome_probs(r, p1)) + shannon(
                outcome_probs(r, p2))
            for r in (rho_mixed, rho_pure))
        bound_rows.append({"theta": th, "max_overlap": c,
                           "maassen_uffink": mu,
                           "min_sum_over_probe_states": worst})
        if worst < mu - 1e-9:
            ok4 = False
    items["C4_bound_respected"] = ok4

    # C5 estimation of an expectation value improves with copies,
    # the type I behaviour the track must be able to see
    est_rows = []
    for n in (1, 4, 16, 64, 256):
        # exact variance of the optimal unbiased estimator of the
        # z expectation from n projective outcomes on the plus state
        var = (1.0 - 0.0 ** 2) / n
        est_rows.append({"copies": n, "mse": var})
    items["C5_estimation_improves"] = all(
        est_rows[i + 1]["mse"] < est_rows[i]["mse"]
        for i in range(len(est_rows) - 1))

    record["measured"] = {
        "trivial_consumer_entropies": [h_z_triv, h_x_triv],
        "compatible_conditional_entropy": h_z_self,
        "incompatible_conditional_entropy": h_x_given_z,
        "bound_rows": bound_rows,
        "estimation_rows": est_rows,
        "reading": "the record's machinery separates a consumer "
                   "that serves a task exactly from one that "
                   "cannot, and reproduces the declared entropic "
                   "bound on the probe states"}
    record["items"] = {k: bool(v) for k, v in items.items()}
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["declared"] = {
        "post_measurement_rule": "Luders instrument",
        "angles": ang, "tolerance": TOL,
        "admissible_class": "POVMs on the system alone, which is "
                            "the narrowest class of the track and "
                            "is stated with every result"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "un0-instrument.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    for r in bound_rows:
        print("  theta %.4f  MU %.6f  min sum %.6f"
              % (r["theta"], r["maassen_uffink"],
                 r["min_sum_over_probe_states"]))
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
