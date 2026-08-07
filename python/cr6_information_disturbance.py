#!/usr/bin/env python3
"""CR-6 information against disturbance (exploratory).

Protocol declared in CRYPTO-TRACK.md before this run. Every
classical track in this program found that a restricted consumer's
blindness costs the consumer and leaves the substrate untouched,
most sharply in HD-3 where the decayed mode was recovered bit for
bit. A consumer reading a non-orthogonal ensemble cannot do that.
This run measures the exact price, an eavesdropping consumer's
information against the disturbance it causes, beside a classical
control on an orthogonal ensemble where the same structure reads
perfectly and leaves no trace at all.

Everything is computed by exact enumeration of a finite probability
space, and every measured quantity is checked against a declared
closed form.

Exploratory label. No real protocol, device, or implementation is
modeled or evaluated, no attack on any system is developed, and
nothing here is a claim about the security of anything.
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

LAMBDAS = [0.0, 0.1, 0.25, 0.5, 0.75, 1.0]
TOL = 1e-12

KET = {
    ("Z", 0): np.array([1.0, 0.0]),
    ("Z", 1): np.array([0.0, 1.0]),
    ("X", 0): np.array([1.0, 1.0]) / math.sqrt(2.0),
    ("X", 1): np.array([1.0, -1.0]) / math.sqrt(2.0),
}


def measure_probs(state, basis):
    """Born probabilities of the two outcomes in a declared basis."""
    return [abs(float(np.dot(KET[(basis, k)], state))) ** 2
            for k in (0, 1)]


def mutual_information(joint):
    """Exact mutual information in bits from a joint distribution
    over pairs, given as a mapping to probabilities."""
    px = defaultdict(float)
    py = defaultdict(float)
    for (x, y), p in joint.items():
        px[x] += p
        py[y] += p
    out = 0.0
    for (x, y), p in joint.items():
        if p > 0:
            out += p * math.log2(p / (px[x] * py[y]))
    return out


def run_family(bases, lam):
    """Exact enumeration. Alice picks a declared basis and bit
    uniformly, Eve intercepts with probability lam and measures in
    the computational basis and resends her outcome, Bob measures
    in Alice's basis. Returns Eve's information and the error rate
    on the sifted key."""
    joint_ae = defaultdict(float)
    err = 0.0
    for basis in bases:
        for bit in (0, 1):
            p_prep = 1.0 / (len(bases) * 2)
            state = KET[(basis, bit)]
            # Eve passes
            joint_ae[(bit, ("pass", basis))] += p_prep * (1 - lam)
            pb = measure_probs(state, basis)
            err += p_prep * (1 - lam) * pb[1 - bit]
            # Eve intercepts, measures Z, resends her outcome
            pe = measure_probs(state, "Z")
            for e_out in (0, 1):
                w = p_prep * lam * pe[e_out]
                if w <= 0:
                    continue
                joint_ae[(bit, ("meas", basis, e_out))] += w
                resent = KET[("Z", e_out)]
                pb2 = measure_probs(resent, basis)
                err += w * pb2[1 - bit]
    return mutual_information(joint_ae), err


def holevo_bound(bases):
    """Holevo quantity of the declared preparation ensemble."""
    rho = np.zeros((2, 2), dtype=complex)
    n = len(bases) * 2
    for basis in bases:
        for bit in (0, 1):
            v = KET[(basis, bit)].astype(complex)
            rho += np.outer(v, v.conj()) / n
    ev = np.linalg.eigvalsh(rho)
    ev = ev[ev > 1e-15]
    return float(-np.sum(ev * np.log2(ev)))


def main() -> int:
    record: dict = {"schema": "cr6-information-disturbance-v1",
                    "label": "exploratory"}
    items = {}

    # C1 the classical control, an orthogonal ensemble
    info_c, err_c = run_family(["Z"], 1.0)
    items["C1_orthogonal_reads_without_trace"] = (
        abs(info_c - 1.0) <= TOL and abs(err_c) <= TOL)

    # C2 to C5, the non-orthogonal ensemble
    rows = []
    worst_form = 0.0
    strict_ok = True
    zero_ok = True
    for lam in LAMBDAS:
        info, err = run_family(["Z", "X"], lam)
        pred_info = lam / 2.0
        pred_err = lam / 4.0
        worst_form = max(worst_form, abs(info - pred_info),
                         abs(err - pred_err))
        if lam > 0 and not (info > 0 and err > 0):
            strict_ok = False
        if lam == 0 and not (abs(info) <= TOL
                             and abs(err) <= TOL):
            zero_ok = False
        rows.append({"lambda": lam, "eve_information_bits": info,
                     "qber": err,
                     "closed_form_information": pred_info,
                     "closed_form_qber": pred_err,
                     "information_over_qber":
                         (info / err if err > 0 else None)})
        print(f"  lam={lam} I={info:.12f} QBER={err:.12f}",
              flush=True)
    items["C2_no_information_without_disturbance"] = strict_ok
    items["C3_closed_form_tradeoff"] = worst_form <= TOL
    items["C4_zero_disturbance_zero_information"] = zero_ok

    chi = holevo_bound(["Z", "X"])
    max_info = max(r["eve_information_bits"] for r in rows)
    items["C5_holevo_bound_respected"] = max_info <= chi + TOL

    ratios = [r["information_over_qber"] for r in rows
              if r["information_over_qber"] is not None]
    findings = {
        "C6_tradeoff_is_exactly_two_bits_per_unit_error": bool(
            all(abs(r - 2.0) <= 1e-9 for r in ratios))}

    record["measured"] = {
        "classical_control": {"eve_information_bits": info_c,
                              "qber": err_c},
        "ladder": rows,
        "worst_closed_form_deviation": float(worst_form),
        "holevo_bound_bits": chi,
        "max_eve_information_bits": float(max_info),
        "information_per_unit_qber": ratios,
        "reading": "an orthogonal ensemble is read perfectly and "
                   "leaves no trace, while every consumer that "
                   "learns anything about a non-orthogonal "
                   "ensemble disturbs it, at a rate this family "
                   "fixes exactly at two bits of information per "
                   "unit of induced error"}
    record["items"] = {k: bool(v) for k, v in items.items()}
    record["findings"] = findings
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["declared"] = {
        "lambdas": LAMBDAS, "tolerance": TOL,
        "eavesdropper": "intercept with probability lambda, "
                        "measure in the computational basis, "
                        "resend the collapsed state",
        "closed_forms": "information equals lambda over two, "
                        "error equals lambda over four",
        "scope": "toy ensemble, methodology only, no real "
                 "protocol or device, no claim about any system"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "cr6-information-disturbance.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("classical control", info_c, err_c)
    print("worst closed-form deviation", worst_form,
          "holevo", chi)
    print("items", items, "findings", findings)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
