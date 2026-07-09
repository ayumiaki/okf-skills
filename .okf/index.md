---
okf_version: "0.1"
---

# okf-skills — documented in its own format

This is the [okf-skills](https://github.com/ayumiaki/okf-skills) repository
described as an OKF bundle — the toolkit eating its own dog food. Render it with
`uv run skills/visualize/scripts/okf_visualize.py .okf -o viz.html --title "OKF Skills"`.

# Skills

* [okf skill](skills/okf.md) — produce / maintain / consume bundles, now with prescriptive multi-layer produce mode.
* [validate skill](skills/validate.md) — deterministic §9 conformance check.
* [visualize skill](skills/visualize.md) — render a bundle to an interactive graph.

# Components

* [okf_validate.py](components/validator.md) — the conformance checker.
* [okf_visualize.py](components/visualizer.md) — the graph renderer.
* [okf_forge.py](components/forge.md) — the bootstrap scaffolder.
* [CI pipeline](components/ci-pipeline.md) — the quality gate workflow.

# Reference

* [OKF v0.1 specification](reference/okf-spec.md) — the vendored source of truth.

# Decisions

* [Dual distribution — plugin + skills.sh](decisions/dual-distribution.md)
* [Ship no hooks — soft-mode upkeep](decisions/no-hooks.md)
* [Self-contained skills via CLAUDE_SKILL_DIR](decisions/self-contained-skills.md)
* [Prescriptive produce mode — structured bundles by architecture](decisions/prescriptive-bundles.md)
* [CI quality gate — strict validation on push](decisions/ci-quality-gate.md)
