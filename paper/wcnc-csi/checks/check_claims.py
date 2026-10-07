"""Machine check of every quantitative claim in wcnc-csi.tex.

Same design as the OFC checker: each claim names a snippet that must appear
VERBATIM in the paper (whitespace collapsed) and a value derived from a sealed
record, a deterministic output, or a runner constant. FAIL if the snippet is
gone or the record disagrees. Exit 0 only if nothing fails.

    python check_claims.py --tex ../wcnc-csi.tex --analysis <campaigns>/analysis \
        [--curves /home/claude/csi/nr_bler_curves_sionna.npz]

Run on Atlas (laptop compute is off-limits).
"""
import argparse
import json
import math
import os
import re
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--tex", required=True)
ap.add_argument("--analysis", required=True, help="observation-theory-campaigns/analysis")
ap.add_argument("--curves", default=None, help="nr_bler_curves_sionna.npz (for the deep-fade claim)")
a = ap.parse_args()

TEX = re.sub(r"\s+", " ", open(a.tex, encoding="utf-8").read())
A = os.path.abspath(a.analysis)


def J(rel):
    return json.load(open(os.path.join(A, rel), encoding="utf-8"))


def src(rel):
    return open(os.path.join(A, rel), encoding="utf-8").read()


def const(text, name):
    m = re.search(r"^" + name + r"\s*=\s*([^#\n]+)", text, re.M)
    if not m:
        raise KeyError(name)
    return eval(m.group(1).strip(), {})


def r3(x):  # conventional half-up rounding to 3 decimals (avoid float half-even surprises)
    return math.floor(x * 1000 + 0.5 + 1e-9) / 1000


rows = []


def claim(cid, snippet, ok, detail):
    present = re.sub(r"\s+", " ", snippet) in TEX
    st = "PASS" if (present and ok) else "FAIL"
    if not present:
        detail = "snippet not found in tex :: " + detail
    rows.append((st, cid, detail))


def mean(xs):
    return sum(xs) / len(xs)


def rng3(xs):
    return f"{r3(min(xs)):.3f}--{r3(max(xs)):.3f}"


# ------------------------------------------------------------------ Sec. III budget study
u = J("urllc/XPROTO-URLLC-graded.json")
assert u["verdict"] == "PASS"
uc = u["cells"]
emb = [c["achieved_embb"] for c in uc]
claim("bud.table", r"20260824 & $0.1119$ & $0.1119$ & $1.7\times10^{-5}$",
      [c["seed"] for c in uc] == [20260824, 20260825, 20260826]
      and [round(x, 4) for x in emb] == [0.1119, 0.1103, 0.1125]
      and all(c["achieved_embb"] == c["achieved_urllc_naive"] for c in uc),
      f"eMBB per seed {emb}; naive column identical")
aw = [c["achieved_urllc_aware"] for c in uc]
claim("bud.aware", r"$1.9\times10^{-5}$ & \\ 20260826 & $0.1125$ & $0.1125$ & $<10^{-5}$",
      round(aw[0], 6) == 1.7e-5 and round(aw[1], 6) == 1.9e-5 and aw[2] < 1e-5, f"aware {aw}")
om = mean(emb) / 1e-3
claim("bud.112", "by a factor of 112", round(om) == 112, f"mean overrun {om:.1f}")
claim("bud.omega", r"($1.1$ vs $112$)", round(mean(emb) / 0.1, 1) == 1.1 and round(om) == 112,
      f"Omega eMBB {mean(emb) / 0.1:.3f}")
claim("bud.B", r"$\widehat{B}\approx 0.112$", round(mean(emb), 3) == 0.112, f"mean B {mean(emb):.4f}")

s = J("urllc/URLLCSNRREP-graded-raw.json")
grid = s["constants"]["snr_grid_db"]
emb_at = {g: [c["sweep"][str(g)]["embb"] for c in s["cells"]] for g in grid}
inr = [x / 1e-3 for g in (9, 12, 15, 18) for x in emb_at[g]]
claim("snr.grid", r"from $3$ to $21$\,dB", grid[0] == 3 and grid[-1] == 21, f"grid {grid}")
claim("snr.band", r"between $77\times$ and $142\times$ at every in-range SNR",
      round(min(inr)) == 77 and round(max(inr)) == 142, f"in-range (9-18 dB) overruns {min(inr):.1f}..{max(inr):.1f}")
claim("snr.sat", r"still $54\times$ where the MCS table saturates", round(min(emb_at[21]) / 1e-3) == 54,
      f"21 dB overruns {[round(x / 1e-3, 1) for x in emb_at[21]]}")
claim("snr.edge", r"($\widehat{B}\approx 0.20$ at $6$\,dB and $0.33$ at $3$\,dB)",
      round(mean(emb_at[6]), 2) == 0.20 and round(mean(emb_at[3]), 2) == 0.33
      and min(emb_at[6]) > 0.1 and min(emb_at[3]) > 0.1,
      f"6 dB {emb_at[6]}, 3 dB {emb_at[3]}")
fu = src("urllc/fam_urllc.py")
claim("bud.aware_policy", r"raises the backoff to $\Delta=4$\,dB and combines $K{=}3$ diversity branches",
      const(fu, "URLLC_MARGIN_DB") == 4.0 and const(fu, "DIVERSITY_K") == 3, "fam_urllc constants")

# deep-fade fraction: lowest MCS curve + Rayleigh at the mean SNR
if a.curves:
    import numpy as np
    d = np.load(a.curves)
    g, c0 = d["grid"], d["curves"][0]
    i = int(np.where(c0 <= 1e-3)[0][0])
    rho = g[i - 1] + (g[i] - g[i - 1]) * (c0[i - 1] - 1e-3) / (c0[i - 1] - c0[i])
    p = 1 - math.exp(-10 ** ((rho - 12.0) / 10))
    claim("bud.deepfade", r"spends about $6\%$ of its time in fades where even the lowest MCS misses the $10^{-3}$ budget", round(p * 100) == 6,
          f"lowest-MCS 1e-3 point {rho:.2f} dB; Rayleigh P(below) = {p:.4f} (TDL-A traces measured 0.058-0.064)")
else:
    rows.append(("UNCHECKED", "bud.deepfade", "pass --curves to check the 6% deep-fade claim"))

marg = [1e-3 / x for x in aw if x > 0]
claim("bud.fifty", r"lies below the $10^{-3}$ budget by a factor of about fifty",
      40 <= min(marg) and max(marg) <= 65, f"budget / aware product per seed {[round(m) for m in marg]} (third seed 0)")

# ------------------------------------------------------------------ Sec. IV age horizon
c = J("csi/XPROTO-CSI-graded.json")
assert c["verdict"] == "PASS"
cc = c["cells"]
nv, ol, er = [x["naive_bler"] for x in cc], [x["olla_bler"] for x in cc], [x["cqi_err_db"] for x in cc]
claim("age.err", r"off by $5.7$\,dB on average", round(mean(er), 1) == 5.7, f"cqi_err_db mean {mean(er):.3f}")
claim("age.naive", r"$\widehat{B}\approx 0.36$ against the $0.10$ budget, an overrun of $3.6\times$",
      round(mean(nv), 2) == 0.36 and round(mean(nv) / 0.10, 1) == 3.6, f"naive mean {mean(nv):.4f}")
claim("age.olla", r"$0.34$ to $0.37$ naive against $0.101$ to $0.102$ corrected",
      round(min(nv), 2) == 0.34 and round(max(nv), 2) == 0.37 and r3(min(ol)) == 0.101 and r3(max(ol)) == 0.102,
      f"naive {nv}, olla {ol}")
cs = src("csi/csi_sionna.py")
claim("age.cell", r"At $200$\,Hz Doppler with a $20$-TTI report period",
      all(x["fd_hz"] == 200.0 and x["report_period"] == 20 for x in cc), "cell constants")
ex = J("csi/CSI-refreshfloor.json")
p1 = [ex["bler_grid"][k][0] for k in ex["bler_grid"]]
fresh200 = [x["fresh_bler"] for x in cc]
claim("age.uncal", r"($\widehat{B}\approx 0.11$)",
      "SUPERSEDED" in ex and all(0.10 < x < 0.12 for x in p1 + fresh200) and round(mean(p1), 2) == 0.11,
      f"uncalibrated fresh: exploration P=1 over Dopplers {p1} (mean {mean(p1):.4f}); sealed 200 Hz {fresh200}")
claim("age.law", r"$P^\star\approx 0.18\,T_{\mathrm{coh}}$", "0.177*Tcoh" in ex["SUPERSEDED"],
      "exploration fit 0.177 T_coh, refuted and disclosed")
w = J("csi/XPROTO-CSI-SWEEP2-graded.json")
assert w["verdict"] == "PASS" and not any(x["censored_fds"] for x in w["cells"])
fl = {x["seed"]: x["floors_tti"] for x in w["cells"]}
claim("age.table", r"20260827 & $4$ & $2$ & $1$ & $0.080$ \\ 20260828 & $6$ & $2$ & $1$ & $0.078$ \\ 20260829 & $4$ & $3$ & $1$ & $0.080$",
      [(f[str(10)], f[str(25)], max(f[k] for k in ("50", "100", "200", "400"))) for f in fl.values()]
      == [(4, 2, 1), (6, 2, 1), (4, 3, 1)]
      and [r3(max(x["fresh_bler"].values())) for x in w["cells"]] == [0.080, 0.078, 0.080],
      f"floors {fl}")
claim("age.cal", r"(a $0.5$\,dB backoff suffices)",
      all(x["d_cal_db"] == 0.5 for x in w["cells"]) and all(max(x["fresh_bler"].values()) <= 0.09 for x in w["cells"]),
      "d_cal 0.5 dB; fresh <= 0.09 at every Doppler")
fs2 = src("csi/fam_csi_sweep2.py")
claim("age.sweep", r"$f_D=10$--$400$\,Hz, $P=1$--$32$ TTI",
      const(fs2, "FDS")[0] == 10 and const(fs2, "FDS")[-1] == 400
      and const(fs2, "PERIODS")[0] == 1 and const(fs2, "PERIODS")[-1] == 32, "FDS, PERIODS")
claim("age.step", r"chosen in $0.25$\,dB steps", const(fs2, "CAL_STEP_DB") == 0.25 and const(fs2, "CAL_MARGIN") == 0.09,
      "CAL_STEP_DB, CAL_MARGIN")
claim("age.len", r"$12\,000$ TTI (age)", const(fs2, "NTTI") == 12000, "NTTI")
# Doppler -> speed at the carrier
fc = const(cs, "FC_HZ")
kmh = lambda fd: fd * 299792458.0 / fc * 3.6
claim("age.walk", r"Ten hertz is about $3$\,km/h", round(kmh(10)) == 3, f"10 Hz = {kmh(10):.2f} km/h at {fc / 1e9} GHz")
claim("age.bike", r"$50$\,Hz about $15$\,km/h", round(kmh(50)) == 15, f"50 Hz = {kmh(50):.2f} km/h")

# ------------------------------------------------------------------ Sec. V four certificates
b = J("beam/XPROTO-BEAM-graded.json")
ph = J("phy/XPROTO-PHY-graded.json")
assert b["verdict"] == "PASS" and ph["verdict"] == "PASS"
bc = b["cells"]
P = {k: [x for x in ph["cells"] if x["cell"] == k] for k in ("pmi", "ri", "ta")}
nb, wb, fb, lb = ([x[k] for x in bc] for k in ("naive_bler", "bfr_bler", "fresh_bler", "beam_loss_db"))
claim("fam.beam", r"beam, FR2 & $4.67$--$4.79$\,dB & $0.310$--$0.329$ & $0.098$--$0.104$ & $0.021$--$0.027$",
      (rng3(nb), rng3(wb), rng3(fb)) == ("0.310--0.329", "0.098--0.104", "0.021--0.027")
      and round(min(lb), 2) == 4.67 and round(max(lb), 2) == 4.79, f"beam naive {nb} bfr {wb} fresh {fb} loss {lb}")
pm = P["pmi"]
claim("fam.pmi", r"precoder & $3.09$--$3.11$\,dB & $0.299$--$0.311$ & $0.124$--$0.130$ & $0$",
      round(min(x["aging"] for x in pm), 2) == 3.09 and round(max(x["aging"] for x in pm), 2) == 3.11
      and rng3([x["naive_fc"] for x in pm]) == "0.299--0.311" and rng3([x["witnessed_fc"] for x in pm]) == "0.124--0.130"
      and all(x["fresh_fc"] == 0 for x in pm), "pmi cells")
ri = P["ri"]
claim("fam.ri", r"rank & (see text) & $0.268$--$0.299$ & $0.079$--$0.085$ & $0$",
      rng3([x["naive_fc"] for x in ri]) == "0.268--0.299" and rng3([x["witnessed_fc"] for x in ri]) == "0.079--0.085"
      and all(x["fresh_fc"] == 0 for x in ri) and all(x["aging"] == x["naive_fc"] for x in ri),
      "ri cells; drift == failure rate by construction")
ta = P["ta"]
claim("fam.ta", r"timing adv. & $0.420$--$0.427$ & $0.419$--$0.425$ & $0.055$--$0.056$ & $0$",
      rng3([x["aging"] for x in ta]) == "0.420--0.427" and rng3([x["naive_fc"] for x in ta]) == "0.419--0.425"
      and rng3([x["witnessed_fc"] for x in ta]) == "0.055--0.056" and all(x["fresh_fc"] == 0 for x in ta), "ta cells")
claim("fam.ta_text", r"mean residual of $0.42$ cyclic prefixes", round(mean([x["aging"] for x in ta]), 2) == 0.42,
      f"mean {mean([x['aging'] for x in ta]):.4f}")
means = [mean(nb)] + [mean([x["naive_fc"] for x in P[k]]) for k in ("pmi", "ri", "ta")]
claim("fam.span", r"the four rates span $2.8$ to $4.2$ times the target",
      round(min(means) / 0.1, 1) == 2.8 and round(max(means) / 0.1, 1) == 4.2, f"seed means / target {[round(m / 0.1, 2) for m in means]}")
over = [x["witnessed_fc"] / 0.1 - 1 for x in pm]
claim("fam.pmi_over", r"which is $24$ to $30$ percent above", round(min(over) * 100) == 24 and round(max(over) * 100) == 30,
      f"overshoot {[round(o * 100, 1) for o in over]} %")
claim("fam.requotes", "549 to 558 times in 6000 slots",
      min(x["n_requotes"] for x in pm) == 549 and max(x["n_requotes"] for x in pm) == 558
      and all(x["n_tti"] == 6000 for x in pm), "n_requotes")
claim("fam.rule3", r"bound the fresh rate below $5\times10^{-4}$ at $95\%$",
      abs(3 / 6000 - 5e-4) < 1e-12 and 1 - 0.05 ** (1 / 6000) < 5e-4, f"exact 95% bound {1 - 0.05 ** (1 / 6000):.3e}")
fb_ = src("beam/fam_beam.py")
fp = src("phy/fam_phy.py")
claim("fam.beamcell", r"sixteen-element half-wavelength array factor over a twenty-four-beam codebook spanning $\pm 60$ degrees",
      const(fb_, "N_ANT") == 16 and const(fb_, "N_BEAMS") == 24 and const(fb_, "FOV_DEG") == 60.0, "fam_beam")
claim("fam.beamdrift", r"drifting at $300$ degrees per second and a one-degree measurement error",
      const(fb_, "OMEGA_DPS") == 300.0 and const(fb_, "ANG_NOISE_DEG") == 1.0, "fam_beam")
claim("fam.phy", r"angular drift of $1200$ degrees per second at $0.3$\,dB of gain loss per degree, a rank changing $270$ times per second over four ranks",
      ("PMI_REPORT, OMEGA_PMI = 20, 1200.0" in fp and const(fp, "PMI_LOSS_DB_PER_DEG") == 0.3
       and "RI_REPORT, RANK_FLIP_HZ = 20, 270.0" in fp
       and "rng.integers(1, 5)" in fp and "np.clip(rank + rng.choice([-1, 1]), 1, 4)" in fp),
      "fam_phy literals; ranks 1..4")
claim("fam.ta_model", r"a delay drifting $20\,\mu$s per second against a $4.7\,\mu$s cyclic prefix",
      "TA_REPORT, TA_DRIFT_US_PER_S = 200, 20.0" in fp and const(fp, "CP_US") == 4.7, "fam_phy")
claim("fam.cadence", r"20 slots (200 for TA), 6000 slots",
      const(fb_, "REPORT_PERIOD") == 20 and "PMI_REPORT, OMEGA_PMI = 20" in fp and "RI_REPORT, RANK_FLIP_HZ = 20" in fp
      and "TA_REPORT, TA_DRIFT_US_PER_S = 200" in fp and const(fp, "DURATION") == 6000, "cadences")
claim("fam.bfr2", "re-reports after two consecutive failures",
      const(fb_, "BFR_NACK_THRESH") == 2 and const(fp, "BFR_NACK") == 2, "two-NACK trigger in both runners")
claim("fam.mcs2", "set two decibels below the aligned operating point",
      const(fb_, "MCS_MARGIN_DB") == 2.0 and const(fp, "MCS_MARGIN") == 2.0, "fixed-MCS margin")

# ------------------------------------------------------------------ Method / Table I constants
claim("tab.carrier", r"$3.5$\,GHz / $1$\,ms", const(cs, "FC_HZ") == 3.5e9 and const(cs, "TTI_S") == 0.001, "csi_sionna")
claim("tab.ds", r"TDL-A, DS $=30$\,ns", const(cs, "DELAY_SPREAD_S") == 30e-9, "csi_sionna.DELAY_SPREAD_S")
claim("tab.snr", r"Mean SNR & $12$\,dB", const(cs, "MEAN_SNR_DB") == 12.0, "MEAN_SNR_DB")
claim("tab.curves", r"400 blk/pt, $-8$--$28$\,dB @ $2$\,dB",
      const(cs, "NBLOCKS") == 400 and "np.arange(-8.0, 28.01, 2.0)" in cs, "NBLOCKS, SNR_GRID")
claim("tab.sigma", r"CQI report noise $\sigma$ & $1$\,dB", const(cs, "CQI_NOISE_DB") == 1.0 and const(fu, "CQI_NOISE_DB") == 1.0,
      "CQI_NOISE_DB (csi_sionna, fam_urllc)")
claim("tab.len", r"$6000$ TTI (budget)", const(fu, "DURATION") == 6000 and all(x["n_tti"] == 6000 for x in uc), "budget trace length")
claim("tab.olla", r"$\delta_{\mathrm{up}}=0.1$\,dB, $\delta_{\mathrm{dn}}=0.9$\,dB",
      const(cs, "OLLA_UP_DB") == 0.1 and abs(0.1 * (1 - 0.1) / 0.1 - 0.9) < 1e-12, "OLLA_UP_DB; dn = up(1-b)/b")
claim("tab.zero400", r"binomial $95\%$ upper bound near $7.5\times10^{-3}$", abs(3 / 400 - 7.5e-3) < 1e-12
      and abs((1 - 0.05 ** (1 / 400)) - 7.5e-3) < 2e-4, f"exact {1 - 0.05 ** (1 / 400):.4e}")

# ------------------------------------------------------------------ report
w_ = max(len(r[1]) for r in rows)
for st, cid, det in rows:
    print(f"{st:9s} {cid:{w_}s}  {det}")
cnt = {k: sum(1 for r in rows if r[0] == k) for k in ("PASS", "FAIL", "UNCHECKED")}
print(f"\n{len(rows)} claims: " + ", ".join(f"{k} {v}" for k, v in cnt.items()))
sys.exit(1 if cnt["FAIL"] else 0)
