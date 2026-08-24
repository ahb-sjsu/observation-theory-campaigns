# Markets-Freshness Track: microstructure staleness certificates

**Status:** re-homed 2026-08-24 from `network-governor`. Chip 🕒📈 MKT. Freshness
program ([FRESHNESS-PROGRAM.md](FRESHNESS-PROGRAM.md)). UNSEALED — sealed rung
gated on real tick data (`quote_check` refuses to seal on the sim model rung).

## Question

A market-maker **quote** is a certificate ("this price is live"). The consumer is
the book, with half-spread `s` as its read operator. The quote **false-clears**
under **adverse selection**: the efficient mid moved beyond the quote before the
fill. Witness = the realized mid; correction = a price-triggered re-quote; the
refresh floor scales with spread-coherence `(s/σ)²`. Consumer-relative: a tight
book (small `s`) false-clears far more than a wide book on the same path.

## Cells

- **XPROTO-QUOTE** (`analysis/econ/fam_quote.py`, `quote_check.py`): stale-quote /
  adverse-selection. Model rung (efficient-price random walk — validation, NOT
  evidence): naive_fc ~0.37 / witnessed ~0.012 / fresh ~0.003; same path tight
  (s=2) 0.53 vs wide (s=6) 0.12. Sealed rung = real tick data (gated).
- **Portfolio `tr(P·Σ)` demo** (`analysis/econ/quant_portfolio.py`): the finance
  KV-keys twin — a 99.02%-variance PCA model rates the min-var-under-model book
  near-riskless (tr under-reported 3064×), its 99% VaR breaches 48% of realized
  returns (nominal 1%) while consumer-aware VaR holds at 1.02%. The book loads onto
  the model's blind spot: reconstruction is blind to the consumer's direction —
  the same lesson as turboquant KV-keys / XPROTO-AICSI.

## Seal path

Real intraday tick data (a quote/trade feed); `quote_check.py` refuses to seal on
the simulator. Clean cross-domain companion to the routing/DB/radio/quantum cells:
the witnessed-certificate grammar in market microstructure.
