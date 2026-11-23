# NKA-CLOSED-2026-008: A predictable time-sync nonce and weak server check are real but unreachable in every shipped build profile

**Closed.** A candidate checked and refuted by a second, independent reviewer.

| | |
|---|---|
| Component | network time synchronization capsule protocol handling |
| Location | network time-sync capsule's request and reply-parsing code; kernel clock-adjustment syscall bounds |
| Affected | release yes, main not checked, tested at b3dd1fa37ce2 |
| Reported | 2026-11-18 |
| Closed | 2026-11-23 |

## The claim

A candidate found that the time-sync capsule's protocol implementation uses a predictable nonce derived from the local clock, a fixed, hardcoded server address, and a weak reply-source check, which together would let a network attacker spoof a time update within a wide, multi-decade window.

## Why it is not a finding

Every one of the code-level weaknesses the candidate found is real and would stand as written if the capsule shipped. It does not: a full feature-closure computation over every build profile the project defines shows the capsule's spawn path is compiled out whenever the standard network stack is present, which every real profile has, and no build or packaging script in the tree enables the narrow configuration that would include it. The network attacker this candidate needs has nothing to attack in any image the project actually produces.

## Routes tried

1. Confirmed each code-level claim directly: the nonce is derived from the local wall clock, the server address is fixed in source, and the reply check does not bind to an unpredictable value.
2. Traced the capsule's only spawn call site and confirmed it compiles to nothing whenever the standard network stack feature is enabled, which it is in every real build profile.
3. Computed the feature closure for every build profile the project's configuration defines and confirmed none of them would build the narrow feature set needed to include this capsule.
4. Searched the full tree for any build or packaging script that produces the narrow configuration: none found.

## Evidence

Checked independently of the original write-up: yes.

- An independent feature-closure computation over the project's own build-profile configuration confirmed the capsule's exclusion from every real profile.
