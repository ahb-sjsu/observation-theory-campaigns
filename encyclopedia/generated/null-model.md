# null model

**id.** null-model
**kind.** instrument

## definition

A version of the data with the structure under test removed and everything else kept, the right comparison for any measured statistic. Chapter 0 section 0.9.

## equation

Book equation 0.17.

    \Pr[X\ge c]=1-\sum_{i<c}e^{-\mu}\frac{\mu^{i}}{i!},\qquad c^{\star}=\max\{c:\ n\Pr[X\ge c]\ge 1\},\qquad \mu=\frac{n_q\,k}{n}.

Book equation 8.3.

    \Pr[\text{at least one of } m\text{ null tests passes}]=1-(1-\alpha)^{m},\qquad \alpha_{\mathrm{Bonferroni}}=\frac{\alpha}{m}.

## ledger

- OT-4. Operator drift predicts a real long-generation degradation and a derived refresh intervention moves it. `[refuted]`. `geometric-observation/claims/LEDGER.md:36` at 7d91883.
- NEG-15 (Bell boundary). *Query-conditioned hubness supplies a mechanism for Bell-inequality violation without action at a distance.* Refuted as a mechanism; the settings-as-queries reframing survives only as vocabulary. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:93` at 7d91883.

## first stated

Chapter 0 section 0.9 and chapter 8 section 8.4 of *Data Mining as Observation*, with the program's Poisson, paired, and permutation nulls in openvector-bench, readscope, and the encoder gate.

## measurements

none

## failures and corrections

- OT-4, `[refuted]`. Operator drift predicts a real long-generation degradation and a derived refresh intervention moves it.

## conditions

- A version of the data with the structure under test removed and everything else kept. A label permutation keeps every class size and the bag of scores, so any statistic that reads only class sizes or only scores is unchanged by it, and only a statistic that reads the pairing between score and label can move.
- That is what makes the permuted statistic the right comparison, and the excess over the null mean is the number a chapter reports. A number without its null is not yet a finding, and the drift claim that lost half its size to a paired null is the ledger's case.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/NullModel.lean`, theorems `card_pos_perm`, `scores_perm`, `stat_of_counts_const`, `excess_eq_zero_iff`, at observation-data-mining 2b00d80.

## used in

*Data Mining as Observation* chapters 0, 2, 3, 4, 5, 8, 9, 10, 11, 12, 14.

## related

poisson-ceiling, chance-level, cross-corpus-gate, p-value, harness

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns e448a13, theory-radar 37c4e6c, observation-data-mining 2b00d80, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
