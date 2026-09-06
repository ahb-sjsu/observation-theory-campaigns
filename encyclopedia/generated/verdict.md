# verdict

**id.** verdict
**kind.** concept

## definition

The outcome of a registered test, pass, fail, or abstain, taken as the worst group with the groups too thin to score counted. Chapter 1 section 1.5 and chapter 10 section 10.4.

## equation

Book equation 10.7.

    \text{verdict}=\min_{i:\ n_i\ge n_{\min},\ |Q_i|\ge q_{\min}}\ \mathrm{score}_i,\qquad \text{ABSTAIN otherwise}.

Book equation 14.5.

    \mathrm{FC}_g=\Pr\big[y=\text{violation}\ \big|\ \hat y=\text{clear},\ g\big],\qquad \text{verdict}=\max_{g:\ n_g\ge n_{\min}}\mathrm{FC}_g,\qquad \text{ABSTAIN otherwise}.

Book equation 8.3.

    \Pr[\text{at least one of } m\text{ null tests passes}]=1-(1-\alpha)^{m},\qquad \alpha_{\mathrm{Bonferroni}}=\frac{\alpha}{m}.

## ledger

- GO-3. The certificate's vacuity threshold predicts where single-stage retrieval dies. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:65` at 9f3829f.
- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 9f3829f.

## first stated

Chapter 1 section 1.5 and chapter 10 section 10.4 of *Data Mining as Observation*, with the six classes in `geometric-observation/PROTOCOL.md:58-75`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.5 | the six classes and the ledger rule | `geometric-observation\PROTOCOL.md:58-75`; `geometric-observation\OBSERVATION.md:43-45` |
| chapter 3 section 3.5 | query mass best single feature at every K for all four responses, seven features add at most 20 percent, threshold 1.25 on three of four, zero of four, 1000 real queries, 1024 dimensions | `openvector-bench\results\R13_STAGE0_RESULT.md:40-50`; `openvector-bench\results\R13_STAGE1_RESULT.md:1-40` |
| chapter 8 section 8.10 | the six classes | `geometric-observation\PROTOCOL.md:58-75` |
| chapter 9 section 9.2 | 12 of 12, dimensions 1.81, 2.80, 1.74, angular Spearman ranges, eccentricity spreads, verdict confirmed, GO-P-2026-041 | `the-angular-observer\experiments\manifold-recovery\battery_result.json` |
| chapter 10 section 10.2 | five kinds, balanced accuracy 0.611, 0.718, 0.684, the category table, per-category 0.57 to 0.82, the sweep, pigeonhole floor | `openvector-bench\results\R13_STAGE1_RESULT.md:40-75` |
| chapter 10 section 10.2 | half 2 failed, at most 1.28 times against 2, withdrawal and its scope | `openvector-bench\results\R13_STAGE1_RESULT.md:75-110` |
| chapter 11 section 11.6 | query mass best single feature at every K for all four responses, seven features add at most 20 percent at 12 leaves, threshold 1.25 on three of four, zero of four, 1000 real queries, 1024 dimensions | `openvector-bench\results\R13_STAGE0_RESULT.md:40-50`; `openvector-bench\results\R13_STAGE1_RESULT.md:1-40` |

## failures and corrections

- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- The outcome of a registered test, pass, fail, or abstain, taken as the worst group with the groups too thin to score counted. A verdict at one bar implies the verdict at every lower bar, and an abstention is reported as a verdict and not dropped.
- A verdict is relative to a budget and does not transfer to another, and the same two codes get opposite verdicts from two output metrics, so a verdict names its bar, its null, its budget, and its consumer.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Bar.lean`, theorems `passes_anti`, `passes_mono`, `discriminates_iff`, `no_bar_of_null_ge`, `exists_bar_of_lt`, `vacuous_of_null_passes`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Abstention.lean`, theorems `abstain_not_passes`, `verdict_eq_none_iff`, `passes_verdict_iff`, `inf_le_of_subset`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14.

## related

bar, abstention, ledger-class, min-over-strata, certificate

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
