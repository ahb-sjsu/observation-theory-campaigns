# BGE and Nash relationship (augmented game)

**id.** bge-nash-relationship
**kind.** result
**volume.** Geometric Economics, Volume 4 of the Geometric Series

## definition

A profile is a BGE exactly when it is a Nash equilibrium of the augmented game, whose strategies are the simple paths to the goal and whose payoffs are the negative of behavioral friction. With zero penalties and covariance on $d_1$ alone it is the Nash equilibrium of the monetary game. Positive penalties exclude scalar equilibria that cross a boundary.

**Example.** Two paths with behavioral friction 4 and 6 have augmented payoffs -4 and -6. The path of least friction is the strategy of greatest payoff, so the two best-response conditions coincide.

**Known as, or related to prior art.** Nash equilibrium and Nash's existence theorem.

## equation

none

## conditions

- Equivalence holds by construction of the augmented game, with finite sets of simple paths as strategies.
- Scalar nesting is stated for a single-action game with all penalties zero and the covariance confined to the monetary dimension, and it uses the goal region to restrict the feasible actions.
- Refinement removes a boundary-crossing equilibrium only when the penalty exceeds the scalar cost disadvantage of the path that avoids the boundary.

Conditions are curated in `volumes/geometric-economics.toml` rather than read from a record.

## ledger

none. *standing.* Tagged a conditional theorem in the front matter. Existence of a mixed BGE follows from Nash's theorem of 1950 through the equivalence.

## first stated

Definition 20 and Theorem 21, Chapter 7, [`geometric-economics/chapters/ch07_bond_geodesic_equilibrium.md:72-90`](https://github.com/ahb-sjsu/geometric-economics/blob/ab7b319/chapters/ch07_bond_geodesic_equilibrium.md#L72-L90), with the proof at [`geometric-economics/chapters/ch07_bond_geodesic_equilibrium.md:94-106`](https://github.com/ahb-sjsu/geometric-economics/blob/ab7b319/chapters/ch07_bond_geodesic_equilibrium.md#L94-L106). Online, [Geometric Economics](https://erisml.org/geometric-economics/ch07_bond_geodesic_equilibrium.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Economics*, Volume 4 of the Geometric Series.

## related

bond-geodesic-equilibrium, bond-geodesic, moral-economic-boundary, price-as-scalar-heuristic

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
