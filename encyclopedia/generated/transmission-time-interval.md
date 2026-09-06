# transmission time interval

**id.** transmission-time-interval
**kind.** concept

## definition

The one-millisecond slot in which a 5G tower schedules a transmission, abbreviated TTI. Chapter 13.

## equation

Book equation 0.25.

    T_{\mathrm{coh}}=\frac{0.423}{f_D}.

Book equation 13.2.

    \begin{gathered} T_{\mathrm{coh}}=\frac{0.423}{f_D}, \\ \text{refuted fit:}\ \ \phi\approx0.177\,T_{\mathrm{coh}}\ (R^{2}=0.915), \qquad \text{sealed:}\ \ \phi\le 6\ \text{TTI at }10\ \text{Hz},\ \ 1\ \text{TTI at}\ \ge50\ \text{Hz}. \end{gathered}

## ledger

none

## first stated

Chapter 0 section 0.13 of *Data Mining as Observation*, with the program's sealed floors in `observation-theory-campaigns/experiments/RADIO-FRESHNESS-TRACK.md:20-35`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 13 section 13.3 | radio 0.27 to 0.42 naive to 0.055 to 0.13, neural reconstruction 0.28 to 0.13 | `observation-theory-campaigns\experiments\RADIO-FRESHNESS-TRACK.md:20-35` |
| chapter 13 section 13.4 | refuted fit 0.177 T_coh R² 0.915, 0.15 threshold vs 0.10 claim, fresh baseline 0.113, do not cite | `observation-theory-campaigns\analysis\csi\CSI-refreshfloor.json:2,111-114`; `observation-theory-campaigns\experiments\RADIO-FRESHNESS-TRACK.md:41-47` |

## failures and corrections

none

## conditions

- The one-millisecond slot in which a 5G tower schedules a transmission, abbreviated TTI. A duration of m milliseconds spans m slots, slots add over consecutive durations, and a longer duration spans more of them, which is the arithmetic the refresh floors are counted in.
- The sealed floors were 4, 1, and 1 slots at Doppler frequencies of 10, 50, and 400 hertz, and the earlier fit of the floor as a fixed fraction of the coherence time was refuted and is not to be cited.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/TTI.lean`, theorems `slots_of_ms`, `slots_add`, `slots_mono`, `slots_coherence`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 0, 13.

## related

block-error-rate, coherence-time, refresh-floor, freshness

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 8c6986b, observation-theory-campaigns 553a902, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
