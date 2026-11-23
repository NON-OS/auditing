# Closed-case template

Use this to convert a refuted candidate into a closed case. When it is ready to publish, convert it
to the JSON form described by `schema/closed-case.schema.json`.

## Header

- **ID:** NKA-CLOSED-YYYY-NNN
- **Title:**
- **Component:**
- **Affected:** release tag (yes or no), main (yes or no, checked or not), and the commit hashes tested
- **Location:** file and line at the recorded commit

## The claim

What the worker suspected, in one or two sentences, stated fairly, as the worker meant it.

## Why it is not a finding

The actual reason a second, independent reviewer refuted it: an unreachable precondition, an existing
check that already stops it, documented and intended behavior, or evidence that did not reproduce.
State which, and say why in terms of the code.

## Routes tried

Every route the reviewer tried to make the candidate real, numbered, with the result of each.
A route that found nothing is still listed.

## Evidence

- Was anything run to check this, independently of the original worker's own notes?
- The exact steps or the harness and the command.
- The output.

## Timeline

Reported, checked, closed.
