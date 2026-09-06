# discretization

**id.** discretization
**kind.** instrument

## definition

Collapsing an ordered quantity to a few labels by binning it, so that values in one cell become indistinguishable. It forms a quotient. Chapter 2 section 2.5.

## equation

Book equation 2.1.

    P_{C_2\circ C_1}(x)=J_1(x)^{\top}\,P_{C_2}\big(C_1(x)\big)\,J_1(x),\qquad \operatorname{rank}P_{C_2\circ C_1}(x)\le\operatorname{rank}P_{C_2}\big(C_1(x)\big)\quad\text{at each row } x.

Book equation 0.12a.

    x\sim_C x'\quad\Longleftrightarrow\quad d_G\big(C(x),C(x')\big)=0.

## ledger

none

## first stated

Chapter 2 section 2.5 of *Data Mining as Observation*, after TSK section 2.3.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.1 | the four attribute types and permitted transformations | TSK 2e section 2.1 |
| chapter 2 section 2.3 | MCAR, MAR, MNAR and the remedies, imputation before splitting | TSK 2e section 2.2; instructor working documents, not public [@bond2026course], `ECE_514-01_FA26_session-outlines.md:64-72` |

## failures and corrections

none

## conditions

- Collapsing an ordered quantity to a few labels by binning it. The bin index is nondecreasing in the value, every value in a cell gets the cell's index, two values in the same cell become indistinguishable, and a sample confined to m cells has at most m distinct labels.
- A discretization forms a quotient before anyone has said who reads the result, and a consumer that read the values it merged has lost them for every stage after.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Discretization.lean`, theorems `bin_mono`, `bin_of_mem`, `bin_eq_of_same_cell`, `card_bins_le`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 2.

## related

quotient, standardization, attribute-type, bit, quantization

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
