# FT Track: Fluctuation Theorems Under Restricted Observation

**Status:** design draft, unsealed, non-claim-bearing. Chip 🔴 FT.
Everything is measured in declared exact finite models.

## 1. Question

The Jarzynski equality and the Crooks relation are exact identities
for an observer who sees the full trajectory. The track question is
what happens to them for a consumer with a restricted channel. Do
apparent violations appear, are they predicted exactly by the
declared detector model, the lawful-demon audit, and is the free
energy that appears in the identities itself consumer-relative,
Paper V's consumer-relative Landauer bound extended to fluctuation
identities.

## 2. Anchors (verified citations to be completed before any seal)

Jarzynski 1997, Crooks 1999, and the Sagawa-Ueda feedback
generalization. Each enters as a replication target or a
comparison, never as an inserted answer.

## 3. Anti-circularity contract

Work definitions, protocols, and observer channels are declared
before claim-bearing runs. No apparent violation is reported
without its declared detector-model prediction alongside.

## 4. Experiments

### FT-0: Exact path-space instrument layer

Three states, declared energy protocol interpolating linearly from
(0, 0.5, 1.0) to (1.0, 0.2, 0.0) over eight steps at unit inverse
temperature, quench-then-relax updates with Metropolis kernels in
detailed balance with the current energies, equilibrium start. The
full path space (3^9 paths) is enumerated exactly. Protocol
declared 2026-08-05, before the run.

C1 Jarzynski, the path-space average of exp(-W) equals exp(-dF)
within 1e-12. C2 Crooks per path, for every one of the 3^9 paths,
the forward path probability times exp(-W) equals the reverse
protocol's probability of the reversed path times exp(-dF), maximum
deviation 1e-12, the identity holds path by path, not only on
average. C3 second law and quasistatic control, the mean work
exceeds dF by a measured positive margin, and the frozen protocol
gives mean work exactly zero equal to its dF. C4 restricted
observer preview, a declared lumped observer merging the two lowest
states, with the declared lumped free energies, has a measured
Jarzynski defect recorded as the FT-1 seed, measurement with no
bar. C1 through C3 or FT-0 fails. Exploratory label,
results/ft0-instrument.json.

#### FT-0 results (run 2026-08-05, record sha 0c83a3dc7109...)

Verdict PASS, all three barred items. Jarzynski holds on the
ensemble with deviation exactly zero, and Crooks holds path by path
across all 19683 paths with maximum deviation 2.2e-19, the identity
is exact at the finest grain the model has. Mean work -0.0788
against dF -0.1021, dissipation 0.0233, and the frozen protocol
gives exactly zero work on every path. The lumped-observer preview
measured a Jarzynski defect of 4.33e-4 at equal lumped and true
free energies, the restricted consumer's identity fails by a
definite measured amount, the FT-1 seed on record.

### FT-1: The lawful-demon audit

Declared blind observers (lumped states, missed transitions,
finite-resolution work meters). Bars, the complete observer shows
zero defect, and every restricted observer's defect is predicted
exactly by its declared detector model, the PF-6 clause on
fluctuation identities.

#### FT-1 protocol (declared 2026-08-05, before the run)

The FT-0 system unchanged. Four declared observers. The complete
observer sees the full path. The lumped observer merges states zero
and one and computes apparent work from the declared lumped free
energies of its observed symbol. The held observer reads the state
only at even stages and computes apparent work holding its last
reading. The blind observer sees nothing and books the equilibrium
free-energy change as its work. Each observer's Jarzynski defect is
the absolute difference between the path average of exp(-apparent
work) and exp(-dF).

Bars. L1, the complete observer's defect is at most 1e-14. L2, the
blind observer's defect is at most 1e-14, its apparent work
telescopes to dF exactly, total blindness satisfies the identity
trivially. L3, the lumped observer's defect is at least 1e-5,
strictly broken in between. L4, lawfulness by route agreement, for
the lumped and held observers the defect computed by full path
enumeration equals the defect computed independently from the
observed-record process, the exact hidden-Markov marginal over
records, within 1e-12, the declared detector model predicts the
defect exactly. Mean apparent work per observer recorded. All four
or FT-1 fails. The reading, the defect lives strictly between full
sight and total blindness, and it is never an anomaly, always the
declared channel's exact arithmetic. Exploratory label,
results/ft1-lawful-demon.json.

### FT-2: Consumer-relative free energy

Whether a lumped consumer's fluctuation identities are exactly
restored by replacing dF with a declared consumer-relative free
energy, connecting to Paper V. Either outcome is a result.

### FT-3: Feedback and measurement

The Sagawa-Ueda generalization replicated exactly in a declared
finite model, then the campaign question, whether the mutual
information term is the consumer's information or any observer's.

## 5. Evidence discipline and non-claims

Seals, labels, append-only records, and falsification bars as in
CAMPAIGN.md. Substrate, exact finite models in Python on Atlas.
Nothing in this track is a claim about laboratory thermodynamics.
