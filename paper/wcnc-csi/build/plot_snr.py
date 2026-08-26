"""WCNC Fig. 3: SNR-robustness of the reliability-target relativity. Reads the SEALED
XPROTO-URLLC-SNR graded record (3 seeds x 7 mean SNRs). BLER vs mean SNR for
eMBB/URLLC-naive (identical), and URLLC-aware; both targets as lines. Log-y; marker
shape distinguishes policies; whiskers = min/max over seeds."""
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DEF = os.path.join(HERE, "..", "..", "..", "analysis", "urllc", "URLLCSNRREP-graded-raw.json")
plt.rcParams.update({"font.size": 8.5, "font.family": "serif", "axes.grid": True,
                     "grid.alpha": 0.3, "savefig.dpi": 300, "savefig.bbox": "tight"})
FLOOR = 1e-6


def main(inp=DEF, out=os.path.join(HERE, "snr_robustness.pdf")):
    d = json.load(open(inp))
    cells = d["cells"]
    snrs = cells[0]["snr_grid_db"]
    et = cells[0]["embb_target"]; ut = cells[0]["urllc_target"]

    def series(key):
        m, lo, hi = [], [], []
        for M in snrs:
            v = np.array([max(c["sweep"][str(M)][key], FLOOR) for c in cells])
            m.append(v.mean()); lo.append(v.mean() - v.min()); hi.append(v.max() - v.mean())
        return np.array(m), np.array(lo), np.array(hi)

    un, unlo, unhi = series("urllc_naive")     # == embb series (same certificate)
    ua, ualo, uahi = series("urllc_aware")

    fig, ax = plt.subplots(figsize=(3.5, 2.8))
    ax.errorbar(snrs, un, yerr=[unlo, unhi], fmt="s-", ms=5, color="0.2", lw=1.2,
                mfc="white", capsize=2.5, label="naive (eMBB = URLLC read)")
    ax.errorbar(snrs, ua, yerr=[ualo, uahi], fmt="o-", ms=5, color="0.45", lw=1.2,
                capsize=2.5, label="URLLC target-aware")
    ax.axhline(et, ls="--", color="0.25", lw=1.0)
    ax.axhline(ut, ls=":", color="0.25", lw=1.0)
    ax.text(20.8, et * 1.2, "eMBB target", ha="right", va="bottom", fontsize=7)
    ax.text(20.8, ut * 1.2, "URLLC target", ha="right", va="bottom", fontsize=7)
    ax.axvspan(2.5, 7.5, color="0.9", zorder=0)
    ax.text(5, 2.2e-6, "cell edge:\neMBB budget\nlost", ha="center", fontsize=6.8, color="0.35")
    ax.set_yscale("log"); ax.set_ylim(1e-6, 1.0)
    ax.set_xlabel("mean SNR (dB)"); ax.set_ylabel("achieved BLER")
    ax.legend(fontsize=7, loc="center right", framealpha=0.95)
    fig.tight_layout()
    fig.savefig(out); fig.savefig(os.path.splitext(out)[0] + ".png")
    print(f"naive at 9-18 dB: {un[2]:.3f}-{un[5]:.3f} (vs URLLC 1e-3); "
          f"cell edge 3 dB: {un[0]:.3f} (vs eMBB 1e-1) -> {out}", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
