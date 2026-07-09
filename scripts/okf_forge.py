#!/usr/bin/env python3
"""okf_forge.py — one-shot OKF bundle scaffolder.

Usage:
    uv run scripts/okf_forge.py <bundle_dir> --title "My project" [--link URL]

Creates a spec-compliant .okf/ bundle skeleton:
    <bundle_dir>/
      index.md          # root progressive-disclosure index
      log.md            # ISO-dated change history (starts empty)
      services/
        index.md
        _template.md   # sample concept (Type, title, description, resource, tags)
      datasets/
        index.md
      decisions/
        index.md
      runbooks/
        index.md
      metrics/
        index.md

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


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new OKF bundle.")
    parser.add_argument("bundle_dir", type=Path, help="Target directory (e.g. .okf)")
    parser.add_argument("--title", required=True, help="Project title")
    parser.add_argument("--link", default="", help="Optional back-link to source repo")
    args = parser.parse_args()

    bundle = args.bundle_dir.resolve()
    if bundle.exists() and any(bundle.iterdir()):
        print(f"Refusing to overwrite non-empty directory: {bundle}", flush=True)
        return 1

    title = args.title.strip()
    link_line = f"[Source]({args.link})\n" if args.link else ""
    title_slug = slugify(title)

    # Root index with okf_version frontmatter (matches sample bundle shape)
    write(
        bundle / "index.md",
        textwrap.dedent(f"""\
        ---
        okf_version: "0.1"
        title: {title}
        description: TODO — one-line summary of this project.
        {link_line}---

        # {title}

        ## Concepts

        - [Services](services/index.md)
        - [Datasets](datasets/index.md)
        - [Decisions](decisions/index.md)
        - [Runbooks](runbooks/index.md)
        - [Metrics](metrics/index.md)
        """),
    )

    # log.md — no frontmatter (matches upstream sample-bundle shape; validator warns on frontmatter here)
    write(
        bundle / "log.md",
        textwrap.dedent(f"""\
        # {title} — OKF log

        ISO-dated entries, newest first.

        ## {datetime.date.today().isoformat()}

        - Bootstrap created by `okf_forge.py`.
        """),
    )

    cats = {
        "services": "Service",
        "datasets": "Dataset",
        "decisions": "Decision",
        "runbooks": "Runbook",
        "metrics": "Metric",
    }
    for folder, kind in cats.items():
        # Category index — no frontmatter, simple bullet list
        write(
            bundle / folder / "index.md",
            textwrap.dedent(f"""\
            # {kind}s

            _Add concepts here — one file per concept, path is its ID._

            * [{title} example]({title_slug}-template.md)
            """),
        )
        sample_name = f"{title_slug}-template"
        write(
            bundle / folder / f"{sample_name}.md",
            concept_frontmatter(kind, f"{title} — example {kind.lower()}"),
        )

    print(f"OKF bundle created at {bundle}", flush=True)
    print("Next steps:", flush=True)
    print(f"  uv run skills/validate/scripts/okf_validate.py {bundle} --strict", flush=True)
    print("  uv run skills/visualize/scripts/okf_visualize.py \\", flush=True)
    print(f"    {bundle} -o viz.html --title \"{title}\"", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
