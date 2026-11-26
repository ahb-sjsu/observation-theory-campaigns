# Political Bond Index

**id.** political-bond-index
**kind.** instrument
**volume.** Geometric Politics, Volume 10 of the Geometric Series

## definition

For a set of voters and an electoral system, $BI$ is the average over voters of the manifold distance to the actual representative minus the distance to the closest possible representative under an unconstrained optimal assignment. It is zero for a perfect system and positive otherwise.

**Example.** Two voters are 2.0 and 3.0 from their actual representatives and 1.0 and 1.5 from their optimal ones. The excesses are 1.0 and 1.5, so the index is 1.25. In the volume's illustration a move from 1.2 to 0.9 is a 25 percent reduction.

**Known as, or related to prior art.** The political instance of the Bond Index of Geometric Ethics.

## equation

none

## conditions

- It needs voter positions from a six-dimensional survey, representative positions estimated from roll-call votes, statements and platforms, and an optimal assignment computed as a minimum-cost matching against a hypothetical pool of representatives.
- The README says the instrument has not been built or gated. Chapter 18 lists its adoption as a legal standard among the open questions.
- A low average can hide large gaps between subgroups. The volume computes it by subgroup and by dimension for that reason.
- Every value printed for District 7 is illustrative, and the printed values are not all consistent. Plurality is given 2.8 in the comparison table and 1.2 in the first scenario of the same chapter, a difference the volume's corrections record of 2026-11-26 lists as unresolved. The chapter says the computation has not been carried out for a real district.

Conditions are curated in `volumes/geometric-politics.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, and says a political-argument instrument is plausible but has not been built or gated. District 7, the source of nearly every number in the volume, is a fictional district, and Chapter 18 says precise estimation of the manifold needs larger and richer datasets than currently exist.

## first stated

Definition 8 of Chapter 15, [`geometric-politics/manuscript/part_iv/ch15_political_bond_index.md:27-36`](https://github.com/ahb-sjsu/geometric-politics/blob/0fe7a96/manuscript/part_iv/ch15_political_bond_index.md#L27-L36). The computation is specified in Appendix C.3, [`geometric-politics/manuscript/appendices/appendix_c_voting.md:91-93`](https://github.com/ahb-sjsu/geometric-politics/blob/0fe7a96/manuscript/appendices/appendix_c_voting.md#L91-L93). Online, [Geometric Politics](https://erisml.org/geometric-politics/appendix_c_voting.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Politics*, Volume 10 of the Geometric Series.

## related

bond-index, legal-bond-index, gerrymandering-index, mahalanobis-distance, rcv-recovery-theorem, political-bond-invariance-principle

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
