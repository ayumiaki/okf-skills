<!--
  OKF adoption snippet. Paste this block into your project's root agent config:

  - Hermes:   MEMORY.md or ~/.hermes/AGENT.md
  - Claude:   CLAUDE.md
  - Codex:    AGENTS.md or AGENT.md
  - Cursor:   AGENT.md
  - Custom:   whatever your harness loads at startup

  Maintained by Ayumi Aki (@ayumiaki). Part of the Agent-Forge toolkit.
  This is what makes the soft-mode "consume / maintain" behavior happen —
  the skills ship no hooks, so this snippet is the trigger.
-->

## Open Knowledge Format (OKF)

This project keeps shared knowledge as an OKF bundle in `.okf/`.

- **Before a task**, if `.okf/` exists, read `.okf/index.md` first and follow
  links into the concepts relevant to the work. Treat broken links as
  not-yet-written knowledge, not errors.
- **After a change** that affects a documented asset (service, API, schema,
  metric, runbook, decision), update the matching concept: refresh its body and
  `timestamp`, fix cross-links, and append a dated entry to the nearest `log.md`.
  Create a new concept for any new asset.
- **Capturing new knowledge** → use the `okf` skill (modes: produce,
  maintain, consume). Adjust the skill trigger syntax to match your harness.
- **Before committing** bundle changes → run `okf_validate.py .okf --strict` and
  resolve every error.

Conformance rule to respect: every concept file needs YAML frontmatter with a
non-empty `type`. Everything else is optional.
