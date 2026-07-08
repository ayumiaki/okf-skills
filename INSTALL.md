# OKF Skills — Universal Install

OKF skills are flat markdown + self-locating Python scripts. They drop into
**any agent harness** that reads SKILL.md files and can run shell commands.

## Skill layout

```
skills/
  okf/SKILL.md           # produce / maintain / consume
  validate/SKILL.md      # deterministic §9 conformance check
  visualize/SKILL.md     # render bundle -> self-contained viz.html
scripts/                  # (inside each skill dir; referenced by SKILL.md)
  okf_validate.py
  okf_visualize.py
templates/
  AGENT-SETUP.md          # paste into your project's root agent config
```

## Agent harnesses

### Hermes Agent / Hermes TUI

1. Copy the entire `skills/` directory into `~/.hermes/skills/`
2. Restart the session (`/new`) or load manually
3. Paste `templates/AGENT-SETUP.md` into any project that wants OKF adoption

### Claude Code

1. `claude --plugin-dir /path/to/okf-skills` (local dev)
2. Or: `/plugin marketplace add scaccogatto/okf-skills && /plugin install okf@scaccogatto`
3. Project local adoption: paste `templates/AGENT-SETUP.md` into `CLAUDE.md`

### Codex CLI

1. Copy `skills/` into your project `.codex/skills/` (or wherever your config points)
2. Models with tool-use will auto-discover SKILL.md files
3. Project local adoption: paste `templates/AGENT-SETUP.md` into `AGENTS.md` or `AGENT.md`

### Cursor / Windsurf

1. Copy `skills/` into `.cursor/skills/` or `.windsurf/skills/`
2. Restart editor
3. Project local adoption: paste `templates/AGENT-SETUP.md` into `AGENT.md`

### Generic skill.sh install

```bash
npx skills add scaccogatto/okf-skills
```

## Requirements

- Python 3.11+
- `uv` (preferred) or `python3` + `pyyaml` (PEP 723 inline deps handle install)

The Python scripts are fully standalone: they resolve their own path via `__file__`
and `$0`, so no environment variables, plugin manifests, or harness-specific
config is needed.

## What changed from the Claude-only version

- All `${CLAUDE_SKILL_DIR}` references replaced with self-locating `$0` / `__file__` logic
- `templates/CLAUDE-okf.md` retained for Claude users; `templates/AGENT-SETUP.md`
  added as the universal variant
- No harness-specific code in the Python scripts — they work identically everywhere
- `.claude-plugin/` retained alongside as a first-class install option but is no
  longer required
