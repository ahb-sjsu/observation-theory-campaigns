# the flip

**id.** flip
**kind.** result

## definition

At matched bits, the outcome in which the code with the worse reconstruction error scores better on the consumer's task, while a code built to destroy the read subspace scores worst. The book's central empirical claim. Chapter 4.

## equation

Book equation 4.5.

    \text{flip}:\quad \mathrm{task}(O)>\mathrm{task}(R)\ \ \text{and}\ \ \operatorname{tr}M^{O}_\delta>\operatorname{tr}M^{R}_\delta,\qquad \mathrm{task}(\text{anti})<\mathrm{task}(R),\qquad \text{bits}(O)=\text{bits}(R).

Book equation 3.1.

    \begin{gathered} d_O(u)=u^{\top}\Sigma\,u, \qquad u=(\cos15^\circ,\ \sin15^\circ), \\ \Sigma_1=\operatorname{diag}(0.3,1.7),\ \Sigma_2=\operatorname{diag}(1.7,0.3), \qquad d_O=0.394\ \text{vs}\ 1.606. \end{gathered}

Book equation 0.10.

    d_O=\operatorname{tr}(P_C\,M_\delta)=\mathbb E\!\left[\delta^{\top}P_C\,\delta\right],\qquad M_\delta=\mathbb E\!\left[\delta\delta^{\top}\right],\qquad P_C=I\ \Rightarrow\ d_O=\operatorname{tr}M_\delta.

## ledger

- GO-2 (neg. half: not reconstruction). At matched bits, downstream preservation is not controlled by reconstruction error. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:63` at 7d91883.
- GO-2 (pos. half: consumer-projected covariance *controls*). Downstream preservation is controlled by the error covariance projected on the consumer's read subspace, tr(P_C·Σ_δ). `[replicated]`. `geometric-observation/claims/LEDGER.md:64` at 7d91883.
- GO-4. Fixed-budget verdicts invert under budget-matched observation, per the wavelength mechanism. `[replicated]`. `geometric-observation/claims/LEDGER.md:66` at 7d91883.
- NEG-16 (KV serving, end-task). *At matched bits and matched reconstruction error, steering KV quantization error into the attention read subspace degrades LongBench task score by the registered floors on a deployed-class model.* Refuted at its registered effect sizes on this model and task. `[refuted]`. `geometric-observation/claims/LEDGER.md:92` at 7d91883.

## first stated

Volume 14, chapter 8, `geometric-observation/chapters/ch08_value.md:1-30`, DOI 10.5281/zenodo.21776291. The two-dimensional case is the cover and equation 3.1 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.4 | cosine 0.995 and perplexity of order ten thousand, the recalibration negative | `geometric-observation\chapters\ch02_failure_of_observer_free_measurement.md:40-60`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 and NEG-4; `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 1 section 1.4 | the flip sealed in twelve domains and three physics, held in at least five domains and all three | `geometric-observation\chapters\ch08_value.md:40-70`; `geometric-observation\claims\LEDGER.md` rows GO-2, GO-B-AV163, D3, 038 |
| chapter 2 section 2.5 | whitened code wins at every budget | `geometric-observation\chapters\ch08_value.md:84-97` |
| chapter 3 section 3.3 | the self-refuted v0.8 claim, NEG-1 | `the-angular-observer\README.md:170-175`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-1 |
| chapter 4 section 4.3 | the flip definition, flip versus (A2) verdict | `geometric-observation\chapters\ch08_value.md:1-30,100-108` |
| chapter 4 section 4.3 | GO-2 0.0934 vs 0.0938, 2.53 times, 12 of 12, anti 21 times; retrieval 0.0964, negative 4.70 and positive 4.65, recon 0.40 | `geometric-observation\claims\LEDGER.md` rows GO-2 negative and positive halves |
| chapter 4 section 4.3 | acoustic 148 of 201, 201 of 201, 152 of 201; seismic 13 of 17, 17 of 17, 13 of 17; whale 0.934 vs 0.883, 2 times, 300 of 300; at least 5 domains and 3 physics; battery prediction met | `geometric-observation\chapters\ch08_value.md:40-70`; `geometric-observation\claims\LEDGER.md` rows GO-B-AV163, D3, 038 |
| chapter 4 section 4.3 | whitened code on whale 0.83, 0.85, 0.97 vs 0.41, 0.80, 0.89 | `geometric-observation\chapters\ch08_value.md:84-97` |
| chapter 4 section 4.4 | gradient compression anti 300 of 300, flip 27 percent, coupling boundary | `geometric-observation\chapters\ch08_value.md:108-116` |
| chapter 4 section 4.4 | GO-4 budget inversion, fixed m 10 rises, matched m 121, 126, 159 collapses, 3 seeds | `geometric-observation\claims\LEDGER.md` row GO-4 |
| chapter 4 section 4.6 | NEG-4 through NEG-10, the 25 percent codebook confound, Spearman 0.80, the recon-matched precondition | `geometric-observation\chapters\ch16_honest_negatives.md` NEG-4 to NEG-10 |
| chapter 6 section 6.2 | real model, median 0.567 vs bar 0.60, about 4.5 times chance, heads at 0.815 and 0.958, sixteen of sixteen both, two of three triggers, NEG-12, later rematch four of four | `geometric-observation\claims\LEDGER.md` rows GO-B-Llama and NEG-12; `geometric-observation\chapters\ch16_honest_negatives.md:73-81` |
| chapter 6 section 6.2 | whale clan classifier, 8718 codas, 0.934 vs 0.883, reconstructs twice as well, 300 of 300 | `geometric-observation\chapters\ch08_value.md:40-70`; `geometric-observation\claims\LEDGER.md` row 038 |
| chapter 8 section 8.2 | cosine 0.995, perplexity near 1e4 | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 |
| chapter 8 section 8.2 | recalibration improves reconstruction and worsens the consumer | `geometric-observation\chapters\ch16_honest_negatives.md` NEG-4 |

## failures and corrections

- NEG-16 (KV serving, end-task), `[refuted]`. *At matched bits and matched reconstruction error, steering KV quantization error into the attention read subspace degrades LongBench task score by the registered floors on a deployed-class model.* Refuted at its registered effect sizes on this model and task.
- `geometric-observation/chapters/ch16_honest_negatives.md:28-30` at 7d91883. **NEG-4 — lightweight online (Lloyd) key calibration beats the default.** `[refuted]`. It *improves reconstruction and is worse on the consumer metric* — reconstruction-is-not-the- target, in its purest, most anti-correlated form.
- `geometric-observation/chapters/ch16_honest_negatives.md:32-34` at 7d91883. **NEG-5 … NEG-9 — the KV-key ladder that found the right statistic.** Five refuted proxies, and together the most instructive sequence in the ledger, because each refutation *located* the next hypothesis:
- `geometric-observation/chapters/ch16_honest_negatives.md:36-50` at 7d91883. - **NEG-5**: the originally-registered test missed (2/4 bars); the apparent reversal was a matched-bits confound (an uncounted per-block codebook, ~+25% bits). Refutes the *test*, not GO-2 — and forced a bit-matched redesign. - **NEG-6**: a demeaned-error-norm proxy fails to order the arms. The controlling quantity is the across-token *variance* of the query-projected error, not an error-magnitude scalar. *Magnitude ≠ downstream-relevant structure* (Chapter 6's lemma, learned here). - **NEG-7**: at *fixed reconstruction*, the downstream ranking **flips** with the consumer. Invariant-preservation is a property of the (compressor, consumer) *pair*, not the compressor — the sharpest form of GO-2's negative half. - **NEG-8**: the variance-ratio proxy reaches only Spearman 0.80; it is a noisy linear estimator of $\operatorname{tr}(P_C\Sigma_\delta)$. Gate on the *direct* projection instead. - **NEG-9**: even the direct trace $\operatorname{tr}(P_C\Sigma_\delta)$, while nailing the discriminating flip 12/12, is *not a complete rank statistic* — it misorders a middle pair whose per-token error has structure the trace misses. The mechanism is real; the scalar is not exhaustive.
- `geometric-observation/chapters/ch16_honest_negatives.md:56-61` at 7d91883. **NEG-10 — the flip appears on any independent representation (prospective).** `[refuted]`. On embedding retrieval, arm b reconstructed strictly better *and* Pareto-dominated downstream — no flip — so reconstruction was not falsified there. **Precondition discovered: the flip is observable only for reconstruction-matched arms.** The anti-probe half still transferred. This negative is why every later flip row is built on recon-matched arms; the miss defined the protocol.
- `geometric-observation/chapters/ch16_honest_negatives.md:106-112` at 7d91883. - **Identifiability** (fixable): NEG-5, NEG-10, legal-035, NEG-12 — the read operator was mis-estimated or the arms weren't recon-matched. Fixed by the blind probe and by protocol. - **Coupling** (a true boundary): D4 — read and signal energy intrinsically aligned; not rehabilitatable by any read-operator recovery. - **Precondition** (needs a working consumer): moral-on-frozen-embeddings — no read direction to protect until the consumer is competent. - **Mechanism-absent** (a genuine refutation): NEG-11 — the claimed effect does not exist.

## conditions

- Matched bits, and reconstruction matched or reported, for every comparison of two codes.
- A read operator misaligned with where the signal has its energy. The alignment of book equation 4.6 is the dial, and near one, the coupling null, no flip is possible.
- The read operator is the average of local linearizations, and the ordering it predicts is the ordering on average over the workload.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Flip.lean`, theorems `trace_eq`, `reading_difference`, `reader_swap_reverses`, `flip`, `cos_sq_pi_div_twelve`, `sin_sq_pi_div_twelve`, `reading_15_first`, `reading_15_second`, `sqrt_three_bounds`, `readings_15_to_three_decimals`, `reader_75_is_swap`, `four_to_one_flip`, at observation-data-mining 6c05d0a.

## used in

*Data Mining as Observation* chapters 2, 3, 4, 6, 7, 11, 12, 13, 14.

## related

read-distortion, alignment, anti-arm, rank-certificate, coupling-null

## status

Generated 2026-09-03 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 766096a, theory-radar 37c4e6c, observation-data-mining 6c05d0a, turboquant-pro 856c4cb, gtc-prototype 328741f.
