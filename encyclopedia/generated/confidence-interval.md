# confidence interval

**id.** confidence-interval
**kind.** concept

## definition

A range that would contain the true value in a stated fraction of repeated samples, usually 95 percent. Chapter 0 section 0.9.

## equation

Book equation 8.3.

    \Pr[\text{at least one of } m\text{ null tests passes}]=1-(1-\alpha)^{m},\qquad \alpha_{\mathrm{Bonferroni}}=\frac{\alpha}{m}.

Book equation 8.2.

    \begin{gathered} \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2}, \\ J=1000,\ \frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}=\frac14\ \Rightarrow\ 1+250=251,\ \ \sqrt{251}=15.84. \end{gathered}

## ledger

none

## first stated

Chapter 0 section 0.9 of *Data Mining as Observation*, with the program's intervals in the re-gate table of chapter 14 and the hubness intervals of chapter 11.

## measurements

none

## failures and corrections

none

## conditions

- A range that would contain the true value in a stated fraction of repeated samples. An interval with coverage one minus alpha misses in a fraction alpha, over m independent intervals the expected misses are m alpha and the chance that all cover is one minus alpha to the m, and the chance that at least one misses is at most m alpha.
- Nine intervals at ninety-five percent have a chance near seven percent of two or more misses, which is how the re-gate table's seven of nine inside the interval is read.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ConfidenceInterval.lean`, theorems `missRate_eq`, `some_miss_le`, `nine_intervals`, `nine_expected`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 0, 6, 8, 14.

## related

bootstrap, standard-error, p-value, preregistration

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 01e53bc, observation-theory-campaigns 0c2e3f9, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
