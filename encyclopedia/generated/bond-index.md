# Bond Index

**id.** bond-index
**kind.** instrument
**volume.** Geometric Ethics, Volume 2 of the Geometric Series

## definition

A dimensionless audit measure of how much an evaluation moves when only the description changes, $Bd = D_{op} / \tau$. $D_{op}$ is the mean, over the inputs tested and the re-descriptions declared, of the distance between the evaluation before and after the re-description, and the divisor is a tolerance. Zero is perfect invariance.

**Example.** In the game form the distance is 0 when a pairing is the correlative and 1 when it is not. One wrong pairing in 8 gives 1/8 = 0.125, close to the volume's mean of about 0.13. Random choice among four positions is wrong 3 times in 4, which gives 0.75.

## equation

none

## conditions

- The distance is 0 or 1 for a verdict or a Hohfeldian position, the absolute change over the scale for a score, and the distance under the moral metric for a vector or a tensor. The vector form therefore inherits the untested metric.
- It is reported with the worst single case and the share of tests in which the evaluation moved, because a mean hides both.
- A result covers the declared suite of re-descriptions and nothing outside it (corrected in v1.27). A value of zero is not a guarantee against re-descriptions that were not tested.
- The clinical Bond Index of Chapter 21 shares the name and is a different quantity, the expected excess cost of a policy's mandated path over the manifold-optimal path. A value of one says nothing about the other.

Conditions are curated in `volumes/geometric-ethics.toml` rather than read from a record.

## ledger

none. *standing.* An instrument with one definition as of v1.26 and v1.27, which also corrected two statements about it (random play in the Dear Ethicist game scores about 0.75, not 0.5, and Appendix B now uses the five tiers of Chapter 18). The convergence claim about it, Proposition 19.4, is a Conditional Theorem whose ledger row GE-PROP-19-4 is exploratory.

## first stated

Requirement 3 of Section 18.9.6, [`geometric-ethics/chapter-18-geometric-ethics-for-artificial-agents.html:1173-1193`](https://github.com/ahb-sjsu/geometric-ethics/blob/ca9f708/chapter-18-geometric-ethics-for-artificial-agents.html#L1173-L1193), stated once there as of v1.26. The game form is in Section 17.4, [`geometric-ethics/chapter-17-empirical-evidence-for-geometric-ethics.html:637-661`](https://github.com/ahb-sjsu/geometric-ethics/blob/ca9f708/chapter-17-empirical-evidence-for-geometric-ethics.html#L637-L661). Online, [Geometric Ethics](https://erisml.org/book/chapter-18-geometric-ethics-for-artificial-agents.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Ethics*, Volume 2 of the Geometric Series.

## related

moral-bond-invariance-principle, hohfeldian-klein-four-group, no-escape-theorem, audit, paraphrase-class, moral-decision-edge-weight

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
