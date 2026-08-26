"""The OFC paper's headline figure: the measured freshness curve and its
dependence on the sync baseline N0 (QOT-sweep2.json, deterministic single-add
sweep).

    python plot_freshness.py QOT-sweep2.json ../../paper/ofc-qot/freshness_curve.pdf

False-clear against channels added since sync, one curve per sync baseline,
the 5% target line, and the nine-add boundary of the sparse-sync case. Marker
shape + line style distinguish baselines (Optica accessibility rule).
"""
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rec = json.load(open(sys.argv[1], encoding="utf-8"))
out = sys.argv[2] if len(sys.argv) > 2 else "freshness_curve.pdf"
plt.rcParams.update({"font.size": 10, "legend.fontsize": 8.5, "pdf.fonttype": 42})

fig, ax = plt.subplots(figsize=(5.4, 2.9))
styles = {"6": ("o", "-", "0.1"), "20": ("s", "--", "0.35"),
          "40": ("^", "-.", "0.55"), "60": ("v", ":", "0.7")}
for n0, (mk, ls, col) in styles.items():
    b = rec["baselines"][n0]
    dns = sorted(int(k) for k in b["fc_curve"])
    ys = [b["fc_curve"][str(d)] for d in dns]
    ax.plot(dns, ys, marker=mk, ls=ls, color=col, ms=3.2, lw=1.1,
            label=f"synced at $N_0={n0}$ ch")
ax.axhline(rec["target_fc"], color="k", lw=1.2)
ax.text(69.5, rec["target_fc"] * 1.25, "5% target", ha="right", fontsize=8)
ax.axvline(9, color="0.2", lw=0.9, ls=(0, (2, 2)))
ax.text(9.6, 0.44, "9 adds:\nsparse-sync\nboundary", fontsize=7.5, color="0.25")
ax.set_xlabel(r"channels added since sync $\Delta N$")
ax.set_ylabel("false-clear rate")
ax.set_xlim(0, 71)
ax.set_ylim(-0.015, 0.55)
ax.legend(frameon=False, loc="center right")
fig.tight_layout(pad=0.4)
fig.savefig(out)
fig.savefig(out.rsplit(".", 1)[0] + ".png", dpi=300)
print(f"wrote {out} (+.png)")
