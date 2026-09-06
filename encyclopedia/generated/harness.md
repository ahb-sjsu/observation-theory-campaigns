# harness

**id.** harness
**kind.** concept

## definition

The code that evaluates a model. It is itself a consumer with a read subspace, and chapter 8 shows how it reads the test fold when allowed to.

## equation

Book equation 8.1.

    O_{\mathrm{harness}}=\big(C_{\mathrm{score}},\ G_{\mathrm{metric}},\ B=\text{folds}\times\text{samples}\times\text{seeds}\big).

Book equation 8.2.

    \begin{gathered} \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2}, \\ J=1000,\ \frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}=\frac14\ \Rightarrow\ 1+250=251,\ \ \sqrt{251}=15.84. \end{gathered}

Book equation 8.3.

    \Pr[\text{at least one of } m\text{ null tests passes}]=1-(1-\alpha)^{m},\qquad \alpha_{\mathrm{Bonferroni}}=\frac{\alpha}{m}.

## ledger

- OT-11. Feedback-free staleness: streaming-retrieval damage tracks measured drift; derived-cadence re-allocation removes it. `[void]`. `geometric-observation/claims/LEDGER.md:48` at 01e53bc.
- NEG-2. Reconstruction cosine as a proxy for key quality. `[refuted]`. `geometric-observation/claims/LEDGER.md:95` at 01e53bc.
- NEG-4. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL. `[refuted]`. `geometric-observation/claims/LEDGER.md:97` at 01e53bc.

## first stated

Chapter 8 section 8.1 of *Data Mining as Observation*, with the program's own harness failures in `openvector-bench/results/QUERY_COUPLING_ARTIFACT.md:1-20` and `constraint-gap/review/FINDINGS.md:1-35`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.4 | cosine 0.995 and perplexity of order ten thousand, the recalibration negative | `geometric-observation\chapters\ch02_failure_of_observer_free_measurement.md:40-60`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 and NEG-4; `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 2 section 2.5 | cosine 0.995 and the softmax reader | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 3 section 3.2 | condition (A2), tangential displacement | `turboquant-pro\docs\KV_KEYS_FINDING.md:61-86`; `geometric-observation\chapters\ch09_legibility.md:42-54` |
| chapter 6 section 6.4 | the uncorrected t stored as sigma, 251 and 15.84, nine wins to three, seven, eight, 3 wins 17 ties 11 losses on 31 datasets, the three-way inconsistency | `constraint-gap\review\FINDINGS.md:1-35`; `constraint-gap\README.md:57-76` |
| chapter 8 section 8.1 | G1 339.9 vs 71.9 same corpus, real about 61, rounds 1 to 4 at 300 to 420, three families falsified | `openvector-bench\results\QUERY_COUPLING_ARTIFACT.md:1-20` |
| chapter 8 section 8.2 | cosine 0.995, perplexity near 1e4 | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 |
| chapter 8 section 8.4 | real 1.038 [0.958, 1.118], rotated 1.019 [0.903, 1.353], smooth 2.804 withdrawn, second attempt 0.184 | `constraint-gap-measurements\notes\negative_control.md:1-50` |
| chapter 8 section 8.4 | gate meta-rule, relative contrast discriminates nothing | `openvector-bench\openvector_bench\score_rc1.py:1-14`; `turboquant-pro\docs\RESEARCH_ROADMAP.md:133-160` |
| chapter 8 section 8.5 | variance inflation 251, SE inflation 15.84, J_eff 3.98, about 62 needed, 3 of 9 at full, 7 at half, 8 at a third | `constraint-gap\review\FINDINGS.md:1-35` |
| chapter 11 section 11.1 | condition (A2), cosine satisfies it, post-rotary keys do not, the cone below cell size | `turboquant-pro\docs\KV_KEYS_FINDING.md:61-86`; `the-angular-observer\README.md:26-31` |
| chapter 11 section 11.2 | fp16 12.24, values-only 13.12, PolarQuant K4 10643 and 0.095, per-channel uniform K4 14.91 and 0.062, per-channel NUQ K3 15.77 and 0.148, 2.4x and 670x, pre-rotary near 22000, 2 key heads serve 12 query heads | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |

## failures and corrections

- NEG-2, `[refuted]`. Reconstruction cosine as a proxy for key quality.
- NEG-4, `[refuted]`. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL.
- `theory-radar/paper/REVISION_PLAN.md:39-45` at 37c4e6c. **Fix:** - Drop "σ significance" everywhere - Report: mean ΔF1, std, 95% CI, and corrected resampled t-statistic - Table columns: "Test F1", "GB F1", "ΔF1", "95% CI", "Direction" - Text: "the formula outperforms GB by ΔF1=0.031, 95% CI [0.028, 0.034]" - Add Nadeau-Bengio corrected t-test (accounts for CV fold correlation) - Keep effect size as supplementary but don't call it "σ"

## conditions

- The harness is the code that evaluates a model, and it is a consumer with its own read subspace, its output metric, and a budget of folds, samples, and seeds. What it reads decides what the reported score measures.
- A harness that is allowed to see the test fold, through feature selection before the split, through repeated selection on one split, or through a metric that discriminates nothing, reports a score of itself.
- Repeated cross-validation folds are not independent, so the variance of a fold mean is understated unless corrected, and the program's own retracted comparison is the case.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Bonferroni.lean`, theorems `family_error_le`, `bonferroni`, `one_look`, at observation-data-mining 424e077.

## used in

*Data Mining as Observation* chapters 1, 2, 4, 6, 7, 8, 10, 12, 14.

## related

leakage, observer, preregistration, ledger-class

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 01e53bc, observation-theory-campaigns 55ee1c6, theory-radar 37c4e6c, observation-data-mining 424e077, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
