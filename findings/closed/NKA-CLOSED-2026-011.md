# NKA-CLOSED-2026-011: The premise that a development-capsule build guard only covers release kernels does not hold: the development profile that carries the capsule is itself the guarded configuration

**Closed.** A candidate checked and refuted by a second, independent reviewer.

| | |
|---|---|
| Component | build-time feature guards for development-only attack-simulation capsules |
| Location | development-capsule compile guards; build-profile feature configuration |
| Affected | release yes, main not checked, tested at b3dd1fa37ce2 |
| Reported | 2026-11-21 |
| Closed | 2026-11-23 |

## The claim

A candidate found that two development-only capsules refuse to compile alongside a release-marker feature but not alongside a separate production-marker feature, and concluded this let a production-marked kernel still carry development attack capsules.

## Why it is not a finding

The premise that the production-marker feature identifies a release build does not hold. A full feature-closure computation shows the development profile that is specifically built to carry these attack capsules also carries the production marker by design, and the project's own build tooling refers to that exact combination as its intended development configuration. A guard that refused the production marker would refuse the very development image the capsules exist for. The actual release path is produced by a separate toolchain that adds the true release marker and explicitly refuses development loaders and development capsule sets.

## Routes tried

1. Computed the feature closure for the project's build profiles to confirm which profile carries which markers, and found the development-attack profile carries the production marker by design.
2. Checked the project's own build-tooling comments, which name this exact combination as the intended development configuration.
3. Traced the actual release-production toolchain and confirmed it uses a different, true release marker that the development-capsule guard does check, and that it separately refuses development loaders and development capsule sets.
4. Checked a related comparison the candidate made about a different guard in the same area and found it was based on an outdated line reference; the corrected reading shows that guard follows the same, consistent rule.

## Evidence

Checked independently of the original write-up: yes.

- An independent feature-closure computation was performed over the project's build-profile configuration to confirm which markers each profile carries.
- No kernel build was actually run to double-check the computed closure against a real compiled artifact.
