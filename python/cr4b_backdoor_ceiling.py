#!/usr/bin/env python3
"""CR-4b the backdoor audit ceiling, corrected (exploratory).

Protocol declared in CRYPTO-TRACK.md before this run. CR-4 failed
two bars on a group of ninety-six elements where eight output
values cannot be near uniform, and its comparison asked whether two
parameter sets induce identical distributions, which they do not
and need not. The corrected question is sharper. A trapdoor scalar
is a constant of the parameter set, not a source of randomness, so
it cannot change any conditional distribution of the outputs. Its
whole content is the cost of a computation. An audit built from
informations must therefore be exactly blind to it, and the
measurement here is that blindness beside a positive control that
the same audit does detect.

Exploratory label. No real curve, standard, protocol,
implementation, or deployed system is modeled or evaluated, no
attack is developed, and nothing here is a claim about the security
of anything.
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

P_FIELD = 1009
OUT_BITS = 3
OUT_MASK = (1 << OUT_BITS) - 1
LEAK_BIT = 1


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


def is_prime(n):
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True


def find_curve():
    """First declared curve with prime group order."""
    for a in range(1, 40):
        for b in range(1, 40):
            if (4 * a ** 3 + 27 * b ** 2) % P_FIELD == 0:
                continue
            n = curve_order(a, b)
            if is_prime(n):
                return a, b, n
    raise RuntimeError("no prime-order curve found")


def make_tables(a, b, order):
    def inv(z):
        return pow(z % P_FIELD, P_FIELD - 2, P_FIELD)

    def padd(p, q):
        if p is None:
            return q
        if q is None:
            return p
        if p[0] == q[0] and (p[1] + q[1]) % P_FIELD == 0:
            return None
        if p == q:
            lam = (3 * p[0] * p[0] + a) * inv(2 * p[1]) % P_FIELD
        else:
            lam = (q[1] - p[1]) * inv(q[0] - p[0]) % P_FIELD
        x = (lam * lam - p[0] - q[0]) % P_FIELD
        y = (lam * (p[0] - x) - p[1]) % P_FIELD
        return (x, y)

    base = None
    for x in range(P_FIELD):
        rhs = (x * x * x + a * x + b) % P_FIELD
        if legendre(rhs) != 1:
            continue
        # the field is small, so the root is found by search and no
        # square-root shortcut is assumed about the modulus
        y = next((yy for yy in range(1, P_FIELD)
                  if (yy * yy) % P_FIELD == rhs), None)
        if y is not None:
            base = (x, y)
            break
    assert base is not None, "no base point"
    table = [None] * order
    cur = None
    for i in range(order):
        table[i] = cur
        cur = padd(cur, base)
    return base, table


def x_of(pt):
    return pt[0] if pt is not None else 0


def main() -> int:
    record: dict = {"schema": "cr4b-backdoor-ceiling-v1",
                    "label": "exploratory"}
    a, b, order = find_curve()
    base, table = make_tables(a, b, order)
    d_known = 7
    e_known = pow(d_known, order - 2, order)

    def step(s, d):
        """One generator step, returns (next state, output word)."""
        r = table[s % order]
        s2 = x_of(r) % order
        t = table[(s2 * d) % order]
        return s2, x_of(t) & OUT_MASK

    def pair_counts(d, leak=False):
        c1 = Counter()
        c12 = Counter()
        c_seed_w = Counter()
        for s in range(1, order):
            s2, w1 = step(s, d)
            if leak:
                w1 = (w1 & ~LEAK_BIT) | (s & LEAK_BIT)
            _, w2 = step(s2, d)
            c1[w1] += 1
            c12[(w1, w2)] += 1
            c_seed_w[(s & LEAK_BIT, w1)] += 1
        return c1, c12, c_seed_w

    def ent(counts, total):
        out = 0.0
        for v in counts:
            if v > 0:
                pr = v / total
                out -= pr * math.log2(pr)
        return out

    tot = order - 1
    uniform_h = float(OUT_BITS)

    # clean parameter set, declared nothing-up-my-sleeve rule, the
    # scalar recovered by enumeration only so the run can state it
    d_clean = next(k for k in range(2, order)
                   if x_of(table[k]) >= 500)

    items = {}
    c1_k, c12_k, _ = pair_counts(d_known)
    c1_c, c12_c, _ = pair_counts(d_clean)
    h1_k, h1_c = ent(c1_k.values(), tot), ent(c1_c.values(), tot)
    h12_k = ent(c12_k.values(), tot)
    h12_c = ent(c12_c.values(), tot)
    cond_k = h12_k - h1_k
    cond_c = h12_c - h1_c
    items["B2_near_uniform"] = (abs(h1_k - uniform_h) < 0.05
                                and abs(h1_c - uniform_h) < 0.05)
    items["B4_scalar_recovered_by_enumeration"] = bool(
        x_of(table[d_clean]) >= 500)

    # B3 the trapdoor confers no information, two routes
    def cond_with_trapdoor(d):
        """The holder of the scalar computes the same conditional
        law by the inverse map, a different code path and the same
        quantity."""
        c1 = Counter()
        c12 = Counter()
        for s in range(1, order):
            s2 = x_of(table[s % order]) % order
            w1 = x_of(table[(s2 * d) % order]) & OUT_MASK
            a_pt = table[(s2 * d) % order]
            s_next = x_of(table[(x_of(a_pt)
                                 * pow(d, order - 2, order))
                                % order]) % order
            w2 = x_of(table[(s_next * d) % order]) & OUT_MASK
            c1[w1] += 1
            c12[(w1, w2)] += 1
        return ent(c12.values(), tot) - ent(c1.values(), tot)

    cond_k_trap = cond_with_trapdoor(d_known)
    items["B3_trapdoor_confers_no_information"] = (
        abs(cond_k - cond_k_trap) <= 1e-9)

    # B1 the positive control, an information-theoretic leak
    c1_l, c12_l, seedw_l = pair_counts(d_clean, leak=True)
    h_seedbit = 1.0
    h_w_leak = ent(c1_l.values(), tot)
    h_joint = ent(seedw_l.values(), tot)
    mi_leak = h_seedbit + h_w_leak - h_joint
    _, _, seedw_clean = pair_counts(d_clean, leak=False)
    mi_clean = (h_seedbit + h1_c
                - ent(seedw_clean.values(), tot))
    items["B1_audit_detects_a_leak"] = (mi_leak >= 0.5
                                        and mi_clean <= 0.05)

    findings = {
        "B5_audit_blind_to_trapdoor": bool(
            abs(cond_k - cond_k_trap) <= 1e-9),
        "B6_audit_sees_leak_but_not_trapdoor": bool(
            mi_leak - mi_clean >= 0.5
            and abs(cond_k - cond_k_trap) <= 1e-9)}

    record["measured"] = {
        "field": P_FIELD, "curve": [a, b], "group_order": order,
        "base_point": list(base),
        "declared_known_scalar": d_known,
        "clean_scalar_recovered": int(d_clean),
        "output_bits": OUT_BITS,
        "public_entropy_backdoored": float(h1_k),
        "public_entropy_clean": float(h1_c),
        "uniform_entropy": uniform_h,
        "conditional_entropy_public": float(cond_k),
        "conditional_entropy_trapdoor_route": float(cond_k_trap),
        "conditional_entropy_difference":
            float(abs(cond_k - cond_k_trap)),
        "conditional_entropy_clean": float(cond_c),
        "mutual_information_leaky_bits": float(mi_leak),
        "mutual_information_clean_bits": float(mi_clean),
        "reading": "a trapdoor scalar is a constant of the "
                   "parameter set and not a source of randomness, "
                   "so it changes no conditional law and an audit "
                   "built from informations is exactly blind to "
                   "it, while the same audit sees a declared "
                   "one-bit leak immediately"}
    record["items"] = {k: bool(v) for k, v in items.items()}
    record["findings"] = findings
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items),
                         "note": "B5 and B6 are the ceiling "
                                 "measurements, either outcome a "
                                 "result"}
    record["declared"] = {
        "out_mask": OUT_MASK, "leak_bit": LEAK_BIT,
        "clean_rule": "first scalar whose point abscissa is at "
                      "least 500",
        "scope": "toy curve, methodology only, no real standard, "
                 "no attack, no claim about any system"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out_path = Path(__file__).resolve().parents[1] / "results" \
        / "cr4b-backdoor-ceiling.json"
    out_path.write_text(json.dumps(record, indent=2,
                                   sort_keys=True),
                        encoding="utf-8")
    print("curve", a, b, "order", order)
    print("H1 known", h1_k, "clean", h1_c, "uniform", uniform_h)
    print("cond public", cond_k, "cond trapdoor", cond_k_trap,
          "diff", abs(cond_k - cond_k_trap))
    print("MI leak", mi_leak, "MI clean", mi_clean)
    print("items", items)
    print("findings", findings)
    print("VERDICT", verdict)
    print(out_path)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
