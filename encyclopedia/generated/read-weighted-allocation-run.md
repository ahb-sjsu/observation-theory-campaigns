# read-weighted allocation, the recorded run of Section 22.4

**id.** read-weighted-allocation-run
**kind.** result
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

On a synthetic consumer that reads 3 directions of an 8-dimensional Gaussian source, reverse water-filling against a read metric estimated from 200 probe points gave 0.476, 0.334 and 0.196 of the consumer loss of the identity-weighted allocation at 1, 2 and 4 nats. Its reconstruction error was larger at every rate.

**Example.** At 4 nats the volume's table gives consumer losses of 0.033 and 0.170 and reconstruction errors of 0.722 and 0.307. The loss ratio from these rounded values is 0.19, where the record gives 0.196, and the reconstruction ratio is 2.4.

## equation

none

## conditions

- Three predictions were written in the script, and the script was committed, before it ran. All three passed, the first at 1 nat with little room, 0.476 against a mark of 0.5.
- There is one synthetic consumer, one seed, and no registration outside the script.
- The consumer was built with a kernel that is the same at every point, the favourable case for an averaged metric.
- The estimate costs 2p queries for each probe point, 3,200 queries here, and recovers the local metric only. Whether a direction is unread or only weakly read cannot be settled by a finite number of probes.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* Exploratory in the sense of Chapter 21. Three predictions were fixed in the committed script before the run of 25 November 2026 and graded on that one run, with one synthetic consumer and one seed.

## first stated

Section 22.4, [`geometric-methods/chapters/chapter-22-the-read-metric.md:118-137`](https://github.com/ahb-sjsu/geometric-methods/blob/371478c/chapters/chapter-22-the-read-metric.md#L118-L137), with the estimator in Section 22.2, [`geometric-methods/chapters/chapter-22-the-read-metric.md:44-48`](https://github.com/ahb-sjsu/geometric-methods/blob/371478c/chapters/chapter-22-the-read-metric.md#L44-L48). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-22-the-read-metric.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Methods*, Volume 1 of the Geometric Series.

## related

water-filling, read-operator, blind-probe, mahalanobis-distance, finite-difference, moving-kernel-excess-rate

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
