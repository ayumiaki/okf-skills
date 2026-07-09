---
type: Tool
title: okf_produce.py
description: Walk a source tree, map files to taxonomy layers, and generate OKF concept stubs for each meaningful source file.
resource: https://github.com/ayumiaki/okf-skills/blob/main/scripts/okf_produce.py
tags: [python, produce, source-analysis, scaffolding]
timestamp: "2026-07-09T00:00:00Z"
---

# Overview

Analyses a source code directory, identifies meaningful source files (skipping
node_modules/, .git/, __pycache__/, binary assets, generated files, and index
files), maps each to an OKF taxonomy layer using directory name patterns and
file extensions, then creates one concept stub per file.

The [produce mode](/skills/okf.md) it supports is agent-driven (the agent uses
this script to bootstrap concept files, then fills in the bodies), not a fully
automatic knowledge extraction tool — it handles the *scaffolding* and *mapping*
phases of the produce workflow.

# Usage

```shell
# First scaffold the bundle skeleton
uv run scripts/okf_forge.py .okf --title "My Project"

# Then populate with concept stubs from source
uv run scripts/okf_produce.py --source . --bundle .okf --name "My Project"

# Dry-run without writing anything
uv run scripts/okf_produce.py --source src/ --bundle .okf --dry-run
```

# Pattern mapping

Matches source directory names (case-insensitive, substring) to taxonomy layers:

| Source pattern | Layer | OKF type |
|----------------|-------|----------|
| `pages/`, `components/`, `views/` | `ui/` | `Page` / `Component` |
| `controllers/`, `routes/`, `api/` | `api/` | `Controller` |
| `services/`, `domain/`, `use-cases/` | `services/` | `Service` |
| `models/`, `db/`, `entities/` | `data/` | `Model` / `Migration` |
| `deploy/`, `terraform/`, `docker/` | `infra/` | `Deployment` |
| `runbooks/`, `playbooks/` | `processes/` | `Runbook` |
| `adr/`, `decisions/`, `rfcs/` | `decisions/` | `ADR` |

Unmatched files fall back to extension-based heuristics (`.py` → `Service`,
`.tsx` → `Component`, `.tf` → `Deployment`, etc.).

# Relationship

Depends on [okf_forge.py](forge.md) to scaffold the bundle skeleton first.
Output can be validated by [okf_validate.py](validator.md).

# Citations

- Source mapping heuristics inspired by [srcery](https://github.com/srcery-colors/srcery)
  and conventions from typical web/mobile monorepo layouts.
- Type taxonomy defined in [prescriptive-bundles decision](/decisions/prescriptive-bundles.md).
