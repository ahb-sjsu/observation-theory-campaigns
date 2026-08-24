"""5G/6G NTN (non-terrestrial): CSI feedback under extreme Doppler + long delay.

Bridges the cellular CSI-aging wing to the space-comms crucibles (SC-1/SC-2).
Two forces make CSI-based closed-loop adaptation fail over satellite links:

  1. Doppler collapses the coherence time (Tcoh = 0.423/fd). The OT-14 refresh
     floor -- the max report period holding false-clear at target -- scales as
     floor ~ K * Tcoh (K = 0.177 measured terrestrially in csi_sweep.py). At NTN
     residual Doppler (post pre-compensation, ~kHz) the floor is sub-TTI.
  2. The propagation round-trip delay (RTT) means the CSI report is already old
     when the decision using it is transmitted. If RTT exceeds Tcoh, the report
     is *stale on arrival* -- the feedback loop is longer than the channel's
     memory -- and no report period, however short, helps.

Unifying condition: **CSI feedback is viable iff RTT < Tcoh** (the loop closes
within a coherence time). This is the delay-decorrelation limit (SC-2 / the
observation-age -> infinity face of the taxonomy) at the air interface.

Analytical (uses the measured refresh-floor constant + orbital RTT physics); the
terrestrial floor law itself is the sealed/measured XPROTO-CSI result. Emits
CSI-NTN.json + CSI-NTN.png. Runs locally.
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
K_FLOOR = 0.177              # measured refresh-floor slope (floor = K * Tcoh)


def tcoh_ms(fd_hz):
    return 0.423 / fd_hz * 1000.0


# (name, effective/residual Doppler Hz, one-way-then-doubled service RTT ms, note)
SCENARIOS = [
    ("Terrestrial pedestrian", 10,   1,   "urban, 3 km/h"),
    ("Terrestrial vehicular",  200,  1,   "~100 km/h @3.5 GHz"),
    ("Terrestrial HSR",        1000, 2,   "high-speed rail, residual Doppler"),
    ("LEO regenerative",       1000, 7,   "550 km, on-board gNB, post pre-comp"),
    ("LEO bent-pipe",          1000, 30,  "550 km via ground gateway"),
    ("MEO",                    300,  100, "~8000 km"),
    ("GEO",                    80,   270, "35786 km, bent-pipe"),
]


def main():
    rows = []
    for name, fd, rtt, note in SCENARIOS:
        tc = tcoh_ms(fd)
        floor = K_FLOOR * tc
        ratio = rtt / tc
        rows.append({"scenario": name, "fd_hz": fd, "tcoh_ms": round(tc, 3),
                     "refresh_floor_ms": round(floor, 3), "rtt_ms": rtt,
                     "rtt_over_tcoh": round(ratio, 2),
                     "csi_feedback_viable": bool(rtt < tc), "note": note})
        print(f"{name:24s} fd={fd:5d}Hz Tcoh={tc:7.2f}ms floor={floor:6.3f}ms "
              f"RTT={rtt:4d}ms  RTT/Tcoh={ratio:6.2f}  "
              f"{'VIABLE' if rtt < tc else 'STALE-ON-ARRIVAL'}")

    fig, ax = plt.subplots(figsize=(7, 5))
    for r in rows:
        viable = r["csi_feedback_viable"]
        ax.scatter(r["tcoh_ms"], r["rtt_ms"], s=90,
                   c=("#2ca02c" if viable else "#d62728"),
                   edgecolors="k", zorder=3)
        ax.annotate(r["scenario"], (r["tcoh_ms"], r["rtt_ms"]),
                    textcoords="offset points", xytext=(7, 4), fontsize=8)
    lim = np.array([0.05, 500])
    ax.plot(lim, lim, "k--", lw=1, label="RTT = Tcoh (viability boundary)")
    ax.fill_between(lim, lim, 500, color="#d62728", alpha=0.06)
    ax.fill_between(lim, 0.01, lim, color="#2ca02c", alpha=0.06)
    ax.text(30, 0.2, "CSI feedback VIABLE\n(loop closes within Tcoh)",
            color="#2ca02c", fontsize=8, ha="center")
    ax.text(0.5, 120, "STALE ON ARRIVAL\n(RTT > Tcoh)",
            color="#d62728", fontsize=8, ha="center")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(0.05, 500); ax.set_ylim(0.3, 400)
    ax.set_xlabel("coherence time  Tcoh = 0.423/fd  (ms)")
    ax.set_ylabel("feedback round-trip delay  RTT  (ms)")
    ax.set_title("NTN CSI feedback: viable iff RTT < Tcoh\n"
                 "(the delay-decorrelation limit at the air interface)")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "CSI-NTN.png"), dpi=120)

    json.dump({"k_floor": K_FLOOR, "condition": "CSI feedback viable iff RTT < Tcoh",
               "scenarios": rows}, open(os.path.join(HERE, "CSI-NTN.json"), "w"), indent=1)
    print("\nwrote CSI-NTN.json + CSI-NTN.png")


if __name__ == "__main__":
    main()
