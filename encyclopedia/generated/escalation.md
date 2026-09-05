# escalation

**id.** escalation
**kind.** concept

## definition

The decision to hand an item to a person rather than decide it, the single-decision form of abstention. Chapter 14.

## equation

Book equation 14.5.

    \mathrm{FC}_g=\Pr\big[y=\text{violation}\ \big|\ \hat y=\text{clear},\ g\big],\qquad \text{verdict}=\max_{g:\ n_g\ge n_{\min}}\mathrm{FC}_g,\qquad \text{ABSTAIN otherwise}.

Book equation 10.7.

    \text{verdict}=\min_{i:\ n_i\ge n_{\min},\ |Q_i|\ge q_{\min}}\ \mathrm{score}_i,\qquad \text{ABSTAIN otherwise}.

Book equation 0.26.

    \mathrm{FC}=\Pr\big[W\ \text{refutes}\ \big|\ \mathcal C_t\ \text{clears}\big],\qquad \text{coverage}=\Pr\big[\mathcal C_t\ \text{clears}\big].

## ledger

none

## first stated

Chapter 14 section 14.9 of *Data Mining as Observation*, the single-decision form of abstention, with the refusal counts of the re-description test.

## measurements

none

## failures and corrections

none

## conditions

- The decision to hand an item to a person rather than decide it. A rule that escalates every item whose margin is below a bar decides a set that can only shrink as the bar rises, so coverage can only fall, every decided item carries at least the bar's margin, and a bar of zero escalates nothing.
- Coverage times the decided false-clear rate is the fraction of all items cleared and wrong, so an escalation policy trades coverage for a false-clear rate and a deployment report states both.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Escalation.lean`, theorems `decided_anti`, `coverage_anti`, `decided_margin`, `decided_zero`, `joint_rate`, at observation-data-mining 43ea852.

## used in

*Data Mining as Observation* chapters 0, 2, 8, 9, 10, 11, 14.

## related

abstention, margin, coverage, false-clear-rate, certificate

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns b331d4f, theory-radar 37c4e6c, observation-data-mining 43ea852, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
