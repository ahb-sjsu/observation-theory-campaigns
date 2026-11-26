# Legal friction

**id.** legal-friction
**kind.** concept
**volume.** Geometric Law, Volume 5 of the Geometric Series

## definition

The legal friction of a path of cases is the sum of its edge weights plus, for each evidentiary requirement $j$, a weight $\omega_j$ times the shortfall of the path's evidence below that requirement's threshold. A strong argument is a low-friction path, and the burden of proof is the least friction from the starting case to the goal region.

**Example.** A path of two edges with weights 2 and 3, plus one evidentiary requirement of weight 4 whose evidence falls 0.25 short of its threshold, has friction 2 + 3 + 4 x 0.25 = 6.

## equation

none

## conditions

- The path must follow directed edges of the judicial complex. An edge of infinite weight makes the argument impossible.
- Standards of proof are stated as thresholds on this quantity. Preponderance asks the plaintiff's best path to be shorter than the defendant's, clear and convincing asks it to be shorter by a factor below 1, and beyond reasonable doubt asks it to be below a small bound.
- The chapter's body formula writes the boundary penalties as a separate term and says they are counted once. Its appendix gives the equivalent compact form with the penalties inside the edge weights, which is the form given here.
- The friction values in the volume's worked examples are illustrative units. No friction computed from real cases is reported.

Conditions are curated in `volumes/geometric-law.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic status of 2026-07-14 calls the volume a posited framework with one instrumented corner. That corner is the legal text embedding LeBSE, validated in the xbse admission filter on US case law with labels from the CourtListener citation graph, and the README says this covers structure preservation in legal text embeddings and not the book's broader jurisprudential claims, which remain posited theory at licensed strength.

## first stated

Chapter 4, [`geometric-law/chapters/ch04_legal_metric.md:161-173`](https://github.com/ahb-sjsu/geometric-law/blob/1e50dfc/chapters/ch04_legal_metric.md#L161-L173), the appendix form at [`geometric-law/chapters/ch04_legal_metric.md:418-422`](https://github.com/ahb-sjsu/geometric-law/blob/1e50dfc/chapters/ch04_legal_metric.md#L418-L422), and the burden of proof at [`geometric-law/chapters/ch04_legal_metric.md:212-220`](https://github.com/ahb-sjsu/geometric-law/blob/1e50dfc/chapters/ch04_legal_metric.md#L212-L220). Online, [Geometric Law](https://erisml.org/geometric-law/ch04_legal_metric.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Law*, Volume 5 of the Geometric Series.

## related

legal-edge-weight, doctrinal-heuristic, judicial-complex, threshold

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
