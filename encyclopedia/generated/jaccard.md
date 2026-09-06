# Jaccard

**id.** jaccard
**kind.** concept

## definition

The size of the intersection of two sets over the size of their union, between zero and one, zero exactly when the sets are disjoint, which discards joint absence. Chapter 0 section 0.6 and chapter 3.

## equation

Book equation 0.1.

    x\cdot y=\sum_{i=1}^{d}x_i y_i,\qquad \|x\|=\sqrt{x\cdot x},\qquad \cos\theta=\frac{x\cdot y}{\|x\|\,\|y\|}.

Book equation 3.1.

    \begin{gathered} d_O(u)=u^{\top}\Sigma\,u, \qquad u=(\cos15^\circ,\ \sin15^\circ), \\ \Sigma_1=\operatorname{diag}(0.3,1.7),\ \Sigma_2=\operatorname{diag}(1.7,0.3), \qquad d_O=0.394\ \text{vs}\ 1.606. \end{gathered}

## ledger

none

## first stated

Jaccard, the distribution of the flora in the alpine zone, 1912, as chapter 0 section 0.6 and chapter 3 section 3.1 of *Data Mining as Observation* read it.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.2 | traces 2.0, diagonals 0.3 and 1.7, consumers at 15 and 75 degrees, distortion 0.39 vs 1.61, 4.1 to one, computed not drawn | `observation-theory\assets\make_flip_figure.py:4-24,107-119` |

## failures and corrections

none

## conditions

- The size of the intersection of two sets over the size of their union, between zero and one, one for a nonempty set against itself, symmetric, and zero exactly when the sets are disjoint. A subset's coefficient is its share of the larger set.
- It reads nothing outside the union, so its distance lives on the quotient that discards joint absence, which is the right quotient for a consumer that reads presence and the wrong one for a consumer that reads counts.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Jaccard.lean`, theorems `jaccard_nonneg`, `jaccard_le_one`, `jaccard_self`, `jaccard_comm`, `jaccard_eq_zero_iff`, `jaccard_subset`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 3.

## related

cosine, quotient, bag-of-words, euclidean-distance, itemset

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
