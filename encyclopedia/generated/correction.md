# correction

**id.** correction
**kind.** concept

## definition

A change to a published number or claim that the record keeps beside the original, naming what was wrong. A statistical correction rescales a variance for a dependence the harness ignored. Chapter 2 section 2.4 and chapter 8 section 8.5.

## equation

Book equation 8.2.

    \begin{gathered} \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2}, \\ J=1000,\ \frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}=\frac14\ \Rightarrow\ 1+250=251,\ \ \sqrt{251}=15.84. \end{gathered}

Book equation 8.1.

    O_{\mathrm{harness}}=\big(C_{\mathrm{score}},\ G_{\mathrm{metric}},\ B=\text{folds}\times\text{samples}\times\text{seeds}\big).

Book equation 2.1.

    P_{C_2\circ C_1}(x)=J_1(x)^{\top}\,P_{C_2}\big(C_1(x)\big)\,J_1(x),\qquad \operatorname{rank}P_{C_2\circ C_1}(x)\le\operatorname{rank}P_{C_2}\big(C_1(x)\big)\quad\text{at each row } x.

## ledger

- NEG-9. The projected-variance trace tr(P_C·Σ_δ) is a complete rank statistic for softmax-KL across all arms. `[refuted]`. `geometric-observation/claims/LEDGER.md:102` at 9f3829f.
- NEG-13 → resolved. (GO-P-2026-026, prospective, real LLM) Appendix-E's omission floor is a rate-irreducible downstream wall on trained Llama read operators. `[missed]`. `geometric-observation/claims/LEDGER.md:106` at 9f3829f.

## first stated

Chapter 2 section 2.4 and chapter 8 section 8.5 of *Data Mining as Observation*, with the standing corrections in `geometric-observation/claims/LEDGER.md`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 6 section 6.4 | the uncorrected t stored as sigma, 251 and 15.84, nine wins to three, seven, eight, 3 wins 17 ties 11 losses on 31 datasets, the three-way inconsistency | `constraint-gap\review\FINDINGS.md:1-35`; `constraint-gap\README.md:57-76` |
| chapter 6 section 6.4 | the reviewer's revision plan, drop sigma, bounded claim, 19 at 200 by 5 vs 11 at 20 by 5, rerun in progress | `theory-radar\paper\REVISION_PLAN.md:1-60` |
| chapter 6 section 6.5 | loading weights and stability across folds requested | `theory-radar\paper\REVISION_PLAN.md` issue 6 |
| chapter 8 section 8.5 | variance inflation 251, SE inflation 15.84, J_eff 3.98, about 62 needed, 3 of 9 at full, 7 at half, 8 at a third | `constraint-gap\review\FINDINGS.md:1-35` |

## failures and corrections

- NEG-9, `[refuted]`. The projected-variance trace tr(P_C·Σ_δ) is a complete rank statistic for softmax-KL across all arms.

## conditions

- A change to a published number or claim that the record keeps beside the original, naming what was wrong and what replaced it. A statistical correction rescales a variance for a dependence the harness ignored, and a changed digest proves a changed file, so a correction is itself a sealed object.
- A correction can be the wrong shape. The uncorrected t was stored as a sigma, the fitted correction that transferred with mean absolute error zero was the identity, and the rows stay visible with the correction pointing at them.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/NadeauBengio.lean`, theorems `correctedVar_eq`, `naiveVar_le_correctedVar`, `inflation_unbounded`, `book_numbers`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Seal.lean`, theorems `changed_of_hash_ne`, `hash_eq_of_eq`, `exists_collision`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14.

## related

nadeau-and-bengio-correction, ledger-class, sealed, harness, retraction

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
