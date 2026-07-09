<div align="center">

# 📚 OKF Skills

**Portable coding-agent skills for producing, validating, and visualizing
[Open Knowledge Format](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)
bundles. One format, any agent, zero lock-in.**

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
[![OKF spec](https://img.shields.io/badge/OKF-v0.1-6E56CF.svg)](skills/okf/reference/SPEC.md)

```shell
uv run skills/okf-visualize/scripts/okf_visualize.py .okf -o viz.html --title "My project"
```

</div>

---

## Skills

| Skill | What it does |
|-------|--------------|
| [`skills/okf/`](skills/okf/) | **Produce, maintain, and consume** OKF bundles. Scans source trees, maps layers (ui/api/services/data/infra/decisions), generates frontmatter, creates index files, and tracks changes. Ships its own produce script (`scripts/okf_produce.py`) and bootstrap scaffold (`scripts/okf_forge.py`). |
| [`skills/okf-validate/`](skills/okf-validate/) | **Deterministic §9 conformance check.** Zero-config — `uv run skills/okf-validate/scripts/okf_validate.py <path> --strict`. Catches missing frontmatter, wrong types, broken cross-links. |
| [`skills/okf-visualize/`](skills/okf-visualize/) | **Self-contained interactive graph.** Renders any bundle to a single `viz.html` — nodes coloured by type, clickable, searchable, deep-linkable. |

Every skill is a flat `SKILL.md` + `scripts/` (or `templates/` or `reference/`). Copy a skill directory to any agent's skill path and it works — no plugin manifest, no dependency.

## Quick start

```shell
# Bootstrap a new bundle in any project
uv run skills/okf/scripts/okf_forge.py .okf --title "My project"

# Validate before committing
uv run skills/okf-validate/scripts/okf_validate.py .okf --strict

# Visualize the knowledge graph
uv run skills/okf-visualize/scripts/okf_visualize.py .okf -o viz.html --title "My project"
```

All scripts are **self-locating** — they work from any working directory because they find their own path via `__file__`.

## Bundle structure

```
.okf/
├── index.md          # Project overview + layer index
├── log.md            # ISO-dated change history
├── ui/               # Pages, components, routes
├── api/              # Controllers, endpoints, middleware
├── services/         # Business logic, background jobs
├── data/             # Tables, views, migrations
├── infra/            # Docker, CI/CD, Terraform
├── processes/        # Runbooks, playbooks, SOPs
└── decisions/        # ADRs, architecture decisions
```

Types are two families: **code artifacts** (Page, Controller, Service, Table...) and **process artifacts** (Process, ADR, Playbook, Metric...). Source paths mirror into bundle paths.

## Install

All three skills are flat-copy. Drop them into any agent's skill loader:

```shell
# Hermes
cp -r skills/okf ~/.hermes/skills/okf
cp -r skills/okf-validate ~/.hermes/skills/okf-validate
cp -r skills/okf-visualize ~/.hermes/skills/okf-visualize

# Claude Code / Codex CLI / Cursor / Windsurf
cp -r skills/<name> /path/to/agent/skills/
```

Install docs coming soon.

## License

MIT. The OKF spec (`skills/okf/reference/SPEC.md`) is vendored from the
[Google Cloud Data Cloud team](https://github.com/GoogleCloudPlatform/knowledge-catalog)
under Apache-2.0.
