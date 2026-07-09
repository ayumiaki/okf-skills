---
okf_version: "0.1"
---

# Storefront — Sample OKF Bundle

A small, conformant bundle that documents a fictional online store backend. It
shows the knowledge sources OKF targets — **code** (services, schema),
**curated decisions** (ADRs), and **operations** (runbooks, metrics) — and how
markdown links turn a folder of files into a navigable knowledge graph.

# Layers

This bundle demonstrates the recommended produce-mode taxonomy:

* [Services](services/) — business logic concepts (auth, orders, payments)
* [Data](data/) — database schemas and models
* [Decisions](decisions/) — architecture decision records
* [Processes](processes/) — operational runbooks
* [Metrics](metrics/) — business KPIs and measurements

| Render it yourself: `uv run skills/visualize/scripts/okf_visualize.py examples/sample-bundle`

# Services

* [Auth API](services/auth-api.md) — issues and verifies JWTs for the platform.
* [Orders API](services/orders-api.md) — owns the order lifecycle and checkout.
* [Payments API](services/payments-api.md) — captures charges and refunds.

# Data

* [Orders database](data/orders-db.md) — Postgres schema of record for orders and charges.

# Decisions

* [Adopt OKF for shared knowledge](decisions/use-okf.md) — why this repo uses OKF.
* [Event-driven service communication](decisions/event-driven.md) — why services publish events.

# Processes

* [Payment failures runbook](processes/payment-failures.md) — respond to a spike in failed charges.

# Metrics

* [Checkout conversion](metrics/checkout-conversion.md) — paid orders over started checkouts.
