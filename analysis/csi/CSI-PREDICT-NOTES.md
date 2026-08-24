# Channel prediction vs the OT-14 refresh floor — result

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
  Tcoh** — exactly the OT-14 refresh floor.

## Why this is fundamental, not an artifact of a weak predictor

For Rayleigh/Jakes fading the complex channel gain is a **Gaussian process**.
For a Gaussian process the linear MMSE (Wiener) predictor is the **optimal**
predictor of any kind — no nonlinear or deep-learning predictor can beat it.
So the coherence-time wall measured here is not a limitation of "not using AI";
it is information-theoretic: past ~Tcoh the future channel is (nearly)
independent of the past, and no predictor recovers independent information.

**Takeaway.** OT-14's refresh floor is a coherence-time wall. 6G AI-native CSI
prediction can (a) track accurately within a coherence time and (b) beat
naive-hold by sqrt(2) via mean-reversion — but it **cannot extend the horizon
over which CSI is knowable**. You may refresh at the floor, or predict within a
coherence time of it; you cannot report past it and predict the gap away.

*Caveat:* real channels are not perfectly stationary/Gaussian — deep predictors
help where there is exploitable non-Gaussian structure (deterministic mobility,
beam/geometry priors, non-stationarity). The canonical Rayleigh model has none,
so it is the clean worst case for "prediction beats the floor," and prediction
loses. The `naive_horizon`/`extension` fields in `CSI-PREDICT.json` use a loose
error-budget reference and are superseded by this saturation analysis.
