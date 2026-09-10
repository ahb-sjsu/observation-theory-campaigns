# Closing annotation of the D2 line (2026-09-10, not a gate)

Question. The D2v9 record left one boundary of the standing law undeclared, the Laplace family at
d = 64 and N = 12000, where the frozen D2v7 law read 0.656, 0.917 and 0.67 on three seeds against
limits of 0.655, 0.73 and 0.64. Is that a boundary in N, or a cell on the limit?

Sweep (`d2_close_sweep.py`, `sweep.json`, `sweep.log`, Atlas 2026-09-10). Laplace at d = 64 and, as
the control that held on every earlier run, Student t with 3 degrees at d = 64, at N = 4000, 8000,
12000 and 16000, three seeds each (20261019 to 20261021), the D2v9 observers and k ladder, the frozen
D2v7 law applied as it stands, error the RMS log ratio in hub excess on in-scope rows (cv_knn at least
0.015, which every row of these worlds satisfies), against the D2v9 limit 2 REF = 0.638.

| family | N = 4000 | N = 8000 | N = 12000 | N = 16000 |
|---|---|---|---|---|
| Laplace, mean over seeds (min to max) | 0.49 (0.39 to 0.56) | 0.74 (0.56 to 0.86) | 0.76 (0.55 to 0.90) | 0.76 (0.58 to 0.85) |
| Laplace, seeds over the limit | 0 of 3 | 2 of 3 | 2 of 3 | 2 of 3 |
| Student t with 3 degrees, mean | 0.23 | 0.24 | 0.38 | 0.29 |
| Student t, seeds over the limit | 0 of 3 | 0 of 3 | 0 of 3 | 0 of 3 |

Reading. A boundary in N for the Laplace family, with a step between N = 4000 and N = 8000 and a
plateau after it, not a gradual growth and not seed variance alone (one seed of three sits just
under the limit at every N from 8000 up, two sit over). The miss is at the near-isotropic readers:
the median residual at exponent 0 is -0.5 to -1.0 in log excess at N = 4000 and -0.9 to -1.5 from
N = 8000 up, a factor of about four, and it is gone by exponent 1 (-0.01 to -0.24) at every N. The
Laplace excess under the isotropic reader roughly doubles between N = 4000 (21 to 29) and N = 8000
(29 to 49) and then saturates (52 to 57 at 12000 and 16000); the law's three variables do not move
with N, so it cannot follow. Student t with 3 degrees, whose excess also grows with N, stays inside at
every N, so the boundary is the family's and not the sample size's alone.

Statement for the record. The standing law of the track is the D2v7 law with the D2v9 scope, and it
has two boundaries. Below a tenth-neighbour concentration of 0.015 the concentration term diverges
and the law is withdrawn (D2v9, declared and tested). For the Laplace family at N of 8000 or more
under readers with exponent below 1, the law under-predicts the excess by a factor of about four
(this annotation, recorded and not declared). A law that covered the second would carry a term in N
and is a new family; it is not registered. The D2 line is closed at nine registrations.
