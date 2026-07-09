---
type: Decision
title: Prescriptive produce mode — structured bundles by project architecture
description: >-
  Instead of letting agents choose any layout, the produce mode now enforces
  a fixed taxonomy of layer directories (ui/api/services/data/processes/decisions/infra)
  and maps source tree hierarchy onto bundle paths. This prevents flat, shallow bundles
  and ensures consistency across projects.
tags: [structure, layout, produce, taxonomy]
timestamp: "2026-07-09T00:00:00Z"
---

# Context

The original OKF spec says: "Directory structure is independent of the domain —
producers organize concepts however makes sense." While true to the spec, this
guidance was too weak. Agents consistently produced flat bundles with concepts
dumped at root or in a single directory. Google's own example bundles
(crypto_bitcoin, ga4, stackoverflow) use consistent category directories with
per-directory index files and 2+ levels of nesting.

When Stephen asked the agent to document Razor Pages, the output put all pages at
`.okf/` root instead of `.okf/ui/pages/account/login.md`. The skill needed stronger
structure enforcement.

# Decision

- **Define fixed layer directories**: `ui/`, `api/`, `services/`, `data/`, `infra/`,
  `processes/`, `decisions/` — each with documented valid `type` values.
- **Enforce hierarchy mirroring**: source paths must map to bundle paths,
  preserving meaningful hierarchy below the framework prefix.
- **Require classification**: every concept must be classified as a code artifact
  (gets a layer-specific type like `Page`, `Controller`, `Table`) or a process
  artifact (gets a cross-cutting type like `Playbook`, `ADR`).
- **Never flat**: no concept may be filed directly at bundle root without a
  subdirectory context.

# Consequences

- Bundles are consistent across projects, agents, and teams.
- Agents can no longer flatten everything into a single directory.
- The `--layers` flag on `okf_forge.py` lets users scaffold only what their
  project needs — no unused directory clutter.
- Consumers (both human and agent) can navigate any bundle with the same
  expectations: ui/pages/, api/controllers/, data/tables/, etc.
- The spec is not violated — this is a producer convention, not a conformance rule.
