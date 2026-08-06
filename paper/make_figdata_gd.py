#!/usr/bin/env python3
"""Generate pgfplots data tables for the games-decisions paper.

Every number is read from a committed evidence record in results/.
Pure standard library, no numpy, no free parameters. Output tables
land in paper/figdata/. Consistency assertions bind the emitted
tables to the sealed records they come from.
"""
from __future__ import annotations

import json
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


# Figure D1: GD-1 ensemble classification and the wedge subsets.
gd1 = load("gd1-flip-blackwell.json")
c = gd1["G3"]["counts"]
assert c["comparable"] + c["incomparable"] + c["ambiguous"] \
    == gd1["G3"]["ensemble"], "GD-1 classes do not partition"
assert c["wedge_comparable"] == 0, "G3 bar violated in record"
assert c["unanimous_incomparable"] == c["wedge_incomparable"], \
    "unanimous and reversal counts differ in record"
write("gd1_counts.dat", "idx count",
      [(1, c["comparable"]), (2, c["incomparable"]),
       (3, c["ambiguous"]), (4, c["unanimous_incomparable"]),
       (5, c["wedge_incomparable"])])

# Figure D2a: GD-2b stake-game value ladder, task-optimal versus
# best fidelity-optimal read at every cell budget.
gd2b = load("gd2b-budget-flip-game.json")
per = gd2b["exhibit"]["per_budget"]
for key, declared in gd2b["exhibit"]["closed_forms"].items():
    assert abs(declared["measured"] - declared["declared"]) <= 1e-12, \
        f"closed form {key} off in record"
write("gd2b_ladder.dat", "k vtask vfid",
      [(k, per[str(k)]["v_task"], per[str(k)]["v_fid_best"])
       for k in range(1, 7)])

# Figure D2b: GD-2b ensemble flip magnitudes at budgets 2 and 3.
ens = gd2b["ensemble"]
write("gd2b_ensemble.dat", "k count fraction median maxflip",
      [(k, ens[str(k)]["flip_count"], ens[str(k)]["flip_fraction"],
        ens[str(k)]["flip_median_over_flips"], ens[str(k)]["flip_max"])
       for k in (2, 3)])

# Figure D3: GD-3 P2 weighting curve at sigma 1.0, symmetric and
# shifted environments, from the committed auxiliary curve artifact,
# which is bound by hash to the sealed GD-3 record.
curve = load("gd3-figdata-curve.json")
gd3 = load("gd3-prospect-signatures.json")
assert curve["parent_sha256"] == gd3["record_sha256"], \
    "curve artifact does not match the sealed GD-3 record"
write("gd3_wcurve.dat", "p wsym wshift",
      [(p, ws, wsh) for p, ws, wsh in curve["points"]])

# Figure D4: GD-5 attention complementarity, player one equilibrium
# information against the opponent's budget ladder.
gd5 = load("gd5-budgeted-equilibrium.json")
lads = gd5["part2"]["complementarity_l2_ladder"]
i1s = gd5["part2"]["complementarity_I1"]
assert all(i1s[i + 1] <= i1s[i] + 1e-10 for i in range(len(i1s) - 1)), \
    "complementarity not monotone in record"
write("gd5_complement.dat", "lam2 I1",
      list(zip(lads, i1s)))

# Table cross-checks, emitted so every typed table traces to a
# generated file. GD-5 part-one ladder.
p1 = gd5["part1"]["results"]
write("gd5_ri_ladder.dat", "lam psafe value info",
      [(lam, p1[key]["p0"][0], p1[key]["value"],
        p1[key]["info_nats"])
       for lam, key in ((1e-6, "1e-06"), (0.05, "0.05"),
                        (0.2, "0.2"), (1.0, "1.0"), (5.0, "5.0"))])

# GD-4 valuations at sigma 2.5, one row per battery gamble.
gd4 = load("gd4-reference-functionals.json")
v25 = gd4["valuations"]["2.5"]
mus = gd4["gamble_means"]
write("gd4_val25.dat", "idx mean O1 O2 O3 O4",
      [(i + 1, mus[n], v25[n]["O1"], v25[n]["O2"], v25[n]["O3"],
        v25[n]["O4"])
       for i, n in enumerate(["B1", "B2", "B3", "B4", "B5", "B6"])])
