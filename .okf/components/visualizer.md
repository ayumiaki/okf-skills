---
type: Tool
title: okf_visualize.py
description: Standalone bundle→viz.html renderer (Cytoscape + marked via CDN).
resource: https://github.com/ayumiaki/okf-skills/blob/main/skills/visualize/scripts/okf_visualize.py
tags: [python, visualization, cytoscape]
timestamp: "2026-06-28T00:00:00Z"
---

# Overview

The engine behind the [visualize skill](/skills/visualize.md). Parses a bundle
into nodes (concepts, coloured by `type`, sized by body length) and edges
(markdown links), then emits one self-contained HTML file — no backend, nothing
leaves the page.

# Flags

| Flag | Effect |
|------|--------|
| `--title` / `--link` | Name the graph; show a back-link to source. |
| `--layout` | Initial layout (`cose`, `breadthfirst`, `circle`, …). |
| `--og-image` | Emit Open Graph / Twitter Card meta for rich link previews. |

Also supports `?layout=` / `?select=` URL params and deep-linkable concepts
(`viz.html#services/auth-api`).

# Example

```shell
uv run skills/visualize/scripts/okf_visualize.py .okf \
  -o docs/self.html \
  --title "okf-skills" \
  --layout breadthfirst \
  --link "https://github.com/ayumiaki/okf-skills"
```

This produces a self-contained HTML page where:
- Each concept is a coloured node (colour = `type`)
- Markdown links between concepts become directed edges
- Clicking a node opens a detail panel with rendered markdown, metadata table,
  and "Links to / Cited by" backlinks
- The URL hash updates so any concept is shareable by deep link
- The `--og-image` flag embeds Open Graph meta for rich link previews when shared

# Citations

[1] [okf_visualize.py source](https://github.com/ayumiaki/okf-skills/blob/main/skills/visualize/scripts/okf_visualize.py)
[2] [Cytoscape.js docs](https://js.cytoscape.org/)
[3] [marked markdown renderer](https://marked.js.org/)

