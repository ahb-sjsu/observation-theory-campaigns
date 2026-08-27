# Outreach draft — P3787 working group, first contact

**To:** Xiaoxiao Chen (P3787 working group chair)
**Cc:** Malia Zaman (IEEE program manager) — for question 3
**From:** andrew.bond@sjsu.edu
**Status: DRAFT — owner reviews and sends. Not sent by the assistant.**

*Salutation note: "Dear Chair Chen" is role-based and avoids assuming a
degree or a form of address. Switch to "Dear Xiaoxiao" if the roster or
the group's mailing list shows first-name norms, which is common once a
group is meeting regularly.*

---

Subject: New participant, and a proposed contribution on validity attestation

Dear Chair Chen,

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

3. Patent policy logistics, and I have copied Malia Zaman since this is
   likely an administrative question rather than a technical one. I want
   to handle the call for potentially essential patents correctly from
   the start. My university has one related disclosure under internal
   review. Nothing in what I propose to contribute depends on it, and
   everything I would cite is already published under a permissive
   licence or archived with a DOI, but I would rather raise it early than
   late. Where the potential holder is the participant's institution
   rather than the participant, what is the right route for an assurance
   letter, and is there anything I should have on file before I present?

Happy to be useful in whatever way the group needs, including review work
that has nothing to do with my own contribution.

Best regards,

Andrew H. Bond
Senior Member, IEEE
Department of Computer Engineering
San José State University
