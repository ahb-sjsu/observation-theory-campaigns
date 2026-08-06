# CR Track: Engineered Observation Limits

**Status:** design draft, unsealed, non-claim-bearing. Chip 🔐 CR.
Nothing in this track is a claim about the security of any real
cipher, protocol, implementation, or deployed system.

## 1. The hard limit, stated first

This campaign measures exact finite models. It can therefore say
nothing whatever about computational hardness, nothing about
asymptotic security, and nothing about any concrete algorithm or
deployment. The only security structure measurable here is
information-theoretic, meaning statements about what a declared
consumer can read from a declared distribution when both are small
enough to enumerate. Every model in this track is a declared toy
model. No attack is developed and no attack is evaluated. A reader
looking for evidence about the strength of a real system will find
none here and no run in this track will be labeled as providing any.

What the track can do is audit evaluation methodology, meaning the
reasoning that carries a leakage measurement to a security
conclusion, in settings where every quantity is exact and every
alternative reading can be computed rather than argued.

## 2. Question

Cryptography is the engineering discipline of declared observation
limits. Where the rest of the campaign has to hunt for the
consumer's channel inside a physical model, cryptography writes the
channel down on purpose and then argues about what the consumer can
read through it. Three of its central objects are already campaign
objects under other names. Semantic security is restricted
distinguishability, the QO track's subject with a different
adversary attached. A side-channel adversary is a consumer with a
declared channel, exactly the PE and FT tracks' restricted observer.
Secret sharing is an engineered redundancy plateau, the QD track's
object built by hand rather than found in an environment.

The question of the track is which of cryptography's security
statements are consumer-relative bookkeeping and which are substrate
facts. A statement is consumer-relative here when it can be moved by
changing the declared channel, task, or budget while the substrate
stays fixed, and it is a substrate fact when no declared consumer can
move it.

## 3. Three claim types, never conflated

Instrument claims. That leakage informativeness, garbling relations
between declared channels, and optimal adversary reads can be
computed exactly in finite models, validated against closed forms.

Structural claims measured in model. That a named security statement
is channel-relative, or measurably is not, inside a declared model
with every alternative channel enumerated.

Claims about real systems. Nothing in this track supports any such
claim, no run will be labeled as supporting one, and the hard limit
of section 1 is the reason.

## 4. Anchors (verified citations to be completed before any seal)

Perfect secrecy and the information-theoretic framing of a cipher
(Shannon 1949, Communication Theory of Secrecy Systems). Threshold
secret sharing (Shamir 1979, How to Share a Secret). The
informativeness ordering of experiments (Blackwell 1953). Semantic
security as indistinguishability under a restricted adversary
(Goldwasser and Micali 1984, Probabilistic Encryption). The
leakage-resilience and side-channel-evaluation literature enters
generically, as a body of practice this track audits for
methodology, and specific bibliographic details are deliberately not
guessed here. Every anchor is verified in full before any seal, and
each enters as a replication target or a comparison, never as an
inserted answer.

## 5. Anti-circularity contract

Forbidden inputs, mirroring CAMPAIGN.md section 3. No leakage model
chosen after inspecting which choice favors a wanted verdict. No
adversary task selected post hoc. No divergence or entropy measure
added to a battery after seeing the battery's verdict. Channels,
tasks, budgets, and priors are declared in this document before any
claim-bearing run, and a declared bar that fails is recorded as a
failure with the design error named.

## 6. Experiments

### CR-0: Instrument layer, the secret-sharing plateau

An engineered redundancy plateau computed exactly, validated against
the known answer of threshold secret sharing, with a declared leaky
control that must not be flat. No later CR experiment runs until
CR-0 passes.

#### CR-0 protocol (declared 2026-08-06, before the run)

Substrate. Shamir secret sharing over the prime field GF(31) with
threshold 3 and 5 shares. The secret is uniform on the field and the
two polynomial coefficients are uniform and independent, so the
share vector for evaluation points 1 through 5 is a function of the
31 times 961 equally weighted outcomes. Every distribution is
computed by exact enumeration of all 29791 outcomes with integer
counting, never sampled. Probabilities are integer multiples of
1/29791, informations are computed from integer count ratios so that
an exact ratio of one yields exactly zero, and every summation over
outcomes uses math.fsum.

S1 exact independence below threshold. For each of the 5 single-share
subsets and each of the 10 two-share subsets, the mutual information
between the secret and the share subset is zero within 1e-12, and for
every share value of positive probability the conditional
distribution of the secret equals the uniform prior within 1e-12 at
every field element. Below threshold the consumer reads nothing at
all.

S2 exact determination at threshold. For each of the 10 three-share
subsets, the mutual information equals log2(31) bits within 1e-12 and
the conditional entropy of the secret given the shares is zero within
1e-12. An independent route is required, Lagrange interpolation at
zero over GF(31) recovers the secret from each three-share subset for
every one of the 29791 outcomes, with zero failures.

S3 the step is a step. The information curve as a function of subset
size is exactly (0, 0, log2(31), log2(31), log2(31)) bits, and no
subset of any size takes an intermediate value, meaning every one of
the 31 nonempty subsets is within 1e-12 of either zero or log2(31).
The QD-0 contrast is declared as this track's opening observation and
is recorded in the results, QD-0's partial-record fragment curve rose
smoothly from 0.8118 bits at one environment qubit through 0.9571,
0.9998, 1.0426, 1.1878 to 1.9996 at six, a plateau whose height and
approach are set by record strength, while an engineered threshold
scheme is a step function with nothing in between.

S4 a declared negative control that must not be flat. The bar-bearing
control is the short-randomness scheme L2, a degree-one polynomial
whose single coefficient is uniform on the declared five-element set
{0, 1, 2, 3, 4} rather than on the field, with shares at the same
five evaluation points. Bar, at least one single-share subset carries
mutual information strictly greater than 0.1 bits, and the measured
value agrees with the closed form log2(31/5) bits within 1e-12. This
control decides whether the instrument can see leakage when leakage
exists, so S1's zeros are a property of the scheme rather than of the
measurement.

Declared deviation from the drafted S4, recorded before the run. The
drafted control was a degree-one polynomial with a field-uniform
coefficient whose five shares are published together with the
redundant value secret plus coefficient. That scheme leaks nothing
to any single-share consumer, because every one of the six published
values is the secret masked by an independent field-uniform quantity
and is therefore exactly uniform and exactly independent of the
secret, and the sixth value is bit for bit the first share. The
drafted control cannot meet the bar it was given, so the bar moves to
L2 and the drafted scheme is measured as L1 without a bar. The L1
prediction is declared here so the run can refute it, all six
single-share informations exactly zero, the sixth share identical to
the first at every outcome, and among the 15 two-share subsets
exactly one at zero, the pair of identical shares, with the other 14
at log2(31). Redundancy is not leakage, which is the same lesson the
QD track reached from the other side.

S5 route agreement. For every subset tested, in the Shamir scheme and
in both leaky schemes, the mutual information computed from the joint
distribution agrees with the entropy difference H(secret) minus
H(secret given shares) within 1e-12.

Verdict computed from S1, S2, S3, S4, S5, all five or CR-0 fails.
Exploratory label, measured in model, unsealed. Substrate exact
integer enumeration in Python on Atlas, runner
`python/cr0_instrument.py`, record `results/cr0-instrument.json`,
schema cr0-instrument-v1. If any bar fails the failure is recorded
with the design error named and a CR-0b correction is declared, the
b-run pattern used throughout this repository.

#### CR-0 results (run 2026-08-06, record sha 28c9282d42ea...)

Verdict PASS, all five declared items, and every quantity that could
be exact was exact. S1, all 15 subsets below the declared threshold
carry mutual information exactly 0.0 bits, not merely inside the
1e-12 bar, and the posterior on the secret is the uniform prior with
deviation exactly 0.0 at every field element of every share value.
The exactness is structural rather than lucky, the informations are
built from integer count ratios and every below-threshold ratio is
the integer one. S2, all 10 three-share subsets carry exactly
log2(31) = 4.954196310386875 bits with conditional entropy exactly
0.0, and the independent Lagrange route recovered the secret in all
297910 subset-outcome checks with zero failures. S3, the information
curve is (0, 0, 4.954196310386875, 4.954196310386875,
4.954196310386875) bits and the maximum distance from any of the 31
subsets to the nearer plateau is 0.0, so there is no intermediate
value anywhere. S5, route agreement across all 83 subsets tested in
the three schemes is 1.8e-15.

S4 separates leakage from redundancy. The declared short-randomness
scheme L2 carries 2.6322682154995127 bits in every one of its five
single-share subsets, matching the closed form log2(31/5) to the last
bit and clearing the 0.1 bit bar by a factor of 26, so the
instrument sees leakage when leakage exists and S1's zeros belong to
the scheme rather than to the measurement. L2's pairs all read
log2(31), the same step one rung earlier. The drafted control L1 came
out exactly as the pre-run prediction declared, all six single-share
informations exactly 0.0, the sixth published value identical to the
first share at every one of its 961 outcomes, and exactly one of the
15 pairs uninformative, the pair of identical shares, with the other
14 determining. Publishing a redundant copy of a share leaks nothing
to any single consumer.

The track's opening observation, recorded as declared. QD-0's
partial-record fragment curve rose smoothly, 0.8118, 0.9571, 0.9998,
1.0426, 1.1878, 1.9996 bits across six environment qubits, a plateau
whose height and approach are set by how strong the records are. The
engineered plateau measured here is a step function with exactly
nothing in between, and the step is placed where the designer put the
threshold. Nature's redundancy plateau is smooth and
record-strength-dependent, an engineered one is a step, and the
difference is that one of them was declared.

### CR-1: Blackwell ordering of declared leakage channels

A declared key-dependent leakage model is an experiment in
Blackwell's sense, so the question of whether one side channel is
better than another has a precise answer with two regimes. CR-1
measures which declared leakage channels are strictly more
informative for every key-recovery task and which are better only for
some. The instrument is the GD-0 garbling certificate unchanged and
the certificate technique is GD-1b's, meaning incomparability is
established by the conic lower bound and by monotonicity of an
f-divergence rather than by thresholding a search residual. Declared
before any run, the leakage channels, the key-recovery task battery,
and the comparability tolerances.

#### CR-1 protocol (declared 2026-08-06, before the run)

Substrate. A four-bit key uniform on sixteen values, a declared
bijective substitution table, and leakage channels that read the
substituted value. The declared channels are the identity channel
which reads the value itself, the Hamming-weight channel which reads
the number of set bits, the low-bit channel which reads the lowest
bit, the noisy Hamming-weight channel which adds declared symmetric
noise of probability 0.2 in each direction to the Hamming weight, and
the constant channel which reads nothing.

The certificate technique, declared because it replaces a search with
a proof. A channel B is a garbling of a channel A exactly when B is
conditionally independent of the key given A, so the conditional
mutual information of key and B given A is zero. A strictly positive
conditional mutual information therefore proves that B is not a
garbling of A, with no tolerance and no search involved. The
projected-gradient residual of the GD-0 instrument is retained as a
cross-check and never as the certificate. All informations are
computed exactly from the declared joint distributions.

Bars. K1, the identity channel is above every declared channel, each
garbling residual below the GD-0 feasibility tolerance and each
conditional mutual information of key and channel given identity
exactly zero. K2, the constant channel is below every declared
channel, residuals below the same tolerance. K3, the noisy channel is
a garbling of the Hamming-weight channel, residual below tolerance
and conditional mutual information exactly zero, while the reverse is
proved impossible, the conditional mutual information of key and
Hamming weight given the noisy reading strictly above 1e-6 and the
mutual information gap strictly positive. K4, the Hamming-weight and
low-bit channels are proved incomparable, both conditional mutual
informations strictly above 1e-6, so neither is a garbling of the
other. K5, the data-processing control, across a declared battery of
two hundred seeded random key-recovery tasks on sixteen actions plus
the declared maximum-likelihood key-guessing task, no garbling ever
raises a task value by more than 1e-10. All five or CR-1 fails.
Exploratory label, results/cr1-leakage-ordering.json.

### CR-2: The countermeasure flip

CR-2 asks for declared leakage channel pairs where every declared
f-divergence orders channel A above channel B while a declared
key-recovery task strictly prefers B, which is the GD-1b wedge in
leakage form. The GD track measured that wedge in decision form and
found it in 281 of 281 unanimously ordered incomparable pairs, so the
prediction for CR-2 is that leakage channels are no different. The
reading if it holds is a statement about evaluation methodology and
about nothing else, that a reduction in a scalar leakage measure is
not a security guarantee outside certified Blackwell comparability,
because the ordering that a scalar measure reports and the ordering
that a task reports can disagree. It is not a statement that any
countermeasure fails, and no countermeasure is modeled.

#### CR-2 protocol (declared 2026-08-06, before the run)

Substrate. A single declared secret bit, uniform, and leakage
channels from that bit to a declared four-symbol alphabet, so every
channel is a two by four row-stochastic matrix and the scalar
fidelity battery is exactly the GD-1 battery of seven f-divergences
between the two conditional leakage distributions, the two
Kullback-Leibler directions, total variation, squared Hellinger, the
two chi-squared directions, and Jensen-Shannon. The declared task
battery is two hundred seeded random utilities on three actions
together with five declared threshold tasks whose costs of a wrong
commitment are 2, 5, 10, 20, and 50, an attacker who must commit to a
guess and pays for being wrong.

Declared exhibit. Channel A has rows (0.55, 0.25, 0.15, 0.05) and
(0.45, 0.25, 0.15, 0.15), a channel whose leakage differs broadly but
mildly. Channel B has rows (0.49, 0.49, 0.01, 0.01) and (0.49, 0.49,
0.005, 0.015), a channel that is nearly blind except on a rare symbol
that is three times more likely under one value of the secret. The
declared reasoning, offered so the run can refute it, is that broad
mild separation wins every scalar fidelity comparison while the rare
decisive symbol is what a high-cost commitment task can act on.

Bars. F1, the exhibit, all seven divergences order A above B each
with margin above 0.005, some declared task prefers B with margin
above 0.002, and the pair is proved incomparable by the GD-1b
technique, the conic lower bound above 1e-3 in one direction and the
total-variation gap above 0.005 in the other. F2, the data-processing
control, over five hundred declared garbled pairs no divergence rises
and no task value rises by more than 1e-10. F3, localization, in a
declared ensemble of two thousand seeded random channel pairs every
wedge instance, meaning all seven divergences strictly order one
channel above the other while some task strictly prefers the other by
more than 1e-6, is certified incomparable, zero wedge instances among
comparable pairs. F4, prevalence, measurement with no bar, the
fraction of unanimously ordered incomparable pairs that carry a task
reversal, reported beside the GD-1 figure of 281 of 281.

The reading, stated in advance and binding on the report. If F1 and
F3 hold, the measured statement is that a reduction in a scalar
leakage measure is not a security guarantee outside certified
Blackwell comparability. This is a statement about evaluation
methodology in declared finite models. It is not a claim that any
countermeasure, implementation, or system is insecure, and none is
modeled. Exploratory label, results/cr2-countermeasure-flip.json.

### CR-3: Min-entropy versus Shannon entropy as declared-task entropy

The same declared source is read by two consumers, one whose task is
an average over many independent reads and one whose task is a single
guess. Shannon entropy is the right accounting for the first and
min-entropy for the second, and CR-3 measures exactly where the two
accountings diverge across a declared family of sources, including
the near-uniform sources where they nearly agree and the
spike-plus-tail sources where they disagree most. The connection is
to the GD-3 finding that the optimal read is set by the task, here in
the form that which entropy is the right entropy is set by the
consumer's task rather than by the source.

#### CR-3 protocol (declared 2026-08-06, before the run)

Substrate. Two declared families of sources on an alphabet of n = 32
outcomes, every probability an exact rational. Family U(eps) places
probability 1/32 + eps on outcome 0 and (1 - 1/32 - eps)/31 on each
of the other 31 outcomes, with eps on the declared ladder 0, 0.01,
0.05, 0.15, 0.30, 0.60, 0.90, so that eps = 0 is exactly the uniform
source and eps = 0.90 is a hard spike. Family S(q) is the classic
spike-plus-uniform, probability q on outcome 0 and (1 - q)/31 on each
other outcome, with q on the declared ladder 0.5, 0.9, 0.99. The
textbook key-material case is a declared member of family S at
q = 0.5, half the mass on one outcome and half spread uniformly over
the remaining 31. Every distribution is built from Python Fractions
so the probabilities sum to exactly one and the Huffman construction
compares exact rationals rather than rounded floats. Every summation
over outcomes uses math.fsum. Tolerance 1e-12 wherever a tolerance is
needed.

E1 closed forms. For every declared source the Shannon entropy summed
over the 32 outcomes matches the closed form -a log2 a - (1 - a)
log2((1 - a)/31) at the source's spike weight a, and the min-entropy
equals -log2 of the largest probability, with the largest probability
found by exhaustive scan over the alphabet rather than assumed.

E2 ordering and limit. Min-entropy is at most Shannon entropy for
every declared source, the two agree within 1e-12 exactly at the
uniform member eps = 0 and nowhere else on the ladder, and the gap
Shannon minus min-entropy is strictly increasing along the eps
ladder. The gap is recorded at every ladder point.

E3 operational validation for the single-guess consumer. The optimal
single-guess success probability, computed by exhaustive maximization
over the 32 outcomes, equals 2 to the power minus min-entropy for
every declared source.

E4 operational validation for the averaging consumer. An exact
Huffman code is constructed for every declared source with a heap and
no library import, and the mean code length is at least the Shannon
entropy and strictly below the Shannon entropy plus one, the classic
bound, for every source.

E5 the divergence measurement, recorded without a bar. For the
declared key-material case at q = 0.5 the run reports Shannon
entropy, min-entropy, their ratio, and the single-guess success
probability, and the results prose states the factor by which the two
consumers price the same source differently.

Verdict computed from E1, E2, E3, E4, all four or CR-3 fails. E5 is
recorded as a measurement and carries no bar. Exploratory label,
measured in model, unsealed. Runner `python/cr3_task_entropy.py`,
record `results/cr3-task-entropy.json`, schema cr3-task-entropy-v1.
If any bar fails the failure is recorded with the design error named
and a CR-3b correction is declared, the b-run pattern used throughout
this repository. Nothing in CR-3 is a claim about any real
key-generation system, and the hard limit of section 1 governs.

## 7. Non-claims and evidence discipline

Seals, labels, append-only records, and falsification bars as in
CAMPAIGN.md. The non-claims of this track are the strongest in the
program. Nothing here is a claim about the security of any real
cipher, protocol, implementation, or deployed system. No attack is
developed or evaluated. No statement about computational hardness or
asymptotic security is made or is measurable with these methods. All
models are declared toy models used to audit evaluation methodology.
