# cross-corpus gate

**id.** cross-corpus-gate
**kind.** instrument

## definition

The validation rule that an encoder votes only if its held-out AUROC on a corpus it was not trained on clears a preregistered margin over a bag-of-words null. Chapters 12 and 14.

## equation

Book equation 12.3.

    \text{validated}\iff \mathrm{AUROC}_{\text{cross}}-\max\big(\mathrm{AUROC}_{\text{untrained}},\ \mathrm{AUROC}_{\text{BoW}}\big)\ \ge\ 0.10.

Book equation 0.16.

    \mathrm{AUROC}=\Pr\big[s^{+}>s^{-}\big]\ +\ \tfrac12\Pr\big[s^{+}=s^{-}\big].

## ledger

none

## first stated

The moral-embedding program, `xbse/README.md:104-130,160-172`, and chapter 12 section 12.5 and chapter 14 section 14.2 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 8 section 8.6 | rights encoder 0.467 below untrained baseline, the AUROC lesson, cross-corpus same-sign fix | `xbse\README.md:160-172`; `xbse\experiments\rights_r6_summary.json` |
| chapter 12 section 12.5 | within 0.75 to 0.955 collapsing to 0.47 to 0.55, cross-corpus positives as the fix, adversary not load-bearing | `xbse\README.md:104-130,160-172` |

## failures and corrections

none

## conditions

- An encoder votes only if its held-out AUROC on a corpus it was not trained on clears both nulls, the untrained encoder and the bag-of-words baseline, by the preregistered margin of one tenth. A validated encoder therefore beats each null by the margin.
- Since AUROC is at most one, a null above nine tenths cannot be cleared by any encoder, and the gate's verdict is unchanged by any strictly monotone recalibration of the score.
- The rights encoder fell below the untrained baseline and was retired rather than tuned, and the within-corpus scores that had collapsed on a second corpus were the reason the gate is cross-corpus.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/CrossCorpusGate.lean`, theorems `clears_bow`, `clears_untrained`, `not_validated_of_saturated`, `margin_example`, `validated_comp`, at observation-data-mining 8d458b2.

## used in

*Data Mining as Observation* chapters 8, 12, 14.

## related

reliability-weight, harness, leakage, preregistration

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 429cc9d, theory-radar 37c4e6c, observation-data-mining 8d458b2, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
