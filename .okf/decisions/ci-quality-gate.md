---
type: Decision
title: CI quality gate — strict validation on push
description: The CI pipeline fails on any warning (not just errors) from the conformance checker, enforcing full spec adherence.
tags: [adr, ci, quality, validation]
timestamp: "2026-07-09T00:00:00Z"
---

# Context

The [validate skill](/skills/validate.md) outputs two levels: `ERROR` (hard §9
failures) and `warn` (soft guidance like missing recommended fields or broken
links). With `--strict`, warnings are promoted to exit-code failures.

The question was: should CI use `--strict` (failing on warnings) or bare mode
(failing only on errors)?

# Decision

CI runs **strict** mode — warnings are treated as failures. Rationale: the
bundle is the repo's self-documentation. A missing `description`, a stale
`timestamp`, or a broken cross-link degrades consumption for both humans and
agents. Cheap to fix at commit time, expensive to debug in production.

# Consequences

Positive: the bundle stays clean as code changes. Negative: contributors must
run validation locally before pushing. Mitigated by CI surfacing the exact
line and field for each warning.

# Related

- [CI pipeline](/components/ci-pipeline.md) — the implementation
- [validate skill](/skills/validate.md) — the checker
- [no-hooks decision](/decisions/no-hooks.md) — why we don't ship pre-commit hooks
