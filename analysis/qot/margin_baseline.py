"""Scalar-margin baseline for the OFC surrogate section, derived from the sealed
per-prediction records (QOTML-preds.json, graded seed 20260825). Question: how
much uniform backoff must the average-error surrogate carry to match the
quantile objective's false-clear, and what does that cost in delivered bits?

    python margin_baseline.py [QOTML-preds.json]

LEAKAGE CONTROL (review round 3): the backoff is CALIBRATED on a designated
validation half (even record indices) as the smallest 0.05 dB multiple whose
validation FC is at or below the quantile model's validation FC, then FROZEN
and EVALUATED on the held-out test half (odd indices), where both objectives
are compared. The earlier version tuned on the full evaluation set; that
number (0.85 dB) is kept in the output for transparency but is not the
comparative result.

Selection rule (matches fam_qotml.py): highest declared format whose required
GSNR the (backed-off) prediction clears at the 0.5 dB design margin; fail =
true GSNR below the chosen format's requirement; delivered bits = format bits
on success, 0 on failure. The script first re-derives the recorded
mse_fail/aware_fail flags to prove the rule matches the sealed runner.
"""
import json
import sys

import numpy as np

REQ = np.array([6.5, 9.0, 12.5, 16.0, 19.0])
BITS = np.array([2, 3, 4, 5, 6])
MARGIN_DB = 0.5      # the runner's design margin (fam_qotml.MARGIN_DB)


def choose(pred):
    """Index of the highest format cleared at the design margin, -1 if none."""
    idx = np.searchsorted(REQ, pred - MARGIN_DB, side="right") - 1
    return idx


def stats(pred, true):
    idx = choose(pred)
    ok = idx >= 0
    fail = np.zeros(len(pred), bool)
    fail[ok] = REQ[idx[ok]] > true[ok]
    bits = np.where(ok & ~fail, BITS[np.clip(idx, 0, None)], 0)
    return fail.mean(), bits.mean()


def main(path="QOTML-preds.json"):
    r = json.load(open(path))["records"]
    true = np.array([x["true"] for x in r])
    pm = np.array([x["pred_mse"] for x in r])
    pa = np.array([x["pred_aware"] for x in r])
    mf = np.array([x["mse_fail"] for x in r], bool)
    af = np.array([x["aware_fail"] for x in r], bool)

    # prove the selection rule reproduces the sealed flags
    idx = choose(pm)
    rep_m = np.zeros(len(r), bool)
    rep_m[idx >= 0] = REQ[idx[idx >= 0]] > true[idx >= 0]
    idx = choose(pa)
    rep_a = np.zeros(len(r), bool)
    rep_a[idx >= 0] = REQ[idx[idx >= 0]] > true[idx >= 0]
    print(f"rule check: mse flags match {np.mean(rep_m == mf):.4f}, "
          f"aware {np.mean(rep_a == af):.4f}")
    if not (np.array_equal(rep_m, mf) and np.array_equal(rep_a, af)):
        sys.exit("selection rule does NOT reproduce the sealed flags -- stop.")

    fc_a, bits_a = stats(pa, true)
    fc_m0, bits_m0 = stats(pm, true)
    print(f"pooled -- aware: FC={fc_a:.4f} bits={bits_a:.3f} | mse raw: "
          f"FC={fc_m0:.4f} bits={bits_m0:.3f}")
    for m in np.arange(0, 3.01, 0.05):
        fc, bits = stats(pm - m, true)
        if fc <= fc_a:
            print(f"[transparency only, tuned on full set] m={m:.2f} dB: "
                  f"FC={fc:.4f} bits={bits:.3f}")
            break

    # leakage-controlled comparison: calibrate on even indices, test on odd
    val = np.arange(len(true)) % 2 == 0
    tst = ~val
    fc_a_val, _ = stats(pa[val], true[val])
    m_star = None
    for m in np.arange(0, 3.01, 0.05):
        fc, _ = stats(pm[val] - m, true[val])
        if fc <= fc_a_val:
            m_star = float(m)
            break
    if m_star is None:
        print("no margin up to 3 dB matches the aware FC on validation")
        return
    fc_m_t, bits_m_t = stats(pm[tst] - m_star, true[tst])
    fc_a_t, bits_a_t = stats(pa[tst], true[tst])
    print(f"leakage-controlled: m*={m_star:.2f} dB frozen on validation "
          f"(n={val.sum()}); held-out test (n={tst.sum()}): "
          f"backed-off MSE FC={fc_m_t:.4f} bits={bits_m_t:.3f} | "
          f"quantile FC={fc_a_t:.4f} bits={bits_a_t:.3f}")


if __name__ == "__main__":
    main(*sys.argv[1:])
