# geometric feature vector (156 dimensions)

**id.** acoustic-geometric-feature-vector
**kind.** instrument
**volume.** Geometric Communication, Volume 7 of the Geometric Series

## definition

For one audio signal, the concatenation of 136 SPD features (the upper triangle of the matrix logarithm of the 16 by 16 frequency-band covariance), 4 spectral-trajectory features (path length, geodesic distance, deviation, step count) and 16 TDA features (8 persistence summary statistics each for $H_0$ and $H_1$).

**Example.** A symmetric 16 by 16 matrix has 16 times 17 over 2 = 136 independent entries. Adding 4 trajectory features and 2 times 8 = 16 persistence features gives 156, as the volume prints.

## equation

none

## conditions

- The covariance is computed from 16 bands of a mel spectrogram with a regularization of 0.0001 times the identity. The TDA features come from a time-delay embedding of the waveform with delay 10 and dimension 3.
- The chapter calls the parameter values design choices that can be adjusted for other domains.
- Proposition 4.3 claims that the combined vector classifies better than any one part on the BirdCLEF 206-species data. Neither Chapter 4 nor Chapter 8 prints the accuracies.
- In Chapter 8 the vector feeds a LightGBM model that carries 0.30 of the ensemble weight beside two convolutional networks.

Conditions are curated in `volumes/geometric-communication.toml` rather than read from a record.

## ledger

none. *standing.* A definition of a feature pipeline. The complementarity claim made for it (Proposition 4.3) is stated without printed numbers.

## first stated

Definition 4.16, [`geometric-communication/manuscript/part_ii/ch04_three_geometries.md:591-601`](https://github.com/ahb-sjsu/geometric-communication/blob/217c957/manuscript/part_ii/ch04_three_geometries.md#L591-L601). Online, [Geometric Communication](https://erisml.org/geometric-communication/ch04_three_geometries.html).

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

spectral-trajectory-geodesic-deviation, log-euclidean-distance, persistent-homology, covariance-matrix, communication-manifold

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
