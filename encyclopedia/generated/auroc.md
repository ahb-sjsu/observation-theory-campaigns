# AUROC

**id.** auroc
**kind.** concept

## definition

The area under the receiver operating characteristic curve, equal to the probability that a random positive scores above a random negative, ties counted as one half. Equation 0.16.

## equation

Book equation 0.16.

    \mathrm{AUROC}=\Pr\big[s^{+}>s^{-}\big]\ +\ \tfrac12\Pr\big[s^{+}=s^{-}\big].

Book equation 0.38.

    w=\max\big(0,\ 2\cdot\mathrm{AUROC}-1\big).

Book equation 12.3.

    \text{validated}\iff \mathrm{AUROC}_{\text{cross}}-\max\big(\mathrm{AUROC}_{\text{untrained}},\ \mathrm{AUROC}_{\text{BoW}}\big)\ \ge\ 0.10.

## ledger

- GO-B-legal (035→036). Legal-citation retrieval (CourtListener), cosine-ranking consumer, LaBSE embeddings — real large corpus, non-physical consumer `[predicted]`. `geometric-observation/claims/LEDGER.md:119` at 9f3829f.
- GO-B-whale (038). Sperm-whale coda dialect (DSWP/Sharma 2024), Clan classifier — cetacean communication; promotes the exploratory (A2) verdict to a sealed flip `[predicted]`. `geometric-observation/claims/LEDGER.md:120` at 9f3829f.

## first stated

Chapter 0 section 0.8 of *Data Mining as Observation*, the pairwise definition with ties counted one half, and the held-out AUROC of every encoder gate and flip in the program.

## measurements

none

## failures and corrections

none

## conditions

- The probability that a random positive scores above a random negative, ties counted one half. It lies in the unit interval, is one when every positive scores above every negative and zero when every negative scores above every positive, is one half for a constant score, and is unchanged by a strictly monotone transform of the score.
- It reads the ranking and not the values, so it is the discrimination half of every encoder's validation and says nothing about calibration.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Auroc.lean`, theorems `pair_nonneg`, `auroc_nonneg`, `auroc_le_one`, `auroc_perfect`, `auroc_reversed`, `auroc_chance`, `auroc_monotone_invariant`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 0, 5, 6, 8, 11, 12, 14.

## related

monotone-invariance, reliability-weight, chance-level, youden-f1-bound, cross-corpus-gate

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
