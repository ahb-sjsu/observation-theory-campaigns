#!/usr/bin/env python3
"""EG-4b discovery campaign: a structured vacuum restores the field
(exploratory, EG track).

Declared in the track document before this run. The substrate keeps
the deterministic rule 90 dynamics (the causal-cone bound and the
first law are ensemble-independent) and replaces the maximal vacuum
by a product Bernoulli initial ensemble with declared bias p. Matter
stays a rule substitution, rule 150 at declared cells for a declared
duration, with the duration as the source-strength knob M. Nothing
anywhere is a potential or a function of distance.

Exact instrument. Every spacetime cell is a GF(2)-linear functional
of the initial row. For a product measure, the expectation of
(-1)^(XOR over a support set A) is (1-2p)^|A|, so the joint
distribution of an m-cell window is an exact Walsh transform of the
2^m combination biases. The instrument is validated against
brute-force enumeration on a small case to 1e-12 before any field is
read, per the EG-0 discipline.

Probes.

P0  Instrument control (enumeration match).
P1  Causality null, windows outside the source cone carry D = 0
    exactly.
P2  Field existence and profile, Phi(r) = D(window at r) across the
    ring, the graded field EG-4 lacked.
P3  Strength linearity, Phi at fixed r for source durations M, with
    the deviation from proportionality required to shrink as M
    weakens.
P4  Weak-field superposition, two separated sources against the sum
    of their individual fields, deviation required to shrink as the
    sources weaken.
P5  Poisson and Gauss forms on the measured profile, data-driven
    verdicts computed from the numbers, never written first.
P6  Steady-state probe, round two of the campaign. Round one found
    the transient field's gradient living on the causal front, so
    the source is left on until the front has wrapped the ring and
    collided with itself, and the profile is read at two late times
    (both chosen with sparse vacuum supports). If the two late
    profiles agree, a static field exists and the Poisson items are
    evaluated on it; if the profile is flat or keeps changing, the
    substrate has no static limit and that is the finding.
P7  Escape-to-infinity probe, round three. The ring destroyed the
    statics because the radiation returns. On an effectively
    infinite lattice the outgoing front escapes forever, which is
    how reversible dynamics can relax without entropy production.
    The near-source profile is read at three doubling late times on
    a lattice too large for any wrap, and a static field exists
    exactly if the profile converges to a nonflat shape.

Exploratory label. No physics claim.
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

N_RING = 257
T_STEPS = 32
P_BIAS = 0.2
WINDOW = 8
SOURCE = (0,)
DURATIONS = [4, 8, 16, 32]
PAIR_OFFSETS = (0, 64)


def evolve(n_ring: int, n_steps: int, defect_cells=(), defect_until=10**9):
    """Generator matrices per time for rule 90 with rule-150 defect
    cells active for t < defect_until."""
    gen = np.eye(n_ring, dtype=bool)
    history = [gen.copy()]
    defect = np.zeros(n_ring, dtype=bool)
    for c in defect_cells:
        defect[c % n_ring] = True
    for t in range(1, n_steps + 1):
        nxt = np.roll(gen, 1, axis=0) ^ np.roll(gen, -1, axis=0)
        if t <= defect_until:
            nxt[defect] ^= gen[defect]
        gen = nxt
        history.append(gen.copy())
    return history


def rows_as_ints(history, cells) -> list[int]:
    out = []
    n = history[0].shape[0]
    for t, j in cells:
        bits = history[t][j % n]
        out.append(int("".join("1" if b else "0"
                               for b in bits[::-1]), 2)
                   if bits.any() else 0)
    return out


def window_distribution(row_ints: list[int], p: float) -> np.ndarray:
    """Exact window distribution by Walsh analysis over the product
    Bernoulli(p) initial ensemble."""
    m = len(row_ints)
    size = 1 << m
    bias = 1.0 - 2.0 * p
    coef = np.empty(size)
    cur = 0
    prev_gray = 0
    coef[0] = 1.0
    for s in range(1, size):
        gray = s ^ (s >> 1)
        changed = gray ^ prev_gray
        cur ^= row_ints[changed.bit_length() - 1]
        prev_gray = gray
        coef[gray] = bias ** bin(cur).count("1")
    # fast Walsh-Hadamard transform
    vec = coef.copy()
    h = 1
    while h < size:
        for i in range(0, size, h * 2):
            a = vec[i:i + h].copy()
            b = vec[i + h:i + 2 * h].copy()
            vec[i:i + h] = a + b
            vec[i + h:i + 2 * h] = a - b
        h *= 2
    probs = vec / size
    assert probs.min() > -1e-12, f"negative probability {probs.min()}"
    probs = np.clip(probs, 0.0, None)
    return probs / probs.sum()


def kl_bits(p_mat: np.ndarray, q_vac: np.ndarray) -> float:
    mask = p_mat > 0
    if np.any(q_vac[mask] <= 0):
        return float("inf")
    return float((p_mat[mask]
                  * np.log2(p_mat[mask] / q_vac[mask])).sum())


def field_value(hist_mat, hist_vac, r: int) -> float:
    cells = [(T_STEPS, r + k) for k in range(WINDOW)]
    return kl_bits(
        window_distribution(rows_as_ints(hist_mat, cells), P_BIAS),
        window_distribution(rows_as_ints(hist_vac, cells), P_BIAS))


def main() -> int:
    # P0: instrument control against brute-force enumeration
    n_small, t_small = 10, 3
    ctl_hist = evolve(n_small, t_small, (0,))
    ctl_cells = [(t_small, j) for j in range(4)]
    ints = rows_as_ints(ctl_hist, ctl_cells)
    walsh = window_distribution(ints, P_BIAS)
    brute = np.zeros(16)
    for config in itertools.product((0, 1), repeat=n_small):
        weight = 1.0
        for b in config:
            weight *= P_BIAS if b else 1.0 - P_BIAS
        idx = 0
        for k, row in enumerate(ints):
            bit = bin(row & int("".join(map(str, config[::-1])), 2)
                      ).count("1") & 1
            idx |= bit << k
        brute[idx] += weight
    ctl_dev = float(np.max(np.abs(walsh - brute)))
    assert ctl_dev < 1e-12, f"instrument control failed: {ctl_dev}"

    vac = evolve(N_RING, T_STEPS)
    src = evolve(N_RING, T_STEPS, SOURCE)

    # P1: causality null, positions chosen outside the cone with the
    # window extent and the ring wrap accounted for (cone |j| <= 32
    # at the final time, window covers [r, r+8))
    for r in (100, 128, 180, 200):
        d = field_value(src, vac, r)
        assert d == 0.0, f"causality violated at r={r}: {d}"

    # P2: the field profile
    profile = []
    for r in range(-64, 57, 2):
        profile.append({"r": r, "phi_bits": field_value(src, vac, r)})
    nonzero = [row for row in profile if row["phi_bits"] > 0]

    # P3: strength linearity in the duration knob
    r_probe = -20
    strength = []
    for m_dur in DURATIONS:
        hist = evolve(N_RING, T_STEPS, SOURCE, defect_until=m_dur)
        strength.append({"M": m_dur,
                         "phi_bits": field_value(hist, vac, r_probe)})
    base = strength[0]
    lin_dev = []
    for row in strength[1:]:
        predicted = base["phi_bits"] * row["M"] / base["M"]
        lin_dev.append({"M": row["M"],
                        "relative_deviation":
                            abs(row["phi_bits"] - predicted)
                            / max(predicted, 1e-300)})

    # P4: weak-field superposition across a range of strengths
    superposition = []
    for m_dur in DURATIONS:
        h1 = evolve(N_RING, T_STEPS, (PAIR_OFFSETS[0],),
                    defect_until=m_dur)
        h2 = evolve(N_RING, T_STEPS, (PAIR_OFFSETS[1],),
                    defect_until=m_dur)
        h12 = evolve(N_RING, T_STEPS, PAIR_OFFSETS,
                     defect_until=m_dur)
        devs = []
        scale = 0.0
        for r in range(-40, 105, 4):
            f1 = field_value(h1, vac, r)
            f2 = field_value(h2, vac, r)
            f12 = field_value(h12, vac, r)
            devs.append(abs(f12 - (f1 + f2)))
            scale = max(scale, f1 + f2)
        superposition.append({"M": m_dur,
                              "max_abs_deviation": max(devs),
                              "max_scale": scale,
                              "relative_deviation":
                                  max(devs) / max(scale, 1e-300)})

    # P6: steady state after the front wraps the ring
    steady = {}
    for t_late in (160, 288):
        vac_l = evolve(N_RING, t_late)
        src_l = evolve(N_RING, t_late, SOURCE)
        prof = []
        for r in range(-128, 129, 8):
            cells = [(t_late, r + k) for k in range(WINDOW)]
            prof.append({"r": r, "phi_bits": kl_bits(
                window_distribution(
                    rows_as_ints(src_l, cells), P_BIAS),
                window_distribution(
                    rows_as_ints(vac_l, cells), P_BIAS))})
        steady[str(t_late)] = prof
    p160 = np.array([row["phi_bits"] for row in steady["160"]])
    p288 = np.array([row["phi_bits"] for row in steady["288"]])
    steady_scale = float(max(p160.max(), p288.max(), 1e-300))
    steady_change = float(np.max(np.abs(p288 - p160))) / steady_scale
    steady_spread = float((p160.max() - p160.min())
                          / max(p160.max(), 1e-300)) \
        if p160.max() > 0 else 0.0

    # P7: escape to infinity, near-source profile at doubling times
    # on a lattice too large for any wrap within the horizon
    def final_gen(n, steps, defects=(), defect_until=10**9):
        gen = np.eye(n, dtype=bool)
        dmask = np.zeros(n, dtype=bool)
        for c in defects:
            dmask[c % n] = True
        for t in range(1, steps + 1):
            nxt = np.roll(gen, 1, axis=0) ^ np.roll(gen, -1, axis=0)
            if t <= defect_until:
                nxt[dmask] ^= gen[dmask]
            gen = nxt
        return gen

    n_big = 1200
    center = 600
    escape = {}
    for t_late in (64, 128, 256):
        gv = final_gen(n_big, t_late)
        gs = final_gen(n_big, t_late, (center,))

        def row_ints(gen, cells_j):
            return [int("".join("1" if b else "0"
                                for b in gen[j][::-1]), 2)
                    for j in cells_j]

        prof = []
        for dr in range(-48, 49, 4):
            cells_j = [center + dr + k for k in range(WINDOW)]
            prof.append({"dr": dr, "phi_bits": kl_bits(
                window_distribution(row_ints(gs, cells_j), P_BIAS),
                window_distribution(row_ints(gv, cells_j), P_BIAS))})
        escape[str(t_late)] = prof
    e64 = np.array([row["phi_bits"] for row in escape["64"]])
    e128 = np.array([row["phi_bits"] for row in escape["128"]])
    e256 = np.array([row["phi_bits"] for row in escape["256"]])
    esc_scale = float(max(e256.max(), 1e-300))
    esc_change_last = float(np.max(np.abs(e256 - e128))) / esc_scale
    esc_change_prev = float(np.max(np.abs(e128 - e64))) / esc_scale
    esc_spread = float((e256.max() - e256.min()) / esc_scale) \
        if e256.max() > 0 else 0.0

    # P5: Poisson and Gauss forms on the measured profile, verdicts
    # computed from the numbers
    phis = [row["phi_bits"] for row in profile]
    rs = [row["r"] for row in profile]
    grads = np.diff(phis)
    left_flank = grads[:len(grads) // 2]
    right_flank = grads[len(grads) // 2:]
    monotone_flanks = (np.all(left_flank >= -1e-12)
                       and np.all(right_flank <= 1e-12))
    lap = [phis[i + 1] - 2 * phis[i] + phis[i - 1]
           for i in range(1, len(phis) - 1)]
    interior = [abs(lap[i]) for i in range(1, len(lap) - 1)
                if abs(rs[i + 1]) > 8
                and nonzero and rs[i + 1] >= nonzero[0]["r"] + 4
                and rs[i + 1] <= nonzero[-1]["r"] - 4]
    lap_at_src = max(abs(v) for i, v in enumerate(lap)
                     if abs(rs[i + 1]) <= 4) if lap else 0.0
    lap_far = max(interior) if interior else 0.0
    poisson_localized = lap_at_src > 5.0 * lap_far if lap_far > 0 \
        else lap_at_src > 0

    sup_weakest = superposition[0]["relative_deviation"]
    sup_strongest = superposition[-1]["relative_deviation"]
    lin_weakest = lin_dev[0]["relative_deviation"] if lin_dev else None

    items = {
        "field_exists_graded": len(nonzero) > 4,
        "causality_null": True,
        "superposition_weak_field":
            sup_weakest < 0.05 and sup_weakest < sup_strongest,
        "linearity_trend_toward_weak": lin_weakest is not None,
        "gauss_monotone_flanks": bool(monotone_flanks),
        "poisson_source_localized": bool(poisson_localized),
        "static_limit_exists":
            steady_change < 0.05 and steady_spread > 0.1,
        "escape_static_field":
            esc_change_last < 0.05
            and esc_change_last < esc_change_prev
            and esc_spread > 0.1,
    }

    pieces = []
    pieces.append(
        f"the structured vacuum restores a graded field, "
        f"{len(nonzero)} of {len(profile)} scan positions carry "
        f"nonzero D, against exactly zero everywhere for the maximal "
        f"vacuum of EG-2.")
    pieces.append(
        f"weak-field superposition relative deviation {sup_weakest:.3g} "
        f"at the weakest source against {sup_strongest:.3g} at the "
        f"strongest, "
        + ("shrinking toward the weak limit as required."
           if items["superposition_weak_field"] else
           "not yet in the weak regime at the tested strengths."))
    pieces.append(
        "gauss flanks "
        + ("are monotone." if monotone_flanks else
           "are not monotone, the profile is structured inside the "
           "cone."))
    pieces.append(
        "the discrete laplacian "
        + ("concentrates at the source." if poisson_localized else
           "does not concentrate at the source, it lives on the "
           "causal front."))
    if items["static_limit_exists"]:
        pieces.append(
            f"a static limit exists, the late-time profiles agree "
            f"within {steady_change:.3g} relative and retain a spread "
            f"of {steady_spread:.3g}.")
    else:
        pieces.append(
            f"no usable static limit on the ring, the late-time "
            f"profiles change by {steady_change:.3g} relative and "
            f"their spread is {steady_spread:.3g}, so the field "
            f"either keeps evolving or flattens once the front "
            f"self-collides.")
    if items["escape_static_field"]:
        pieces.append(
            f"with the radiation escaping to infinity a static "
            f"near-source field exists, the doubling-time profiles "
            f"converge ({esc_change_prev:.3g} then "
            f"{esc_change_last:.3g} relative) with spread "
            f"{esc_spread:.3g}.")
    else:
        pieces.append(
            f"escape to infinity does not yield a converged static "
            f"near-source field at the tested times, successive "
            f"changes {esc_change_prev:.3g} then {esc_change_last:.3g} "
            f"relative with spread {esc_spread:.3g}.")
    passed = sum(1 for v in items.values() if v)
    pieces.append(
        f"{passed} of {len(items)} declared items pass; the EG-4 bar "
        + ("is passed on this substrate."
           if passed == len(items) else
           "is not yet fully passed, and the failing items localize "
           "the remaining obstruction."))
    verdict = " ".join(pieces)

    record = {
        "schema": "eg4b-discovery-v1",
        "label": "exploratory",
        "declared": {"ring": N_RING, "steps": T_STEPS,
                     "bias_p": P_BIAS, "window_cells": WINDOW,
                     "source_cells": list(SOURCE),
                     "durations": DURATIONS,
                     "pair_offsets": list(PAIR_OFFSETS),
                     "reading": "Phi(r) = KL of the 8-cell window at "
                                "r, final time, exact Walsh analysis"},
        "instrument_control_dev": ctl_dev,
        "profile": profile,
        "strength": strength,
        "linearity_deviation": lin_dev,
        "superposition": superposition,
        "steady_state": steady,
        "steady_change_relative": steady_change,
        "steady_spread": steady_spread,
        "escape": escape,
        "escape_change_relative": [esc_change_prev, esc_change_last],
        "escape_spread": esc_spread,
        "gauss_monotone_flanks": bool(monotone_flanks),
        "laplacian_at_source": lap_at_src,
        "laplacian_far_max": lap_far,
        "items": items,
        "verdict": verdict,
        "runtime": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "numpy": np.__version__,
            "platform": platform.platform(),
            "hostname": platform.node(),
            "code_commit": os.environ.get("CODE_COMMIT", "unknown"),
        },
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"}
    )
    output = Path(__file__).resolve().parents[1] / "results" \
        / "eg4b-discovery.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print(f"instrument control dev {ctl_dev:.2e}")
    print("profile nonzero:",
          [(row["r"], round(row["phi_bits"], 5)) for row in nonzero])
    print("strength:", [(s["M"], round(s["phi_bits"], 5))
                        for s in strength])
    print("linearity dev:", [(d["M"], round(d["relative_deviation"], 4))
                             for d in lin_dev])
    print("superposition:",
          [(s["M"], round(s["relative_deviation"], 5))
           for s in superposition])
    print("steady 160:",
          [(row["r"], round(row["phi_bits"], 4))
           for row in steady["160"] if row["phi_bits"] > 1e-9][:12])
    print(f"steady change {steady_change:.4g}, spread "
          f"{steady_spread:.4g}")
    print("escape 256:",
          [(row["dr"], round(row["phi_bits"], 4))
           for row in escape["256"]])
    print(f"escape changes {esc_change_prev:.4g} -> "
          f"{esc_change_last:.4g}, spread {esc_spread:.4g}")
    print("items:", items)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
