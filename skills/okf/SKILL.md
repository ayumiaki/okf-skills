---
name: okf
description: >-
  Author, maintain, and consume Open Knowledge Format (OKF) knowledge bundles —
  portable markdown + YAML frontmatter that both humans and agents read. Use when
  capturing project knowledge (services, APIs, schemas, metrics, runbooks,
  decisions) into an OKF bundle, when updating one after code or docs change, or
  when a repository contains an `.okf/` (or other OKF) bundle that should inform
  the task. Triggers on: "document this in OKF", "update the knowledge bundle",
  "capture this as a concept", or any work in a repo that has an OKF bundle.
user-invocable: true
argument-hint: "[produce|maintain|consume] [path]"
allowed-tools: Read Write Edit Grep Glob Bash
---

# Open Knowledge Format (OKF) skill

OKF represents knowledge as a directory of markdown files with YAML frontmatter.
It is minimal by design: no schema registry, no runtime, no SDK. Your job is to
produce, maintain, and consume OKF bundles **conformant with the spec**, not your
memory of it.

**Always read the canonical spec before non-trivial work:**
[reference/SPEC.md](reference/SPEC.md). It is the verbatim OKF v0.1 specification
and the source of truth for every rule below.

## The one hard rule

A bundle is conformant (§9) iff: every non-reserved `.md` file has a parseable
YAML frontmatter block, and every such block has a **non-empty `type`** field.
Everything else is soft guidance. Consumers MUST tolerate missing optional
fields, unknown types, and broken links — never reject a bundle over them.

## Conventions to apply

- **One concept = one file.** The file path (minus `.md`) is the concept ID.
- **Frontmatter:** `type` is required. Add `title`, `description`, `tags`,
  `timestamp` (ISO 8601) when they aid consumption; add `resource` (a canonical
  URI) only for concepts bound to a real asset — omit it for abstract concepts.
- **Body:** prefer structural markdown (headings, tables, lists, fenced code).
  Conventional headings: `# Schema`, `# Examples`, `# Citations`.
- **Cross-links:** standard markdown links; prefer absolute bundle-relative
  form (`/services/auth-api.md`). A link asserts a relationship; its *kind* lives
  in the surrounding prose, not the link.
- **Reserved files:** `index.md` (directory listing, no frontmatter — except the
  bundle-root index may carry only `okf_version`) and `log.md` (ISO-dated change
  history, newest first). Never use these names for concepts.

Templates to copy: [concept](templates/concept.md), [index](templates/index.md),
[log](templates/log.md).

## Default bundle location

Use `.okf/` at the repository root unless the project already uses another
location. Commit it alongside the code it describes — knowledge as code.

## Modes

### produce — create or extend a bundle

**Critical rule: never dump concepts flat at bundle root.**
Every concept belongs in a subdirectory that reflects its layer in the project.
The only exceptions: bundle-root `index.md` and `log.md`.

#### Step 1 — Read the spec

Read [reference/SPEC.md](reference/SPEC.md) before writing anything.

#### Step 2 — Analyze the source tree

Walk the project to identify its layers. Not all projects have all layers. Use
your judgement based on what you actually see in the source.

| If the project has…                    | It has these layers               |
|----------------------------------------|-----------------------------------|
| Views, Pages, Components, Routes       | `ui/`                             |
| Controllers, API routes, Middleware    | `api/` or `api/{service}/`        |
| Service classes, Business logic, Jobs  | `services/`                       |
| Entities, Migrations, Seed data        | `data/`                           |
| Infrastructure config, CI/CD, Deploy   | `infra/`                          |

Projects can have one or many layers. A full-stack app has all of them. A
database-only project may only have `data/`. A frontend-only SPA may only have
`ui/`. Never invent layers that don't exist in the source.

Record your findings: this determines which directories the bundle needs.

#### Step 3 — Map source hierarchy to bundle paths

**The path of a concept inside the bundle MUST mirror its meaningful location
inside the source tree.** Do not flatten.

Rules:

- Drop the language- or framework-specific top-level prefix (e.g. `src/`,
  `app/`, `lib/`, `MyApp.UI/`, `MyApp.API/`).
- Keep the meaningful hierarchy below that. Every subdirectory level in the
  source produces one subdirectory level in the bundle.
- Use lowercase with hyphens for all directory and file names in the bundle.
- Map framework-specific naming to OKF-standard form (e.g. `Login.cshtml` →
  `login.md`, `OrdersController.cs` → `orders-controller.md`).

Examples:

| Source file                                              | Bundle path                                    |
|----------------------------------------------------------|------------------------------------------------|
| `src/MyApp.UI/Pages/Account/Login.cshtml`                | `.okf/ui/pages/account/login.md`               |
| `src/MyApp.UI/Components/Navbar.razor`                   | `.okf/ui/components/navbar.md`                 |
| `src/MyApp.API/Controllers/OrdersController.cs`          | `.okf/api/controllers/orders-controller.md`    |
| `src/MyApp.API/Middleware/RequestLogging.cs`             | `.okf/api/middleware/request-logging.md`       |
| `src/MyApp.Core/Services/PricingService.cs`              | `.okf/services/pricing-service.md`             |
| `src/MyApp.Core/Jobs/InvoiceReminderJob.cs`              | `.okf/services/jobs/invoice-reminder.md`       |
| `src/MyApp.Data/Entities/Order.cs`                       | `.okf/data/entities/order.md`                  |
| `src/MyApp.Data/Migrations/20240101_AddPendingOrders.cs` | `.okf/data/migrations/add-pending-orders.md`   |
| `database/schema/tables/orders.sql`                      | `.okf/data/tables/orders.md`                   |
| `database/schema/views/active_customers.sql`             | `.okf/data/views/active-customers.md`          |
| `database/stored_procedures/sp_calculate_totals.sql`     | `.okf/data/stored-procedures/calculate-totals.md` |
| `docker-compose.yml`                                     | `.okf/infra/docker-compose.md`                 |
| `.github/workflows/deploy.yml`                           | `.okf/infra/ci/deploy.md`                      |
| `terraform/modules/network/main.tf`                      | `.okf/infra/terraform/network.md`              |

**When a single source directory contains many files of the same kind**, group
them into one concept only when they form a natural unit (e.g. all migrations
could be one `migrations.md` if they're simple; split them if each has distinct
schema worth documenting). Prefer one-concept-per-file when each file is large
or semantically distinct.

#### Step 4 — Classify every concept by kind using the `type` field

The `type` frontmatter field distinguishes code-level artifacts from
process-level artifacts. Use the following taxonomy:

**Layer-specific code types** — for concepts bound to actual source files:

| Layer        | Valid `type` values                                                   |
|--------------|-----------------------------------------------------------------------|
| `ui/`        | `Page`, `Component`, `Layout`, `Route`, `Hook`, `Store`, `Style`     |
| `api/`       | `Controller`, `Endpoint`, `Middleware`, `DTO`, `Guard`, `Route`      |
| `services/`  | `Service`, `Background Job`, `Event Handler`, `Publisher`            |
| `data/`      | `Table`, `View`, `Stored Procedure`, `Migration`, `Index`, `Trigger`, `Seed`, `Entity` |
| `infra/`     | `Deployment`, `CI Pipeline`, `Docker`, `Terraform`, `Config`         |

**Cross-cutting concept types** — for knowledge artifacts not bound to a
specific source file:

| Directory         | Valid `type` values                                                   |
|-------------------|-----------------------------------------------------------------------|
| `processes/`      | `Process`, `Playbook`, `On-Call`, `Workflow`, `SOP`                  |
| `decisions/`      | `Decision`, `ADR`                                                     |
| `architecture/`   | `Architecture`, `Diagram`, `Overview`, `ADR`                          |
| `metrics/`        | `Metric`, `KPI`, `Dashboard`                                          |
| `references/`     | `Reference`, `Guide`, `FAQ`                                           |

**Always set a `type` that reflects what a concept IS, not where it lives.**
A `Page` type belongs in `ui/` but could also exist in `processes/` if it
describes a process for pages. Be honest about the distinction — code types
for files in the repository, process types for how-things-work knowledge.

#### Step 5 — Write each concept

For each file identified in Step 3:

1. Copy [templates/concept.md](templates/concept.md) as your starting shell.
2. Set `type` using the taxonomy in Step 4.
3. Set `title` to the readable name of the artifact.
4. Set `description` to a single sentence summarising what it is/does.
5. Set `tags` for cross-cutting categorisation.
6. Set `timestamp` to the current ISO 8601 datetime.
7. Use bundle-relative cross-links (`/ui/pages/login.md`) to connect related
   concepts — every relationship in the source code should have a corresponding
   link in the bundle.
8. If the concept describes a data asset (table, view, DTO), include a
   `# Schema` section with a markdown table of fields/columns.
9. If it depends on or is called by other concepts, include a `# Dependencies`
   or `# Consumers` section linking to them.

#### Step 6 — Create directory indices

Every directory MUST have an `index.md` (the bundle-root index is the project
overview; subdirectory indices list concepts within that group).

Use [templates/index.md](templates/index.md):

```markdown
# Directory Name

* [Concept Title](concept-path) — description
* [Another Concept](other-path) — description
```

The bundle-root `index.md` is special: it may include `okf_version: "0.1"`
in its YAML frontmatter (the only `index.md` that carries frontmatter). It
should list every top-level directory with a one-line description of what
lives there, plus any concepts filed at bundle root (there shouldn't be any
by the rules above).

#### Step 7 — Update the log

Append a dated entry to `log.md` (ISO 8601 date heading, newest first):

```markdown
## 2026-07-09
* **Creation**: Initial OKF knowledge bundle for the Razor Pages project.
  Documented 12 UI pages across Account, Orders, and Admin sections.
* **Creation**: Added API layer: 3 controllers, 2 middleware concepts.
* **Creation**: Data layer: 5 entity types, 8 migrations.
```

#### Step 8 — Validate

Run the deterministic checker. See the [Validation](#validation) section below.
Fix every ERROR before finishing.

---

### Example: what a full-stack .NET project bundle looks like

```
.okf/
├── index.md                    # Project overview, layers listed
├── log.md                      # Changelog
├── ui/
│   ├── index.md                # UI overview
│   ├── pages/
│   │   ├── index.md
│   │   ├── account/
│   │   │   ├── index.md
│   │   │   ├── login.md        # type: Page
│   │   │   └── register.md     # type: Page
│   │   ├── orders/
│   │   │   ├── index.md
│   │   │   ├── list.md         # type: Page
│   │   │   └── detail.md       # type: Page
│   │   └── admin/
│   │       └── dashboard.md    # type: Page
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
│   ├── entities/
│   │   ├── index.md
│   │   ├── order.md               # type: Entity
│   │   └── customer.md            # type: Entity
│   └── migrations.md              # type: Migration (single file for all)
├── processes/
│   ├── index.md
│   └── order-fulfillment.md       # type: Process
├── decisions/
│   ├── index.md
│   └── use-blazor-over-mvc.md     # type: ADR
└── infra/
    ├── index.md
    ├── docker-compose.md          # type: Docker
    └── ci/
        ├── index.md
        └── deploy.md              # type: CI Pipeline
```

### Example: what a database-only bundle looks like

```
.okf/
├── index.md                      # Database project overview
├── log.md
├── data/
│   ├── index.md
│   ├── tables/
│   │   ├── index.md
│   │   ├── orders.md             # type: Table
│   │   └── customers.md          # type: Table
│   ├── views/
│   │   ├── index.md
│   │   └── active-customers.md   # type: View
│   └── stored-procedures/
│       ├── index.md
│       └── calculate-totals.md   # type: Stored Procedure
├── processes/
│   ├── index.md
│   └── nightly-batch.md          # type: Process
└── decisions/
    ├── index.md
    └── partitioning-strategy.md  # type: ADR
```

### produce — key anti-patterns to avoid

| ❌ Don't do this                                      | ✅ Do this instead                                  |
|-------------------------------------------------------|-----------------------------------------------------|
| File concept directly at `.okf/login.md`              | `.okf/ui/pages/account/login.md`                    |
| Dump all database concepts in `.okf/databases.md`     | `.okf/data/tables/orders.md`, `.okf/data/views/…`  |
| Use generic `type: Document` or no type               | `type: Page`, `type: Controller`, `type: Table`     |
| Put a runbook in `ui/` just because it's about a page | Put it in `processes/` with `type: Playbook`        |
| Flatten everything into one directory                 | Mirror source hierarchy with subdirectories         |
| Name files `OrdersController.cshtml.md`               | Name files `orders-controller.md`                   |

### maintain — keep a bundle in sync with reality

1. Identify which concepts the change affects (search by `resource`, path, or
   topic). This bookkeeping is exactly what agents are good at — touch every
   affected file in one pass.
2. Update the body and `timestamp`; fix or add cross-links; create new concepts
   for new assets; mark removed assets (`**Deprecation**`) rather than silently
   deleting context.
3. Update the relevant `index.md` files and append a dated `log.md` entry
   describing what changed.
4. Validate.

### consume — use a bundle as context

1. Read the bundle-root `index.md` first for progressive disclosure, then follow
   links only into the concepts relevant to the task.
2. Treat broken links as not-yet-written knowledge, not errors.
3. If you learn something durable while working, switch to **maintain** and
   write it back.

## Validation (do this before declaring done)

Never eyeball conformance — run the deterministic checker. Invoke the companion
**`validate`** skill, which ships the checker.

```bash
SCRIPT_DIR="$(cd "$(dirname "$0")/../validate/scripts" && pwd)"
uv run "${SCRIPT_DIR}/okf_validate.py" <bundle-dir> --strict
```

Resolve every `ERROR` (hard §9 failures). Warnings are soft; fix them when cheap,
but they never block.
