# fine-tuning

**id.** fine-tuning
**kind.** instrument

## definition

Continuing to train an encoder on a new objective or corpus, so that its quotient changes. Chapter 11 section 11.8 and chapter 12 section 12.4.

## equation

Book equation 12.3.

    \text{validated}\iff \mathrm{AUROC}_{\text{cross}}-\max\big(\mathrm{AUROC}_{\text{untrained}},\ \mathrm{AUROC}_{\text{BoW}}\big)\ \ge\ 0.10.

Book equation 11.1.

    \cos\big(k,\hat k\big)=0.995\qquad\text{while}\qquad \mathrm{PPL}:\ 12.24\ \to\ 10643.

## ledger

- GO-B-Llama. Trained frontier LLM (Llama-3.2-3B), softmax-attention consumer — blind probe on real post-RoPE keys `[predicted]`. `geometric-observation/claims/LEDGER.md:115` at 9f3829f.
- GO-B-Llama-rematch. Trained frontier LLM (Llama-3.2-3B), softmax-attention consumer — recon-matched dissociation on real post-RoPE keys `[predicted]`. `geometric-observation/claims/LEDGER.md:118` at 9f3829f.
- GO-B-legal (035→036). Legal-citation retrieval (CourtListener), cosine-ranking consumer, LaBSE embeddings — real large corpus, non-physical consumer `[predicted]`. `geometric-observation/claims/LEDGER.md:119` at 9f3829f.

## first stated

Chapter 11 section 11.8 and chapter 12 section 12.4 of *Data Mining as Observation*, with the translation-trained encoder in `turboquant-pro/docs/RESULTS_multilingual_strata.md:55-90`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 10 section 10.4 | first run, 350000 of 2391361 rows, 7 of 14 eligible, abstentions with 2 and 1 rows, Robin Hood 0.3447 to 0.4469 ratio 1.30 against 1.5, skew 2.68 to 4.40 ratio 1.64 against 3, 63 times sample range | `turboquant-pro\docs\RESULTS_multilingual_strata.md:1-55` |
| chapter 10 section 10.4 | second prediction inverted, transit 0.389 vs 0.291, centrality difference signs, share 0.473 vs 0.391, seven of thirteen backbone | `turboquant-pro\docs\RESULTS_multilingual_strata.md:55-90`; `turboquant-pro\docs\STRATA_RFC.md:98-130` |
| chapter 11 section 11.8 | 0.765 to 0.971 with interval 0.190 to 0.223, 0.545 to 0.562 with interval 0.004 to 0.031, v1 0.340 with interval negative 0.214 to negative 0.081, anisotropy 0.570 to 0.259 | `lebse\README.md:40-75`; `lebse\PAPER.md:1-15,60-66`; `lebse\MODEL_CARD.md:48-52` |
| chapter 12 section 12.4 | 0.765 to 0.971, 0.545 to 0.562, v1 0.340, cosine 0.570 to 0.259 | `lebse\README.md:40-75`; `lebse\PAPER.md:1-15,60-66` |
| chapter 12 section 12.4 | seven of thirteen backbone areas under the translation-trained encoder, all local-hub under the general one | `turboquant-pro\docs\RESULTS_multilingual_strata.md:55-90` |
| chapter 12 section 12.5 | within 0.75 to 0.955 collapsing to 0.47 to 0.55, cross-corpus positives as the fix, adversary not load-bearing | `xbse\README.md:104-130,160-172` |

## failures and corrections

none

## conditions

- Continuing to train an encoder on a new objective or corpus, so that its quotient changes. A contrastive objective pulls declared pairs together, and the cross-corpus gate asks whether the tuned encoder still separates on a corpus it never saw.
- An encoder fine-tuned on one relation is evaluated on that relation and on one it never saw, with a paired interval on each, and the within-corpus score of 0.75 to 0.955 collapsed to 0.47 to 0.55 across corpora until cross-corpus positives were added.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Contrastive.lean`, theorems `loss_nonneg`, `loss_eq_zero_iff`, `not_both`, `loss_mono_margin`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/CrossCorpusGate.lean`, theorems `clears_bow`, `clears_untrained`, `not_validated_of_saturated`, `margin_example`, `validated_comp`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 11, 12.

## related

contrastive-objective, encoder, cross-corpus-gate, leakage, paraphrase-class

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
