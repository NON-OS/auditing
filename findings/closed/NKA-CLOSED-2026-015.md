# NKA-CLOSED-2026-015: A package format's internal page-digest table is not checked by parsing alone, but the format's actual production reader never trusts parsing alone either

**Closed.** A candidate checked and refuted by a second, independent reviewer.

| | |
|---|---|
| Component | userspace package format used to deliver Linux-compatible application content |
| Location | package format's low-level parsing and page-table layout code; the production loader and content-serving code that actually uses packages at runtime |
| Affected | release yes, main not checked, tested at b3dd1fa37ce2 |
| Reported | 2026-11-22 |
| Closed | 2026-11-23 |

## The claim

A candidate found that the package format's low-level parser accepts a package whose internal page-level digest table does not match its contents, which the candidate read as breaking the format's own documented one-pack-one-layout guarantee.

## Why it is not a finding

The parser's behavior reproduces exactly as described, but the guarantee the candidate read into the code is narrower than stated: the format's own documented guarantee is about physical layout (placement, ordering, no gaps), which is checked, not about content digests, which are deliberately checked only when content is actually served, not at parse time. The production code path that loads and serves packages at runtime never relies on the low-level parser alone; it separately verifies both whole-file and per-page content digests before serving any bytes, and those served bytes are additionally bound to a kernel-verified installation record that an attacker was not shown able to forge.

## Routes tried

1. Checked whether the low-level parser's documented guarantee actually covers content digests: it does not, on a direct reading of the code's own stated guarantee, which is about layout placement only.
2. Checked whether the production application-loading code actually uses the low-level parser's unchecked guarantee directly: it does not; it uses a separate, higher-level interface that verifies content digests before serving any file or page.
3. Checked whether an attacker could place a package with a mismatched digest table where the production loader would accept it: doing so requires passing the kernel's own installation verification over the package header, and no route was found for an attacker to forge that verification.
4. Determined the effect if a mismatched header somehow were accepted: whole-file reads would still serve digest-matching bytes, and page-level reads would fail closed, so the worst case is an availability effect under a precondition that was not shown reachable.

## Evidence

Checked independently of the original write-up: yes.

- Independently reconstructed the reported parser behavior in a standalone test harness built from the production source, and confirmed it reproduces byte for byte.
- Traced the actual production loading and content-serving code path and confirmed it does not call the low-level parser interface the candidate exercised.
