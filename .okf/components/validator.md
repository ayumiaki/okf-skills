---
type: Tool
title: okf_validate.py
description: Zero-config Python conformance checker (PEP 723 / uv, PyYAML).
resource: https://github.com/ayumiaki/okf-skills/blob/main/skills/validate/scripts/okf_validate.py
tags: [python, validator, uv]
timestamp: "2026-06-28T00:00:00Z"
---

# Overview

The deterministic engine behind the [validate skill](/skills/validate.md). A
single self-describing script (dependencies declared inline via PEP 723) that
parses every non-reserved `.md` file and enforces the one hard rule of the
[OKF v0.1 spec](/reference/okf-spec.md): parseable YAML frontmatter with a
non-empty `type`.

# Output

| Signal | Meaning |
|--------|---------|
| `ERROR` | Hard §9 failure — bundle is non-conformant. |
| `warn`  | Soft guidance (missing recommended field, broken link). |

Exit code is non-zero on any error (or any warning with `--strict`). `--json` emits
machine-readable output for CI.

# Example output

```json
{
  "path": ".okf",
  "conformant": true,
  "strict": true,
  "errors": [],
  "warnings": [
    {
      "file": "skills/okf.md",
      "field": "timestamp",
      "message": "Missing recommended field 'timestamp'",
      "line": 6
    }
  ],
  "files_checked": 12,
  "duration_ms": 4
}
```

# Usage

```shell
# Basic conformance check
uv run skills/validate/scripts/okf_validate.py .okf

# Strict mode — warnings become failures
uv run skills/validate/scripts/okf_validate.py .okf --strict

# Machine-readable for CI
uv run skills/validate/scripts/okf_validate.py .okf --strict --json > report.json
```

The [validate skill](/skills/validate.md) wraps this script with environment-aware
path resolution; the [CI pipeline](/components/ci-pipeline.md) uses `--json` output
for its report.

# Citations

[1] [okf_validate.py source](https://github.com/ayumiaki/okf-skills/blob/main/skills/validate/scripts/okf_validate.py)
[2] [OKF v0.1 §9 — Conformance](/reference/okf-spec.md#9-conformance)

