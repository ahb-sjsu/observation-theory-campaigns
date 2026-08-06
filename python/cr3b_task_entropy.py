#!/usr/bin/env python3
"""CR-3b corrected task-entropy run (CR track).

CR-3 failed on one clause of E2, the additive gap between Shannon
entropy and min-entropy was declared strictly increasing along the
eps ladder and the run measured it rising then falling. Both
entropies go to zero together as the spike takes all the mass, so
the gap has an interior maximum and the additive difference was the
wrong quantity to ask for monotonicity from. The CR-3b protocol,
declared in CRYPTO-TRACK.md before this run, keeps the ordering and
equality clauses, replaces the monotonicity clause with the ratio of
min-entropy to Shannon entropy, declares the additive gap unimodal
with a bracketed sign change, checks the closed-form derivative
against a finite difference, and locates the interior maximum.

Items and bars are the declared F1, F2, F3, with F4 and E5 recorded
as measurements carrying no bar. The verdict is computed from the
items.

Exploratory label. Nothing here is a claim about any real
key-generation system, any cipher, any protocol, or any deployed
system. The hard limit of CRYPTO-TRACK.md section 1 governs.
"""
from __future__ import annotations

import json
import math
import os
import platform
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cr3_task_entropy import (KEY_MATERIAL, N, S_LADDER, TAIL, TOL,  # noqa: E402,E501
                              U_LADDER, measure, shannon_closed)
from projection_fold import canonical_sha256  # noqa: E402

DERIV_TOL = 1e-6             # declared F3 route tolerance
BISECT_WIDTH = 1e-12         # declared F4 bracket width
BRACKET = ("0.30", "0.60")   # declared F2 sign-change bracket


def gap_closed(a: float) -> float:
    """Shannon entropy minus min-entropy at spike weight a."""
    tail = (1.0 - a) / TAIL
    h = math.fsum([-a * math.log2(a), -(1.0 - a) * math.log2(tail)])
    return h + math.log2(a)


def gap_derivative(a: float) -> float:
    """Closed-form d(gap)/da, declared in the CR-3b protocol."""
    return (math.log2((1.0 - a) / (TAIL * a))
            + 1.0 / (a * math.log(2.0)))


def central_difference(a: float, h: float = 1e-6) -> float:
    return (gap_closed(a + h) - gap_closed(a - h)) / (2.0 * h)


def main() -> int:
    record: dict = {"schema": "cr3b-task-entropy-v1",
                    "label": "exploratory"}
    items: dict = {}

    sources = []
    for e in U_LADDER:
        sources.append(measure("U(eps=%s)" % e, "U", e,
                               Fraction(1, N) + Fraction(e)))
    for q in S_LADDER:
        sources.append(measure("S(q=%s)" % q, "S", q, Fraction(q)))
    u_rows = [s for s in sources if s["family"] == "U"]
    s_rows = [s for s in sources if s["family"] == "S"]

    # ---- F1 the unchanged items ------------------------------------
    f1_max_h_dev = max(s["shannon_closed_form_deviation"]
                       for s in sources)
    f1_max_hmin_dev = max(s["min_entropy_route2_deviation"]
                          for s in sources)
    f1_scan_ok = all(s["scan_max_equals_spike_weight"]
                     for s in sources)
    f1_e3_max_dev = max(s["guess_identity_deviation"]
                        for s in sources)
    f1_e3_bit_exact = sum(1 for s in sources
                          if s["guess_identity_deviation"] == 0.0)
    f1_e4_lower = min(s["huffman_lower_margin"] for s in sources)
    f1_e4_upper = min(s["huffman_upper_margin"] for s in sources)
    f1_kraft = all(s["kraft_sum"] == "1" for s in sources)
    items["F1_unchanged_items_repeat"] = bool(
        f1_max_h_dev <= TOL and f1_max_hmin_dev <= TOL and f1_scan_ok
        and f1_e3_max_dev <= TOL and f1_e4_lower >= -TOL
        and f1_e4_upper > 0.0 and f1_kraft)

    # ---- F2 ordering and limit, corrected --------------------------
    f2_worst_ordering = max(s["min_entropy_bits"] - s["shannon_bits"]
                            for s in sources)
    gaps = [s["gap_shannon_minus_min_bits"] for s in u_rows]
    f2_uniform_gap = gaps[0]
    f2_equality_only_at_uniform = bool(
        abs(f2_uniform_gap) <= TOL and all(g > TOL for g in gaps[1:]))

    u_ratios = [s["min_over_shannon_ratio"] for s in u_rows]
    s_ratios = [s["min_over_shannon_ratio"] for s in s_rows]
    f2_u_ratio_pairs = [bool(u_ratios[i + 1] < u_ratios[i])
                        for i in range(len(u_ratios) - 1)]
    f2_s_ratio_pairs = [bool(s_ratios[i + 1] < s_ratios[i])
                        for i in range(len(s_ratios) - 1)]
    f2_ratio_decreasing = (all(f2_u_ratio_pairs)
                           and all(f2_s_ratio_pairs))

    a_ladder = [s["spike_weight_float"] for s in u_rows]
    derivs = [gap_derivative(a) for a in a_ladder]
    signs = [1 if d > 0 else (-1 if d < 0 else 0) for d in derivs]
    sign_changes = [i for i in range(len(signs) - 1)
                    if signs[i] != signs[i + 1]]
    f2_one_sign_change = len(sign_changes) == 1
    lo_i = sign_changes[0] if f2_one_sign_change else -1
    f2_bracket_as_declared = bool(
        f2_one_sign_change
        and U_LADDER[lo_i] == BRACKET[0]
        and U_LADDER[lo_i + 1] == BRACKET[1])
    increments = [gaps[i + 1] - gaps[i] for i in range(len(gaps) - 1)]
    f2_increments_before = all(increments[i] > 0.0
                               for i in range(lo_i)) if lo_i >= 0 \
        else False
    f2_increments_after = all(increments[i] < 0.0
                              for i in range(lo_i + 1,
                                             len(increments))) \
        if lo_i >= 0 else False
    items["F2_ordering_ratio_and_unimodality"] = bool(
        f2_worst_ordering <= TOL and f2_equality_only_at_uniform
        and f2_ratio_decreasing and f2_bracket_as_declared
        and f2_increments_before and f2_increments_after)

    # ---- F3 the derivative route -----------------------------------
    fd = [central_difference(a) for a in a_ladder]
    f3_devs = [abs(d - f) for d, f in zip(derivs, fd)]
    f3_max_dev = max(f3_devs)
    items["F3_derivative_route_agreement"] = bool(
        f3_max_dev <= DERIV_TOL)

    # ---- F4 the interior maximum, no bar ---------------------------
    lo = float(Fraction(1, N) + Fraction(BRACKET[0]))
    hi = float(Fraction(1, N) + Fraction(BRACKET[1]))
    d_lo, d_hi = gap_derivative(lo), gap_derivative(hi)
    steps = 0
    while hi - lo > BISECT_WIDTH:
        mid = 0.5 * (lo + hi)
        if gap_derivative(mid) > 0.0:
            lo = mid
        else:
            hi = mid
        steps += 1
    a_star = 0.5 * (lo + hi)
    gap_star = gap_closed(a_star)
    f4 = {"bracket_lo_spike_weight": float(Fraction(1, N)
                                           + Fraction(BRACKET[0])),
          "bracket_hi_spike_weight": float(Fraction(1, N)
                                           + Fraction(BRACKET[1])),
          "derivative_at_bracket_lo": d_lo,
          "derivative_at_bracket_hi": d_hi,
          "bisection_steps": steps,
          "final_bracket_width": hi - lo,
          "maximizing_spike_weight": a_star,
          "maximizing_eps": a_star - 1.0 / N,
          "maximum_gap_bits": gap_star,
          "derivative_at_maximum": gap_derivative(a_star),
          "shannon_at_maximum_bits": shannon_closed(
              Fraction(a_star).limit_denominator(10 ** 12)),
          "largest_ladder_gap_bits": max(gaps)}

    # ---- E5 the divergence measurement, no bar ---------------------
    km = next(s for s in sources if s["name"] == KEY_MATERIAL)
    e5 = {"case": KEY_MATERIAL,
          "shannon_bits": km["shannon_bits"],
          "min_entropy_bits": km["min_entropy_bits"],
          "min_over_shannon_ratio": km["min_over_shannon_ratio"],
          "shannon_over_min_factor": (km["shannon_bits"]
                                      / km["min_entropy_bits"]),
          "single_guess_success": km["single_guess_success"],
          "huffman_mean_length": km["huffman_mean_length"]}

    record["measured"] = {
        "sources": sources,
        "f1_max_shannon_closed_form_deviation": f1_max_h_dev,
        "f1_max_min_entropy_route_deviation": f1_max_hmin_dev,
        "f1_scan_max_matches_closed_form": f1_scan_ok,
        "f1_max_guess_identity_deviation": f1_e3_max_dev,
        "f1_bit_exact_guess_sources": f1_e3_bit_exact,
        "f1_min_huffman_lower_margin_bits": f1_e4_lower,
        "f1_min_huffman_upper_margin_bits": f1_e4_upper,
        "f1_kraft_equalities_hold": f1_kraft,
        "f2_worst_min_minus_shannon_bits": f2_worst_ordering,
        "f2_uniform_member_gap_bits": f2_uniform_gap,
        "f2_equality_only_at_uniform": f2_equality_only_at_uniform,
        "f2_eps_ladder": list(U_LADDER),
        "f2_q_ladder": list(S_LADDER),
        "f2_gap_ladder_bits": gaps,
        "f2_gap_increments_bits": increments,
        "f2_u_ratio_ladder": u_ratios,
        "f2_s_ratio_ladder": s_ratios,
        "f2_u_ratio_strictly_decreasing_pairwise": f2_u_ratio_pairs,
        "f2_s_ratio_strictly_decreasing_pairwise": f2_s_ratio_pairs,
        "f2_gap_derivative_ladder": derivs,
        "f2_gap_derivative_signs": signs,
        "f2_sign_change_count": len(sign_changes),
        "f2_sign_change_bracket": ([U_LADDER[lo_i],
                                    U_LADDER[lo_i + 1]]
                                   if f2_one_sign_change else []),
        "f2_bracket_as_declared": f2_bracket_as_declared,
        "f2_increments_positive_before_bracket": bool(
            f2_increments_before),
        "f2_increments_negative_after_bracket": bool(
            f2_increments_after),
        "f3_finite_difference_ladder": fd,
        "f3_deviation_ladder": f3_devs,
        "f3_max_deviation": f3_max_dev,
        "f4_interior_maximum": f4,
        "e5_key_material_case": e5}
    record["items"] = {k: bool(v) for k, v in items.items()}
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["statement"] = (
        "the corrected monotone statement holds where the refuted one "
        "did not, the fraction of the averaging consumer's accounting "
        "that survives to the single-guess consumer falls strictly "
        "along both declared ladders while the additive difference "
        "between the two accountings is unimodal, rising to an "
        "interior maximum and falling back to zero as the source "
        "becomes certain under either accounting; the two consumers "
        "price the declared key-material source at 3.477 bits and 1 "
        "bit, and which entropy is the right entropy is set by the "
        "consumer's task rather than by the source; nothing here is a "
        "claim about any real key-generation system")
    record["declared"] = {
        "alphabet_size": N, "tolerance": TOL,
        "derivative_tolerance": DERIV_TOL,
        "bisection_width": BISECT_WIDTH,
        "sign_change_bracket_eps": list(BRACKET),
        "u_family_eps_ladder": list(U_LADDER),
        "s_family_q_ladder": list(S_LADDER),
        "key_material_case": KEY_MATERIAL,
        "arithmetic": "exact rationals via Fraction, fsum summation",
        "huffman": "implemented here with a heap, no library import",
        "verdict_from": ["F1", "F2", "F3"],
        "f4_and_e5_carry_no_bar": True,
        "corrects": "CR-3 E2 gap-monotonicity clause",
        "protocol": "experiments/CRYPTO-TRACK.md, CR-3b"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "cr3b-task-entropy.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")

    for s in sources:
        print("%-14s H=%.15f Hmin=%.15f gap=%.15f ratio=%.15f "
              "pguess=%.15f Lbar=%.15f"
              % (s["name"], s["shannon_bits"], s["min_entropy_bits"],
                 s["gap_shannon_minus_min_bits"],
                 s["min_over_shannon_ratio"],
                 s["single_guess_success"],
                 s["huffman_mean_length"]))
    print("items", items)
    print("F1 H dev", f1_max_h_dev, "Hmin dev", f1_max_hmin_dev,
          "guess dev", f1_e3_max_dev, "bit exact", f1_e3_bit_exact,
          "lower", f1_e4_lower, "upper", f1_e4_upper, "kraft",
          f1_kraft)
    print("F2 worst ordering", f2_worst_ordering, "uniform gap",
          f2_uniform_gap)
    print("F2 U ratios", u_ratios)
    print("F2 S ratios", s_ratios)
    print("F2 derivatives", derivs)
    print("F2 signs", signs, "changes", len(sign_changes),
          "bracket as declared", f2_bracket_as_declared)
    print("F2 gap increments", increments)
    print("F3 max deviation", f3_max_dev)
    print("F4", f4)
    print("E5", e5)
    print("VERDICT", verdict)
    print("record sha", record["record_sha256"])
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
