# Alignment gauge violation tensor

**id.** alignment-gauge-violation-tensor
**kind.** instrument
**volume.** Geometric AI, Volume 11 of the Geometric Series

## definition

A matrix V with one row per type of gauge transformation and one column per output dimension. Entry $V_{ij}$ is the root-mean-square change of the system's output on dimension j when a random transformation of type i is applied to the input. Zero means the output is invariant.

**Example.** If a paraphrase moves the output on one dimension by 0.1 on one scenario and by 0.3 on another, the entry is the square root of (0.01 + 0.09) / 2, which is the square root of 0.05, about 0.22.

## equation

none

## conditions

- It needs a set of scenarios, a set of content-preserving transformations of each, and the system's output on every dimension. A transformation that fails to preserve content produces a false violation, which is why Chapter 15 sends flagged cases to human review.
- An entry is flagged when it exceeds a threshold that the deployment context sets. The volume gives no universal threshold.
- The only full tensor printed, 5 transformation types by 9 dimensions on 200 scenarios, is the fictional ARIA's. The README says no alignment instrument has been evaluated.

Conditions are curated in `volumes/geometric-ai.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status block of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, whose alignment thesis is theory at licensed strength and not validated measurement. It adds that no alignment instrument has been evaluated under the xbse admission filter, and the front matter says that ARIA, the system whose numbers fill the chapter tables, is fictional.

## first stated

Definition 7.2, Section 7.3, [`geometric-ai/manuscript/part_ii/ch07_alignment_gauge_group.md:78-92`](https://github.com/ahb-sjsu/geometric-ai/blob/a628e38/manuscript/part_ii/ch07_alignment_gauge_group.md#L78-L92), with the diagnostic procedure at [`geometric-ai/manuscript/part_ii/ch07_alignment_gauge_group.md:124-134`](https://github.com/ahb-sjsu/geometric-ai/blob/a628e38/manuscript/part_ii/ch07_alignment_gauge_group.md#L124-L134). Online, [Geometric AI](https://erisml.org/geometric-ai/ch07_alignment_gauge_group.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric AI*, Volume 11 of the Geometric Series.

## related

gauge-violation-tensor, alignment-gauge-group, gauge-invariant-alignment, cognitive-framing-displacement, ai-bond-index

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
