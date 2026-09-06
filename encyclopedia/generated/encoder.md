# encoder

**id.** encoder
**kind.** concept

## definition

A model that maps an input to an embedding. Chapter 12.

## equation

Book equation 12.3.

    \text{validated}\iff \mathrm{AUROC}_{\text{cross}}-\max\big(\mathrm{AUROC}_{\text{untrained}},\ \mathrm{AUROC}_{\text{BoW}}\big)\ \ge\ 0.10.

Book equation 14.1.

    S=\frac{\sum_i w_i\,s_i}{\sum_i w_i},\qquad w_i=\max\big(0,\ 2\cdot\mathrm{AUROC}_i-1\big).

## ledger

- GO-B-legal (035→036). Legal-citation retrieval (CourtListener), cosine-ranking consumer, LaBSE embeddings — real large corpus, non-physical consumer `[predicted]`. `geometric-observation/claims/LEDGER.md:119` at 7d91883.

## first stated

Chapter 12 section 12.5 of *Data Mining as Observation*, with the program's encoders in xbse and the calibrated authority of `gtc-prototype/docs/CALIBRATED_AUTHORITY.md:19-63`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 8 section 8.6 | rights encoder 0.467 below untrained baseline, the AUROC lesson, cross-corpus same-sign fix | `xbse\README.md:160-172`; `xbse\experiments\rights_r6_summary.json` |
| chapter 12 section 12.5 | within 0.75 to 0.955 collapsing to 0.47 to 0.55, cross-corpus positives as the fix, adversary not load-bearing | `xbse\README.md:104-130,160-172` |
| chapter 12 section 12.5 | the gate, both nulls, margin 0.10, scorecard 0.622 to 0.853, bag of words 0.46 to 0.54, rights 0.509 vs 0.512 and 0.467 | `xbse\README.md:130-160,195-219` |
| chapter 12 section 12.5 | ECE 0.018 to 0.101 vs raw up to 0.223, reliability weight, audit binding | `xbse\README.md:175-195`; `gtc-prototype\docs\CALIBRATED_AUTHORITY.md:19-63` |
| chapter 14 section 14.1 | the three questions, the trust beats, the audit binding | `gtc-prototype\README.md:10-58`; `xbse\README.md:195-219` |
| chapter 14 section 14.2 | reliability weights and calibration errors per axis, the collapsed family's mean weight 0.559 against the general valence channel's own 0.735, the three design rules, 0.048 to 0.049 and 0.089 to 0.101 at 696 pairs | `gtc-prototype\docs\CALIBRATED_AUTHORITY.md:1-65` |

## failures and corrections

none

## conditions

- A model that maps an input to an embedding. An encoder votes only when its held-out AUROC on a corpus it was not trained on clears both nulls by the preregistered margin, its authority is its reliability weight, and a strictly monotone recalibration of its score changes neither the verdict nor the weight.
- The rights encoder fell below the untrained baseline and was retired rather than tuned, and the legal-citation encoder's flip is the ledger's demonstrated row.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/CrossCorpusGate.lean`, theorems `clears_bow`, `clears_untrained`, `not_validated_of_saturated`, `margin_example`, `validated_comp`, at observation-data-mining 1c6cd64.

## used in

*Data Mining as Observation* chapters 0, 7, 8, 9, 10, 11, 12, 14.

## related

embedding, cross-corpus-gate, reliability-weight, retrieval-augmented-pipeline

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 09cc919, theory-radar 37c4e6c, observation-data-mining 1c6cd64, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
