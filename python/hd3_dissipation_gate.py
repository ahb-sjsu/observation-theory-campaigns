#!/usr/bin/env python3
"""HD-3 dissipation declared-or-absent, the reversal gate
(exploratory).

Protocol declared in HYDRODYNAMICS-TRACK.md before this run. The
substrate is HD-2's FHP-I gas unchanged, imported from the HD-2
runner rather than reimplemented. An FHP-I update is a bijection,
so the exact inverse step exists, un-stream every channel along its
own direction, then invert the collision at the recorded parity,
head-on pairs rotate the opposite chirality and the three-body
flip is its own inverse, realized here as the HD-2 collision with
flipped time parity. D1, the forward run of T steps is inverted in
reverse parity order and must recover the initial state bit for
bit in every realization. D2, the inverse-run shear amplitude
sequence must equal the forward sequence reversed exactly, the
"dissipated" mode is exactly recoverable, no strict dissipative
law governs the coarse observable. D3, one declared bit flipped at
time T destroys the recovery for its realization alone, the
returned amplitude is at most half the true initial amplitude
while the 49 untouched realizations return exactly, and the
Hamming lightcone flood is sampled every 30 inverse steps. PE-4 at
the level of transport.

Exploratory label. No claim about physical fluids.
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

from hd2_fhp_viscosity import (  # noqa: E402
    AMP, CYU, F0, L, M, T, TABLE, collide, step, x_phys)
from projection_fold import canonical_sha256  # noqa: E402

SEED = 20260825
K = 1
FLIP = (0, 0, 32, 32)  # channel, realization, row, col at time T
HAMMING_EVERY = 30
PROJ = np.sin(2 * np.pi * K * np.arange(L) / L)


def unstream(m):
    """Exact inverse of hd2 stream: pull each channel back."""
    out = np.zeros_like(m)
    rows = np.arange(L)
    for i in range(6):
        for p in (0, 1):
            dr, dc = TABLE[p][i]
            src = rows[rows % 2 == p]
            dst = (src + dr) % L
            out[i][..., src, :] = np.roll(m[i][..., dst, :], -dc,
                                          axis=-1)
    return out


def unstep(m, t):
    """Exact inverse of step(n, t) = stream(collide(n, t)).

    Un-stream, then invert the parity-t collision. The forward
    even-parity collision rotates head-on pairs by +60 degrees and
    the odd-parity by -60, so the inverse rotation is the opposite
    chirality, which is exactly the hd2 collision at parity t+1;
    the three-body flip is its own inverse and is applied by any
    parity.
    """
    return collide(unstream(m), t + 1)


def col_momenta(n):
    """Per-realization per-column integer y momentum in s3 units."""
    f = sum(CYU[i] * n[i].astype(np.int64) for i in range(6)
            if CYU[i] != 0)
    return f.sum(axis=1)  # [M, L(c)]


def amp_ens(n):
    return float(col_momenta(n).mean(axis=0) @ PROJ * 2.0 / L)


def amp_r0(n):
    return float(col_momenta(n)[0] @ PROJ * 2.0 / L)


def main() -> int:
    record: dict = {"schema": "hd3-dissipation-gate-v1",
                    "label": "exploratory"}
    record["declared"] = {
        "model": "FHP-I of HD-2 unchanged, 64x64 even-r offset "
                 "triangular torus, 6 channels, imported from "
                 "hd2_fhp_viscosity (collide, step, geometry)",
        "L": L, "M": M, "T": T, "f0": F0, "amp": AMP, "k": K,
        "seed": SEED,
        "inverse": "unstep(m, t) = collide(unstream(m), t+1); "
                   "un-stream pulls each channel back along its "
                   "own direction, collide at flipped parity "
                   "rotates head-on pairs the opposite chirality, "
                   "three-body flip is its own inverse",
        "flip": {"channel": 0, "realization": 0, "row": 32,
                 "col": 32, "at_time": T},
        "hamming_cadence": HAMMING_EVERY,
        "bars": {
            "D1": "initial state recovered bit for bit in every "
                  "realization",
            "D2": "inverse-run amplitude sequence equals the "
                  "forward sequence reversed exactly, float for "
                  "float",
            "D3": "perturbed return amplitude of realization 0 at "
                  "most half its true initial amplitude, the "
                  "other 49 realizations return bit for bit"}}
    items = {}

    # declared initial ensemble, HD-2 shear prescription, new seed
    rng = np.random.RandomState(SEED)
    s = np.sin(2 * np.pi * K * x_phys() / L)[None, :, :]
    p = np.empty((6, M, L, L))
    for i in range(6):
        p[i] = np.clip(F0 + AMP * CYU[i] * s, 0.0, 1.0)
    n0 = rng.random((6, M, L, L)) < p

    # forward run, parity sequence is t = 0..T-1
    n = n0.copy()
    a_fwd = [amp_ens(n)]
    for t in range(T):
        n = step(n, t)
        a_fwd.append(amp_ens(n))
    n_final = n.copy()

    # D1 + D2, the exact inverse run
    n = n_final.copy()
    a_inv = [amp_ens(n)]
    ckpt = {0: n[:, 0].copy()}
    for sidx, t in enumerate(range(T - 1, -1, -1), start=1):
        n = unstep(n, t)
        a_inv.append(amp_ens(n))
        if sidx % HAMMING_EVERY == 0:
            ckpt[sidx] = n[:, 0].copy()
    items["D1_exact_invertibility"] = bool(np.array_equal(n, n0))
    rev_dev = max(abs(a_inv[si] - a_fwd[T - si])
                  for si in range(T + 1))
    items["D2_loschmidt_account"] = bool(
        all(a_inv[si] == a_fwd[T - si] for si in range(T + 1)))

    # D3, one bit of lost reversal reach
    n = n_final.copy()
    n[FLIP] ^= True
    hamming = [[0, int(np.count_nonzero(n[:, 0] != ckpt[0]))]]
    for sidx, t in enumerate(range(T - 1, -1, -1), start=1):
        n = unstep(n, t)
        if sidx % HAMMING_EVERY == 0:
            hamming.append(
                [sidx,
                 int(np.count_nonzero(n[:, 0] != ckpt[sidx]))])
    a0_r0 = amp_r0(n0)
    a_pert_r0 = amp_r0(n)
    return_ratio = abs(a_pert_r0) / abs(a0_r0)
    others_exact = bool(np.array_equal(n[:, 1:], n0[:, 1:]))
    items["D3_reversal_reach"] = bool(return_ratio <= 0.5
                                      and others_exact)

    record["measured"] = {
        "amp_forward_t0": a_fwd[0],
        "amp_forward_T": a_fwd[T],
        "forward_decay_ratio": float(abs(a_fwd[T]) / abs(a_fwd[0])),
        "amp_forward_every10": [a_fwd[t]
                                for t in range(0, T + 1, 10)],
        "inverse_reversed_max_dev": float(rev_dev),
        "inverse_matches_forward_reversed_exactly":
            bool(items["D2_loschmidt_account"]),
        "hamming_divergence_r0": hamming,
        "amp_r0_true_initial": a0_r0,
        "amp_r0_perturbed_return": a_pert_r0,
        "perturbed_return_ratio": float(return_ratio),
        "untouched_49_return_bit_exact": others_exact,
        "reading": "dissipation on this substrate is "
                   "declared-or-absent in the consumer, exactly "
                   "PE-4's lesson at the level of transport, the "
                   "coarse mode's decay is recoverable by any "
                   "observer with exact reversal reach and "
                   "irrecoverable after the loss of one bit"}
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
        / "hd3-dissipation-gate.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("forward decay",
          record["measured"]["forward_decay_ratio"])
    print("rev_dev", rev_dev)
    print("hamming", hamming)
    print("return_ratio", return_ratio, "others", others_exact)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
