---
type: Tool
title: okf_forge.py
description: One-shot bootstrap scaffolder for new OKF bundles — creates the spec-compliant skeleton in any project.
resource: https://github.com/ayumiaki/okf-skills/blob/main/scripts/okf_forge.py
tags: [python, scaffolding, bootstrap]
timestamp: "2026-07-09T00:00:00Z"
---

# Overview

A zero-dependency script (PyYAML via PEP 723) that scaffolds a conformant `.okf/`
skeleton in any project directory. Creates `index.md`, `log.md`, empty layer
directories, and their `index.md` files — all with spec-valid frontmatter.

# Workflow

```shell
# Basic scaffold
uv run scripts/okf_forge.py .okf --title "My project"

# With description
uv run scripts/okf_forge.py .okf \
  --title "Auth Platform" \
  --description "SSO and token services" \
  --tags "auth, platform, identity"
```

# Layers created

| Directory | Purpose |
|-----------|---------|
| `ui/` | Frontend concepts |
| `api/` | Backend endpoint concepts |
| `data/` | Database schema concepts |
| `decisions/` | Architecture decision records |
| `processes/` | Runbooks and playbooks |
| `metrics/` | Business KPIs |
| `infra/` | Infrastructure concepts |

Each directory gets an `index.md` with a link placeholder, and the root
`index.md` carries the `okf_version` frontmatter required by §4 of the spec.

# After scaffolding

The bundle is immediately conformant — validate it with:
```shell
uv run skills/validate/scripts/okf_validate.py .okf --strict
```

Then fill in concepts using the [produce mode](/skills/okf.md) of the okf skill.

# Citations

[1] [okf_forge.py source](https://github.com/ayumiaki/okf-skills/blob/main/scripts/okf_forge.py)
[2] [OKF v0.1 §4 — Bundle structure](/reference/okf-spec.md#4-bundle-structure)
[3] [Produce skill](/skills/okf.md) — generating concept content after scaffolding
