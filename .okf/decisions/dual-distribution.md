---
type: Decision
title: Dual distribution — plugin + skills.sh
description: Ship the same repo as a Claude Code plugin and as skills.sh-installable skills, plus flat-install copy-paste for Hermes and any other harness.
tags: [adr, distribution]
timestamp: "2026-06-28T00:00:00Z"
---

# Context

OKF tooling is only useful where the agent already works. Claude Code users want a
plugin; the broader agent ecosystem (Hermes, Codex, Cursor, Windsurf, 20+ agents)
installs via skills.sh or flat copy-paste.

# Decision

One repo, multiple install paths: `.claude-plugin/` makes it a plugin marketplace;
`skills/<name>/SKILL.md` makes it skills.sh-discoverable; flat copy-paste covers
Hermes and any custom harness. The
[okf](/skills/okf.md), [validate](/skills/validate.md), and
[visualize](/skills/visualize.md) skills are identical in every path.

# Consequences

* Maximum reach from a single source of truth.
* Scripts must resolve their own path in every layout — see the
  [self-contained-skills decision](/decisions/self-contained-skills.md).
* Hermes-first flat install is the recommended path for new adopters.
