---
name: visualize
description: >-
  Render an Open Knowledge Format (OKF) bundle as a single self-contained,
  interactive HTML graph (viz.html) — concepts as nodes coloured/sized by type,
  markdown links as edges, a wiki-style detail panel with rendered markdown plus
  "Links to" / "Cited by" backlinks, layout switching, per-type filter and search.
  Use when asked to visualize, graph, preview, or explore an OKF bundle.
user-invocable: true
argument-hint: "[bundle-dir] [-o viz.html]"
allowed-tools: Bash
---

# Visualize an OKF bundle

Generate a self-contained HTML graph of the target bundle (default the project's
`.okf/`). No backend, no install on the viewing side, no data leaves the page.

```bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
uv run "${SCRIPT_DIR}/okf_visualize.py" $ARGUMENTS
```

If `uv` is unavailable:

```bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 -m pip install --quiet pyyaml && \
python3 "${SCRIPT_DIR}/okf_visualize.py" $ARGUMENTS
```

The script is self-locating using `$0`, so it works whether installed as a
plugin, skills.sh skill, or manual copy to any agent's tools directory.
