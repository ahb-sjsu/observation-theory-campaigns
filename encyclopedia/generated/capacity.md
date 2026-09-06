# capacity

**id.** capacity
**kind.** concept

## definition

The number of distinctions a model class can draw, the model-side half of the budget. Chapter 6.

## equation

Book equation 1.1.

    O=(C,\ G,\ B).

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

Book equation 11.4.

    \text{directions resolved}(k)=\begin{cases}1\ \text{or}\ 2,& k<d\\[2pt] \operatorname{rank}P_C,& k\ge d\end{cases}\qquad \text{cost}=2d\ \text{consumer calls per operating point}.

## ledger

- GO-4. Fixed-budget verdicts invert under budget-matched observation, per the wavelength mechanism. `[replicated]`. `geometric-observation/claims/LEDGER.md:66` at 9f3829f.

## first stated

Chapter 6 section 6.1 of *Data Mining as Observation*, with the budget inversion in `geometric-observation/claims/LEDGER.md` row GO-4.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.4 | GO-4 budget inversion, fixed m 10 rises, matched m 121, 126, 159 collapses, 3 seeds | `geometric-observation\claims\LEDGER.md` row GO-4 |
| chapter 6 section 6.3 | depth three, ten binary and eight unary operations, exact optimal F1 by sort and sweep, beam, projections | `theory-radar\README.md:50-100,140-200` |

## failures and corrections

none

## conditions

- The number of distinctions a model class can draw, the budget's model-side half. A read operator's rank is at most the dimension, and a probe with fewer directions than the dimension cannot resolve the operator, which is the cliff.
- A formula of depth three over eighteen operations has a capacity the ensemble exceeds, and the ensemble wins exactly when the boundary needs that excess.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ProbeCliff.lean`, theorems `centralDiff_affine`, `centralDiff_basis`, `exists_blind_direction`, `indistinguishable`, `budget_cliff`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Rank.lean`, theorems `rank_le_width`, `rank_le_height`, `rank_outer_le_one`, `rank_mul_le`, `rank_zero`, `rank_transpose`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 6, 7.

## related

budget, budget-cliff, rank, formula-classifier, ensemble

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
