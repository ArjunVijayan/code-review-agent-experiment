#!/usr/bin/env python3
"""Render a CodeReviewContext JSON document as review/review-context.md."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def inline(value: object) -> str:
    return str(value).replace("`", "' ")


def render(context: dict) -> str:
    repository = context["repository"]
    change = context["change"]
    change_request = context.get("change_request", {})
    lines = [
        "# Code Review Context",
        "",
        "## 1. Review Scope",
        "",
        f"- Base: `{inline(change['base'])}`",
        f"- Source: `{inline(change['source'])}`",
        f"- Merge Base: `{inline(change['merge_base'])}`",
        f"- PR/MR: `{inline(change_request.get('url', 'Not supplied'))}`",
        "",
        "## 2. Repository",
        "",
        f"- Root: `{inline(repository['root'])}`",
        f"- Files discovered: {len(repository.get('files', []))}",
        f"- Manifests: {', '.join(f'`{inline(path)}`' for path in repository.get('manifests', [])) or 'None found'}",
        "",
        "## 3. Change Statistics",
        "",
        f"- Files changed: {change.get('statistics', {}).get('files_changed', 0)}",
        f"- Insertions: {change.get('statistics', {}).get('insertions', 0)}",
        f"- Deletions: {change.get('statistics', {}).get('deletions', 0)}",
        "",
        "## 4. Changed Files",
        "",
    ]
    lines.extend(f"- `{inline(item['path'])}` ({item['status']})" for item in change["files"])
    if not change["files"]:
        lines.append("- No changed files")
    lines.extend(["", "## 5. Commit History", ""])
    for commit in context.get("history", {}).get("commits", []):
        lines.append(f"- `{commit['sha'][:12]}` {commit['subject']} ({commit['author']}, {commit['date']})")
    if not context.get("history", {}).get("commits"):
        lines.append("- No commits introduced by the source ref")
    lines.extend(["", "## 6. Repository Instructions", ""])
    for item in context.get("instructions", {}).get("files", []):
        lines.append(f"- `{item['path']}` (scope `{item['scope']}`)")
    if not context.get("instructions", {}).get("files"):
        lines.append("- No instruction files found")
    tests = context.get("tests", {})
    lines.extend(["", "## 7. Tests", "", f"- Test files: {len(tests.get('test_files', []))}"])
    lines.extend(f"- Changed test: `{path}`" for path in tests.get("changed_tests", []))
    lines.extend(["", "## 8. Diff", "", "```diff", change.get("diff", ""), "```", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("context", type=Path)
    parser.add_argument("--output", type=Path, default=Path("review/review-context.md"))
    args = parser.parse_args()
    context = json.loads(args.context.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(context), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())