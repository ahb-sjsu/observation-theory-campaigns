#!/usr/bin/env python3
"""CR-5 rigidity as designer freedom (exploratory).

Protocol declared in CRYPTO-TRACK.md before this run. CR-4c
measured that an audit built from informations is blind to a
trapdoor by an exact bound. What such an audit can see is
provenance, and provenance is a counting question. A designer who
may re-roll a derivation until the result lands in a rare weak
class needs only enough freedom to cover that class's rarity, and
the published artifact records nothing about how many rolls were
taken.

This run counts three things exactly in a toy parameter space, the
density of a declared weak class, the size of the reachable set of
a declared rigid procedure and of a declared flexible one, and
whether the flexible procedure's freedom times the density reaches
one, which is the point at which manipulation is expected to
succeed.

The connection recorded with the result. Removing the designer's
freedom to re-roll is what rigid parameter generation does in
cryptography and what preregistration does in this campaign. They
are one idea in two fields.

Exploratory label. No real curve, standard, implementation, or
deployed system is modeled or evaluated, no attack is developed,
and nothing here is a claim about the security of anything.
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

P_FIELD = 101
SMOOTH_BOUND = 5
RIGID_SEEDS = [1]
FLEX_SEED_RANGE = 4096
A_OFFSET = 17
B_OFFSET = 23


def legendre(a):
    return pow(a % P_FIELD, (P_FIELD - 1) // 2, P_FIELD)


def curve_order(a, b):
    n = 1
    for x in range(P_FIELD):
        rhs = (x * x * x + a * x + b) % P_FIELD
        if rhs == 0:
            n += 1
        elif legendre(rhs) == 1:
            n += 2
    return n


def is_smooth(n, bound):
    m = n
    f = 2
    while f * f <= m:
        while m % f == 0:
            if f > bound:
                return False
            m //= f
        f += 1
    return m <= bound or m == 1


def seed_to_curve(seed):
    a = (seed * seed + A_OFFSET) % P_FIELD
    b = (seed * seed * seed + B_OFFSET) % P_FIELD
    if (4 * a ** 3 + 27 * b ** 2) % P_FIELD == 0:
        return None
    return (a, b)


def main() -> int:
    record: dict = {"schema": "cr5-rigidity-v1",
                    "label": "exploratory"}

    # P1 the weak-class density, exact over the whole space
    total = 0
    weak = 0
    weak_set = set()
    for a in range(P_FIELD):
        for b in range(P_FIELD):
            if (4 * a ** 3 + 27 * b ** 2) % P_FIELD == 0:
                continue
            total += 1
            n = curve_order(a, b)
            if is_smooth(n, SMOOTH_BOUND):
                weak += 1
                weak_set.add((a, b))
    density = weak / total

    # P2 the reachable sets of the two declared procedures
    rigid_curves = {seed_to_curve(s) for s in RIGID_SEEDS}
    rigid_curves.discard(None)
    flex_curves = {}
    for s in range(1, FLEX_SEED_RANGE + 1):
        c = seed_to_curve(s)
        if c is not None and c not in flex_curves:
            flex_curves[c] = s
    rigid_n = len(rigid_curves)
    flex_n = len(flex_curves)

    # P3 the manipulation threshold and the demonstration
    flex_product = flex_n * density
    rigid_product = rigid_n * density
    found_seed = None
    found_curve = None
    for s in range(1, FLEX_SEED_RANGE + 1):
        c = seed_to_curve(s)
        if c is not None and c in weak_set:
            found_seed, found_curve = s, c
            break
    weak_seeds = sum(1 for s in range(1, FLEX_SEED_RANGE + 1)
                     if (seed_to_curve(s) or (None, None))
                     in weak_set)
    rigid_weak = any(c in weak_set for c in rigid_curves)

    items = {
        "P1_density_measured": total > 0 and 0.0 < density < 1.0,
        "P2_reachable_sets_counted": rigid_n >= 1 and flex_n > 1,
        "P3_threshold_and_demonstration": bool(
            flex_product >= 1.0 and found_seed is not None)}

    findings = {
        "P4_artifact_carries_no_search_count": bool(
            weak_seeds >= 1),
        "P5_rigid_procedure_below_threshold": bool(
            rigid_product < 1.0),
        "P6_rigid_procedure_landed_weak_by_chance": bool(
            rigid_weak)}

    record["measured"] = {
        "field": P_FIELD,
        "smoothness_bound": SMOOTH_BOUND,
        "nonsingular_curves": int(total),
        "weak_curves": int(weak),
        "weak_class_density": float(density),
        "rigid_reachable": int(rigid_n),
        "flexible_seed_range": FLEX_SEED_RANGE,
        "flexible_reachable_distinct": int(flex_n),
        "flexible_freedom_times_density": float(flex_product),
        "rigid_freedom_times_density": float(rigid_product),
        "first_weak_seed": (int(found_seed) if found_seed
                            else None),
        "first_weak_curve": (list(found_curve) if found_curve
                             else None),
        "weak_producing_seeds_in_range": int(weak_seeds),
        "expected_rolls_to_manipulate": (
            float(FLEX_SEED_RANGE / weak_seeds)
            if weak_seeds else None),
        "rigid_curve": [list(c) for c in sorted(rigid_curves)],
        "rigid_landed_weak": bool(rigid_weak),
        "reading": "the published artifact is a curve and a seed, "
                   "and a seed that was reached on the first roll "
                   "is indistinguishable from one reached on the "
                   "thousandth, so the artifact carries no record "
                   "of the search and only the procedure's "
                   "declared freedom is auditable"}
    record["items"] = {k: bool(v) for k, v in items.items()}
    record["findings"] = findings
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items),
                         "note": "P4 through P6 are measurements, "
                                 "either outcome a result"}
    record["declared"] = {
        "seed_map": "a = seed squared plus 17, b = seed cubed "
                    "plus 23, both modulo the field, singular "
                    "pairs rejected",
        "rigid_seeds": RIGID_SEEDS,
        "flex_seed_range": FLEX_SEED_RANGE,
        "weak_class": "group order smooth to the declared bound",
        "threshold_rule": "freedom times density at least one",
        "scope": "toy parameter space, methodology only, no real "
                 "standard, no attack, no claim about any system"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "cr5-rigidity.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("curves", total, "weak", weak, "density", density)
    print("rigid", rigid_n, "flex distinct", flex_n,
          "flex*density", flex_product)
    print("first weak seed", found_seed, found_curve,
          "weak seeds", weak_seeds)
    print("items", items)
    print("findings", findings)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
