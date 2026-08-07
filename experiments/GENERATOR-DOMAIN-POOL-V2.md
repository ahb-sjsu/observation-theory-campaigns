# Domain pool and draw protocol, version 2

**Status:** FROZEN CANDIDATE, awaiting seal. Supersedes
GENERATOR-DOMAIN-POOL.md, sealed 2026-08-07 at commit 5150771 with
blob c3e814a05753fc, which remains in the record unedited.

**Why a version 2 rather than an edit.** The campaign's rule is
that a sealed document may not change and that a correction is a
new registration naming the defect. Two defects were found while
rehearsing the draw machinery, before any beacon value existed.

---

## 1. The defects in version 1

**Ambiguous granularity.** Version 1's stratum N listed
`astro-ph` and `cond-mat excluding stat-mech` alongside leaf
categories such as `physics.optics`. Those two entries name
archives, not categories, and the arXiv taxonomy resolves them
into six and nine leaf categories respectively. A draw could not
have been executed unambiguously from version 1.

**Hand transcription.** Version 1's stratum lists were typed by
hand and were not exhaustive of their archives. Stratum A omitted
q-bio.OT, q-bio.QM, q-fin.EC, q-fin.GN, q-fin.MF, and q-fin.PR
among others. That leaves selection discretion inside a pool whose
entire purpose is to remove it, since the person choosing which
categories to type is the person whose kernel is under test.

**Why correcting now is safe.** The seed for the draw is the NIST
beacon pulse at 2026-08-14T00:00:00Z, which does not yet exist and
which nobody here can produce. No change made before that instant
can be steered toward a wanted draw. That property, and not
anyone's good intentions, is what makes this correction sound.

---

## 2. The pool, now derived rather than transcribed

The pool is built by `python/g1_build_pool.py`, which fetches the
published arXiv taxonomy once, keeps every leaf category whose
archive lies in a declared group, and removes the declared
exclusions. Its output is frozen in `results/g1-domain-pool.json`,
record sha 5101708b206e884f, fetched 2026-08-07T09:26:10Z.

**Archive groups.** Stratum N is astro-ph, cond-mat, nucl-ex,
nucl-th, physics, and nlin. Stratum F is math, cs, and stat.
Stratum A is q-bio, q-fin, econ, and eess.

**Exclusions, unchanged from version 1.** quant-ph,
cond-mat.stat-mech, hep-th, hep-ph, gr-qc, cs.IT, math.IT, cs.CR,
econ.TH, nlin.CG. These are the areas that contributed to the
kernel's construction and the prospective condition requires their
removal.

**Resulting sizes.** Stratum N has 42 categories, stratum F has
75, stratum A has 25, for 142 in total. The lists are frozen in
the committed record and this document does not restate them, so
that the record and the document cannot disagree.

**Aliases.** Cross-listed aliases such as `math.MP` and `cs.SY`
are not deduplicated. A draw of an alias is treated as its
subject. This is recorded rather than corrected because
deduplication would reintroduce a judgment.

---

## 3. The draw, unchanged in substance

**Source.** The NIST Randomness Beacon, version 2.0, the pulse
whose timestamp is 2026-08-14T00:00:00Z, obtained from the
by-time endpoint. Its `outputValue` is the seed material.

**Case is immaterial.** The service returns `outputValue` in
uppercase hexadecimal while version 1 described it as lowercase.
Conversion to an integer in base sixteen is case insensitive, so
the derived seed is identical either way and version 1's phrasing
changes nothing. Recorded so that the discrepancy cannot later be
mistaken for a defect.

**Algorithm.**

1. Convert `outputValue` to an integer in base sixteen.
2. Instantiate Python's `random.Random` with that integer.
3. Take each stratum's list from `results/g1-domain-pool.json`
   and sort it lexicographically.
4. For each stratum in the order N, F, A, call `shuffle` once and
   take the first four entries.

Twelve domains result. There is no redraw for any reason,
including a category being judged unsuitable after the fact. A
category whose published description cannot be retrieved is
recorded as a generator failure of class one rather than replaced.

**Subsets.** After every packet is sealed, the pulse at
2026-08-21T00:00:00Z seeds a second draw by the identical
algorithm over the sorted list of the twelve drawn domains, taking
the first four for full execution and the first six for the
ablation arms.

**Recorded.** The pulse timestamp, its `outputValue`, the derived
integer, the interpreter and library versions, and the resulting
lists go to `results/g1-domain-draw.json`, committed before any
packet is generated. Anyone can repeat the draw from the published
beacon value, the committed pool, and this document.

---

## 4. Standing restriction, unchanged

No member of this campaign may open a new track in any pooled
category before the twelve packets are scored. Every domain
touched informally is a test domain burned. This restriction is in
force from the sealing of version 1 and is lifted when scoring is
complete.

---

## 5. What version 2 does not change

The generator specification GENERATOR-G1.md is untouched, still
sealed at commit 5150771 with blob
99f953d948ce88ba3f1264009bacab0b8ee97e47529739266c793258e27f2761,
and remains the frozen operator under test. This document changes
only how the pool is enumerated and how the draw reads it.
