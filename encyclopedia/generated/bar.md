# bar

**id.** bar
**kind.** instrument

## definition

A threshold a statistic must reach, written down before the measurement. A bar discriminates only when the null fails it and the real system passes it, and a bar the null passes is vacuous. Chapter 8 section 8.3.

## equation

Book equation 8.3.

    \Pr[\text{at least one of } m\text{ null tests passes}]=1-(1-\alpha)^{m},\qquad \alpha_{\mathrm{Bonferroni}}=\frac{\alpha}{m}.

Book equation 8.1.

    O_{\mathrm{harness}}=\big(C_{\mathrm{score}},\ G_{\mathrm{metric}},\ B=\text{folds}\times\text{samples}\times\text{seeds}\big).

Book equation 10.7.

    \text{verdict}=\min_{i:\ n_i\ge n_{\min},\ |Q_i|\ge q_{\min}}\ \mathrm{score}_i,\qquad \text{ABSTAIN otherwise}.

## ledger

- OT-11. Feedback-free staleness: streaming-retrieval damage tracks measured drift; derived-cadence re-allocation removes it. `[void]`. `geometric-observation/claims/LEDGER.md:48` at 9f3829f.
- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 9f3829f.

## first stated

Chapter 8 section 8.3 of *Data Mining as Observation*, with the anti-vacuity bar quoted from `observation-theory-campaigns/experiments/PREREG-PF5-002.md:79-86`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 8 section 8.3 | PF5-001 vacuous pass (8 cells, 20000 census, 6.1e-7 vs 1e-5, 96 members, 160000 transmitted, zero reversing, record sha 073f6e692253) | `observation-theory-campaigns\experiments\CAMPAIGN.md:255-277` |
| chapter 8 section 8.3 | anti-vacuity bar, quoted | `observation-theory-campaigns\experiments\PREREG-PF5-002.md:79-86` |
| chapter 9 section 9.2 | the battery, three new templates, frozen ratios, code hash, bars at least 10 of 12 and the dimension ordering, eccentricity scope | `the-angular-observer\PREREG_RECOGNIZER_BATTERY.md:1-80` |

## failures and corrections

- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- A threshold a statistic must reach, written down before the measurement. Passing a higher bar passes every lower one, a larger statistic passes every bar a smaller one passes, a bar discriminates exactly when it sits strictly above the null and at or below the real system, no bar discriminates when the null scores at least as high, and a bar the null passes is vacuous.
- A pass on eight cells at six parts in ten million against a bar of one in a hundred thousand was vacuous because the null cleared the bar too, which is where the anti-vacuity bar came from.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Bar.lean`, theorems `passes_anti`, `passes_mono`, `discriminates_iff`, `no_bar_of_null_ge`, `exists_bar_of_lt`, `vacuous_of_null_passes`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14.

## related

gate, vacuity-threshold, null-model, preregistration, verdict

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
