# block error rate

**id.** block-error-rate
**kind.** concept

## definition

The fraction of transmitted radio blocks the receiver cannot decode, abbreviated BLER. Chapter 13.

## equation

Book equation 13.2.

    \begin{gathered} T_{\mathrm{coh}}=\frac{0.423}{f_D}, \\ \text{refuted fit:}\ \ \phi\approx0.177\,T_{\mathrm{coh}}\ (R^{2}=0.915), \qquad \text{sealed:}\ \ \phi\le 6\ \text{TTI at }10\ \text{Hz},\ \ 1\ \text{TTI at}\ \ge50\ \text{Hz}. \end{gathered}

Book equation 0.25.

    T_{\mathrm{coh}}=\frac{0.423}{f_D}.

## ledger

- OT-4. Operator drift predicts a real long-generation degradation and a derived refresh intervention moves it. `[refuted]`. `geometric-observation/claims/LEDGER.md:36` at 7d91883.
- OT-11. Feedback-free staleness: streaming-retrieval damage tracks measured drift; derived-cadence re-allocation removes it. `[void]`. `geometric-observation/claims/LEDGER.md:48` at 7d91883.

## first stated

Chapter 13 section 13.4 of *Data Mining as Observation*, with the radio freshness track, `observation-theory-campaigns/experiments/RADIO-FRESHNESS-TRACK.md:20-35`, and the sealed sweep `observation-theory-campaigns/analysis/csi/PREREG-XPROTO-CSI-SWEEP2.md`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 13 section 13.3 | radio 0.27 to 0.42 naive to 0.055 to 0.13, neural reconstruction 0.28 to 0.13 | `observation-theory-campaigns\experiments\RADIO-FRESHNESS-TRACK.md:20-35` |
| chapter 13 section 13.4 | refuted fit 0.177 T_coh R² 0.915, 0.15 threshold vs 0.10 claim, fresh baseline 0.113, do not cite | `observation-theory-campaigns\analysis\csi\CSI-refreshfloor.json:2,111-114`; `observation-theory-campaigns\experiments\RADIO-FRESHNESS-TRACK.md:41-47` |
| chapter 13 section 13.4 | sealed correction, 0.5 dB calibration, floors 4/6/4, 2/2/3, 1, slopes 0.1008, 0.1398, 0.1086, R² 0.7376, 0.9218, 0.6174, bars B1 to B4 and MC1 to MC4 all true, seeds 20260827 to 20260829, sealed 1d3de4a | `observation-theory-campaigns\analysis\csi\PREREG-XPROTO-CSI-SWEEP2.md:1-60`; `observation-theory-campaigns\analysis\csi\XPROTO-CSI-SWEEP2-graded.json`; `observation-theory-campaigns\experiments\SEALS.md:90` |

## failures and corrections

- OT-4, `[refuted]`. Operator drift predicts a real long-generation degradation and a derived refresh intervention moves it.
- `observation-theory-campaigns/experiments/RADIO-FRESHNESS-TRACK.md:41-50` at 09cc919. **The age horizon** (`analysis/csi/`, XPROTO-CSI-SWEEP2 sealed 2026-08-27, graded PASS): at the calibrated 0.10 budget the largest compliant report period is a few TTI at 10 Hz and 1 TTI at 50 Hz and above, so there is no proportionality law to fit. The earlier `CSI-refreshfloor.*` claim of a floor ≈ 0.177·T_coh (R²=0.915) was an **unsealed exploration** measured at a relaxed 0.15 threshold against the 0.10 target, with a fresh baseline that never met the budget. It is refuted; the record is kept, not cited. Separately, the optimal linear predictor cannot beat the one-coherence-time wall (Gaussian fading → Wiener optimal), and that wall sits well outside the budget horizon. The **RAN governor** (`analysis/ran`) is the reference O-RAN rApp core: observe→measure false-clear→refresh at the floor→escalate (diversity / re-route).

## conditions

- The fraction of transmitted radio blocks the receiver cannot decode, in the unit interval. A block of n symbols each lost independently with probability q fails with probability one minus one minus q to the n, at most n q, never falling as the block grows, and equal to q for a single symbol.
- The measured rates of the radio track and the refuted refresh law fit against them are the ledger's numbers, with the sealed sweep's calibrated baseline as the correction.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/BlockErrorRate.lean`, theorems `bler_mem_unit`, `blockFail_le`, `blockFail_mono`, `blockFail_one`, `blockFail_zero`, at observation-data-mining 1c6cd64.

## used in

*Data Mining as Observation* chapters 0.

## related

coherence-time, refresh-floor, freshness, false-clear-rate

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 09cc919, theory-radar 37c4e6c, observation-data-mining 1c6cd64, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
