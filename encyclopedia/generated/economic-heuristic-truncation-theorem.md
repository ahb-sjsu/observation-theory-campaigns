# Heuristic Truncation Theorem (moral heuristics as admissible heuristics)

**id.** economic-heuristic-truncation-theorem
**kind.** result
**volume.** Geometric Economics, Volume 4 of the Geometric Series

## definition

A moral heuristic that charges, at each state, the sum over boundaries of the penalty times the probability that the action crosses the boundary is admissible when each penalty is a lower bound on the true cost of crossing. A* search with it then finds the optimal path on the decision complex.

**Example.** One boundary with penalty 5, true crossing cost 8 and crossing probability 0.5 gives a heuristic value of 2.5. The same sum with the true cost is 4, so the heuristic does not overestimate.

**Known as, or related to prior art.** The admissibility theorem for A* search of Hart, Nilsson and Raphael, and the bounded suboptimality of weighted A*.

## equation

none

## conditions

- The decision is modelled as A* search with cost f = g + h, where g is the accumulated edge weight and h the heuristic estimate of the remaining cost. The identification of g with deliberate and h with intuitive judgment is the volume's modelling.
- The premise is that each penalty does not exceed the true cost of crossing. A heuristic that overestimates moral cost is inadmissible, and the volume calls that case genuine bias.
- Theorem 10 makes admissibility relative to the space. An infinite penalty can be admissible on the full complex and inadmissible on the monetary projection.
- Definition 11 and Theorem 12 relax the claim to a heuristic within a factor one plus epsilon of the true cost, with path cost at most that factor times the optimum.

Conditions are curated in `volumes/geometric-economics.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status block of 2026-07-14 calls the volume a posited framework, speculative theory awaiting instruments, and says that no economics instrument has been evaluated by the series' admission filter and that none passes its gate. Its claims are to be read as theory at licensed strength and not as validated measurement, and the chapters tag each claim as established mathematics, empirical, modeling axiom, conditional theorem or speculation.

## first stated

Theorem 7, Chapter 5, [`geometric-economics/chapters/ch05_price_as_heuristic.md:92-98`](https://github.com/ahb-sjsu/geometric-economics/blob/0382d57/chapters/ch05_price_as_heuristic.md#L92-L98), within the pathfinding setting of Definition 6, [`geometric-economics/chapters/ch05_price_as_heuristic.md:34-41`](https://github.com/ahb-sjsu/geometric-economics/blob/0382d57/chapters/ch05_price_as_heuristic.md#L34-L41). Online, [Geometric Economics](https://erisml.org/geometric-economics/ch05_price_as_heuristic.html).

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

moral-economic-boundary, price-as-scalar-heuristic, bond-geodesic, economic-decision-complex

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
