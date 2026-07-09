---
type: Pipeline
title: CI quality gate
description: GitHub Actions workflow that validates the .okf bundle and sample bundle on every push, enforcing strict conformance.
resource: https://github.com/ayumiaki/okf-skills/blob/main/.github/workflows/ci.yml
tags: [ci, workflow, github-actions, validation]
timestamp: "2026-07-09T00:00:00Z"
---

# Overview

A GitHub Actions workflow that runs on every push and pull request to `main`. It
dogfoods the [validate skill](/skills/validate.md) against both the repo's own
`.okf/` bundle and the [sample bundle](/examples/sample-bundle/).

# Steps

1. **Setup** — install `uv` and checkout the repo.
2. **Validate `.okf/`** — runs `okf_validate.py .okf --strict --json`.
3. **Validate sample bundle** — runs `okf_validate.py examples/sample-bundle --strict --json`.
4. **Report** — uploads the JSON reports as workflow artifacts.

# Strict mode

Uses `--strict` to promote warnings to failures. This enforces:
- No stale or orphaned concepts
- No stale cross-links
- All recommended fields present (title, description, tags, timestamp)
- ISO-formatted timestamps

See the [CI quality gate decision](/decisions/ci-quality-gate.md) for rationale.

# Cleanup mode

On the first of each month, a separate scheduled workflow validates the `docs/`
directory and removes any unreferenced visualization HTML files older than 90
days. This keeps the GitHub Pages site tidy as bundles evolve.

# Self-documentation

The pipeline validates itself — every push ensures both bundles are conformant
before merging. It is the project's quality belt, not just a checkmark.

# Citations

[1] [CI workflow source](https://github.com/ayumiaki/okf-skills/blob/main/.github/workflows/ci.yml)
[2] [CI quality gate decision](/decisions/ci-quality-gate.md) — why strict mode
[3] [validate skill](/skills/validate.md) — the checker it runs
