<div align="center">

# 📚 OKF Skills — the Open Knowledge Format toolkit for any coding agent

**Ship project knowledge as portable markdown bundles. One format, every agent,
zero lock-in. Built for multi-harness shops that run more than one coding agent.**

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
[![OKF spec](https://img.shields.io/badge/OKF-v0.1-6E56CF.svg)](skills/okf/reference/SPEC.md)
[![CI](https://github.com/ayumiaki/okf-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/ayumiaki/okf-skills/actions/workflows/ci.yml)

### Visualise any OKF bundle as an interactive graph

```shell
uv run skills/visualize/scripts/okf_visualize.py .okf -o viz.html --title "My project"
# Open viz.html in any browser — click nodes, search, share deep links
```

</div>

---

> [**OKF**](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)
> is an open, vendor-neutral format (announced by Google Cloud, June 2026) that
> represents knowledge — the context and curated insight around your systems — as
> a directory of markdown files with YAML frontmatter. No schema registry. No
> runtime. If you can `cat` a file you can read it; if you can `git clone`
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
> behind it live in [`.okf/`](.okf/). CI validates that bundle on every push
> (dogfooding the conformance checker). See it as a self-graph by running
> `uv run skills/visualize/scripts/okf_visualize.py .okf -o docs/self.html --title "OKF Skills"`.

## What's inside

| Component | What it does |
|-----------|--------------|
| `skills/okf/SKILL.md` | Produce / maintain / consume bundles, applying the spec and templates. Auto-triggers when a repo has an OKF bundle. The `produce` mode enforces proper multi-layer bundle structure with type taxonomy (see below). |
| `skills/validate/SKILL.md` | Deterministic §9 conformance check (not an eyeball pass). |
| `skills/visualize/SKILL.md` | Render a bundle to a self-contained interactive HTML graph (`viz.html`). |
| `skills/validate/scripts/okf_validate.py` | Standalone, zero-config validator (`uv run`, PyYAML via PEP 723). |
| `skills/visualize/scripts/okf_visualize.py` | Standalone bundle→`viz.html` renderer (Cytoscape + marked via CDN). |
| `skills/okf/reference/SPEC.md` | The OKF v0.1 spec, vendored verbatim — the source of truth. |
| `templates/AGENT-SETUP.md` | Universal adoption snippet (Hermes, Codex, Cursor, Windsurf, custom). |
| `examples/sample-bundle/` | A conformant reference bundle (8 concepts: services, datasets, decisions, runbooks, metrics). |
| `scripts/okf_forge.py` | One-shot bootstrap: scaffold a new `.okf/` bundle in any project with spec-compliant skeleton, with `--layers` flag to match your project type. |

## How a bundle looks

The toolkit enforces **structured bundles** — never flat. Every concept lives in a
subdirectory that mirrors the project's architecture layer.

**Full-stack project (Razor Pages + API + database):**

```
.okf/
├── index.md                    # Project overview, lists all layers
├── log.md                      # ISO-dated change history
├── ui/
│   ├── index.md
│   ├── pages/
│   │   ├── index.md
│   │   ├── account/
│   │   │   ├── index.md
│   │   │   ├── login.md        # type: Page
│   │   │   └── register.md     # type: Page
│   │   └── orders/
│   │       ├── index.md
│   │       ├── list.md         # type: Page
│   │       └── detail.md       # type: Page
│   └── components/
│       ├── index.md
│       ├── navbar.md           # type: Component
│       └── data-table.md       # type: Component
├── api/
│   ├── index.md
│   ├── controllers/
│   │   ├── index.md
│   │   ├── orders-controller.md   # type: Controller
│   │   └── auth-controller.md     # type: Controller
│   └── middleware/
│       ├── index.md
│       └── request-logging.md     # type: Middleware
├── services/
│   ├── index.md
│   ├── pricing-service.md         # type: Service
│   └── jobs/
│       ├── index.md
│       └── invoice-reminder.md    # type: Background Job
├── data/
│   ├── index.md
│   ├── tables/
│   │   ├── index.md
│   │   ├── orders.md              # type: Table
│   │   └── customers.md           # type: Table
│   ├── views/
│   │   ├── index.md
│   │   └── active-customers.md    # type: View
│   └── migrations.md              # type: Migration
├── processes/
│   ├── index.md
│   └── order-fulfillment.md       # type: Process
└── decisions/
    ├── index.md
    └── use-blazor-over-mvc.md     # type: ADR
```

**Database-only project:**

```
.okf/
├── index.md
├── log.md
├── data/
│   ├── index.md
│   ├── tables/
│   │   ├── index.md
│   │   ├── orders.md             # type: Table
│   │   └── customers.md          # type: Table
│   ├── views/ …                  # type: View
│   └── stored-procedures/ …      # type: Stored Procedure
├── processes/ …
└── decisions/ …
```

### Layer taxonomy

| Layer | What goes there | Valid `type` values |
|-------|----------------|---------------------|
| `ui/` | Pages, components, layouts, routes | `Page`, `Component`, `Layout`, `Route`, `Hook`, `Store`, `Style` |
| `api/` | Controllers, endpoints, middleware, DTOs | `Controller`, `Endpoint`, `Middleware`, `DTO`, `Guard`, `Route` |
| `services/` | Business logic, service classes, background jobs | `Service`, `Background Job`, `Event Handler`, `Publisher` |
| `data/` | Tables, views, stored procs, migrations, entities | `Table`, `View`, `Stored Procedure`, `Migration`, `Index`, `Trigger`, `Seed`, `Entity` |
| `infra/` | Docker, CI/CD, Terraform, deploy config | `Deployment`, `CI Pipeline`, `Docker`, `Terraform`, `Config` |
| `processes/` | Runbooks, playbooks, SOPs, workflows | `Process`, `Playbook`, `On-Call`, `Workflow`, `SOP` |
| `decisions/` | ADRs, architecture decisions | `Decision`, `ADR` |

Source paths mirror into bundle paths: `src/MyApp.UI/Pages/Account/Login.cshtml`
→ `.okf/ui/pages/account/login.md`.

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

**Claude Code plugin** (legacy compatibility):

```shell
/plugin marketplace add ayumiaki/okf-skills
/plugin install okf@ayumiaki
```

See [INSTALL.md](INSTALL.md) for per-harness setup, including path config,
agent config snippets (`AGENTS.md`, `CLAUDE.md`, etc).

The scripts live inside their skills and are **self-locating** via `$0` /
`__file__`, so they work identically in every install path — no
`${CLAUDE_SKILL_DIR}` dependency.

Requires [`uv`](https://docs.astral.sh/uv/) for the scripts (or `python3` +
`pyyaml`).

## Use it

**Bootstrap a new bundle** in any project:

```shell
uv run scripts/okf_forge.py .okf --title "My project"

# For a frontend-only project:
uv run scripts/okf_forge.py .okf --title "My SPA" --layers ui,decisions

# For a database project:
uv run scripts/okf_forge.py .okf --title "My DB" --layers data,processes,decisions
```

**Produce a bundle** with your agent — ask it to document your project in OKF.
The agent will:
1. Analyse the source tree to identify layers (ui, api, services, data, infra...)
2. Mirror source paths into bundle paths (never flat!)
3. Use the correct `type` taxonomy for each concept (code types vs process types)
4. Create per-directory `index.md` files and update `log.md`

**Validate** before committing:

```shell
uv run skills/validate/scripts/okf_validate.py .okf --strict
```

**Visualize** the knowledge graph — a self-contained `viz.html` that opens in any
browser:

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

## Repository layout

```
okf-skills/
├── skills/okf/{SKILL.md, reference/SPEC.md, templates/}
├── skills/validate/{SKILL.md, scripts/okf_validate.py}
├── skills/visualize/{SKILL.md, scripts/okf_visualize.py}
├── scripts/okf_forge.py             # one-shot bundle scaffolder
├── examples/sample-bundle/          # reference bundle (8 concepts)
├── docs/                            # offline HTML visualizations
├── templates/AGENT-SETUP.md         # universal adoption snippet
├── INSTALL.md                       # per-harness install guide
├── .github/workflows/ci.yml
└── .okf/                            # this repo documents itself in OKF
```

## Contributing

Issues and PRs welcome — new templates, producers for more sources, validator and
visualizer improvements, harness-specific installers, and anything that makes
knowledge-as-code feel less like a chore and more like a superpower. CI validates
the plugin manifest, the example bundle, and the repo's own `.okf/` bundle on
every push.

## Credits & license

- The **Open Knowledge Format** specification is by the Google Cloud Data Cloud
  team, released under Apache-2.0. `skills/okf/reference/SPEC.md` is vendored
  verbatim from the [reference repository](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)
  with attribution.
- **OKF Skills** (this fork) is maintained by **Ayumi Aki** ([@ayumiaki](https://github.com/ayumiaki)).
  It adds universal multi-harness support (flat install, self-locating scripts,
  agent-agnostic setup templates), Hermes-native install paths, the
  `okf_forge.py` bootstrap tool, and the prescriptive multi-layer produce mode
  that enforces structured bundles by project architecture. Released under **MIT**.
