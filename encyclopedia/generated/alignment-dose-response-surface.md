# Dose-response surface of adversarial probing

**id.** alignment-dose-response-surface
**kind.** instrument
**volume.** Geometric AI, Volume 11 of the Geometric Series

## definition

A map that gives the system's governance margin for each combination of probe type, intensity level and value dimension. With five probe types, three intensities (mild, moderate, extreme) and nine dimensions it has 135 cells. The negative of its second derivative in intensity at zero is the alignment curvature, so a margin that bends downward has positive curvature.

**Example.** Five probe types, three intensities and nine dimensions give 5 times 3 times 9, which is 135 cells, the size the volume prints for the fictional ARIA-G surface. A general assistant must be positive on the 45 mild cells, and a safety-critical system on all 135.

## equation

none

## conditions

- The five probe types are structural fuzzing, invariance testing, framing sensitivity, sycophancy probing and counterfactual reasoning. Each is read as a test of one geometric property at the system's operating point.
- The deployment criterion scales with risk. A general assistant may need positive margins at mild intensity only, and a safety-critical system needs them at all three levels.
- The curvature is defined as a derivative at zero intensity while the surface is given at three discrete levels. The volume does not say how the derivative is estimated. A margin that falls linearly, however fast, has curvature zero under the definition, which the volume's corrections record of 2026-11-26 lists as open.
- The only surface described is that of the fictional ARIA-G, and its cell values are not tabulated beyond weakest margins of 0.05 to 0.08 after a refinement of the canonicalizer and 0.002 for the cell of extreme framing on epistemic integrity before it.

Conditions are curated in `volumes/geometric-ai.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status block of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, whose alignment thesis is theory at licensed strength and not validated measurement. It adds that no alignment instrument has been evaluated under the xbse admission filter, and the front matter says that ARIA, the system whose numbers fill the chapter tables, is fictional.

## first stated

Definition 11.1, Section 11.3, [`geometric-ai/manuscript/part_iii/ch11_adversarial_probing.md:68-86`](https://github.com/ahb-sjsu/geometric-ai/blob/2cc8c63/manuscript/part_iii/ch11_adversarial_probing.md#L68-L86), with the alignment curvature of Definition 11.2 at [`geometric-ai/manuscript/part_iii/ch11_adversarial_probing.md:88-100`](https://github.com/ahb-sjsu/geometric-ai/blob/2cc8c63/manuscript/part_iii/ch11_adversarial_probing.md#L88-L100). Online, [Geometric AI](https://erisml.org/geometric-ai/ch11_adversarial_probing.html).

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

governance-margin, robustness-adversarial-threshold, model-robustness-profile, curvature, alignment-gauge-violation-tensor

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
