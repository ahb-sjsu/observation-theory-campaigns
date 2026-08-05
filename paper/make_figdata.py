#!/usr/bin/env python3
"""Generate pgfplots data tables for both paper drafts.

Every number is read from a committed evidence record in results/ or
recomputed deterministically from committed instrument code. No free
parameters. Output tables land in paper/figdata/.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "figdata"
OUT.mkdir(exist_ok=True)

sys.path.insert(0, str(ROOT / "python"))
from projection_fold import binned_fold_entropy  # noqa: E402


def write(name: str, header: str, rows) -> None:
    lines = [header] + [" ".join(f"{v:.10g}" for v in row) for row in rows]
    (OUT / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{name}: {len(lines) - 1} rows")


# Figure E1: PE-2 part A staircase (level, multiplicity, entropy, signed).
pe2 = json.loads((ROOT / "results" / "pe2-cycle.json").read_text())
a = pe2["part_a_observation_axis"]
write(
    "pe2_staircase.dat",
    "level multiplicity entropy signed",
    zip(a["levels"], a["multiplicity"], a["branch_entropy_bits"],
        a["signed_count"], strict=True),
)

# Figure E2: PE-1 caustic convergence, recomputed from the sealed instrument.
limit = 1.0 - 1.0 / math.log(2.0)
rows = []
for eps in (1e-4, 1e-5, 1e-6):
    deviation = abs(binned_fold_entropy(eps) + math.log2(eps) - limit)
    rows.append((eps, deviation))
write("pe1_convergence.dat", "eps deviation", rows)

# Figure E3: PE-2 part B forward and reversed entropy curves, every 5th point.
b = pe2["part_b_reversible_ensemble"]
tau = b["snapshot_tau"]
fwd = b["forward_entropy_bits"]
rev = b["reverse_entropy_bits"]
n = len(tau)
keep = [i for i in range(n) if i % 5 == 0 or i == n - 1]
write(
    "pe2_cycle.dat",
    "tau forward reverse_reflected",
    [(tau[i], fwd[i], rev[n - 1 - i]) for i in keep],
)

# Figure Q1: QO-1 hierarchy chains at theta 0.8, both axes.
qo1 = json.loads((ROOT / "results" / "qo1-hierarchy.json").read_text())
levels = ["position_only", "position_plus_flux", "full_boundary", "full_state"]
za = qo1["quantum"]["hierarchies"]["z"]["0.8"]["chain"]
xa = qo1["quantum"]["hierarchies"]["x"]["0.8"]["chain"]
write(
    "qo1_hierarchy.dat",
    "index zchain xchain",
    [(i + 1, za[lv], xa[lv]) for i, lv in enumerate(levels)],
)

# Figure Q2: QO-2 flip, held-out distortions by budget and arm.
qo2 = json.loads((ROOT / "results" / "qo2-flip.json").read_text())
rows = []
for entry in qo2["budgets"]:
    h = entry["held_out"]
    rows.append((
        entry["budget_qubits"],
        h["F"]["task_distortion"], h["F"]["infidelity"],
        h["T"]["task_distortion"], h["T"]["infidelity"],
        h["anti"]["task_distortion"],
    ))
write("qo2_flip.dat", "budget Ftask Finfid Ttask Tinfid antitask", rows)

# Figure C1: tdot_f versus ge under the two prescriptions (Cayley pole
# versus continuous exponential), recomputed from the committed PF-3 code.
from shp_land2016 import final_velocity, tdot_final  # noqa: E402

V_REF, RHAT_REF = 0.4, (0.8, 0.6)
TDOT_IN = 1.0 / math.sqrt(1.0 - V_REF**2)
W_IN = V_REF * TDOT_IN * RHAT_REF[0]
C2 = (TDOT_IN + 1.0) ** 2 - W_IN**2

rows = []
ge = 0.0
while ge <= 6.0 + 1e-9:
    if abs(ge - 2.0) < 0.05:
        cayley = float("nan")
    else:
        cayley = tdot_final(TDOT_IN, V_REF, RHAT_REF[0], ge)
    continuous = ((TDOT_IN + 1.0) * math.cosh(ge)
                  - W_IN * math.sinh(ge)) - 1.0
    rows.append((ge, cayley, continuous))
    ge += 0.02
write("pf3_prescriptions.dat", "ge cayley continuous", rows)

# Figure C2: the invariant hyperbola in the (w, tdot+1) plane, the
# continuous path along the physical branch, and Cayley images crossing
# to the PT branch above the pole.
rows = []
for i in range(241):
    w = -3.0 + i * 0.025
    top = math.sqrt(C2 + w * w)
    rows.append((w, top, -top))
write("pf3_hyperbola.dat", "w upper lower", rows)

rows = []
for i in range(101):
    s = i / 100.0
    ge = 3.0
    tp = ((TDOT_IN + 1.0) * math.cosh(ge * s) - W_IN * math.sinh(ge * s))
    w = (W_IN * math.cosh(ge * s) - (TDOT_IN + 1.0) * math.sinh(ge * s))
    rows.append((w, tp))
write("pf3_flowpath.dat", "w tplus", rows)

rows = []
for ge in (0.0, 0.5, 1.0, 1.5, 1.9, 2.1, 3.0, 5.0):
    velocity = final_velocity(TDOT_IN, V_REF, RHAT_REF, ge)
    w_f = velocity[1] * RHAT_REF[0] + velocity[2] * RHAT_REF[1]
    invariant = (velocity[0] + 1.0) ** 2 - w_f**2
    assert abs(invariant - C2) < 1e-9, "Cayley left the invariant set"
    rows.append((ge, w_f, velocity[0] + 1.0))
write("pf3_cayley_points.dat", "ge w tplus", rows)

# Figures T1/T2: TB-1 ladder convergence and TB-2 flip persistence.
tb1 = json.loads((ROOT / "results" / "tb1-ladder.json").read_text())
rungs = tb1["rungs"]
ns = [r["N"] for r in rungs]
rows = []
for idx, r in enumerate(rungs):
    def sdiff(label):
        if idx == 0:
            return float("nan")
        return abs(r[label]["D"] - rungs[idx - 1][label]["D"])
    rows.append((r["N"], r["site"]["D"], r["pair"]["D"], r["half"]["D"],
                 sdiff("site"), sdiff("pair"), sdiff("half"),
                 r["half_entropy_vacuum"]))
write("tb1_ladder.dat",
      "N dsite dpair dhalf sdiff_site sdiff_pair sdiff_half shalf", rows)

tb2 = json.loads((ROOT / "results" / "tb2-flip-ladder.json").read_text())
rows = []
for r in tb2["rungs"]:
    b1 = r["budgets"]["1"]
    rows.append((r["N"], b1["F_task"] - b1["T_task"],
                 b1["T_infid"] - b1["F_infid"]))
write("tb2_flip.dat", "N taskgap infidgap", rows)

# Figures P1/P2: PF-4 governed cells with the G line, and the pilot's
# critical manifold.
rows = []
for run_id, fname in ((1, "prereg-pf4-001.json"), (2, "prereg-pf4-002.json")):
    rec = json.loads((ROOT / "results" / fname).read_text())
    for split in ("train_cells", "held_cells"):
        for c in rec[split]:
            if (c["count"] >= 5 and c["fraction"] < 0.9
                    and c["max_relative_energy_drift"] < 1e-4
                    and not c["deterministically_reversing"]):
                d = c["deterministic_pt_min"]
                rows.append((run_id, 0 if split == "train_cells" else 1,
                             c["P"], c["E"], d, (d / c["E"]) ** 2,
                             -math.log(c["fraction"])))
write("pf4_cells.dat", "run split P E d xg neglogf", rows)

rec2 = json.loads((ROOT / "results" / "prereg-pf4-002.json").read_text())
g = rec2["fits"]["model_G"]
rows = []
for i in range(40):
    x = 0.03 + (0.24 - 0.03) * i / 39.0
    rows.append((x, g["alpha"] + g["beta"] * x))
write("pf4_gline.dat", "xg pred", rows)

pilot = json.loads((ROOT / "results" / "pf4-pilot.json").read_text())
rows = []
for c in pilot["family_p2s"]["cells"]:
    rows.append((c["P"], c["E"], c["deterministic_pt_min"],
                 1 if c["deterministically_reversing"] else 0))
write("pf4_manifold.dat", "P E d regime", rows)

# Figure M1: PE-3 observed entropy curves, integrable versus chaotic
# dynamics, every 10th snapshot of the committed record.
pe3 = json.loads((ROOT / "results" / "pe3-mixing.json").read_text())
ci = pe3["results"]["integrable"]["entropy_curve_every_40"]
cc = pe3["results"]["chaotic"]["entropy_curve_every_40"]
n3 = len(ci)
tau_max = pe3["declared"]["tau_max"]
keep = [i for i in range(n3) if i % 10 == 0 or i == n3 - 1]
write(
    "pe3_curves.dat",
    "tau integrable chaotic",
    [(i * tau_max / (n3 - 1), ci[i], cc[i]) for i in keep],
)

# Figure M2: PE-4 recovery defects, retrace defect, and coarse mutual
# information across the coupling grid.
pe4 = json.loads((ROOT / "results" / "pe4-noise.json").read_text())
rows = []
for kappa in pe4["declared"]["kappas"]:
    entry = pe4["per_kappa"][f"{kappa:g}"]
    rows.append((kappa,
                 entry["recovery_defect_system_flip"],
                 entry["recovery_defect_full_flip"],
                 entry["entropy_retrace_defect_bits"],
                 entry["mutual_information_Z_Ebath_bits"]))
write("pe4_defects.dat", "kappa sysflip fullflip retrace mi", rows)

# Figure Q3: QO-3 joint survival versus family size, families A and B.
qo3 = json.loads((ROOT / "results" / "qo3-family.json").read_text())
strict = qo3["summary"]["strict"]
curve_a = strict["joint_survival_by_prefix_size"]
curve_b = strict["family_b_joint_survival_by_prefix_size"]
rows = []
for i in range(max(len(curve_a), len(curve_b))):
    rows.append((
        i + 1,
        curve_a[i] if i < len(curve_a) else float("nan"),
        curve_b[i] if i < len(curve_b) else float("nan"),
    ))
write("qo3_survival.dat", "familysize jointA jointB", rows)
# Figure G1: EG-1 area-gate counts, all five exact series versus R.
# Volume pairs and area pairs separate into slope-2 and slope-1 families.
eg1 = json.loads((ROOT / "results" / "eg1-area-gate.json").read_text())
r_grid = eg1["declared"]["R_grid"]
arm_b = eg1["arm_b"]
assert [row["R"] for row in arm_b] == r_grid, "arm B off the declared R grid"
arm_a_primary = eg1["arm_a"]["H_given_boundary"]
arm_b_primary = [row["H_given_boundary"] for row in arm_b]
arm_b_mi = [row["MI"] for row in arm_b]
arm_c_access = eg1["arm_c"]["accessible_image_bits"]
arm_c_hidden = eg1["arm_c"]["hidden_residual_bits"]
for i, r in enumerate(r_grid):
    assert arm_a_primary[i] == (r - 2) ** 2, "arm A closed form broken"
    assert arm_b_primary[i] == (r - 1) ** 2, "arm B closed form broken"
    assert arm_b_mi[i] == 4 * r - 5, "arm B MI closed form broken"
    assert arm_c_access[i] == 4 * r - 4, "arm C access closed form broken"
    assert arm_c_hidden[i] == (r - 2) ** 2, "arm C hidden closed form broken"
write(
    "eg1_counts.dat",
    "R armA_primary armB_primary armB_mi armC_access armC_hidden",
    zip(r_grid, arm_a_primary, arm_b_primary, arm_b_mi,
        arm_c_access, arm_c_hidden, strict=True),
)
