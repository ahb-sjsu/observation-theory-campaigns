# FT Track: Fluctuation Theorems Under Restricted Observation

**Status:** design draft, unsealed, non-claim-bearing. Chip 🌡️ FT.
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

#### FT-2 protocol (declared 2026-08-06, before the run)

The FT-0 system and the FT-1 observers unchanged. The declared
restoration, a budgeted consumer replaces its naive apparent work
with the Bayes work estimate, minus the log of the conditional
expectation of exp(-W) given its record, computed by exact
filtering through its declared detector model. The tower property
of conditional expectation makes the restored Jarzynski identity
exact whenever the filter uses the true model, so the bar tests
the machinery and the lawfulness clause together.

Bars. E1, the naive defects replicate FT-1, lumped at least 1e-5
and held at least 1e-3. E2, restoration, with the true detector
model the restored identity holds within 1e-12 for both the lumped
and the held observer. E3, no restoration by a wrong model, the
same filter built from kernels at inverse temperature 0.9 leaves
the lumped observer's restored defect at least 1e-6, magnitude
recorded. The reading, the fluctuation identity for a budgeted
consumer is an inference theorem, restored exactly by lawful
inference through the true declared channel and by nothing less.
Exploratory label, results/ft2-restoration.json.

### FT-3: Feedback and measurement

The Sagawa-Ueda generalization replicated exactly in a declared
finite model, then the campaign question, whether the mutual
information term is the consumer's information or any observer's.

#### FT-3 protocol (declared 2026-08-06, before the run)

The FT-0 system with declared measurement and feedback. After the
fourth relax step the controller measures the state through a
declared symmetric noisy channel with error rate 0.2, split evenly
between the two wrong outcomes, and if the outcome is the third
state it switches the remaining protocol stages to the declared
alternate energies, the FT-0 linear path retargeted to final
energies (0.2, 1.0, 0.3), otherwise the original protocol
continues. The free-energy change is branch-final, computed from
whichever final energies the feedback selected. The pointwise
information is the log ratio of the outcome likelihood to the
outcome's marginal probability at the measurement time.

Bars. T1, the Sagawa-Ueda identity, the path-and-outcome average
of exp(-(W - dF) - I) equals one within 1e-12. T2, feedback beats
the bare identity, the average of exp(-(W - dF)) without the
information term differs from one by at least 1e-3, the measured
efficacy recorded. T3, the information is the consumer's, refeeding
the identity with the pointwise information of a declared bystander
who sees the same measurement through additional noise, total
error rate 0.4, leaves a defect of at least 1e-4, while the
controller's own information restores it within 1e-12, the
identity knows which observer acts. T4, measurement with no bar,
the information-corrected second law margin, mean work minus dF
plus mean information, nonnegative and recorded. All of T1 through
T3 or FT-3 fails. Exploratory label, results/ft3-feedback.json.

#### FT-3 results (run 2026-08-06, record sha b07b5aadff64...)

Verdict PASS, all three barred items. The Sagawa-Ueda identity
holds to 5.6e-15 with the controller's pointwise information. The
bare identity fails by 7.3e-3, efficacy 0.9927, the feedback
demon's measured advantage. The bystander's information, the same
measurement seen through additional noise, leaves a defect of
5.3e-3 while the controller's restores exactness, the identity
knows which observer acts. The information-corrected second law
holds with margin 0.489 nats. With FT-1 and FT-2 the arc is
complete, fluctuation identities for restricted and feedback
observers are inference theorems about declared channels, and the
information that appears in them is the acting consumer's, not
anyone's.

## 5. Evidence discipline and non-claims

Seals, labels, append-only records, and falsification bars as in
CAMPAIGN.md. Substrate, exact finite models in Python on Atlas.
Nothing in this track is a claim about laboratory thermodynamics.
