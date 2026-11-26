# communication heuristic field

**id.** communication-heuristic-field
**kind.** concept
**volume.** Geometric Communication, Volume 7 of the Geometric Series

## definition

A smooth function h on the communication manifold that gives, at each point, the estimated cost of reaching the intended communicative act. Its negative gradient points toward the interpretations the heuristic judges more likely. It is admissible if it never overestimates the distance to the intended meaning.

**Example.** If the true cost to the intended reading is 5, an estimate of 3 is admissible and an estimate of 7 is not. In the volume's illustration, hearing the word bank in a talk about fishing gives a steep descent toward the riverbank reading.

**Known as, or related to prior art.** Admissible and consistent heuristics of A* search, and the principle of charity of Grice and Davidson, which the chapter names.

## equation

none

## conditions

- Interpretation is modelled as search on the manifold. The hearer is given the signal and partial information about pragmatics and content.
- The field is not static. The chapter says it is assembled from at least four sources, among them linguistic convention and discourse context.
- An admissible heuristic may underestimate ambiguity. It is consistent only if it also satisfies the triangle inequality $h(m_1) \le d(m_1, m_2) + h(m_2)$.
- The formalism is inherited from Geometric Reasoning. No heuristic field is estimated in this volume.

Conditions are curated in `volumes/geometric-communication.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments. It says that no communication-domain instrument has been evaluated by the series' admission filter (xbse), that none currently passes its gate, and that the claims are theory at licensed strength and not validated measurement.

## first stated

Definitions 3.3 and 3.4, [`geometric-communication/manuscript/part_i/ch03_communication_manifold.md:205-217`](https://github.com/ahb-sjsu/geometric-communication/blob/8184f3a/manuscript/part_i/ch03_communication_manifold.md#L205-L217). Online, [Geometric Communication](https://erisml.org/geometric-communication/ch03_communication_manifold.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Communication*, Volume 7 of the Geometric Series.

## related

heuristic-field, heuristic-admissibility, communication-manifold, communication-metric

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
