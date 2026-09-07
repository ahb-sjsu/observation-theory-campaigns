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
| [geometric decision cost](generated/geometric-decision-cost.md) | concept | the Mahalanobis distance of an alternative's encoding from a task's reference point, the pullback distance of the encoding under the inverse covariance |
| [licensed, not licensed](generated/licensed.md) | concept | a theorem checked in Lean or a sealed measurement that survived its null and bar, against exploratory or posited |
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
| [degree](generated/degree.md) | concept | the number of edges a node has, summing to twice the edge count |
| [eigenvalue, eigenvector](generated/eigenvalue-eigenvector.md) | concept | a direction a symmetric matrix only stretches and the factor, orthogonal across distinct eigenvalues |
| [isotropic](generated/isotropic.md) | concept | the same variance in every direction, which every reader reads alike, so the flip needs anisotropy |
| [threshold](generated/threshold.md) | concept | the value at which a score becomes a decision, shrinking the predicted set as it rises |
| [ROUGE](generated/rouge.md) | concept | overlap of a candidate with a reference over the reference's length, reading bags and not order |
| [classifier](generated/classifier.md) | concept | a consumer that scores a row and thresholds the score, with a rank-one read operator when linear |
| [decision boundary](generated/decision-boundary.md) | concept | the inputs whose score equals the threshold, crossed once along the weights and never orthogonally |
| [margin](generated/margin.md) | concept | how far a score sits from the threshold, a certificate against perturbations smaller than it |
| [null model](generated/null-model.md) | instrument | the data with the structure under test removed and everything else kept, the comparison every number needs |
| [escalation](generated/escalation.md) | concept | handing an item to a person rather than deciding it, coverage traded for a false-clear rate |
| [score](generated/score.md) | concept | the number a classifier produces before a threshold, whose ordering fixes every decision |
| [confound](generated/confound.md) | concept | a variable moving with treatment and outcome, biasing the naive difference by its effect times its imbalance |
| [replica](generated/replica.md) | concept | a copy trailing the primary by a lag, whose stale keys grow with the lag |
| [block error rate](generated/block-error-rate.md) | concept | the fraction of radio blocks the receiver cannot decode, at most the symbol count times the symbol loss rate |
| [template match](generated/template-match.md) | instrument | the smallest log-distance to a stored eigenvalue-ratio template, reading shape and not size |
| [cache](generated/cache.md) | concept | a store of recent data whose hit rate is the requests' number, zero cold and one warm |
| [hash](generated/hash.md) | instrument | a fixed-length fingerprint whose change proves a change and whose equality is evidence |
| [encoder](generated/encoder.md) | concept | a model that maps an input to an embedding, voting only when it clears the cross-corpus gate |
| [embedding](generated/embedding.md) | concept | a vector per object, a quotient of the objects, with a further quotient under a cosine reader |
| [head](generated/head.md) | concept | one attention operation, reading its keys only through their scores against its query |
| [paraphrase class](generated/paraphrase-class.md) | concept | the rewordings of one input, across which an invariant verdict does not move |
| [contrastive objective](generated/contrastive-objective.md) | concept | pulls declared pairs together and pushes others apart, so the declared pairs define similar |
| [validity index](generated/validity-index.md) | concept | a clustering score without labels, an output metric that needs a null |
| [query, key, value](generated/query-key-value.md) | concept | the three vectors a token produces in attention, keys read along the query and values averaged |
| [commit hash](generated/commit-hash.md) | instrument | git's fingerprint of a snapshot, fixing the state a number was measured in |
| [itemset](generated/itemset.md) | concept | items that appear together, with support anti-monotone and every maximal frequent itemset closed |
| [support](generated/support.md) | concept | the fraction of transactions containing an itemset, which cannot rise as the itemset grows |
| [confidence](generated/confidence.md) | concept | a rule's itemset support over its antecedent's, equal to the consequent's support under independence |
| [precision, recall](generated/precision-recall.md) | concept | predicted positives that are true, and true positives that were predicted, with F1 their harmonic mean |
| [F1](generated/f1.md) | concept | twice precision times recall over their sum, whose optimum over thresholds depends only on the ranking |
| [AUROC](generated/auroc.md) | concept | the chance a random positive outscores a random negative, one at separation, one half at chance, ranking-only |
| [trace](generated/trace.md) | concept | the sum of the diagonal, linear, order-free on products, and the read distortion of a rank-one error |
| [bit](generated/bit.md) | concept | the unit of a budget, doubling the levels, halving the step, and quartering the squared error |
| [graph](generated/graph.md) | concept | nodes and edges, the neighbourhood graph with k out-neighbours and its symmetric mutual form |
| [manifold](generated/manifold.md) | concept | a surface that looks flat up close, whose dimension the Laplacian's eigenvalue count reveals |
| [quantization](generated/quantization.md) | concept | replacing each number by one of a few allowed values, with error at most half a step |
| [codebook](generated/codebook.md) | concept | the allowed values under the nearest-codeword rule, with distortion never larger for a larger codebook |
| [direction-only quantizer](generated/direction-only-quantizer.md) | instrument | length stored exactly and direction rounded, so the score error scales with the length |
| [per-channel quantizer](generated/per-channel-quantizer.md) | instrument | a step per coordinate, with squared error at most the sum of the squared half steps |
| [spectrum](generated/spectrum.md) | concept | a matrix's eigenvalues, whose effective rank lies between one and the dimension |
| [hub](generated/hub.md) | concept | a row retrieved far more often than chance allows, few by arithmetic and a property of the queries |
| [concentrated](generated/concentrated.md) | concept | a spectrum with a few eigenvalues carrying most of the total, with effective rank at most one over the fraction squared |
| [challenge set](generated/challenge-set.md) | instrument | a test collection on which a benchmark-passing shortcut fails, necessarily outside the benchmark |
| [cross-validation](generated/cross-validation.md) | instrument | folds tested once each, whose size-weighted mean accuracy is the overall accuracy, sharing training data |
| [rotary position embedding](generated/rotary-position-embedding.md) | concept | a rotation by position under which a head reads relative position only |
| [anisotropic](generated/anisotropic.md) | concept | a covariance with unequal variances across directions, the condition under which readers disagree |
| [anti-monotonicity](generated/anti-monotonicity.md) | concept | support cannot rise as an itemset grows, the license Apriori prunes under |
| [attribution](generated/attribution.md) | instrument | a per-feature share of one prediction, which for a gradient sums to the output change and estimates the read operator |
| [commute time](generated/commute-time.md) | concept | steps there and back for a random walk, symmetric, whose collapsed resistance depends on degrees alone |
| [expected calibration error](generated/expected-calibration-error.md) | instrument | the bin-weighted gap between mean score and positive fraction, zero exactly when calibrated |
| [finite difference](generated/finite-difference.md) | instrument | a derivative from two evaluations a step apart, exact on quadratics when centred, at a price of 2d |
| [latent semantic analysis](generated/latent-semantic-analysis.md) | instrument | principal components on the TF-IDF matrix, the identity reader on term-document variance |
| [multiplet](generated/multiplet.md) | concept | a group of equal or near-equal eigenvalues, the circle's paired at k and n minus k |
| [output metric](generated/output-metric.md) | concept | the rule that scores a consumer's mistakes, under which a negated consumer keeps its read operator and reverses every ranking |
| [principal component analysis](generated/principal-component-analysis.md) | instrument | projection onto the top eigenvectors, whose dropped error is the dropped eigenvalues, the identity reader's code |
| [sources table](generated/sources-table.md) | instrument | the per-chapter table naming the file and lines behind every number, bound by a commit hash |
| [spectral embedding](generated/spectral-embedding.md) | instrument | a node's low-eigenvector coordinates, whose row normalization is the unit sphere and keeps the cosine |
| [token](generated/token.md) | concept | the unit a language model reads and writes, whose bits per token set the perplexity |
| [transmission time interval](generated/transmission-time-interval.md) | concept | the one-millisecond slot a 5G tower schedules in, the unit the refresh floors are counted in |
| [Weyl's law](generated/weyls-law.md) | concept | the eigenvalue count grows like the value to half the dimension, which the slope reads off |
| [anti-hub recall](generated/anti-hub-recall.md) | instrument | recall at k on the rarely retrieved rows, taken as the minimum over strata |
| [boosting](generated/boosting.md) | instrument | weak scorers fitted in sequence, with a step size positive exactly when one beats chance and a reweighting that makes its error one half |
| [cold, warm](generated/cold-warm.md) | concept | a measurement before or after the cache is filled, with the hit rate zero cold and one warm on the footprint |
| [cosine](generated/cosine.md) | concept | the dot product over the two lengths, between minus one and one and unchanged by rescaling |
| [curvature](generated/curvature.md) | concept | the second derivative of a consumer, which the finite difference does not read and which sets the linear model's error |
| [DBSCAN](generated/dbscan.md) | instrument | core points by neighbour count within a radius, clusters by reachability, the rest noise |
| [decision tree](generated/decision-tree.md) | instrument | axis-aligned splits, flat within a leaf, so the sensitivity is zero almost everywhere |
| [density](generated/density.md) | concept | the local crowding of rows, the coordinate the geodesic reader discards and DBSCAN reads |
| [ensemble](generated/ensemble.md) | instrument | an average of scorers, between its members and with squared error at most their mean squared error |
| [Hessian](generated/hessian.md) | concept | the matrix of second derivatives, diagonal for a score additive across features |
| [hierarchical clustering](generated/hierarchical-clustering.md) | instrument | merging the closest clusters under a linkage whose merge heights never decrease |
| [importance](generated/importance.md) | instrument | a per-feature score of how much a classifier reads it, counting splits for a tree |
| [imputation](generated/imputation.md) | instrument | writing a value into a missing cell, which for the mean keeps the mean and shrinks the variance |
| [Jaccard](generated/jaccard.md) | concept | intersection over union, in the unit interval and zero exactly when disjoint |
| [Jacobian](generated/jacobian.md) | concept | the derivative matrix of a vector-valued consumer, absent for a discrete stage |
| [k-means](generated/k-means.md) | instrument | the sum of squared errors to centres, minimized by the mean, the identity reader's clustering |
| [logistic regression](generated/logistic-regression.md) | instrument | the sigmoid of a weighted sum, whose decision at one half is the sign of the sum |
| [naive Bayes](generated/naive-bayes.md) | instrument | a product of one-dimensional likelihoods whose log is additive, blind to interactions |
| [neighbourhood graph](generated/neighbourhood-graph.md) | concept | each row joined to its k nearest rows or to every row within a radius |
| [operating point](generated/operating-point.md) | concept | the row at which a consumer is read or the threshold at which a classifier is scored, at 2d evaluations each |
| [outlier](generated/outlier.md) | concept | a row the reader cannot place, past a z-score threshold for at most one over the threshold squared of the weight |
| [refresh interval](generated/refresh-interval.md) | instrument | the longest renewal period that keeps a certificate within its error, measured and not assumed |
| [ROC curve](generated/roc-curve.md) | instrument | true positive rate against false positive rate as the threshold sweeps, with area the AUROC |
| [seed](generated/seed.md) | concept | the number that fixes a run's randomness, so only different seeds measure variance |
| [shard](generated/shard.md) | instrument | a partition of an index searched separately, whose merged top k loses nothing |
| [spectral clustering](generated/spectral-clustering.md) | instrument | clustering the row-normalized spectral embedding, which reads the angle and discards the density |
| [standardization](generated/standardization.md) | instrument | subtracting the mean and dividing by the spread, invertible and order preserving |
| [stratification](generated/stratification.md) | instrument | scoring strata separately so that the minimum over strata can be reported |
| [Youden index](generated/youden-index.md) | instrument | true positive rate minus false positive rate, whose maximum bounds the best F1 |
| [variance](generated/variance.md) | concept | the weighted mean of the squared deviation of a column from its weighted mean |
| [rank](generated/rank.md) | concept | the dimension of a matrix's column space |
| [metric](generated/metric.md) | concept | a rule for the distance between two rows, or between two outputs |
| [correction](generated/correction.md) | concept | a change to a published number or claim that the record keeps beside the original, naming what was wrong and what replaced it |
| [correlation](generated/correlation.md) | concept | the cosine of two centred columns |
| [floor, ceiling](generated/floor-ceiling.md) | concept | a floor is a lower bound a quantity cannot fall below, and a ceiling an upper bound it cannot exceed, each proved or measured and named as such |
| [gate](generated/gate.md) | instrument | a bar that a build or a claim must pass before it proceeds, with the bar and the null written down first |
| [distortion](generated/distortion.md) | concept | the error a code costs a reader, the trace of the read operator against the error covariance |
| [bar](generated/bar.md) | instrument | a threshold a statistic must reach, written down before the measurement |
| [verdict](generated/verdict.md) | concept | the outcome of a registered test, pass, fail, or abstain, taken as the worst group with the groups too thin to score counted |
| [registered](generated/registered.md) | concept | of a claim, bar, null, or budget, written into a sealed file before the measurement, so that a changed digest would prove a changed prediction |
| [refusal](generated/refusal.md) | concept | an instrument's declining to report a number it cannot support, when samples do not exceed the dimension, when no template matches, or when a group is too thin |
| [control](generated/control.md) | instrument | a comparison arm that should not show the effect, run beside the arm that should |
| [sweep](generated/sweep.md) | instrument | running a measurement across a range of one parameter, a threshold, a budget, or a degradation, and reading the curve |
| [baseline](generated/baseline.md) | instrument | the simplest scorer a claim must beat, chance, a constant, an untrained encoder, or a single model, run under the same protocol |
| [audit](generated/audit.md) | instrument | a check of a published number or system against its record, by a reader who did not produce it |
| [planted](generated/planted.md) | instrument | of a case, built so that the answer is known before the instrument reads it |
| [matched bits](generated/matched-bits.md) | instrument | the rule that two codes are compared only at the same bit count, since each added bit halves the step and quarters the squared error |
| [declaration](generated/declaration.md) | instrument | a statement of what a study will count, drop, or treat as a failure, sealed before the run |
| [split](generated/split.md) | instrument | a partition of the rows into a part the model is fit on and a part it is scored on |
| [reconstruction error](generated/reconstruction-error.md) | concept | the squared length of the difference between a row and its approximation, the identity reader's distortion |
| [nearest neighbour](generated/nearest-neighbour.md) | concept | a row at minimal distance from a query under a chosen distance |
| [aggregation](generated/aggregation.md) | concept | combining rows or groups into one number, a mean, a sum, or a rate |
| [session deck](generated/session-deck.md) | reference | the lecture deck of the course the book accompanies, ECE 514, cited by line range from the instructor's session outlines |
| [detector](generated/detector.md) | instrument | a scorer that calls a row an outlier, of four families |
| [chunk](generated/chunk.md) | concept | a piece of a document, the unit a retrieval pipeline encodes and indexes |
| [sampling](generated/sampling.md) | instrument | choosing which rows to read |
| [skewness](generated/skewness.md) | concept | the weighted mean cubed deviation of a column from its mean over the cube of its spread |
| [percentile](generated/percentile.md) | concept | the value below which a given fraction of the rows fall |
| [transaction](generated/transaction.md) | concept | one row of a market-basket table, the set of items bought together |
| [footprint](generated/footprint.md) | concept | the set of entries a reader reads |
| [allocation](generated/allocation.md) | instrument | the assignment of a bit budget across directions |
| [rerank](generated/rerank.md) | instrument | reordering a candidate list with a second scorer |
| [kernel](generated/kernel.md) | concept | the directions a matrix sends to zero |
| [orthogonal](generated/orthogonal.md) | concept | of two vectors, having dot product zero |
| [language model](generated/language-model.md) | concept | a model that reads a sequence of tokens and outputs a probability for the next one |
| [truncation](generated/truncation.md) | instrument | keeping the first k components of a spectrum and dropping the rest |
| [query set](generated/query-set.md) | concept | the rows a retrieval benchmark asks about |
| [fine-tuning](generated/fine-tuning.md) | instrument | continuing to train an encoder on a new objective or corpus, so that its quotient changes |
| [read direction](generated/read-direction.md) | concept | an eigenvector of the read operator with a nonzero eigenvalue, a direction the consumer is sensitive to |
| [paired](generated/paired.md) | instrument | of a comparison, made on the same rows or the same seeds for both arms, so that the difference is scored row by row |
| [outer product](generated/outer-product.md) | concept | the matrix whose entry in row i and column j is the product of the i-th and j-th coordinates of a vector |
| [positive semidefinite](generated/positive-semidefinite.md) | concept | of a symmetric matrix, having every quadratic form nonnegative |
| [nat](generated/nat.md) | concept | the unit of information measured with the natural logarithm, as a bit is measured with the logarithm to base two |
| [surrogate](generated/surrogate.md) | instrument | a quadratic stand-in for the consumer's output metric, the read distortion, used to allocate bits when the output itself cannot be |
| [discretization](generated/discretization.md) | instrument | collapsing an ordered quantity to a few labels by binning it |
| [random forest](generated/random-forest.md) | instrument | an ensemble of decision trees, each fit on a bootstrap sample with a random subset of features at each split, that averages or votes |
| [bagging](generated/bagging.md) | instrument | fitting the same model on bootstrap resamples of the rows and averaging |
| [linear classifier](generated/linear-classifier.md) | instrument | a classifier that scores by a weighted sum, logistic regression or a linear support vector machine |
| [lag](generated/lag.md) | concept | how far a replica trails the primary, in writes or in time |
| [early stopping](generated/early-stopping.md) | instrument | halting a boosting or gradient run when a held-out score stops improving |
| [attribute type](generated/attribute-type.md) | concept | the declaration of which transformations of a column do not change its meaning |
| [residualization](generated/residualization.md) | instrument | removing from a column the least-squares multiple of another |
| [contraction](generated/contraction.md) | instrument | a formula that reduces several axes to one verdict, here ten axes to a toxicity verdict |
| [capacity](generated/capacity.md) | concept | the number of distinctions a model class can draw, the budget's model-side half |
| [Gaussian](generated/gaussian.md) | concept | the normal distribution, in many dimensions the one with density falling with the Mahalanobis distance |
| [sum of squared errors](generated/sum-of-squared-errors.md) | concept | the sum over rows of the squared distance to the row's cluster centre, the validity index k-means minimizes |

The first three entries were filled by hand and are the generator's acceptance test. The
other two hundred and thirty-seven exist only as generated entries, built from the records by `generate.py`.

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
its checkable core, one hundred and forty-three files as of 2026-09-06, and the book's appendix C states what each
check does not cover. On 2026-09-04 the three generated entries carried every number of their hand-filled
counterparts.

## The PDF

`python encyclopedia/build_pdf.py` builds the whole encyclopedia as one document,
`encyclopedia/pdf/Observation-Theory-Encyclopedia.pdf`, with a preface that says how to read an
entry, a table of contents, the entries in alphabetical order with cross-references that carry
page numbers, and back matter listing the entries by kind, by chapter of the book, by Lean file,
and by ledger row, followed by the provenance of the records. It needs pandoc and xelatex and is
rebuilt and committed after every batch.

## Figures and relationships

Every entry carries a schematic drawn by `encyclopedia/figures.py` in the book's figure style,
saved in `encyclopedia/figures/<id>.svg` and placed at the top of the entry. A record joins an
entry by a typed edge, defines, proves, measures, or refutes and corrects, and only records that
name the entry appear in its body. Records cited beside an entry without naming it are listed
under its see-also heading. `SCHEMA.md` states the rules.

## The website

`python encyclopedia/build_site.py C:/source` builds the web-first form into `encyclopedia/site/`.
`index.html` has search, a letter rail, and a tile per entry. Each entry's page opens with a card,
the definition and aliases, the book version and commit, the epistemic and correction status, the
defining equation, the assumptions and scope, the prior art, the evidence links, and the last
semantic review date, followed by the schematic and the full entry. `kinds.html`, `chapters.html`,
`lean.html`, and `ledger.html` are the back matter, the ledger page printing every cited row once in
full, and `provenance.html` names the records' commits. `all.html` is the whole site in one file
with hash routing, for viewing without a server. The site is hosted at https://erisml.org/encyclopedia/ from
the erisml-lib repository's `docs/encyclopedia`, which `publish_site.py` copies the built site into;
commit and push erisml-lib after each rebuild. The PDF is the archival snapshot of the same
records.

## From TSK to the encyclopedia

A student reading Tan, Steinbach, Karpatne, and Kumar meets a term and does not know which entries to read. This table, curated in `tsk_map.toml`, gives the entries in reading order and the chapter of *Data Mining as Observation* that takes the term up.

| TSK term | TSK | Entries to read | Book chapter |
|---|---|---|---|
| attribute types, nominal, ordinal, interval, ratio | 2.1 | [attribute type](generated/attribute-type.md), [standardization](generated/standardization.md), [discretization](generated/discretization.md) | 2 |
| data quality, noise and outliers | 2.2 | [outlier](generated/outlier.md), [detector](generated/detector.md), [skewness](generated/skewness.md) | 2 |
| missing values | 2.2 | [imputation](generated/imputation.md), [leakage](generated/leakage.md) | 2 |
| aggregation and sampling | 2.3 | [aggregation](generated/aggregation.md), [sampling](generated/sampling.md), [Simpson's paradox](generated/simpsons-paradox.md) | 2 |
| dimensionality reduction | 2.3, appendix B | [principal component analysis](generated/principal-component-analysis.md), [truncation](generated/truncation.md), [explained variance](generated/explained-variance.md), [the flip](generated/flip.md) | 4 |
| feature subset selection | 2.3 | [read subspace](generated/read-subspace.md), [nuisance](generated/nuisance.md), [importance](generated/importance.md) | 4 |
| discretization and binarization | 2.3 | [discretization](generated/discretization.md), [quotient](generated/quotient.md) | 2 |
| variable transformation, standardization | 2.3 | [standardization](generated/standardization.md), [whitening](generated/whitening.md) | 2 |
| Euclidean distance, Minkowski distance | 2.4 | [Euclidean distance](generated/euclidean-distance.md), [metric](generated/metric.md), [identity reader](generated/identity-reader.md) | 3 |
| cosine similarity | 2.4 | [cosine](generated/cosine.md), [dot product](generated/dot-product.md), [read direction](generated/read-direction.md), [quotient](generated/quotient.md) | 3 |
| Jaccard coefficient, simple matching | 2.4 | [Jaccard](generated/jaccard.md), [quotient](generated/quotient.md) | 3 |
| correlation | 2.4 | [correlation](generated/correlation.md), [Spearman correlation](generated/spearman-correlation.md), [Kendall correlation](generated/kendall-correlation.md) | 3 |
| Mahalanobis distance | 2.4 | [Mahalanobis distance](generated/mahalanobis-distance.md), [whitening](generated/whitening.md), [covariance matrix](generated/covariance-matrix.md) | 10 |
| decision tree induction | 3.3 | [decision tree](generated/decision-tree.md), [importance](generated/importance.md), [classifier](generated/classifier.md) | 6 |
| model overfitting | 3.4 | [capacity](generated/capacity.md), [harness](generated/harness.md), [early stopping](generated/early-stopping.md) | 6 |
| model selection, validation set | 3.5, 3.6 | [split](generated/split.md), [cross-validation](generated/cross-validation.md), [leakage](generated/leakage.md) | 8 |
| model evaluation, holdout, cross-validation, bootstrap | 3.6 | [cross-validation](generated/cross-validation.md), [bootstrap](generated/bootstrap.md), [Nadeau and Bengio correction](generated/nadeau-and-bengio-correction.md), [seed](generated/seed.md) | 8 |
| confusion matrix, accuracy, precision, recall, F-measure | 3.2, 4.11 | [precision, recall](generated/precision-recall.md), [F1](generated/f1.md), [balanced accuracy](generated/balanced-accuracy.md), [threshold](generated/threshold.md) | 6 |
| ROC curve | 4.11 | [ROC curve](generated/roc-curve.md), [AUROC](generated/auroc.md), [Youden index](generated/youden-index.md), [Monotone Invariance Theorem](generated/monotone-invariance.md) | 5 |
| rule-based classifier | 4.2 | [formula search](generated/formula-search.md), [safe pruning](generated/safe-pruning.md) | 6 |
| nearest neighbor classifier | 4.3 | [nearest neighbour](generated/nearest-neighbour.md), [neighbourhood graph](generated/neighbourhood-graph.md), [hub](generated/hub.md) | 6 |
| naive Bayes classifier | 4.4 | [naive Bayes](generated/naive-bayes.md), [Hessian](generated/hessian.md) | 6 |
| logistic regression | 4.6 | [logistic regression](generated/logistic-regression.md), [linear classifier](generated/linear-classifier.md), [decision boundary](generated/decision-boundary.md) | 6 |
| artificial neural network, deep learning | 4.7, 4.8 | [encoder](generated/encoder.md), [embedding](generated/embedding.md), [attention](generated/attention.md), [language model](generated/language-model.md) | 11 |
| support vector machine, margin | 4.9 | [margin](generated/margin.md), [linear classifier](generated/linear-classifier.md), [decision boundary](generated/decision-boundary.md) | 6 |
| ensemble methods, bagging, boosting, random forest | 4.10 | [ensemble](generated/ensemble.md), [bagging](generated/bagging.md), [boosting](generated/boosting.md), [random forest](generated/random-forest.md) | 7 |
| class imbalance | 4.11 | [balanced accuracy](generated/balanced-accuracy.md), [chance level](generated/chance-level.md), [stratification](generated/stratification.md) | 6 |
| itemset, support, frequent itemset | 5.1, 5.2 | [itemset](generated/itemset.md), [support](generated/support.md), [transaction](generated/transaction.md) | 5 |
| Apriori principle, candidate pruning | 5.2 | [Apriori principle](generated/apriori.md), [anti-monotonicity](generated/anti-monotonicity.md), [safe pruning](generated/safe-pruning.md) | 5 |
| association rule, confidence | 5.3 | [confidence](generated/confidence.md), [lift](generated/lift.md), [cross-support ratio](generated/cross-support-ratio.md) | 5 |
| FP-growth, closed and maximal itemsets | 5.4, 5.5 | [itemset](generated/itemset.md), [anti-monotonicity](generated/anti-monotonicity.md) | 5 |
| objective interestingness measures | 5.6 | [lift](generated/lift.md), [output metric](generated/output-metric.md), [Simpson's paradox](generated/simpsons-paradox.md) | 5 |
| k-means | 7.2 | [k-means](generated/k-means.md), [sum of squared errors](generated/sum-of-squared-errors.md), [identity reader](generated/identity-reader.md) | 9 |
| agglomerative hierarchical clustering, linkage | 7.3 | [hierarchical clustering](generated/hierarchical-clustering.md), [metric](generated/metric.md) | 9 |
| DBSCAN, density-based clustering | 7.4 | [DBSCAN](generated/dbscan.md), [density](generated/density.md), [degree](generated/degree.md) | 9 |
| cluster validity, silhouette, SSE | 7.5 | [validity index](generated/validity-index.md), [silhouette](generated/silhouette.md), [sum of squared errors](generated/sum-of-squared-errors.md), [vacuity threshold](generated/vacuity-threshold.md) | 9 |
| spectral clustering, graph-based clustering | 8.5 | [spectral clustering](generated/spectral-clustering.md), [spectral embedding](generated/spectral-embedding.md), [Laplacian](generated/laplacian.md), [commute time](generated/commute-time.md) | 3 |
| curse of dimensionality | 8.1 | [distance concentration](generated/distance-concentration.md), [intrinsic dimension](generated/intrinsic-dimension.md), [manifold](generated/manifold.md) | 3 |
| statistical anomaly detection | 9.3 | [outlier](generated/outlier.md), [Gaussian](generated/gaussian.md), [Mahalanobis distance](generated/mahalanobis-distance.md) | 10 |
| proximity-based and density-based anomaly detection | 9.4, 9.5 | [detector](generated/detector.md), [density](generated/density.md), [anti-hub](generated/anti-hub.md) | 10 |
| clustering-based and reconstruction-based anomaly detection | 9.6, 9.7 | [detector](generated/detector.md), [reconstruction error](generated/reconstruction-error.md) | 10 |
| evaluation of anomaly detection | 9.10 | [min-over-strata](generated/min-over-strata.md), [abstention](generated/abstention.md), [anti-hub recall](generated/anti-hub-recall.md) | 10 |
| hypothesis testing, p-value, null hypothesis | 10.2 | [p-value](generated/p-value.md), [null model](generated/null-model.md), [control](generated/control.md), [bar](generated/bar.md) | 8 |
| multiple hypothesis testing, Bonferroni, false discovery rate | 10.3 | [multiple comparisons](generated/multiple-comparisons.md), [harness](generated/harness.md) | 8 |
| pitfalls, p-hacking, data dredging | 10.4 | [preregistration](generated/preregistration.md), [sealed](generated/sealed.md), [registered](generated/registered.md), [declaration](generated/declaration.md) | 8 |
| confidence interval, standard error | appendix C, 10.2 | [confidence interval](generated/confidence-interval.md), [standard error](generated/standard-error.md), [paired](generated/paired.md) | 8 |
| eigenvalues and eigenvectors, matrix rank | appendix A | [eigenvalue, eigenvector](generated/eigenvalue-eigenvector.md), [spectrum](generated/spectrum.md), [rank](generated/rank.md), [positive semidefinite](generated/positive-semidefinite.md) | 0 |
| singular value decomposition, PCA | appendix B | [principal component analysis](generated/principal-component-analysis.md), [latent semantic analysis](generated/latent-semantic-analysis.md), [effective rank](generated/effective-rank.md) | 4 |
| covariance matrix, variance | appendix A, C | [covariance matrix](generated/covariance-matrix.md), [variance](generated/variance.md), [trace](generated/trace.md), [anisotropic](generated/anisotropic.md) | 0 |
| gradient, derivative | appendix E | [sensitivity](generated/sensitivity.md), [finite difference](generated/finite-difference.md), [curvature](generated/curvature.md), [Jacobian](generated/jacobian.md) | 0 |
| TF-IDF, document vectors | 2.4, 8.1 | [TF-IDF](generated/tf-idf.md), [bag of words](generated/bag-of-words.md), [latent semantic analysis](generated/latent-semantic-analysis.md) | 12 |
| vector quantization, compression | 7.2, 2.3 | [quantization](generated/quantization.md), [codebook](generated/codebook.md), [product quantization](generated/product-quantization.md), [bit](generated/bit.md), [matched bits](generated/matched-bits.md) | 11 |
| scalability, indexing, nearest-neighbour search | 4.3, 8.4 | [inverted file](generated/inverted-file.md), [recall at k](generated/recall-at-k.md), [shard](generated/shard.md), [rerank](generated/rerank.md), [rank certificate](generated/rank-certificate.md) | 11 |
