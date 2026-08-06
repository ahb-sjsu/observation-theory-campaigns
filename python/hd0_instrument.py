#!/usr/bin/env python3
"""HD-0 exact lattice-gas instrument layer (exploratory).

Protocol declared in HYDRODYNAMICS-TRACK.md before this run. HPP on
a 16 by 16 torus, four boolean velocity channels, streaming plus
head-on collisions. Integer-exact conservation, bit-exact
reversibility, the observational-entropy Loschmidt control, and
rotation equivariance. Verdict computed from the measured items.

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

from projection_fold import canonical_sha256  # noqa: E402

L = 16
T = 200
# channels 0:E, 1:N, 2:W, 3:S


def collide(n):
    ew = n[0] & n[2] & ~n[1] & ~n[3]
    ns = n[1] & n[3] & ~n[0] & ~n[2]
    out = n.copy()
    out[0] = (n[0] & ~ew) | ns
    out[2] = (n[2] & ~ew) | ns
    out[1] = (n[1] & ~ns) | ew
    out[3] = (n[3] & ~ns) | ew
    return out


def stream(n):
    out = np.empty_like(n)
    out[0] = np.roll(n[0], 1, axis=1)   # E moves +x
    out[2] = np.roll(n[2], -1, axis=1)  # W moves -x
    out[1] = np.roll(n[1], -1, axis=0)  # N moves -row (up)
    out[3] = np.roll(n[3], 1, axis=0)   # S moves +row
    return out


def step(n):
    return stream(collide(n))


def revstep(n):
    """Inverse-order automaton. With velocities reversed, running
    collide-after-stream exactly inverts the collide-then-stream
    forward step, R revstep R = step inverse."""
    return collide(stream(n))


def reverse_velocities(n):
    return n[[2, 3, 0, 1]]


def rotate90(n):
    """Rotate lattice and relabel channels E->N->W->S->E."""
    r = np.stack([np.rot90(ch) for ch in n])
    return r[[3, 0, 1, 2]]


def invariants(n):
    mass = int(n.sum())
    px = int(n[0].sum()) - int(n[2].sum())
    py = int(n[1].sum()) - int(n[3].sum())
    return mass, px, py


def coarse_entropy_bits(n):
    counts = n.sum(axis=0).reshape(4, 4, 4, 4).sum(axis=(1, 3))
    tot = counts.sum()
    p = counts.flatten() / tot
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))


def initial_state():
    rng = np.random.RandomState(20260811)
    n = np.zeros((4, L, L), dtype=bool)
    n[:, 5:11, 5:11] = True                       # the blob
    sprinkle = rng.random((4, L, L)) < 0.05
    n |= sprinkle
    return n


def main() -> int:
    record: dict = {"schema": "hd0-instrument-v1",
                    "label": "exploratory"}
    items = {}
    n0 = initial_state()

    # C1 conservation, forward run with entropy curve
    n = n0.copy()
    inv0 = invariants(n)
    h_fwd = [coarse_entropy_bits(n)]
    cons_ok = True
    states = [n.copy()]
    for _ in range(T):
        n = step(n)
        cons_ok = cons_ok and invariants(n) == inv0
        h_fwd.append(coarse_entropy_bits(n))
        states.append(n.copy())
    items["C1_conservation"] = bool(cons_ok)

    # C2 bit-exact reversibility
    m = reverse_velocities(n)
    h_rev = [coarse_entropy_bits(m)]
    rev_states = [m.copy()]
    for _ in range(T):
        m = revstep(m)
        h_rev.append(coarse_entropy_bits(m))
        rev_states.append(m.copy())
    back = reverse_velocities(m)
    items["C2_reversibility"] = bool(np.array_equal(back, n0))

    # C3 observational entropy and the Loschmidt retrace
    rise = h_fwd[-1] - h_fwd[0]
    retrace = max(abs(h_rev[k] - h_fwd[T - k]) for k in range(T + 1))
    # the reversed trajectory must visit the forward states in
    # reverse order, velocity-reversed, bit for bit
    exact_retrace = all(
        np.array_equal(rev_states[k],
                       reverse_velocities(states[T - k]))
        for k in range(T + 1))
    items["C3_entropy_rise_and_retrace"] = bool(
        rise >= 0.3 and retrace == 0.0 and exact_retrace)

    # C4 rotation equivariance
    a = rotate90(n0)
    for _ in range(50):
        a = step(a)
    b = n0.copy()
    for _ in range(50):
        b = step(b)
    items["C4_rotation_equivariance"] = bool(
        np.array_equal(a, rotate90(b)))

    record["measured"] = {
        "invariants": list(inv0),
        "entropy_initial_bits": h_fwd[0],
        "entropy_final_bits": h_fwd[-1],
        "entropy_rise_bits": float(rise),
        "retrace_max_dev": float(retrace),
        "entropy_curve_every_20":
            [float(h_fwd[k]) for k in range(0, T + 1, 20)]}
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
        / "hd0-instrument.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("rise", rise, "retrace", retrace)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
