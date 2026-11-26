# Coalition fragility index

**id.** coalition-fragility-index
**kind.** result
**volume.** Geometric Politics, Volume 10 of the Geometric Series

## definition

$F(C)$ is the share of dimensions outside the coalition's agreement submanifold, multiplied by the largest ratio of within-coalition variance to squared tolerance among those outside dimensions. A coalition with $F(C)$ above 1 is called geometrically fragile.

**Example.** With six dimensions and agreement on two, the first factor is $4/6$, about 0.67. The index reaches 1 when the worst outside dimension has variance equal to 1.5 times the squared tolerance, since $0.67 \times 1.5 = 1$. These are the volume's figures.

## equation

none

## conditions

- The chapter states the theorem and gives no proof. The index and its threshold of 1 work as a definition.
- The theorem also calls a coalition vulnerable on a dimension whose within-coalition variance exceeds the squared tolerance. The chapter says the two conditions are nested, since an index above 1 needs a variance above $d/(d - \dim A_C)$ times the squared tolerance, so every fragile coalition is vulnerable and not every vulnerable one is fragile.
- It needs the tolerance and the within-coalition variance on each dimension, neither of which the volume measures.
- The claim that both American party coalitions operate near the threshold is argued from the posited agreement dimension of 2.

Conditions are curated in `volumes/geometric-politics.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, and says a political-argument instrument is plausible but has not been built or gated. District 7, the source of nearly every number in the volume, is a fictional district, and Chapter 18 says precise estimation of the manifold needs larger and richer datasets than currently exist.

## first stated

Theorem 6 of Chapter 12, [`geometric-politics/manuscript/part_iii/ch12_coalitions.md:71-79`](https://github.com/ahb-sjsu/geometric-politics/blob/8f4a831/manuscript/part_iii/ch12_coalitions.md#L71-L79). Online, [Geometric Politics](https://erisml.org/geometric-politics/ch12_coalitions.html).

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

agreement-submanifold, sample-variance, threshold, political-preference-manifold

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
