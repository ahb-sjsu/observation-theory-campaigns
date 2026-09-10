# Nine registrations, one law: the observer-relative hubness line of the OD track

Andrew H. Bond, 2026-09-10. Draft 0.1. Every number below is read from a sealed record in
`experiments/OD/` of this repository, cited by gate. Nothing here is a new claim.

## Summary

The D2 line of the Observational Discovery track asked one question nine times, each time
under a sealed registration with its bars fixed before the run. Is there a law, discovered
by a declared search over a declared family of variables, that predicts how hubby a corpus
becomes when it is read through an observer, and that survives observers, families of
worlds, real corpora and larger samples it was not discovered on? The answer after nine
registrations is one law, one declared scope and two named boundaries. The law predicts the
log of the Poisson hub excess from three variables of the observed data, the concentration
of the tenth-neighbour distance, the spectral dimension and the intrinsic dimension. Inside
its scope it held on every unseen world the track ever built, on fresh real corpora and at
four times its discovery sample, and it beat the nominal formula and the chance level in
every group. Outside its scope it fails, and the record says how. The route to it went
through four laws in the skewness that each held one side of a divide and lost the other,
a change of target that dissolved the divide, and a coverage repair that reproduced it in
miniature. Three of the nine registrations failed and are recorded as failures.

## 1. The question and the instrument

A hub is a row that appears in many other rows' nearest-neighbour lists. The program's
hubness instrument counts, for every row of a corpus, how often it is retrieved among the
ten nearest neighbours of the other rows, and summarises the counts two ways. The skewness
of the counts is the classical summary. The Poisson hub excess is the busiest row's count
divided by the largest count that a random assignment of the same retrieval slots would be
expected to reach. An excess of one is chance. The observer is a linear read of the corpus,
a rotation followed by a diagonal rescaling whose spectrum falls as a power of the index,
with the exponent from zero (a pure rotation) to two (a reader that sees one direction).
The track's earlier gates and the openvector-bench campaign had shown that the hubs of a
corpus are made by the reader as much as by the corpus. The D2 line asked whether the
amount of hubness is lawful in the reader's own variables.

The family of laws was declared once and kept. A law is linear in at most three features
drawn from a pool of transforms of variables measured on the observed data (spectral
dimension, entropy dimension, top eigenvalue share, distance concentration, the shape of
the centroid distances, the TwoNN intrinsic dimension, the concentration of the tenth
neighbour distance, and from D2v5 on, four tail measures of the neighbour distances). The
search fits every model of the family on the training worlds and ranks by error on
held-out worlds under unseen observer spectra. The pilot freezes the best. The registration
is sealed by renaming with the frozen law inside, the run uses a fresh seed, and the sealed
grader grades. The bars are multiples of REF, the frozen law's own pooled pilot error. Fresh
seeds within 1.5 REF, every unseen world within 2 REF and the group within 1.5 REF, real
corpora within 3 REF, scale cells within 2 REF, and the law at most 0.8 of the nominal
formula's error and of every earlier frozen law's at 0.9 or 0.95, pooled and within every
group. A competitor beating the law pooled on the transfer groups is a FAIL. Anything short
of every bar and short of a fail clause is INDETERMINATE.

## 2. The nine registrations

| gate | what changed | frozen law | verdict | what decided it |
|---|---|---|---|---|
| D2 | Gaussian clouds only | skew from distance concentration and spectral dimension | FAIL | the law did not transfer off Gaussians |
| D2v2 | seven shape families | skew from entropy dimension, concentration, top share | INDETERMINATE | held every synthetic family and SIFT, missed Wikipedia (intrinsic dimension 8 to 20 under a spectral dimension to 320) |
| D2v3 | manifold worlds in the set | skew from concentration, intrinsic dimension, spectral dimension | INDETERMINATE | real corpora within REF; missed a cube at d = 256 and heavy tails at N = 16000 |
| D2v4 | clouds at d = 256 and heavy tails in the set | skew from centroid spread, nominal dimension, intrinsic dimension | INDETERMINATE | extrapolated to d = 512, real slices at 0.43; missed heavier tails at higher d |
| D2v5 | tail variables on the neighbour distances | the search declined them; D2v3's form refitted | INDETERMINATE | halved D2v4's misses, lost heavy tails at N = 16000 |
| D2v6 | heavy tails placed at the transfer dimensions | skew, nominal dimension term | FAIL | the frozen D2v5 law beat it pooled; the tails fit, the d = 512 clouds were lost |
| D2v7 | target changed to log hub excess | log excess from concentration, spectral and intrinsic dimension | INDETERMINATE | held heavy tails, d = 512 Gaussian, real, scale at once; missed the cube at d = 512 and one scale cell by 0.001 |
| D2v8 | clouds at d = 384 to 512 in the set under the new target | first law to take a neighbour-distance tail term | FAIL | the frozen D2v7 law beat it pooled; the clouds fit, the tails and a ball were lost |
| D2v9 | no search; the D2v7 law with a declared scope | the D2v7 law | INDETERMINATE | every bar held except the one cell named in advance |

Records: `experiments/DISCOVERY-TRACK.md`, sections D2 to D2v9; `experiments/OD/D2*/grade.json`;
`claims/transformations/OD.toml`.

## 3. What the discovery set taught

The first four registrations changed the discovery set and kept everything else, and the
law changed with the set each time. D2's law, found on Gaussian clouds, read the distance
concentration and the spectral dimension and failed off Gaussians. D2v2's law, found on
seven shape families, held every synthetic family and the SIFT descriptors and missed the
Wikipedia embeddings, whose TwoNN intrinsic dimension of 8 to 20 sat under a spectral
dimension of up to 320. The intrinsic dimension was in the pool and the search had dropped
it, because on full-dimensional families it duplicates the spectral dimension. D2v3 put
manifold worlds into the set, the search took the intrinsic dimension, and the law fitted
every real corpus within its own pilot error. The Wikipedia error fell from 5.3 to 2.5 to
1.0 across the three gates. The registry test written after D2v3 says it in one line. The
discovery set decides the law.

D2v4 widened the set to full-dimensional clouds at d = 256 and heavy tails, and its law
extrapolated to clouds at d = 512 that D2v3's law had missed by a factor of three. It
missed the heavier tails at higher dimension than the set held, Student t with four
degrees at d = 256 at 3.52 against a limit of 2.13 and Laplace at d = 192 at 4.75. Its record
named two repairs, a tail variable measured on the neighbour distances and heavy tails
placed at the transfer dimensions, and the next two registrations took them in turn.

## 4. What the family could not do

D2v5 put four scale-free tail measures of the neighbour distances into the pool. The search
declined every one of them. The best model containing a tail variable had held-out error
0.752 against the frozen law's 0.709 and was worse on five of the eight heavy-tailed pilot
worlds, and that was recorded in the registration before the run, as the first outcome its
falsification section had named. The law the search froze was D2v3's form refitted with
heavy tails at d = 128 and 192 in the training rows. It halved D2v4's misses and paid with
the scale, losing the heavy tails at N = 16000 that D2v4 had held.

D2v6 placed the heavy tails in the discovery set at the dimensions the transfer asked about,
bracketing the unseen worlds. Its pilot produced the first law of the track whose pooled
pilot error trailed two competitors on the same rows, the frozen D2v5 and D2v3 laws, because
the search ranks by held-out error and the training rows now held the hardest worlds. The
run confirmed the trade. Every bracketed heavy-tailed world fitted, Student t with four
degrees at d = 256 at 1.64 against D2v4's 3.52, and the clouds at d = 512 were lost, the cube
at 4.65 against D2v5's 1.09. The frozen D2v5 law was the better predictor pooled over the
transfer groups and the gate failed by its own clause. Three registrations had by then put
the same worlds on both sides of the same limit. The largest error of every law sat where
the hubness skewness exceeds 12, on isotropic readers of heavy-tailed or very
high-dimensional clouds, where a linear law in either transform of the skewness cannot
turn over. The D2v6 record said the family, not the set, was the limit, and that the next
registration had to change the target or the shape.

## 5. The target was the limit

D2v7 changed the target and nothing else. The law predicts the log of the Poisson hub
excess, errors are root-mean-square log ratios, and the chance level is zero. On D2v6's
world, the same 73 worlds and readers, the search froze

    log(excess) = -1.103 - 0.025 / cv_knn + 0.167 log(d_eff) + 0.434 sqrt(id_twonn)

with pooled pilot error 0.328, a factor of 1.39 in the excess, against 1.135 for the nominal
formula and 1.598 for chance. In sample it fitted the heavy tails at d = 256 and the clouds
at d = 256 at once, where D2v6's law had read 5.41 on Student t with three degrees. On the
run it held Student t with four degrees at d = 256 at 0.18, Laplace at d = 224 at 0.19,
Student t with 2.5 degrees at d = 128 at 0.11, the Gaussian at d = 512 at 0.58, the four fresh
real slices at 0.19 to 0.45, and the heavy tails at N = 16000 at 0.35 to 0.44, together. It
beat the nominal formula and chance pooled and inside every group, the first law of the
track to do so. It missed two per-world limits by small margins, the cube at d = 512 at 0.82
against 0.66 and Laplace at N = 12000 at 0.656 against 0.655. The record's reading is that the
skewness saturates where the excess keeps counting, and a law linear in the concentration
and the dimensions can turn over in one and not in the other. Same family, same pool, same
search, same worlds. The target was the limit.

## 6. Coverage under the new target

D2v8 asked whether the excess family, unlike the skewness family, takes coverage without
paying for it. Clouds at d = 384 and 512 joined the training set, bracketing an unseen cube
at d = 448 and an unseen ball at d = 384. The search chose, for the first time in the track,
a neighbour-distance tail variable, the reciprocal of the Hill log-excess of the tenth
neighbour distance, and the pilot again showed the frozen D2v7 law ahead on the same rows.
The run bought every full-dimensional world beyond d = 256, the cube at d = 640 one step
beyond the set at 0.65 against D2v7's 0.76, and the best real-slice errors of the track,
0.14 to 0.24. It paid on every heavy-tailed world, on two heavy-tailed scale cells, and on
the unseen ball at d = 384, at 1.44 and worse than chance. The D2v7 law was again the better
predictor pooled and the gate failed. The trade-off D2v6 had found in the skewness family
held in the excess family at about a third of the size and with the same sign.

## 7. The boundary

Before a ninth registration, an exploration on the rows already collected asked whether
any shape of the declared family holds the clouds beyond d = 256 and the heavy tails at
once under the sealed bars, scored against the frozen D2v7 law. Twelve configurations,
products of tail and dimension, four terms, softened reciprocals, the divergent terms
removed, a concentrated world held out, on two training sets. None passed, and the four-term
search on the D2v7 set overfitted its held-out worlds to a transfer error of 0.79 with the
ball at 3.2. The exploration named the mechanism instead. Under the isotropic reader the
uniform ball at d = 384 has a tenth-neighbour concentration of 0.003, six times below a
Gaussian's at the same dimension. The law's concentration term is a reciprocal, it diverges
there, and it predicts an excess near zero against a truth of 1.4. Remove the reciprocal and
the law loses the real corpora, which the reciprocal fits. That is a shape boundary of the
family. (`experiments/OD/D2v9_explore/README.md`.)

D2v9 registered the boundary as the claim and searched nothing. A row is in scope when its
tenth-neighbour concentration on the observed data is at least 0.015, a threshold declared
from the collected rows before the pilot and not moved after it. Inside the scope the frozen
D2v7 law is claimed within D2v7's bars on fresh worlds. Outside it the law is not claimed,
and its pooled error there must exceed the in-scope limit, or the scope was a convenience
and the claim fails as stated. The Laplace scale cell at N = 12000 sits inside the scope, and
the registration named it in advance as the bar that would decide PASS against
INDETERMINATE, with the reason the scope must not cover it, which is that the law has no
term in N. The
pilot's own rows showed the scope catching rows the law fits as well as rows it misses, and
the registration said so before the run.

The run held every bar but that one. All eighteen unseen worlds sat inside the limit on
their in-scope rows, the balls at d = 256 and 384 at 0.43 and 0.44 and the cube at d = 640 at
0.37 among them, pooled 0.31 against 0.48. The real slices read 0.12 to 0.41. The law beat
both competitors in every group at 0.34 against 1.63 and 1.64. The out-of-scope rows, 180 of
them in twelve worlds, erred at 1.19 against 0.64, the balls under-predicted and the cubes
over-predicted, with two worlds, the torus and the sphere, fitted anyway. Laplace at
N = 12000 read 0.67 against 0.64. INDETERMINATE, by the named cell and no other.

## 8. The scale sweep

After D2v9, one annotation and not a gate (`experiments/OD/D2_close/README.md`). Laplace at
d = 64 and, as the control, Student t with three degrees, at N = 4000, 8000, 12000 and 16000,
three seeds each, with the frozen law applied as it stands and the D2v9 limit of 0.64. The
Laplace error is 0.49 at N = 4000 with every seed inside, steps to 0.74 at N = 8000 and stays at
0.76 through N = 16000, with two of three seeds over the limit at every N from 8000 up. The
control stays at 0.23 to 0.38 at every N with no seed over. The miss sits at the near-isotropic
readers, a factor of about four at exponent zero from N = 8000 up against about two at
N = 4000, and it is gone by exponent one. The Laplace excess under the isotropic reader roughly
doubles between N = 4000 and 8000 and then saturates, and the law's three variables do not
move with N, so it cannot follow. It is a boundary in N for one family, with a step and a
plateau, and not a cell on the limit. It is recorded and not declared. A law that covered it
would carry a term in N, which is a new family, and the line closes without registering one.

## 9. What stands

The standing law of the track is the D2v7 law with the D2v9 scope. Its statement is short.
For a corpus read through a linear observer, on rows whose tenth-neighbour distances vary by
at least 1.5 percent, the log of the busiest row's retrieval count over the Poisson ceiling
is a linear function of the reciprocal of that variation, the log of the spectral dimension
and the square root of the TwoNN intrinsic dimension of the observed data, to a factor of
about 1.4 in the excess, on every family of world the track built, on Wikipedia and SIFT
slices it never saw, and at four times its discovery sample. Its two boundaries are on
record. Below 1.5 percent variation the concentration term diverges and the law is
withdrawn. For the Laplace family at N = 12000 the law under-predicts by a factor of about
three under the isotropic reader, because it carries no term in N. The sweep of Section 8
shows it is a boundary in N, a step between N = 4000 and 8000 and a plateau after. Neither boundary is repaired by
a change of set, and the exploration says the family has no shape that repairs the first
without losing the real corpora.

## 10. What the discipline did

Three things happened in this line that the discipline was written to make happen. The bars
never moved. Every registration's REF and limits were fixed from its own pilot before the
seal, and three registrations failed on their own clauses. Two pilots produced a frozen law
that trailed a competitor on the pilot's own rows, D2v6's and D2v8's, and both were sealed
and run as registered with that fact recorded in Section 7, because the transfer groups are
the test and the pilot is not. And when the owner asked for a registration that would pass,
the answer the record allowed was a change of claim, a boundary declared before the run with
its risk named, and the run returned exactly the outcome the risk named. A registration
built to pass by dropping the worlds that fail, without naming that as a scope, was not
built.

The line also produced its finding by the ordinary route of the discipline, four failures
in a row on the same worlds. The discovery set decides the law (D2 to D2v4). The family
cannot hold both sides of the skewness divide (D2v5, D2v6). The target was the limit (D2v7).
Coverage moves the excess family's error too (D2v8). The boundary is a divergent term, not
a missing world (D2v9 and the exploration). Each of those is a registry test in
`claims/transformations/OD.toml` with its record beside it, and the encyclopedia's hubness
entry carries them at erisml.org/encyclopedia.

## References to records

- `experiments/DISCOVERY-TRACK.md`, gates D2, D2v2, D2v3, D2v4, D2v5, D2v6, D2v7, D2v8, D2v9, with
  the run records and seal blob hashes.
- `experiments/OD/D2v7/law.json`, the standing law; `experiments/OD/D2v9/law.json`, the same law
  with its scope; `experiments/OD/D2v9/grade.json`, the boundary run.
- `experiments/OD/D2v9_explore/README.md`, the twelve-shape exploration.
- `experiments/OD/D2_close/`, the scale sweep of Section 8.
- `claims/transformations/OD.toml`, the registry tests, one per registration.
