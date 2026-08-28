# Channel prediction vs the OT-14 refresh floor — result

> **SUPERSEDED PROVENANCE (2026-08-27).** This note was written against the
> `csi_sweep.py` / `CSI-refreshfloor.json` refresh-floor exploration, which measured its
> floors at a relaxed 0.15 threshold against a 0.10 claim and whose fresh baseline
> (BLER ≈ 0.113) never met the budget. That exploration was never sealed and its
> ≈ 0.177·T_coh law is refuted. It is superseded by **XPROTO-CSI-SWEEP2 (sealed
> 2026-08-27, graded PASS)**, where the horizon at the true 0.10 budget collapses to
> 4/6/4 TTI at 10 Hz, 2/2/3 TTI at 25 Hz, and 1 TTI at 50 Hz and above. The prediction
> result below (the coherence-time wall) is independent of that law and stands; only the
> "exactly the refresh floor" identification does not. Record kept.

*Exploration, 2026-08-23 (`csi_predict.py`, real Sionna TDL substrate). Answers:
can 6G "AI-native" channel prediction beat the refresh floor by reporting less
often and predicting the aged channel forward?*

## What was measured

The optimal linear (Wiener) predictor for the real fading process, using the
M=8 most recent CSI samples to predict the effective SINR `Delta` steps ahead,
vs the naive "hold the last report" estimator. Mean |SINR error| in dB vs
lookahead, at fd = 50 Hz (Tcoh 8.5 ms) and 200 Hz (Tcoh 2.1 ms). See
`CSI-PREDICT.png`.

## Result: prediction cannot see past the coherence time

- **Both** error curves rise steeply and **saturate within ~one coherence
  time** (by ~8 ms at 50 Hz, ~2 ms at 200 Hz). Beyond Tcoh neither estimator is
  tracking the channel — the error is flat.
- The predictor's **residual floor is the channel standard deviation** sigma
  (~4.2 dB): once the channel has decorrelated, the Wiener predictor reverts to
  the mean SINR. The naive-hold floor is **~sqrt(2)*sigma** (~6 dB): the
  difference of two near-independent samples. Measured ratio ~1.4, i.e. sqrt(2),
  confirming both are *guessing* beyond Tcoh.
- The persistent ~1.7 dB advantage of prediction at large lookahead is therefore
  **mean-reversion, not lookahead** — predicting the long-run mean beats holding
  a stale random sample by sqrt(2), but it is not seeing the future.
- Genuine tracking (error well below saturation) exists **only for Delta <~
  Tcoh**. That wall sits far outside the sealed operating horizon. At the true
  0.10 budget the largest compliant report period is 4/6/4 TTI at 10 Hz, 2/2/3
  TTI at 25 Hz, and 1 TTI at 50 Hz and above (XPROTO-CSI-SWEEP2, sealed
  2026-08-27). Prediction is therefore accurate over a window the budget has
  already closed.

## Why this is fundamental, not an artifact of a weak predictor

For Rayleigh/Jakes fading the complex channel gain is a **Gaussian process**.
For a Gaussian process the linear MMSE (Wiener) predictor is the **optimal**
predictor of any kind — no nonlinear or deep-learning predictor can beat it.
So the coherence-time wall measured here is not a limitation of "not using AI";
it is information-theoretic: past ~Tcoh the future channel is (nearly)
independent of the past, and no predictor recovers independent information.

**Takeaway.** Channel predictability is bounded by a coherence-time wall. That
wall is not the operating constraint. At the true 0.10 budget the sealed age
horizon is already only a few TTI at walking pace and 1 TTI at 50 Hz and above
(XPROTO-CSI-SWEEP2), well inside the coherence time. 6G AI-native CSI
prediction can (a) track accurately within a coherence time and (b) beat
naive-hold by sqrt(2) via mean-reversion, but it **cannot extend the horizon
over which CSI is knowable**. It also cannot buy back the horizon the budget
takes away. Periodic reporting alone cannot protect a tight budget at practical
mobility; the HARQ-witnessed correction is mandatory, not optional.

*Caveat:* real channels are not perfectly stationary/Gaussian — deep predictors
help where there is exploitable non-Gaussian structure (deterministic mobility,
beam/geometry priors, non-stationarity). The canonical Rayleigh model has none,
so it is the clean worst case for "prediction beats the floor," and prediction
loses. The `naive_horizon`/`extension` fields in `CSI-PREDICT.json` use a loose
error-budget reference and are superseded by this saturation analysis.
