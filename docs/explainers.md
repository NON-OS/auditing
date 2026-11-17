# Explainers

The audit explains the system as well as testing it. A reader who is not a kernel engineer should be able to learn what each mechanism does, what it does not do, and how to check it.

Each mechanism examined gets one explainer, in this order:

1. **What it is,** in one paragraph.
2. **Why it exists,** the problem and for whom.
3. **How it works,** step by step. Each step cites the code that does it, with a `kernel:` citation at the audited commit.
4. **What it protects against,** by adversary from [threat-model.md](threat-model.md), and under which conditions.
5. **What it does not protect against,** written with the same care.
6. **How to check it yourself,** with commands a reader can run and the output they should see. The commands are run before the explainer is published.
7. **Status.** Which parts are proved, tested, reviewed or assumed, with links.
8. **What the audit found.** Links to published findings that touch it.

Where the audit could not establish something, the explainer says so and does not fill the gap.

The first explainers cover the mechanisms most claims depend on: the boot chain, capsule spawn and its checks, capabilities, the enrolment proof, nsh attestation, the network routes, memory clearing and the data volume. A person who did not write an explainer reads it before it is published, and the notes from that reading are kept.
