"""Fig 3 for the WCNC paper: the age horizon at the true 0.10 budget.

    python plot_age.py CSISWEEP2REP-family.json ../../paper/wcnc-csi/build/age_horizon

Emits <out>.pdf and <out>.png. Panel (a): held-CSI BLER against report period
(seed 0, all Dopplers) with the 0.10 budget line. Panel (b): the measured
horizon P* per Doppler (all seeds, marker per seed) against the superseded
0.15-threshold exploration law 0.177*Tcoh, which the calibrated recompute kills.
Line styles + markers, not colour alone.
"""
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rec = json.load(open(sys.argv[1], encoding="utf-8"))
out = sys.argv[2]
periods = rec["constants"]["periods"]
fds = rec["constants"]["fds"]
cells = rec["cells"]

plt.rcParams.update({"font.size": 8.5, "axes.labelsize": 9,
                     "legend.fontsize": 7.2, "pdf.fonttype": 42})
fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.1, 2.55))

# (a) BLER vs report period, seed 0
styles = [("o", "-"), ("s", "--"), ("^", "-."), ("v", ":"), ("D", "-"), ("x", "--")]
rows = cells[0]["bler_rows"]
for (fd, (mk, ls)) in zip(fds, styles):
    ax.plot(periods, rows[str(fd)], marker=mk, ls=ls, ms=3.5, lw=1.0,
            label=f"{fd} Hz")
ax.axhline(0.10, color="k", lw=1.4)
ax.text(1.05, 0.104, "0.10 budget", fontsize=7.2)
ax.set_xscale("log", base=2)
ax.set_xticks(periods)
ax.set_xticklabels([str(p) for p in periods])
ax.set_xlabel("report period $P$ (TTI)")
ax.set_ylabel(r"held-CSI BLER $\widehat{B}$")
ax.legend(ncol=2, title="Doppler", frameon=False, title_fontsize=7.2)
ax.set_title(f"(a) aging past the budget (seed {cells[0]['seed']})", fontsize=9)

# (b) the horizon vs Doppler, against the dead exploration law
law_fds = [f for f in fds]
law = [0.177 * 0.423 / f * 1000.0 for f in law_fds]   # TTI (1 ms)
bx.plot(law_fds, law, "k--", lw=1.2,
        label=r"$0.18\,T_{\mathrm{coh}}$ (0.15-thr. exploration)")
seed_mk = ["o", "s", "^"]
jit = [0.94, 1.0, 1.064]          # nudge x so identical floors stay visible
for c, mk, j in zip(cells, seed_mk, jit):
    xs = [f * j for f in fds if str(f) in c["floors_tti"]]
    ys = [c["floors_tti"][str(f)] for f in fds if str(f) in c["floors_tti"]]
    bx.plot(xs, ys, marker=mk, ls="-", ms=4, lw=0.9,
            label=f"measured, seed {c['seed']}")
bx.set_xscale("log")
bx.set_xticks(fds)
bx.set_xticklabels([str(f) for f in fds])
bx.set_xlabel("Doppler $f_D$ (Hz)")
bx.set_ylabel(r"age horizon $P^\star$ (TTI)")
bx.set_ylim(0, 8.5)
bx.legend(frameon=False)
bx.set_title("(b) the horizon collapses at 0.10", fontsize=9)

fig.tight_layout(pad=0.4)
fig.savefig(out + ".pdf")
fig.savefig(out + ".png", dpi=300)
print(f"wrote {out}.pdf/.png")
