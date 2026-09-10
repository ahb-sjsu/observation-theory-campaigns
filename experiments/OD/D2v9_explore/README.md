# D2v9 exploration (2026-09-09, not a gate)

Pre-registration exploration on rows already collected (the D2v7 and D2v8 pilots and the D2v8 run), asked
before any D2v9 registration: is there a shape in the declared law family that holds the clouds beyond d = 256
and the heavy tails at once under the sealed bars, scored against the frozen D2v7 law? Every law here is
discovered on a pilot's training and held-out rows exactly as a pilot would and scored on the D2v8 run rows the
way the sealed grader scores (REF = pooled pilot error; L2 2 REF per unseen world and 1.5 pooled; L4 2 REF per
scale cell; L5 at 0.95 of the D2v7 law pooled and inside every group). Nothing here is a registered claim.

| configuration | script | training rows | pooled transfer error | worst worlds |
|---|---|---|---|---|
| frozen D2v7 law (reference) | `d2v9_explore.py` | none | 0.442 | ball at d = 384 1.21, cube at d = 640 0.76, Laplace at N = 12000 0.92 |
| 3 terms, base pool | `d2v9_explore.py` (A: D2v8 pilot) | D2v8 | 0.473 (= the sealed D2v8 law) | ball 1.44, Laplace N = 12000 0.96 |
| 3 terms, tail-by-dimension products added | A / B | D2v8 / D2v7 | 0.473 / 0.482 | ball 1.44 / 1.69 |
| 4 terms, products added | A / B | D2v8 / D2v7 | 0.454 / 0.793 | ball 1.44 / 3.19 |
| softened reciprocals 1/(x+c) added, 3 and 4 terms | `d2v9_explore2.py` | D2v8 / D2v7 | the ranking never chooses a softened term | ball 1.44 to 1.58 |
| divergent reciprocals removed, 3 terms | `d2v9_explore3.py` | D2v8 / D2v7 | 0.518 / 0.469 | ball 0.95 / 0.66; real slices 0.20 / 0.45; torus, mixture outside |
| as above with the ball at d = 128 moved to held-out, 3 and 4 terms | `d2v9_explore3.py` | D2v8 / D2v7 | 0.446 to 0.568 | ball 0.93 to 0.97, cube at d = 640 0.69 to 0.90, real slices 0.38 to 0.64 |

Finding. No shape of the family passes the sealed bars on this world; every one moves the error and none
removes it. The mechanism: under the isotropic reader the uniform ball at d = 384 has neighbour-distance
concentration cv_knn = 0.003, six times below the Gaussian's at the same dimension, and every law of the
family carries the concentration as a reciprocal, which diverges there and predicts an excess near zero
where the truth is 1.4; removing the reciprocal brings the ball inside and loses the real corpora, which
the reciprocal fits. The second persistent miss, Laplace at d = 64 and N = 12000, reads 0.656 against a
limit of 0.655 on D2v7's seed and 0.92 on D2v8's: seed variance at an excess of about 130. The frozen D2v7
law is the frontier of this family on this world, and its boundary is a shape boundary (over-concentrated
full-dimensional worlds under the isotropic reader) and a scale cell on the limit. A D2v9 that could pass
its bars exists only as a different claim, a boundary claim with the D2v7 law frozen and the scope declared
with its reason; that registration is not written here.

Files: `explore.log`, `explore2.log`, `explore3.log` (the runs); `explore_A.json`, `explore_B.json`,
`soft_*.json`, `nodiv_*.json` (each configuration's law, per-world errors and bars); the three scripts.
