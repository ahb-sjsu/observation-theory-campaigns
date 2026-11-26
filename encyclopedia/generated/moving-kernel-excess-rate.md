# moving kernel and the excess rate of an averaged read metric

**id.** moving-kernel-excess-rate
**kind.** result
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

When the directions a consumer does not read change from point to point, the averaged read metric can have rank q larger than the number k of quantities the consumer reads. A description whose error covariance does not depend on the point then pays an excess rate of about (q - k)/2 times log(1/D) at consumer loss D.

**Example.** For the volume's example, the consumer x1 + a sin(x2) reads one number, so k = 1. Its Jacobian is (1, a) at x2 = 0 and (1, 0) at x2 = pi/2, so the average has rank q = 2 and the leading excess is 0.5 log(1/D), which is 2 nats at D = exp(-4).

## equation

none

## conditions

- Averaging is harmless when the unread directions are the same at every point. The excess, which includes a bounded term, grows without limit as the target loss falls.
- The statement is about one family of Gaussian test channels and about information rates, not about every code.
- The practical test compares the rank of the averaged estimate with the typical rank of the local matrices at the probe points. A clearly larger rank of the average means the kernel moves.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* Exploratory in the ledger of Volume 14 (row T1-MK). The rate statements have written proofs and independent audits and no sealed numerical test (Section 21.8).

## first stated

Section 22.5, [`geometric-methods/chapters/chapter-22-the-read-metric.md:147-158`](https://github.com/ahb-sjsu/geometric-methods/blob/d910c92/chapters/chapter-22-the-read-metric.md#L147-L158). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-22-the-read-metric.html).

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

read-operator, read-subspace, null-space, water-filling, rank, read-weighted-allocation-run

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
