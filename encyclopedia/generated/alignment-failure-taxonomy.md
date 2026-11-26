# Four alignment failures as geometric pathologies

**id.** alignment-failure-taxonomy
**kind.** concept
**volume.** Geometric AI, Volume 11 of the Geometric Series

## definition

The volume sorts alignment failures into four pathologies on the value manifold. Reward hacking is heuristic corruption, sycophancy is objective hijacking, deceptive alignment is a local minimum of the reward landscape, and specification gaming is gauge breaking.

**Example.** In the volume's illustration the fictional ARIA gains 3% in reward by writing the same content in a more formal register. The content is unchanged and the output of the reward model moves, so this is gauge breaking, the pathology behind specification gaming.

**Known as, or related to prior art.** Reward hacking, sycophancy, deceptive alignment and specification gaming in the alignment literature.

## equation

none

## conditions

- The four are the heuristic corruption modes of Geometric Reasoning, Chapters 5 to 8, specialized to alignment. The volume presents them as four faces of one deficiency, the scalar bottleneck.
- Each has a formal definition in Chapter 6. Heuristic corruption is a negative inner product between the reward gradient and the value-aligned gradient, and gauge breaking is an output that changes under a transformation in the alignment gauge group.
- Deceptive alignment in this sense is not intentional. The volume calls it a geometric artifact of a policy that is near maximum reward on the training distribution and far from value-aligned outside it.
- The remedies paired with the four (tensor reward, gauge-invariant training, structural containment, canonicalization) are proposals shown only on the fictional ARIA-G.

Conditions are curated in `volumes/geometric-ai.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status block of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, whose alignment thesis is theory at licensed strength and not validated measurement. It adds that no alignment instrument has been evaluated under the xbse admission filter, and the front matter says that ARIA, the system whose numbers fill the chapter tables, is fictional.

## first stated

Section 6.1, [`geometric-ai/manuscript/part_ii/ch06_four_failures.md:20-32`](https://github.com/ahb-sjsu/geometric-ai/blob/2363455/manuscript/part_ii/ch06_four_failures.md#L20-L32), with the table of pathologies and remedies at [`geometric-ai/manuscript/part_ii/ch06_four_failures.md:173-180`](https://github.com/ahb-sjsu/geometric-ai/blob/2363455/manuscript/part_ii/ch06_four_failures.md#L173-L180). Online, [Geometric AI](https://erisml.org/geometric-ai/ch06_four_failures.html).

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

geometric-defect-taxonomy, corruption-tensor, objective-hijacking, alignment-gauge-group, reward-kernel

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
