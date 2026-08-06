#!/usr/bin/env python3
"""CR-0 engineered-redundancy instrument layer (exploratory, CR track).

Protocol declared in CRYPTO-TRACK.md before this run. Shamir secret
sharing over GF(31), threshold 3, five shares, secret and both
polynomial coefficients uniform. Every distribution is computed by
exact enumeration of all 31 * 961 = 29791 outcomes with integer
counting, never sampled. Informations come from integer count ratios,
so an exact ratio of one yields exactly zero, and every summation
over outcomes uses math.fsum.

Items and bars are the declared S1 through S5. The verdict is
computed from the items.

Exploratory label. Nothing here is a claim about the security of any
real cipher, protocol, implementation, or deployed system. No attack
is developed or evaluated. The models are declared toy models used to
audit evaluation methodology.
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

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402

P = 31                      # prime field
THRESHOLD = 3               # Shamir threshold t
NSHARES = 5                 # Shamir share count n
XS = (1, 2, 3, 4, 5)        # declared evaluation points
LEAK_SET = (0, 1, 2, 3, 4)  # L2's declared short randomness set
TOL = 1e-12
LEAK_BAR_BITS = 0.1
LOG2P = math.log2(P)


def shamir_outcomes():
    """All 29791 equally weighted (secret, share vector) outcomes."""
    out = []
    for s in range(P):
        for a1 in range(P):
            for a2 in range(P):
                out.append((s, tuple((s + a1 * x + a2 * x * x) % P
                                     for x in XS)))
    return out


def l1_outcomes():
    """Drafted control, field-uniform degree-one polynomial plus the
    redundant published value secret + coefficient (share six)."""
    out = []
    for s in range(P):
        for a1 in range(P):
            sh = tuple((s + a1 * x) % P for x in XS)
            out.append((s, sh + ((s + a1) % P,)))
    return out


def l2_outcomes():
    """Bar-bearing control, degree-one polynomial whose coefficient is
    uniform on the declared five-element set instead of the field."""
    out = []
    for s in range(P):
        for a1 in LEAK_SET:
            out.append((s, tuple((s + a1 * x) % P for x in XS)))
    return out


def analyse(outcomes, idxs):
    """Exact MI, secret entropy, conditional entropy, and the maximum
    deviation of the posterior on the secret from the uniform prior.

    MI is assembled from integer count ratios, so a genuinely
    independent pair contributes log2(1.0) = 0.0 with no rounding.
    """
    total = len(outcomes)
    joint: dict = {}
    csec: dict = {}
    ckey: dict = {}
    for s, sh in outcomes:
        key = tuple(sh[i] for i in idxs)
        joint[(s, key)] = joint.get((s, key), 0) + 1
        csec[s] = csec.get(s, 0) + 1
        ckey[key] = ckey.get(key, 0) + 1
    mi = math.fsum(
        (c / total) * math.log2((c * total) / (csec[s] * ckey[key]))
        for (s, key), c in joint.items())
    h_sec = math.fsum(-(c / total) * math.log2(c / total)
                      for c in csec.values())
    h_cond = math.fsum(-(c / total) * math.log2(c / ckey[key])
                       for (s, key), c in joint.items())
    unif = 1.0 / P
    dev = 0.0
    for key, ck in ckey.items():
        for s in range(P):
            post = joint.get((s, key), 0) / ck
            dev = max(dev, abs(post - unif))
    return {"mi": mi, "h_secret": h_sec, "h_cond": h_cond,
            "post_dev_from_uniform": dev,
            "route_gap": abs(mi - (h_sec - h_cond))}


def subsets(nshares):
    for k in range(1, nshares + 1):
        for idxs in itertools.combinations(range(nshares), k):
            yield idxs


def lagrange_zero(points):
    """Reconstruct f(0) over GF(P) from (x, y) pairs."""
    acc = 0
    for i, (xi, yi) in enumerate(points):
        num, den = 1, 1
        for j, (xj, _) in enumerate(points):
            if i == j:
                continue
            num = (num * (-xj)) % P
            den = (den * (xi - xj)) % P
        acc = (acc + yi * num * pow(den, P - 2, P)) % P
    return acc


def main() -> int:
    record: dict = {"schema": "cr0-instrument-v1",
                    "label": "exploratory"}
    items: dict = {}

    sh_out = shamir_outcomes()
    assert len(sh_out) == P * P * P == 29791, "outcome count"

    # ---- Shamir, every nonempty subset -----------------------------
    sh_stats = {idxs: analyse(sh_out, idxs) for idxs in
                subsets(NSHARES)}
    below = [i for i in sh_stats if len(i) < THRESHOLD]
    at_thr = [i for i in sh_stats if len(i) == THRESHOLD]
    assert len(below) == 15 and len(at_thr) == 10, "subset counts"

    # S1: below threshold reads nothing at all
    s1_max_mi = max(abs(sh_stats[i]["mi"]) for i in below)
    s1_max_post = max(sh_stats[i]["post_dev_from_uniform"]
                      for i in below)
    items["S1_below_threshold_exact_zero"] = (s1_max_mi <= TOL
                                              and s1_max_post <= TOL)

    # S2: at threshold the secret is determined, two routes
    s2_max_dev = max(abs(sh_stats[i]["mi"] - LOG2P) for i in at_thr)
    s2_max_hcond = max(abs(sh_stats[i]["h_cond"]) for i in at_thr)
    lagrange_failures = 0
    for idxs in at_thr:
        for s, sh in sh_out:
            pts = [(XS[i], sh[i]) for i in idxs]
            if lagrange_zero(pts) != s:
                lagrange_failures += 1
    assert lagrange_failures == 0, "S2 Lagrange route"
    items["S2_threshold_determines_secret"] = (
        s2_max_dev <= TOL and s2_max_hcond <= TOL
        and lagrange_failures == 0)

    # S3: the step is a step, no intermediate value anywhere
    curve = []
    for k in range(1, NSHARES + 1):
        vals = [sh_stats[i]["mi"] for i in sh_stats if len(i) == k]
        curve.append(math.fsum(vals) / len(vals))
    declared_curve = [0.0, 0.0, LOG2P, LOG2P, LOG2P]
    s3_curve_dev = max(abs(a - b) for a, b in
                       zip(curve, declared_curve))
    s3_max_intermediate = max(
        min(abs(v["mi"]), abs(v["mi"] - LOG2P))
        for v in sh_stats.values())
    items["S3_step_not_ramp"] = (s3_curve_dev <= TOL
                                 and s3_max_intermediate <= TOL)

    # ---- S4: the leaky controls ------------------------------------
    l1_out = l1_outcomes()
    l1_singles = [analyse(l1_out, (i,))["mi"] for i in range(6)]
    l1_identical = all(sh[5] == sh[0] for _, sh in l1_out)
    l1_pairs = {i: analyse(l1_out, i)["mi"] for i in
                itertools.combinations(range(6), 2)}
    l1_zero_pairs = sorted(k for k, v in l1_pairs.items()
                           if abs(v) <= TOL)
    l1_det_pairs = sum(1 for v in l1_pairs.values()
                       if abs(v - LOG2P) <= TOL)

    l2_out = l2_outcomes()
    l2_stats = {idxs: analyse(l2_out, idxs) for idxs in
                subsets(NSHARES)}
    l2_singles = [l2_stats[(i,)]["mi"] for i in range(NSHARES)]
    l2_max_single = max(l2_singles)
    l2_closed_form = math.log2(P / len(LEAK_SET))
    l2_cf_dev = max(abs(v - l2_closed_form) for v in l2_singles)
    items["S4_leaky_control_sees_leakage"] = (
        l2_max_single > LEAK_BAR_BITS and l2_cf_dev <= TOL)

    # ---- S5: route agreement over every subset tested --------------
    s5_gap = max(
        [v["route_gap"] for v in sh_stats.values()]
        + [v["route_gap"] for v in l2_stats.values()]
        + [analyse(l1_out, i)["route_gap"] for i in
           itertools.chain(((j,) for j in range(6)),
                           itertools.combinations(range(6), 2))])
    items["S5_route_agreement"] = s5_gap <= TOL

    qd0_curve = [0.8118065626958508, 0.9570774866295737,
                 0.9998238825988729, 1.042570278568172,
                 1.187841202501895, 1.9996477651977458]

    record["measured"] = {
        "s1_max_abs_mi_bits": s1_max_mi,
        "s1_max_posterior_deviation": s1_max_post,
        "s1_below_threshold_mi_bits": {
            "".join(str(XS[i]) for i in idxs): sh_stats[idxs]["mi"]
            for idxs in sorted(below, key=lambda t: (len(t), t))},
        "s2_max_mi_deviation_from_log2_31": s2_max_dev,
        "s2_max_conditional_entropy_bits": s2_max_hcond,
        "s2_lagrange_route_failures": lagrange_failures,
        "s3_shamir_mi_curve_bits": curve,
        "s3_declared_curve_bits": declared_curve,
        "s3_max_curve_deviation": s3_curve_dev,
        "s3_max_distance_to_nearest_plateau": s3_max_intermediate,
        "s4_l1_single_share_mi_bits": l1_singles,
        "s4_l1_sixth_share_identical_to_first": l1_identical,
        "s4_l1_zero_information_pairs": [list(k) for k in
                                        l1_zero_pairs],
        "s4_l1_determining_pairs": l1_det_pairs,
        "s4_l2_single_share_mi_bits": l2_singles,
        "s4_l2_closed_form_bits": l2_closed_form,
        "s4_l2_closed_form_deviation": l2_cf_dev,
        "s4_l2_pair_mi_bits": [l2_stats[i]["mi"] for i in
                               itertools.combinations(range(5), 2)],
        "s5_max_route_gap_bits": s5_gap,
        "qd0_partial_record_curve_bits": qd0_curve,
        "log2_field_size_bits": LOG2P,
        "shamir_outcome_count": len(sh_out)}
    record["items"] = {k: bool(v) for k, v in items.items()}
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["statement"] = (
        "an engineered redundancy plateau is a step function, exact "
        "independence of the secret from every subset below the "
        "declared threshold and exact determination at it, with no "
        "intermediate value at any subset of any size, while the "
        "QD track's naturally occurring plateau rose smoothly with "
        "record strength; the declared short-randomness control "
        "carries measurable single-share information at its closed "
        "form, so the zeros below threshold are a property of the "
        "scheme and not of the measurement, and the drafted "
        "redundant-share control leaks nothing to any single "
        "consumer, redundancy is not leakage")
    record["declared"] = {
        "field": P, "threshold": THRESHOLD, "shares": NSHARES,
        "evaluation_points": list(XS), "tolerance": TOL,
        "leak_bar_bits": LEAK_BAR_BITS,
        "l2_randomness_set": list(LEAK_SET),
        "enumeration": "exact integer counting, never sampled",
        "protocol": "experiments/CRYPTO-TRACK.md, CR-0"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "cr0-instrument.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("S1 max |MI|", s1_max_mi, "max posterior dev", s1_max_post)
    print("S2 max dev", s2_max_dev, "H(s|shares)", s2_max_hcond,
          "lagrange failures", lagrange_failures)
    print("S3 curve", curve)
    print("S3 max distance to plateau", s3_max_intermediate)
    print("S4 L1 singles", l1_singles)
    print("S4 L1 zero pairs", l1_zero_pairs, "determining",
          l1_det_pairs, "sixth==first", l1_identical)
    print("S4 L2 singles", l2_singles, "closed form", l2_closed_form)
    print("S5 max route gap", s5_gap)
    print("VERDICT", verdict)
    print("record sha", record["record_sha256"])
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
