# Outreach draft — P3787 working group, first contact

**To:** P3787 working group chair / secretary (fill from the roster
confirmation or the project page's officer list)
**From:** andrew.bond@sjsu.edu
**Status: DRAFT — owner reviews and sends. Not sent by the assistant.**

---

Subject: New participant, and a proposed contribution on validity attestation

Dear [chair],

I joined the P3787 roster this week and wanted to introduce myself and
ask three practical questions.

I am on the faculty in Computer Engineering at San José State
University, where I work on freshness and validity of machine-generated
assertions: how a system states that a piece of data is still good, and
how often that statement is wrong. My group has sealed measurements of
that error rate across interdomain routing, replicated databases,
coordination services, and a cellular physical layer, and a public
reference implementation with a third-party-verifiable certificate.

The questions:

1. What is the working group's current state? I would like to know
   whether there is a draft or an outline in circulation, where documents
   live, and what the meeting cadence is, so that anything I bring fits
   the stage you are at rather than the stage I imagine.

2. Would the group like a short contribution on validity attestation? My
   reading of the scope is that P3787 covers who may use an encapsulated
   payload, under what conditions, and until when. What I do not see is a
   place to express whether the payload is still good *for the party now
   reading it*. Validity in production systems is consumer-relative in a
   way a wall-clock expiry cannot capture: in one of our measurements, on
   the same replica at the same instant, a reader with a hot working set
   was stale on roughly 99% of reads while a reader with a cold working
   set was stale on roughly 1%. A single expiry is wrong for one of them.
   Relatedly, attestation as scoped establishes that metadata is intact
   and bound, not that the assertion it carries was true when acted on,
   and an object whose condition has decayed is operationally revoked
   with nothing in the system saying so.

   I have a short written contribution proposing a validity attestation
   class (consumer class, named witness, measured false-clear rate,
   refresh floor) plus one conformance obligation, that enforcement
   points re-evaluate validity at use time against the requesting
   consumer. I would be glad to circulate it, or to present it in ten
   minutes on a call, whichever suits the group.

3. Patent policy logistics. I want to handle the call for potentially
   essential patents correctly from the start. My university has one
   related disclosure under internal review. Nothing in what I propose to
   contribute depends on it, and everything I would cite is already
   published under a permissive licence or archived with a DOI, but I
   would rather raise it early than late. Could you point me to how the
   group handles assurance letters where the potential holder is the
   participant's institution rather than the participant?

Happy to be useful in whatever way the group needs, including review work
that has nothing to do with my own contribution.

Best regards,

Andrew H. Bond
Senior Member, IEEE
Department of Computer Engineering
San José State University
