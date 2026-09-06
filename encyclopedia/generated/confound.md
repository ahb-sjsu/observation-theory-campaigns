# confound

**id.** confound
**kind.** concept

## definition

A variable that moves with both the treatment and the outcome so that a measured difference cannot be attributed. Chapter 8 requires controls before a claim.

## equation

Book equation 8.3.

    \Pr[\text{at least one of } m\text{ null tests passes}]=1-(1-\alpha)^{m},\qquad \alpha_{\mathrm{Bonferroni}}=\frac{\alpha}{m}.

Book equation 8.2.

    \begin{gathered} \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2}, \\ J=1000,\ \frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}=\frac14\ \Rightarrow\ 1+250=251,\ \ \sqrt{251}=15.84. \end{gathered}

## ledger

- NEG-4. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL. `[refuted]`. `geometric-observation/claims/LEDGER.md:97` at 7d91883.
- NEG-5. GO-P-2026-001 as registered: on KV keys, invariant-preserving (asym-NF4) beats reconstruction-optimal (per-block Lloyd) at matched bits, and tangential distortion dominates reconstruction in predicting softmax-KL. `[refuted]`. `geometric-observation/claims/LEDGER.md:98` at 7d91883.
- NEG-6. Relative per-channel-demeaned error norm is the quotient-tangential quantity that controls softmax-KL. `[refuted]`. `geometric-observation/claims/LEDGER.md:99` at 7d91883.

## first stated

Chapter 8 section 8.6 of *Data Mining as Observation*, with the program's codebook confound in Volume 14's honest negatives and the negative controls of the constraint-gap review.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 8 section 8.4 | real 1.038 [0.958, 1.118], rotated 1.019 [0.903, 1.353], smooth 2.804 withdrawn, second attempt 0.184 | `constraint-gap-measurements\notes\negative_control.md:1-50` |
| chapter 8 section 8.5 | three-way inconsistency, lines 544, 548 to 556, 755 | `constraint-gap\review\FINDINGS.md:7-31` against `theory-radar\paper\theory_radar_v6_submission.tex` |

## failures and corrections

- NEG-4, `[refuted]`. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL.
- NEG-5, `[refuted]`. GO-P-2026-001 as registered: on KV keys, invariant-preserving (asym-NF4) beats reconstruction-optimal (per-block Lloyd) at matched bits, and tangential distortion dominates reconstruction in predicting softmax-KL.
- NEG-6, `[refuted]`. Relative per-channel-demeaned error norm is the quotient-tangential quantity that controls softmax-KL.

## conditions

- A variable that moves with both the treatment and the outcome. In the linear case the naive difference of group means is the treatment effect plus the confound's effect times the difference of the confound's means between the groups, so it equals the effect exactly when the confound is balanced or has no effect, and the bias can have either sign and any size.
- Controls come before claims. The twenty-five percent codebook confound in the flip's early arms and the smooth-perturbation control that was withdrawn are the program's cases, each carried in the ledger.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Confound.lean`, theorems `mean_outcome`, `naive_diff`, `naive_diff_of_balanced`, `naive_diff_of_no_effect`, `bias_unbounded`, at observation-data-mining 7eba709.

## used in

*Data Mining as Observation* chapters 2, 3, 4, 6, 7, 8, 9, 12, 13, 14.

## related

harness, null-model, simpsons-paradox, preregistration

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns f5585e7, theory-radar 37c4e6c, observation-data-mining 7eba709, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
