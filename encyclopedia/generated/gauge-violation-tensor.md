# Gauge violation tensor

**id.** gauge-violation-tensor
**kind.** instrument
**volume.** Geometric Law, Volume 5 of the Geometric Series

## definition

A matrix whose entry for transformation $i$ and outcome $j$ is the mean over cases of the absolute change in outcome $j$ when protected characteristic $i$ is swapped, divided by the original outcome. Rows are characteristics such as race or gender, columns are outcomes such as sentence length or bail, and the mean of all entries is the Legal Bond Index.

**Example.** In the volume's hypothetical district the race row is 0.187, 0.213, 0.038, 0.082 and 0.104, which sums to 0.624. The five row sums 0.624, 0.479, 0.637, 0.156 and 0.444 add to 2.340, the total the chapter prints, and 2.340 / 25 is about 0.094.

## equation

none

## conditions

- A swap cannot be applied to a real defendant. The volume estimates entries from matched pairs of cases alike in drug type, quantity, criminal history, role, district and year.
- The appendix floors the denominator at a small positive constant to avoid division by zero.
- The intersectional term is the violation under two simultaneous swaps minus the two separate violations. A positive value is superadditive and a negative value subadditive.
- Chapter 11 says a matched estimate should be reported with a direct measurement of match quality in each group and recomputed under matching parity, because matches across groups can be worse than matches within groups. Its appendix remark says a test of a matched estimate should use a conditional randomization null and not a permutation null, a finding obtained for one index on one dataset and not established for the entries of the tensor.
- The tensor printed in the volume is for a hypothetical district and is introduced as illustrative. No tensor computed from real sentencing data is reported.

Conditions are curated in `volumes/geometric-law.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic status of 2026-07-14 calls the volume a posited framework with one instrumented corner. That corner is the legal text embedding LeBSE, validated in the xbse admission filter on US case law with labels from the CourtListener citation graph, and the README says this covers structure preservation in legal text embeddings and not the book's broader jurisprudential claims, which remain posited theory at licensed strength.

## first stated

Chapter 11, [`geometric-law/chapters/ch11_sentencing_disparities.md:28-48`](https://github.com/ahb-sjsu/geometric-law/blob/1e50dfc/chapters/ch11_sentencing_disparities.md#L28-L48), with the relation to the index at [`geometric-law/chapters/ch11_sentencing_disparities.md:64-68`](https://github.com/ahb-sjsu/geometric-law/blob/1e50dfc/chapters/ch11_sentencing_disparities.md#L64-L68). Online, [Geometric Law](https://erisml.org/geometric-law/ch11_sentencing_disparities.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Law*, Volume 5 of the Geometric Series.

## related

legal-bond-index, equal-protection-gauge-invariance, paired, singular-value-decomposition, confound

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
