# finite difference

**id.** finite-difference
**kind.** instrument

## definition

An estimate of a derivative from two evaluations of the function at points a small step apart. Equation 0.8.

## equation

Book equation 0.8.

    g_j\;\approx\;\frac{C(x+h\,e_j)-C(x-h\,e_j)}{2h},\qquad j=1,\dots,d.

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

Book equation 11.4.

    \text{directions resolved}(k)=\begin{cases}1\ \text{or}\ 2,& k<d\\[2pt] \operatorname{rank}P_C,& k\ge d\end{cases}\qquad \text{cost}=2d\ \text{consumer calls per operating point}.

## ledger

- GO-1. The consumer's invariant/nuisance split is identifiable ex ante from the consumer functional. `[predicted]`. `geometric-observation/claims/LEDGER.md:62` at 9f3829f.

## first stated

Chapter 0 section 0.5 of *Data Mining as Observation*, equation 0.8, with the budget law measured in `readscope/README.md:118-141` and `readscope/CALIBRATION.md:419-434`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 11 section 11.7 | k over d table 1, 2, 2, 16, 16, 16 | `readscope\README.md:118-141`; `readscope\SPEC.md:243-285`, record `readscope\calibration\records\c2e-budget-law.json` |
| chapter 11 section 11.7 | rank-independent, 0.646 vs 0.366 at half dimension, never 0.90 below k equals d | `readscope\CALIBRATION.md:419-434` F-15 |
| chapter 11 section 11.7 | GO-1 overlap 0.936 vs 0.059, flip 12 of 12, reconstruction 0.40 | `geometric-observation\claims\LEDGER.md` row GO-1; `geometric-observation\chapters\ch10_the_blind_probe.md:34-52` |

## failures and corrections

none

## conditions

- An estimate of a derivative from two evaluations of the function at points a small step apart. The central difference recovers the derivative of a quadratic exactly at every step size, while the one-sided difference is off by the curvature times the step, which is why doing it in both directions is more accurate.
- Doing it once per coordinate costs d evaluations and in both directions costs 2d, which chapter 11 shows is the price at one operating point for a probe confined to the directions it chooses. The measurement instrument for that is the blind probe.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/FiniteDifference.lean`, theorems `central_quad`, `forward_quad`, `forward_error`, `central_cost`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 4, 6, 7, 11, 12, 14.

## related

sensitivity, read-operator, blind-probe, budget, budget-cliff

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
