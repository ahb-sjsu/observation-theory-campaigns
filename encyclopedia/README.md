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

The first three entries were filled by hand and are the generator's acceptance test. The
other thirty-five exist only as generated entries, built from the records by `generate.py`.

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
so. On 2026-09-04 the three generated entries carried every number of their hand-filled
counterparts.
