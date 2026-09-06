# baseline

**id.** baseline
**kind.** instrument

## definition

The simplest scorer a claim must beat under the same protocol, chance, a constant, an untrained encoder, or a single model. A score below it is a finding. Chapter 6 section 6.3 and chapter 7 section 7.4.

## equation

Book equation 8.2.

    \begin{gathered} \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2}, \\ J=1000,\ \frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}=\frac14\ \Rightarrow\ 1+250=251,\ \ \sqrt{251}=15.84. \end{gathered}

Book equation 0.28.

    P=\frac{TP}{TP+FP},\qquad R=\frac{TP}{TP+FN},\qquad F_1=\frac{2PR}{P+R}.

Book equation 6.2.

    \begin{gathered} \max_{\tau,\ \mathrm{dir}}F_1\!\Big(\mathbf 1\big[\mathrm{dir}\big(g(f(X)),\tau\big)\big],\,y\Big)=\max_{\tau,\ \mathrm{dir}}F_1\!\Big(\mathbf 1\big[\mathrm{dir}\big(f(X),\tau\big)\big],\,y\Big) \\ \text{for every strictly monotone } g. \end{gathered}

## ledger

- NEG-4. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL. `[refuted]`. `geometric-observation/claims/LEDGER.md:97` at 9f3829f.
- GO-B-legal (035→036). Legal-citation retrieval (CourtListener), cosine-ranking consumer, LaBSE embeddings — real large corpus, non-physical consumer `[predicted]`. `geometric-observation/claims/LEDGER.md:119` at 9f3829f.

## first stated

Chapter 6 section 6.3 and chapter 7 section 7.4 of *Data Mining as Observation*, with the single-model baseline in `constraint-gap/review/INDETERMINATES.md:1-40`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 6 section 6.3 | the five-dataset table, breast cancer 0.955 to 0.963, the pattern, DOI 10.5281/zenodo.20660206 | `theory-radar\README.md:100-140` |
| chapter 7 section 7.3 | the five-dataset outcomes | `theory-radar\README.md:100-140` |
| chapter 7 section 7.4 | nine to three, seventeen indeterminate, five analyses zero resolved, three re-encode the correction | `constraint-gap\review\INDETERMINATES.md:1-40` |
| chapter 8 section 8.6 | rights encoder 0.467 below untrained baseline, the AUROC lesson, cross-corpus same-sign fix | `xbse\README.md:160-172`; `xbse\experiments\rights_r6_summary.json` |

## failures and corrections

- NEG-4, `[refuted]`. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL.

## conditions

- The simplest scorer a claim must beat, chance, a constant, an untrained encoder, or a single model, run under the same protocol. A baseline that passes the bar makes the bar vacuous, and a score below the baseline is a finding.
- The rights encoder read 0.467, below the untrained baseline, and the formula's comparison with the ensemble is fair only against the single-model baseline inside one fold protocol.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ChanceLevel.lean`, theorems `aurocNum_const`, `auroc_const`, `weight_const`, `tau_const`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Bar.lean`, theorems `passes_anti`, `passes_mono`, `discriminates_iff`, `no_bar_of_null_ge`, `exists_bar_of_lt`, `vacuous_of_null_passes`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 5, 6, 7, 8, 10, 11, 12, 13, 14.

## related

chance-level, null-model, bar, formula-classifier, ensemble

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
