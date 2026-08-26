"""Fig. 1 for the OFC XPROTO-QOT paper: (a) naive vs footprint-aware false-clear;
(b) per-lightpath false-clear over (spectral position, reach). Reads the
per-lightpath records emitted by `fam_qot.py --paths-out` and writes a PDF.
Marker SHAPE distinguishes classes (Optica: colour alone is not enough).

    python plot_fig1.py QOT-paths.json ../../paper/ofc-qot/fc_footprint.pdf
"""
import json
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
mpl.rcParams.update({"font.size": 11, "axes.titlesize": 11, "legend.fontsize": 10})
import matplotlib.pyplot as plt  # noqa: E402


def main(paths_json="QOT-paths.json", out_pdf="fc_footprint.pdf"):
    recs = json.load(open(paths_json))["records"]
    naive = np.array([r["naive_fail"] for r in recs], bool)
    aware = np.array([r["aware_fail"] for r in recs], bool)
    pos = np.array([r["position"] for r in recs], float)
    reach = np.array([r["reach"] for r in recs], float)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.9))

    # (a) false-clear rate: naive vs footprint-aware
    ax1.bar([0, 1], [naive.mean(), aware.mean()], width=0.6,
            color=["0.35", "0.75"], hatch=["//", ".."], edgecolor="k")
    ax1.set_xticks([0, 1]); ax1.set_xticklabels(["naive", "footprint-\naware"])
    ax1.set_ylabel("false-clear rate"); ax1.set_ylim(0, max(0.6, naive.mean() * 1.2))
    ax1.set_title("(a) certificate false-clear")

    # (b) per-lightpath footprint: cleared (open o) vs false-clear (x)
    ok = ~naive
    ax2.scatter(pos[ok], reach[ok], marker="o", facecolors="none",
                edgecolors="0.55", s=22, linewidths=0.8, label="cleared")
    ax2.scatter(pos[naive], reach[naive], marker="x", color="k", s=34,
                linewidths=1.3, label="false-clear")
    ax2.set_xlabel("spectral position"); ax2.set_ylabel("reach (80-km spans)")
    ax2.set_title("(b) footprint concentration"); ax2.legend(frameon=False, fontsize=10)

    fig.tight_layout()
    fig.savefig(out_pdf)
    print(f"naive FC={naive.mean():.3f}  aware FC={aware.mean():.3f}  n={len(recs)} -> {out_pdf}")


if __name__ == "__main__":
    main(*sys.argv[1:])
