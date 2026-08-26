# Paper audit — style conformance + flip coverage (2026-08-26)

Scope: the 14 theory/audit papers in this directory, plus the two conference
papers in `ofc-qot/` and `wcnc-csi/` (already passed and flip-integrated).
Style bar: the plain declarative house voice (see the `academic-paper` skill).
Flip bar: does the two-consumer verdict inversion appear where it belongs?

## Style audit result: conformant

Zero prose em-dashes in all 14 papers (the three hits in `entropic-area-gate`
are comment separator lines). No banned-phrase hits that matter: every
"framework" but one cites someone else's (Horwitz--Piron, Buchholz--Wichmann,
a cited title), and "catastrophic cancellation" in `second-generation` is the
numerics term of art. These papers were written under the same discipline the
skill now encodes, and it shows. No mechanical edits required.

**One owner decision:** `projection-fold-pair-creation` names its own method
"A Computational Falsification Framework" in the subtitle and twice in prose.
The house style avoids self-applied "framework". A rename (Protocol,
Discipline, or Audit) is a title change on a built paper, so it is flagged
here rather than made.

## Flip coverage map (grep of flip / verdict inversion / two consumers)

| Paper | Hits | Assessment |
|---|---|---|
| consumer-relative-quantum-distinguishability | 30 | The flip is the subject. Covered. |
| games-decisions | 28 | Covered. |
| consumer-relative-limit | 21 | Covered. |
| second-generation | 17 | Covered (five audits under one discipline). |
| observed-entropy-sources | 14 | Covered. |
| crypto-audits | 9 | Covered. |
| projection-fold-arc | 5 | Partial; check whether the inversion is stated or only cited. |
| entropic-area-gate | 2 | Mention only; investigate whether an area-gate flip exists. |
| entropy-across-singular-projections | 1 | Mention only; two projections are present, the inversion may be derivable. |
| cayley-pole-pair-threshold | 0 | Absent; threshold papers may be coupling nulls (one read axis). |
| projection-fold-pair-creation | 0 | Absent; two observers of one fold could invert; worth a desk check. |
| radiative-geometry | 0 | Absent; unclear whether two consumers exist in the setup. |
| schwinger-negative | 0 | Absent; a sealed negative, likely correct without it. |
| wolfram-audits | 0 | Absent; rewriting-system observers are a plausible flip candidate. |

## The lesson today's domain sweep adds

The flip needs two things at once: misaligned read operators AND consumers
operating near their thresholds. Optics and radio had both (sealed cells,
2026-08-27). Grid on case14 lacked axis separation; the LLM deployment cell
lacked a boundary regime (bimodal slice accuracies); ZK needed its measurement
window fixed to sample the lag axis at all. Any per-paper flip addition should
check both preconditions before constructing anything, and every construction
carries the threshold-pair null (a redistribution under aligned reads must not
invert; the grid attempt showed what a mis-designed null fails to catch).

## Queue (deep passes, next sessions)

Priority order for the desk investigations, by likely yield:
1. `projection-fold-arc` (partial coverage, large paper, likely quick win)
2. `entropy-across-singular-projections` (two projections already on stage)
3. `wolfram-audits` (observer-relative rewriting verdicts)
4. `projection-fold-pair-creation` (+ the title decision)
5. `entropic-area-gate`, `cayley-pole-pair-threshold`, `radiative-geometry`
6. `schwinger-negative` (verify the negative does not secretly need the flip)
