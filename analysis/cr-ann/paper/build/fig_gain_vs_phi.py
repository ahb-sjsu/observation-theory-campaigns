#!/usr/bin/env python3
"""Figure 1: graded mean gain vs the cross-fit retrieval potential Phi,
13 units of both sealed families, fold-SD error bars. Reads the committed
records only (prereg/conversion_pm.json). Serif, 300 dpi, marker shape
encodes family (accessibility rule: never color alone)."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.join(HERE, "..", "..", "prereg", "conversion_pm.json")

j = json.load(open(REC))
units = j["units"]

plt.rcParams.update({"font.family": "serif", "font.size": 9})
fig, ax = plt.subplots(figsize=(3.5, 3.0), dpi=300)

for name, r in units.items():
    fam = r["family"]
    m = "o" if fam == "V1" else "s"
    ax.errorbar(r["pred_xfit"], r["measured_gain"], xerr=r["pred_xfit_sd"],
                fmt=m, ms=4, capsize=2, lw=0.8,
                color="#444444" if fam == "V1" else "#1a6b9a",
                mfc="white" if r["arm"] == "excluded" else None)
    if abs(r["measured_gain"]) > 0.05 or abs(r["pred_xfit"]) > 0.1:
        ax.annotate(name.replace("_", " ").replace("-", " "),
                    (r["pred_xfit"], r["measured_gain"]),
                    textcoords="offset points", xytext=(4, 3), fontsize=6.5)

lo, hi = -0.06, 0.32
ax.plot([lo, hi], [lo, hi], ls="--", lw=0.8, color="#999999", zorder=0)
ax.axhline(0, lw=0.5, color="#bbbbbb", zorder=0)
ax.axvline(0, lw=0.5, color="#bbbbbb", zorder=0)
ax.set_xlabel(r"cross-fit retrieval potential $\Phi$")
ax.set_ylabel("graded mean gain (three seeds)")
ax.set_xlim(lo, hi)
ax.set_ylim(lo, hi)
from matplotlib.lines import Line2D
ax.legend(handles=[
    Line2D([], [], marker="o", ls="", color="#444444", ms=4, label="family V1"),
    Line2D([], [], marker="s", ls="", color="#1a6b9a", ms=4, label="family V2"),
    Line2D([], [], marker="s", ls="", color="#1a6b9a", mfc="white", ms=4,
           label="excluded (descriptive)"),
    Line2D([], [], ls="--", color="#999999", label="gain = $\\Phi$"),
], fontsize=6.5, loc="upper left", frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_gain_vs_phi.pdf"))
fig.savefig(os.path.join(HERE, "fig_gain_vs_phi.png"))
print("wrote fig_gain_vs_phi.{pdf,png}")
