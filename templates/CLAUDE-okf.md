<!--
  OKF adoption snippet for Claude Code (legacy).

  Maintained by Ayumi Aki (@ayumiaki) as part of Agent-Forge.
  For Hermes, Codex, Cursor, Windsurf, and custom harnesses, use
  AGENT-SETUP.md instead.

  This file is NOT loaded automatically. Paste the block below into the CLAUDE.md
  of a project that adopts OKF (or into ~/.claude/CLAUDE.md to apply it globally).
  It is what makes the soft-mode "consume / maintain" behavior actually happen,
  since the plugin ships no hooks.
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
- **Capturing new knowledge** → use the `/okf:okf` skill (modes: produce,
  maintain, consume).
- **Before committing** bundle changes → run `/okf:validate .okf --strict` and
  resolve every error.

Conformance rule to respect: every concept file needs YAML frontmatter with a
non-empty `type`. Everything else is optional.
