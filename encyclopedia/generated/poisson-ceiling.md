# Poisson ceiling

**id.** poisson-ceiling
**kind.** instrument

![The count chance allows.](../figures/poisson-ceiling.svg)

## definition

The largest neighbour count that at least one point in a dataset would reach by chance under a Poisson null, above which a count is evidence of a hub. Equation 0.17.

**Example.** With 1000 queries at k equal to 10 over 1000 rows, each row expects 10 retrievals, and a count above about 20 is beyond chance.

## equation

Book equation 0.17.

    \Pr[X\ge c]=1-\sum_{i<c}e^{-\mu}\frac{\mu^{i}}{i!},\qquad c^{\star}=\max\{c:\ n\Pr[X\ge c]\ge 1\},\qquad \mu=\frac{n_q\,k}{n}.

## conditions

- Under the null that the slots are handed out at random, a row's count is Poisson with mean the slots per row, and the ceiling is the largest count at least one row would reach by chance. A count above it is evidence of a hub, and a count below it is not evidence of anything.
- The ceiling depends on the query set, through the mean and through the rows the queries reach, so it is recomputed when the queries change, and the program's first hubness numbers moved by a factor of several when query coupling was removed.

Conditions are curated in `entries.toml` rather than read from a record.

## ledger

none

## first stated

openvector-bench, `openvector-bench/openvector_bench/hubness.py:41-100`, and chapter 0 section 0.8 and chapter 3 section 3.5 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.5 | Poisson null, hub excess, budget parameter | `openvector-bench/openvector_bench/hubness.py:41-100` |

## failures and corrections

none

## invariance envelope

**Boundary measured.**

- OD:world-transfer, transfer of a law frozen on synthetic worlds to embedding corpora, ANN corpora, and dynamical state spaces without retuning. Claim: With the log Poisson hub excess as the target on D2v6's world, the frozen law log(excess) = -1.103 - 0.025 / cv_knn + 0.167 log(d_eff) + 0.434 sqrt(id_twonn) predicts hubness on the bracketed heavy tails, on the d = 512 clouds, on fresh real slices and at larger N, and beats the nominal-only law and the chance level. `experiments/DISCOVERY-TRACK.md, D2v7 record; experiments/OD/D2v7/grade.json`. Boundary: every heavy-tailed unseen world inside the limit (t with 4 degrees at d = 256 0.18, Laplace at d = 224 0.19, t with 2.5 degrees at d = 128 0.11, log-normal at d = 192 0.14, t with 6 degrees at d = 192 0.18, RMS log ratios against 0.66); the Gaussian at d = 512 0.58 inside, the cube at d = 512 0.82 outside; real slices 0.19 to 0.45 against 0.98; seven of eight scale cells inside, Laplace at N = 12000 at 0.656 against 0.655; fresh seeds 0.29 against 0.49; the law at 0.35 pooled on the transfer groups against 1.64 (nominal) and 1.70 (chance) and inside every group. Witness: the same family, pool, search and worlds that put the heavy tails at d = 256 and the clouds at d = 512 on opposite sides of a limit in skewness hold both in log excess, because the skewness saturates where the excess keeps counting; the target, not the family and not the set, was the limit the skew registrations met. Absorbed by: declaration. Revision: the cube at d = 512 remains the one world beyond the training dimensions the law over-predicts (a factor of 2.3); a D2v8 would add full-dimensional worlds at d = 384 to 512 to the discovery set under this target, and is the coverage repair that D2v6 showed does not work for the skewness.
- OD:world-transfer, transfer of a law frozen on synthetic worlds to embedding corpora, ANN corpora, and dynamical state spaces without retuning. Claim: Inside a declared scope, rows whose k-th neighbour-distance concentration cv_knn on the observed data is at least 0.015, the frozen D2v7 law log(excess) = -1.103 - 0.025 / cv_knn + 0.167 log(d_eff) + 0.434 sqrt(id_twonn) predicts the log Poisson hub excess on fresh worlds, fresh real slices and larger N within D2v7's bars and beats the nominal-only law and the chance level; outside the scope it is not claimed and its pooled error exceeds the in-scope limit. `experiments/DISCOVERY-TRACK.md, D2v9 record; experiments/OD/D2v9/grade.json; experiments/OD/D2v9_explore/README.md`. Boundary: in scope: all eighteen unseen worlds inside 0.64 (balls at d = 256 and 384 at 0.43 and 0.44, cube at d = 640 at 0.37, heavy tails 0.12 to 0.27), pooled 0.31 against 0.48; real slices 0.12 to 0.41 against 0.96; seven of eight scale cells inside, Laplace at d = 64 and N = 12000 at 0.67 against 0.64, the cell the registration named in advance; the law at 0.34 pooled on in-scope transfer rows against 1.63 (nominal) and 1.64 (chance) and inside every group; out of scope: 180 rows in twelve worlds at 1.19 against 0.64, the balls under-predicted (to -0.84 median residual), the cubes over-predicted (to +1.37), the torus and the sphere fitted anyway (0.14, 0.08). Witness: the D2v7 law's failures on this world are where the registration said they are: a regime of unreliability of the reciprocal concentration term on over-concentrated rows under near-isotropic readers, declared before the run at 0.015 and confirmed by the out-of-scope error; inside it the law holds on every world no earlier registration held together; the one in-scope miss is the Laplace family at N = 12000, where the law has no term in N, at 0.656, 0.917 and 0.67 on three seeds against limits of 0.655, 0.73 and 0.64. Absorbed by: declaration. Revision: the standing law of the track is the D2v7 law with this scope; its second boundary, in N for the Laplace family, is on record and not declared; a registration that declared it would need a term in N, a change of family, and is not registered.

**Failed, with witness.**

- OD:world-transfer, transfer of a law frozen on synthetic worlds to embedding corpora, ANN corpora, and dynamical state spaces without retuning. Claim: With full-dimensional clouds at d = 384 and 512 in the discovery set under the log hub-excess target, the frozen law log(excess) = -0.950 - 0.010 / hill_rk + 0.219 log(d_eff) + 0.366 sqrt(id_twonn) predicts hubness on the bracketed clouds, on a cube one step beyond, on the heavy tails, on fresh real slices and at larger N, and beats the nominal law, the chance level and the frozen D2v7 law. `experiments/DISCOVERY-TRACK.md, D2v8 record; experiments/OD/D2v8/grade.json`. Boundary: the clouds beyond d = 256 all inside the limit and better than D2v7 (cube at d = 448 0.53, Gaussian at d = 512 0.50, cube at d = 640 0.65 against 0.73); real slices 0.14 to 0.24, the best of the track; heavy tails inside the limit but worse than D2v7 on every world (t with 4 degrees at d = 256 0.25 against 0.14); Laplace at N = 12000 at 0.96 outside 0.73; the unseen ball at d = 384 at 1.44, outside and worse than chance; pooled over the transfer groups the frozen D2v7 law at 0.44 beats the law's 0.47, the fail clause. Witness: coverage of the clouds beyond d = 256 moves the excess family's error onto the heavy tails and the ball, the sign D2v6 found for the skewness family at about a third of the size; the first law to take a neighbour-distance tail variable misreads the lightest-tailed family, the uniform ball, where the reciprocal Hill term is largest; the D2v7 law, frozen without the clouds, stands as the track's law. Absorbed by: declaration. Revision: not registered: a change of shape, a term carrying the dimension and the neighbour-distance tail together rather than either alone, is the one repair of D2v6's list not yet tried; D2v7's law is the standing law until a registration beats it on the transfer groups.


## machine checked

[`lean/DataMiningAsObservation/PoissonCeiling.lean`](https://github.com/ahb-sjsu/observation-data-mining/blob/f3914f0/lean/DataMiningAsObservation/PoissonCeiling.lean), theorems `mass_nonneg`, `tail_antitone`, `tail_zero`, `tail_le_one`, `expectedAtLeast_antitone`, `example_mean`, at observation-data-mining f3914f0; what the check covers is stated in the book's [appendix C](https://github.com/ahb-sjsu/observation-data-mining/blob/f3914f0/chapters/machine_checked.md).

## used in

*Data Mining as Observation* primer S, chapters 0, 3.

## related

hubness, anti-hub, harness, min-over-strata

## see also

Book equations stated beside the entry's terms, not defining it: 10.3.

Ledger rows that cite the entry's records without naming it: NEG-11.

Sources-table rows that share a record with the entry without naming it: chapter 3 section 3.5, chapter 8 section 8.1, chapter 10 section 10.2, chapter 10 section 10.3, chapter 11 section 11.6.

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
