<div align="center">

# 📚 Agent-Forge — the Open Knowledge Format toolkit for any coding agent

**Ship project knowledge as portable markdown bundles. One format, every agent,
zero lock-in. Built for multi-harness shops that actually run more than one
coding agent.**

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
[![OKF spec](https://img.shields.io/badge/OKF-v0.1-6E56CF.svg)](skills/okf/reference/SPEC.md)
[![skills.sh](https://img.shields.io/badge/skills.sh-installable-22C55E.svg)](https://skills.sh/ayumiaki/agent-forge)
[![Hermes native](https://img.shields.io/badge/Hermes-native-22C55E.svg)](skills/okf/SKILL.md)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-3B82F6.svg)](#contributing)

### ▶ [**Open the live demo**](https://ayumiaki.github.io/agent-forge/) — a real OKF bundle as an interactive graph

[![agent-forge — explore an OKF bundle as an interactive graph](docs/assets/demo.gif)](https://ayumiaki.github.io/agent-forge/)

*Click any node → rendered markdown, typed metadata, and "Links to / Cited by" backlinks. No backend, nothing leaves the page.*

</div>

---

> [**OKF**](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)
> is an open, vendor-neutral format (announced by Google Cloud, June 2026) that
> represents knowledge — the context and curated insight around your systems — as
> a directory of markdown files with YAML frontmatter. No schema registry. No
> runtime. No SDK. If you can `cat` a file you can read it; if you can `git clone`
> a repo you can ship it.

This is the **agent-agnostic** OKF toolchain. It teaches *any* coding agent to
**produce**, **maintain**, **consume**, **validate**, and **visualize** OKF
bundles as a normal part of how it already works — driven by the *verbatim*
spec, backed by a deterministic conformance checker, with a self-contained graph
renderer. Ships as **standalone skills** (Hermes, Claude Code, Codex CLI,
Cursor, Windsurf, 20+ harnesses) with zero plugin-manifest dependency.

## Why knowledge-as-code (and where OKF fits)

Project knowledge lives scattered across wikis, code comments, and people's heads;
agents re-discover it from scratch every session. OKF gives it one durable,
diffable, portable home — versioned next to the code it describes. It is
**complementary** to the rest of your context stack, not a replacement:

| | **OKF bundle** (this) | `AGENTS.md` / `CLAUDE.md` | Agent auto-memory | Wiki / Notion |
|---|:---:|:---:|:---:|:---:|
| Purpose | curated **knowledge** | standing **instructions** | implicit notes | human docs |
| Portable across agents/tools | ✅ plain md + yaml | ⚠️ agent-specific | ❌ per-agent store | ⚠️ export needed |
| Versioned with code in git | ✅ | ✅ | ❌ | ❌ |
| Typed & queryable | ✅ frontmatter | ❌ prose | ❌ | ⚠️ |
| Graph of linked concepts | ✅ | ❌ | ❌ | ⚠️ |
| Curated & reviewed in PRs | ✅ | ✅ | ❌ implicit | ⚠️ |
| Scales past the context window | ✅ progressive disclosure | ❌ loaded wholesale | ⚠️ | n/a |

Use `AGENTS.md` for *how to behave*, auto-memory for *what the agent picked up*,
and an OKF bundle for *what the team knows* — shared, structured, and shippable.

> 🪞 **This repo documents itself in OKF.** The architecture, skills, and decisions
> behind Agent-Forge live in [`.okf/`](.okf/) — explore them as a
> [**live self-graph**](https://ayumiaki.github.io/agent-forge/self.html). CI
> validates that bundle on every push (dogfooding the conformance checker).

## What's inside

| Component | What it does |
|-----------|--------------|
| `skills/okf/SKILL.md` | Produce / maintain / consume bundles, applying the spec and templates. Auto-triggers when a repo has an OKF bundle. |
| `skills/validate/SKILL.md` | Deterministic §9 conformance check (not an eyeball pass). |
| `skills/visualize/SKILL.md` | Render a bundle to a self-contained interactive HTML graph (`viz.html`). |
| `skills/validate/scripts/okf_validate.py` | Standalone, zero-config validator (`uv run`, PyYAML via PEP 723). |
| `skills/visualize/scripts/okf_visualize.py` | Standalone bundle→`viz.html` renderer (Cytoscape + marked via CDN). |
| `skills/okf/reference/SPEC.md` | The OKF v0.1 spec, vendored verbatim — the source of truth. |
| `templates/AGENT-SETUP.md` | Universal adoption snippet (Hermes, Codex, Cursor, Windsurf, custom). |
| `examples/sample-bundle/` | The conformant bundle behind the live demo — code, data, decisions, runbooks, metrics. |
| `scripts/okf_forge.py` | One-shot bootstrap: scaffold a new `.okf/` bundle in any project with the spec-compliant skeleton. |

## Install

**Hermes skill** (recommended for Ayumi / Hermes users):

```shell
cp -r skills/okf   ~/.hermes/skills/okf
cp -r skills/validate ~/.hermes/skills/validate
cp -r skills/visualize ~/.hermes/skills/visualize
```

**Flat install for any harness** (Claude Code, Codex CLI, Cursor, Windsurf, custom):

```shell
cp -r skills/<name> /path/to/your/agent/skills/
```

**Optional: Claude Code plugin** (legacy compatibility):

```shell
/plugin marketplace add ayumiaki/agent-forge
/plugin install okf@ayumiaki
```

See [INSTALL.md](INSTALL.md) for per-harness setup, including path config,
agent config snippets (`AGENTS.md`, `CLAUDE.md`, etc), and what changed from the
Claude-only origin.

The scripts live inside their skills and are **self-locating** via `$0` /
`__file__`, so they work identically in every install path — no
`${CLAUDE_SKILL_DIR}` dependency.

Requires [`uv`](https://docs.astral.sh/uv/) for the scripts (or `python3` +
`pyyaml`).

## Use it

**Bootstrap a new bundle** in any project:

```shell
uv run scripts/okf_forge.py .okf --title "My project"
```

**Produce a bundle** — ask your agent to "document the auth service in OKF", or run:

```shell
uv run skills/okf/scripts/okf_produce.py .okf   # if shipped
# or invoke via your harness's skill system
```

**Validate** before committing:

```shell
uv run skills/validate/scripts/okf_validate.py .okf --strict
```

**Visualize** the knowledge graph — a self-contained `viz.html` that opens in any
browser ([live example](https://ayumiaki.github.io/agent-forge/)):

```shell
uv run skills/visualize/scripts/okf_visualize.py .okf \
  -o viz.html --title "My project" --link "https://github.com/me/project"
```

Every concept gets a shareable deep link — open `viz.html#services/auth-api` and the
graph loads with that concept already selected.

**Turn on automatic upkeep (soft mode).** This repo ships *no hooks* by design.
To have your agent consult `.okf/` before tasks and write knowledge back after changes,
paste [`templates/AGENT-SETUP.md`](templates/AGENT-SETUP.md) into your project's
agent config (`AGENTS.md`, `CLAUDE.md`, etc).

## How a bundle looks

```
.okf/
├── index.md                  # progressive disclosure (root carries okf_version)
├── log.md                    # ISO-dated change history, newest first
├── services/
│   ├── index.md
│   └── auth-api.md           # one concept = one file; path is its ID
├── datasets/orders-db.md
├── decisions/use-okf.md
├── runbooks/payment-failures.md
└── metrics/checkout-conversion.md
```

Each concept needs only one thing to be conformant: YAML frontmatter with a
non-empty `type`. Everything else is optional and tolerated when missing.

```markdown
---
type: Service
title: Auth API
description: Issues and verifies short-lived access tokens.
resource: https://github.com/acme/auth
tags: [auth, platform]
timestamp: 2026-06-14T10:00:00Z
---

# Endpoints
| Method | Path     | Description                |
|--------|----------|----------------------------|
| `POST` | `/token` | Exchange creds for a JWT.  |
```

## Repository layout

```
agent-forge/
├── skills/okf/{SKILL.md, reference/SPEC.md, templates/}
├── skills/validate/{SKILL.md, scripts/okf_validate.py}
├── skills/visualize/{SKILL.md, scripts/okf_visualize.py}
├── scripts/okf_forge.py             # one-shot bundle scaffolder
├── examples/sample-bundle/          # the live-demo bundle
├── docs/                            # GitHub Pages: live interactive demo
├── templates/AGENT-SETUP.md         # universal adoption snippet
├── INSTALL.md                       # per-harness install guide
├── .github/workflows/ci.yml
└── .okf/                            # this repo is documented in OKF too
```

## Contributing

Issues and PRs welcome — new templates, producers for more sources, validator and
visualizer improvements, harness-specific installers, and anything that makes
knowledge-as-code feel less like a chore and more like a superpower. CI validates
the plugin manifest and the example bundle on every push.

## Credits & license

- The **Open Knowledge Format** specification is by the Google Cloud Data Cloud
  team, released under Apache-2.0. `skills/okf/reference/SPEC.md` is vendored
  verbatim from the [reference repository](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)
  with attribution.
- **Agent-Forge** (this fork) is maintained by **Ayumi Aki** ([@ayumiaki](https://github.com/ayumiaki)).
  It adds universal multi-harness support (flat install, self-locating scripts,
  agent-agnostic setup templates), Hermes-native install paths, and the
  `okf_forge.py` bootstrap tool. Released under **MIT**.

