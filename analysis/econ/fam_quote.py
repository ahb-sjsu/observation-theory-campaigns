"""XPROTO-QUOTE family (F-QUOTE): the market-making stale-quote / adverse-
selection cell -- the economics entry in the vacuity taxonomy.

Certificate = a live quote ("tradeable at this price"). Consumer = the market
maker's book, whose half-spread s IS its read operator (how far the true price
may move before the book is hurt). False-clear = adverse selection: the true mid
moved beyond the quote, so a fill picks off the stale side and the maker loses.
Witness = the realized mid. Deployed correction = re-quote on an observed price
move (a witnessed, price-triggered re-quote), the maker's actual practice.

The false-clear rate rises with quote age as the mid random-walks away; the
refresh floor -- the max quote lifetime holding adverse selection at target --
scales as the spread-coherence time (s/sigma)^2 (the financial OT-14).
Consumer-relativity: on the SAME price path a tight-spread book is picked off by
moves a wide-spread book tolerates.

  mode "sim"   : an efficient-price random walk. Validates the phenomenon and
                 the grading in the canonical microstructure model -- NOT
                 evidence about real markets (as fam_csi's sim is not evidence
                 about real 5G). quote_check.py refuses to SEAL on sim.
  mode "ticks" : real mid-price tick series (econ/ticks/seed_<n>.csv). The
                 sealed rung (gated on data access, like CCA on SDR hardware).

    python3 fam_quote.py --sim              # phenomenon + grading validation
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- sealed cell constants (bars reference these; do not tune) -------
SIGMA = 1.0                 # mid-price step volatility
HALF_SPREAD = 3.0           # the reference book's half-spread s (= 3 sigma)
REPORT_PERIOD = 30          # naive fixed re-quote cadence (steps)
TRIGGER_K = 0.5             # witnessed: re-quote when |mid - quote| > K*s
DURATION = 20000
TIGHT_S = 2.0              # consumer-relativity: tight book
WIDE_S = 6.0              # consumer-relativity: wide book
TARGET = 0.10


def _random_walk(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return np.cumsum(rng.normal(0.0, SIGMA, DURATION))


def load_ticks(seed: int) -> np.ndarray:
    path = os.path.join(HERE, "ticks", f"seed_{seed}.csv")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"real tick series missing: {path} -- the sealed "
                                f"run needs market data (mode=ticks).")
    return np.loadtxt(path)


def naive(mid: np.ndarray, s: float, period: int) -> tuple[float, float]:
    """Fixed-cadence re-quote: quote = mid at the last period boundary."""
    quote = mid[(np.arange(len(mid)) // period) * period]
    dev = np.abs(mid - quote)
    return float(np.mean(dev > s)), float(np.mean(dev) / s)


def fresh(mid: np.ndarray, s: float) -> float:
    quote = np.concatenate([[mid[0]], mid[:-1]])   # re-quote every step
    return float(np.mean(np.abs(mid - quote) > s))


def witnessed(mid: np.ndarray, s: float, k: float) -> tuple[float, int]:
    """Re-quote when the observed move exceeds k*s (the witness-triggered
    correction). False-clear is checked against the pre-step quote."""
    quote = mid[0]
    fc = req = 0
    for t in range(len(mid)):
        if abs(mid[t] - quote) > s:
            fc += 1                                 # picked off before re-quoting
        if abs(mid[t] - quote) > k * s:
            quote = mid[t]; req += 1                # re-quote on the observed move
    return fc / len(mid), req


def run_cell(seed: int, mode: str = "sim") -> dict:
    mid = load_ticks(seed) if mode == "ticks" else _random_walk(seed)
    nfc, dev_over_s = naive(mid, HALF_SPREAD, REPORT_PERIOD)
    wfc, req = witnessed(mid, HALF_SPREAD, TRIGGER_K)
    ffc = fresh(mid, HALF_SPREAD)
    nt, _ = naive(mid, TIGHT_S, REPORT_PERIOD)
    nw, _ = naive(mid, WIDE_S, REPORT_PERIOD)
    return {
        "seed": int(seed), "mode": mode,
        "naive_fc": round(nfc, 4), "witnessed_fc": round(wfc, 4),
        "fresh_fc": round(ffc, 4),
        "naive_tight": round(nt, 4), "naive_wide": round(nw, 4),
        "mean_dev_over_spread": round(dev_over_s, 4),
        "n_steps": len(mid), "n_requotes": int(req), "target": TARGET,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sim", action="store_true",
                    help="synthetic efficient-price walk (model validation, not evidence)")
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "QUOTEREP-family.json"))
    args = ap.parse_args()
    mode = "sim" if args.sim else "ticks"
    cells = [run_cell(s, mode) for s in args.seeds]
    for c in cells:
        print(f"seed {c['seed']}: naive_fc={c['naive_fc']} witnessed_fc={c['witnessed_fc']} "
              f"fresh_fc={c['fresh_fc']} | tight={c['naive_tight']} wide={c['naive_wide']} "
              f"dev/s={c['mean_dev_over_spread']} requotes={c['n_requotes']}", flush=True)
    rec = {"family": "F-QUOTE", "mode": mode,
           "sim_is_model_validation_not_evidence": (mode == "sim"),
           "constants": {"sigma": SIGMA, "half_spread": HALF_SPREAD,
                         "report_period": REPORT_PERIOD, "trigger_k": TRIGGER_K,
                         "duration": DURATION, "target": TARGET,
                         "substrate": ("efficient-price random walk (canonical "
                                       "microstructure model); sealed rung = real ticks")},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
