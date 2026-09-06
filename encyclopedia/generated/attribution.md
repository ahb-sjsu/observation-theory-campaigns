# attribution

**id.** attribution
**kind.** instrument

## definition

An assignment to each feature of a share of one prediction. A gradient-based attribution estimates the consumer's sensitivity, and so a diagonal entry of the read operator when averaged. Shapley, permutation, and partial-dependence methods measure other things and are named for them. Chapter 14.

## equation

Book equation 0.8.

    g_j\;\approx\;\frac{C(x+h\,e_j)-C(x-h\,e_j)}{2h},\qquad j=1,\dots,d.

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

Book equation 14.5.

    \mathrm{FC}_g=\Pr\big[y=\text{violation}\ \big|\ \hat y=\text{clear},\ g\big],\qquad \text{verdict}=\max_{g:\ n_g\ge n_{\min}}\mathrm{FC}_g,\qquad \text{ABSTAIN otherwise}.

## ledger

- GO-1. The consumer's invariant/nuisance split is identifiable ex ante from the consumer functional. `[predicted]`. `geometric-observation/claims/LEDGER.md:62` at 9f3829f.
- GO-EC-3. A read operator recovered from a black-box consumer by query-only finite-difference probing, composed with the Kalman covariance as tr(P̂_C Σ), prospectively selects sensors that improve the held-out consumer at matched budgets with probe cost charged — capturing 94.6% of the known analytic optimum's gain on the positive-control arm (gate ≥ 75%) and improving 16.3% over the best consumer-agnostic policy on non-analytic consumers (gate ≥ 8%), with trace-matched ordering carried by the composition at 86.9% over 61 pairs (gate ≥ 65%). `[predicted]`. `geometric-observation/claims/LEDGER.md:162` at 9f3829f.

## first stated

Lundberg and Lee, a unified approach to interpreting model predictions, 2017, as chapter 14 section 14.5 of *Data Mining as Observation* reads it, with the program's contraction formula in `gtc-prototype/docs/SPECTRUM_FINDINGS.md:90-99`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 11 section 11.7 | GO-1 overlap 0.936 vs 0.059, flip 12 of 12, reconstruction 0.40 | `geometric-observation\claims\LEDGER.md` row GO-1; `geometric-observation\chapters\ch10_the_blind_probe.md:34-52` |
| chapter 14 section 14.5 | the contraction formula fairness minus the general component | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:90-99` |

## failures and corrections

none

## conditions

- An assignment to each feature of a share of one prediction. A gradient-based attribution gives coordinate i the share g_i times the move along it, those shares sum exactly to the change in output for an affine consumer, a coordinate the consumer does not read gets share zero, and the average of the squared sensitivity is a diagonal entry of the read operator, so an averaged gradient attribution estimates the read operator.
- Shapley, permutation, and partial-dependence methods measure other things and are named for them, and for a tree the sensitivity is zero almost everywhere, so importances that count splits are the right reading and finite differences the wrong one.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Attribution.lean`, theorems `attr_sum_affine`, `attr_unread`, `sq_sensitivity_eq_readOp_diag`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 8, 14.

## related

sensitivity, read-operator, finite-difference, consumer

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
