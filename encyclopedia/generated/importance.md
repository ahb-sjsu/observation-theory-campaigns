# importance

**id.** importance
**kind.** instrument

## definition

A per-feature score of how much a classifier reads it. For a tree it counts splits, which is the right sensitivity for a reader that is flat within leaves. Permutation importance and partial dependence answer related questions. Chapter 7 and chapter 14.

## equation

Book equation 14.5.

    \mathrm{FC}_g=\Pr\big[y=\text{violation}\ \big|\ \hat y=\text{clear},\ g\big],\qquad \text{verdict}=\max_{g:\ n_g\ge n_{\min}}\mathrm{FC}_g,\qquad \text{ABSTAIN otherwise}.

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

## ledger

- GO-EC-3. A read operator recovered from a black-box consumer by query-only finite-difference probing, composed with the Kalman covariance as tr(P̂_C Σ), prospectively selects sensors that improve the held-out consumer at matched budgets with probe cost charged — capturing 94.6% of the known analytic optimum's gain on the positive-control arm (gate ≥ 75%) and improving 16.3% over the best consumer-agnostic policy on non-analytic consumers (gate ≥ 8%), with trace-matched ordering carried by the composition at 86.9% over 61 pairs (gate ≥ 65%). `[predicted]`. `geometric-observation/claims/LEDGER.md:162` at 9f3829f.

## first stated

Breiman, random forests, 2001, as chapter 7 section 7.1 and chapter 14 section 14.5 of *Data Mining as Observation* read it, with the selection-consumer regime in `readscope/readscope/regimes.py:1-60`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.3 | refusal regimes, selection consumers read order, recurrences compound | `readscope\readscope\regimes.py:1-60` |
| chapter 6 section 6.1 | selection consumers have zero sensitivity almost everywhere | `readscope\readscope\regimes.py:1-60` |
| chapter 7 section 7.1 | bagging variance, out-of-bag estimation, random forests, importances, AdaBoost | Hastie, Tibshirani, Friedman, ESL 2e chapters 15 and 10.1; TSK 2e 4.10 |
| chapter 14 section 14.5 | the contraction formula fairness minus the general component | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:90-99` |

## failures and corrections

none

## conditions

- A per-feature score of how much a classifier reads it. For a gradient reader the averaged squared sensitivity is the read operator's diagonal, and for a tree, whose finite difference is zero at every row that does not straddle a split, counting splits is the right sensitivity.
- Permutation importance averages the consumer over rows that may never occur together, and partial dependence reads it at inputs it was never trained on, so the three answer different questions and the report names which.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Attribution.lean`, theorems `attr_sum_affine`, `attr_unread`, `sq_sensitivity_eq_readOp_diag`, at observation-data-mining 5bb2c0d.

`lean/DataMiningAsObservation/DecisionTree.lean`, theorems `stump_flat_left`, `stump_flat_right`, `split_reads_one_axis`, `gini_le_half`, `gini_eq_zero_iff`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 4, 6, 7, 14.

## related

attribution, decision-tree, sensitivity, read-operator, ensemble

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
