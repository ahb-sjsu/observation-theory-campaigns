# PREREG-XPROTO-QUOTE — market-making stale-quote / adverse-selection cell

**STATUS: UNSEALED.** FAMILY-CONSTRUCTED: 2026-08-23. Earliest compliant
seal **2026-08-24** (`quote_check.py` codes the cooling-off). The **sealed
graded run needs real mid-price tick data** (mode="ticks"); the synthetic
efficient-price random walk (`fam_quote.py --sim`) validates the phenomenon and
the grading but is **not evidence about real markets** — `quote_check.py`
refuses to seal on sim, as the CSI cell refuses its sim and the CCA cell is gated
on SDR hardware. The sealed run is therefore gated on **market-data access**, not
on funding or cooling-off. Graded seeds {20260824, 20260825, 20260826}, disjoint
from the sim validation's {0,1,2}.

**IP posture:** public methodology; the economics instance of the
consumer-relative, witnessed certificate (the finance sibling of turboquant-pro's
`tr(P_C·Σ)` and the CSI/DB/coordination freshness cells). Nothing gated.

## The claim

A market maker's live quote is a **certificate**: it asserts a fair, tradeable
price. Between re-quotes the efficient mid random-walks away. When the true mid
moves beyond the quote by more than the maker's half-spread `s`, the stale side
is **picked off** — an informed fill executes against a mispriced quote and the
maker is adversely selected. This is a **false-clear**: the certificate said
"fair," the realized mid (the **witness**) says otherwise. Graded against the
realized mid, a naive fixed-cadence quote has an adverse-selection rate far above
target, while a **witnessed** policy (re-quote when the observed move exceeds a
fraction of the spread) holds it near target. The rate is **consumer-relative**:
`s` is the book's read operator, so on the SAME price path a tight-spread book is
picked off by moves a wide-spread book tolerates. The refresh floor — the max
quote lifetime holding adverse selection at target — scales as the
**spread-coherence time** `(s/σ)²` (the financial OT-14).

## Family F-QUOTE (constructed + shaken down 2026-08-23)

Efficient-price random walk, step vol σ. Reference book half-spread `s = 3σ`.
Three policies: **naive** (re-quote every 30 steps), **witnessed** (re-quote
when `|mid − quote| > 0.5 s`, the price-triggered correction), **fresh**
(re-quote every step — control). Consumer-relativity measured on the same path
at `s = 2σ` (tight) vs `s = 6σ` (wide).

## Bars (bind at seal; checked against the family record first)

*Demonstrated on the sim, seeds {0,1,2} (validation, not evidence).*

- **B1 — quote vacuity.** Per seed: `naive_fc ≥ 0.25` (stale quote adversely
  selected ≥ 2.5× the 0.10 target).
- **B2 — witness holds.** Per seed: `witnessed_fc ≤ 0.10`.
- **B3 — dominance.** Per seed: `witnessed_fc ≤ naive_fc / 2`.

**Manipulation checks (bars too):**
- **MC1 — aging is real.** `mean_dev_over_spread ≥ 0.5` (the mid drifts a real
  fraction of the spread under the naive cadence).
- **MC2 — a fresh quote is sane.** `fresh_fc ≤ 0.10`.
- **MC3 — non-degenerate + consumer-relative.** `n_steps ≥ 5000`,
  `n_requotes ≥ 1`, and `naive_tight > naive_wide` (the book's spread — its read
  operator — sets the felt adverse selection).

**Verdict rule:** any MC failure → VOID; all MCs + B1–B3 on every graded seed →
PASS; else FAIL, kept as executed. **Kills:** `naive_fc < 0.15`, or
`witnessed_fc > 0.20`.

## Seal procedure

On 2026-08-24 or later, **with real tick data**: place mid-price series at
`econ/ticks/seed_{20260824,25,26}.csv`, confirm `QUOTEREP-family.json`
(mode="sim") PASSes `quote_check.py --check-family`, reread this prereg, flip
STATUS to `SEALED <date>`, commit; run `fam_quote.py --seeds 20260824 20260825
20260826 --out QUOTEREP-graded-raw.json` (mode ticks), `quote_check.py` →
commit `XPROTO-QUOTE-graded.json` as executed.

## Scope

An efficient-price random walk is the canonical microstructure model; it stands
in for real ticks exactly as `fam_csi`'s sim stands in for real 5G. Real venues
add jumps, autocorrelation, latency, and heterogeneous flow — the sealed rung.
Adverse selection is credited microstructure (Glosten-Milgrom lineage); OT's
delta is the *measured, consumer-relative, calibrated* false-clear rate and the
*derivable* spread-coherence refresh floor. This is measurement methodology, not
a trading strategy.

## Provenance

- Exploration: applying OT to geometric-economics (portfolio `tr(P_C·Σ)` +
  the stale-quote freshness sibling of the CSI/DB/ZK cells).
- Family + grading: `fam_quote.py`; graded runner `quote_check.py` (seal-guard +
  coded cooling-off + real-ticks-only sealed grading + pre-seal record check).
