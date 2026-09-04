# coherence time

**id.** coherence-time
**kind.** concept

## definition

The interval over which a changing quantity stays correlated with itself. A value measured longer ago than the coherence time is a guess. Equation 0.25.

## equation

Book equation 0.25.

    T_{\mathrm{coh}}=\frac{0.423}{f_D}.

Book equation 13.2.

    \begin{gathered} T_{\mathrm{coh}}=\frac{0.423}{f_D}, \\ \text{refuted fit:}\ \ \phi\approx0.177\,T_{\mathrm{coh}}\ (R^{2}=0.915), \qquad \text{sealed:}\ \ \phi\le 6\ \text{TTI at }10\ \text{Hz},\ \ 1\ \text{TTI at}\ \ge50\ \text{Hz}. \end{gathered}

## ledger

- OT-4. Operator drift predicts a real long-generation degradation and a derived refresh intervention moves it. `[refuted]`. `geometric-observation/claims/LEDGER.md:36` at 7d91883.

## first stated

Clarke's model of mobile-radio reception for the formula, and Volume 14 chapter 19 for its role as the interval past which a certificate has decorrelated.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 13 section 13.3 | radio 0.27 to 0.42 naive to 0.055 to 0.13, neural reconstruction 0.28 to 0.13 | `observation-theory-campaigns\experiments\RADIO-FRESHNESS-TRACK.md:20-35` |
| chapter 13 section 13.4 | refuted fit 0.177 T_coh R² 0.915, 0.15 threshold vs 0.10 claim, fresh baseline 0.113, do not cite | `observation-theory-campaigns\analysis\csi\CSI-refreshfloor.json:2,111-114`; `observation-theory-campaigns\experiments\RADIO-FRESHNESS-TRACK.md:41-47` |
| chapter 13 section 13.4 | sealed correction, 0.5 dB calibration, floors 4/6/4, 2/2/3, 1, slopes 0.1008, 0.1398, 0.1086, R² 0.7376, 0.9218, 0.6174, bars B1 to B4 and MC1 to MC4 all true, seeds 20260827 to 20260829, sealed 1d3de4a | `observation-theory-campaigns\analysis\csi\PREREG-XPROTO-CSI-SWEEP2.md:1-60`; `observation-theory-campaigns\analysis\csi\XPROTO-CSI-SWEEP2-graded.json`; `observation-theory-campaigns\experiments\SEALS.md:90` |

## failures and corrections

- OT-4, `[refuted]`. Operator drift predicts a real long-generation degradation and a derived refresh intervention moves it.
- `observation-theory-campaigns/experiments/RADIO-FRESHNESS-TRACK.md:41-50` at 4d22223. **The age horizon** (`analysis/csi/`, XPROTO-CSI-SWEEP2 sealed 2026-08-27, graded PASS): at the calibrated 0.10 budget the largest compliant report period is a few TTI at 10 Hz and 1 TTI at 50 Hz and above, so there is no proportionality law to fit. The earlier `CSI-refreshfloor.*` claim of a floor ≈ 0.177·T_coh (R²=0.915) was an **unsealed exploration** measured at a relaxed 0.15 threshold against the 0.10 target, with a fresh baseline that never met the budget. It is refuted; the record is kept, not cited. Separately, the optimal linear predictor cannot beat the one-coherence-time wall (Gaussian fading → Wiener optimal), and that wall sits well outside the budget horizon. The **RAN governor** (`analysis/ran`) is the reference O-RAN rApp core: observe→measure false-clear→refresh at the floor→escalate (diversity / re-route).

## conditions

- Clarke's formula gives the coherence time from the Doppler frequency alone and assumes the fading model behind it.
- A value measured longer ago than the coherence time is a guess, and a certificate issued that long ago has decorrelated from the state it certified.
- The proportional refresh-floor law that was fit to it was refuted and is not cited. Its sealed replacement calibrated the baseline first and found floors at a few transmission intervals.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/CoherenceTime.lean`, theorems `clarke_to_three_decimals`, `examples`, `refuted_law_exceeds_sealed`, at observation-data-mining 2b1108b.

## used in

*Data Mining as Observation* chapters 0, 13.

## related

certificate, false-clear-rate, refresh-floor, witness

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 4d22223, theory-radar 37c4e6c, observation-data-mining 2b1108b, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
