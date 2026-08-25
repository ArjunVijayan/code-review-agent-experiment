#!/usr/bin/env python3
"""Collect deterministic, change-focused test and coverage facts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


COVERAGE_FILES = {"coverage.xml", "coverage.json", "lcov.info", "jacoco.xml"}
TEST_COMMAND_KEYS = {"pytest", "jest", "nyc", "test", "coverage", "go test", "dotnet test"}


def discover_coverage_files(repository: Path) -> list[str]:
    return sorted(
        path.relative_to(repository).as_posix()
        for path in repository.rglob("*")
        if path.is_file() and (path.name in COVERAGE_FILES or path.name.endswith(".lcov"))
    )


def discover_test_commands(repository: Path, manifests: list[str]) -> list[dict]:
    commands = []
    for manifest in manifests:
        path = repository / manifest
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            if any(key in line.lower() for key in TEST_COMMAND_KEYS):
                commands.append({"manifest": manifest, "line": line_number, "text": line.strip()})
    return commands


def analyze(context: dict, repository: Path) -> dict:
    changed_files = context["change"]["files"]
    source_files = [item["path"] for item in changed_files if item["status"] not in {"added", "deleted"}]
    changed_tests = context.get("tests", {}).get("changed_tests", [])
    test_files = context.get("tests", {}).get("test_files", [])
    coverage_files = discover_coverage_files(repository)
    manifests = context.get("repository", {}).get("manifests", [])
    return {
        "scope": {
            "base": context["change"]["base"],
            "source": context["change"]["source"],
            "changed_files": [item["path"] for item in changed_files],
            "behavioral_candidates": source_files,
        },
        "tests": {
            "all_test_files": test_files,
            "changed_test_files": changed_tests,
            "potentially_relevant_tests": [path for path in test_files if any(Path(source).stem in path for source in source_files)],
        },
        "coverage": {
            "measured_report_files": coverage_files,
            "measured_data_available": bool(coverage_files),
            "note": "No numeric coverage claim is made by this collector.",
        },
        "test_commands": discover_test_commands(repository, manifests),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("context", type=Path)
    parser.add_argument("--repository", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    context = json.loads(args.context.read_text(encoding="utf-8"))
    repository = args.repository.resolve()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(analyze(context, repository), indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())