# attribute type

**id.** attribute-type
**kind.** concept

## definition

The declaration of which transformations of a column keep its meaning: any injective relabelling for nominal, a strictly increasing map for ordinal, an affine map for interval, a positive rescaling for ratio, nested in that order. Chapter 2 section 2.1.

## equation

Book equation 2.1.

    P_{C_2\circ C_1}(x)=J_1(x)^{\top}\,P_{C_2}\big(C_1(x)\big)\,J_1(x),\qquad \operatorname{rank}P_{C_2\circ C_1}(x)\le\operatorname{rank}P_{C_2}\big(C_1(x)\big)\quad\text{at each row } x.

Book equation 0.12a.

    x\sim_C x'\quad\Longleftrightarrow\quad d_G\big(C(x),C(x')\big)=0.

## ledger

none

## first stated

Stevens, on the theory of scales of measurement, 1946, as chapter 2 section 2.1 of *Data Mining as Observation* reads it after TSK section 2.1.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.1 | the four attribute types and permitted transformations | TSK 2e section 2.1 |

## failures and corrections

none

## conditions

- The declaration of which transformations of a column do not change its meaning. A ratio scale permits a positive rescaling, an interval scale an affine map with positive slope, an ordinal scale a strictly increasing map, and a nominal scale any injective relabelling, and the four classes are nested in that order.
- A rescaling preserves ratios and an affine map preserves ratios of differences, so a consumer that reads a ratio of two interval-scale columns reads the origin the scale said was arbitrary.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/AttributeType.lean`, theorems `scale_affine`, `affine_strictMono`, `strictMono_injective`, `scale_preserves_ratio`, `affine_preserves_difference_ratio`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 2, 13.

## related

standardization, discretization, quotient, monotone-invariance-theorem

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
