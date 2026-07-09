---
type: Skill
title: okf skill
description: >-
  Produce, maintain, and consume OKF bundles, driven by the verbatim v0.1 spec.
  The produce mode enforces multi-layer bundle structure matching project architecture.
resource: https://github.com/ayumiaki/okf-skills/blob/main/skills/okf/SKILL.md
tags: [skill, produce, maintain, consume]
timestamp: "2026-07-09T00:00:00Z"
---

# Overview

The authoring skill. It teaches the agent to derive concepts from code, docs, and
human decisions; write conformant frontmatter; and cross-link concepts into a
graph — always against the [vendored OKF v0.1 spec](/reference/okf-spec.md), not
memory of it.

# Modes

| Mode | What it does |
|------|--------------|
| `produce` | Analyse the source tree, identify layers (ui/api/services/data/infra), mirror source hierarchy into bundle paths, apply type taxonomy to distinguish code artifacts from process artifacts. Never flat. |
| `maintain` | Keep a bundle in sync with reality after a change. |
| `consume` | Read a bundle as context, following links from `index.md`. |

# Produce mode details

The produce mode now enforces a structured bundle creation workflow:

1. **Read the spec** — always consult [SPEC.md](/reference/okf-spec.md) before writing.
2. **Analyse source tree** — identify which layers the project has (frontend, backend, database, infra).
3. **Map source → bundle** — mirror meaningful source hierarchy, strip framework prefixes, preserve nesting.
4. **Classify by type** — code artifacts get layer-specific types (Page, Controller, Table, Service); process artifacts get cross-cutting types (Process, Playbook, ADR).
5. **Write each concept** — cross-link related concepts using bundle-relative paths.
6. **Create directory indices** — every directory gets an index.md listing its children.
7. **Update log** — append dated entry to log.md.
8. **Validate** — run the deterministic checker; fix every ERROR.

# Relationships

Validates its output with the [validate skill](/skills/validate.md) and can render
it with the [visualize skill](/skills/visualize.md). Its dual delivery is set by
the [dual-distribution decision](/decisions/dual-distribution.md); automatic upkeep
is governed by the [no-hooks decision](/decisions/no-hooks.md). The structured
produce mode is covered by the [prescriptive-bundles decision](/decisions/prescriptive-bundles.md).
