#!/usr/bin/env python3
"""Generate pgfplots data tables for the complete PF-arc paper.

Every number is read from a committed evidence record in results/ or
from a committed track document or preregistration in experiments/.
Pure standard library, no numpy, no free parameters. Output tables
land in paper/figdata/. The check() calls bind every value typed in
paper/projection-fold-arc.tex, in its abstract, its prose, its figure
captions, and its ledger tables, to the record value it was copied
from, so a record edit breaks the build rather than silently
disagreeing with the paper.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "figdata"
OUT.mkdir(exist_ok=True)


def doc(name: str) -> str:
    return (ROOT / "experiments" / name).read_text(encoding="utf-8")


CAMPAIGN = doc("CAMPAIGN.md")
FREEZE = doc("PF0-TOLERANCE-FREEZE.md")
CEILING = doc("PF7-CEILING.md")
SEALS = doc("SEALS.md")
PF4DESIGN = doc("PF4-DESIGN.md")
PF3PROV = doc("PF3-PROVENANCE.md")
PF5DOC = doc("PF5-INSTRUMENT.md")
PREREG = {n: doc(f"PREREG-{n}.md") for n in
          ("PF4-001", "PF4-002", "PF4-003", "PF4-009",
           "PF5-001", "PF5-002", "PF6-001", "PF6-002")}

CHECKS = 0


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


def check_declared(label: str, text: str, source: str = None) -> None:
    """Bind a declared parameter typed in the paper to its document."""
    global CHECKS
    hay = source if source is not None else CAMPAIGN
    assert text in hay, f"{label}: not declared, missing {text!r}"
    CHECKS += 1


def check_true(label: str, value) -> None:
    global CHECKS
    assert value is True, f"{label}: recorded {value!r}, not True"
    CHECKS += 1


def pct(x: float) -> float:
    return 100.0 * x


# ---------------------------------------------------------------
# Section II. The instrument net, structural stability, and the
# negative control.
# ---------------------------------------------------------------
check_declared("net, creation fold branch counts",
               "branch count `0 -> 1 -> 2`; signed count remains zero")
check_declared("net, annihilation fold",
               "P1 annihilation fold | `t(tau)=-tau^2` | branch count "
               "`2 -> 1 -> 0`")
check_declared("net, degenerate cubic refused",
               "no false classification as a nondegenerate pair fold")
check_declared("net, monotone null",
               "N0 monotone time | `t(tau)=tau` | zero folds and one "
               "branch on every regular slice")
check_declared("freeze, double fold band counts",
               "band counts 1-3-3-3-1, signed count +1 at every slice, "
               "both folds at +/-1/sqrt(3)", FREEZE)
check_declared("freeze, separation exponent",
               "error < 1e-12", FREEZE)
check_declared("freeze, cross-language branch locations",
               "max difference <= 4.5e-16", FREEZE)
check_declared("freeze, first_tol",
               "**first_tol = 1e-9 (frozen).**", FREEZE)
check_declared("freeze, worst first-derivative residual",
               "<= 4.6e-13 on the adaptive path", FREEZE)
check_declared("freeze, second_tol",
               "**second_tol = 1e-8 (frozen).**", FREEZE)
check_declared("freeze, smallest fold curvature",
               "the smallest |d^2 t / d tau^2| is 0.208", FREEZE)
check_declared("freeze, invalidation condition",
               "whose fold curvatures approach 1e-5 in the campaign\n"
               "units invalidates this derivation", FREEZE)
check_declared("freeze, adaptive path tolerances",
               "RelTol 1e-10, AbsTol 1e-12, MaxStep <= 0.01", FREEZE)
check_declared("freeze, fixed-step path",
               "velocity Verlet, dt = 1e-3, valid for tau_max <= 40",
               FREEZE)
check_declared("seal ledger, tolerance freeze",
               "| PF0-FREEZE-001 | experiments/PF0-TOLERANCE-FREEZE.md",
               SEALS)

pf1 = load("pf1-pilot-v2.json")
check_exact("PF-1 trials per norm", pf1["n_trials"], 500)
eps = pf1["epsilon"]
check_exact("PF-1 number of declared perturbation norms", len(eps), 12)
check("PF-1 smallest norm", eps[0], 1e-5, 0.0)
check("PF-1 largest norm", eps[-1], 0.316, 5e-4)
check("PF-1 second largest norm", eps[-2], 0.123, 5e-4)
assert all(p == 1.0 for p in pf1["persistence"][:-1]), \
    "PF-1 persistence is not exactly 1 below the largest norm"
CHECKS += 1
check("PF-1 persistence at the largest norm", pf1["persistence"][-1],
      0.956, 5e-4)
check_exact("PF-1 folds lost at the largest norm", pf1["lost"][-1], 22)
assert all(v == 0 for v in pf1["lost"][:-1]), "PF-1 lost a fold early"
assert all(v == 0 for v in pf1["degenerate"]), \
    "PF-1 recorded a degenerate classification"
CHECKS += 2
worst_exp = max(abs(v - 0.5) for v in pf1["median_exponent"])
check("PF-1 worst median exponent deviation", worst_exp, 2.8e-6, 5e-8)

ens = load("atlas-ensemble.json")
ver = load("atlas-verlet.json")
smoke = load("nrp-smoke.json")
r2run = load("atlas-verlet-r2.json")
check_exact("PF-2 ensemble size", ens["n"], 1000)
check_exact("PF-2 folds in every member", ens["max_folds"], 12)
check_exact("PF-2 mean folds", ens["mean_folds"], 12.0)
check_exact("PF-2 total folds", ens["total_folds"], 12000)
assert all(v == 12 for v in ens["sample_fold_counts"]), \
    "PF-2 sampled member fold counts are not all 12"
hist = ens["fold_histogram"]
assert [i for i, v in enumerate(hist) if v] == [12] and hist[12] == 1000, \
    "PF-2 fold histogram records dispersion"
CHECKS += 2
check("PF-2 ensemble mean relative drift",
      ens["mean_relative_energy_drift"], 6.7e-10, 5e-12)
check_exact("PF-2 single member fold count",
            ver["outcome"]["fold_count"], 12)
check_exact("PF-2 positive orientation segments",
            ver["outcome"]["positive_orientation_segments"], 7)
check_exact("PF-2 negative orientation segments",
            ver["outcome"]["negative_orientation_segments"], 6)
check("PF-2 single member relative drift",
      ver["outcome"]["max_relative_energy_drift"], 1.3e-7, 5e-9)
check_exact("PF-2 cross-substrate outcome hash",
            smoke["outcome_sha256"], ver["outcome_sha256"])
check_exact("PF-2 cross-substrate scenario hash",
            smoke["scenario_sha256"], ver["scenario_sha256"])
check_exact("PF-2 repeat-run outcome hash",
            r2run["outcome_sha256"], ver["outcome_sha256"])

# ---------------------------------------------------------------
# Section III. The replication.
# ---------------------------------------------------------------
pf3 = load("pf3-land2016.json")
g3 = pf3["guards"]
check("PF-3 closed form against the linear system",
      g3["eq66_vs_eq67_max_residual"], 5.7e-14, 5e-16)
check("PF-3 two published forms of the time component",
      g3["eq67_vs_eq76_max_mismatch"], 1.4e-14, 5e-16)
check_true("PF-3 threshold at coupling 2", g3["threshold_ge2_exact"])
check_exact("PF-3 spacelike cells recorded",
            g3["n_spacelike_cells"], 27)
check_exact("PF-3 spacelike cells listed",
            len(g3["spacelike_cells"]), 27)
check("PF-3 Rutherford limit",
      g3["rutherford_cot_half_angle_08_06"], 0.75, 5e-15)
check_exact("PF-3 crossings below threshold",
            pf3["midpoint_bridge"]["below_threshold"][
                "n_tdot_zero_crossings"], 0)
check_exact("PF-3 crossings above threshold",
            pf3["midpoint_bridge"]["above_threshold"][
                "n_tdot_zero_crossings"], 1)
check_exact("PF-3 classification above threshold",
            pf3["midpoint_bridge"]["above_threshold"]["crossings"][0][
                "classification"], "annihilation-fold")
check_declared("PF-3 Cayley pole reading",
               "the Cayley\ntransform (I - G/2)^{-1}(I + G/2), the "
               "Pade(1,1) approximant of the\nexponential, whose pole "
               "at g_e = 2 is exactly the published\nannihilation "
               "threshold", PF3PROV)

# ---------------------------------------------------------------
# Section IV. The Sauter family and the sealed negative.
# ---------------------------------------------------------------
check_declared("Sauter family constants",
               "H = p_t^2/2 + p_u^2/2 + omega_u^2 u^2/2 + lambda u^4/4",
               PREREG["PF4-001"])
check_declared("Sauter family parameters",
               "omega_u = 1.2, lambda = 0.1, g = 0.25,\nL = 3, T = 1, "
               "t(0) = -4L", PREREG["PF4-001"])
check_declared("Sauter integrator",
               "velocity Verlet at dt = 1e-3", PREREG["PF4-001"])

pilot = load("pf4-pilot.json")
pcells = pilot["family_p2s"]["cells"]
check_exact("PF-4 pilot cell count", len(pcells), 18)
check_exact("PF-4 pilot ensemble size", pcells[0]["n"], 50000)
worst_pilot_drift = max(c["max_relative_energy_drift"] for c in pcells)
assert worst_pilot_drift < 7e-7, \
    "a PF-4 pilot cell drifts by more than 7e-7"
CHECKS += 1
razor = {(c["P"], c["E"]): c["fraction"] for c in pcells}
check("PF-4 pilot fraction at gap 0.5 field 0.65", razor[(0.5, 0.65)],
      2.8e-4, 5e-6)
check("PF-4 pilot fraction at gap 0.5 field 0.80", razor[(0.5, 0.80)],
      0.9115, 5e-5)
measurable = [c for c in pcells if 0.0 < c["fraction"] < 0.9]
check_exact("PF-4 pilot measurable cells", len(measurable), 2)

p401 = load("prereg-pf4-001.json")
check_exact("PF4-001 verdict", p401["label"], "neither-axis")
check_exact("PF4-001 cell count",
            len(p401["train_cells"]) + len(p401["held_cells"]), 20)
check_exact("PF4-001 declared held-out MSE bar",
            p401["declared"]["mse_g_bar"], 4.0)
check("PF4-001 fitted effective-gap slope",
      p401["fits"]["model_G"]["beta"], 41.24, 5e-3)
check("PF4-001 held-out weighted error",
      p401["fits"]["model_G"]["held_out_wmse"], 81.22, 5e-3)
check("PF4-001 ratio of the two models",
      p401["fits"]["ratio_S_over_G"], 3.28, 5e-3)
for key in ("near_1pct", "near_10pct"):
    for arm in ("rk4", "dt_half"):
        check_exact(f"PF4-001 control {key} {arm}",
                    p401["controls"][key][arm]["z"], 0.0)
check_exact("PF4-001 zero-field null count",
            p401["zero_field_null"]["count"], 0)
check_declared("PF4-001 binomial-unit bars",
               "bars measured in binomial units test a\nmodel that was "
               "never claimed", PREREG["PF4-002"])

p402 = load("prereg-pf4-002.json")
check_exact("PF4-002 verdict", p402["label"], "demonstrated-in-model")
check_exact("PF4-002 declared generalization bar",
            p402["declared"]["generalization_ratio_bar"], 2.0)
check_exact("PF4-002 declared competition bar",
            p402["declared"]["s_ratio_bar"], 2.0)
gen_ratio = p402["fits"]["model_G"]["generalization_ratio"]
s_ratio = p402["fits"]["ratio_S_over_G_held"]
check("PF4-002 generalization ratio", gen_ratio, 0.3842, 5e-5)
check("PF4-002 generalization ratio, abstract", gen_ratio, 0.38, 5e-3)
check("PF4-002 competition ratio", s_ratio, 3.1398, 5e-5)
check("PF4-002 competition ratio, abstract", s_ratio, 3.14, 5e-3)
check("PF4-002 fitted effective-gap slope",
      p402["fits"]["model_G"]["beta"], 43.18, 5e-3)
for key in ("near_1pct", "near_10pct"):
    for arm in ("rk4", "dt_half"):
        check_exact(f"PF4-002 control {key} {arm}",
                    p402["controls"][key][arm]["z"], 0.0)
check_exact("PF4-002 zero-field null count",
            p402["zero_field_null"]["count"], 0)
check_exact("PF4-002 declared training gaps",
            p402["declared"]["train_P"], [0.55, 0.75, 0.95])
check_exact("PF4-002 declared held-out gaps",
            p402["declared"]["held_P"], [0.65, 0.85])

# The sealed usability rule of PREREG-PF4-001, carried over by
# PREREG-PF4-002, applied to the committed cells.
check_declared("PF4-002 usable-cell rule",
               "Usable cell: count >= 5,\nfraction < 0.9, drift < 1e-4,"
               " probe sub-critical (d > 0)", PREREG["PF4-001"])


def usable(cells):
    return [c for c in cells
            if c["count"] >= 5 and c["fraction"] < 0.9
            and c["max_relative_energy_drift"] < 1e-4
            and c["deterministic_pt_min"] > 0]


u_train = usable(p402["train_cells"])
u_held = usable(p402["held_cells"])
check_exact("PF4-002 usable training cells", len(u_train), 10)
check_exact("PF4-002 usable held-out cells", len(u_held), 7)
check_exact("PF4-002 declared training cells",
            len(p402["train_cells"]), 12)
check_exact("PF4-002 declared held-out cells",
            len(p402["held_cells"]), 8)

alpha_g = p402["fits"]["model_G"]["alpha"]
beta_g = p402["fits"]["model_G"]["beta"]
check("PF4-002 figure line intercept", alpha_g,
      -0.12429061298285399, 0.0)
check("PF4-002 figure line slope", beta_g, 43.176187880553684, 0.0)


def axis_point(c):
    x = (c["deterministic_pt_min"] / c["E"]) ** 2
    return (x, -math.log(c["fraction"]))


write("pf4_train.dat", "xg nlogf",
      [axis_point(c) for c in u_train])
write("pf4_held.dat", "xg nlogf",
      [axis_point(c) for c in u_held])

# ---------------------------------------------------------------
# Section V. The pulse-train family measured empty.
# ---------------------------------------------------------------
check_declared("pulse train field", "E = 0.6,\nL = 3, D = 18",
               PREREG["PF4-003"])
check_declared("pulse train cap", "cap 4000\nslabs", PREREG["PF4-003"])
p403 = load("prereg-pf4-003.json")
check_exact("PF4-003 verdict", p403["label"], "unevaluable")
check_exact("PF4-003 declared cap", p403["declared"]["n_cap"], 4000)
check_exact("PF4-003 training velocities",
            len(p403["declared"]["train_P"]), 4)
check_exact("PF4-003 held-out velocities",
            len(p403["declared"]["held_P"]), 3)
for arm in ("smooth", "plant"):
    for group in ("train", "held"):
        for cell in p403[arm][group]:
            check_exact(f"PF4-003 {arm} {group} cell reversed",
                        cell["reversed"], False)

probe4 = load("pf4-004-probe.json")
check_exact("PF4-004 probe cap", probe4["declared"]["cap"], 300)
n_probe_cells = sum(len(v) for v in probe4["grid"].values())
check_exact("PF4-004 probe cell count", n_probe_cells, 12)
check_exact("PF4-004 probe field ladder",
            len(probe4["declared"]["E_ladder"]), 3)
check_exact("PF4-004 probe velocity grid",
            len(probe4["declared"]["P_grid"]), 4)
for rung in probe4["grid"].values():
    for cell in rung:
        check_exact("PF4-004 probe cell reversed", cell["reversed"],
                    False)

mech = load("pf4-mechanism.json")
check_exact("PF4 mechanism flag", mech["finding"]["supported"], False)
ratios = [c["cancellation_ratio"] for c in mech["cells"]]
for i, typed in enumerate([0.033, 0.009, 0.050]):
    check(f"PF4 mechanism cancellation ratio {i}", ratios[i], typed,
          5e-4)
check("PF4 mechanism drift percent 0", pct(ratios[0]), 3.3, 5e-2)
check("PF4 mechanism drift percent 1", pct(ratios[1]), 0.9, 5e-2)
check("PF4 mechanism drift percent 2", pct(ratios[2]), 5.0, 5e-2)
assert round(max(ratios), 3) <= 0.05 and min(ratios) >= 0.008, \
    "the cancelled fraction is not between 95 and 99 percent"
CHECKS += 1
flips = [c["sign_flip_fraction"] for c in mech["cells"]]
for i, typed in enumerate([0.54, 0.68, 0.27]):
    check(f"PF4 mechanism sign-flip fraction {i}", flips[i], typed,
          5e-3)
check("PF4 mechanism third-cell drift per slab",
      mech["cells"][2]["mean_drift_per_slab"], 0.0096, 5e-5)
assert mech["cells"][2]["mean_drift_per_slab"] > 0, \
    "the third mechanism cell's drift is not positive"
CHECKS += 1

# ---------------------------------------------------------------
# Section VI. The two mandatory gates.
# ---------------------------------------------------------------
inst5 = load("pf5-instrument.json")
c5 = inst5["controls"]
check("PF-5 harmonic control drift", c5["C1_harmonic_drift"], 4.4e-7,
      5e-9)
check_declared("PF-5 harmonic control bar",
               "drift 4.4e-7 against the 1e-6 control\nbar", PF5DOC)
check_exact("PF-5 field-free control transmitted",
            c5["C2a_field_free_census"]["transmitted"], 2000)
check_exact("PF-5 deterministic control reversing",
            c5["C2b_deterministic_census"]["reversing"], 2000)
check_exact("PF-5 failure control nonfinite",
            c5["C3_failure_census"]["nonfinite"], 200)
check_exact("PF-5 capped control", c5["C3b_capped_census"]["capped"],
            100)
check_exact("PF-5 double fold levels", c5["C4_levels_checked"], 41)
check_true("PF-5 deletion trap flagged", c5["C5_deletion_flagged"])
check_declared("PF-5 charge assignment",
               "charge = sign(dt/dtau)", PREREG["PF5-001"])
check_exact("PF-5 declared energy bar", inst5["declared"]["energy_bar"],
            1e-5)

p501 = load("prereg-pf5-001.json")
check_exact("PF5-001 verdict", p501["verdict"]["value"], "PASS")
check_exact("PF5-001 evaluable cells", p501["evaluable_cells"], 8)
check_exact("PF5-001 ensemble size", p501["declared"]["n"], 20000)
cells501 = p501["cells"]
check_exact("PF5-001 cell count", len(cells501), 8)
for name, c in cells501.items():
    tot = sum(c["counts"].values())
    check_exact(f"PF5-001 census sums at {name}", tot, 20000)
    check_exact(f"PF5-001 reversing at {name}", c["counts"]["reversing"],
                0)
    check_exact(f"PF5-001 transmitted at {name}",
                c["counts"]["transmitted"], 20000)
    check_exact(f"PF5-001 path-degree failures at {name}",
                c["path_degree_failures"], 0)
    check_exact(f"PF5-001 refused levels at {name}",
                c["refused_levels"], 0)
worst501 = max(c["max_energy_residual"] for c in cells501.values())
check("PF5-001 worst relative residual", worst501, 6.5e-7, 5e-9)
check_exact("PF5-001 declared polyline members per cell",
            p501["declared"]["k_poly"], 12)
check_exact("PF5-001 declared polyline members in total",
            8 * p501["declared"]["k_poly"], 96)
check_exact("PF5-001 members transmitted in total",
            8 * 20000, 160000)

probe5 = load("pf5-placement-probe.json")
check_exact("PF5 placement probe window",
            probe5["declared"]["window"], [0.02, 0.3])
fracs5 = [r["frac_selected"] for r in probe5["rows"]]
for i, typed in enumerate([0.1000, 0.0970, 0.0995, 0.1030]):
    check(f"PF5 placement probe fraction {i}", fracs5[i], typed, 5e-5)
    check_true(f"PF5 placement probe cell {i} in window",
               probe5["rows"][i]["in_window"])

p502 = load("prereg-pf5-002.json")
check_exact("PF5-002 verdict", p502["verdict"]["value"], "PASS")
check_exact("PF5-002 evaluable cells", p502["evaluable_cells"], 4)
check_exact("PF5-002 declared minimum total reversals",
            p502["declared"]["min_total_reversals"], 2000)
cells502 = p502["cells"]
rev502 = [cells502[k]["counts"]["reversing"] for k in sorted(cells502)]
check_exact("PF5-002 reversing counts", rev502,
            [1998, 1952, 1881, 2237])
check_exact("PF5-002 audited pair events", sum(rev502), 8068)
for name, c in cells502.items():
    check_exact(f"PF5-002 census sums at {name}",
                sum(c["counts"].values()), 20000)
    check_exact(f"PF5-002 path-degree failures at {name}",
                c["path_degree_failures"], 0)
    check_exact(f"PF5-002 refused levels at {name}",
                c["refused_levels"], 0)
worst502 = max(c["max_energy_residual"] for c in cells502.values())
check("PF5-002 worst relative residual", worst502, 7.3e-7, 5e-9)
check_exact("PF5-002 declared polyline members in total",
            4 * p502["declared"]["k_poly"], 48)

inst6 = load("pf6-instrument.json")
check("PF-6 translation validation",
      inst6["P1_translation"]["reversing"]["max_worldline_dev"],
      2.7e-13, 5e-15)
check_exact("PF-6 reparametrization path deviation",
            inst6["P2_reparametrization"]["path_dev"], 0.0)
check_exact("PF-6 reparametrization rate ratio",
            inst6["P2_reparametrization"]["rate_per_tau_ratio"],
            inst6["P2_reparametrization"]["predicted_ratio"])
check("PF-6 boost commutation",
      inst6["P3_boost"]["worst_commutation"], 4.5e-13, 5e-15)
check("PF-6 boost invariant drift",
      inst6["P3_boost"]["worst_invariant_drift"], 7.1e-11, 5e-13)
assert inst6["P3_boost"]["min_future_cone_margin"] > 0, \
    "the future-cone margin is not positive"
CHECKS += 1
check("PF-6 gauge control history",
      inst6["P4_gauge_control"]["history_dev"], 2.2e-13, 5e-15)
check("PF-6 gauge control canonical shift",
      inst6["P4_gauge_control"]["canonical_shift_dev"], 1.1e-12, 5e-14)
check_declared("PF-6 gauge clause not applicable",
               "Recorded not-applicable, the Sauter tilt is\n"
               "   declared non-electromagnetic", PREREG["PF6-002"])

p601 = load("prereg-pf6-001.json")
check_exact("PF6-001 verdict", p601["verdict"]["value"], "vacuous")
check_exact("PF6-001 cells without folds",
            p601["measured"]["cells_without_folds"], 4)
for name, c in p601["cells"].items():
    check_exact(f"PF6-001 fold count at {name}", c["fold_count"], 0)
check_exact("PF6-001 anti-vacuity bar", p601["bars"]["b6_anti_vacuity"],
            False)

probe6 = load("pf6-member-probe.json")
p602 = load("prereg-pf6-002.json")
check_exact("PF6-002 verdict", p602["verdict"]["value"], "PASS")
folds602 = [p602["cells"][k]["fold_count"] for k in sorted(p602["cells"])]
check_exact("PF6-002 fold counts", folds602, [4, 2, 2, 2])
check_exact("PF6-002 fold counts match the probe", folds602,
            p602["declared"]["probe_folds"])
check_exact("PF6-002 total folds", p602["measured"]["total_folds"], 10)
check_true("PF6-002 all fold counts even",
           p602["measured"]["all_fold_counts_even"])
check("PF6-002 worst worldpoint deviation",
      p602["measured"]["worst_worldpoint_dev"], 3.1e-14, 5e-16)
check_exact("PF6-002 rate ratio deviation",
            p602["measured"]["worst_rate_ratio_dev"], 0.0)
check("PF6-002 boost commutation",
      p602["measured"]["boost_worst_commutation"], 4.5e-13, 5e-15)
check("PF6-002 boost invariant drift",
      p602["measured"]["boost_worst_invariant_drift"], 7.1e-11, 5e-13)
check_exact("PF6-002 declared observer grid",
            len(p602["declared"]["alpha_grid"]), 6)
for name, c in p602["cells"].items():
    check_exact(f"PF6-002 observer readings at {name}",
                len(c["observer_curve"]), 6)
check_true("PF6-002 observer audit", p602["bars"]["b5_observer_detector"])

# ---------------------------------------------------------------
# Section VII. The quantum-structure ceiling.
# ---------------------------------------------------------------
pf7 = load("pf7-quantum-ceiling.json")
d7 = pf7["declared"]
check_exact("PF-7 declared gap", d7["delta"], 0.3)
check_exact("PF-7 declared sweep rate", d7["sweep_v"], 1.0)
check_exact("PF-7 declared quantum bar", d7["quantum_osc_bar"], 0.3)
check_exact("PF-7 declared classical bar", d7["classical_osc_bar"], 0.15)
check_exact("PF-7 declared ratio bar", d7["ratio_bar"], 3.0)
check_exact("PF-7 declared ensemble", d7["n_ensemble"], 2000)
lz = pf7["measured"]["q1_probability_closed_form"]
check("PF-7 Landau-Zener closed form", lz, 0.868167, 5e-7)
check("PF-7 closed form from its own formula",
      math.exp(-math.pi * d7["delta"] ** 2 / (2.0 * d7["sweep_v"])),
      lz, 1e-15)
check_exact("PF-7 verdict", pf7["verdict"]["value"], "FAIL")
check("PF-7 single-passage measurement",
      pf7["measured"]["q1_probability_measured"], 0.8631, 5e-5)
check("PF-7 single-passage deviation", pf7["measured"]["q1_deviation"],
      5.06e-3, 5e-6)
check("PF-7 quantum statistic",
      pf7["measured"]["quantum_osc_power_ratio"], 0.2238, 5e-5)
check("PF-7 norm conservation",
      pf7["measured"]["quantum_worst_norm_dev"], 5.5e-14, 5e-16)
check_exact("PF-7 classical grid size",
            len(pf7["measured"]["classical_curve"]), 24)
assert all(v == 1.0 for v in pf7["measured"]["classical_curve"]), \
    "the first ceiling run's classical curve is not exactly constant"
assert all(v == 2000 for v in
           pf7["measured"]["classical_reversing_counts"]), \
    "the first ceiling run did not reverse every member"
CHECKS += 2
check_declared("PF-7 chirp diagnosis",
               "oscillation is a chirp whose local frequency grows "
               "linearly with\ndelay", CEILING)

cp1 = load("pf7-classical-probe.json")
check_exact("PF-7 first probe rejected its range",
            cp1["measured"]["in_window"], False)
check_exact("PF-7 first probe fraction at the shortest delay",
            cp1["measured"]["frac_at_edge_delays"]["4.0"], 1.0)
cp2 = load("pf7-classical-probe2.json")
check_true("PF-7 second probe in window", cp2["measured"]["in_window"])
fb = cp2["measured"]["fraction_by_delay"]
for key, typed in [("8.0", 0.5245), ("11.0", 0.4945), ("14.0", 0.4750),
                   ("17.0", 0.4835), ("20.0", 0.4955)]:
    check(f"PF-7 second probe fraction at delay {key}", fb[key], typed,
          5e-5)

pf7b = load("pf7b-quantum-ceiling.json")
m7b = pf7b["measured"]
check_exact("PF-7b verdict", pf7b["verdict"]["value"], "PASS")
check("PF-7b single-passage deviation", m7b["q1_deviation"], 1.49e-3,
      5e-6)
check("PF-7b quantum statistic", m7b["quantum_osc_power_ratio"],
      0.8702, 5e-5)
check("PF-7b norm conservation", m7b["quantum_worst_norm_dev"],
      5.9e-14, 5e-16)
check("PF-7b classical minimum", m7b["classical_fraction_min"], 0.4645,
      5e-5)
check("PF-7b classical maximum", m7b["classical_fraction_max"], 0.5245,
      5e-5)
check("PF-7b classical statistic", m7b["classical_osc_power_ratio"],
      0.3626, 5e-5)
check("PF-7b quantum to classical ratio",
      m7b["quantum_over_classical_ratio"], 2.40, 5e-3)
check_exact("PF-7b grid size", len(m7b["quantum_curve"]), 32)
write("pf7_quantum.dat", "t2 p",
      [(t * t, p) for t, p in zip(pf7b["declared"]["t_half_grid"],
                                  m7b["quantum_curve"])])

pf7c = load("pf7c-noise-floor.json")
m7c = pf7c["measured"]
check_exact("PF-7c verdict", pf7c["verdict"]["value"], "PASS")
check_exact("PF-7c null draws", pf7c["declared"]["n_null"], 20000)
check("PF-7c binomial sigma", m7c["binomial_sigma"], 0.011, 5e-4)
check("PF-7c curve span",
      m7c["curve_range"][1] - m7c["curve_range"][0], 0.06, 5e-4)
check("PF-7c null mean", m7c["null_mean"], 0.2165, 5e-5)
check("PF-7c null ninety-fifth percentile", m7c["null_q95"], 0.3310,
      5e-5)
check("PF-7c classical p-value", m7c["classical_p_value"], 0.0262,
      5e-5)
check_exact("PF-7c quantum p-value", m7c["quantum_p_value"], 0.0)
check_exact("PF-7c points", m7c["n_points"], 32)

pf7d = load("pf7d-ringing-test.json")
m7d = pf7d["measured"]
check_exact("PF-7d verdict", pf7d["verdict"]["value"], "PASS")
check_exact("PF-7d ensemble", pf7d["declared"]["n_members"], 8000)
check("PF-7d p-value", m7d["p_value"], 0.02605, 5e-6)
check("PF-7d prior p-value", m7d["prior_p_value_at_2000_members"],
      0.0262, 5e-5)
check("PF-7d peak period", m7d["peak_period_in_delay"], 12.52, 5e-3)
check("PF-7d declared ringing period", m7d["declared_ringing_period"],
      5.236, 5e-4)
check_exact("PF-7d ringing finding", pf7d["findings"][
    "R4_peak_at_ringing_frequency"], False)
curve7d = m7d["curve"]
half = len(curve7d) // 2
check("PF-7d first-half mean", sum(curve7d[:half]) / half, 0.4942,
      5e-5)
check("PF-7d second-half mean", sum(curve7d[half:]) / half, 0.4829,
      5e-5)
check("PF-7d curve range", max(curve7d) - min(curve7d), 0.0425, 5e-5)
write("pf7_classical.dat", "d f",
      list(zip(m7d["delays"], curve7d)))

pf7e = load("pf7e-detrended.json")
m7e = pf7e["measured"]
check_exact("PF-7e verdict", pf7e["verdict"]["value"], "FAIL")
check_exact("PF-7e first item", pf7e["items"][
    "E1_detrend_reduces_classical"], False)
check("PF-7e raw classical statistic", m7e["classical_raw_statistic"],
      0.4480, 5e-5)
check("PF-7e detrended classical statistic",
      m7e["classical_detrended_statistic"], 0.5014, 5e-5)
check("PF-7e raw p-value", m7e["classical_raw_p_value"], 0.02605,
      5e-6)
check("PF-7e detrended p-value", m7e["classical_detrended_p_value"],
      0.01185, 5e-6)
check("PF-7e quantum before", m7e["quantum_raw_statistic"], 0.8702,
      5e-5)
check("PF-7e quantum after", m7e["quantum_detrended_statistic"],
      0.8702, 5e-5)
check("PF-7e trend drop", m7e["trend_drop_over_range"], 0.0234, 5e-5)
check("PF-7e binomial sigma", m7e["binomial_sigma"], 0.0056, 5e-5)
check("PF-7e trend in standard errors", m7e["trend_in_sigma"], 4.19,
      5e-3)

pf7f = load("pf7f-smooth-residual.json")
m7f = pf7f["measured"]
check_exact("PF-7f verdict", pf7f["verdict"]["value"], "PASS")
check_true("PF-7f classical residual consistent with noise",
           pf7f["findings"][
               "F4_classical_consistent_with_noise_after_smooth_model"])
check_true("PF-7f trend is real", pf7f["findings"]["F5_trend_is_real"])
check("PF-7f raw classical statistic", m7f["classical_raw_statistic"],
      0.4480, 5e-5)
check("PF-7f residual statistic",
      m7f["classical_detrended_statistic"], 0.2122, 5e-5)
check("PF-7f residual p-value", m7f["classical_detrended_p_value"],
      0.757, 5e-4)
check("PF-7f quantum after", m7f["quantum_detrended_statistic"],
      0.8724, 5e-5)
check("PF-7f trend in standard errors", m7f["trend_in_sigma"], 4.19,
      5e-3)
assert m7f["classical_detrended_statistic"] < m7f["null_detrended_mean"], \
    "the PF-7f residual does not sit below the null mean"
CHECKS += 1
write("pf7_stats.dat", "idx stat",
      [(1, m7f["null_detrended_mean"]),
       (2, m7f["null_detrended_q95"]),
       (3, m7f["classical_raw_statistic"]),
       (4, m7f["classical_detrended_statistic"]),
       (5, m7f["quantum_detrended_statistic"])])
check_declared("PF-7f terminus declared before the run",
               "The terminus, declared now so the campaign does not "
               "chase this", CEILING)

# ---------------------------------------------------------------
# Section VIII. The decay gate.
# ---------------------------------------------------------------
blind = load("pf8-blind-probe.json")
pooled_u = blind["arm_a_pooled_u"]
check_exact("PF-8 probe pooled crossings", pooled_u["n_crossings"], 533)
check("PF-8 probe smallest transverse coordinate", pooled_u["min"],
      -2.68598, 5e-6)
check("PF-8 probe largest transverse coordinate", pooled_u["max"],
      2.714888, 5e-7)
check_declared("PF-8 probe measured the pair-creation window empty",
               "t_end equals t_max and t_start equals t_min on every "
               "bound member", blind["declared"]["first_pass_note"])

pf8 = load("pf8-decay-gate.json")
m8 = pf8["measured"]
check_exact("PF-8 verdict", pf8["verdict"]["value"], "PASS")
for key in ("D1_complete_observer_parity", "D2_signed_count",
            "D3_blind_consumer", "D4_anti_vacuity"):
    check_true(f"PF-8 bar {key}", pf8["bars"][key])
check_exact("PF-8 blind window", pf8["declared"]["blind_window_u"],
            [-0.7, 0.7])
check_exact("PF-8 members audited", m8["members_audited"], 4)
check_exact("PF-8 observations", m8["blind_observations"], 441)
check_exact("PF-8 polylines audited", m8["polylines_audited"], 400)
check_exact("PF-8 odd events", m8["odd_events"], 0)
check_exact("PF-8 deterministic parity failures",
            m8["parity_failures_deterministic"], 0)
check_exact("PF-8 thermal parity failures",
            m8["parity_failures_thermal"], 0)
check_exact("PF-8 deterministic signed-count failures",
            m8["signed_count_failures_deterministic"], 0)
check_exact("PF-8 thermal signed-count failures",
            m8["signed_count_failures_thermal"], 0)
check_exact("PF-8 signed-count spread", m8["signed_count_spread"], 0)
check_exact("PF-8 hidden crossings", m8["hidden_crossings"], 147)
check_exact("PF-8 parity flips", m8["blind_parity_flips"], 129)
check("PF-8 parity flip fraction", m8["blind_parity_flip_fraction"],
      0.2925, 5e-5)
check_exact("PF-8 apparent decay events", m8["apparent_decay_events"],
            63)
check_exact("PF-8 detector-model mismatches",
            m8["blind_detector_mismatches"], 0)
check_exact("PF-8 multibranch levels", m8["multibranch_levels"], 46)
check_exact("PF-8 thermal reversing total", m8["thermal_reversing_total"],
            1963)
check_exact("PF-8 thermal missing trajectories",
            m8["thermal_missing_trajectories"], 0)
check("PF-8 thermal worst residual", m8["thermal_max_energy_residual"],
      6.3e-7, 5e-9)
check("PF-8 hidden fraction of probe crossings",
      m8["hidden_crossings"] / pooled_u["n_crossings"], 0.276, 5e-4)

members8 = pf8["arm_a_members"]
check_exact("PF-8 member count", len(members8), 4)
folds8 = [members8[k]["fold_count"] for k in sorted(members8)]
check_exact("PF-8 fold counts", folds8, [4, 2, 2, 2])
assert all(f % 2 == 0 for f in folds8), "a PF-8 fold count is odd"
CHECKS += 1
narrowest = min(e["width"] for m in members8.values()
                for e in m["excursions"])
check("PF-8 narrowest fold excursion", narrowest, 0.000253, 5e-7)
check_declared("PF-8 background ladder spacing",
               "against a uniform ladder spacing", CAMPAIGN)

complete_pool = {0: 0, 1: 0, 2: 0, 3: 0}
blind_pool = {0: 0, 1: 0, 2: 0, 3: 0}
for m in members8.values():
    for k, v in m["complete_counts"].items():
        complete_pool[int(k)] += v
    for k, v in m["blind_counts"].items():
        blind_pool[int(k)] += v
    for k in m["complete_jumps"]:
        assert int(k) in (-2, 0, 2), \
            f"a complete-observer jump of {k} was recorded"
    for k in m["signed_counts_seen"]:
        check_exact("PF-8 signed count on an audited member", k, 1)
CHECKS += 1
check_exact("PF-8 complete observer never records 0 branches",
            complete_pool[0], 0)
check_exact("PF-8 complete observer never records 2 branches",
            complete_pool[2], 0)
check_exact("PF-8 complete observer total",
            sum(complete_pool.values()), 441)
check_exact("PF-8 blind observer total", sum(blind_pool.values()), 441)
write("pf8_complete.dat", "n count",
      [(n, complete_pool[n]) for n in (0, 1, 2, 3)])
write("pf8_blind.dat", "n count",
      [(n, blind_pool[n]) for n in (0, 1, 2, 3)])

b8 = pf8["pf8b_summary"]
ps = b8["pooled_stats"]
check_exact("PF-8b pooled sample", ps["n"], 1963)
check("PF-8b pooled mean proper time", ps["mean_tau"], 18.92, 5e-3)
check("PF-8b pooled standard deviation", ps["sd_tau"], 3.01, 5e-3)
check("PF-8b pooled coefficient of variation",
      ps["coefficient_of_variation"], 0.159, 5e-4)
check("PF-8b pooled sup deviation", ps["exp_fit_sup_deviation"], 0.506,
      5e-4)
check("PF-8b onset-shifted coefficient of variation",
      ps["coefficient_of_variation_onset_shifted"], 0.494, 5e-4)
check("PF-8b onset-shifted sup deviation",
      ps["exp_fit_sup_deviation_onset_shifted"], 0.232, 5e-4)
cellcv = [pf8["pf8b_cells"][k]["stats"]["coefficient_of_variation"]
          for k in sorted(pf8["pf8b_cells"])]
for i, typed in enumerate([0.0526, 0.0530, 0.0694, 0.0764]):
    check(f"PF-8b coefficient of variation in cell {i}", cellcv[i],
          typed, 5e-5)
cellsup = [pf8["pf8b_cells"][k]["stats"]["exp_fit_sup_deviation"]
           for k in sorted(pf8["pf8b_cells"])]
assert all(abs(v - 0.57) < 0.011 for v in cellsup), \
    "a per-cell sup deviation is not near 0.57"
CHECKS += 1
check_exact("PF-8b cross-check sample", b8["exact_crosscheck_n"], 32)
check("PF-8b cross-check mean", b8["exact_crosscheck_mean_tau"], 18.94,
      5e-3)
check("PF-8b cross-check coefficient of variation",
      b8["exact_crosscheck_cv"], 0.188, 5e-4)

# ---------------------------------------------------------------
# Section IX. The summit sequence.
# ---------------------------------------------------------------
hunt = load("pf4-hunt-probe1.json")
check("hunt probe coefficient of determination",
      hunt["fit"]["r_squared"], 0.9921, 5e-5)
check("hunt probe slope", hunt["fit"]["slope_vs_invP"], -7.8186, 5e-5)
check("hunt probe naive estimate", hunt["fit"]["analyticity_prediction"],
      -11.3097, 5e-5)

a005 = load("pf4-005-analyticity.json")
m005 = a005["measured"]
check_exact("PF4-005 verdict", a005["verdict"]["value"], "FAIL")
check("PF4-005 timestep control", m005["convergence_relative_change"],
      6.9e-11, 5e-13)
cells005 = m005["cells"]
check("PF4-005 replication of the hunt probe slope",
      cells005["sech2_L3.0"]["slope_vs_inv_p"], -7.8154, 5e-5)
for i, (key, typed) in enumerate([("lorentz_L2.0", 0.99997),
                                  ("lorentz_L3.0", 0.99991),
                                  ("lorentz_L4.0", 0.99933)]):
    check(f"PF4-005 Lorentzian fit quality {i}",
          cells005[key]["r_squared"], typed, 5e-6)
for i, (key, typed) in enumerate([("lorentz_L2.0", 1.0095),
                                  ("lorentz_L3.0", 1.0344),
                                  ("lorentz_L4.0", 1.0658)]):
    check(f"PF4-005 Lorentzian ratio {i}",
          cells005[key]["slope_over_naive"], typed, 5e-5)
for i, (key, typed) in enumerate([("sech2_L2.0", 0.5430),
                                  ("sech2_L3.0", 0.6910),
                                  ("sech2_L4.0", 0.8098)]):
    check(f"PF4-005 sech-squared ratio {i}",
          cells005[key]["slope_over_naive"], typed, 5e-5)
a05b = load("pf4-005b-analyticity.json")
check_declared("PF4-005 named error",
               "the velocity grid was declared in absolute velocity",
               a05b["declared"]["named_error_of_the_prior_run"])
m05b = a05b["measured"]
check_exact("PF4-005b verdict", a05b["verdict"]["value"], "FAIL")
check_exact("PF4-005b failed bar", a05b["items"]["B1_exponential_form"],
            False)
check_true("PF4-005b width universality",
           a05b["items"]["B2_lorentz_width_universal"])
check_true("PF4-005b parameter-free agreement",
           a05b["items"]["B3_lorentz_matches_prediction"])
check_exact("PF4-005b refuted expectation",
            a05b["findings"]["F1_sech2_not_width_universal"], False)
check_exact("PF4-005b parameter-free prediction",
            m05b["absolute_prediction"], -2.0)
lz_slopes = m05b["lorentz_slopes"]
for i, typed in enumerate([-2.0661, -2.0639, -2.0607]):
    check(f"PF4-005b Lorentzian exponent {i}", lz_slopes[i], typed,
          5e-5)
check("PF4-005b Lorentzian spread percent",
      pct(m05b["lorentz_relative_spread"]), 0.26, 5e-3)
lorentz_over = [a05b["measured"]["cells"][k]["slope_over_prediction"]
                for k in ("lorentz_L2.0", "lorentz_L3.0",
                          "lorentz_L4.0")]
assert all(abs(pct(v - 1.0) - 3.3) < 0.35 for v in lorentz_over), \
    "the Lorentzian exponents are not 3.3 percent above the prediction"
CHECKS += 1
s2_slopes = m05b["sech2_slopes"]
for i, typed in enumerate([-1.0490, -1.0478, -1.0462]):
    check(f"PF4-005b sech-squared exponent {i}", s2_slopes[i], typed,
          5e-5)
check("PF4-005b sech-squared spread percent",
      pct(m05b["sech2_relative_spread"]), 0.27, 5e-3)
check("PF4-005b sech-squared fraction of the naive value",
      a05b["measured"]["cells"]["sech2_L2.0"]["slope_over_prediction"],
      0.5245, 5e-5)
check("PF4-005b timestep control", m05b["convergence_relative_change"],
      1.8e-13, 5e-15)
check_exact("PF4-005b declared fit-quality bar",
            a05b["declared"]["r2_bar"], 0.99)
for i, key in enumerate(("sech2_L2.0", "sech2_L3.0", "sech2_L4.0")):
    check(f"PF4-005b sech-squared fit quality {i}",
          a05b["measured"]["cells"][key]["r_squared"],
          [0.9886, 0.9887, 0.9889][i], 5e-5)
for i, key in enumerate(("lorentz_L2.0", "lorentz_L3.0",
                         "lorentz_L4.0")):
    check(f"PF4-005b Lorentzian fit quality {i}",
          a05b["measured"]["cells"][key]["r_squared"], 0.9998, 5e-5)
check_exact("PF4-005b widths", a05b["declared"]["L_grid"],
            [2.0, 3.0, 4.0])
write("pf4_005b_lorentz.dat", "L slope",
      [(a05b["measured"]["cells"][k]["L"],
        a05b["measured"]["cells"][k]["slope_vs_kappa"])
       for k in ("lorentz_L2.0", "lorentz_L3.0", "lorentz_L4.0")])

# The adiabaticity of Eq. (6), rebuilt from the record's own grids.
for key, c in a05b["measured"]["cells"].items():
    for kappa, p in zip(c["kappa_grid"], c["p_values"]):
        check(f"adiabaticity definition at {key}",
              1.2 * c["pole_distance"] / p, kappa, 1e-5)

a006 = load("pf4-006-gate.json")
m006 = a006["measured"]
check_exact("PF4-006 verdict", a006["verdict"]["value"], "FAIL")
check_exact("PF4-006 failed item",
            a006["items"]["G4_entry_and_timestep_independence"], False)
check_true("PF4-006 conservation", a006["items"]["G1_conserved_quantity"])
check_true("PF4-006 census", a006["items"]["G2_complete_census"])
check_true("PF4-006 translation",
           a006["items"]["G3_translation_covariance"])
check("PF4-006 worst conservation drift",
      m006["worst_hamiltonian_drift"], 8.6e-14, 5e-16)
check("PF4-006 worst translation change",
      m006["worst_translation_change"], 8.8e-14, 5e-16)
check_exact("PF4-006 census transmitted", m006["census"]["transmitted"],
            9)
check_exact("PF4-006 census nonfinite", m006["census"]["nonfinite"], 0)
check_exact("PF4-006 declared shift bar",
            a006["declared"]["shift_bar"], 1e-10)
check_exact("PF4-006 declared stability bar",
            a006["declared"]["stability_bar"], 1e-8)
entry006 = [m006["stability_relative_changes"][f"L{L}_entry"]
            for L in (2.0, 3.0, 4.0)]
for i, typed in enumerate([1.289, 1.295, 1.291]):
    check(f"PF4-006 entry-point change {i}", pct(entry006[i]), typed,
          5e-3)
step006 = [m006["stability_relative_changes"][f"L{L}_timestep"]
           for L in (2.0, 3.0, 4.0)]
assert all(1e-7 < v < 1e-6 for v in step006), \
    "the PF4-006 timestep changes are not near 3e-7"
CHECKS += 1

a007 = load("pf4-007-span.json")
m007 = a007["measured"]
check_exact("PF4-007 verdict", a007["verdict"]["value"], "PASS")
lad = m007["ladders"]["lorentz"]["successive_relative_change"]
for i, typed in enumerate([1.278, 0.586, 0.130, 0.015]):
    check(f"PF4-007 Lorentzian successive change {i}", pct(lad[i]),
          typed, 5e-3)
check("PF4-007 sech-squared change along the ladder",
      max(m007["ladders"]["sech2"]["successive_relative_change"]),
      1.1e-13, 6e-15)
check_exact("PF4-007 declared convergence bar",
            a007["declared"]["bars"]["S2_sech2_convergence"], 1e-9)
check("PF4-007 worst exponent change",
      pct(m007["worst_relative_exponent_change"]), 0.28, 5e-3)
check("PF4-007 universality at the furthest span",
      pct(m007["lorentz_spread_at_far_span"]), 0.36, 5e-3)

a008 = load("pf4-008-pole-order.json")
m008 = a008["measured"]
check_exact("PF4-008 verdict", a008["verdict"]["value"], "FAIL")
check_exact("PF4-008 failed item",
            a008["items"]["P1a_conserved_quantity"], False)
check_exact("PF4-008 distance-only hypothesis",
            a008["findings"]["F1_distance_only"], False)
check_true("PF4-008 order hypothesis",
           a008["findings"]["F2_order_matters"])
check("PF4-008 entry-point clause", m008["entry_relative_change"],
      5.7e-11, 5e-13)
check("PF4-008 timestep clause", m008["timestep_relative_change"],
      4.9e-13, 5e-15)
check("PF4-008 translation clause", m008["translation_relative_change"],
      6.5e-15, 5e-17)
for i, typed in enumerate([-1.9333, -1.9286, -1.9217]):
    check(f"PF4-008 Gudermannian exponent {i}",
          m008["gudermann_slopes"][i], typed, 5e-5)
check("PF4-008 Gudermannian spread percent",
      pct(m008["gudermann_relative_spread"]), 0.61, 5e-3)
for i, typed in enumerate([-1.1028, -1.1015, -1.0997]):
    check(f"PF4-008 sech-squared exponent {i}",
          m008["sech2_slopes"][i], typed, 5e-5)
check("PF4-008 sech-squared spread percent",
      pct(m008["sech2_relative_spread"]), 0.29, 5e-3)
check("PF4-008 exponent ratio", m008["ratio_gudermann_over_sech2"],
      1.75, 5e-3)
check("PF4-008 worst conservation drift",
      m008["worst_hamiltonian_drift"], 1.9e-10, 5e-12)
check_exact("PF4-008 declared conservation bar",
            a008["declared"]["bars"]["hamiltonian"], 1e-10)
check_exact("PF4-008 Lorentzian entry-point failure carried forward",
            a006["measured"]["worst_stability_change"] > 1e-2, True)
check("PF4-008 Lorentzian entry-point failure magnitude",
      a006["measured"]["worst_stability_change"], 1.3e-2, 5e-4)

a08b = load("pf4-008b-pole-order.json")
check_exact("PF4-008b verdict", a08b["verdict"]["value"], "FAIL")
check_exact("PF4-008b halved timestep", a08b["declared"]["dt"],
            a008["declared"]["dt"] / 2.0)
check("PF4-008b worst conservation drift",
      a08b["measured"]["worst_hamiltonian_drift"], 2.0e-10, 5e-12)

a08c = load("pf4-008c-pole-order.json")
m08c = a08c["measured"]
check_exact("PF4-008c verdict", a08c["verdict"]["value"], "PASS")
check_exact("PF4-008c item count", len(a08c["items"]), 8)
for key, val in a08c["items"].items():
    check_true(f"PF4-008c item {key}", val)
check("PF4-008c worst conservation drift",
      m08c["worst_hamiltonian_drift"], 2.6e-12, 5e-14)
check("PF4-008c entry-point independence",
      m08c["entry_relative_change"], 3.0e-9, 5e-11)
check("PF4-008c timestep independence",
      m08c["timestep_relative_change"], 6.6e-13, 5e-15)
check("PF4-008c translation covariance",
      m08c["translation_relative_change"], 2.5e-15, 5e-17)
for i in range(3):
    check(f"PF4-008c exponent {i} moves only in its seventh digit",
          m08c["gudermann_slopes"][i], m008["gudermann_slopes"][i],
          1e-6)
check_declared("PF4-008c floating-point diagnosis",
               "A hyperbolic tangent of twenty rounds to exactly one\n"
               "in double precision", CAMPAIGN)
check_declared("PF4-008 reciprocal-fit error",
               "a fitting helper that regresses against the reciprocal "
               "of the adiabaticity rather", CAMPAIGN)
write("pf4_008c_gud.dat", "L slope",
      [(a08c["measured"]["cells"][k]["L"],
        a08c["measured"]["cells"][k]["slope_vs_kappa"])
       for k in ("gudermann_L1.5", "gudermann_L2.5", "gudermann_L3.5")])
write("pf4_008c_sech2.dat", "L slope",
      [(a08c["measured"]["cells"][k]["L"],
        a08c["measured"]["cells"][k]["slope_vs_kappa"])
       for k in ("sech2_L1.5", "sech2_L2.5", "sech2_L3.5")])

p409 = load("prereg-pf4-009.json")
m409 = p409["measured"]
check_exact("PF4-009 verdict", p409["verdict"]["value"], "PASS")
check_exact("PF4-009 item count", len(p409["items"]), 8)
for key, val in p409["items"].items():
    check_true(f"PF4-009 item {key}", val)
check_exact("PF4-009 declared universality bar",
            p409["declared"]["bars"]["universality"], 0.02)
check_exact("PF4-009 declared conservation bar",
            p409["declared"]["bars"]["hamiltonian"], 1e-11)
check_exact("PF4-009 declared entry bar",
            p409["declared"]["bars"]["entry"], 1e-7)
check_exact("PF4-009 declared fit-quality bar",
            p409["declared"]["bars"]["r_squared"], 0.995)
check_exact("PF4-009 declared widths", p409["declared"]["L_grid"],
            [1.8, 2.8, 3.8, 4.6])
check_exact("PF4-009 declared adiabaticities",
            len(p409["declared"]["kappa_grid"]), 6)
check("PF4-009 width ratio", 4.6 / 1.8, 2.56, 5e-3)
slopes409 = m409["gudermann_slopes"]
for i, typed in enumerate([-1.929735, -1.924383, -1.916823,
                           -1.909268]):
    check(f"PF4-009 sealed exponent {i}", slopes409[i], typed, 5e-7)
check("PF4-009 spread percent", pct(m409["gudermann_relative_spread"]),
      1.07, 5e-3)
check("PF4-009 figure mean line", m409["gudermann_mean_slope"],
      -1.9200522391689598, 0.0)
worst_r2 = min(c["r_squared"] for c in m409["cells"].values())
assert worst_r2 >= 0.9989, \
    "a sealed cell's coefficient of determination is below 0.9989"
CHECKS += 1
check("PF4-009 worst fit quality", worst_r2, 0.9989, 5e-5)
check("PF4-009 worst conservation drift",
      m409["worst_hamiltonian_drift"], 3.7e-13, 5e-15)
check("PF4-009 entry-point independence", m409["entry_relative_change"],
      9.2e-9, 5e-11)
write("pf4_009_sealed.dat", "L slope",
      sorted((c["L"], c["slope_vs_kappa"])
             for c in m409["cells"].values()))
check_exact("PF4-009 seal ledger entry",
            "| PREREG-PF4-009 | experiments/PREREG-PF4-009.md" in SEALS,
            True)
check_declared("PF4-009 non-claims",
               "The observable is the per-crossing transfer and not an "
               "event rate.", PREREG["PF4-009"])
check_declared("PF4-009 non-claim on quantum field theory",
               "Nothing in this registration is a claim about\nquantum "
               "field theory or about any physical process.",
               PREREG["PF4-009"])

# ---------------------------------------------------------------
# Section X. The standing rule and the nine seals.
# ---------------------------------------------------------------
check_declared("standing rule, unconditional form",
               "any arm of any\nexperiment must have a committed probe "
               "showing it contains the", CEILING)
check_declared("standing rule, gate form",
               "every gate registration\nmust cite a committed probe "
               "that verifies event presence for every\nbound cell and "
               "member", PREREG["PF6-002"])
sealed_rows = [line for line in SEALS.splitlines()
               if line.startswith("| PF0-FREEZE-001")
               or line.startswith("| PREREG-PF4-")
               or line.startswith("| PREREG-PF5-")
               or line.startswith("| PREREG-PF6-")]
check_exact("nine sealed documents in this arc", len(sealed_rows), 9)

print(f"all figure data written, {CHECKS} paper values bound "
      f"to committed records and declarations")
