# decision tree

**id.** decision-tree
**kind.** instrument

## definition

A classifier that scores by a sequence of axis-aligned splits, flat within each leaf, so that its sensitivity is zero almost everywhere and its importances count splits. Chapter 6.

## equation

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

Book equation 0.8.

    g_j\;\approx\;\frac{C(x+h\,e_j)-C(x-h\,e_j)}{2h},\qquad j=1,\dots,d.

Book equation 14.5.

    \mathrm{FC}_g=\Pr\big[y=\text{violation}\ \big|\ \hat y=\text{clear},\ g\big],\qquad \text{verdict}=\max_{g:\ n_g\ge n_{\min}}\mathrm{FC}_g,\qquad \text{ABSTAIN otherwise}.

## ledger

- GO-1. The consumer's invariant/nuisance split is identifiable ex ante from the consumer functional. `[predicted]`. `geometric-observation/claims/LEDGER.md:62` at 9f3829f.

## first stated

Breiman, Friedman, Olshen, and Stone, classification and regression trees, 1984, as chapter 6 section 6.1 of *Data Mining as Observation* reads it, with the selection-consumer regime in `readscope/readscope/regimes.py:1-60`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.3 | refusal regimes, selection consumers read order, recurrences compound | `readscope\readscope\regimes.py:1-60` |
| chapter 6 section 6.1 | selection consumers have zero sensitivity almost everywhere | `readscope\readscope\regimes.py:1-60` |
| chapter 6 section 6.3 | the five-dataset table, breast cancer 0.955 to 0.963, the pattern, DOI 10.5281/zenodo.20660206 | `theory-radar\README.md:100-140` |
| chapter 7 section 7.3 | the five-dataset outcomes | `theory-radar\README.md:100-140` |

## failures and corrections

none

## conditions

- A classifier that scores by a sequence of axis-aligned splits and is flat within each leaf. Its finite difference is zero at every row that does not straddle a split, a split on one coordinate reads nothing of the others, and the Gini impurity it splits on is at most one half for two classes and zero exactly for a pure leaf.
- Its read subspace is spanned by the coordinates it splits on and a feature that appears in no split is in its nuisance exactly, which is why a finite-difference probe of a tree returns zero at most rows and importances that count splits are the right sensitivity for this reader.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/DecisionTree.lean`, theorems `stump_flat_left`, `stump_flat_right`, `split_reads_one_axis`, `gini_le_half`, `gini_eq_zero_iff`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 4, 5, 6, 7, 8, 9, 11, 14.

## related

classifier, importance, boosting, ensemble, sensitivity

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
