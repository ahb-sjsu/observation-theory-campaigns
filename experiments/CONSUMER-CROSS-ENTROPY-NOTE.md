# Is there a consumer-relative cross-entropy?

Design note, unsealed, non-claim-bearing. No experimental claims. Everything
below is either a short derivation, a statement of known mathematics, or an
assessment of whether a proposed framing is warranted.

Prompted by 3Blue1Brown, "But what is cross-entropy? Compression is Intelligence
Part 2" (2026-07-16), which presents the Lagrange argument for why the loss must
be a logarithm. The question asked here is whether that argument generalises to
the consumer-relative setting of this programme, and whether the phrase
"compression is intelligence" is warranted once a consumer is introduced.

## 0. Summary of findings

1. The Lagrange route does NOT yield a new consumer-relative cross-entropy. It
   yields an obstruction, and the obstruction is informative.
2. The property that forces the logarithm is LOCALITY, and consumer relativity
   is precisely a failure of locality. The two demands are in direct tension.
3. A short argument shows that with a local loss, any non-uniform consumer
   weighting is incompatible with the minimiser sitting at the data
   distribution. Non-uniform weights move the minimiser to a tilted target.
4. If the tilted target is accepted as the goal, the logarithm IS forced again,
   but the resulting object is ordinary importance-weighted cross-entropy and
   nothing is gained.
5. The correct bridge is geometric, not variational. `P_C = J^T G J` is a
   PULLBACK METRIC, and `tr(P_C Sigma_delta)` is the second-order term of a
   consumer-side divergence. Cross-entropy's Fisher information is the case
   where the output metric is Fisher-Rao, and reconstruction error is the case
   `J = I, G = I`.
6. The mathematics in 1 to 5 is classical. What is this programme's own is the
   empirical demonstration that the distinction bites, and the instrument that
   measures it.

## 1. The standard argument, restated

A local loss assigns to each observation a penalty depending only on the
probability the model gave to the symbol that actually occurred. Write it
`F(q_i)`. Expected loss under the data distribution `p` is

```
L(q) = sum_i p_i F(q_i)      subject to   sum_i q_i = 1
```

Stationarity with multiplier `lambda` gives `p_i F'(q_i) = lambda` for all `i`.
Demanding that `q = p` be stationary for EVERY interior `p` gives

```
p_i F'(p_i) = lambda(p)     for all i
```

so `x F'(x)` is constant, hence `F'(x) = c / x` and `F(x) = c log x + d`. With
`F` strictly decreasing, `c < 0`, which is the negative logarithm.

This is not new with the video. It is the characterisation of the logarithmic
score as the unique LOCAL strictly proper scoring rule, due to Shuford, Albert
and Massengill (1966) and Bernardo (1979), for alphabets of size at least three.
**Citation to be verified before any use in a paper.** The relevant point for us
is not the attribution but the hypothesis: locality is doing all the work.

## 2. First attempt, consumer weights on a local loss

The obvious consumer-relative move is to weight symbols by how much the consumer
cares about them. Let `w_i >= 0` be read weights, the diagonal case of `P_C`,
and take

```
L(q) = sum_i w_i p_i F(q_i)      subject to   sum_i q_i = 1
```

Stationarity gives `w_i p_i F'(q_i) = lambda`. Demand that `q = p` be stationary
for every interior `p`:

```
w_i p_i F'(p_i) = lambda      for all i
```

Now pick any two symbols `i` and `j` and any interior `p` with `p_i = p_j = t`.
Then `w_i t F'(t) = w_j t F'(t)`. Since `t > 0` and `F` is strictly decreasing so
`F'(t) != 0`, this forces `w_i = w_j`. The symbols were arbitrary, so all weights
are equal.

**Result.** With a local loss, the ONLY consumer weighting under which the
minimiser sits at the data distribution is the uniform one. Any genuine consumer
weighting moves the minimiser.

Where does it move to? Keep the logarithm, `F'(x) = -1/x`. Then
`w_i p_i / q_i = -lambda`, so

```
q*_i  =  w_i p_i / sum_j w_j p_j
```

the consumer-tilted distribution. This is worth stating plainly because it is a
practical warning rather than an abstraction. **A model trained under a
consumer-weighted log loss does not learn the data distribution. It learns the
data distribution tilted by the read weights, and that is the intended
behaviour, not a bug.**

## 3. Second attempt, accept the tilted target

Suppose we declare the tilted distribution to be the goal. Demand that
`q* = w p / Z` with `Z = sum_j w_j p_j` be stationary. Writing `v_i = w_i p_i / Z`
so that `w_i p_i = Z v_i`, stationarity reads

```
Z v_i F'(v_i) = lambda      hence      v F'(v) = lambda / Z
```

As `p` ranges over the interior simplex with `w` fixed, `v` ranges over an open
set, so `v F'(v)` is constant on an interval and `F` is again a logarithm.

**Result.** Uniqueness survives, but the object recovered is ordinary
importance-weighted cross-entropy. No new functional appears. The theorem is
true and uninteresting.

## 4. Why the route fails, stated structurally

The consumer's defining feature in this programme is `ker P_C`, the directions it
cannot see. Two states differing only inside the kernel are consumer-equivalent
and a consumer-relative loss must not separate them. That means the minimiser is
a SET, not a point, so the loss is proper but never STRICTLY proper.

Strict propriety is exactly what the Lagrange argument assumes when it demands a
unique stationary point at `q = p`. So the argument's hypothesis and consumer
relativity are incompatible by construction, not by accident.

Equivalently, and more usefully: a local loss reads only `q_i`, the probability
at the realised symbol. A consumer that reads a functional of the whole
distribution is non-local by definition. Locality forces the logarithm;
consumer relativity forbids locality. **There is no consumer-relative cross-
entropy of the local kind, and the reason is a theorem rather than a gap.**

## 5. The bridge that does work, and it is geometric

The consumer-relative distortion this programme actually uses is
`tr(P_C Sigma_delta)`, which is quadratic in an error, not logarithmic in a
probability. That mismatch is the clue.

Let the consumer be a map `C` from the state `x` to an output, and let `D` be a
divergence on outputs vanishing at coincidence. For a perturbation `delta`,

```
D( C(x) || C(x + delta) )  =  (1/2) delta^T J^T G J delta  +  O(delta^3)
```

with `J = dC/dx` and `G` the Hessian of `D` at coincidence. Averaging over
`delta` with covariance `Sigma_delta`,

```
E[ D ]  =  (1/2) tr( J^T G J Sigma_delta )  +  ...  =  (1/2) tr( P_C Sigma_delta )
```

So `tr(P_C Sigma_delta)` IS the expected consumer-side divergence to second
order, and `P_C = J^T G J` is the pullback of the output metric through the
consumer's Jacobian. That is exactly the form this programme already uses.

Two special cases place the video and this programme on one axis.

- `D` = KL on the consumer's output distribution. Then `G` is the Fisher-Rao
  metric of the output family and `P_C` is a PULLBACK FISHER METRIC. For a
  softmax consumer, `G` in probability coordinates is `diag(1/p)`. This is the
  same fact the information-geometry literature states as "KL induces the Fisher
  metric", specialised to a consumer.
- `J = I` and `G = I`. Then `P_C = I` and `tr(Sigma_delta)` is mean squared
  error, that is reconstruction error. This is the `identity` provider already
  registered in `turboquant_pro/read_operators.py`.

**So the video's framing is the `J = I, G = I` corner of the same picture, and
cross-entropy's Fisher information is the `G = Fisher-Rao` corner.** The
programme's `P_C` is the general pullback. That is the unification, and it needs
no new variational principle.

## 6. Is the framing warranted?

**"Consumer-relative cross-entropy derived by a Lagrange uniqueness argument":
NOT warranted.** Section 4 shows the hypothesis fails structurally. Claiming
such a theorem would be wrong.

**"Compression is intelligence, indexed by a consumer": warranted, and this
programme has the sharpest available evidence for the index mattering.**
GO-P-2026-021 built two key-error arms reconstruction-matched to `7.5e-9`, so by
an undifferentiated bit count they are the same compressor, and measured that
blind `tr(P_hat Sigma_delta)` picks the downstream-worse arm on 16 of 16 heads
while reconstruction, exactly tied, scores 2 of 16, which the ledger notes is not
chance since chance is 8 of 16. Two encoders that compress equally well are not
equally good, and the difference is invisible to the metric the slogan uses.

**"P_C is a pullback metric and consumer distortion is a second-order
divergence": warranted, and it is the right way to say it.** But it is classical
information geometry, not a discovery. It should be presented as placing the
programme's object in a known frame, which is a strength, not as a new theorem.

## 7. What is actually this programme's own

The mathematics of sections 1 to 5 is standard. What is not standard, and what
should carry any write-up, is threefold. First, that the distinction is
MEASURABLE BLIND, by the probe, without knowing the consumer. Second, that it
BITES ON A TRAINED MODEL with reconstruction provably tied, which is
GO-P-2026-021. Third, that the gap between two defensible choices of `G` is
LARGE, roughly 0.3 in overlap on one attention head, per C-4 and C-10 in
readscope, so the index is not a technicality.

## 8. Open, if anyone wants it

The non-local scoring rule literature is the right place to look for a
characterisation theorem that survives a kernel. Dropping locality admits the
whole Bregman family, and asking which Bregman divergence is compatible with a
prescribed `ker P_C` is well posed and, as far as this note's author knows,
unasked in this form. It would need a literature check before being called open.
