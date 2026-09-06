"""Figure 1 of the POSO paper.

(a) per-scan raw turboSETI narrowband hits over the six-scan ABACAD cadence of
HIP101027 (GBT L-band, MJD 57574, coarse channels 119-144); (b) the cadence
consumer: 6651 raw on-source hits collapse to 3 that survive the ON-OFF test,
a false-clear rate of 1 - 3/6651 = 0.99955.

Per-scan counts VERIFIED 2026-09-06 against the raw turbo_seti .dat outputs in
/archive/seti/data/cadence/dats (rows minus comment header), snr=10, max_drift=4:
  A HIP101027 2112 (ON) | B HIP100014 2190 (OFF) | A HIP101027 2239 (ON) |
  C HIP100244 2252 (OFF) | A HIP101027 2300 (ON) | D HIP100325 2325 (OFF).
ON total 2112+2239+2300 = 6651 (cadence_result.json total_on_hits); 3 hits
survive the threshold-3 cadence filter (events_f3.csv); false_clear_all_on =
1 - 3/6651 = 0.99955. This script redraws those verified counts.
Output: poso-cadence.pdf (300 dpi, serif).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# (a) per-scan hits over the ABACAD cadence (A = target ON; B,C,D = off-positions)
scans = ["A\n(ON)", "B\n(OFF)", "A\n(ON)", "C\n(OFF)", "A\n(ON)", "D\n(OFF)"]
hits = [2112, 2190, 2239, 2252, 2300, 2325]
on = [i % 2 == 0 for i in range(6)]
GOLD, GREY, GREEN = "#d4972a", "#9aa0a6", "#3f7f5c"

plt.rcParams.update({"font.family": "serif", "font.size": 8})
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.6, 2.6), gridspec_kw={"width_ratios": [3, 1.5]})

ax1.bar(range(6), hits, color=[GOLD if o else GREY for o in on], edgecolor="black", linewidth=0.4)
for i, h in enumerate(hits):
    ax1.text(i, h + 25, str(h), ha="center", va="bottom", fontsize=6.5)
ax1.set_xticks(range(6)); ax1.set_xticklabels(scans, fontsize=7)
ax1.set_ylabel("raw turboSETI hits"); ax1.set_ylim(0, 2500)
ax1.set_title("(a) Hits per scan, HIP101027 ABACAD cadence", fontsize=8)

ax2.bar([0, 1], [6651, 3], color=[GOLD, GREEN], edgecolor="black", linewidth=0.4)
ax2.set_yscale("log"); ax2.set_ylim(1, 2e4)
ax2.text(0, 6651 * 1.4, "6651", ha="center", va="bottom", fontsize=7)
ax2.text(1, 3 * 1.4, "3", ha="center", va="bottom", fontsize=7)
ax2.set_xticks([0, 1]); ax2.set_xticklabels(["raw ON\nhits", "survive\ncadence"], fontsize=7)
ax2.set_title("(b) The cadence consumer", fontsize=8)
ax2.annotate("false clear\n= 0.9995", xy=(0.5, 200), ha="center", fontsize=7, color=GREEN)

fig.tight_layout()
fig.savefig("poso-cadence.pdf", dpi=300)
fig.savefig("poso-cadence.png", dpi=300)
print("wrote poso-cadence.pdf / .png")
