# refusal

**id.** refusal
**kind.** concept

## definition

An instrument's declining to report a number it cannot support. A refusal is a verdict, and it is counted. Chapter 2 section 2.4 and chapter 9 section 9.2.

## equation

Book equation 10.7.

    \text{verdict}=\min_{i:\ n_i\ge n_{\min},\ |Q_i|\ge q_{\min}}\ \mathrm{score}_i,\qquad \text{ABSTAIN otherwise}.

Book equation 14.4.

    \text{attribution}_j(x)\approx g_j(x)\,\delta_j,\qquad \overline{\text{importance}}_j\approx\big(P_C\big)_{jj}=\mathbb E\big[g_j^{2}\big].

Book equation 9.3.

    \hat\mu=\frac{\bar s_{\mathrm{true}}-\bar s_{\mathrm{distr}}}{\sigma_{\mathrm{distr}}},\qquad \mu_{\mathrm{crit}}=\mathbb E\Big[\max_{N-1}\mathcal N(0,1)\Big],\qquad \rho=\frac{\hat\mu}{\mu_{\mathrm{crit}}},\qquad \rho=1\ \text{vacuous}.

## ledger

- GO-3. The certificate's vacuity threshold predicts where single-stage retrieval dies. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:65` at 9f3829f.
- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 9f3829f.

## first stated

Chapter 2 section 2.4 and chapter 9 section 9.2 of *Data Mining as Observation*, with the refusal regimes in `readscope/readscope/regimes.py:1-60`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.3 | refusal regimes, selection consumers read order, recurrences compound | `readscope\readscope\regimes.py:1-60` |
| chapter 2 section 2.6 | 0.647 published, 1.000 recovered, weighted vs unweighted median 0.796 range 0.678 to 0.985, probe 1.000 on every cell, 36 cells, one cell at 0.985 | `readscope\SPEC.md:410-450` |
| chapter 6 section 6.1 | selection consumers have zero sensitivity almost everywhere | `readscope\readscope\regimes.py:1-60` |
| chapter 10 section 10.4 | area map, boundary rule, hash, refuse not warn, intra and transit counts, area classes, abstention rule | `turboquant-pro\docs\STRATA_RFC.md:24-98` |
| chapter 10 section 10.4 | second prediction inverted, transit 0.389 vs 0.291, centrality difference signs, share 0.473 vs 0.391, seven of thirteen backbone | `turboquant-pro\docs\RESULTS_multilingual_strata.md:55-90`; `turboquant-pro\docs\STRATA_RFC.md:98-130` |

## failures and corrections

- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- An instrument's declining to report a number it cannot support, when samples do not exceed the dimension, when no template matches, or when a group is too thin. A refusal is a verdict, it is counted, and a mean never hides it.
- The recognizer refuses when the ratios match no stored template, the probe refuses to extrapolate past its fit range, and the strata design refuses rather than warns.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Abstention.lean`, theorems `abstain_not_passes`, `verdict_eq_none_iff`, `passes_verdict_iff`, `inf_le_of_subset`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 2, 8, 9, 10, 11, 14.

## related

abstention, vacuity-threshold, recognizer, verdict, coverage

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
