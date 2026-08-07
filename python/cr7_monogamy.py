#!/usr/bin/env python3
"""CR-7 monogamy as consumer exclusion (exploratory).

Protocol declared in CRYPTO-TRACK.md before this run. The QD track
measured redundancy, many environment fragments carrying the same
record, and QD-3 measured two disjoint consumers agreeing at a rate
set by record strength. This run measures the boundary of that
plateau. Classical records are freely shareable, so a broadcast bit
gives every consumer the whole record at once. Quantum correlation
is not shareable, and for the declared family the tradeoff is an
exact identity rather than an inequality, so every unit one
consumer gains is a unit another loses.

Exploratory label. No real protocol, device, or implementation is
modeled or evaluated, and nothing here is a claim about the
security of anything.
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

PHI_GRID = [0.0, math.pi / 12, math.pi / 6, math.pi / 4,
            math.pi / 3, 5 * math.pi / 12, math.pi / 2]
TOL = 1e-12
SIGMA_Y = np.array([[0.0, -1j], [1j, 0.0]])


def w_class_state(phi, a2=0.5):
    """The declared W-class family, one excitation shared between
    the two consumers with the declared weight split."""
    a = math.sqrt(a2)
    rest = math.sqrt(1.0 - a2)
    b = rest * math.cos(phi)
    c = rest * math.sin(phi)
    psi = np.zeros(8, dtype=complex)
    psi[0b100] = a   # A excited
    psi[0b010] = b   # B excited
    psi[0b001] = c   # E excited
    return psi / np.linalg.norm(psi)


def reduced(psi, keep):
    t = psi.reshape(2, 2, 2)
    drop = [q for q in range(3) if q not in keep]
    t = np.transpose(t, list(keep) + drop)
    m = t.reshape(2 ** len(keep), 2 ** len(drop))
    return m @ m.conj().T


def concurrence(rho):
    """Wootters concurrence of a two-qubit state, exact."""
    yy = np.kron(SIGMA_Y, SIGMA_Y)
    rho_t = yy @ rho.conj() @ yy
    ev = np.linalg.eigvals(rho @ rho_t)
    ev = np.sqrt(np.clip(ev.real, 0.0, None))
    ev = np.sort(ev)[::-1]
    return float(max(0.0, ev[0] - ev[1] - ev[2] - ev[3]))


def tangle_one_vs_rest(psi, q):
    rho = reduced(psi, [q])
    return float(2.0 * (1.0 - np.trace(rho @ rho).real))


def entropy_bits(p):
    out = 0.0
    for v in p:
        if v > 0:
            out -= v * math.log2(v)
    return out


def classical_broadcast():
    """A declared classical record copied to both consumers. The
    mutual informations are computed from the exact joint."""
    joint = {(b, b, b): 0.5 for b in (0, 1)}
    pa = {0: 0.5, 1: 0.5}

    def mi(idx):
        out = 0.0
        for key, p in joint.items():
            pxy = p
            px = pa[key[0]]
            py = 0.5
            out += pxy * math.log2(pxy / (px * py))
        return out

    return mi(1), mi(2)


def main() -> int:
    record: dict = {"schema": "cr7-monogamy-v1",
                    "label": "exploratory"}
    items = {}

    # M1 classical polygamy, the QD plateau in its purest form
    i_ab, i_ae = classical_broadcast()
    items["M1_classical_record_is_shareable"] = (
        abs(i_ab - 1.0) <= TOL and abs(i_ae - 1.0) <= TOL)

    # M2 to M4, the quantum family
    rows = []
    worst_sum = 0.0
    worst_ckw = 0.0
    for phi in PHI_GRID:
        psi = w_class_state(phi)
        c_ab = concurrence(reduced(psi, [0, 1]))
        c_ae = concurrence(reduced(psi, [0, 2]))
        tau_a = tangle_one_vs_rest(psi, 0)
        s = c_ab ** 2 + c_ae ** 2
        worst_sum = max(worst_sum, abs(s - 1.0))
        worst_ckw = max(worst_ckw, abs(tau_a - s))
        rows.append({"phi": phi, "c_ab": c_ab, "c_ae": c_ae,
                     "sum_of_squares": s, "tangle_a_vs_rest":
                         tau_a})
        print(f"  phi={phi:.6f} C_AB={c_ab:.12f} "
              f"C_AE={c_ae:.12f} sum={s:.12f}", flush=True)
    items["M2_exact_tradeoff_identity"] = worst_sum <= 1e-9
    items["M4_ckw_saturated_on_this_class"] = worst_ckw <= 1e-9

    first, last = rows[0], rows[-1]
    items["M3_exclusion_at_the_extreme"] = (
        abs(first["c_ab"] - 1.0) <= 1e-9
        and abs(first["c_ae"]) <= 1e-9
        and abs(last["c_ae"] - 1.0) <= 1e-9
        and abs(last["c_ab"]) <= 1e-9)

    findings = {
        "M5_classical_sum_exceeds_the_quantum_identity": bool(
            (i_ab + i_ae) > 1.0 + 1e-9
            and abs(rows[0]["sum_of_squares"] - 1.0) <= 1e-9)}

    record["measured"] = {
        "classical_broadcast": {"i_ab_bits": i_ab,
                                "i_ae_bits": i_ae,
                                "sum_bits": i_ab + i_ae},
        "quantum_family": rows,
        "worst_identity_deviation": float(worst_sum),
        "worst_ckw_deviation": float(worst_ckw),
        "reading": "a classical record is held in full by every "
                   "consumer at once, which is the redundancy the "
                   "QD track measured, while quantum correlation "
                   "obeys an exact tradeoff on this family so a "
                   "consumer that holds all of it excludes every "
                   "other consumer entirely"}
    record["items"] = {k: bool(v) for k, v in items.items()}
    record["findings"] = findings
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["declared"] = {
        "phi_grid": PHI_GRID, "weight_a_squared": 0.5,
        "family": "one excitation shared between the two "
                  "consumers at the declared weight split",
        "tolerance": TOL,
        "scope": "toy three-qubit family, methodology only, no "
                 "real protocol or device, no claim about any "
                 "system"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "cr7-monogamy.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("classical", i_ab, i_ae)
    print("worst identity dev", worst_sum, "ckw dev", worst_ckw)
    print("items", items, "findings", findings)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
