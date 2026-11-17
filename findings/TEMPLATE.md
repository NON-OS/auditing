# Finding template

Use this privately, outside the repository, from the first candidate to the verified finding.
When the finding is ready to publish, convert it to the JSON form described by the schema.

## Header

- **ID:** NKA-YYYY-NNN
- **Title:**
- **Component:**
- **Affected:** release tag (yes or no), main (yes or no), and the commit hashes tested
- **Location:** file and line at the recorded commit

## Rating

- **Adversary:** A1 to A5, from the threat model
- **Preconditions:** what the adversary needs
- **Severity:** critical, high, medium, low or informational, with the reason from the rubric
- **CVSS 4.0 vector:**
- **Confidence:** confirmed or supported

## Description

What is wrong, and why. State the root cause.

## Impact

What the adversary gains, in terms of the assets in the threat model.

## Attack scenario

Numbered steps from the adversary's starting position to the effect.

## Evidence

- Was it reproduced?
- The exact steps, or the harness and the command that runs it.
- The output.

## Refutation

Who tried to refute this, what they tried, and why it held.

## Remediation

A concrete fix. A regression test or an invariant that would stop the whole class.

## Timeline

Reported, confirmed by the maintainers, fixed, published.
