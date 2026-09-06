# matched bits

**id.** matched-bits
**kind.** instrument

## definition

The rule that two codes are compared only at the same bit count. At matched bits two codes with equal reconstruction error can still differ for a reader, which is the flip. Chapter 4 section 4.3.

## equation

Book equation 4.2.

    D(b)=\sum_i s_i\sigma_i^{2}\,2^{-2b_i},\qquad s_i=v_i^{\top}P_C\,v_i,\qquad b_i^{\star}=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i\sigma_i^{2}}{\theta}\Big),\qquad \sum_i b_i^{\star}=B,

Book equation 4.6.

    \kappa=\operatorname{tr}\big(\bar P_C\,\bar\Sigma_x\big)\in[0,1],\qquad \kappa\to1\ \text{is the coupling null (no flip)}.

Book equation 0.15.

    \tau=\frac{\#\{\text{concordant pairs}\}-\#\{\text{discordant pairs}\}}{n(n-1)/2}.

## ledger

- GO-2 (neg. half: not reconstruction). At matched bits, downstream preservation is not controlled by reconstruction error. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:63` at 9f3829f.
- GO-2 (pos. half: consumer-projected covariance *controls*). Downstream preservation is controlled by the error covariance projected on the consumer's read subspace, tr(P_C·Σ_δ). `[replicated]`. `geometric-observation/claims/LEDGER.md:64` at 9f3829f.
- NEG-4. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL. `[refuted]`. `geometric-observation/claims/LEDGER.md:97` at 9f3829f.

## first stated

Chapter 4 section 4.3 of *Data Mining as Observation*, with the bit-matched redesign in `geometric-observation/chapters/ch08_value.md:1-30`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.4 | cosine 0.995 and perplexity of order ten thousand, the recalibration negative | `geometric-observation\chapters\ch02_failure_of_observer_free_measurement.md:40-60`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 and NEG-4; `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 3 section 3.3 | the self-refuted v0.8 claim, NEG-1 | `the-angular-observer\README.md:170-175`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-1 |
| chapter 4 section 4.3 | the flip definition, flip versus (A2) verdict | `geometric-observation\chapters\ch08_value.md:1-30,100-108` |
| chapter 4 section 4.3 | GO-2 0.0934 vs 0.0938, 2.53 times, 12 of 12, anti 21 times; retrieval 0.0964, negative 4.70 and positive 4.65, recon 0.40 | `geometric-observation\claims\LEDGER.md` rows GO-2 negative and positive halves |
| chapter 4 section 4.6 | NEG-4 through NEG-10, the 25 percent codebook confound, Spearman 0.80, the recon-matched precondition | `geometric-observation\chapters\ch16_honest_negatives.md` NEG-4 to NEG-10 |
| chapter 6 section 6.2 | real model, median 0.567 vs bar 0.60, about 4.5 times chance, heads at 0.815 and 0.958, sixteen of sixteen both, two of three triggers, NEG-12, later rematch four of four | `geometric-observation\claims\LEDGER.md` rows GO-B-Llama and NEG-12; `geometric-observation\chapters\ch16_honest_negatives.md:73-81` |
| chapter 8 section 8.2 | cosine 0.995, perplexity near 1e4 | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 |
| chapter 8 section 8.2 | recalibration improves reconstruction and worsens the consumer | `geometric-observation\chapters\ch16_honest_negatives.md` NEG-4 |

## failures and corrections

- NEG-4, `[refuted]`. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL.

## conditions

- The rule that two codes are compared only at the same bit count, since each added bit halves the step and quarters the squared error. At matched bits two codes with equal reconstruction error can still differ for a reader, and the flip is that difference.
- A comparison that was not bit-matched was refuted by the twenty-five percent codebook confound, and the redesign matched bits before any verdict was read.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Bit.lean`, theorems `levels_succ`, `levels_add`, `step_succ`, `sqError_succ`, `sqError_antitone`, `levels_zero`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Isotropy.lean`, theorems `isotropic_reads_same`, `isotropic_no_flip`, `anisotropic_readers_differ`, `flip_iff_anisotropic`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 4, 6, 12.

## related

bit, flip-the, budget, quantization, control

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
