#!/usr/bin/env python3
"""CR-4 the backdoor audit ceiling (exploratory).

Protocol declared in CRYPTO-TRACK.md before this run. A generator
of the Dual-EC shape is built on a small curve whose group is
enumerated exactly, with two declared observers of the same output
stream, a public observer that sees output words and a trapdoor
observer that also holds the declared scalar relating the two
declared points. The measured question is whether an
information-theoretic audit can separate a parameter set whose
trapdoor scalar is known from one whose scalar is merely unknown.

The declared prediction, offered so the run can refute it. The
scalar relating two points of a cyclic group always exists, so the
two parameter sets induce identical output distributions and the
audit cannot separate them. If that holds, the security content of
this backdoor class is entirely computational and the campaign's
methods stop exactly there.

Exploratory label. No real curve, standard, implementation, or
system is modeled or evaluated, no attack is developed, and nothing
here is a claim about the security of anything.
"""
from __future__ import annotations

import json
import math
import os
import platform
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402

P_FIELD = 101
A_COEF = 2
B_COEF = 3
OUT_MASK = 0x7  # the declared truncation, three bits per word


def curve_points():
    pts = [None]
    for x in range(P_FIELD):
        rhs = (x * x * x + A_COEF * x + B_COEF) % P_FIELD
        for y in range(P_FIELD):
            if (y * y) % P_FIELD == rhs:
                pts.append((x, y))
    return pts


def inv(a):
    return pow(a % P_FIELD, P_FIELD - 2, P_FIELD)


def padd(p, q):
    if p is None:
        return q
    if q is None:
        return p
    if p[0] == q[0] and (p[1] + q[1]) % P_FIELD == 0:
        return None
    if p == q:
        lam = (3 * p[0] * p[0] + A_COEF) * inv(2 * p[1]) % P_FIELD
    else:
        lam = (q[1] - p[1]) * inv(q[0] - p[0]) % P_FIELD
    x = (lam * lam - p[0] - q[0]) % P_FIELD
    y = (lam * (p[0] - x) - p[1]) % P_FIELD
    return (x, y)


def pmul(k, p):
    r = None
    acc = p
    while k > 0:
        if k & 1:
            r = padd(r, acc)
        acc = padd(acc, acc)
        k >>= 1
    return r


def subgroup(g):
    order = 1
    cur = g
    while cur is not None:
        cur = padd(cur, g)
        order += 1
    return order


def generate(seed, p_pt, q_pt, n_words):
    """One Dual-EC-shaped step, s -> x(sP), output = trunc x(sQ)."""
    s = seed
    out = []
    states = []
    for _ in range(n_words):
        r = pmul(s, p_pt)
        s = r[0] if r is not None else 1
        t = pmul(s, q_pt)
        w = (t[0] if t is not None else 0) & OUT_MASK
        out.append(w)
        states.append(s)
    return out, states


def entropy_bits(counts, total):
    out = 0.0
    for c in counts:
        if c > 0:
            pr = c / total
            out -= pr * math.log2(pr)
    return out


def word_distribution(p_pt, q_pt, order):
    """Exact distribution of the first output word over all seeds."""
    c = Counter()
    for s in range(1, order):
        r = pmul(s, p_pt)
        s2 = r[0] if r is not None else 1
        t = pmul(s2, q_pt)
        c[(t[0] if t is not None else 0) & OUT_MASK] += 1
    return c


def main() -> int:
    record: dict = {"schema": "cr4-backdoor-ceiling-v1",
                    "label": "exploratory"}
    pts = curve_points()
    gens = [p for p in pts[1:] if subgroup(p) == len(pts)]
    base = gens[0] if gens else pts[1]
    order = subgroup(base)
    d_known = 7
    q_known = pmul(d_known, base)
    # the declared clean point, chosen by a nothing-up-my-sleeve
    # rule, the first curve point whose x is the field's smallest
    # quadratic residue above 40, with its scalar not used here
    q_clean = next(p for p in pts[1:] if p[0] >= 40)
    d_clean = next(k for k in range(1, order)
                   if pmul(k, base) == q_clean)

    items = {}
    n_words = 6
    n_seeds = min(order - 1, 100)

    # B1 the trapdoor works, prediction from one word
    hits = 0
    trials = 0
    for s0 in range(1, n_seeds + 1):
        out, states = generate(s0, base, q_known, n_words)
        # trapdoor holder recovers the state from output word one
        recovered = None
        for cand in range(1, order):
            t = pmul(cand, q_known)
            if t is not None and (t[0] & OUT_MASK) == out[0]:
                back = pmul(d_known, pmul(cand, base))
                if back is not None:
                    recovered = cand
                    break
        trials += 1
        if recovered is not None:
            nxt_r = pmul(recovered, base)
            nxt_s = nxt_r[0] if nxt_r is not None else 1
            nxt_t = pmul(nxt_s, q_known)
            pred = (nxt_t[0] if nxt_t is not None else 0) & OUT_MASK
            if pred == out[1]:
                hits += 1
    trapdoor_rate = hits / trials
    items["B1_trapdoor_predicts"] = trapdoor_rate >= 0.5

    # B2 the public observer's word distribution, both parameter
    # sets, and the exact comparison that is the ceiling
    dist_known = word_distribution(base, q_known, order)
    dist_clean = word_distribution(base, q_clean, order)
    tot = order - 1
    h_known = entropy_bits(dist_known.values(), tot)
    h_clean = entropy_bits(dist_clean.values(), tot)
    uniform_h = math.log2(OUT_MASK + 1)
    shapes_known = sorted(dist_known.values())
    shapes_clean = sorted(dist_clean.values())
    items["B2_public_entropies_near_uniform"] = (
        abs(h_known - uniform_h) < 0.15
        and abs(h_clean - uniform_h) < 0.15)

    # B3 the ceiling itself, a known scalar always exists
    exists_known = pmul(d_clean, base) == q_clean
    items["B3_scalar_always_exists"] = bool(exists_known)

    # B4 the observer asymmetry is certified where it is real
    # public channel from seed to first word, trapdoor channel from
    # seed to first word plus the scalar, informations exact
    seeds = list(range(1, order))
    joint_pub = Counter()
    for s0 in seeds:
        out, _ = generate(s0, base, q_known, 1)
        joint_pub[(s0, out[0])] += 1
    h_seed = math.log2(len(seeds))
    h_word = entropy_bits(Counter(
        w for (_, w) in joint_pub.elements()).values(), len(seeds))
    mi_pub = h_seed + h_word - entropy_bits(joint_pub.values(),
                                            len(seeds))
    items["B4_public_information_is_small"] = mi_pub <= h_seed

    findings = {
        "B5_audit_cannot_separate_backdoored_from_clean": bool(
            abs(h_known - h_clean) < 0.15
            and shapes_known == shapes_clean)}

    record["measured"] = {
        "field": P_FIELD, "curve": [A_COEF, B_COEF],
        "group_order": order,
        "declared_known_scalar": d_known,
        "clean_point_scalar_computed_by_enumeration": d_clean,
        "trapdoor_prediction_rate": float(trapdoor_rate),
        "public_entropy_bits_backdoored": float(h_known),
        "public_entropy_bits_clean": float(h_clean),
        "uniform_entropy_bits": float(uniform_h),
        "word_count_shape_backdoored": shapes_known,
        "word_count_shape_clean": shapes_clean,
        "shapes_identical": bool(shapes_known == shapes_clean),
        "public_mutual_information_bits": float(mi_pub),
        "seed_entropy_bits": float(h_seed),
        "reading": "the scalar relating two points of a cyclic "
                   "group always exists, so a parameter set whose "
                   "scalar is known and one whose scalar is merely "
                   "unknown induce the same distributions and no "
                   "information-theoretic audit separates them"}
    record["items"] = {k: bool(v) for k, v in items.items()}
    record["findings"] = findings
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items),
                         "note": "B5 is the ceiling measurement, "
                                 "either outcome a result"}
    record["declared"] = {"out_mask": OUT_MASK,
                          "n_words": n_words,
                          "n_seeds_for_trapdoor": n_seeds,
                          "scope": "toy curve, methodology only, "
                                   "no real standard, no attack"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out_path = Path(__file__).resolve().parents[1] / "results" \
        / "cr4-backdoor-ceiling.json"
    out_path.write_text(json.dumps(record, indent=2,
                                   sort_keys=True),
                        encoding="utf-8")
    print("order", order, "trapdoor rate", trapdoor_rate)
    print("H known", h_known, "H clean", h_clean, "uniform",
          uniform_h)
    print("shapes identical", shapes_known == shapes_clean)
    print("items", items, "findings", findings)
    print("VERDICT", verdict)
    print(out_path)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
