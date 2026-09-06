# operating point

**id.** operating-point
**kind.** concept

## definition

The row at which a consumer is read, or the threshold at which a classifier is scored. A probe pays 2d evaluations for one. Chapter 0 section 0.5 and chapter 11 section 11.7.

## equation

Book equation 0.8.

    g_j\;\approx\;\frac{C(x+h\,e_j)-C(x-h\,e_j)}{2h},\qquad j=1,\dots,d.

Book equation 11.4.

    \text{directions resolved}(k)=\begin{cases}1\ \text{or}\ 2,& k<d\\[2pt] \operatorname{rank}P_C,& k\ge d\end{cases}\qquad \text{cost}=2d\ \text{consumer calls per operating point}.

Book equation 0.28.

    P=\frac{TP}{TP+FP},\qquad R=\frac{TP}{TP+FN},\qquad F_1=\frac{2PR}{P+R}.

## ledger

- OT-3. Under subspace-confined second-order transcripts, fewer than d directions cannot identify a hidden leading eigenspace (theorem, adaptive to d−2 / oblivious to d−1); a known k₀-dim exclusion moves the cliff to exactly d−k₀ and never softens it. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:31` at 9f3829f.
- GO-4. Fixed-budget verdicts invert under budget-matched observation, per the wavelength mechanism. `[replicated]`. `geometric-observation/claims/LEDGER.md:66` at 9f3829f.

## first stated

Chapter 0 section 0.5 and chapter 11 section 11.7 of *Data Mining as Observation*, with the budget law in `readscope/README.md:118-141`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 11 section 11.7 | k over d table 1, 2, 2, 16, 16, 16 | `readscope\README.md:118-141`; `readscope\SPEC.md:243-285`, record `readscope\calibration\records\c2e-budget-law.json` |
| chapter 11 section 11.7 | rank-independent, 0.646 vs 0.366 at half dimension, never 0.90 below k equals d | `readscope\CALIBRATION.md:419-434` F-15 |
| chapter 11 section 11.7 | C-15 equal budget, 3072 observations, medians 0.02, 0.11, 0.05, 0.04, 1.0, 1.0, margin 0.883 vs 0.3, 0.062 to 0.057 at 8x | `readscope\SPEC.md:285-323`, record `readscope\calibration\records\c15-budget-surface.json`, `readscope\calibration\DECLARATION-C15.md` |

## failures and corrections

none

## conditions

- The row at which a consumer is read, or the threshold at which a classifier is scored. A central-difference probe pays two evaluations per coordinate for one operating point, and raising a classifier's threshold can only shrink the set it calls positive.
- Whether many cheaper operating points can average their way back to the population operator was measured within a budget range and not proved, and the cliff at k equal to d does not soften for a probe confined to the directions it chooses.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/FiniteDifference.lean`, theorems `central_quad`, `forward_quad`, `forward_error`, `central_cost`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Threshold.lean`, theorems `predicted_anti`, `tp_anti`, `fp_anti`, `decision_comp`, `predicted_extremes`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 2, 5, 6, 11, 14.

## related

finite-difference, budget, budget-cliff, threshold, blind-probe

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
