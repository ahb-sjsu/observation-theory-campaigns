# Observation Theory encyclopedia

One entry per concept, instrument, result, or correction, gathered from the program's own
records and keyed by their identifiers. `SCHEMA.md` gives the fields and the rules. The
entries in `entries/` were filled by hand on 2026-09-03 to fix the schema and are the
acceptance test for the generator that will fill them from the records.

| Entry | Kind | One line |
|---|---|---|
| [the flip](entries/flip.md) | result | at matched bits the code that reconstructs worse can serve the consumer better, and a code that destroys the read subspace is worst |
| [false-clear rate](entries/false-clear-rate.md) | concept | how often a certificate's clearance was wrong, conditional on clearing, reported with coverage |
| [Youden F1 bound](entries/youden-f1-bound.md) | correction | the F1 ceiling from the Youden index holds for every score, the AUROC form only for concave ROC curves |
| [read distortion](generated/read-distortion.md) | concept | the error as the consumer experiences it, the trace of the read operator times the error's second moment |
| [alignment](generated/alignment.md) | concept | the overlap between the averaged read operator and the source covariance, the dial on which the flip turns |
| [certificate](generated/certificate.md) | concept | a claim, made at a time, that something is safe to act on, graded by a witness |
| [witness](generated/witness.md) | concept | an independent measurement of whether a certificate's claim was true |
| [coverage](generated/coverage.md) | concept | the fraction of decisions a certificate clears, read beside its false-clear rate |
| [rank certificate](generated/rank-certificate.md) | instrument | a floor on rank agreement from a corpus's distance-ratio concentration, a guarantee in its strict setting and an estimate in its percentile one |
| [vacuity threshold](generated/vacuity-threshold.md) | result | the derived level below which a clustering or retrieval certificate proves nothing |
| [coherence time](generated/coherence-time.md) | concept | the interval over which a changing quantity stays correlated with itself, past which a certificate has decorrelated |
| [blind probe](generated/blind-probe.md) | instrument | recovers a consumer's read operator from calls to the consumer alone |
| [budget cliff](generated/budget-cliff.md) | result | recovery of a read operator by a confined probe is a cliff at the full dimension, rank-independent |
| [read operator](generated/read-operator.md) | concept | the workload average of a consumer's local sensitivity outer product, whose range is the read subspace and whose kernel is the nuisance |
| [quotient](generated/quotient.md) | concept | the space of inputs with the consumer's null directions declared the same, exact for an affine consumer and local otherwise |
| [identity reader](generated/identity-reader.md) | concept | the consumer whose read operator is the identity, for which read distortion is mean squared error |
| [hubness](generated/hubness.md) | result | rows retrieved far more often than the Poisson null allows, a property of the queries and the reader rather than the corpus |
| [coupling null](generated/coupling-null.md) | concept | the case of alignment near one in which no flip is possible, the flip's stated boundary |
| [anti arm](generated/anti-arm.md) | instrument | the third code of a flip comparison, built to destroy the read subspace, expected to score worst |
| [recognizer](generated/recognizer.md) | instrument | names a manifold from the low eigenvalue multiplets or certifies that none is present |
| [refresh floor](generated/refresh-floor.md) | correction | the refuted proportional law and the sealed horizon that replaced it |
| [min-over-strata](generated/min-over-strata.md) | concept | a verdict over groups is the worst group's verdict, with abstentions counted |
| [water-filling](generated/water-filling.md) | concept | the bit allocation across directions that gives each half the log of its sensitivity-weighted variance over a water level |
| [Monotone Invariance Theorem](generated/monotone-invariance.md) | result | a strictly monotone transform of a score leaves AUROC and optimal thresholded F1 unchanged |
| [safe pruning](generated/safe-pruning.md) | concept | a pruning rule that discards no solution, proved for Apriori and monotone invariance, empirically lossless at best when learned |
| [Apriori principle](generated/apriori.md) | result | every subset of a frequent itemset is frequent, the license to prune the lattice |
| [formula search](generated/formula-search.md) | instrument | enumerates short formulas over the features, pruned by proof, with its retracted comparison carried at full size |
| [observer](generated/observer.md) | concept | a consumer, its output metric, and its budget, the triple every chapter checks |
| [consumer](generated/consumer.md) | concept | the computation that reads a vector, the first element of the observer and part of it after the read operator is known |
| [budget](generated/budget.md) | concept | the bits, rows, calls, or dollars a consumer may spend, which bounds what of the read operator can be measured |
| [nuisance](generated/nuisance.md) | concept | the kernel of the workload-averaged read operator, the directions unread at almost every row |
| [read subspace](generated/read-subspace.md) | concept | the range of the read operator, small, and recoverable from a black box at a price |
| [sensitivity](generated/sensitivity.md) | concept | the gradient of the consumer at a row, whose averaged outer product is the read operator |
| [harness](generated/harness.md) | concept | the code that evaluates a model, itself a consumer whose read subspace decides what the score measures |
| [leakage](generated/leakage.md) | concept | information in the training data known only after the decision, or an identifier that names a test row |
| [preregistration](generated/preregistration.md) | instrument | the hypothesis, the bar, and the analysis committed before the measurement is run |
| [ledger class](generated/ledger-class.md) | concept | one of six labels every headline claim carries, raised only by a sealed pass and lowered by a sealed miss |
| [sealed](generated/sealed.md) | instrument | a prediction committed with its hash recorded before the measurement, verifiable by anyone with the repository |
| [effective rank](generated/effective-rank.md) | concept | the number of directions a spectrum really uses, the participation ratio, with no cutoff to choose |
| [Poisson ceiling](generated/poisson-ceiling.md) | instrument | the largest neighbour count a row would reach by chance under the no-structure null |
| [anti-hub](generated/anti-hub.md) | concept | a row no query retrieves, where compressed indexes fail first |
| [reliability weight](generated/reliability-weight.md) | concept | zero or twice the held-out AUROC minus one, a discrimination weight reported beside its calibration error |
| [posited versus measured](generated/posited-versus-measured.md) | concept | every claim either asserted by design or backed by an artifact, stated at the top of the report |
| [Nadeau and Bengio correction](generated/nadeau-and-bengio-correction.md) | correction | the variance of a repeated cross-validation estimate inflated by one plus the fold count times the test-to-train ratio |
| [cross-corpus gate](generated/cross-corpus-gate.md) | instrument | an encoder votes only if its held-out AUROC on a corpus it was not trained on clears both nulls by the preregistered margin |
| [deployment mismatch](generated/deployment-mismatch.md) | concept | the consumer evaluated is not the consumer deployed, or time moved between the two |
| [distance concentration](generated/distance-concentration.md) | concept | the narrowing of pairwise distances with dimension, read as the reader running out of resolution |
| [calibration](generated/calibration.md) | concept | a score of 0.8 is positive eighty percent of the time, measured by the expected calibration error, separate from ranking |
| [abstention](generated/abstention.md) | concept | the verdict a stratum too thin to score receives, reported and never counted as a pass |
| [drift](generated/drift.md) | concept | a change over time in what a consumer reads or in the data, whose damage is the read distortion of the drift |
| [freshness](generated/freshness.md) | concept | whether a stored value is within its reader's coherence time, consumer-relative |
| [intrinsic dimension](generated/intrinsic-dimension.md) | concept | the number of directions a dataset varies along, twice the slope of log count against log level under Weyl's law |
| [Simpson's paradox](generated/simpsons-paradox.md) | concept | a comparison reversed by pooling, read as an aggregation quotient |
| [multiple comparisons](generated/multiple-comparisons.md) | concept | the inflation of false positives when many hypotheses are tested and the best is reported |
| [disparate impact ratio](generated/disparate-impact-ratio.md) | concept | the favourable rate in one group over the rate in another, one exactly at parity |
| [equalized odds](generated/equalized-odds.md) | concept | equal true-positive and false-positive rates across groups, which conflicts with parity when base rates differ |
| [rank-faithful](generated/rank-faithful.md) | concept | a map that preserves the ordering of distances with no bound on the stretch |
| [bi-Lipschitz](generated/bi-lipschitz.md) | concept | a map that neither stretches nor shrinks any distance by more than a fixed factor |
| [Landauer's principle](generated/landauers-principle.md) | result | erasing a bit costs at least kT ln 2, charged per bit of what the consumer keeps |
| [balanced accuracy](generated/balanced-accuracy.md) | concept | the mean of the per-class recalls, so a large class cannot hide a small one |
| [Kendall correlation](generated/kendall-correlation.md) | concept | agreeing pairs minus disagreeing pairs over all pairs, the rank certificate's statistic |
| [KL divergence](generated/kl-divergence.md) | concept | the expected log ratio of two distributions, nonnegative, zero at agreement, not symmetric |
| [recall at k](generated/recall-at-k.md) | concept | the fraction of a query's true k nearest neighbours the index returned, reported per stratum |
| [Spearman correlation](generated/spearman-correlation.md) | concept | the ordinary correlation between two lists of ranks, a proxy's correlation and not a certificate |
| [silhouette](generated/silhouette.md) | concept | a row's nearest-other minus own-cluster distance over the larger, a validity index under the identity reader |
| [whitening](generated/whitening.md) | concept | rescaling data so its covariance is the identity, a change of reader |
| [Mahalanobis distance](generated/mahalanobis-distance.md) | concept | Euclidean distance from the mean after whitening, the identity reader on whitened data |
| [lift](generated/lift.md) | concept | confidence over the consequent's support, one under independence, and unbounded at low support |
| [explained variance](generated/explained-variance.md) | concept | the fraction of variance the first k components carry, the identity reader's criterion |
| [cross-support ratio](generated/cross-support-ratio.md) | concept | the smallest item support over the largest, anti-monotone in the itemset |
| [Robin Hood index](generated/robin-hood-index.md) | instrument | the fraction of a total that would have to move from above the mean to below it to equalize the counts |
| [perplexity](generated/perplexity.md) | concept | two to the average bits per token, at least one, the vocabulary size for a uniform model |
| [standard error](generated/standard-error.md) | concept | the spread of an estimate across samples, halved only by four times the independent draws |
| [softmax](generated/softmax.md) | concept | exponentiate and normalize, positive weights summing to one, shift invariant and order preserving |
| [attention](generated/attention.md) | concept | a head weights values by the softmax of query-key scores, reading keys only through those scores |
| [product quantization](generated/product-quantization.md) | instrument | pieces quantized with their own codebooks, errors additive and codes separable |
| [bootstrap](generated/bootstrap.md) | instrument | resample with replacement, paired so that shared sampling variation cancels when scores covary |
| [chance level](generated/chance-level.md) | concept | the value a rank statistic reaches under an uninformative ranking, one half for AUROC and zero for a correlation |
| [p-value](generated/p-value.md) | concept | the fraction of null draws at least as large as the observation, at most uniform under the null |
| [confidence interval](generated/confidence-interval.md) | concept | a range that covers the true value in a stated fraction of repeated samples, missing in the rest |
| [Laplacian](generated/laplacian.md) | concept | the graph matrix whose quadratic form is half the weighted squared differences across edges, zero on constants |
| [KV cache](generated/kv-cache.md) | concept | the stored keys and values of earlier tokens, read by each head only through query-key scores |
| [eviction](generated/eviction.md) | concept | choosing what to drop from a full cache, attention over the kept subset |
| [TF-IDF](generated/tf-idf.md) | concept | term frequency times the log of document count over document frequency, zero for a term in every document |
| [bag of words](generated/bag-of-words.md) | concept | a document as its term counts, a quotient that declares word order irrelevant, the encoder's null |
| [retrieval-augmented pipeline](generated/retrieval-augmented-pipeline.md) | concept | a chain of observers whose quotients are inherited and whose rank is at most its narrowest stage's |
| [teacher forcing](generated/teacher-forcing.md) | concept | predicting each token from the correct prefix, agreeing with the free run until the first error |
| [inverted file](generated/inverted-file.md) | instrument | cells searched by probe count, a neighbour found exactly when its cell is probed |
| [dot product](generated/dot-product.md) | concept | the sum of coordinatewise products, reading length where the cosine does not |
| [projection](generated/projection.md) | concept | the component of a vector along a unit direction, the one-direction reader's quotient |
| [covariance matrix](generated/covariance-matrix.md) | concept | the weighted average of centred outer products, whose quadratic form is the variance along a direction |
| [Euclidean distance](generated/euclidean-distance.md) | concept | the identity reader's distance, which reads every coordinate at the scale it arrives in |
| [geodesic distance](generated/geodesic-distance.md) | concept | the shortest path along edges, whose ordering the geodesic-rank reader reads |

The first three entries were filled by hand and are the generator's acceptance test. The
other ninety exist only as generated entries, built from the records by `generate.py`.

The authority for a claim's class is `geometric-observation/claims/LEDGER.md`. The authority
for a measurement is the campaign track file that recorded it. An entry that disagrees with
either is rebuilt, never the other way round.

## The generator

`entries.toml` maps each entry id to the records it is built from. `generate.py` reads those
records from the local checkouts under a source root and writes `generated/<id>.md` under the
schema's headings, naming the commit of every repository it read. A record path that does not
exist fails the run. `check.py` is the acceptance test: every number in a hand-filled entry's
measurements and corrections must appear in the generated entry, and every cited path in either
must exist.

```
python encyclopedia/generate.py C:\source
python encyclopedia/check.py C:\source
```

What the generator reads. Definitions from the book's glossary. Equations from the book's
numbered displays. Ledger rows by id. Measurements from the book's sources tables, the rows
that cite the entry's records, and from campaign track tables by cell name. Corrections from
errata files and the records that carry them, whole section or paragraph, with line ranges.
Lean theorem names from the proof files. Uses from the chapters that mention the term.
Conditions are the one field curated by hand in `entries.toml`, and the generated entry says
so. Every entry now carries a machine-checked section naming the book's Lean file that checks
its checkable core, seventy-three files as of 2026-09-04, and the book's appendix C states what each
check does not cover. On 2026-09-04 the three generated entries carried every number of their hand-filled
counterparts.
