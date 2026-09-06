# p-value

**id.** p-value
**kind.** concept

## definition

The probability of seeing a difference at least as large as the one observed if the true difference were zero. Chapter 0 section 0.9.

## equation

Book equation 8.3.

    \Pr[\text{at least one of } m\text{ null tests passes}]=1-(1-\alpha)^{m},\qquad \alpha_{\mathrm{Bonferroni}}=\frac{\alpha}{m}.

## ledger

none

## first stated

Chapter 0 section 0.9 of *Data Mining as Observation*, with the program's own p-values in the ensemble comparison of chapter 7 and the C-12 record in readscope.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 6 section 6.4 | the uncorrected t stored as sigma, 251 and 15.84, nine wins to three, seven, eight, 3 wins 17 ties 11 losses on 31 datasets, the three-way inconsistency | `constraint-gap\review\FINDINGS.md:1-35`; `constraint-gap\README.md:57-76` |
| chapter 8 section 8.5 | variance inflation 251, SE inflation 15.84, J_eff 3.98, about 62 needed, 3 of 9 at full, 7 at half, 8 at a third | `constraint-gap\review\FINDINGS.md:1-35` |

## failures and corrections

none

## conditions

- Against a finite null sample, the fraction of null draws at least as large as the observation. It lies in the unit interval, never rises as the observation grows, and under the null the fraction of draws with p-value at or below a level is at most that level, which is what makes a threshold on it a false-positive rate.
- A p-value counts one look. Forty looks at five percent pass two by chance, and the book's rule is to count every comparison made and correct for it.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/PValue.lean`, theorems `pvalue_mem_unit`, `pvalue_antitone`, `uniform_bound`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 11.

## related

multiple-comparisons, confidence-interval, harness, preregistration

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
