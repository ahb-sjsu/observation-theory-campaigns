#!/usr/bin/env python3
"""Generate pgfplots data tables for the CR crypto-arc paper.

Every number is read from a committed evidence record in results/.
Pure standard library, no numpy, no free parameters. Output tables
land in paper/figdata/. The check() calls bind every value typed in
paper/crypto-audits.tex, in its tables and in its prose, to the
record value it was copied from, so a record edit breaks the build
rather than silently disagreeing with the paper.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "figdata"
OUT.mkdir(exist_ok=True)
TRACK = (ROOT / "experiments" / "CRYPTO-TRACK.md").read_text(
    encoding="utf-8")

CHECKS = 0


def check_declared(label: str, text: str) -> None:
    """Bind a declared parameter typed in the paper to the track."""
    global CHECKS
    assert text in TRACK, f"{label}: not declared in CRYPTO-TRACK.md"
    CHECKS += 1


def load(name: str) -> dict:
    return json.loads((ROOT / "results" / name).read_text(
        encoding="utf-8"))


def write(name: str, header: str, rows) -> None:
    lines = [header] + [" ".join(f"{v:.12g}" for v in row)
                        for row in rows]
    (OUT / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{name}: {len(lines) - 1} rows")


def check(label: str, record_value: float, typed: float,
          tol: float) -> None:
    """Bind a value typed in the paper to its record value."""
    global CHECKS
    assert abs(record_value - typed) <= tol, (
        f"{label}: paper types {typed}, record holds {record_value}")
    CHECKS += 1


def check_exact(label: str, record_value, typed) -> None:
    global CHECKS
    assert record_value == typed, (
        f"{label}: paper types {typed!r}, record holds "
        f"{record_value!r}")
    CHECKS += 1


# ---------------------------------------------------------------
# CR-0, the engineered step against the natural ramp.
# ---------------------------------------------------------------
cr0 = load("cr0-instrument.json")
qd0 = load("qd0-instrument.json")
m0 = cr0["measured"]

check_exact("CR-0 verdict", cr0["verdict"]["value"], "PASS")
for key in ("S1_below_threshold_exact_zero",
            "S2_threshold_determines_secret", "S3_step_not_ramp",
            "S4_leaky_control_sees_leakage", "S5_route_agreement"):
    check_exact(f"CR-0 item {key}", cr0["items"][key], True)

log2_31 = m0["log2_field_size_bits"]
check("CR-0 log2 field size", log2_31, 4.954196310386875, 0.0)
check_exact("CR-0 curve is the declared curve",
            m0["s3_shamir_mi_curve_bits"], m0["s3_declared_curve_bits"])
check("CR-0 distance to plateau",
      m0["s3_max_distance_to_nearest_plateau"], 0.0, 0.0)
check("CR-0 below-threshold information", m0["s1_max_abs_mi_bits"],
      0.0, 0.0)
check("CR-0 posterior deviation", m0["s1_max_posterior_deviation"],
      0.0, 0.0)
check("CR-0 conditional entropy at threshold",
      m0["s2_max_conditional_entropy_bits"], 0.0, 0.0)
check("CR-0 threshold information deviation",
      m0["s2_max_mi_deviation_from_log2_31"], 0.0, 0.0)
check_exact("CR-0 Lagrange failures",
            m0["s2_lagrange_route_failures"], 0)
check_exact("CR-0 outcome count", m0["shamir_outcome_count"], 29791)
# The paper quotes the number of Lagrange subset-outcome checks as
# the ten threshold subsets times the enumerated outcomes.
check_exact("CR-0 Lagrange check count",
            10 * m0["shamir_outcome_count"], 297910)
check_exact("CR-0 below-threshold subsets counted",
            len(m0["s1_below_threshold_mi_bits"]), 15)
check("CR-0 route agreement", m0["s5_max_route_gap_bits"],
      1.8e-15, 5e-17)

l2 = m0["s4_l2_single_share_mi_bits"]
check_exact("CR-0 L2 single-share subsets", len(l2), 5)
check("CR-0 L2 single-share information", l2[0],
      2.6322682154995127, 0.0)
check("CR-0 L2 closed-form deviation",
      m0["s4_l2_closed_form_deviation"], 0.0, 0.0)
assert all(abs(v - l2[0]) == 0.0 for v in l2), "L2 shares differ"
assert all(abs(v - log2_31) == 0.0
           for v in m0["s4_l2_pair_mi_bits"]), "L2 pairs off plateau"
check_exact("CR-0 leak bar", cr0["declared"]["leak_bar_bits"], 0.1)
# The paper says L2 clears its declared bar by more than a factor
# of 26.
assert l2[0] / cr0["declared"]["leak_bar_bits"] > 26.0, \
    "L2 clears its bar by less than a factor of 26"
CHECKS += 1

check_exact("CR-0 L1 single-share informations",
            m0["s4_l1_single_share_mi_bits"], [0.0] * 6)
check_exact("CR-0 L1 redundant value equals share one",
            m0["s4_l1_sixth_share_identical_to_first"], True)
check_exact("CR-0 L1 determining pairs",
            m0["s4_l1_determining_pairs"], 14)
check_exact("CR-0 L1 uninformative pairs",
            m0["s4_l1_zero_information_pairs"], [[0, 5]])

qd_curve = m0["qd0_partial_record_curve_bits"]
check_exact("QD-0 curve carried in the CR-0 record matches QD-0",
            qd_curve, qd0["measured"]["c3_mi_curve_bits"])
for i, typed in enumerate([0.8118, 0.9571, 0.9998, 1.0426, 1.1878,
                           1.9996]):
    check(f"QD-0 curve point {i}", qd_curve[i], typed, 5e-5)
# The paper says the environment curve takes a different value at
# every fragment size while the engineered curve takes two values
# across all 31 nonempty subsets.
assert len(set(qd_curve)) == len(qd_curve), "QD-0 curve repeats a value"
assert len(set(m0["s3_shamir_mi_curve_bits"])) == 2, \
    "the engineered curve does not take exactly two values"
CHECKS += 2
check_declared("CR-0 substrate",
               "Shamir secret sharing over the prime field GF(31) with")
check_declared("CR-0 threshold and share count",
               "threshold 3 and 5 shares")

write("cr0_step.dat", "n mi",
      [(n + 1, v) for n, v in enumerate(m0["s3_shamir_mi_curve_bits"])])
write("cr0_qd0.dat", "n mi",
      [(n + 1, v) for n, v in enumerate(qd_curve)])
write("cr0_l2.dat", "n mi",
      [(1, m0["s4_l2_single_share_mi_bits"][0]),
       (2, m0["s4_l2_pair_mi_bits"][0])])

# ---------------------------------------------------------------
# CR-1, the certificate and the channel informations.
# ---------------------------------------------------------------
cr1 = load("cr1-leakage-ordering.json")
m1 = cr1["measured"]
check_exact("CR-1 verdict", cr1["verdict"]["value"], "PASS")
for key, val in cr1["items"].items():
    check_exact(f"CR-1 item {key}", val, True)

mi = m1["mutual_information_bits"]
check("CR-1 identity information", mi["ident"], 4.0, 0.0)
check("CR-1 Hamming-weight information", mi["hw"], 2.0306, 5e-5)
check("CR-1 low-bit information", mi["lsb"], 1.0, 0.0)
check("CR-1 noisy information", mi["noisy_hw"], 0.8867, 5e-5)
check("CR-1 constant information", mi["const"], 0.0, 0.0)
# The paper says the Hamming-weight channel carries more than twice
# the low-bit channel's information and is still not above it.
assert mi["hw"] > 2.0 * mi["lsb"], "hw does not exceed twice lsb"
CHECKS += 1

for name, d in m1["k1_detail"].items():
    check(f"CR-1 conditional information given identity, {name}",
          d["cmi_given_ident"], 0.0, 0.0)
    check(f"CR-1 residual against identity, {name}", d["residual"],
          0.0, 0.0)
for name, r in m1["k2_residuals"].items():
    check(f"CR-1 residual to constant, {name}", r, 0.0, 0.0)

k3 = m1["k3"]
check("CR-1 noise garbling residual", k3["residual_hw_to_noisy"],
      2.2e-16, 5e-18)
check("CR-1 noise conditional information",
      k3["cmi_noisy_given_hw"], 4.8e-17, 5e-19)
check("CR-1 reverse conditional information",
      k3["cmi_hw_given_noisy"], 1.1439, 5e-5)
check("CR-1 information difference", k3["mi_gap_bits"], 1.1439, 5e-5)
assert k3["cmi_hw_given_noisy"] == k3["mi_gap_bits"], \
    "the reverse certificate and the information difference differ"
CHECKS += 1

k4 = m1["k4"]
check("CR-1 Hamming weight given low bit", k4["cmi_hw_given_lsb"],
      1.8113, 5e-5)
check("CR-1 low bit given Hamming weight", k4["cmi_lsb_given_hw"],
      0.7806, 5e-5)
check("CR-1 worst task gain", m1["k5_worst_task_gain"], 5.6e-17,
      5e-19)
check_exact("CR-1 battery size", m1["battery_size"], 201)
check_exact("CR-1 key count", cr1["declared"]["n_keys"], 16)
check("CR-1 declared noise", cr1["declared"]["noise"], 0.2, 0.0)

write("cr1_channels.dat", "idx mi",
      [(1, mi["ident"]), (2, mi["hw"]), (3, mi["lsb"]),
       (4, mi["noisy_hw"]), (5, mi["const"])])
write("cr1_certificates.dat", "idx cmi",
      [(1, k3["cmi_noisy_given_hw"]), (2, k3["cmi_hw_given_noisy"]),
       (3, k4["cmi_hw_given_lsb"]), (4, k4["cmi_lsb_given_hw"])])

# ---------------------------------------------------------------
# CR-2, the ensemble and the exhibit.
# ---------------------------------------------------------------
cr2 = load("cr2-countermeasure-flip.json")
m2 = cr2["measured"]
check_exact("CR-2 verdict", cr2["verdict"]["value"], "PASS")
for key, val in cr2["items"].items():
    check_exact(f"CR-2 item {key}", val, True)

check_declared("CR-2 channel A",
               "Channel A has rows (0.55, 0.25, 0.15, 0.05) and\n"
               "(0.45, 0.25, 0.15, 0.15)")
check_declared("CR-2 channel B",
               "Channel B has rows (0.49, 0.49, 0.01, 0.01) and (0.49, "
               "0.49,\n0.005, 0.015)")
check_declared("CR-2 garbling control size",
               "over five hundred declared garbled pairs")
check_declared("CR-2 commitment costs",
               "commitment are 2, 5, 10, 20, and 50")

ex = m2["exhibit"]
check("CR-2 smallest divergence margin", ex["min_divergence_margin"],
      0.0149, 5e-5)
check("CR-2 task margin for B", ex["best_task_margin_for_B"],
      0.00212, 5e-6)
check("CR-2 conic lower bound", ex["conic_lower_bound"], 0.00175,
      5e-9)
check("CR-2 total-variation difference", ex["tv_gap"], 0.095, 5e-5)
assert min(ex["divergence_margins"].values()) \
    == ex["min_divergence_margin"], "exhibit margin bookkeeping"
check_exact("CR-2 divergence battery size",
            len(ex["divergence_margins"]), 7)
CHECKS += 1

f2 = m2["f2"]
check("CR-2 worst task gain under garbling", f2["worst_task_gain"],
      3.3e-16, 5e-18)
check("CR-2 smallest divergence drop under garbling",
      f2["worst_divergence_drop"], 0.00262, 5e-6)

c = m2["f3_counts"]
check_exact("CR-2 ensemble size", cr2["declared"]["ensemble"], 2000)
assert c["comparable"] + c["incomparable"] + c["ambiguous"] \
    == cr2["declared"]["ensemble"], "CR-2 classes do not partition"
CHECKS += 1
check_exact("CR-2 comparable", c["comparable"], 867)
check_exact("CR-2 incomparable", c["incomparable"], 856)
check_exact("CR-2 ambiguous", c["ambiguous"], 277)
check_exact("CR-2 unanimous among incomparable",
            c["unanimous_incomparable"], 268)
check_exact("CR-2 task reversals among incomparable",
            c["wedge_incomparable"], 268)
check_exact("CR-2 task reversals among comparable",
            c["wedge_comparable"], 0)
check_exact("CR-2 unanimous count equals reversal count",
            c["unanimous_incomparable"], c["wedge_incomparable"])

check_exact("CR-2 task reversals among ambiguous",
            c["wedge_ambiguous"], 210)

f4 = m2["f4_prevalence"]
check("CR-2 largest reversal margin", f4["wedge_margin_max"], 0.0796,
      5e-5)
check("CR-2 median reversal margin", f4["wedge_margin_median"],
      0.0183, 5e-5)
check_exact("CR-2 task battery size", cr2["declared"]["battery_size"],
            205)
check_exact("CR-2 comparison with the GD-1 figure",
            f4["gd1_comparison"],
            "GD-1 measured 281 of 281 in decision form")
gd1 = load("gd1-flip-blackwell.json")
check_exact("GD-1 unanimous incomparable pairs",
            gd1["G3"]["counts"]["unanimous_incomparable"], 281)
check_exact("GD-1 task reversals among them",
            gd1["G3"]["counts"]["wedge_incomparable"], 281)

write("cr2_counts.dat", "idx count",
      [(1, c["comparable"]), (2, c["incomparable"]),
       (3, c["ambiguous"]), (4, c["unanimous_incomparable"]),
       (5, c["wedge_incomparable"])])

# ---------------------------------------------------------------
# CR-3 and CR-3b, the two entropy accountings.
# ---------------------------------------------------------------
cr3 = load("cr3-task-entropy.json")
cr3b = load("cr3b-task-entropy.json")
m3, m3b = cr3["measured"], cr3b["measured"]

check_exact("CR-3 verdict", cr3["verdict"]["value"], "FAIL")
check_exact("CR-3 failing item", cr3["items"]["E2_ordering_and_limit"],
            False)
for key in ("E1_closed_forms", "E3_single_guess_identity",
            "E4_huffman_bound"):
    check_exact(f"CR-3 item {key}", cr3["items"][key], True)
check_exact("CR-3b verdict", cr3b["verdict"]["value"], "PASS")
for key, val in cr3b["items"].items():
    check_exact(f"CR-3b item {key}", val, True)

check("CR-3 closed-form agreement",
      m3["e1_max_shannon_closed_form_deviation"], 8.9e-16, 5e-18)
check("CR-3 min-entropy route agreement",
      m3["e1_max_min_entropy_route_deviation"], 8.9e-16, 5e-18)
check_exact("CR-3 exhaustive scan finds the spike",
            m3["e1_scan_max_matches_closed_form"], True)
check("CR-3 single-guess identity",
      m3["e3_max_guess_identity_deviation"], 1.4e-17, 5e-19)
check_exact("CR-3 bit-exact sources", m3["e3_bit_exact_sources"], 8)
check_exact("CR-3 source count", m3["e3_source_count"], 10)
check_exact("CR-3 Kraft equality", m3["e4_kraft_equalities_hold"],
            True)
check("CR-3 smallest Huffman lower margin",
      m3["e4_min_lower_margin_bits"], 0.0, 0.0)
check("CR-3 smallest Huffman upper margin",
      m3["e4_min_upper_margin_bits"], 0.0807, 5e-5)
check("CR-3 worst ordering value",
      m3["e2_worst_min_minus_shannon_bits"], 0.0, 0.0)
check_exact("CR-3 equality only at the uniform member",
            m3["e2_equality_only_at_uniform"], True)
check_exact("CR-3 monotonicity clause",
            m3["e2_gap_strictly_increasing"], False)
check_exact("CR-3 increment signs",
            m3["e2_gap_strictly_increasing_pairwise"],
            [True, True, True, True, False, False])

gap = m3["e2_gap_ladder_bits"]
check_exact("CR-3 and CR-3b report the same difference ladder",
            gap, m3b["f2_gap_ladder_bits"])
for i, typed in enumerate([0.0, 0.398, 1.337, 2.275, 2.635, 2.113,
                           0.599]):
    check(f"difference ladder point {i}", gap[i], typed, 5e-4)

ratio_u = m3b["f2_u_ratio_ladder"]
ratio_s = m3b["f2_s_ratio_ladder"]
for i, typed in enumerate([1.0, 0.9203, 0.7304, 0.5199, 0.3769,
                           0.2390, 0.1464]):
    check(f"ratio ladder point {i}", ratio_u[i], typed, 5e-5)
for i, typed in enumerate([0.2876, 0.1576, 0.1112]):
    check(f"ratio q ladder point {i}", ratio_s[i], typed, 5e-5)
assert all(ratio_u[i + 1] < ratio_u[i]
           for i in range(len(ratio_u) - 1)), "u ratio not decreasing"
assert all(ratio_s[i + 1] < ratio_s[i]
           for i in range(len(ratio_s) - 1)), "q ratio not decreasing"
CHECKS += 2

check_exact("CR-3b sign changes", m3b["f2_sign_change_count"], 1)
check_exact("CR-3b bracket", m3b["f2_sign_change_bracket"],
            ["0.30", "0.60"])
check_exact("CR-3b bracket as declared", m3b["f2_bracket_as_declared"],
            True)
check("CR-3b derivative route agreement", m3b["f3_max_deviation"],
      1.6e-8, 5e-10)
for i, typed in enumerate([46.166, 34.559, 16.301, 5.181, 0.4147,
                           -3.444, -7.165]):
    check(f"CR-3b derivative ladder point {i}",
          m3b["f2_gap_derivative_ladder"][i], typed, 5e-4)
check_exact("CR-3b alphabet size", cr3b["declared"]["alphabet_size"],
            32)
check_exact("CR-3b increments positive before the bracket",
            m3b["f2_increments_positive_before_bracket"], True)
check_exact("CR-3b increments negative after the bracket",
            m3b["f2_increments_negative_after_bracket"], True)
check_declared("CR-3 closed-form derivative",
               "log2((1 - a)/(31a)) + 1/(a ln 2)")
check_declared("CR-3 alphabet and families",
               "Two declared families of sources on an alphabet of "
               "n = 32")

fmax = m3b["f4_interior_maximum"]
check("CR-3b maximizing spike weight", fmax["maximizing_spike_weight"],
      0.35338, 5e-6)
check("CR-3b maximizing eps", fmax["maximizing_eps"], 0.32213, 5e-6)
check("CR-3b maximum difference", fmax["maximum_gap_bits"], 2.6398,
      5e-5)
check("CR-3b derivative at the maximum",
      fmax["derivative_at_maximum"], 4.5e-12, 5e-14)
check_exact("CR-3b bisection steps", fmax["bisection_steps"], 39)
check("CR-3b final bracket width", fmax["final_bracket_width"],
      5.5e-13, 5e-15)
check("CR-3b largest ladder difference",
      fmax["largest_ladder_gap_bits"], 2.635309539404596, 0.0)
check("CR-3b ladder shortfall",
      fmax["maximum_gap_bits"] - fmax["largest_ladder_gap_bits"],
      0.0045, 5e-5)

e5 = m3b["e5_key_material_case"]
check_exact("key-material case is the same in both records", e5,
            m3["e5_key_material_case"])
check("key-material averaging accounting", e5["shannon_bits"],
      3.477098155193437, 0.0)
check("key-material averaging accounting, rounded",
      e5["shannon_bits"], 3.477, 5e-4)
check("key-material single-guess accounting", e5["min_entropy_bits"],
      1.0, 0.0)
check("key-material ratio", e5["min_over_shannon_ratio"], 0.2876,
      5e-5)
check("key-material factor", e5["shannon_over_min_factor"], 3.477,
      5e-4)
check("key-material single-guess success", e5["single_guess_success"],
      0.5, 0.0)
check("key-material Huffman mean length", e5["huffman_mean_length"],
      3.4839, 5e-5)

srcs = {s["name"]: s for s in m3b["measured_sources"]} \
    if "measured_sources" in m3b else \
    {s["name"]: s for s in m3b["sources"]}
u_names = ["U(eps=0)", "U(eps=0.01)", "U(eps=0.05)", "U(eps=0.15)",
           "U(eps=0.30)", "U(eps=0.60)", "U(eps=0.90)"]
eps_ladder = [float(p) for p in m3b["f2_eps_ladder"]]
check_exact("CR-3b eps ladder", eps_ladder,
            [0.0, 0.01, 0.05, 0.15, 0.30, 0.60, 0.90])
for name, eps, g in zip(u_names, eps_ladder, gap):
    s = srcs[name]
    check_exact(f"{name} parameter", float(s["param"]), eps)
    check(f"{name} difference", s["gap_shannon_minus_min_bits"], g,
          0.0)
    check(f"{name} accounting difference route",
          s["shannon_bits"] - s["min_entropy_bits"], g, 1e-15)

check("Shannon entropy at the uniform member",
      srcs["U(eps=0)"]["shannon_bits"], 5.0, 0.0)
check("Huffman mean length at the uniform member",
      srcs["U(eps=0)"]["huffman_mean_length"], 5.0, 0.0)
check("Huffman mean length at q=0.99",
      srcs["S(q=0.99)"]["huffman_mean_length"], 1.0497, 5e-5)
check("Shannon entropy at q=0.99 plus one",
      srcs["S(q=0.99)"]["shannon_bits"] + 1.0, 1.1303, 5e-5)

write("cr3_ladder.dat", "eps shannon minent sepbits",
      [(eps, srcs[n]["shannon_bits"], srcs[n]["min_entropy_bits"],
        srcs[n]["gap_shannon_minus_min_bits"])
       for n, eps in zip(u_names, eps_ladder)])
write("cr3_ratio.dat", "eps ratio",
      [(eps, srcs[n]["min_over_shannon_ratio"])
       for n, eps in zip(u_names, eps_ladder)])
write("cr3_max.dat", "eps sepbits",
      [(fmax["maximizing_eps"], fmax["maximum_gap_bits"])])
write("cr3_deriv.dat", "eps deriv",
      list(zip(eps_ladder, m3b["f2_gap_derivative_ladder"])))

# ---------------------------------------------------------------
# CR-4, CR-4b, CR-4c, the backdoor audit ceiling.
# ---------------------------------------------------------------
cr4 = load("cr4-backdoor-ceiling.json")
cr4b = load("cr4b-backdoor-ceiling.json")
cr4c = load("cr4c-backdoor-ceiling.json")
m4, m4b, m4c = cr4["measured"], cr4b["measured"], cr4c["measured"]

check_exact("CR-4 verdict", cr4["verdict"]["value"], "FAIL")
check_exact("CR-4 trapdoor bar", cr4["items"]["B1_trapdoor_predicts"],
            False)
check_exact("CR-4 uniformity bar",
            cr4["items"]["B2_public_entropies_near_uniform"], False)
check_exact("CR-4 scalar always exists",
            cr4["items"]["B3_scalar_always_exists"], True)
check_exact("CR-4 instrument sanity",
            cr4["items"]["B4_public_information_is_small"], True)
check_exact("CR-4 separation finding",
            cr4["findings"][
                "B5_audit_cannot_separate_backdoored_from_clean"],
            False)
check_exact("CR-4 field", m4["field"], 101)
check_exact("CR-4 group order", m4["group_order"], 96)
check_exact("CR-4 output values", cr4["declared"]["out_mask"] + 1, 8)
check_exact("CR-4 declared seeds",
            cr4["declared"]["n_seeds_for_trapdoor"], 95)
check("CR-4 backdoored public entropy",
      m4["public_entropy_bits_backdoored"], 2.7890, 5e-5)
check("CR-4 clean public entropy", m4["public_entropy_bits_clean"],
      2.8002, 5e-5)
check("CR-4 uniform entropy", m4["uniform_entropy_bits"], 3.0, 0.0)
check("CR-4 trapdoor prediction rate", m4["trapdoor_prediction_rate"],
      0.263, 5e-4)
check_exact("CR-4 clean scalar recovered by enumeration",
            m4["clean_point_scalar_computed_by_enumeration"], 41)
# The paper says the two word-count multisets are not identical, which
# is why the drafted separation question was the wrong question.
check_exact("CR-4 shapes not identical", m4["shapes_identical"], False)
assert m4["word_count_shape_backdoored"] \
    != m4["word_count_shape_clean"], "CR-4 word shapes coincide"
CHECKS += 1
check_declared("CR-4 truncation",
               "declared truncation keeps three bits")
check_declared("CR-4 trapdoor bar",
               "predicts the next output word from one observed word "
               "in at")
check_declared("CR-4 uniformity window", "within 0.15 bits of")

check_exact("CR-4b verdict", cr4b["verdict"]["value"], "FAIL")
check_exact("CR-4b failing item",
            cr4b["items"]["B3_trapdoor_confers_no_information"], False)
for key in ("B1_audit_detects_a_leak", "B2_near_uniform",
            "B4_scalar_recovered_by_enumeration"):
    check_exact(f"CR-4b item {key}", cr4b["items"][key], True)
check_exact("CR-4b field", m4b["field"], 1009)
check_exact("CR-4b group order", m4b["group_order"], 1013)
check("CR-4b backdoored public entropy",
      m4b["public_entropy_backdoored"], 2.9878, 5e-5)
check("CR-4b clean public entropy", m4b["public_entropy_clean"],
      2.9943, 5e-5)
check("CR-4b uniform entropy", m4b["uniform_entropy"], 3.0, 0.0)
check("CR-4b declared leak information",
      m4b["mutual_information_leaky_bits"], 1.0, 0.0)
check("CR-4b unmodified generator information",
      m4b["mutual_information_clean_bits"], 0.0, 0.0)
check_exact("CR-4b clean scalar recovered",
            m4b["clean_scalar_recovered"], 2)
check("CR-4b public route", m4b["conditional_entropy_public"], 2.8811,
      5e-5)
check("CR-4b trapdoor route",
      m4b["conditional_entropy_trapdoor_route"], 2.9125, 5e-5)
check("CR-4b route difference",
      m4b["conditional_entropy_difference"], 0.0314, 5e-5)
check_declared("CR-4b route bar", "route agree within 1e-9")
check_declared("CR-4b field", "the field of 1009 elements")
check_declared("CR-4b prime order", "with prime group order")
check_declared("CR-4b clean rule",
               "the first scalar whose point abscissa is")

check_exact("CR-4c verdict", cr4c["verdict"]["value"], "PASS")
for key, val in cr4c["items"].items():
    check_exact(f"CR-4c item {key}", val, True)
for key, val in cr4c["findings"].items():
    check_exact(f"CR-4c finding {key}", val, True)
check("CR-4c route difference", m4c["conditional_entropy_difference"],
      0.0, 0.0)
check("CR-4c trapdoor entropy", m4c["trapdoor_entropy_bits"], 0.0, 0.0)
check("CR-4c information bound",
      m4c["trapdoor_information_bound_bits"], 0.0, 0.0)
check("CR-4c declared leak information",
      m4c["mutual_information_leaky_bits"], 1.0, 0.0)
check("CR-4c unmodified generator information",
      m4c["mutual_information_clean_bits"], 0.0, 0.0)
check("CR-4c backdoored public entropy",
      m4c["public_entropy_backdoored"], 2.9878, 5e-5)
check("CR-4c clean public entropy", m4c["public_entropy_clean"],
      2.9943, 5e-5)
check_exact("CR-4c and CR-4b share the substrate",
            [m4c["field"], m4c["group_order"], m4c["curve"]],
            [m4b["field"], m4b["group_order"], m4b["curve"]])
check_exact("CR-4c public route unchanged",
            m4c["conditional_entropy_public"],
            m4b["conditional_entropy_public"])
check_exact("CR-4c trapdoor route equals the public route",
            m4c["conditional_entropy_trapdoor_route"],
            m4c["conditional_entropy_public"])

# ---------------------------------------------------------------
# CR-5, designer freedom against class rarity.
# ---------------------------------------------------------------
cr5 = load("cr5-rigidity.json")
m5 = cr5["measured"]
check_exact("CR-5 verdict", cr5["verdict"]["value"], "PASS")
for key, val in cr5["items"].items():
    check_exact(f"CR-5 item {key}", val, True)
check_exact("CR-5 finding P4", cr5["findings"][
    "P4_artifact_carries_no_search_count"], True)
check_exact("CR-5 finding P5", cr5["findings"][
    "P5_rigid_procedure_below_threshold"], True)
check_exact("CR-5 finding P6", cr5["findings"][
    "P6_rigid_procedure_landed_weak_by_chance"], False)
check_exact("CR-5 field", m5["field"], 101)
check_exact("CR-5 smoothness bound", m5["smoothness_bound"], 5)
check_exact("CR-5 non-singular curves", m5["nonsingular_curves"], 10100)
check_exact("CR-5 weak curves", m5["weak_curves"], 2275)
check("CR-5 weak-class density", m5["weak_class_density"], 0.2252,
      5e-5)
check_exact("CR-5 rigid reachable", m5["rigid_reachable"], 1)
check("CR-5 rigid freedom times density",
      m5["rigid_freedom_times_density"], 0.2252, 5e-5)
check_exact("CR-5 rigid landed weak", m5["rigid_landed_weak"], False)
check_exact("CR-5 flexible seed range", m5["flexible_seed_range"], 4096)
check_exact("CR-5 flexible reachable distinct",
            m5["flexible_reachable_distinct"], 99)
check("CR-5 flexible freedom times density",
      m5["flexible_freedom_times_density"], 22.3, 5e-3)
check_exact("CR-5 first weak seed", m5["first_weak_seed"], 10)
check_exact("CR-5 weak-producing seeds", m5[
    "weak_producing_seeds_in_range"], 526)
check("CR-5 expected rolls", m5["expected_rolls_to_manipulate"],
      7.787, 5e-4)
# The paper says the declared seed range overstates the number of
# curves the flexible procedure can reach.
assert m5["flexible_seed_range"] > 40 * m5[
    "flexible_reachable_distinct"], \
    "the declared range overstates the reachable set by under forty"
assert m5["rigid_freedom_times_density"] < 1.0 <= \
    m5["flexible_freedom_times_density"], "CR-5 threshold bookkeeping"
CHECKS += 2
check_declared("CR-5 weak class",
               "a group order smooth to the bound five")
check_declared("CR-5 rigid procedure",
               "The rigid procedure may use exactly")
check_declared("CR-5 flexible procedure",
               "The flexible procedure may use any seed in a")
check_declared("CR-5 seed map",
               "the first coefficient is the seed squared plus "
               "seventeen and the")
check_declared("CR-5 preregistration connection",
               "the four vacuity failures this program has recorded")

# ---------------------------------------------------------------
# CR-6, information against disturbance.
# ---------------------------------------------------------------
cr6 = load("cr6-information-disturbance.json")
m6 = cr6["measured"]
check_exact("CR-6 verdict", cr6["verdict"]["value"], "PASS")
for key, val in cr6["items"].items():
    check_exact(f"CR-6 item {key}", val, True)
check_exact("CR-6 finding C6", cr6["findings"][
    "C6_tradeoff_is_exactly_two_bits_per_unit_error"], True)
check("CR-6 classical control information",
      m6["classical_control"]["eve_information_bits"], 1.0, 0.0)
check("CR-6 classical control induced error",
      m6["classical_control"]["qber"], 0.0, 0.0)
check("CR-6 Holevo quantity", m6["holevo_bound_bits"], 1.0, 0.0)
check("CR-6 largest measured information",
      m6["max_eve_information_bits"], 0.5, 0.0)
check("CR-6 worst closed-form deviation",
      m6["worst_closed_form_deviation"], 1.1e-16, 5e-18)
lad6 = m6["ladder"]
check_exact("CR-6 ladder length", len(lad6), 6)
check_exact("CR-6 declared ladder",
            [r["lambda"] for r in lad6],
            cr6["declared"]["lambdas"])
check_exact("CR-6 declared ladder as typed",
            [r["lambda"] for r in lad6],
            [0.0, 0.1, 0.25, 0.5, 0.75, 1.0])
check("CR-6 information at the first positive rung",
      lad6[1]["eve_information_bits"], 0.05, 0.0)
check("CR-6 induced error at the first positive rung", lad6[1]["qber"],
      0.025, 5e-16)
check("CR-6 information at the top rung",
      lad6[-1]["eve_information_bits"], 0.5, 0.0)
check("CR-6 induced error at the top rung", lad6[-1]["qber"], 0.25,
      5e-16)
check("CR-6 information at zero", lad6[0]["eve_information_bits"], 0.0,
      0.0)
check("CR-6 induced error at zero", lad6[0]["qber"], 0.0, 0.0)
for i, r in enumerate(m6["information_per_unit_qber"]):
    check(f"CR-6 exchange rate rung {i}", r, 2.0, 5e-15)
check("CR-6 worst exchange-rate deviation",
      max(abs(r - 2.0) for r in m6["information_per_unit_qber"]),
      1.3e-15, 1e-16)
assert all(r["eve_information_bits"] > 0.0 and r["qber"] > 0.0
           for r in lad6[1:]), "a positive rung reads zero"
assert all(r["eve_information_bits"] <= m6["holevo_bound_bits"]
           for r in lad6), "a rung passes the Holevo quantity"
CHECKS += 2
check_declared("CR-6 declared ladder",
               "declared ladder 0, 0.1, 0.25, 0.5, 0.75, 1")
check_declared("CR-6 consumer",
               "eavesdropping consumer intercepts with probability "
               "lambda")

write("cr6_ladder.dat", "qber info",
      [(r["qber"], r["eve_information_bits"]) for r in lad6])
write("cr6_classical.dat", "qber info",
      [(m6["classical_control"]["qber"],
        m6["classical_control"]["eve_information_bits"])])
write("cr6_holevo.dat", "qber info",
      [(0.0, m6["holevo_bound_bits"]),
       (0.26, m6["holevo_bound_bits"])])

# ---------------------------------------------------------------
# CR-7, one record for both consumers and one correlation for one.
# ---------------------------------------------------------------
cr7 = load("cr7-monogamy.json")
m7 = cr7["measured"]
check_exact("CR-7 verdict", cr7["verdict"]["value"], "PASS")
for key, val in cr7["items"].items():
    check_exact(f"CR-7 item {key}", val, True)
check_exact("CR-7 finding M5", cr7["findings"][
    "M5_classical_sum_exceeds_the_quantum_identity"], True)
bc = m7["classical_broadcast"]
check("CR-7 first consumer information", bc["i_ab_bits"], 1.0, 0.0)
check("CR-7 second consumer information", bc["i_ae_bits"], 1.0, 0.0)
check("CR-7 classical sum", bc["sum_bits"], 2.0, 0.0)
check("CR-7 worst identity deviation", m7["worst_identity_deviation"],
      1.9e-10, 5e-12)
check("CR-7 worst CKW deviation", m7["worst_ckw_deviation"], 1.9e-10,
      5e-12)
fam = m7["quantum_family"]
check_exact("CR-7 grid length", len(fam), 7)
check_exact("CR-7 declared grid", [r["phi"] for r in fam],
            cr7["declared"]["phi_grid"])
check("CR-7 first consumer at the first extreme", fam[0]["c_ab"], 1.0,
      0.0)
check("CR-7 second consumer at the first extreme", fam[0]["c_ae"], 0.0,
      0.0)
check("CR-7 second consumer at the second extreme", fam[-1]["c_ae"],
      1.0, 0.0)
check("CR-7 first consumer at the second extreme", fam[-1]["c_ab"],
      6.1e-17, 5e-19)
check("CR-7 equal split", fam[3]["c_ab"], 0.7071067811865477, 0.0)
check("CR-7 equal split, second consumer", fam[3]["c_ae"],
      0.7071067811865476, 0.0)
check("CR-7 equal split as typed", fam[3]["c_ab"], 0.7071, 5e-5)
check("CR-7 equal split as typed, second consumer", fam[3]["c_ae"],
      0.7071, 5e-5)
for i, r in enumerate(fam):
    check(f"CR-7 identity at grid point {i}", r["sum_of_squares"], 1.0,
          2e-10)
    check(f"CR-7 CKW at grid point {i}",
          r["tangle_a_vs_rest"] - r["sum_of_squares"], 0.0, 2e-10)
assert bc["sum_bits"] > fam[0]["sum_of_squares"], \
    "the classical sum does not exceed the quantum identity"
CHECKS += 1
check_declared("CR-7 declared grid",
               "an angle on a declared seven-point grid")
check_declared("CR-7 declared family",
               "a declared three-qubit family carrying one")

write("cr7_grid.dat", "cab cae",
      [(r["c_ab"], r["c_ae"]) for r in fam])
write("cr7_classical.dat", "cab cae",
      [(bc["i_ab_bits"], bc["i_ae_bits"])])

# ---------------------------------------------------------------
# The cross-track comparisons quoted in the closing sections.
# ---------------------------------------------------------------
qd1b = load("qd1b-emergence.json")
qd3 = load("qd3-agreement.json")
check_exact("QD-1b verdict", qd1b["verdict"]["value"], "PASS")
check_exact("QD-3 verdict", qd3["verdict"]["value"], "PASS")
ladder_qd = qd1b["measured"]["theta_ladder"]
for key, typed in [("0.196350", 0.0391), ("0.392699", 0.1151),
                   ("0.785398", 0.2903), ("1.570796", 0.6122),
                   ("3.141593", 1.0)]:
    check(f"QD-1b fragment information at {key}",
          ladder_qd[key]["fragment1_mi_bits"], typed, 5e-5)
for key in ("0.196350", "0.392699", "0.785398", "1.570796"):
    check_exact(f"QD-1b redundancy at {key}",
                ladder_qd[key]["redundancy"], 0)
check_exact("QD-1b redundancy at the fully decohering rung",
            ladder_qd["3.141593"]["redundancy"], 6)
check_exact("QD-1b basis-free redundancy",
            qd1b["measured"]["basis_free_global_haar"]["redundancy"], 0)
check("QD-1b basis-free system entropy",
      qd1b["measured"]["basis_free_global_haar"]["system_entropy_bits"],
      0.9945, 5e-5)
for i, typed in enumerate([0.5096, 0.5373, 0.6357, 0.8750, 1.0]):
    check(f"QD-3 agreement point {i}",
          qd3["measured"]["agreement_curve"][i], typed, 5e-5)

hd3 = load("hd3-dissipation-gate.json")
check_exact("HD-3 verdict", hd3["verdict"]["value"], "PASS")
check_exact("HD-3 exact invertibility",
            hd3["items"]["D1_exact_invertibility"], True)
check_exact("HD-3 reversed run matches the forward run",
            hd3["measured"]["inverse_matches_forward_reversed_exactly"],
            True)
# The paper says the coarse mode decayed to a small fraction of its
# initial amplitude before the exact reversal returned the state.
assert hd3["measured"]["forward_decay_ratio"] < 0.1, \
    "the HD-3 coarse mode did not decay to a small fraction"
CHECKS += 1

print(f"all figure data written, {CHECKS} paper values bound "
      f"to committed records")
