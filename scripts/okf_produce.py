#!/usr/bin/env python3
"""okf_produce.py — Analyse a source tree and produce an OKF bundle.

Scans a project directory, identifies meaningful source artifacts by their
file extensions and path patterns, classifies them into the prescribed layer
taxonomy, and generates spec-conformant concept files for each.

Usage:
    uv run scripts/okf_produce.py /path/to/project .okf
    uv run scripts/okf_produce.py /path/to/project .okf --dry-run
    uv run scripts/okf_produce.py /path/to/project .okf --incremental

Output:
    A spec-conformant .okf/ bundle with concept files, directory indices,
    and an updated log.md. Human agents should enrich the generated
    concept bodies (this script populates frontmatter from file metadata
    and writes a stub body).
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import textwrap
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ── Layer taxonomy ──────────────────────────────────────────────────────────

@dataclass
class LayerDef:
    directory: str         # e.g. "ui"
    type_label: str        # e.g. "Page"
    description: str       # e.g. "UI pages and components"
    file_patterns: list[tuple[str, str]] = field(default_factory=list)
    """(glob, optional subdir tag override) pairs. First match wins."""


LAYERS: list[LayerDef] = [
    LayerDef("ui", "Page", "UI pages, components, layouts",
        file_patterns=[
            (r"\.(tsx|jsx|svelte|vue|astro)$", "Component"),
            (r"/(pages|views|screens)/", "Page"),
            (r"/(components|ui)/", "Component"),
            (r"\.(css|scss|less|tailwind|styles?)\.(ts|js)$", "Style"),
        ]),
    LayerDef("api", "Controller", "API endpoints, controllers, middleware",
        file_patterns=[
            (r"/(controllers?|routes?|endpoints?|handlers?)/", "Controller"),
            (r"/(middleware|interceptors?|filters?)/", "Middleware"),
            (r"/(dto|validators?|requests?)/", "DTO"),
            (r"\.(controller|route|handler|resolver)\.(ts|js)$", "Controller"),
        ]),
    LayerDef("services", "Service", "Business logic, service classes, background jobs",
        file_patterns=[
            (r"/(services?|lib|logic|domain)/", "Service"),
            (r"\.(service|use.?case)\.(ts|js|py)$", "Service"),
            (r"/(jobs?|tasks?|workers?|queues?)/", "Job"),
            (r"\.(job|task|worker)\.(ts|js|py)$", "Job"),
            # Generic code catch-all — any source file that didn't match a
            # more specific layer pattern lands here as a GenericService
            (r"\.(py|rb|go|rs|java|kt|scala|swift|c|cpp|ts|js|mjs|cjs)$", "GenericService"),
        ]),
    LayerDef("data", "Table", "Database schemas, tables, views, entities",
        file_patterns=[
            (r"/(models?|entities?|schemas?|types?)/", "Entity"),
            (r"\.(model|entity)\.(ts|js|py)$", "Entity"),
            (r"\.(prisma|sql)$", "Schema"),
            (r"/(migrations?)/", "Migration"),
        ]),
    LayerDef("infra", "Deployment", "Infrastructure, CI/CD, Docker, Terraform",
        file_patterns=[
            (r"(^|/)Dockerfile", "Container"),
            (r"\.(tf|tfvars)$", "Terraform"),
            (r"/(ci|cd|actions?|workflows?)/", "Pipeline"),
            (r"\.ya?ml$", "Config"),  # catch-all for infra configs
            (r"(^|/)docker-compose", "Container"),
        ]),
    LayerDef("processes", "Process", "Business workflows, runbooks, playbooks",
        file_patterns=[
            (r"/(runbooks?|playbooks?|sops?)/", "Playbook"),
            (r"/docs?/runbook", "Playbook"),
        ]),
    LayerDef("decisions", "ADR", "Architecture Decision Records",
        file_patterns=[
            (r"/(adr|decisions?)/", "ADR"),
            (r"\.adr\.md$", "ADR"),
        ]),
]

# Default excluded directories / patterns
EXCLUDE_DIRS = {
    ".git", ".svn", "__pycache__", "node_modules", ".venv",
    ".hermes", ".claude", ".cursor", ".windsurf",
    "dist", "build", ".next", ".nuxt", "out", "target",
    "coverage", ".nyc_output", ".tox", ".eggs",
}

EXCLUDE_FILES = {
    ".DS_Store", "thumbs.db", ".gitkeep", ".gitignore",
}

# Types that belong to process artifacts (cross-cutting)
PROCESS_TYPES = {"Process", "Playbook", "Runbook", "ADR", "Metric"}


# ── Discovery ───────────────────────────────────────────────────────────────

@dataclass
class Artifact:
    rel_path: str          # e.g. "api/controllers/auth.ts"
    layer: str             # e.g. "api"
    subdir: str            # e.g. "controllers"
    type_label: str        # e.g. "Controller"
    title: str             # Human-readable title
    basename: str          # e.g. "auth"
    source_path: str       # Absolute path to source file


def is_code_file(path: Path) -> bool:
    """Return True if the file extension looks like a code or doc artifact.

    Markdown files pass this gate but are further filtered by classify_file()
    — only ADRs, runbooks, and similar pattern-matched docs become artifacts.
    """
    ext = path.suffix.lower()
    return ext in {
        ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
        ".py", ".rb", ".go", ".rs", ".java", ".kt", ".scala",
        ".swift", ".c", ".cpp", ".h", ".hpp",
        ".sql", ".prisma",
        ".tf", ".tfvars",
        ".yaml", ".yml", ".json", ".toml",
        ".css", ".scss", ".less", ".svelte", ".vue", ".astro",
        ".html", ".md",
        ".dockerfile", "dockerfile",
    }


def classify_file(rel_path: str) -> Optional[Artifact]:
    """Given a relative source path, classify it into a layer and subtype."""
    p = Path(rel_path)
    if p.name.lower() in EXCLUDE_FILES:
        return None

    # Normalise to forward slashes for pattern matching
    normalised = rel_path.replace("\\", "/")
    is_md = p.suffix.lower() == ".md"

    # Markdown files are only accepted via specific path patterns (ADRs, runbooks)
    # not via generic extension fallback. Check the layer-specific patterns first.
    if is_md:
        # Only match .md files against decisions/ and processes/ layer patterns
        md_layers = [l for l in LAYERS if l.directory in ("decisions", "processes")]
        for layer in md_layers:
            for pattern, type_label in layer.file_patterns:
                if re.search(pattern, normalised, re.IGNORECASE):
                    slug = slugify(p.stem)
                    parts = normalised.split("/")
                    subdir = parts[1] if len(parts) > 1 else ""
                    return Artifact(
                        rel_path=normalised,
                        layer=layer.directory,
                        subdir=subdir,
                        type_label=type_label,
                        title=humanise(p.stem),
                        basename=slug,
                        source_path="",
                    )
        # Non-ADR/runbook .md files are skipped
        return None

    for layer in LAYERS:
        for pattern, type_label in layer.file_patterns:
            if re.search(pattern, normalised, re.IGNORECASE):
                slug = slugify(p.stem)
                # Extract subdir: the first path component after the layer match
                parts = normalised.split("/")
                subdir = parts[1] if len(parts) > 1 else ""
                return Artifact(
                    rel_path=normalised,
                    layer=layer.directory,
                    subdir=subdir,
                    type_label=type_label,
                    title=humanise(p.stem),
                    basename=slug,
                    source_path="",
                )

    # Fallback: match by extension only (weaker)
    ext = p.suffix.lower()
    for layer in LAYERS:
        for pattern, type_label in layer.file_patterns:
            if pattern.startswith("\\.") and pattern.endswith("$"):
                # Pure extension pattern like r"\.(tsx|jsx)$"
                if re.match(pattern, ext, re.IGNORECASE):
                    slug = slugify(p.stem)
                    parts = normalised.split("/")
                    subdir = parts[1] if len(parts) > 1 else ""
                    return Artifact(
                        rel_path=normalised,
                        layer=layer.directory,
                        subdir=subdir,
                        type_label=type_label,
                        title=humanise(p.stem),
                        basename=slug,
                        source_path="",
                    )

    # No classification — skip
    return None


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.strip().lower()).strip("-")


def humanise(name: str) -> str:
    """Convert a file/camelCase name to a readable title."""
    # Remove common extensions
    stem = re.sub(r"\.[^.]+$", "", name)
    # Split on capitals, underscores, hyphens
    words = re.split(r"[_\-]+|(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", stem)
    return " ".join(w.capitalize() for w in words if w).strip()


def discover_source(
    source_dir: Path,
    incremental: bool = False,
    existing_bundle: Optional[Path] = None,
) -> list[Artifact]:
    """Walk source_dir, classify every file, return artifact list."""
    artifacts: list[Artifact] = []
    existing_names: set[str] = set()

    if incremental and existing_bundle and existing_bundle.exists():
        # Collect concept filenames already in the bundle to avoid duplicates
        for f in existing_bundle.rglob("*.md"):
            if f.name not in ("index.md", "log.md"):
                existing_names.add(f.stem)

    for root, dirs, files in os.walk(source_dir):
        # Prune excluded directories (mutating dirs in-place)
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]

        for fname in sorted(files):
            fpath = Path(root) / fname
            if not is_code_file(fpath):
                continue

            rel = fpath.relative_to(source_dir).as_posix()
            artifact = classify_file(rel)
            if artifact is None:
                continue

            # Set absolute source path
            artifact.source_path = str(fpath.resolve())

            # In incremental mode, skip if already in bundle
            if incremental and artifact.basename in existing_names:
                continue

            artifacts.append(artifact)

    return artifacts


# ── Generation ──────────────────────────────────────────────────────────────

def concept_frontmatter(artifact: Artifact, now: str) -> str:
    """Generate frontmatter + stub body for an artifact."""
    tags = [artifact.layer, artifact.type_label.lower()]
    if artifact.subdir:
        tags.append(artifact.subdir.lower())
    # Remove duplicates preserving order
    tags = list(dict.fromkeys(tags))
    tag_str = ", ".join(tags)

    # Build the string without relying on textwrap.dedent
    parts = [
        "---",
        f"type: {artifact.type_label}",
        f"title: {artifact.title}",
        f"description: TODO -- describe the {artifact.layer} artifact `{artifact.rel_path}`.",
        f"resource: {artifact.source_path}",
        f"tags: [{tag_str}]",
        f"timestamp: {now}",
        "---",
        "",
        f"# {artifact.title}",
        "",
        "## Overview",
        "",
        f"_Auto-generated by `okf_produce.py`. Enrich with purpose, key methods/endpoints/fields, and relationships via markdown links._",
        "",
    ]
    return "\n".join(parts) + "\n"


def index_md(title: str, entries: list[tuple[str, str, str]]) -> str:
    """Generate an index.md with bulleted links.
    entries: list of (basename, title, description)
    """
    if not entries:
        return textwrap.dedent(f"""\
        # {title}

        _(Empty — add concepts here.)_
        """)
    bullets = "\n".join(
        f"* [{t}]({b}.md)" + (f" — {d}" if d else "")
        for b, t, d in entries
    )
    return textwrap.dedent(f"""\
    # {title}

    {bullets}
    """)


def generate_bundle(
    artifacts: list[Artifact],
    bundle_dir: Path,
    title: str,
    link: str = "",
    dry_run: bool = False,
) -> int:
    """Generate or update an OKF bundle from discovered artifacts."""
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    today = datetime.date.today().isoformat()
    link_line = f"source: {link}\n" if link else ""

    # Group artifacts flat by layer (no subdir nesting)
    by_layer: dict[str, list[Artifact]] = defaultdict(list)
    for art in artifacts:
        by_layer[art.layer].append(art)

    if not by_layer:
        print("No classifiable source artifacts found in the given path.", flush=True)
        return 1

    # ── Write bundle ────────────────────────────────────────────────────
    def write(path: Path, content: str) -> None:
        if dry_run:
            print(f"  [dry-run] would write: {path.relative_to(bundle_dir)}", flush=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    bundle_dir.mkdir(parents=True, exist_ok=True)

    # Root index.md
    layer_links = "\n".join(
        f"* [{LAYER_DESC.get(l, l.capitalize())}]({l}/index.md)"
        for l in sorted(by_layer.keys())
    )
    write(
        bundle_dir / "index.md",
        textwrap.dedent(f"""\
        ---
        okf_version: "0.1"
        ---

        # {title}

        OKF bundle produced from source analysis of **{title}**.

        {link_line}## Layers

        {layer_links}
        """),
    )

    # log.md
    log_entry = textwrap.dedent(f"""\
    # Update Log

    ## {today}

    * **Produce**: Auto-generated by `okf_produce.py` from source analysis.
      {len(artifacts)} artifacts classified across {len(by_layer)} layers.

    """)
    log_path = bundle_dir / "log.md"
    if log_path.exists():
        existing_log = log_path.read_text(encoding="utf-8")
        lines = existing_log.split("\n", 1)
        header = lines[0]
        rest = lines[1] if len(lines) > 1 else ""
        log_content = f"{header}\n\n{log_entry.strip()}\n\n{rest}".strip() + "\n"
    else:
        log_content = f"# Update Log\n\n{log_entry}"
    write(log_path, log_content)

    # Per-layer files — ALL artifacts written directly in layer root
    for layer_name in sorted(by_layer.keys()):
        arts = sorted(by_layer[layer_name], key=lambda a: a.basename)
        layer_dir = bundle_dir / layer_name
        layer_desc = LAYER_DESC.get(layer_name, layer_name.capitalize())
        layer_entries: list[tuple[str, str, str]] = []

        for art in arts:
            # Write concept file directly at layer root
            write(
                layer_dir / f"{art.basename}.md",
                concept_frontmatter(art, now),
            )
            layer_entries.append((art.basename, art.title, ""))

        write(
            layer_dir / "index.md",
            index_md(layer_desc, layer_entries),
        )

    if dry_run:
        print(f"\n[dry-run] would create {len(artifacts)} concepts in {bundle_dir}", flush=True)
    else:
        print(
            f"OKF bundle produced at {bundle_dir}: "
            f"{len(artifacts)} artifacts, {len(by_layer)} layers.",
            flush=True,
        )
        print("Next step: validate with `okf_validate.py --strict`.", flush=True)
    return 0


LAYER_DESC = {
    "ui": "UI pages and components",
    "api": "API endpoints and controllers",
    "services": "Business logic services",
    "data": "Database schemas and entities",
    "infra": "Infrastructure config",
    "processes": "Runbooks and playbooks",
    "decisions": "Architecture decision records",
}


# ── CLI ─────────────────────────────────────────────────────────────────────

def dump_json(artifacts: list[Artifact]) -> None:
    """Emit discovered artifacts as JSON for pipeline consumption."""
    payload = [
        {
            "rel_path": a.rel_path,
            "layer": a.layer,
            "type": a.type_label,
            "title": a.title,
            "basename": a.basename,
        }
        for a in sorted(artifacts, key=lambda x: x.rel_path)
    ]
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyse a source tree and produce an OKF bundle."
    )
    parser.add_argument("source", type=Path, help="Source project directory to analyse")
    parser.add_argument("bundle_dir", type=Path, nargs="?", default=".okf",
                        help="Target bundle directory (default: .okf)")
    parser.add_argument("--title", default="Untitled project",
                        help="Project title for the bundle")
    parser.add_argument("--link", default="",
                        help="Optional source repo URL")
    parser.add_argument("--incremental", action="store_true",
                        help="Only add new/changed files; don't regenerate existing concepts")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be written without writing anything")
    parser.add_argument("--json", action="store_true", dest="emit_json",
                        help="Instead of writing a bundle, emit the artifact manifest as JSON")
    args = parser.parse_args()

    if not args.source.is_dir():
        print(f"Error: source path is not a directory: {args.source}", flush=True)
        return 1

    # Discover
    print(f"Scanning {args.source} ...", flush=True)
    artifacts = discover_source(
        args.source,
        incremental=args.incremental,
        existing_bundle=args.bundle_dir if args.incremental else None,
    )

    if not artifacts:
        print("No classifiable source artifacts found.", flush=True)
        return 0

    print(f"  Found {len(artifacts)} classifiable artifacts.", flush=True)

    if args.emit_json:
        dump_json(artifacts)
        return 0

    # Generate bundle
    return generate_bundle(
        artifacts,
        args.bundle_dir.resolve(),
        title=args.title,
        link=args.link,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    raise SystemExit(main())
