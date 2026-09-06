# projection

**id.** projection
**kind.** concept

## definition

The component of a vector along a unit direction. Equation 0.2.

## equation

Book equation 0.2.

    \operatorname{proj}_u(x)=(u\cdot x)\,u,\qquad \|u\|=1.

Book equation 0.12a.

    x\sim_C x'\quad\Longleftrightarrow\quad d_G\big(C(x),C(x')\big)=0.

Book equation 0.12b.

    x\sim_{\bar P_{C,\mu}} x'\quad\Longleftrightarrow\quad x-x'\in\ker\bar P_{C,\mu}.

## ledger

- GO-1. The consumer's invariant/nuisance split is identifiable ex ante from the consumer functional. `[predicted]`. `geometric-observation/claims/LEDGER.md:62` at 9f3829f.

## first stated

Chapter 0 section 0.2 of *Data Mining as Observation*, with the program's angular projection in Volume 14 chapter 9, `geometric-observation/chapters/ch09_legibility.md:31-41`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 6 section 6.2 | planted probe, overlap 0.936 vs 0.059, twelve of twelve, reconstruction 0.40, five of five | `geometric-observation\claims\LEDGER.md` row GO-1 |
| chapter 11 section 11.7 | GO-1 overlap 0.936 vs 0.059, flip 12 of 12, reconstruction 0.40 | `geometric-observation\claims\LEDGER.md` row GO-1; `geometric-observation\chapters\ch10_the_blind_probe.md:34-52` |

## failures and corrections

none

## conditions

- The component of a vector along a unit direction, the direction scaled by their dot product. Projecting twice is projecting once, the remainder is orthogonal to the direction, the projection is no longer than the vector, and adding anything orthogonal to the direction leaves it unchanged.
- The last is the quotient a one-direction reader takes. Row normalization is the projection onto the read subspace of the geodesic-rank consumer, and the invariant-nuisance split of the ledger is the same statement for a general consumer.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Projection.lean`, theorems `proj_proj`, `dot_sub_proj`, `proj_sq_le`, `proj_add_orth`, `proj_add`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 1, 3, 4, 6, 7, 9, 11.

## related

dot-product, read-subspace, quotient, nuisance

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
