# random forest

**id.** random-forest
**kind.** instrument

## definition

An ensemble of decision trees, each fit on a bootstrap sample with a random subset of features at each split. Chapter 7.

## equation

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

Book equation 14.5.

    \mathrm{FC}_g=\Pr\big[y=\text{violation}\ \big|\ \hat y=\text{clear},\ g\big],\qquad \text{verdict}=\max_{g:\ n_g\ge n_{\min}}\mathrm{FC}_g,\qquad \text{ABSTAIN otherwise}.

## ledger

none

## first stated

Breiman, random forests, 2001, as chapter 7 section 7.1 of *Data Mining as Observation* reads it.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 6 section 6.3 | the five-dataset table, breast cancer 0.955 to 0.963, the pattern, DOI 10.5281/zenodo.20660206 | `theory-radar\README.md:100-140` |
| chapter 7 section 7.1 | bagging variance, out-of-bag estimation, random forests, importances, AdaBoost | Hastie, Tibshirani, Friedman, ESL 2e chapters 15 and 10.1; TSK 2e 4.10 |
| chapter 7 section 7.3 | the five-dataset outcomes | `theory-radar\README.md:100-140` |

## failures and corrections

none

## conditions

- An ensemble of decision trees, each fit on a bootstrap sample with a random subset of features at each split, that averages or votes. The average lies between its members and its squared error is at most their mean squared error, and each tree is flat within a leaf so the forest's importances count splits.
- On the five-dataset benchmark the forest and the boosted trees win when the boundary needs many features and lose to a formula when it needs few.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Ensemble.lean`, theorems `average_between`, `sq_average_le`, `average_const`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/DecisionTree.lean`, theorems `stump_flat_left`, `stump_flat_right`, `split_reads_one_axis`, `gini_le_half`, `gini_eq_zero_iff`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 6, 7.

## related

ensemble, decision-tree, bagging, importance, boosting

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
