# Domain pool and draw protocol for the G1 experiment

**Status:** FROZEN CANDIDATE, awaiting seal. Sealed separately from
GENERATOR-G1.md so that the pool and the draw cannot be adjusted to
suit the kernel, and so that the kernel cannot be adjusted to suit
the draw.

---

## 1. Why the pool is external

The pool is taken from the arXiv subject taxonomy, which is public,
maintained by people outside this campaign, and organized without
reference to it. Each drawn category's own published description is
the domain description supplied verbatim to every arm. Nobody here
writes the description, so no target phenomenon can be smuggled
into it.

---

## 2. Exclusions, declared before the draw

The prospective condition requires excluding every area that
contributed to the kernel's construction. The following are removed
from the pool. Excluding them is required by the experiment and is
recorded here so the exclusion cannot be revised after the draw.

- quant-ph, for the quantum observation and quantum Darwinism work.
- cond-mat.stat-mech, for entropy, fluctuation relations, and
  lattice gas work.
- hep-th and hep-ph, for the pair-creation and gauge work.
- gr-qc, for the entropic geometry work.
- cs.IT and math.IT, for the information and Blackwell work.
- cs.CR, for the cryptography work.
- econ.TH, for the games and decisions work.
- nlin.CG, for the cellular automaton and rewriting work.

---

## 3. Strata

Three strata, defined by archive rather than by judgment, with four
domains drawn from each for twelve in total.

**Stratum N, near.** Physics archives other than the excluded ones.
astro-ph, cond-mat excluding stat-mech, nucl-th, nucl-ex,
physics.acc-ph, physics.ao-ph, physics.app-ph, physics.atm-clus,
physics.atom-ph, physics.bio-ph, physics.chem-ph, physics.class-ph,
physics.comp-ph, physics.flu-dyn, physics.geo-ph, physics.ins-det,
physics.med-ph, physics.optics, physics.plasm-ph, physics.soc-ph,
physics.space-ph, nlin.AO, nlin.CD, nlin.PS, nlin.SI.

**Stratum F, far.** Mathematics, computer science, and statistics
archives other than the excluded ones. math.AG, math.AT, math.CO,
math.CT, math.DG, math.LO, math.NT, math.RT, cs.AR, cs.CC, cs.DB,
cs.DS, cs.GR, cs.LO, cs.NA, cs.PL, cs.SE, stat.AP, stat.ME.

**Stratum A, adversarial.** Archives whose native language is
furthest from a substrate and consumer split. q-bio.BM, q-bio.CB,
q-bio.GN, q-bio.MN, q-bio.NC, q-bio.PE, q-bio.SC, q-bio.TO,
q-fin.CP, q-fin.PM, q-fin.RM, q-fin.ST, q-fin.TR, econ.EM,
econ.GN, eess.AS, eess.IV, eess.SP, eess.SY.

---

## 4. The draw

The seed does not exist yet and cannot be produced by anyone here.

**Source.** The NIST Randomness Beacon, the pulse whose declared
timestamp is 2026-08-14T00:00:00Z. Its 512-bit outputValue, as a
lowercase hexadecimal string without a leading marker, is the seed
material.

**Algorithm, fixed now and verifiable by anyone.**

1. Take the outputValue string and convert it to an integer in
   base sixteen.
2. Instantiate Python's `random.Random` with that integer.
3. Sort each stratum's list above lexicographically.
4. For each stratum in the order N, F, A, call `shuffle` once on
   its sorted list and take the first four entries.

The twelve results are the drawn domains and there is no redraw for
any reason, including a category being judged unsuitable. A
category with no usable published description is recorded as a
generator failure of class one rather than replaced.

**Execution and ablation subsets.** After every packet is sealed, a
second draw uses the pulse at 2026-08-21T00:00:00Z by the identical
algorithm applied to the sorted list of the twelve drawn domains,
taking the first four for full execution and the first six for the
ablation arms.

---

## 5. What is recorded

The pulse timestamp, its outputValue, the derived integer, the
library version used for the draw, and the resulting lists are
written to `results/g1-domain-draw.json` and committed before any
packet is generated. Anyone can repeat the draw from the published
beacon value and this document.

---

## 6. Standing restriction while the pool is live

No member of this campaign may open a new track in any pooled
category before the experiment concludes. Every domain touched
informally is a test domain burned, and the cryptography track
consumed one in a single day. This restriction takes effect at
sealing and is lifted when the twelve packets are scored.
