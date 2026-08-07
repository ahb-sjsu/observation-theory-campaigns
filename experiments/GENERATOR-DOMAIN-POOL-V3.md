# Domain pool and draw protocol, version 3

**Status:** FROZEN CANDIDATE, awaiting seal. Supersedes
GENERATOR-DOMAIN-POOL-V2.md, sealed 2026-08-07 at commit 9e16022
with blob 9503db7ed2254a87, which remains in the record unedited,
as does version 1.

The beacon pulse that seeds the draw is dated 2026-08-14T00:00:00Z
and still does not exist, so no correction made now can be steered
toward a wanted draw.

---

## 1. The defect in version 2

Version 2's protocol says that a category whose published
description cannot be retrieved is recorded as a generator failure
of class one rather than replaced. Rehearsing the harness showed
that this measures the wrong thing.

Three categories in the taxonomy carry the literal placeholder
text `Description coming soon` in place of a description, and two
of them, physics.gen-ph and physics.pop-ph, were inside the pool.
The third, quant-ph, was already excluded. Drawing one of those two
would have supplied every arm with no domain description at all,
and the resulting empty packet would have been scored as a failure
of the generator when in fact the experiment's required input did
not exist. The probability of drawing at least one of them was
about 0.18, so this was likely enough to matter.

A missing input is not a generator failure. Categories that cannot
supply the input are removed from the pool.

## 2. The criterion, and one it is not

**Criterion.** A category is removed if its published description
is exactly the placeholder string `Description coming soon`. The
test is an exact match and is applied by the committed builder.

**Rejected criterion, recorded so the choice is visible.** A
minimum description length was considered first and rejected. At
forty characters it would also have removed stat.CO, whose
description is `Algorithms, Simulation, Visualization`, which is
terse but real. Choosing a numeric threshold after seeing which
categories it removes is exactly the discretion this pool exists to
eliminate. stat.CO stays in the pool, and a three-word description
is a hard case for every arm equally, which is acceptable and
arguably desirable.

## 3. The pool

Built by `python/g1_build_pool.py` from the published taxonomy,
frozen in `results/g1-domain-pool.json`, record sha
6447651b58437058. Stratum N has 40 categories, stratum F has 75,
stratum A has 25, for 140 in total. Removed for having no
published description, physics.gen-ph, physics.pop-ph, and
quant-ph, the last already excluded.

**Descriptions are frozen in the record.** The builder now stores
each pooled category's published description verbatim alongside the
pool. The description supplied to every arm on the day is the
frozen one, so the experiment does not depend on the taxonomy page
being reachable or unchanged when the packets are generated. This
also fixes the exact text every arm receives, which version 2 left
to a future fetch.

Archive groups, exclusions, strata, aliases and the case-immaterial
note are unchanged from version 2.

## 4. The draw

Unchanged from version 2 in every respect. The pulse at
2026-08-14T00:00:00Z, its `outputValue` converted to an integer in
base sixteen, `random.Random` seeded with it, each stratum's list
taken from the committed pool and sorted lexicographically, one
`shuffle` per stratum in the order N, F, A, first four taken. No
redraws. Subsets from the pulse at 2026-08-21T00:00:00Z after
packets are sealed.

The implementation is `python/g1_draw.py`, which has been
rehearsed against a past pulse. It refuses to run before the sealed
instant, refuses to overwrite an existing draw record, and produces
byte-identical results across repeated runs on the same pulse.

## 5. Unchanged

The standing restriction on opening new tracks in pooled
categories remains in force until the twelve packets are scored.
GENERATOR-G1.md is untouched and remains the sealed operator under
test.
