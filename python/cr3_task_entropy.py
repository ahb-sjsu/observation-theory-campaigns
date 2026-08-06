#!/usr/bin/env python3
"""CR-3 task entropy, min-entropy against Shannon entropy (CR track).

Protocol declared in CRYPTO-TRACK.md before this run. One declared
source read by two consumers, one averaging over many independent
reads and one making a single guess. Two declared families on an
alphabet of 32 outcomes, the near-uniform family U(eps) and the
spike-plus-uniform family S(q), every probability an exact rational
built from Python Fractions so the masses sum to exactly one and the
Huffman construction compares exact rationals rather than rounded
floats. Every summation over outcomes uses math.fsum.

Items and bars are the declared E1 through E4, with E5 recorded as a
measurement carrying no bar. The verdict is computed from the items.

Exploratory label. Nothing here is a claim about any real
key-generation system, any cipher, any protocol, or any deployed
system. The hard limit of CRYPTO-TRACK.md section 1 governs.
"""
from __future__ import annotations

import heapq
import itertools
import json
import math
import os
import platform
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402

N = 32                       # declared alphabet size
TAIL = N - 1                 # outcomes sharing the remaining mass
TOL = 1e-12
U_LADDER = ("0", "0.01", "0.05", "0.15", "0.30", "0.60", "0.90")
S_LADDER = ("0.5", "0.9", "0.99")
KEY_MATERIAL = "S(q=0.5)"    # the declared textbook key-material case


def source(a: Fraction):
    """The declared 32-outcome source with spike weight a."""
    rest = (1 - a) / TAIL
    probs = (a,) + (rest,) * TAIL
    assert sum(probs) == 1, "declared masses must sum to exactly one"
    return probs


def shannon_summed(probs) -> float:
    """H from the distribution, one term per outcome, fsum."""
    return math.fsum(-float(p) * math.log2(float(p)) for p in probs)


def shannon_closed(a: Fraction) -> float:
    """The declared closed form at spike weight a."""
    af = float(a)
    tailf = float((1 - a) / TAIL)
    return math.fsum([-af * math.log2(af),
                      -float(1 - a) * math.log2(tailf)])


def scan_max(probs):
    """Exhaustive maximization over the alphabet, no assumption."""
    best_i, best_p = 0, probs[0]
    for i, p in enumerate(probs):
        if p > best_p:
            best_i, best_p = i, p
    return best_i, best_p


def min_entropy(pmax: Fraction) -> float:
    return -math.log2(float(pmax))


def min_entropy_route2(pmax: Fraction) -> float:
    """Second route, from the exact numerator and denominator."""
    return math.log2(pmax.denominator) - math.log2(pmax.numerator)


def huffman_lengths(probs):
    """Exact Huffman code lengths, heap over exact rationals."""
    heap = []
    tiebreak = itertools.count()
    for i, p in enumerate(probs):
        heapq.heappush(heap, (p, next(tiebreak), (i,)))
    lengths = [0] * len(probs)
    if len(heap) == 1:
        return [1]
    while len(heap) > 1:
        w1, _, g1 = heapq.heappop(heap)
        w2, _, g2 = heapq.heappop(heap)
        merged = g1 + g2
        for i in merged:
            lengths[i] += 1
        heapq.heappush(heap, (w1 + w2, next(tiebreak), merged))
    return lengths


def kraft(lengths) -> Fraction:
    return sum(Fraction(1, 2 ** L) for L in lengths)


def measure(name, family, param, a: Fraction):
    probs = source(a)
    h_sum = shannon_summed(probs)
    h_cf = shannon_closed(a)
    arg, pmax = scan_max(probs)
    hmin = min_entropy(pmax)
    hmin2 = min_entropy_route2(pmax)
    lengths = huffman_lengths(probs)
    mean_len_exact = sum(p * L for p, L in zip(probs, lengths))
    mean_len = float(mean_len_exact)
    return {
        "name": name, "family": family, "param": param,
        "spike_weight": str(a), "spike_weight_float": float(a),
        "tail_mass_each": str((1 - a) / TAIL),
        "shannon_bits": h_sum,
        "shannon_closed_form_bits": h_cf,
        "shannon_closed_form_deviation": abs(h_sum - h_cf),
        "min_entropy_bits": hmin,
        "min_entropy_route2_deviation": abs(hmin - hmin2),
        "argmax_outcome": arg,
        "max_probability": str(pmax),
        "scan_max_equals_spike_weight": bool(pmax == a),
        "gap_shannon_minus_min_bits": h_sum - hmin,
        "min_over_shannon_ratio": (hmin / h_sum) if h_sum > 0 else
        float("nan"),
        "single_guess_success": float(pmax),
        "two_to_minus_min_entropy": 2.0 ** (-hmin),
        "guess_identity_deviation": abs(float(pmax) - 2.0 ** (-hmin)),
        "huffman_mean_length": mean_len,
        "huffman_mean_length_exact": str(mean_len_exact),
        "huffman_length_histogram": {
            str(L): lengths.count(L) for L in sorted(set(lengths))},
        "huffman_lower_margin": mean_len - h_sum,
        "huffman_upper_margin": (h_sum + 1.0) - mean_len,
        "kraft_sum": str(kraft(lengths)),
    }


def main() -> int:
    record: dict = {"schema": "cr3-task-entropy-v1",
                    "label": "exploratory"}
    items: dict = {}

    sources = []
    for e in U_LADDER:
        eps = Fraction(e)
        sources.append(measure("U(eps=%s)" % e, "U", e,
                               Fraction(1, N) + eps))
    for q in S_LADDER:
        sources.append(measure("S(q=%s)" % q, "S", q, Fraction(q)))

    u_rows = [s for s in sources if s["family"] == "U"]

    # ---- E1 closed forms -------------------------------------------
    e1_max_h_dev = max(s["shannon_closed_form_deviation"]
                       for s in sources)
    e1_max_hmin_dev = max(s["min_entropy_route2_deviation"]
                          for s in sources)
    e1_scan_ok = all(s["scan_max_equals_spike_weight"]
                     for s in sources)
    items["E1_closed_forms"] = bool(e1_max_h_dev <= TOL
                                    and e1_max_hmin_dev <= TOL
                                    and e1_scan_ok)

    # ---- E2 ordering and limit -------------------------------------
    e2_worst_ordering = max(s["min_entropy_bits"] - s["shannon_bits"]
                            for s in sources)
    e2_ordering_ok = e2_worst_ordering <= TOL
    gaps = [s["gap_shannon_minus_min_bits"] for s in u_rows]
    e2_uniform_gap = gaps[0]
    e2_equality_only_at_uniform = bool(
        abs(e2_uniform_gap) <= TOL
        and all(g > TOL for g in gaps[1:]))
    e2_increasing_pairs = [bool(gaps[i + 1] > gaps[i])
                           for i in range(len(gaps) - 1)]
    e2_gap_increasing = all(e2_increasing_pairs)
    items["E2_ordering_and_limit"] = bool(
        e2_ordering_ok and e2_equality_only_at_uniform
        and e2_gap_increasing)

    # ---- E3 single-guess consumer ----------------------------------
    e3_max_dev = max(s["guess_identity_deviation"] for s in sources)
    e3_bit_exact = sum(1 for s in sources
                       if s["guess_identity_deviation"] == 0.0)
    items["E3_single_guess_identity"] = bool(e3_max_dev <= TOL)

    # ---- E4 averaging consumer -------------------------------------
    e4_min_lower = min(s["huffman_lower_margin"] for s in sources)
    e4_min_upper = min(s["huffman_upper_margin"] for s in sources)
    e4_kraft_ok = all(s["kraft_sum"] == "1" for s in sources)
    items["E4_huffman_bound"] = bool(e4_min_lower >= -TOL
                                     and e4_min_upper > 0.0
                                     and e4_kraft_ok)

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
        "e1_max_shannon_closed_form_deviation": e1_max_h_dev,
        "e1_max_min_entropy_route_deviation": e1_max_hmin_dev,
        "e1_scan_max_matches_closed_form": e1_scan_ok,
        "e2_worst_min_minus_shannon_bits": e2_worst_ordering,
        "e2_uniform_member_gap_bits": e2_uniform_gap,
        "e2_equality_only_at_uniform": e2_equality_only_at_uniform,
        "e2_eps_ladder": list(U_LADDER),
        "e2_gap_ladder_bits": gaps,
        "e2_gap_strictly_increasing_pairwise": e2_increasing_pairs,
        "e2_gap_strictly_increasing": bool(e2_gap_increasing),
        "e2_ratio_ladder_min_over_shannon": [
            s["min_over_shannon_ratio"] for s in u_rows],
        "e3_max_guess_identity_deviation": e3_max_dev,
        "e3_bit_exact_sources": e3_bit_exact,
        "e3_source_count": len(sources),
        "e4_min_lower_margin_bits": e4_min_lower,
        "e4_min_upper_margin_bits": e4_min_upper,
        "e4_kraft_equalities_hold": e4_kraft_ok,
        "e5_key_material_case": e5}
    record["items"] = {k: bool(v) for k, v in items.items()}
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["statement"] = (
        "the same declared source priced by two consumers, an "
        "averaging consumer whose accounting is Shannon entropy and "
        "a single-guess consumer whose accounting is min-entropy, "
        "with both accountings validated operationally, the "
        "single-guess success probability equal to two to the minus "
        "min-entropy by exhaustive maximization and the Huffman mean "
        "length inside the classic Shannon bound; which entropy is "
        "the right entropy is set by the consumer's task and not by "
        "the source, the GD-3 lesson in entropy accounting form; "
        "nothing here is a claim about any real key-generation "
        "system")
    record["declared"] = {
        "alphabet_size": N, "tolerance": TOL,
        "u_family_eps_ladder": list(U_LADDER),
        "s_family_q_ladder": list(S_LADDER),
        "key_material_case": KEY_MATERIAL,
        "arithmetic": "exact rationals via Fraction, fsum summation",
        "huffman": "implemented here with a heap, no library import",
        "verdict_from": ["E1", "E2", "E3", "E4"],
        "e5_carries_no_bar": True,
        "protocol": "experiments/CRYPTO-TRACK.md, CR-3"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "cr3-task-entropy.json"
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
    print("E1 max H dev", e1_max_h_dev, "max Hmin route dev",
          e1_max_hmin_dev, "scan ok", e1_scan_ok)
    print("E2 worst ordering", e2_worst_ordering, "uniform gap",
          e2_uniform_gap, "equality only at uniform",
          e2_equality_only_at_uniform)
    print("E2 gap ladder", gaps)
    print("E2 increasing pairwise", e2_increasing_pairs)
    print("E3 max dev", e3_max_dev, "bit exact", e3_bit_exact,
          "of", len(sources))
    print("E4 min lower margin", e4_min_lower, "min upper margin",
          e4_min_upper, "kraft", e4_kraft_ok)
    print("E5", e5)
    print("VERDICT", verdict)
    print("record sha", record["record_sha256"])
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
