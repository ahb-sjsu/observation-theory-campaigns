# refresh interval

**id.** refresh-interval
**kind.** instrument

## definition

The longest renewal period that keeps a certificate within its promised error, a measured property of the system and not a convention. Chapter 13.

## equation

Book equation 13.2.

    \begin{gathered} T_{\mathrm{coh}}=\frac{0.423}{f_D}, \\ \text{refuted fit:}\ \ \phi\approx0.177\,T_{\mathrm{coh}}\ (R^{2}=0.915), \qquad \text{sealed:}\ \ \phi\le 6\ \text{TTI at }10\ \text{Hz},\ \ 1\ \text{TTI at}\ \ge50\ \text{Hz}. \end{gathered}

Book equation 0.25.

    T_{\mathrm{coh}}=\frac{0.423}{f_D}.

Book equation 0.26.

    \mathrm{FC}=\Pr\big[W\ \text{refutes}\ \big|\ \mathcal C_t\ \text{clears}\big],\qquad \text{coverage}=\Pr\big[\mathcal C_t\ \text{clears}\big].

## ledger

- OT-4. Operator drift predicts a real long-generation degradation and a derived refresh intervention moves it. `[refuted]`. `geometric-observation/claims/LEDGER.md:36` at 9f3829f.

## first stated

Chapter 13 section 13.2 of *Data Mining as Observation*, with the sealed floors in `observation-theory-campaigns/experiments/RADIO-FRESHNESS-TRACK.md:20-35` and the refuted fit in `observation-theory-campaigns/analysis/csi/CSI-refreshfloor.json`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 13 section 13.3 | radio 0.27 to 0.42 naive to 0.055 to 0.13, neural reconstruction 0.28 to 0.13 | `observation-theory-campaigns\experiments\RADIO-FRESHNESS-TRACK.md:20-35` |
| chapter 13 section 13.4 | refuted fit 0.177 T_coh R² 0.915, 0.15 threshold vs 0.10 claim, fresh baseline 0.113, do not cite | `observation-theory-campaigns\analysis\csi\CSI-refreshfloor.json:2,111-114`; `observation-theory-campaigns\experiments\RADIO-FRESHNESS-TRACK.md:41-47` |
| chapter 13 section 13.4 | freshness sweep classes, sensing refuted at about 1.6 times | `geometric-observation\BOOK-OUTLINE.md:70-90` |

## failures and corrections

- OT-4, `[refuted]`. Operator drift predicts a real long-generation degradation and a derived refresh intervention moves it.

## conditions

- The longest renewal period that keeps a certificate within its promised error, a measured property of the system and not a convention. A certificate older than the interval is stale for every consumer whose floor is shorter, and the floors are counted in slots that add over consecutive durations.
- There is no proportionality law between the interval and the coherence time. The fit of the floor as 0.177 of the coherence time was refuted and is not to be cited, and the sealed floors were 4, 1, and 1 slots at 10, 50, and 400 hertz.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/CoherenceTime.lean`, theorems `clarke_to_three_decimals`, `examples`, `refuted_law_exceeds_sealed`, at observation-data-mining 5bb2c0d.

`lean/DataMiningAsObservation/TTI.lean`, theorems `slots_of_ms`, `slots_add`, `slots_mono`, `slots_coherence`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 13, 14.

## related

refresh-floor, coherence-time, certificate, false-clear-rate, transmission-time-interval

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
