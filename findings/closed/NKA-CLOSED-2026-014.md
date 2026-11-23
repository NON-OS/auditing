# NKA-CLOSED-2026-014: A crafted image that decodes faster than it should does not amplify cost beyond what a normal image of the same size already costs

**Closed.** A candidate checked and refuted by a second, independent reviewer.

| | |
|---|---|
| Component | image-decoding capsule, JPEG decoder |
| Location | image-decoding capsule's sized-decode entry point and its surface-based input handling |
| Affected | release yes, main not checked, tested at b3dd1fa37ce2 |
| Reported | 2026-11-18 |
| Closed | 2026-11-23 |

## The claim

A candidate found that a small, specially crafted JPEG file could be decoded by the image codec capsule in a way that consumed a disproportionate amount of CPU time relative to its small declared file size, raising a denial-of-service concern.

## Why it is not a finding

The timing the candidate measured reproduces exactly, but the comparison that would make it a distinct weakness does not hold: a normal, validly-encoded image of a realistic size costs the same or more CPU time to decode than the crafted file, and the decoder's own fixed output-size and work caps bound every decode regardless of input size. Because the codec reads its input from a shared memory surface whose size the sender controls independently of any small fixed-size message channel, anyone who can send the tiny crafted file can just as easily send a normal, larger image that costs the same or more, so the small input size itself adds no new capability.

## Routes tried

1. Reran the exact crafted input through an independent build of the decoder on an idle host and confirmed the reported decode time, then compared it against several normal, validly-encoded images of increasing size produced independently.
2. Confirmed that decode cost for the crafted file is bounded by the same fixed caps (maximum output pixels, maximum work budget) that bound every other decode, so the crafted file does not exceed a cost a normal image could not also reach.
3. Checked whether the small size of the crafted input itself grants any special capability, such as fitting inside a narrower, more frequent message channel: it does not, since the actual image bytes are delivered through a shared memory surface of arbitrary size, not the small fixed-size control channel.

## Evidence

Checked independently of the original write-up: yes.

- Rebuilt the decoder from the production source in an independent release build and reran the exact crafted input, reproducing a comparable decode time to the original report.
- Generated several normal, validly-encoded comparison images independently and measured their decode times under the same conditions, finding them equal to or greater than the crafted file's.
