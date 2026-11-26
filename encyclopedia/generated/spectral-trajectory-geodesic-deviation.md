# spectral trajectory and its geodesic deviation

**id.** spectral-trajectory-geodesic-deviation
**kind.** instrument
**volume.** Geometric Communication, Volume 7 of the Geometric Series

## definition

Slide a window of w frames with hop h across a spectrogram and compute a covariance matrix at each position, giving a sequence $\Sigma_1, \ldots, \Sigma_K$ of SPD matrices. The geodesic deviation is the sum of the log-Euclidean distances between consecutive matrices minus the log-Euclidean distance from $\Sigma_1$ to $\Sigma_K$.

**Example.** A spectrogram of 100 frames with window 20 and hop 10 gives (100 - 20)/10 + 1 = 9 matrices. If the three steps of a four-matrix path each have length 1 and the endpoints are 1 apart, the deviation is 3 - 1 = 2.

## equation

none

## conditions

- The number of windows is $K = \lfloor (T - w)/h \rfloor + 1$ for a spectrogram of T frames.
- By the triangle inequality the deviation is at least zero, with equality if and only if the trajectory is a geodesic.
- The chapter reads the deviation as song complexity. A descending whistle gives low deviation. A trill gives high deviation if the window resolves each repetition, and low deviation with the one-second sub-windows of the implementation, where the trajectory stays near one point. This reading is the chapter's interpretation and is not tested separately.

Conditions are curated in `volumes/geometric-communication.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments. It says that no communication-domain instrument has been evaluated by the series' admission filter (xbse), that none currently passes its gate, and that the claims are theory at licensed strength and not validated measurement.

## first stated

Definitions 4.9 and 4.10, [`geometric-communication/manuscript/part_ii/ch04_three_geometries.md:358-370`](https://github.com/ahb-sjsu/geometric-communication/blob/22f0bb0/manuscript/part_ii/ch04_three_geometries.md#L358-L370). Online, [Geometric Communication](https://erisml.org/geometric-communication/ch04_three_geometries.html).

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

acoustic-geometric-feature-vector, log-euclidean-distance, geodesic-distance, reasoning-geodesic-deviation, covariance-matrix

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
