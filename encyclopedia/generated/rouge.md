# ROUGE

**id.** rouge
**kind.** concept

## definition

A family of scores for generated text against a reference. Chapter 0 section 0.11.

## equation

Book equation 0.22.

    \mathrm{PPL}=2^{H},\qquad H=-\frac1T\sum_{t=1}^{T}\log_2 p\big(w_t\mid w_{<t}\big).

## ledger

- NEG-4. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL. `[refuted]`. `geometric-observation/claims/LEDGER.md:97` at 9f3829f.

## first stated

Lin, ROUGE, 2004, as chapter 0 section 0.11 states it, with the program's 13.7 ROUGE-L number and its re-validation in `turboquant-pro/CLAIMS.md:63-81`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 8 section 8.9 | 13.7 ROUGE-L, 0.25/4.19/9.60/13.7 at 64/128/256/512, re-validation negative 0.31 n=40, 26.64 under symmetric nf4, `_quant_nf4a_group` unchanged since `289bdfc` before `4f7baab` | `turboquant-pro\CLAIMS.md:63-81`; `turboquant-pro\benchmarks\kvquant_matrix\REVAL-2026-08-08.md` |

## failures and corrections

- NEG-4, `[refuted]`. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL.

## conditions

- A family of scores for generated text against a reference. ROUGE-1 recall counts the reference's words the candidate contains, with multiplicity, over the reference's length. It lies in the unit interval, is one for the reference itself, and is one for any rearrangement of the reference, since it reads bags and not order.
- A ROUGE score therefore certifies less than it seems to. The 13.7 ROUGE-L difference at 512 tokens re-validated at negative 0.31 on forty documents, and the claims ledger carries both numbers.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Rouge.lean`, theorems `overlap_le`, `rouge1_mem_unit`, `rouge1_self`, `rouge1_perm`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 8.

## related

bag-of-words, perplexity, harness, certificate

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
