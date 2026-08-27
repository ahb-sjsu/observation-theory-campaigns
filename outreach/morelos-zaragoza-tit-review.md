# Outreach draft — internal read request, T-IT manuscript

**To:** robert.morelos-zaragoza@sjsu.edu
**From:** andrew.bond@sjsu.edu
**Attachments:** tit-cr-context.pdf (34 pp)
**Status: DRAFT — owner reviews and sends. Not sent by the assistant.**

---

Subject: Would you give a rate-distortion manuscript a 30-minute read?

Dear Robert,

I am a colleague over in Computer Engineering, and I have a manuscript headed
for the IEEE Transactions on Information Theory that sits squarely in your
territory. I would value a short, skeptical read from someone who works in
coding and information theory natively, and you are the person at SJSU I would
most trust to catch what a T-IT referee will catch.

The paper in three sentences. An encoder observes a jointly Gaussian pair
(Y, V) and describes Y for a decoder that sees the description alone; a third
party holds a noisy copy S = V + U of the context V, and S prices the
description's conditional content I(X; X-hat | S), which is the ideal erasure
work of the stored description under Landauer accounting. This is Steinberg's
common-reconstruction functional applied to the augmented source X = (Y, V),
and the paper evaluates it in closed form: the larger root of an explicit
quadratic, in any ambient dimension, together with the exact region of
achievable rate and conditional-content pairs, whose Pareto frontier is a
two-water-level system. A complete binary solution (doubly symmetric source,
BSC context channel) closes the discrete case through a tilt equation that
interpolates Gray's conditional function at one end and the marginal
rate-distortion function at the other.

I am not asking for a full review of thirty-four pages. Two bounded things, maybe
thirty to forty-five minutes:

1. Table II, on page 3, places each result against its nearest prior
   (Steinberg 2009; Lapidoth, Malar, and Wigger 2014; Xiao and Luo 2005; Gray
   1972). Does the delineation hold up to someone who knows this literature?
   That table is where a referee will attack first.

2. The paper runs thirty-four pages. Section VI (the exact attainment condition
   for the determinant lower bound) is separable. Would you split it out, or
   does a T-IT reader tolerate the length for a self-contained treatment?

Some context you may find interesting: every closed form in the paper is
verified by independent symbolic and numerical scripts, and the algebraic core
is machine-checked in Lean 4. The verification record travels with the
manuscript in a public repository. An earlier, much broader manuscript of mine
was declined at T-IT; this one is the narrow, classical-genre paper that came
out of taking that review seriously.

I would be glad to return the favor on anything of yours, and happier still to
buy the coffee if you prefer to talk it through in person. No deadline
pressure on my side; T-IT is a rolling submission.

Best regards,

Andrew Bond
Department of Computer Engineering
San Jose State University
