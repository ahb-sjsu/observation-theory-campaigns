#!/usr/bin/env python3
"""OT-finance shakedown (UNSEALED, exploratory) -- the consumer-relative
staleness law on real market data.

Claim under construction: staleness is not a property of a feed; it is a
property of (feed, consumer). A threshold monitor at relative distance d
reading a price feed with lag L flips its verdict (lagged read disagrees with
fresh read) at a rate governed by the dimensionless ratio

    u = sigma * sqrt(L) / d        (diffusive first-passage scaling)

so the refresh floor L*(d) scales as (d/sigma)^2: near-threshold consumers
need quadratically fresher data, and the SAME feed at the SAME lag is
simultaneously fresh (far consumer) and stale (near consumer). This is the
flip law (misaligned read AND near threshold) + the OT-14 refresh floor,
transferred to market data.

Substrate: Binance public bulk data (data.binance.vision, free, no auth):
one full day of BTCUSDT aggTrades (primary) and ETHUSDT (replication arm),
last-trade price on a 100 ms grid. Consumer = liquidation-style monitor:
threshold theta = p(t0)*(1 - d) fixed at each 5-minute window start; at
evaluation times t (every 1 s) the monitor reads p(t - L) and asserts breach
iff p(t-L) <= theta; truth uses p(t). Flip = verdicts differ. Window realized
vol sigma_w from 1 s log-returns (per sqrt-second, relative units).

Grid: d in {2, 5, 10, 20, 50} bps; L in {0.1, 0.3, 1, 3, 10, 30} s.

PRE-STATED PREDICTIONS (graded after the run, disclosed either way):
  P1 collapse: pooled (window, d, L) cell means of flip rate vs
     u = sigma_w*sqrt(L)/d fit a single monotone curve: Spearman(flip, u)
     >= 0.9 over the 30 (d,L) cells and isotonic-fit R^2 >= 0.85.
  P2 consumer-relative verdict: at L = 3 s, flip(d=2bps) >= 20x flip(d=50bps)
     and flip(d=50bps) <= 0.1% of decisions. Same feed, same lag: stale for
     the near consumer, fresh for the far one.
  P3 refresh floor: L*(d) = smallest grid lag with flip rate > 0.5%;
     log-log slope of L* vs d = 2 +/- 0.4 (the first-passage exponent).
  P4 regime control: top- vs bottom-vol-tercile windows give the same f(u)
     (max relative gap <= 20% at matched u bins with both occupied): the law
     lives in u, not in wall-clock lag.
  P5 replication arm: P1 holds on ETHUSDT (Spearman >= 0.9, R^2 >= 0.85).

Zero live exposure: historical public data, no orders, no keys.
Output: ~/ot-finance/staleness_result.json
"""

import io
import json
import os
import urllib.request
import zipfile

import numpy as np

HERE = os.path.expanduser("~/ot-finance")
DAY = "2026-08-28"
SYMS = ["BTCUSDT", "ETHUSDT"]
GRID_MS = 100
EVAL_EVERY_MS = 1000
WINDOW_MS = 300_000
D_BPS = [2.0, 5.0, 10.0, 20.0, 50.0]
LAGS_S = [0.1, 0.3, 1.0, 3.0, 10.0, 30.0]
FLOOR = 0.005


def _to_ms(t):
    # Binance bulk data moved to MICROSECOND timestamps (~1e15 epoch); the
    # first run treated them as ms, shrinking every lag 1000x (degenerate
    # zero-flip result, disclosed). Normalize to ms.
    return t // 1000 if t[0] > 10 ** 14 else t


def fetch(sym):
    p = os.path.join(HERE, f"{sym}-aggTrades-{DAY}.npz")
    if os.path.exists(p):
        z = np.load(p)
        return _to_ms(z["t"]), z["px"]
    url = (f"https://data.binance.vision/data/spot/daily/aggTrades/{sym}/"
           f"{sym}-aggTrades-{DAY}.zip")
    print(f"[data] fetching {url}", flush=True)
    raw = urllib.request.urlopen(url, timeout=300).read()
    zf = zipfile.ZipFile(io.BytesIO(raw))
    name = zf.namelist()[0]
    ts, px = [], []
    with zf.open(name) as f:
        for line in f:
            c = line.decode().split(",")
            if not c[0].isdigit():
                continue
            px.append(float(c[1]))
            ts.append(int(c[5]))
    t = np.array(ts, dtype=np.int64)
    x = np.array(px, dtype=np.float64)
    order = np.argsort(t, kind="stable")
    t, x = t[order], x[order]
    np.savez(p, t=t, px=x)
    print(f"[data] {sym}: {len(t)} trades", flush=True)
    return _to_ms(t), x


def price_grid(t, px):
    t0 = (t[0] // GRID_MS) * GRID_MS
    n = int((t[-1] - t0) // GRID_MS)
    grid_t = t0 + GRID_MS * np.arange(n)
    idx = np.searchsorted(t, grid_t, side="right") - 1
    idx = np.clip(idx, 0, len(px) - 1)
    return grid_t, px[idx]


def run_symbol(sym):
    t, px = fetch(sym)
    gt, gp = price_grid(t, px)
    n = len(gp)
    per_grid_eval = EVAL_EVERY_MS // GRID_MS
    per_grid_win = WINDOW_MS // GRID_MS
    max_lag_pts = int(max(LAGS_S) * 1000 / GRID_MS)
    win_starts = np.arange(max_lag_pts + per_grid_win, n - per_grid_win,
                           per_grid_win)
    # realized vol per window from 1 s log-returns, per sqrt-second, relative
    lp = np.log(gp)
    r1s = lp[per_grid_eval:] - lp[:-per_grid_eval]
    cells = {(d, L): [0, 0] for d in D_BPS for L in LAGS_S}
    win_rows = []
    for w0 in win_starts:
        w1 = w0 + per_grid_win
        rr = r1s[w0:w1 - per_grid_eval]
        sig = float(np.sqrt(np.mean(rr ** 2)))  # per sqrt(1 s), relative
        p0 = gp[w0]
        ev = np.arange(w0, w1, per_grid_eval)
        truth_p = gp[ev]
        row = {"sigma": sig}
        for d in D_BPS:
            theta = p0 * (1 - d * 1e-4)
            vt = truth_p <= theta
            for L in LAGS_S:
                lag_pts = int(L * 1000 / GRID_MS)
                vl = gp[ev - lag_pts] <= theta
                fl = int(np.sum(vt != vl))
                cells[(d, L)][0] += fl
                cells[(d, L)][1] += len(ev)
                row[f"flip_{d}_{L}"] = fl / len(ev)
        win_rows.append(row)
    out = {}
    for (d, L), (fl, tot) in cells.items():
        u_med = float(np.median([r["sigma"] for r in win_rows])) \
            * np.sqrt(L) / (d * 1e-4)
        out[f"{d}bps_{L}s"] = {"d_bps": d, "L_s": L, "flip": fl / tot,
                               "u_median_sigma": u_med, "n": tot}
    return out, win_rows


def grade(cellmap, win_rows, tag):
    from scipy.stats import spearmanr
    ds = np.array([c["d_bps"] for c in cellmap.values()])
    Ls = np.array([c["L_s"] for c in cellmap.values()])
    fl = np.array([c["flip"] for c in cellmap.values()])
    u = np.array([c["u_median_sigma"] for c in cellmap.values()])
    sp = float(spearmanr(u, fl).statistic)
    # isotonic fit R^2 in u
    from sklearn.isotonic import IsotonicRegression
    ir = IsotonicRegression(increasing=True).fit(u, fl)
    pred = ir.predict(u)
    ss = 1 - np.sum((fl - pred) ** 2) / max(np.sum((fl - fl.mean()) ** 2), 1e-18)
    p1 = {"spearman": sp, "iso_R2": float(ss),
          "pass": bool(sp >= 0.9 and ss >= 0.85)}
    f2 = fl[(ds == 2.0) & (Ls == 3.0)][0]
    f50 = fl[(ds == 50.0) & (Ls == 3.0)][0]
    p2 = {"flip_2bps_3s": float(f2), "flip_50bps_3s": float(f50),
          "ratio": float(f2 / max(f50, 1e-12)),
          "pass": bool(f2 >= 20 * f50 and f50 <= 1e-3)}
    lstar = {}
    for d in D_BPS:
        sub = sorted([(c["L_s"], c["flip"]) for c in cellmap.values()
                      if c["d_bps"] == d])
        hit = [Lv for Lv, fv in sub if fv > FLOOR]
        if hit:
            lstar[d] = min(hit)
    if len(lstar) >= 3:
        dd = np.log(list(lstar.keys()))
        ll = np.log(list(lstar.values()))
        slope = float(np.polyfit(dd, ll, 1)[0])
        p3 = {"L_star": {str(k): v for k, v in lstar.items()},
              "loglog_slope": slope, "pass": bool(abs(slope - 2) <= 0.4)}
    else:
        p3 = {"L_star": {str(k): v for k, v in lstar.items()},
              "loglog_slope": None,
              "pass": False, "note": "fewer than 3 d values crossed the floor"}
    # P4: vol-tercile regime control on per-window flip vs u
    sigs = np.array([r["sigma"] for r in win_rows])
    lo_t, hi_t = np.quantile(sigs, [1 / 3, 2 / 3])
    ub, fb = {"lo": [], "hi": []}, {"lo": [], "hi": []}
    for r in win_rows:
        reg = "lo" if r["sigma"] <= lo_t else ("hi" if r["sigma"] >= hi_t else None)
        if reg is None:
            continue
        for d in D_BPS:
            for L in LAGS_S:
                ub[reg].append(r["sigma"] * np.sqrt(L) / (d * 1e-4))
                fb[reg].append(r[f"flip_{d}_{L}"])
    bins = np.logspace(-2, 1, 10)
    gaps = []
    for i in range(len(bins) - 1):
        vals = {}
        for reg in ("lo", "hi"):
            uu = np.array(ub[reg])
            ff = np.array(fb[reg])
            m = (uu >= bins[i]) & (uu < bins[i + 1])
            if m.sum() >= 30:
                vals[reg] = float(ff[m].mean())
        if len(vals) == 2 and max(vals.values()) > 1e-4:
            gaps.append(abs(vals["lo"] - vals["hi"]) / max(vals.values()))
    p4 = {"matched_u_bins": len(gaps),
          "max_rel_gap": float(max(gaps)) if gaps else None,
          "pass": bool(gaps and max(gaps) <= 0.20)}
    return {"P1_collapse": p1, "P2_consumer_relative": p2,
            "P3_refresh_floor": p3, "P4_regime_control": p4}


def main():
    os.makedirs(HERE, exist_ok=True)
    result = {"day": DAY, "grid_ms": GRID_MS, "window_ms": WINDOW_MS,
              "d_bps": D_BPS, "lags_s": LAGS_S, "symbols": {}}
    for i, sym in enumerate(SYMS):
        cellmap, win_rows = run_symbol(sym)
        g = grade(cellmap, win_rows, sym)
        result["symbols"][sym] = {"cells": cellmap, "grades": g,
                                  "n_windows": len(win_rows)}
        print(f"[{sym}] " + json.dumps(g), flush=True)
    btc = result["symbols"]["BTCUSDT"]["grades"]
    eth = result["symbols"]["ETHUSDT"]["grades"]
    result["P5_replication"] = {"eth_P1": eth["P1_collapse"],
                                "pass": eth["P1_collapse"]["pass"]}
    result["verdicts"] = {
        "P1": btc["P1_collapse"]["pass"], "P2": btc["P2_consumer_relative"]["pass"],
        "P3": btc["P3_refresh_floor"]["pass"], "P4": btc["P4_regime_control"]["pass"],
        "P5": result["P5_replication"]["pass"]}
    print("[verdicts] " + json.dumps(result["verdicts"]), flush=True)
    with open(os.path.join(HERE, "staleness_result.json"), "w") as f:
        json.dump(result, f, indent=2)
    print(f"wrote {HERE}/staleness_result.json", flush=True)


if __name__ == "__main__":
    main()
