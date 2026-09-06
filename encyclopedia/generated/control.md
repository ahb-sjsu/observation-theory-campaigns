# control

**id.** control
**kind.** instrument

## definition

A comparison arm that should not show the effect, run beside the arm that should. A control that passes the bar makes the bar vacuous. Chapter 8 section 8.4.

## equation

Book equation 8.3.

    \Pr[\text{at least one of } m\text{ null tests passes}]=1-(1-\alpha)^{m},\qquad \alpha_{\mathrm{Bonferroni}}=\frac{\alpha}{m}.

Book equation 0.17.

    \Pr[X\ge c]=1-\sum_{i<c}e^{-\mu}\frac{\mu^{i}}{i!},\qquad c^{\star}=\max\{c:\ n\Pr[X\ge c]\ge 1\},\qquad \mu=\frac{n_q\,k}{n}.

Book equation 4.6.

    \kappa=\operatorname{tr}\big(\bar P_C\,\bar\Sigma_x\big)\in[0,1],\qquad \kappa\to1\ \text{is the coupling null (no flip)}.

## ledger

- GO-6. At matched rate, output coding ≤ surrogate ≤ reconstruction on the consumer metric; the output–reconstruction gap is governed by the $\ker P_C$ entropy share, and the surrogate–output gap vanishes as rate grows. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:68` at 9f3829f.
- NEG-2. Reconstruction cosine as a proxy for key quality. `[refuted]`. `geometric-observation/claims/LEDGER.md:95` at 9f3829f.
- NEG-4. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL. `[refuted]`. `geometric-observation/claims/LEDGER.md:97` at 9f3829f.

## first stated

Chapter 8 section 8.4 of *Data Mining as Observation*, with the negative control in `constraint-gap-measurements/notes/negative_control.md:1-50`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.2 | GO-6, d 8 and r 4, output at or below surrogate at or below reconstruction at every rate, about 500 times, gap 0.41 to 0.005, isotropic control collapses | `geometric-observation\claims\LEDGER.md` row GO-6; `geometric-observation\chapters\ch07_cost.md` |
| chapter 8 section 8.4 | real 1.038 [0.958, 1.118], rotated 1.019 [0.903, 1.353], smooth 2.804 withdrawn, second attempt 0.184 | `constraint-gap-measurements\notes\negative_control.md:1-50` |
| chapter 8 section 8.4 | gate meta-rule, relative contrast discriminates nothing | `openvector-bench\openvector_bench\score_rc1.py:1-14`; `turboquant-pro\docs\RESEARCH_ROADMAP.md:133-160` |

## failures and corrections

- NEG-2, `[refuted]`. Reconstruction cosine as a proxy for key quality.
- NEG-4, `[refuted]`. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL.

## conditions

- A comparison arm that should not show the effect, run beside the arm that should. A control that passes the bar makes the bar vacuous, so a claim names its control and reports both, and an isotropic control collapses the flip because there is no direction to read.
- The first smooth-field control read 2.804 and was controlling for nothing, because the gradient it was compared against was piecewise constant, and the second attempt read 0.184.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/NullModel.lean`, theorems `card_pos_perm`, `scores_perm`, `stat_of_counts_const`, `excess_eq_zero_iff`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Bar.lean`, theorems `passes_anti`, `passes_mono`, `discriminates_iff`, `no_bar_of_null_ge`, `exists_bar_of_lt`, `vacuous_of_null_passes`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 2, 3, 4, 6, 7, 8, 9, 12, 13.

## related

null-model, bar, chance-level, confound, isotropic

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
