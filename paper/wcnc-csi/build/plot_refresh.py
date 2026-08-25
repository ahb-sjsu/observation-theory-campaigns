"""WCNC Fig. 2: the CSI certificate's refresh horizon (OT-14). Reads the SEALED
CSI-refreshfloor sweep. (a) BLER vs report period across Doppler -- the certificate
ages, faster at higher mobility. (b) the refresh floor is proportional to the Clarke
coherence time: floor ~ 0.177*Tcoh (R^2=0.915); at high Doppler it saturates at the
minimum report period (>=1 TTI). Marker shape, not colour."""
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DEF = os.path.join(HERE, "..", "..", "..", "analysis", "csi", "CSI-refreshfloor.json")
plt.rcParams.update({"font.size": 8.5, "font.family": "serif", "axes.grid": True,
                     "grid.alpha": 0.3, "savefig.dpi": 300, "savefig.bbox": "tight"})
MARK = {"25": "o", "100": "s", "400": "^"}


def main(inp=DEF, out=os.path.join(HERE, "refresh_floor.pdf")):
    d = json.load(open(inp))
    periods = np.array(d["periods_tti"], float)
    thr = d["threshold_bler"]
    grid = d["bler_grid"]
    floors = d["floors"]
    fit = d["fit"]
    slope, r2 = fit["floor_ms_per_tcoh_ms"], fit["r2"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.7))

    # (a) aging: BLER vs report period, selected Dopplers
    for fd in ("25", "100", "400"):
        ax1.plot(periods, grid[fd], marker=MARK[fd], ms=5, color="0.2", lw=1.1,
                 mfc="white", label=f"$f_D$={fd} Hz")
    ax1.axhline(thr, ls="--", color="0.45", lw=1.1)
    ax1.text(periods[-1], thr * 1.03, "target", ha="right", va="bottom", fontsize=7, color="0.4")
    ax1.set_xscale("log"); ax1.set_xlabel("CSI report period (TTI)")
    ax1.set_ylabel("BLER"); ax1.set_title("(a) the certificate ages", fontsize=9)
    ax1.legend(fontsize=7, loc="upper left")

    # (b) the OT-14 law: floor vs coherence time
    fds = sorted(floors, key=lambda k: int(k))
    tcoh = np.array([floors[fd]["tcoh_ms"] for fd in fds])
    fl = np.array([floors[fd]["floor_tti"] for fd in fds])
    ax2.scatter(tcoh, fl, marker="D", s=40, color="0.15", zorder=3, label="measured floor")
    xs = np.linspace(0, tcoh.max() * 1.05, 50)
    ax2.plot(xs, slope * xs, ls="-", color="0.45", lw=1.3,
             label=f"OT-14: {slope:.3f}$\\,T_{{coh}}$")
    ax2.axhline(1.0, ls=":", color="0.6", lw=1.0)
    ax2.text(tcoh.max(), 1.05, "min period (1 TTI)", ha="right", va="bottom",
             fontsize=6.8, color="0.5")
    ax2.set_xlabel("coherence time $T_{coh}=0.423/f_D$ (ms)")
    ax2.set_ylabel("refresh floor (TTI)")
    ax2.set_title(f"(b) floor $\\propto T_{{coh}}$  ($R^2$={r2:.2f})", fontsize=9)
    ax2.legend(fontsize=7, loc="upper left")

    fig.tight_layout()
    fig.savefig(out); fig.savefig(os.path.splitext(out)[0] + ".png")
    print(f"OT-14 floor ~ {slope:.3f}*Tcoh (R2={r2:.3f}); floors(tti)={list(fl)} -> {out}",
          flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
