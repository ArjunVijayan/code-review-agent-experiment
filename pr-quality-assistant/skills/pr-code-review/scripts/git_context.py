#!/usr/bin/env python3
"""Collect validated Git metadata for a base/source comparison."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


class GitContextError(RuntimeError):
    """Raised when the repository or comparison cannot be resolved."""


def run_git(repository: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or "git command failed"
        raise GitContextError(detail)
    return result.stdout


def resolve_repository(path: str) -> Path:
    candidate = Path(path).expanduser().resolve()
    if not candidate.is_dir():
        raise GitContextError(f"repository '{path}' does not exist")
    try:
        root = run_git(candidate, "rev-parse", "--show-toplevel").strip()
    except GitContextError as error:
        raise GitContextError(f"'{path}' is not a Git repository: {error}") from error
    return Path(root).resolve()


def collect_context(repository: Path, base: str, source: str) -> dict:
    base_commit = run_git(repository, "rev-parse", "--verify", f"{base}^{{commit}}").strip()
    source_commit = run_git(repository, "rev-parse", "--verify", f"{source}^{{commit}}").strip()
    if base_commit == source_commit:
        raise GitContextError("base and source refs resolve to the same commit")

    merge_base = run_git(repository, "merge-base", base, source).strip()
    if not merge_base:
        raise GitContextError(f"unable to determine merge base between '{base}' and '{source}'")

    name_status = run_git(repository, "diff", "--name-status", "-z", f"{base}...{source}")
    files = []
    entries = name_status.split("\0")
    index = 0
    while index < len(entries) - 1:
        status = entries[index]
        index += 1
        if not status:
            continue
        paths_needed = 2 if status[0] in {"R", "C"} else 1
        paths = entries[index : index + paths_needed]
        index += paths_needed
        if len(paths) == paths_needed and all(paths):
            item = {"path": paths[-1], "status": status_name(status)}
            if paths_needed == 2:
                item["previous_path"] = paths[0]
            files.append(item)

    stat = run_git(repository, "diff", "--shortstat", f"{base}...{source}").strip()
    statistics = parse_shortstat(stat)
    commits = run_git(
        repository,
        "log",
        "--format=%H%x1f%an%x1f%aI%x1f%s%x1f%b%x1e",
        f"{base}..{source}",
    )
    history = []
    for record in commits.split("\x1e"):
        fields = record.strip("\n").split("\x1f")
        if len(fields) >= 5 and fields[0]:
            history.append(
                {
                    "sha": fields[0],
                    "author": fields[1],
                    "date": fields[2],
                    "subject": fields[3],
                    "body": fields[4].strip(),
                }
            )

    return {
        "repository": {"root": str(repository)},
        "change": {
            "base": base,
            "source": source,
            "base_commit": base_commit,
            "source_commit": source_commit,
            "merge_base": merge_base,
            "files": files,
            "statistics": statistics,
            "diff": run_git(repository, "diff", f"{base}...{source}"),
        },
        "history": {"commits": history},
    }


def status_name(status: str) -> str:
    mapping = {"A": "added", "D": "deleted", "M": "modified", "R": "renamed", "C": "copied"}
    return mapping.get(status[0], status.lower())


def parse_shortstat(stat: str) -> dict:
    values = {"files_changed": 0, "insertions": 0, "deletions": 0}
    patterns = {
        "files_changed": r"(\d+) file(?:s)? changed",
        "insertions": r"(\d+) insertion(?:s)?\(\+\)",
        "deletions": r"(\d+) deletion(?:s)?\(-\)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, stat)
        if match:
            values[key] = int(match.group(1))
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--repository", default=".")
    args = parser.parse_args()
    try:
        repository = resolve_repository(args.repository)
        print(json.dumps(collect_context(repository, args.base, args.source), indent=2))
    except GitContextError as error:
        print(f"Context collection failed.\n\nReason:\n{error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())