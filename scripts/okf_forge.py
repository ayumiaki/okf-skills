#!/usr/bin/env python3
"""okf_forge.py — one-shot OKF bundle scaffolder.

Usage:
    uv run scripts/okf_forge.py .okf --title "My project" [--link URL] [--layers ui,api,services,data,processes,decisions,infra]

Creates a spec-compliant .okf/ bundle skeleton matching the project's layers.
By default scaffolds ALL layer directories; pass --layers to restrict to what
your project actually has (e.g. --layers ui,api for a frontend+API project).

Every concept file gets minimal YAML frontmatter with a non-empty `type` so it
passes strict validator immediately.
"""

from __future__ import annotations

import argparse
import datetime
import os
import textwrap
from pathlib import Path


def slugify(text: str) -> str:
    return text.strip().lower().replace(" ", "-")


def concept_frontmatter(kind: str, title: str) -> str:
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return textwrap.dedent(f"""\
    ---
    type: {kind}
    title: {title}
    description: TODO — add a one-line description.
    tags: []
    timestamp: {now}
    ---

    # {title}
    """)


# Layer definition: (directory, type for sample concept, frontmatter type family, description)
LAYERS = {
    "ui": {
        "type": "Page",
        "subdirs": ["pages", "components", "layouts"],
        "desc": "UI pages, components, layouts, and routes",
    },
    "api": {
        "type": "Controller",
        "subdirs": ["controllers", "middleware", "dto"],
        "desc": "API endpoints, controllers, middleware, and DTOs",
    },
    "services": {
        "type": "Service",
        "subdirs": ["jobs"],
        "desc": "Business logic, service classes, background jobs",
    },
    "data": {
        "type": "Table",
        "subdirs": ["tables", "views", "stored-procedures", "migrations", "entities"],
        "desc": "Database schemas, tables, views, and entities",
    },
    "processes": {
        "type": "Process",
        "subdirs": [],
        "desc": "Business workflows, runbooks, playbooks, and SOPs",
    },
    "decisions": {
        "type": "ADR",
        "subdirs": [],
        "desc": "Architecture Decision Records and design decisions",
    },
    "infra": {
        "type": "Deployment",
        "subdirs": ["ci", "terraform", "docker"],
        "desc": "Infrastructure, CI/CD pipelines, Docker, Terraform",
    },
}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def index_md(title: str, items: list[str]) -> str:
    bullets = "\n".join(f"* [{t}]({p})" for p, t in items)
    return textwrap.dedent(f"""\
    # {title}

    {bullets}
    """)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new OKF bundle.")
    parser.add_argument("bundle_dir", type=Path, help="Target directory (e.g. .okf)")
    parser.add_argument("--title", required=True, help="Project title")
    parser.add_argument("--link", default="", help="Optional back-link to source repo")
    parser.add_argument(
        "--layers",
        default=",".join(LAYERS.keys()),
        help=f"Comma-separated layers to scaffold. Options: {','.join(LAYERS.keys())}",
    )
    args = parser.parse_args()

    bundle = args.bundle_dir.resolve()
    if bundle.exists() and any(bundle.iterdir()):
        print(f"Refusing to overwrite non-empty directory: {bundle}", flush=True)
        return 1

    title = args.title.strip()
    title_slug = slugify(title)
    link_line = f"[Source]({args.link})\\n" if args.link else ""

    selected = [s.strip() for s in args.layers.split(",") if s.strip() in LAYERS]
    if not selected:
        print(f"Error: no valid layers specified. Choose from: {','.join(LAYERS.keys())}", flush=True)
        return 1

    # Root index with okf_version frontmatter
    layer_links = "\n".join(
        f"- [{LAYERS[l]['desc']}]({l}/index.md)"
        for l in selected
    )
    write(
        bundle / "index.md",
        textwrap.dedent(f"""\
        ---
        okf_version: "0.1"
        title: {title}
        description: TODO — one-line summary of this project.
        {link_line}---
        # {title}

        ## Layers

        {layer_links}
        """),
    )

    # log.md
    write(
        bundle / "log.md",
        textwrap.dedent(f"""\
        # {title} — OKF log

        ISO-dated entries, newest first.

        ## {datetime.date.today().isoformat()}

        - Bootstrap created by `okf_forge.py`.
        """),
    )

    # Scaffold each selected layer
    for layer_name in selected:
        layer = LAYERS[layer_name]
        subdirs = layer["subdirs"]

        # Layer index
        subdir_links = "\n".join(
            f"* [{s.capitalize()}]({s}/index.md)"
            for s in subdirs
        )
        write(
            bundle / layer_name / "index.md",
            textwrap.dedent(f"""\
            # {layer_name.capitalize()}

            {layer['desc']}.

            {subdir_links}

            * [{title} example]({title_slug}-{layer_name}.md)
            """),
        )

        # Sample concept at layer root
        write(
            bundle / layer_name / f"{title_slug}-{layer_name}.md",
            concept_frontmatter(layer["type"], f"{title} — example {layer_name} concept"),
        )

        # Scaffold subdirectories
        for sub in subdirs:
            write(
                bundle / layer_name / sub / "index.md",
                textwrap.dedent(f"""\
                # {sub.capitalize()}

                _Add {layer_name} {sub} concepts here._

                * [{title} example]({title_slug}-{sub}.md)
                """),
            )
            write(
                bundle / layer_name / sub / f"{title_slug}-{sub}.md",
                concept_frontmatter(layer["type"], f"{title} — {sub} example"),
            )

    print(f"OKF bundle created at {bundle}", flush=True)
    print(f"  Layers: {', '.join(selected)}", flush=True)
    print("Next steps:", flush=True)
    print(f"  uv run skills/validate/scripts/okf_validate.py {bundle} --strict", flush=True)
    print(f"  uv run skills/visualize/scripts/okf_visualize.py \\", flush=True)
    print(f"    {bundle} -o viz.html --title \"{title}\"", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
