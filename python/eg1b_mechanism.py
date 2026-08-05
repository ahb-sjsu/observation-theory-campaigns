#!/usr/bin/env python3
"""EG-1b mechanism discovery: causal determinism passes the gate
(exploratory, EG track).

The discovery effort is theory-guided by a lemma recorded in the track
document before this run.

ENTROPY-DENSITY LEMMA (proved). For a translation-invariant hidden
ensemble with entropy density h, the chain rule gives
H(interior | boundary) >= H(region) - H(boundary) >= h R^2 - c R in
two dimensions. An area-law primary count therefore forces h = 0.
Every mechanism class with positive bulk entropy density fails the
gate before construction, which is why every EG-1 arm failed. A
passing mechanism must have zero bulk entropy density with
boundary-sized residual freedom.

The natural non-inserted origin of that structure is DETERMINISTIC
LOCAL DYNAMICS with the region read as a spacetime region.

CAUSAL-CONE BOUND (proved). For any deterministic cellular automaton
of radius one, the configuration of an R x R spacetime patch is a
function of its causal-cone data, the 3R-2 initial cells whose
light cone covers the patch. Hence H(patch) <= 3R-2, perimeter
scaling, for ANY such rule and any initial ensemble. Nothing about
the rule is tuned; the bound is causality itself. The deterministic
interior also makes H(interior | patch boundary) exactly zero, since
the top row and side columns determine the interior by induction.

This runner measures the mechanism exactly and runs the
structural-origin audit demanded by the section 10 corollary
decision.

Arm one, additive rules 90 and 150. The patch cells are GF(2)-linear
functionals of the cone cells, so with an i.i.d. uniform initial
ensemble every entropy is a matrix rank, computed exactly: H(patch),
H(patch boundary), and H(interior | boundary) = rank(patch) -
rank(boundary), asserted exactly zero.

Arm two, the structural-origin audit. The same rule 90 on a ring with
one fresh noise bit per cell per step. Every entropy is again a rank
over the enlarged generator set. Bulk noise must re-inflate H(patch)
to a volume law, showing the area law tracks determinism and nothing
else.

Arm three, universality spot check. The nonlinear rule 110 at small R
by exact enumeration of all cone configurations. H(patch) must sit
inside [R, 3R-2], witnessing that the cone bound is rule-independent.

Exploratory label. The region is a spacetime region, declared, per
the corollary decision. No physics claim.
"""
from __future__ import annotations

import json
import os
import platform
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from eg1_area_gate import fit_exponent  # noqa: E402
from projection_fold import canonical_sha256  # noqa: E402

R_GRID_DET = [3, 4, 6, 8, 11, 16, 23, 32, 45, 64, 91, 128, 181, 256, 301]
R_GRID_NOISE = [3, 4, 6, 8, 11, 16, 23, 32, 45]
R_GRID_110 = [3, 4, 5]


def gf2_rank(rows_bool: np.ndarray) -> int:
    """Exact GF(2) rank of a boolean matrix, bit-packed elimination."""
    n, m = rows_bool.shape
    if n == 0 or m == 0:
        return 0
    words = (m + 63) // 64
    packed = np.zeros((n, words), dtype=np.uint64)
    for w in range(words):
        chunk = rows_bool[:, w * 64:(w + 1) * 64]
        weight = (np.uint64(1) << np.arange(chunk.shape[1],
                                            dtype=np.uint64))
        packed[:, w] = (chunk.astype(np.uint64) * weight).sum(axis=1)
    rank = 0
    for col in range(m):
        w, b = divmod(col, 64)
        bit = np.uint64(1) << np.uint64(b)
        hits = np.nonzero((packed[rank:, w] & bit) != 0)[0]
        if len(hits) == 0:
            continue
        piv = rank + hits[0]
        if piv != rank:
            packed[[rank, piv]] = packed[[piv, rank]]
        below = rank + 1 + np.nonzero(
            (packed[rank + 1:, w] & bit) != 0)[0]
        if len(below):
            packed[below] ^= packed[rank]
        rank += 1
        if rank == n:
            break
    return rank


def patch_rows_deterministic(r: int, rule: int) -> np.ndarray:
    """Boolean matrix (R^2, 3R-2): patch cells as linear functionals
    of the cone cells, for additive rule 90 or 150 on a shrinking
    window."""
    width = 3 * r - 2
    gen = np.eye(width, dtype=bool)
    rows = []
    lo = r - 1
    for t in range(r):
        rows.append(gen[lo: lo + r].copy())
        nxt = np.zeros_like(gen)
        nxt[1:-1] = gen[:-2] ^ gen[2:]
        if rule == 150:
            nxt[1:-1] ^= gen[1:-1]
        gen = nxt
    return np.concatenate(rows, axis=0)


def patch_boundary_mask(r: int) -> np.ndarray:
    mask = np.zeros((r, r), dtype=bool)
    mask[0, :] = mask[-1, :] = True
    mask[:, 0] = mask[:, -1] = True
    return mask.reshape(-1)


def deterministic_arm(rule: int):
    rows_out = []
    for r in R_GRID_DET:
        m = patch_rows_deterministic(r, rule)
        bnd = patch_boundary_mask(r)
        h_patch = gf2_rank(m)
        h_bnd = gf2_rank(m[bnd])
        h_int_given = gf2_rank(m) - h_bnd  # rank(int u bnd) - rank(bnd)
        assert r <= h_patch <= 3 * r - 2, f"cone bound broken at R={r}"
        assert h_int_given == 0, \
            f"deterministic interior must be boundary-determined, R={r}"
        rows_out.append({"R": r, "H_patch": h_patch,
                         "H_boundary": h_bnd,
                         "H_int_given_boundary": h_int_given})
    return rows_out


def noise_arm():
    rows_out = []
    for r in R_GRID_NOISE:
        ring = 3 * r
        ncols = ring * r
        gen = np.zeros((ring, ncols), dtype=bool)
        gen[:, :ring] = np.eye(ring, dtype=bool)
        rows = [gen[0:r].copy()]
        for t in range(1, r):
            gen = np.roll(gen, 1, axis=0) ^ np.roll(gen, -1, axis=0)
            gen[:, ring * t: ring * (t + 1)] = np.eye(ring, dtype=bool)
            rows.append(gen[0:r].copy())
        m = np.concatenate(rows, axis=0)
        h_patch = gf2_rank(m)
        assert h_patch >= 0.95 * r * r, f"noise arm rank low at R={r}"
        rows_out.append({"R": r, "H_patch": h_patch, "cells": r * r})
    return rows_out


def rule110_step(row: tuple[int, ...]) -> tuple[int, ...]:
    table = {(1, 1, 1): 0, (1, 1, 0): 1, (1, 0, 1): 1, (1, 0, 0): 0,
             (0, 1, 1): 1, (0, 1, 0): 1, (0, 0, 1): 1, (0, 0, 0): 0}
    return tuple(table[(row[j - 1], row[j], row[j + 1])]
                 for j in range(1, len(row) - 1))


def rule110_arm():
    rows_out = []
    for r in R_GRID_110:
        width = 3 * r - 2
        lo = r - 1
        counts: Counter = Counter()
        for x in range(2 ** width):
            row = tuple((x >> k) & 1 for k in range(width))
            cells = []
            cur = row
            offset = 0
            for t in range(r):
                start = lo - offset
                cells.extend(cur[start: start + r])
                cur = rule110_step(cur)
                offset += 1
            counts[tuple(cells)] += 1
        total = 2 ** width
        h = -sum((c / total) * np.log2(c / total)
                 for c in counts.values())
        assert r - 1e-9 <= h <= 3 * r - 2 + 1e-9, \
            f"cone bound broken for rule 110 at R={r}: {h}"
        rows_out.append({"R": r, "H_patch_bits": float(h),
                         "cone_bound": 3 * r - 2})
    return rows_out


def main() -> int:
    arm_90 = deterministic_arm(90)
    arm_150 = deterministic_arm(150)
    arm_noise = noise_arm()
    arm_110 = rule110_arm()

    rs_det = [row["R"] for row in arm_90]
    fits = {
        "rule90_patch": fit_exponent(rs_det,
                                     [w["H_patch"] for w in arm_90]),
        "rule150_patch": fit_exponent(rs_det,
                                      [w["H_patch"] for w in arm_150]),
        "noise_patch": fit_exponent([w["R"] for w in arm_noise],
                                    [w["H_patch"] for w in arm_noise]),
    }
    assert fits["rule90_patch"]["classification"] == "area"
    assert fits["rule150_patch"]["classification"] == "area"
    assert fits["noise_patch"]["classification"] == "volume"

    verdict = (
        "mechanism found: causal determinism passes the gate without "
        "insertion; for any deterministic radius-one rule the causal "
        "cone confines an R x R spacetime patch to at most 3R-2 "
        "distinguishable states' worth of entropy, measured exactly "
        "area-scaling for rules 90 and 150 over two decades of R and "
        "bounded for the nonlinear rule 110, with the deterministic "
        "interior exactly boundary-determined; the structural-origin "
        "audit holds, one fresh noise bit per cell re-inflates the "
        "same construction to a volume law, so the area law tracks "
        "determinism and nothing tuned; the entropy-density lemma "
        "explains the EG-1 negatives structurally, positive bulk "
        "entropy density forbids an area law in the primary count"
    )

    record = {
        "schema": "eg1b-mechanism-v1",
        "label": "exploratory",
        "declared": {
            "corollary_decision": "spacetime-region count decided in "
                "the track document section 10 before this run; "
                "H(patch) vs patch volume R^2 and patch boundary R; "
                "H(interior|boundary) reported alongside",
            "R_grid_deterministic": R_GRID_DET,
            "R_grid_noise": R_GRID_NOISE,
            "R_grid_rule110": R_GRID_110,
            "rules": [90, 150, 110],
            "insertion_audit": "rules generic and untuned, the cone "
                "bound holds for every radius-one deterministic rule; "
                "no area-sized structure, potential, or code declared "
                "anywhere; the noise control flips the verdict",
        },
        "lemma": "H(interior|boundary) >= h R^2 - c R, so an area-law "
                 "primary count forces zero bulk entropy density",
        "cone_bound": "H(patch) <= 3R-2 for any deterministic "
                      "radius-one rule",
        "arm_rule90": arm_90,
        "arm_rule150": arm_150,
        "arm_noise": arm_noise,
        "arm_rule110": arm_110,
        "fits": fits,
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
        / "eg1b-mechanism.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print("rule 90 H(patch):",
          [(w["R"], w["H_patch"]) for w in arm_90][:5], "...")
    print("rule 150 H(patch):",
          [(w["R"], w["H_patch"]) for w in arm_150][:5], "...")
    print("noise H(patch):",
          [(w["R"], w["H_patch"]) for w in arm_noise])
    print("rule 110 exact:",
          [(w["R"], round(w["H_patch_bits"], 4)) for w in arm_110])
    for key, f in fits.items():
        print(f"{key}: slope {f['free_slope']:.4f} -> "
              f"{f['classification']}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
