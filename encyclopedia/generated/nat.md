# nat

**id.** nat
**kind.** concept

## definition

The unit of information measured with the natural logarithm, between 1.4426 and 1.4427 bits. Chapter 0 section 0.7.

## equation

Book equation 0.15.

    \tau=\frac{\#\{\text{concordant pairs}\}-\#\{\text{discordant pairs}\}}{n(n-1)/2}.

Book equation 4.2.

    D(b)=\sum_i s_i\sigma_i^{2}\,2^{-2b_i},\qquad s_i=v_i^{\top}P_C\,v_i,\qquad b_i^{\star}=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i\sigma_i^{2}}{\theta}\Big),\qquad \sum_i b_i^{\star}=B,

Book equation 0.16.

    \mathrm{AUROC}=\Pr\big[s^{+}>s^{-}\big]\ +\ \tfrac12\Pr\big[s^{+}=s^{-}\big].

## ledger

- GO-7. A stored description's description rate and its conditional Landauer reset content are operationally separate resources: the same finite-$n$ code index needing $\hat R\approx0.67$ bits/symbol to describe is fully recoverable from retained side information at bin rate $0.26=0.39\hat R$, fails increasingly below its conditional content, and fails absolutely (err 1.00 at every bin rate) without $S$. `[replicated]`. `geometric-observation/claims/LEDGER.md:69` at 9f3829f.
- NEG-13 → resolved. (GO-P-2026-026, prospective, real LLM) Appendix-E's omission floor is a rate-irreducible downstream wall on trained Llama read operators. `[missed]`. `geometric-observation/claims/LEDGER.md:106` at 9f3829f.

## first stated

Chapter 0 section 0.7 of *Data Mining as Observation*, with the omission floor in nats in `geometric-observation/chapters/ch07_cost.md`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.4 | C-7, sixteen points in 128 dimensions, rank fifteen, near ten to the eleventh nats, refuses when samples do not exceed dimension, warns below five per dimension, loading is a property of two distributions | `readscope\SPEC.md:653-680` |
| chapter 2 section 2.4 | C-7b, 92.1 percent, fit range 0.89 to 91.64, 15 percent inside, maximum 1.9e12, endpoint attenuation 0.437, 202 of 240 at 1.0, refuses to extrapolate, loading is a warning | `readscope\SPEC.md:680-720`; `readscope\readscope\loading.py:136-219` |
| chapter 2 section 2.6 | 0.647 published, 1.000 recovered, weighted vs unweighted median 0.796 range 0.678 to 0.985, probe 1.000 on every cell, 36 cells, one cell at 0.985 | `readscope\SPEC.md:410-450` |
| chapter 2 section 2.6 | C-10, 24 to 576 queries, reference rank 24 to 128, 0.821 to 0.703 vs 0.647, 68 percent of distance closed, 0.174 to 0.056, probe 1.000000 on 16 cells, residual uncontrolled | `readscope\SPEC.md:450-500` |
| chapter 4 section 4.2 | GO-6, d 8 and r 4, output at or below surrogate at or below reconstruction at every rate, about 500 times, gap 0.41 to 0.005, isotropic control collapses | `geometric-observation\claims\LEDGER.md` row GO-6; `geometric-observation\chapters\ch07_cost.md` |
| chapter 4 section 4.2 | commission tax of order half r log M over m, omission floor, unbounded corrected to floor, naive projector 30 percent over, VI-6 | `geometric-observation\chapters\ch07_cost.md` section on mismatch; `geometric-observation\claims\LEDGER.md` VI-6 |
| chapter 4 section 4.2 | floor measured on 16 of 16 heads, naive assumption off 20 to 60 percent, about 100000 times, 0.10 nats against about 6e-7, first gate missed 0 of 16, NEG-13 | `geometric-observation\chapters\ch07_cost.md`; `geometric-observation\claims\LEDGER.md` GO-P-2026-027 and NEG-13 |
| chapter 8 section 8.4 | C-11c paired null, rank 2 positional 0.385 vs null 0.572, 0.615 vs 0.224, 14 of 16 cells, scope 16 cells one 3B model 192 positions | `readscope\SPEC.md:806-857`; `readscope\calibration\records\c11c-operator-drift.json` |
| chapter 11 section 11.3 | tau floor 1 minus 2 mu, Spearman floor 1 minus 3 mu, example kappa 1.0148, mu 0.0664, floor 0.8671, 19900 pairs, max certifiable 1.83, vacuous means exact rerank, sha256 binding, reference field and the 0.3 overlap difference | `turboquant-pro\docs\CERTIFICATE_SPEC.md:1-80` |
| chapter 11 section 11.7 | k over d table 1, 2, 2, 16, 16, 16 | `readscope\README.md:118-141`; `readscope\SPEC.md:243-285`, record `readscope\calibration\records\c2e-budget-law.json` |
| chapter 11 section 11.7 | C-15 equal budget, 3072 observations, medians 0.02, 0.11, 0.05, 0.04, 1.0, 1.0, margin 0.883 vs 0.3, 0.062 to 0.057 at 8x | `readscope\SPEC.md:285-323`, record `readscope\calibration\records\c15-budget-surface.json`, `readscope\calibration\DECLARATION-C15.md` |
| chapter 11 section 11.9 | C-12 four bars, 40 documents, 512 tokens, 13.4 point difference, teacher forcing removes it, negative 0.015 vs 0.005, Spearman negative 0.13 at p 0.45, sign test p 0.42, verdict FAIL, feedback compounding | `readscope\calibration\records\c12-longgen-drift-sym.json`; `readscope\calibration\DECLARATION-C12.md` at commit `90e2ce2`; `readscope\SPEC.md:806-825` |

## failures and corrections

none

## conditions

- The unit of information measured with the natural logarithm, as a bit is measured with the logarithm to base two. The two conversions undo each other, the conversion is monotone, and one nat is between 1.4426 and 1.4427 bits.
- The omission floor was measured at 0.10 nats against about six in ten million on sixteen of sixteen heads, and Landauer's bound is stated per nat as kT and per bit as kT times the log of two.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/NatUnit.lean`, theorems `log_two_pos`, `nats_bits`, `bits_nats`, `bitsOfNats_mono`, `one_nat_in_bits`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Bit.lean`, theorems `levels_succ`, `levels_add`, `step_succ`, `sqError_succ`, `sqError_antitone`, `levels_zero`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 2, 4.

## related

bit, budget, landauers-principle, perplexity, kl-divergence

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
