# Hohfeldian Klein four-group (V4)

**id.** hohfeldian-klein-four-group
**kind.** result
**volume.** Geometric Ethics, Volume 2 of the Geometric Series

## definition

The four Hohfeldian positions Obligation, Claim, Liberty and No-claim carry two operations, the correlative s (O with C, L with N) and the jural flip n (O with L, C with N). They are commuting involutions and generate the Klein four-group $V_4 = \{e, n, s, sn\}$, which acts regularly on the four positions.

**Example.** With the volume's two-bit code O = 00, L = 10, C = 01, N = 11, n = 10 and s = 01, operations act by XOR. From O, s then n gives 00, 01, 11, which is N. From O, n then s gives 00, 10, 11, which is N again, so the order does not matter.

**Known as, or related to prior art.** Hohfeld's jural relations (correlatives and opposites), with the Klein four-group of elementary group theory.

## equation

none

## conditions

- The theorem is about the permutation group of four labels under the two stated operations. That moral positions are these four, with these two operations, is a modeling choice (Axioms A1 and A2).
- No operation in the group cycles the four positions. The quarter-turn O to C to N to L to O lies outside it, and the earlier dihedral claim is withdrawn.
- The group is abelian, so the result of a sequence of operations depends only on how many times s and n occur modulo 2. Order effects in judgment cannot come from this group.
- The measured correlative rates are below 100 percent (O with C at 87 percent, L with N at 82 percent in the volume's corpus). The group is the structure, not a description of how people always reason.

Conditions are curated in `volumes/geometric-ethics.toml` rather than read from a record.

## ledger

none. *standing.* Tagged Proved in the text and Proved (Lean) in Appendix F, machine-checked in Lean 4 with Mathlib. Ledger rows GE-PROP-8-3-V4 and GE-THM-12-2-V4 have class proved. The full gauge group V4 times U(1)_H is Posit 12.3, a modeling choice (GE-POSIT-12-3, exploratory).

## first stated

Proposition 8.3, Section 8.4, [`geometric-ethics/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html:567-578`](https://github.com/ahb-sjsu/geometric-ethics/blob/cf2325e/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html#L567-L578), and Theorem 12.2, [`geometric-ethics/chapter-12-noether-s-theorem-for-ethics-symmetry-invariance-.html:308-319`](https://github.com/ahb-sjsu/geometric-ethics/blob/cf2325e/chapter-12-noether-s-theorem-for-ethics-symmetry-invariance-.html#L308-L319). Online, [Geometric Ethics](https://erisml.org/book/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Ethics*, Volume 2 of the Geometric Series.

## related

hohfeldian-dihedral-withdrawal, semantic-gate, moral-bond-invariance-principle, bond-index, moral-holonomy

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
