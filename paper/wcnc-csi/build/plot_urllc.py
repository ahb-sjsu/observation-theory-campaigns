"""WCNC Fig. 1: consumer-relativity of the CSI certificate in the reliability target.
Reads the SEALED XPROTO-URLLC graded record (3 seeds). The identical CSI-derived MCS
that meets the eMBB target (BLER 0.1) misses the URLLC target (0.001) by ~110x; a
target-aware policy meets it. Bar, log-y, means +/- std. Marker/hatch, not colour."""
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DEF = os.path.join(HERE, "..", "..", "..", "analysis", "urllc", "XPROTO-URLLC-graded.json")
plt.rcParams.update({"font.size": 8.5, "font.family": "serif", "axes.grid": True,
                     "grid.alpha": 0.3, "savefig.dpi": 300, "savefig.bbox": "tight"})
FLOOR = 1e-5


def _ms(cells, k):
    v = np.array([c[k] for c in cells], float)
    return v.mean(), v.std()


def main(inp=DEF, out=os.path.join(HERE, "urllc_relativity.pdf")):
    d = json.load(open(inp))
    cells = d["cells"]
    et = cells[0]["embb_target"]; ut = cells[0]["urllc_target"]
    embb, embb_s = _ms(cells, "achieved_embb")
    un, un_s = _ms(cells, "achieved_urllc_naive")
    aw, aw_s = _ms(cells, "achieved_urllc_aware")
    aw = max(aw, FLOOR)

    fig, ax = plt.subplots(figsize=(3.4, 2.7))
    x = np.arange(3)
    vals = [embb, un, aw]
    errs = [embb_s, un_s, 0]
    bars = ax.bar(x, vals, 0.62, yerr=errs, capsize=3,
                  color=["0.45", "0.3", "0.75"], hatch=["", "xx", ".."], edgecolor="k")
    ax.set_yscale("log")
    ax.set_ylim(5e-6, 1.0)
    ax.axhline(et, ls="--", color="0.25", lw=1.1)
    ax.axhline(ut, ls=":", color="0.25", lw=1.1)
    ax.text(2.4, et * 1.15, "eMBB target $10^{-1}$", ha="right", va="bottom", fontsize=7)
    ax.text(2.4, ut * 1.15, "URLLC target $10^{-3}$", ha="right", va="bottom", fontsize=7)
    ax.set_xticks(x)
    ax.set_xticklabels(["eMBB\n(naive)", "URLLC\n(naive)", "URLLC\n(aware)"])
    ax.set_ylabel("achieved BLER")
    # annotate the 110x miss
    ax.annotate(f"${un/ut:.0f}\\times$ over\ntarget", (1, un), (1.02, un * 3.0),
                fontsize=7.5, ha="center", color="0.1",
                arrowprops=dict(arrowstyle="->", color="0.4", lw=0.8))
    fig.tight_layout()
    fig.savefig(out); fig.savefig(os.path.splitext(out)[0] + ".png")
    print(f"eMBB {embb:.4f} | URLLC-naive {un:.4f} ({un/ut:.0f}x over) | "
          f"URLLC-aware {aw:.2e} -> {out}", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
