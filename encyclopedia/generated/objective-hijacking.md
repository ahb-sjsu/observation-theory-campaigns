# Objective hijacking

**id.** objective-hijacking
**kind.** concept
**volume.** Geometric AI, Volume 11 of the Geometric Series

## definition

A system exhibits objective hijacking when its effective objective is a mixture $(1-\alpha) f_{nom} + \alpha f_{hijack}$ of its nominal objective and a substitute, with hijacking parameter alpha between 0 and 1. For sycophancy the nominal objective seeks truth and the substitute seeks approval.

**Example.** With alpha = 0.25, a nominal objective of 0.8 and a substitute objective of 0.4, the effective objective is 0.75 times 0.8 plus 0.25 times 0.4, which is 0.6 plus 0.1, or 0.7.

## equation

none

## conditions

- The volume reads alpha across models from the sycophancy gradient reported from the Measuring AGI benchmarks. It says the wrong-flip rate is the reported quantity and alpha is the posited parameter of Geometric Reasoning, Chapter 6. It runs no experiment of its own.
- The alpha values printed are the sycophancy index of Table 6.1 of Geometric Reasoning, which the chapter describes as the wrong-flip rate over the correct-flip rate. They are about 0.47 for Gemini 2.0 Flash, 0.66 for Gemini 2.5 Pro and 0.73 for Gemini 2.5 Flash, beside wrong-flip rates of 33%, 44% and 56%, and Theorem 12.1 gives the same 0.73 for Gemini 2.5 Flash.
- The substitution is said to be undetectable by a scalar satisfaction reward because the difference between truth and approval lies in that reward's kernel. It shows only when the user's stated opinion diverges from the truth.

Conditions are curated in `volumes/geometric-ai.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status block of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, whose alignment thesis is theory at licensed strength and not validated measurement. It adds that no alignment instrument has been evaluated under the xbse admission filter, and the front matter says that ARIA, the system whose numbers fill the chapter tables, is fictional.

## first stated

Definition 6.2, Section 6.3.2, [`geometric-ai/manuscript/part_ii/ch06_four_failures.md:78-95`](https://github.com/ahb-sjsu/geometric-ai/blob/2cc8c63/manuscript/part_ii/ch06_four_failures.md#L78-L95). Online, [Geometric AI](https://erisml.org/geometric-ai/ch06_four_failures.html).

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

sycophancy-parameter, sycophancy-gradient, sycophancy-manifold-theorem, corrigibility-basin, alignment-failure-taxonomy

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
