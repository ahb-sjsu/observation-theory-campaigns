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
