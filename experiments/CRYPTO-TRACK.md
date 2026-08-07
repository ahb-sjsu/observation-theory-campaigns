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

#### CR-1 results (run 2026-08-06, record sha b3ee26a9f818...)

Verdict PASS, all five items, and the proof certificate behaved as
declared. The identity channel carries 4 bits about the key, the
Hamming-weight channel 2.0306, the low-bit channel exactly 1, the
noisy Hamming-weight channel 0.8867, and the constant channel
exactly 0. The identity channel is above every declared channel,
each search residual below the feasibility tolerance and each
conditional mutual information given the identity exactly zero to
5e-17. Adding declared noise is a garbling, residual 2.2e-16 and
conditional information 4.8e-17, while the reverse is proved
impossible without any tolerance argument, the conditional
information of key and Hamming weight given the noisy reading is
1.1439 bits and the mutual information gap is the same 1.1439 bits.

The incomparable pair is the useful one. The Hamming-weight channel
and the low-bit channel each carry information the other does not,
1.8113 bits of the Hamming weight survive knowing the low bit and
0.7806 bits of the low bit survive knowing the Hamming weight, so
neither is a garbling of the other and no scalar comparison can
order them for every task. The Hamming-weight channel carries twice
the mutual information of the low-bit channel and is still not
above it in Blackwell's sense. The data-processing control holds
across the declared battery of 201 key-recovery tasks with worst
task gain 5.6e-17.

The certificate technique is the transferable part. A garbling
leaves nothing conditionally, so a strictly positive conditional
mutual information is a proof of non-garbling with no tolerance and
no search, which is what GD-1's residual threshold should have been
and what GD-1b had to repair after the fact.

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

#### CR-2 results (run 2026-08-06, record sha 4f1dcd811d62...)

Verdict PASS, all three barred items, and the prevalence
measurement reproduces the GD-1 figure in leakage form. The
declared exhibit stands, all seven divergences order channel A
above channel B with minimum margin 0.0149, a declared commitment
task prefers B by 0.00212, and the pair is proved incomparable, the
conic lower bound 0.00175 in one direction and the total-variation
gap 0.095 in the other. The data-processing control holds, across
five hundred declared garbles no divergence rose and no task value
rose by more than 3.3e-16.

The ensemble is the result. Of two thousand seeded random channel
pairs, 867 are certified comparable, 856 incomparable, and 277
ambiguous. Among the incomparable pairs, 268 are ordered
unanimously by all seven declared divergences, and every one of
those 268 carries a task reversal in the declared battery, maximum
margin 0.0796 and median 0.0183. No comparable pair carries a
wedge, which is Blackwell's theorem holding as it must. GD-1
measured 281 of 281 in decision form and CR-2 measures 268 of 268
in leakage form.

Correction to the CR-2 results prose, recorded 2026-08-06 during the
proofread of the paper. The paragraph above and the drafted exhibit
reasoning both attributed the task that prefers B to a commitment
task. That attribution is wrong. Recomputing the declared battery
from the committed runner and the declared seed, the task that
prefers B by 0.0021156 is one of the two hundred random three-action
utilities, and no commitment task prefers B. Four of the five
commitment tasks value both channels at zero, because with a cost of
5 or more for a wrong guess neither channel ever makes a commitment
worth taking, and the fifth, at cost 2, prefers A by 0.025. The
declared bar F1 asked only that some declared task prefer B by more
than 0.002, so the bar and the verdict are unaffected and the record
is unchanged. What is refuted is the second half of the drafted
reasoning, that the rare decisive symbol is what a high-cost
commitment task can act on. The commitment tasks carry an abstain
action, so a reader who is never confident enough to commit simply
declines, and neither channel reaches the confidence a high cost
demands. The paper states only what the record holds, that a declared
task prefers B by 0.00212.

The reading, as declared in advance. A reduction in a scalar
leakage measure is not a security guarantee outside certified
Blackwell comparability, because the ordering a scalar measure
reports and the ordering a task reports disagree in every
unanimously ordered incomparable pair measured here. This is a
statement about evaluation methodology in declared finite models.
It is not a claim that any countermeasure, implementation, or
system is insecure, and none was modeled. The constructive half of
the statement matters as much, the CR-1 certificate decides
comparability by proof, so an evaluation that establishes
comparability can rely on its scalar ordering.

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

#### CR-3 results (run 2026-08-06, record sha 865a0373a295...)

Verdict FAIL, on E2 alone, and the failure is in one clause of the
declaration rather than in the substrate. E1, E3, and E4 passed
sharply. E1, the summed Shannon entropy agrees with the closed form
to 8.9e-16 at every one of the ten declared sources, the min-entropy
computed from the exact numerator and denominator of the largest
probability agrees with the direct route to 8.9e-16, and the
exhaustive scan over the alphabet found the declared spike weight as
the largest probability at every source rather than being told where
to look. E3, the single-guess success probability found by exhaustive
maximization equals two to the power minus min-entropy with worst
deviation 1.4e-17, and eight of the ten sources are bit for bit
identical. E4, every Huffman code satisfies the Kraft equality
exactly, the smallest lower margin is exactly 0.0 at the uniform
member where the mean length is exactly 5 bits and the entropy is
exactly 5 bits, and the smallest upper margin is 0.0807 bits at
q = 0.99 where the mean length 1.0497 sits below the entropy plus one
of 1.1303.

E2 failed on its monotonicity clause and passed everything else. The
ordering held with the worst value of min-entropy minus Shannon
entropy exactly 0.0 across all ten sources, and the two entropies
agree to exactly 0.0 at the uniform member and are separated by more
than the tolerance at every other ladder point. The measured gap
along the declared eps ladder is 0.0, 0.3983679711748964,
1.3367478843916603, 2.2751050863811666, 2.635309539404596,
2.1128507492677056, 0.599082908339557 bits, so the first four
increments are positive and the last two are negative.

The design error, named. The declaration extended a fact about the
near-uniform end of the ladder to the whole ladder without checking
the other limit. Both entropies go to zero together as the spike
takes all the mass, since a source with almost all its weight on one
outcome is almost certain under either accounting, so the additive
gap has to turn around and its maximum is interior. The declared
ladder crossed that maximum between eps = 0.30 and eps = 0.60. The
additive gap was the wrong quantity to ask for monotonicity from, and
the run says so.

E5, recorded as declared and carrying no bar. For the textbook
key-material case, half the mass on one outcome and half spread
uniformly over the remaining 31, the averaging consumer's accounting
is 3.477098155193437 bits and the single-guess consumer's accounting
is exactly 1 bit, a ratio of 0.2875961377467552 and a factor of
3.477098155193437 between the two prices. The single-guess success
probability is exactly 0.5 and the Huffman mean length is
3.4838709677419355 bits. The same declared source is worth about
three and a half bits to one consumer and one bit to the other, and
neither number is wrong. Which entropy is the right entropy is set by
the consumer's task rather than by the source, which is the GD-3
lesson in entropy accounting form. Nothing in this is a claim about
any real key-generation system.

#### CR-3b protocol (declared 2026-08-06, before the CR-3b run)

The correction replaces the refuted monotonicity clause with the
monotone statement the substrate actually supports, and adds the
location of the interior maximum as a measurement. Everything else is
unchanged, the same two families, the same ladders, the same exact
rational arithmetic, the same tolerance of 1e-12.

F1 the unchanged items. E1, E3, and E4 are re-run without any change
to their bars and must pass again.

F2 ordering and limit, corrected. The ordering clause and the
equality clause are kept unchanged, min-entropy is at most Shannon
entropy at every declared source and the two agree within 1e-12
exactly at the uniform member and nowhere else. The monotonicity
clause becomes a statement about the ratio rather than the
difference, the ratio of min-entropy to Shannon entropy is strictly
decreasing along the full eps ladder and strictly decreasing along
the full q ladder. The additive gap is declared unimodal on the eps
ladder instead of increasing, meaning the closed-form derivative of
the gap with respect to the spike weight changes sign exactly once
across the ladder, the sign change is bracketed strictly between
eps = 0.30 and eps = 0.60, and the gap increments are positive at
every ladder step before the bracket and negative at every ladder
step after it.

F3 the derivative route. The closed-form derivative of the gap with
respect to the spike weight a is log2((1 - a)/(31a)) + 1/(a ln 2),
and it must agree with a central finite difference of the measured
gap to within 1e-6 at every ladder point, so the unimodality claim
rests on a derivative that has been checked against the quantity it
differentiates.

F4 the interior maximum, located and recorded without a bar. The
stationary point is found by bisection on the closed-form derivative
inside the declared bracket to a width below 1e-12, and the
maximizing spike weight and the maximum gap are recorded.

Verdict computed from F1, F2, F3, all three or CR-3b fails. F4 and
E5 are recorded as measurements and carry no bar. Exploratory label,
measured in model, unsealed. Runner `python/cr3b_task_entropy.py`,
record `results/cr3b-task-entropy.json`, schema
cr3b-task-entropy-v1. Nothing in CR-3b is a claim about any real
key-generation system, and the hard limit of section 1 governs.

#### CR-3b results (run 2026-08-06, record sha c8e0db539cb6...)

Verdict PASS, all three declared items. F1, the unchanged items
repeated their CR-3 values exactly, closed-form agreement 8.9e-16,
min-entropy route agreement 8.9e-16, the exhaustive scan finding the
declared spike weight at every source, single-guess identity to
1.4e-17 with eight of ten sources bit for bit identical, Kraft
equality exact everywhere, and Huffman margins 0.0 below and 0.0807
above.

F2 passed on the corrected statement. The ordering held with worst
value exactly 0.0 and the equality clause held exactly at the uniform
member. The ratio of min-entropy to Shannon entropy falls strictly
along the whole eps ladder, 1.0, 0.9202918130749266,
0.7303985098755919, 0.5199240276284444, 0.376894797099704,
0.23904214295745602, 0.14641401304235882, and strictly along the
whole q ladder, 0.2875961377467552, 0.15761166929284676,
0.11124838824221533. The closed-form derivative of the additive gap
reads 46.166, 34.559, 16.301, 5.181, 0.4147, -3.444, -7.165 along the
eps ladder, one sign change and it falls exactly in the declared
bracket between eps = 0.30 and eps = 0.60, with the gap increments
positive at every step before the bracket and negative at every step
after it.

F3, the closed-form derivative agrees with a central finite
difference of the gap to 1.6e-8 at every ladder point, against the
declared 1e-6, so the unimodality claim rests on a derivative checked
against the quantity it differentiates.

F4, recorded without a bar. Bisection inside the declared bracket
converged in 39 steps to a final width of 5.5e-13 and places the
maximizing spike weight at 0.353383436367676, an eps of
0.322133436367676, where the gap reaches 2.6398252258132944 bits and
the derivative reads 4.5e-12. The largest gap on the declared ladder
was 2.635309539404596 bits at eps = 0.30, so the ladder came within
0.0045 bits of the true maximum and stepped over it.

The reading, adjacent to the numbers. The fraction of the averaging
consumer's accounting that survives to the single-guess consumer
falls strictly and without exception as the source concentrates,
from all of it at the uniform source to 0.111 at q = 0.99, while the
number of bits separating the two accountings rises to an interior
maximum near eps = 0.32 and then falls back toward zero, because a
source that is almost certain is cheap under either accounting. For
the declared key-material case the averaging consumer prices the
source at 3.477098155193437 bits and the single-guess consumer
prices the same source at exactly 1 bit, a factor of
3.477098155193437, and the single guess succeeds with probability
exactly 0.5 while a Huffman code for the same source averages
3.4838709677419355 bits per symbol. Both numbers are correct
readings of one substrate and the disagreement is entirely in the
task. Which entropy is the right entropy is set by the consumer's
task rather than by the source, which is the GD-3 lesson in entropy
accounting form. Nothing in this is a claim about any real
key-generation system.

### CR-4: The backdoor audit ceiling

#### CR-4 protocol (declared 2026-08-07, before the run)

A backdoor of the Dual-EC shape is a consumer-relative asymmetry,
two observers read the same output stream and one holds a scalar
that turns an apparently random stream into a decodable channel.
CR-1's certificate is the right instrument for that asymmetry, and
CR-4 asks the prior question, whether an information-theoretic
audit can tell a parameter set whose scalar is known from one whose
scalar is merely unknown.

Substrate. The curve y squared equals x cubed plus two x plus three
over the field of 101 elements, all points enumerated, a generator
of the full group, and a generator step of the Dual-EC shape where
the state advances by one point multiplication and the output word
is the truncation of the abscissa of a second multiplication. The
declared truncation keeps three bits. Two declared parameter sets,
one whose second point is the seventh multiple of the generator so
the scalar is known by construction, and one whose second point is
fixed by a declared nothing-up-my-sleeve rule with its scalar
recovered afterwards by enumeration only so the run can state it.

Bars. B1, the trapdoor works, an observer holding the declared
scalar predicts the next output word from one observed word in at
least half of the declared seeds. B2, the public word distributions
of both parameter sets are near uniform, each within 0.15 bits of
the truncation's uniform entropy. B3, the scalar always exists, the
enumerated scalar of the clean point reproduces that point. B4, the
public observer's mutual information with the seed does not exceed
the seed entropy, an instrument sanity check.

Finding B5, the ceiling measurement, recorded individually with
either outcome a result. The audit cannot separate the two
parameter sets when their public entropies agree within 0.15 bits
and their word-count multisets are identical.

The declared prediction, offered so the run can refute it. The
scalar relating two points of a cyclic group always exists, so the
two parameter sets induce the same output distributions and no
information-theoretic audit separates them. If that prediction
holds, the security content of this backdoor class is entirely
computational, the campaign's methods stop exactly there, and the
boundary is drawn in measured numbers rather than asserted.

Scope, stronger here than anywhere else in the program. The curve
is a toy chosen for exact enumeration. No real curve, standard,
protocol, implementation, or deployed system is modeled or
evaluated. No attack is developed. Nothing measured here is a
claim about the security of anything, and the trapdoor arm exists
only to establish that the audit sees a backdoor when one is
present by construction. Exploratory label,
results/cr4-backdoor-ceiling.json.

#### CR-4 results (run 2026-08-07, record sha in the record)

Verdict FAIL on two bars, and the analysis of the failure sharpened
the question. The group had ninety-six elements while the declared
truncation has eight output values, so ninety-five seeds spread
over eight bins cannot approach uniform and the measured public
entropies, 2.7890 and 2.8002 bits against three, missed the
declared 0.15-bit window by finite size alone. The trapdoor arm
predicted at 0.263 against a declared 0.5 because the recovery loop
accepted the first candidate consistent with one observed word
instead of testing candidates against the next word.

The finding B5 read False, and it was the wrong question. Two
different second points induce genuinely different exact output
distributions, so asking whether the backdoored and clean parameter
sets are distributionally identical was never the ceiling. The
scalar of the clean point was recovered by enumeration in the same
run, which shows why. Every point has a scalar, so the two
parameter sets are not two classes at all.

#### CR-4b protocol (declared 2026-08-07, before the run)

The corrected question. A trapdoor scalar is a constant of the
parameter set and not a source of randomness, so it cannot change
any conditional law of the outputs. Its whole content is the cost
of a computation. An audit built from informations must therefore
be exactly blind to it, and the measurement is that blindness
placed beside a positive control the same audit does detect.

Substrate. The first declared curve over the field of 1009 elements
with prime group order, a base point taken by the declared
first-abscissa rule, and the generator step of CR-4 unchanged with
three output bits. The clean second point is fixed by a declared
nothing-up-my-sleeve rule, the first scalar whose point abscissa is
at least 500, with the scalar recovered by enumeration only so the
run can state it.

Bars. B1, the positive control, a declared generator that writes
one seed bit into its output word carries at least 0.5 bits of
mutual information with that seed bit while the unmodified
generator carries at most 0.05. B2, both parameter sets are near
uniform within 0.05 bits of the truncation's uniform entropy, which
the larger group makes attainable. B3, the trapdoor confers no
information, the conditional entropy of the second word given the
first computed by the public route and by the trapdoor holder's
inverse-map route agree within 1e-9. B4, the clean point's scalar
is recovered by enumeration, so both parameter sets sit in one
class.

Findings, recorded individually with either outcome a result. B5,
the audit is blind to the trapdoor. B6, the same audit sees the
declared leak and not the trapdoor, the two measurements together.

The reading if they hold. This campaign's machinery detects
backdoors that are leakage and is exactly blind to backdoors that
are trapdoors, because the first changes a distribution and the
second changes only the cost of a computation. The boundary is
where computational assumptions must take over, and it is drawn in
measured numbers. Scope as in CR-4, unchanged and strict.
Exploratory label, results/cr4b-backdoor-ceiling.json.

#### CR-4b results (run 2026-08-07, record sha in the record)

Verdict FAIL on B3, from a code error, with the other three bars
passing and the positive control exact. The larger group delivered
near uniformity as designed, public entropies 2.9878 and 2.9943
bits against three, and the clean point's scalar was recovered by
enumeration. The declared leak carried exactly 1.0 bits of mutual
information with the seed bit while the unmodified generator
carried exactly 0.0, so the audit sees an information-theoretic
backdoor immediately and the positive control is sharp.

B3 compared two routes to one conditional entropy and measured
2.8811 against 2.9125, a difference of 0.0314 where the bar was
1e-9. The named error is in the inverse map, the trapdoor route
multiplied the observed point's abscissa as though it were a scalar
instead of scalar-multiplying the observed point by the inverse of
the trapdoor scalar. The two routes are equal by the group law, so
the disagreement measured the bug and nothing about trapdoors.

#### CR-4c protocol (declared 2026-08-07, before the run)

Two corrections, the second of which is the better statement of the
ceiling.

The inverse map is corrected, the trapdoor route now multiplies the
observed point by the inverse scalar as the group law requires, and
the route agreement becomes B3b with the same 1e-9 bar. This checks
the arithmetic and claims nothing more.

The ceiling itself becomes B3a and it is exact rather than
empirical. A trapdoor scalar is a fixed constant of the parameter
set, so its entropy is exactly zero, and the information any
constant can carry about any observable is bounded by its own
entropy. The audit's blindness is therefore not a limitation of
this instrument or this toy, it is a bound.

The findings stand unchanged in meaning and sharper in form. B5,
the audit is blind to the trapdoor, recorded as an exact zero bound
rather than an agreement within tolerance. B6, the same audit sees
the declared one-bit leak and is blind to the trapdoor.

The reading. Backdoors that change a distribution are visible to
this machinery and backdoors that change only the cost of a
computation are invisible to it by a bound rather than by an
oversight. Scope unchanged and strict. Exploratory label,
results/cr4c-backdoor-ceiling.json.

### CR-5: Rigidity as designer freedom

#### CR-5 protocol (declared 2026-08-07, before the run)

CR-4c measured that an audit built from informations is blind to a
trapdoor by an exact bound. What such an audit can see is
provenance, and provenance is a counting question. A designer who
may re-roll a derivation until the result lands in a rare weak
class needs only enough freedom to cover that class's rarity, and
the artifact records nothing about how many rolls were taken.

Substrate. All non-singular curves over the field of 101 elements,
group orders computed exactly by counting points. The declared weak
class is a group order smooth to the bound five, which is a
weakness because a smooth order splits the discrete logarithm into
small pieces. Two declared procedures share one declared seed map,
the first coefficient is the seed squared plus seventeen and the
second is the seed cubed plus twenty-three, both modulo the field,
with singular pairs rejected. The rigid procedure may use exactly
one declared seed. The flexible procedure may use any seed in a
declared range of 4096.

Bars. P1, the weak-class density is measured exactly over the whole
space and lies strictly between zero and one. P2, both reachable
sets are counted, the rigid one at least one curve and the flexible
one more than one. P3, the manipulation threshold and its
demonstration, the flexible procedure's distinct reachable count
times the measured density is at least one, and the search actually
finds a weak curve inside its declared range.

Measurements with no bar, recorded either way. P4, the artifact
carries no search count, recorded as the number of weak-producing
seeds in the range and the expected number of rolls a manipulating
designer would need, beside the observation that a seed reached on
the first roll and one reached on the thousandth are the same kind
of object. P5, whether the rigid procedure sits below the
threshold. P6, whether the rigid procedure landed in the weak class
by chance anyway, which would say the parameter space is unsafe
rather than the designer dishonest.

The connection recorded with the result. Removing the designer's
freedom to re-roll is what rigid parameter generation does in
cryptography and what preregistration does in this campaign,
including in the four vacuity failures this program has recorded
against itself. They are one idea in two fields, and this
experiment measures the quantity that both of them bound.

Scope unchanged and strict. Exploratory label,
results/cr5-rigidity.json.

### CR-6: Information against disturbance

#### CR-6 protocol (declared 2026-08-07, before the run)

Why this belongs in this arc. CR-4c measured that an audit built
from informations is blind to security that lives in computational
hardness and sighted for security that lives in distributions.
Quantum key distribution is the second kind by construction, so it
is exactly where this campaign's instruments have no ceiling, and
leaving it out would stop the arc one step before the part it can
speak about most directly.

The contrast with every classical track. PE, HD, and FT all found
that a restricted consumer's blindness costs the consumer and
leaves the substrate untouched, most sharply in HD-3 where the
decayed mode was recovered bit for bit and the substrate forgot
nothing. A consumer reading a non-orthogonal ensemble cannot do
that, and this run measures the price exactly.

Substrate. Four declared preparations, the two computational and
the two conjugate states, chosen uniformly. The declared
eavesdropping consumer intercepts with probability lambda,
measures in the computational basis, and resends its outcome, on
the declared ladder 0, 0.1, 0.25, 0.5, 0.75, 1. Everything is
enumerated exactly over the finite probability space.

Bars. C1, the classical control, an orthogonal ensemble is read
perfectly and leaves no trace, the consumer's information exactly
one bit and the induced error exactly zero. C2, no information
without disturbance, at every positive lambda both the information
and the error are strictly positive. C3, the closed forms, the
measured information equals lambda over two and the measured error
equals lambda over four, each within 1e-12. C4, at lambda zero both
are exactly zero. C5, the Holevo quantity of the preparation
ensemble bounds the consumer's information.

Finding C6, recorded either way, the family fixes the exchange rate
at exactly two bits of information per unit of induced error.
Exploratory label, results/cr6-information-disturbance.json.

### CR-7: Monogamy as consumer exclusion

#### CR-7 protocol (declared 2026-08-07, before the run)

This experiment closes a loop the QD track opened. QD measured
redundancy, many environment fragments carrying the same record,
with the plateau appearing exactly when the declared interaction
wrote records for them, and QD-3 measured two disjoint consumers
agreeing at a rate set by record strength. CR-7 measures the
boundary of that plateau, the information for which redundancy is
not merely absent but forbidden.

Substrate. A declared classical control, one bit broadcast to both
consumers, and a declared three-qubit family carrying one
excitation shared between the two consumers at a fixed weight
split, parametrised by an angle on a declared seven-point grid.
Correlations are measured by the Wootters concurrence of the exact
reduced states and by the tangle of one party against the rest.

Bars. M1, classical polygamy, the broadcast record gives each
consumer the whole bit, both mutual informations exactly one. M2,
the exact tradeoff, the sum of the squared concurrences is exactly
one across the whole grid, so the inequality that usually bounds
monogamy is saturated on this family and the tradeoff is an
identity. M3, exclusion at the extremes, one consumer holding the
correlation entirely leaves the other with exactly none. M4, the
Coffman-Kundu-Wootters relation is saturated, the tangle of the
first party against the rest equals that sum.

Finding M5, recorded either way, the classical informations sum
past the quantum identity, so the same three parties can share a
classical record in full and cannot share quantum correlation at
all.

The reading if the bars hold. Redundancy is what makes a fact
objective, and it is available exactly for information that has
already become classical. The QD track found the plateau and this
run finds its boundary. Exploratory label,
results/cr7-monogamy.json.

## 7. Non-claims and evidence discipline

Seals, labels, append-only records, and falsification bars as in
CAMPAIGN.md. The non-claims of this track are the strongest in the
program. Nothing here is a claim about the security of any real
cipher, protocol, implementation, or deployed system. No attack is
developed or evaluated. No statement about computational hardness or
asymptotic security is made or is measurable with these methods. All
models are declared toy models used to audit evaluation methodology.
