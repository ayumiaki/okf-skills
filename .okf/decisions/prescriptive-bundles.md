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

The original produce mode let agents pick any directory layout. This led to
inconsistent bundles — some flat (all concepts in root), some using arbitrary
folder names, none predictable across projects.

The [okf skill](/skills/okf.md) produce mode now enforces a fixed-layer taxonomy
so that every project's bundle follows the same structural contract. Agents
analysing a new project mirror source tree layers onto bundle paths.

# Decision

The produce mode enforces these layers:

| Layer | When to use | Example source paths |
|-------|-------------|---------------------|
| `ui/` | Frontend code | `pages/`, `components/` |
| `api/` | Backend endpoints | `controllers/`, `routes/` |
| `services/` | Business logic services | `services/`, `lib/` |
| `data/` | Database schemas, models | `db/`, `models/`, `migrations/` |
| `infra/` | Infrastructure config | `deploy/`, `terraform/` |
| `processes/` | Runbooks, playbooks | `docs/runbooks/` |
| `decisions/` | ADRs | `docs/adr/` |

Types are classified into two families:
- **Code artifacts** — layer-specific types (Page, Controller, Service, Table, etc.)
- **Process artifacts** — cross-cutting types (Process, Playbook, ADR, Metric)

# Consequences

Positive: predictable bundle structure across all projects; agents can navigate
any bundle without guessing. Negative: agents mapping a monorepo with unusual
layouts may need to fit square pegs into round holes. This is mitigated by the
taxonomy being extensible — producers can add layers.

# Related

- [okf skill](/skills/okf.md) — the skill that implements this decision
- [self-contained skills](/decisions/self-contained-skills.md) — how skills ship independently
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
