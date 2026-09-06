# replica

**id.** replica
**kind.** concept

## definition

A copy of a database kept on another machine. Its lag is how far it trails the primary. Chapter 13.

## equation

Book equation 0.26.

    \mathrm{FC}=\Pr\big[W\ \text{refutes}\ \big|\ \mathcal C_t\ \text{clears}\big],\qquad \text{coverage}=\Pr\big[\mathcal C_t\ \text{clears}\big].

Book equation 13.1.

    \mathrm{FC}=\Pr\big[W\ \text{refutes}\ \big|\ \mathcal C_t\ \text{clears}\big],\qquad d_O(\Delta)=\operatorname{tr}\big(P_C\,M_{\mathrm{drift}}(\Delta)\big),\qquad M_{\mathrm{drift}}(\Delta)=\mathbb E\big[\delta_\Delta\delta_\Delta^{\top}\big].

## ledger

- OT-11. Feedback-free staleness: streaming-retrieval damage tracks measured drift; derived-cadence re-allocation removes it. `[void]`. `geometric-observation/claims/LEDGER.md:48` at 7d91883.

## first stated

Chapter 13 section 13.3 of *Data Mining as Observation*, with the program's substrate measurements in `observation-theory-campaigns/analysis/mongo/PREREG-XPROTO-MG.md` and the database rows of the freshness track.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 13 section 13.3 | BGP 0.351, IS-IS 0.184, OSPF 0.083, second collector | `observation-theory-campaigns\analysis\mongo\PREREG-XPROTO-MG.md:42`; `observation-theory-campaigns\experiments\ROUTING-TELEMETRY-TRACK.md:130-150`; `geometric-observation\BOOK-OUTLINE.md:75` |

## failures and corrections

none

## conditions

- A copy of a database kept on another machine, trailing the primary by a lag. The keys stale under a lag grow with the lag and vanish at no lag. A naive certificate that clears every read has coverage one and a false-clear rate equal to the stale fraction, and a witness-backed certificate that clears only keys outside the lag has a false-clear rate of zero at the price of coverage.
- Which reads are stale is consumer-relative, since two readers of the same replica have different coherence times, and the measured false-clear rates on ZooKeeper, Postgres, and MongoDB are the ledger's numbers.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Replica.lean`, theorems `stale_mono`, `stale_zero`, `naive_certificate`, `witnessed_certificate`, `witnessed_coverage`, at observation-data-mining 1c6cd64.

## used in

*Data Mining as Observation* chapters 0, 1, 4, 13.

## related

freshness, certificate, witness, false-clear-rate, coverage

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 09cc919, theory-radar 37c4e6c, observation-data-mining 1c6cd64, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
