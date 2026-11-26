# Campaign Gradient Theorem

**id.** campaign-gradient-theorem
**kind.** result
**volume.** Geometric Politics, Volume 10 of the Geometric Series

## definition

A campaign is modeled as choosing a unit projection axis, the dimension voters attend to. The theorem says a successful campaign finds the axis along which the mean squared projected distance between the electorate and the candidate is smallest.

**Example.** Let the electorate have mean zero, variance 4 on axis 1 and variance 1 on axis 2, and let the candidate sit at $(0, 2)$. The mean squared projected distance is $4 + 0 = 4$ on axis 1 and $1 + 4 = 5$ on axis 2, so the campaign makes axis 1 salient.

**Known as, or related to prior art.** Issue ownership and priming in the campaign-effects literature.

## equation

none

## conditions

- The axis must be politically activatable. A campaign can make salient only the dimensions voters recognize as relevant.
- The model assumes campaigns change the salience of dimensions and leave voters' positions nearly fixed.
- The second displayed form is the expansion of the first. It minimizes the electorate's variance along the axis plus the squared offset of the candidate from the mean along the axis. The proof states that identity and reduces the choice to an eigenvalue problem for the matrix $\Sigma + (x_C - \mu)(x_C - \mu)^T$.
- The code listing of Appendix B.5 still implements an earlier ratio form that the theorem no longer states. The volume's corrections record of 2026-11-26 lists the listing as unresolved.
- The chapter says the theorem is not a new prediction. It offers it as a geometric account of the known regularity that campaigns stress strengths and avoid weaknesses.

Conditions are curated in `volumes/geometric-politics.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, and says a political-argument instrument is plausible but has not been built or gated. District 7, the source of nearly every number in the volume, is a fictional district, and Chapter 18 says precise estimation of the manifold needs larger and richer datasets than currently exist.

## first stated

Theorem 2 of Chapter 6, [`geometric-politics/manuscript/part_ii/ch06_campaigns_heuristic.md:50-58`](https://github.com/ahb-sjsu/geometric-politics/blob/0fe7a96/manuscript/part_ii/ch06_campaigns_heuristic.md#L50-L58), after the projection axis is defined at [`geometric-politics/manuscript/part_ii/ch06_campaigns_heuristic.md:40-44`](https://github.com/ahb-sjsu/geometric-politics/blob/0fe7a96/manuscript/part_ii/ch06_campaigns_heuristic.md#L40-L44). Online, [Geometric Politics](https://erisml.org/geometric-politics/ch06_campaigns_heuristic.html).

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

heuristic-field, media-heuristic-corruption, projection, covariance-matrix, political-frechet-mean

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
