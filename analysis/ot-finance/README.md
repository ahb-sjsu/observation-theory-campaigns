# OT-finance — the consumer-relative staleness law (UNSEALED, exploratory)

Owner go 2026-09-02 (sweep-first per the mined-domain rule). Claim under
construction: staleness is a property of (feed, consumer), governed by
u = σ√L/d — the refresh floor scales with the consumer's threshold distance,
and one feed at one lag is simultaneously stale for a near-threshold consumer
and fresh for a far one. Zero live exposure: Binance public bulk data,
no keys, no orders.

## Prior-art sweep (2026-09-02, arXiv; before building)

Age-of-Information / Age-of-Incorrect-Information: 15 papers checked — all
transmitter-side policy optimization; none derive a consumer-threshold refresh
floor, none use the verdict-flip framing, none touch financial data. Closest
match anywhere: Barzykin 2026 (FX dealer slippage/rejection under latency) —
a single dealer's optimal staleness *response*, i.e., control design for one
consumer; our object is the cross-consumer *law*. DeFi oracle work (ZeroSwap
2023) is adaptive pricing, not staleness laws. "First passage" × "stale price"
returns zero on arXiv. Stale-NAV and latency-arbitrage literatures document
the phenomenon as profits, not as a refresh-floor law.

## Shakedown (2026-09-02, `ot_staleness_shakedown.py`, predictions committed 4cf6dd7 BEFORE running)

BTCUSDT + ETHUSDT aggTrades, 2026-08-28 (1.27M / 0.99M trades), 100 ms price
grid, 286 five-minute windows per symbol; liquidation-style monitors at
d ∈ {2..50} bps; lags L ∈ {0.1..30} s. **Disclosed instrument bug:** the first
run treated Binance's microsecond timestamps as ms, shrinking every lag 1000×
(degenerate zero-flip output; fix + rerun at 0c842d3; predictions unchanged).

| prediction | bar | BTC | ETH | verdict |
|---|---|---|---|---|
| P1 collapse in u = σ√L/d | Spearman ≥ 0.9, iso-R² ≥ 0.85 | 0.940 / 0.970 | 0.959 / 0.965 | **PASS both** |
| P2 cross-consumer split @ L=3s | ratio ≥ 20× AND far ≤ 0.1% | 86× / 0.026% | 24× / **0.114%** | **BTC pass, ETH fail** on the absolute clause |
| P3 refresh-floor exponent | slope 2 ± 0.4 | **0.57** | **0.87** | **FAIL both** |
| P4 vol-regime collapse | max gap ≤ 20% | 82% | 59% | **FAIL both** |
| P5 replication (ETH P1) | as P1 | — | pass | **PASS** |

The flip profile at L = 3 s is the consumer-relative statement in one line
(BTC): d = 2 bps flips 2.2% of decisions, d = 50 bps flips 0.03% — the same
feed, at the same lag, is operationally stale for one consumer and fresh for
another, and the gradient between them is monotone (2.2 / 1.5 / 0.9 / 0.5 /
0.03%).

## Honest read

**The consumer-relative core is confirmed at shakedown grade** (P1 + P2-BTC +
P5): flip rates collapse on the dimensionless ratio u across a 25× range of
thresholds and a 300× range of lags, on two assets, with the verdict split
demonstrated. **The diffusive idealization is refuted in its quantitative
details** (P3, P4), and both failures point at the same known physics:

1. P3's shallow exponent (0.57/0.87 vs the first-passage 2) is partly grid
   quantization (L* saturated at the coarse lag grid, two ties in four
   points) but mainly the variance signature: at sub-second scales price is
   not Brownian (microstructure noise, jumps), so short-lag effective vol is
   higher than √L-scaled 1s vol, and near consumers flip sooner than
   diffusion predicts — the refresh floor is FLATTER in d than d².
2. P4's regime gap says a single per-window σ from 1 s returns does not
   absorb regime structure — the same signature effect plus vol clustering.
3. P2-ETH's absolute-clause failure is law-consistent: ETH's higher vol
   raises u at fixed (d, L), so the far consumer starts flipping too — the
   clause should have been stated at matched u, not matched L. The bar stays
   failed as written.

**Successor cell (the instrument upgrade, pre-registerable):** replace the
single σ with the lag-matched signature vol σ(L) (realized variance at
horizon L), define u_sig = σ(L)√L/d... i.e., u = (expected |move| over L)/d
directly. Prediction: P3's exponent recovers toward the signature-implied
slope and P4's regime gap closes. If it does, the refresh-floor law survives
with the honest vol estimator; if not, the deviation is structure worth
keeping (jump-dominated flips).

## Next

1. Signature-vol successor cell (above), then a second day + a non-crypto
   feed (CAISO LMP or GTFS-realtime) for family breadth.
2. Prereg with the V2 instrument; the P3787 attestation clause inherits
   whichever refresh-floor form survives ([[project_standards_p3787]] note).
