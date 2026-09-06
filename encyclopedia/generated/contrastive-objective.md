# contrastive objective

**id.** contrastive-objective
**kind.** concept

## definition

A training rule that pulls pairs declared similar together and pushes other pairs apart. The declared pairs are where an encoder learns what similar means. Chapter 12.

## equation

Book equation 12.3.

    \text{validated}\iff \mathrm{AUROC}_{\text{cross}}-\max\big(\mathrm{AUROC}_{\text{untrained}},\ \mathrm{AUROC}_{\text{BoW}}\big)\ \ge\ 0.10.

Book equation 11.1.

    \cos\big(k,\hat k\big)=0.995\qquad\text{while}\qquad \mathrm{PPL}:\ 12.24\ \to\ 10643.

## ledger

- NEG-2. Reconstruction cosine as a proxy for key quality. `[refuted]`. `geometric-observation/claims/LEDGER.md:95` at 9f3829f.
- GO-B-legal (035→036). Legal-citation retrieval (CourtListener), cosine-ranking consumer, LaBSE embeddings — real large corpus, non-physical consumer `[predicted]`. `geometric-observation/claims/LEDGER.md:119` at 9f3829f.

## first stated

Chapter 12 section 12.4 of *Data Mining as Observation*, with the program's encoders in xbse, `xbse/README.md:104-130`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 12 section 12.5 | within 0.75 to 0.955 collapsing to 0.47 to 0.55, cross-corpus positives as the fix, adversary not load-bearing | `xbse\README.md:104-130,160-172` |

## failures and corrections

- NEG-2, `[refuted]`. Reconstruction cosine as a proxy for key quality.

## conditions

- A training rule that pulls pairs declared similar together and pushes other pairs apart. With a margin loss the loss is nonnegative, zero exactly when every declared pair scores above every other pair by the margin, and never lower for a larger margin.
- Swapping which pairs are declared similar reverses that condition, and with a positive margin no scorer satisfies both, so the declared pairs are where an encoder learns what similar means. Fine-tuning moves the reader, and the cross-corpus positives were the fix when within-corpus scores collapsed.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Contrastive.lean`, theorems `loss_nonneg`, `loss_eq_zero_iff`, `not_both`, `loss_mono_margin`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 11, 12.

## related

encoder, embedding, cross-corpus-gate, quotient

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
