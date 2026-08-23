#!/usr/bin/env python3
"""Evaluate the sealed PREREG-DB3-001 gates on the governed run."""
import json

import numpy as np

r = json.load(open("/home/claude/db3_results/db3_governed_20261225.json"))
log = r["log"]
arms = list(log.keys())
w = {a: sum(ep["epoch_ms"] for ep in log[a]) for a in arms}
fresh = w["fresh"]
R = {a: (w[a] - fresh) / fresh for a in arms}

spreads = []
for a in arms:
    for ep in log[a]:
        for q, rec in ep["queries"].items():
            raw = np.array(rec["raw"])
            med = np.median(raw)
            spreads.append(np.median(np.abs(raw - med)) / med)
spreads = np.array(spreads)
n_cells = len(spreads)
crn = all(log[a][e]["modes"] == log[arms[0]][e]["modes"]
          for a in arms[1:] for e in range(len(log[arms[0]])))
d = log["directional"]
probe = np.mean([ep["probe_ms"] for ep in d])
ana = np.mean([ep["analyze_ms"] for ep in d if ep["analyze_ms"] > 0])

for a in arms:
    print(f"W({a}) = {w[a]:.0f} ms   R = {R[a]:+.4f}")
print()
gates = {
    "S1  R(none) >= 0.08": R["none"] >= 0.08,
    "S2  W(dir) < W(churn)": w["directional"] < w["churn"],
    "S2b W(dir) < W(churn2)": w["directional"] < w["churn2"],
    "S3  W(dir) < min(age, random)": w["directional"] < min(w["age"],
                                                            w["random"]),
    "S4  probe/analyze <= 0.8": probe / ana <= 0.8,
    "S5  spread mean<=0.08 & p95<=0.20": (spreads.mean() <= 0.08 and
        np.percentile(spreads, 95) <= 0.20),
    "S6  2730 cells + CRN": n_cells == 2730 and crn,
}
for g, v in gates.items():
    print(f"{g}: {'PASS' if v else 'FAIL'}")
print(f"\ndetail: probe/analyze={probe/ana:.3f} spread_mean="
      f"{spreads.mean():.4f} p95={np.percentile(spreads,95):.4f} "
      f"cells={n_cells} crn={crn} wall_s={r['wall_s']:.0f}")
