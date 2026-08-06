#!/usr/bin/env python3
"""Generate pgfplots data tables for the second-generation paper.

Every number is read from a committed evidence record in results/.
Pure standard library, no numpy, no free parameters. Output tables
land in paper/figdata/. Consistency assertions bind the emitted
tables, and the headline numbers quoted in the paper, to the
committed records they come from.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "figdata"
OUT.mkdir(exist_ok=True)


def load(name: str) -> dict:
    return json.loads((ROOT / "results" / name).read_text(
        encoding="utf-8"))


def write(name: str, header: str, rows) -> None:
    lines = [header] + [" ".join(f"{v:.10g}" for v in row)
                        for row in rows]
    (OUT / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{name}: {len(lines) - 1} rows")


def close(a: float, b: float, tol: float = 5e-4) -> bool:
    """Relative closeness for binding quoted headline numbers."""
    return abs(a - b) <= tol * max(abs(a), abs(b), 1e-300)


# ----------------------------------------------------------------
# Verdicts as recorded, asserted so the ledger table cannot drift.
EXPECTED = {
    "rg0-instrument.json": "PASS",
    "rg1-channel-family.json": "FAIL",
    "rg1b-channel-family.json": "PASS",
    "rg2-flip.json": "FAIL",
    "rg2b-flip.json": "PASS",
    "rg3-universality.json": "FAIL",
    "rg3b-universality.json": "PASS",
    "rg4-relevance.json": "PASS",
    "qd0-instrument.json": "PASS",
    "qd1-emergence.json": "FAIL",
    "qd1b-emergence.json": "PASS",
    "qd2-budget-knob.json": "PASS",
    "qd3-agreement.json": "PASS",
    "hd0-instrument.json": "PASS",
    "hd1-transport.json": "FAIL",
    "hd1b-transport.json": "PASS",
    "hd2-fhp-viscosity.json": "PASS",
    "hd3-dissipation-gate.json": "PASS",
    "ft0-instrument.json": "PASS",
    "ft1-lawful-demon.json": "PASS",
    "ft2-restoration.json": "PASS",
    "ft3-feedback.json": "PASS",
    "gg0-instrument.json": "PASS",
    "gg1-observer-family.json": "PASS",
    "gg2-gauss-replay.json": "FAIL",
    "gg2b-gauss-replay.json": "PASS",
    "gg3-minimal-coupling.json": "PASS",
}
records = {}
for name, want in EXPECTED.items():
    rec = load(name)
    got = rec["verdict"]["value"]
    assert got == want, f"{name}: verdict {got}, ledger says {want}"
    records[name] = rec
print(f"verdicts checked: {len(records)} records")

# ----------------------------------------------------------------
# Figure Q1a: QD-3 agreement curve along the angle ladder, with the
# per-consumer Helstrom closed-form marginals alongside.
qd3 = records["qd3-agreement.json"]["measured"]
curve = qd3["agreement_curve"]
table = qd3["table"]
thetas = sorted(table.keys(), key=float)
assert [table[t]["p_agree"] for t in thetas] == curve, \
    "QD-3 table and curve disagree in record"
assert all(curve[i] < curve[i + 1] for i in range(len(curve) - 1)), \
    "QD-3 agreement curve not strictly increasing in record"
assert curve[-1] >= 1 - 1e-10 and curve[0] <= 0.6, \
    "QD-3 endpoint bars not met in record"
assert close(curve[0], 0.510, 2e-3) and close(curve[2], 0.636, 2e-3), \
    "QD-3 quoted endpoints off record"
write("gen2_qd3_agreement.dat", "theta pagree helstrom",
      [(float(t), table[t]["p_agree"], table[t]["helstrom_pred"])
       for t in thetas])

# Figure Q1b: QD-2 portfolio, best against worst two-qubit fragment
# of the unequal-angle consumer.
qd2 = records["qd2-budget-knob.json"]["measured"]
best = qd2["size2_best_bits"]
worst = qd2["size2_worst_bits"]
assert close(best / worst, qd2["size2_ratio"], 1e-9), \
    "QD-2 portfolio ratio inconsistent in record"
assert close(qd2["size2_ratio"], 36.0, 2e-3), \
    "QD-2 quoted ratio 36.0 off record"
assert all(v["fstar"] == 3 for v in qd2["budget_curve"].values()), \
    "QD-2 flat budget curve not flat in record"
write("gen2_qd2_portfolio.dat", "idx bits",
      [(1, best), (2, worst)])

# ----------------------------------------------------------------
# Figure F1: FT defect ladder and restoration. Naive defects from
# FT-1, restored defects and the wrong-model defect from FT-2.
ft1 = records["ft1-lawful-demon.json"]["measured"]
ft2 = records["ft2-restoration.json"]["measured"]
assert ft1["defect_complete"] == 0.0 and ft1["defect_blind"] == 0.0, \
    "FT-1 endpoint defects not exactly zero in record"
assert ft2["naive_defect_lumped"] == ft1["defect_lumped"], \
    "FT-2 replication of FT-1 lumped defect off"
assert ft2["naive_defect_held"] == ft1["defect_held"], \
    "FT-2 replication of FT-1 held defect off"
assert close(ft1["defect_lumped"], 4.331e-4, 1e-3), \
    "quoted lumped defect off record"
assert close(ft1["defect_held"], 0.03244, 1e-3), \
    "quoted held defect off record"
assert ft2["restored_defect_lumped"] <= 1e-12 \
    and ft2["restored_defect_held"] <= 1e-12, \
    "FT-2 restored defects above the declared bar in record"
assert close(ft2["wrong_model_restored_defect"], 3.265e-3, 1e-3), \
    "quoted wrong-model defect off record"
assert ft2["wrong_model_restored_defect"] > ft1["defect_lumped"], \
    "wrong-model defect not worse than naive in record"
write("gen2_ft_defects.dat", "idx naive restored",
      [(1, ft1["defect_lumped"], ft2["restored_defect_lumped"]),
       (2, ft1["defect_held"], ft2["restored_defect_held"])])
write("gen2_ft_wrongmodel.dat", "idx defect",
      [(1, ft2["wrong_model_restored_defect"])])

# ----------------------------------------------------------------
# Figure H1a: HD-3 forward shear amplitude, every ten steps.
hd3 = records["hd3-dissipation-gate.json"]["measured"]
amps = hd3["amp_forward_every10"]
assert amps[0] == hd3["amp_forward_t0"] \
    and amps[-1] == hd3["amp_forward_T"], \
    "HD-3 amplitude endpoints inconsistent in record"
assert close(amps[-1] / amps[0], hd3["forward_decay_ratio"], 1e-9), \
    "HD-3 decay ratio inconsistent in record"
assert hd3["inverse_reversed_max_dev"] == 0.0, \
    "HD-3 retrace deviation not exactly zero in record"
assert close(hd3["perturbed_return_ratio"], 0.0182, 2e-2), \
    "quoted HD-3 return ratio off record"
write("gen2_hd3_amp.dat", "t amp",
      [(10 * i, a) for i, a in enumerate(amps)])

# Figure H1b: HD-2 nine-prescription viscous rates.
hd2 = records["hd2-fhp-viscosity.json"]
gate = hd2["findings"]["H2d_prescription_gate"]
rates = gate["prescription_rates"]
keys = [f"cell{c}_cad{d}" for c in (1, 4, 8) for d in (1, 2, 4)]
assert sorted(keys) == sorted(rates.keys()), \
    "HD-2 prescription keys unexpected in record"
vals = [rates[k] for k in keys]
spread = max(vals) - min(vals)
mean = sum(vals) / len(vals)
assert close(spread, gate["spread"], 1e-9), \
    "HD-2 spread inconsistent in record"
assert close(spread / mean, gate["spread_over_mean"], 1e-9), \
    "HD-2 spread-over-mean inconsistent in record"
assert gate["spread_over_mean"] < 0.10 and gate["bar_passed"], \
    "HD-2 gate outcome inconsistent in record"
assert close(gate["spread_over_mean"], 7.09e-4, 2e-3), \
    "quoted HD-2 spread fraction off record"
nu1 = hd2["measured"]["measured_viscosity_k1"]
assert close(nu1, 0.842, 1e-3), "quoted viscosity off record"
assert close(hd2["measured"]["shear_rate_ratio_k2_over_k1"],
             4.538, 1e-3), "quoted HD-2 rate ratio off record"
write("gen2_hd2_prescriptions.dat", "idx rate",
      [(i + 1, v) for i, v in enumerate(vals)])

# ----------------------------------------------------------------
# Figure G1: GG-2b sector response, link expectation and plaquette
# shift against the deformation, log-log, slopes one and four.
gg2b = records["gg2b-gauss-replay.json"]["measured"]
per = gg2b["per_eps"]
w0 = per["0.0"]["wilson_plaquette"]
assert per["0.0"]["max_link_exp"] == 0.0, \
    "GG-2b zero point not exact in record"
eps_list = [1e-3, 1e-2, 1e-1]
rows = []
for e in eps_list:
    key = f"{e:g}"
    link = per[key]["max_link_exp"]
    shift = per[key]["wilson_plaquette"] - w0
    assert shift > 0, "GG-2b plaquette shift not positive"
    rows.append((e, link, shift))
slope_link = (math.log(rows[1][1]) - math.log(rows[0][1])) \
    / (math.log(1e-2) - math.log(1e-3))
slope_plaq = (math.log(rows[1][2]) - math.log(rows[0][2])) \
    / (math.log(1e-2) - math.log(1e-3))
assert abs(slope_link - gg2b["link_response_slope"]) < 5e-3, \
    "GG-2b link slope does not rebuild from the record"
assert abs(slope_plaq - gg2b["plaquette_response_slope"]) < 5e-2, \
    "GG-2b plaquette slope does not rebuild from the record"
assert close(gg2b["plaquette_response_slope"], 4.000003, 1e-5), \
    "quoted plaquette slope off record"
write("gen2_gg2_response.dat", "eps link plaqshift", rows)

# ----------------------------------------------------------------
# Headline bindings for numbers quoted in text and ledger that do
# not appear in a figure table.
rg0 = records["rg0-instrument.json"]["measured"]
assert close(rg0["c4_majority_nnn_residual"], 0.0260, 2e-3)
assert rg0["c4_majority_nnn_residual"] / 1e-4 > 260 - 1
assert rg0["c2_dev"] < 5e-17 and rg0["c5_dev"] < 3e-17

rg1b = records["rg1b-channel-family.json"]["measured"]
assert close(rg1b["xi_odd"], 1.5026, 1e-3)
assert close(rg1b["xi_even"], 0.5194, 1e-3)
assert close(rg1b["xi_ratio"], 2.893, 1e-3)
assert all(v == 0.0 for v in rg1b["cross_sector_leakage"].values())
assert close(rg1b["route_rel_dev"], 1.3e-14, 5e-2)
rg1 = records["rg1-channel-family.json"]["measured"]
assert close(rg1["route_rel_dev"], 0.0386, 2e-3)
assert close(rg1["amplitude_at_d8"]["pair"], 5.07e-8, 2e-3)

rg2 = records["rg2-flip.json"]["measured"]
assert rg2["flip"] == 0.0 and rg2["n_fidelity_ties"] == 840
assert close(rg2["acc_task_optimal"], 0.6000482, 1e-5)
rg2b = records["rg2b-flip.json"]["measured"]
assert close(rg2b["flip"], 1.123e-4, 1e-3)
assert close(rg2b["acc_task_optimal"], 0.95766, 1e-4)
assert close(rg2b["acc_fidelity_best"], 0.95754, 1e-4)
assert rg2b["eigen_sign_disagreements"] == 15

rg3 = records["rg3-universality.json"]["measured"]
flow = rg3["u2_residual_flow"]
assert close(flow[0], 0.157, 2e-3) and close(flow[1], 0.032, 1e-2) \
    and close(flow[2], 0.0042, 2e-2)
u4 = rg3["u4_micro_dec_maj"]
assert close(u4[0], 0.161, 2e-3) and close(u4[2], 0.0136, 2e-3)
assert u4[2] < u4[1], "RG-3 majority did not undercut decimation"
rg3b = records["rg3b-universality.json"]["measured"]
inf = rg3b["u4_in_family_start_dec_maj"]
assert inf[0] < 1e-12 and close(inf[1], 0.0117, 2e-2)
assert close(rg3b["u3_field_coarse_m"], 0.777, 1e-3)

rg4 = records["rg4-relevance.json"]["measured"]
m = rg4["multipliers"]
assert close(m["h_dec"], 1.834, 1e-3)
assert close(m["h_maj"], 2.407, 1e-3)
assert close(m["j2_dec"], 0.174, 2e-3)
assert close(m["j2_maj"], -0.0707, 2e-3)
assert m["j2_dec"] > 0 > m["j2_maj"]
assert close(rg4["linearity_dev"], 9.1e-5, 5e-3)

qd0 = records["qd0-instrument.json"]["measured"]
assert close(qd0["c4_mean_single_fragment_mi"], 0.0514, 1e-3)
assert close(qd0["c4_system_entropy_bits"], 0.999, 1e-3)
assert qd0["c4_full_env_mi_minus_2S"] == 0.0
assert close(qd0["c3_mi_curve_bits"][0], 0.812, 1e-3)

qd1 = records["qd1-emergence.json"]["measured"]
assert qd1["basis_free"]["redundancy"] == 1
assert close(qd1["basis_free"]["system_entropy_bits"], 0.6647, 1e-3)
assert close(qd1["q1_max_closed_form_dev"], 2.7e-15, 2e-2)
lad = qd1["theta_ladder"]
tkeys = sorted(lad.keys(), key=float)
assert [lad[t]["redundancy"] for t in tkeys] == [0, 0, 0, 0, 6]
qd1b = records["qd1b-emergence.json"]["measured"]
assert qd1b["basis_free_global_haar"]["redundancy"] == 0
assert close(qd1b["basis_free_global_haar"]["system_entropy_bits"],
             0.9945, 1e-3)

hd0 = records["hd0-instrument.json"]["measured"]
assert hd0["invariants"][0] == 194
assert close(hd0["entropy_rise_bits"], 0.637, 1e-3)
assert hd0["retrace_max_dev"] == 0.0

hd1 = records["hd1-transport.json"]["measured"]
assert hd1["shear"]["1"]["decay_ratio"] == 1.0
assert hd1["shear"]["2"]["decay_ratio"] == 1.0
assert abs(hd1["shear"]["1"]["rate"]) < 1e-17
assert close(hd1["sound"]["1"]["c_over_pred"], 1.008, 1e-3)
assert close(hd1["sound"]["2"]["c_over_pred"], 1.012, 1e-3)
assert close(hd1["sound_freq_ratio"], 2.008, 1e-3)

hd2m = hd2["measured"]
assert close(hd2m["shear"]["1"]["rate"], 0.008114, 1e-3)
assert close(hd2m["boltzmann_comparison_nu"], 0.742, 1e-3)
assert close(hd2m["measured_viscosity_k2"], 0.955, 1e-3)

ham = dict(hd3["hamming_divergence_r0"])
assert ham[0] == 1 and ham[30] == 3047 and ham[60] == 11007
assert close(hd3["amp_r0_perturbed_return"], 0.437, 2e-3)
assert close(hd3["amp_r0_true_initial"], 24.04, 1e-3)
assert hd3["untouched_49_return_bit_exact"] is True
# Full-decorrelation comparison from declared parameters f0 = 0.35
# on 24576 bits, arithmetic on declared record fields.
decor = 2 * 0.35 * (1 - 0.35) * 24576
assert close(decor, 11182.08, 1e-6)
assert abs(ham[300] - decor) / decor < 0.01

ft0 = records["ft0-instrument.json"]["measured"]
assert ft0["c1_dev"] == 0.0
assert ft0["c2_max_path_dev"] < 3e-19
assert ft0["n_paths"] == 19683
assert close(ft0["mean_work"], -0.0788, 1e-3)
assert close(ft0["df"], -0.1021, 1e-3)
assert close(ft0["dissipation"], 0.0233, 2e-3)
pre = records["ft0-instrument.json"]["C4_preview"]
assert close(pre["jarzynski_defect"], 4.331e-4, 1e-3)
assert pre["lumped_df"] == pre["true_df"]

assert close(ft1["route_dev_lumped"], 6.7e-16, 5e-2)
assert close(ft1["mean_apparent_work"]["held"], -0.0382, 2e-3)

ft3 = records["ft3-feedback.json"]["measured"]
assert close(ft3["su_deviation"], 5.6e-15, 2e-2)
assert close(ft3["bare_deviation"], 7.34e-3, 1e-3)
assert close(ft3["bare_efficacy"], 0.9927, 1e-4)
assert close(ft3["bystander_deviation"], 5.32e-3, 1e-3)
assert close(ft3["t4_second_law_margin"], 0.489, 1e-3)

gg0 = records["gg0-instrument.json"]["measured"]
w = "0.38032051536830963"
assert f'{gg0["wilson_plaquette_full"]:.17f}' == w
assert f'{gg0["wilson_plaquette_tree_fixed"]:.17f}' == w
assert f'{gg0["wilson_plaquette_closed_form"]:.17f}' == w
assert gg0["elitzur_max_link_exp"] == 0.0
assert gg0["orbit_sizes_counts"] == {"256": 200}
assert close(gg0["tree_fixed_max_nontree_link_exp"],
             gg0["wilson_plaquette_full"], 1e-12)

gg1 = records["gg1-observer-family.json"]["measured"]
assert gg1["g1_max_dev"] == 0.0 and gg1["g2_max_dev"] == 0.0
assert gg1["winding_loops_found"] == 18
assert gg1["winding_max_reading"] == 0.0
assert close(gg1["max_pairwise_link_spread"], 0.855, 1e-3)
assert close(gg1["loop_area2_full"], 0.1455, 1e-3)

gg3 = records["gg3-minimal-coupling.json"]["measured"]
assert gg3["z_ratio_dev"] == 0.0
assert gg3["bare_full_2x2"] == 0.0
assert gg3["dressed_agreement_dev"] == 0.0
assert gg3["bare_unit_observer"] == 1.0
assert close(gg3["dressed_full_2x2"], 0.1008, 1e-3)
assert close(gg3["dressed_3x3"], 0.1004, 1e-3)
assert close(gg3["bare_tree_observer"], 0.1008, 1e-3)
assert close(gg3["observer_bare_spread"], 0.899, 1e-3)

print("all headline bindings hold")
