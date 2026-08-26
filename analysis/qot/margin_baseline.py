"""Scalar-margin baseline for the OFC surrogate section, derived from the sealed
per-prediction records (QOTML-preds.json, graded seeds). Question: how much
uniform backoff must the average-error surrogate carry to match the quantile
objective's false-clear, and what does that cost in delivered bits?

    python margin_baseline.py [QOTML-preds.json]

Selection rule (matches fam_qotml.py): highest declared format whose required
GSNR the (backed-off) prediction clears; fail = true GSNR below the chosen
format's requirement; delivered bits = format bits on success, 0 on failure.
The script first re-derives the recorded mse_fail/aware_fail flags to prove the
rule matches the sealed runner before trusting the margin sweep.
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
    print(f"aware: FC={fc_a:.4f} bits={bits_a:.3f} | mse raw: FC={fc_m0:.4f} "
          f"bits={bits_m0:.3f}")
    for m in np.arange(0, 3.01, 0.05):
        fc, bits = stats(pm - m, true)
        if fc <= fc_a:
            print(f"scalar margin m={m:.2f} dB on the MSE surrogate: FC={fc:.4f} "
                  f"(<= aware {fc_a:.4f}), bits={bits:.3f} "
                  f"(aware {bits_a:.3f}, delta {bits - bits_a:+.3f} b/sym)")
            break
    else:
        print("no margin up to 3 dB matches the aware FC")


if __name__ == "__main__":
    main(*sys.argv[1:])
