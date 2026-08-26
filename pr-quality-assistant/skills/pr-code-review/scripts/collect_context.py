#!/usr/bin/env python3
"""Build the complete CodeReviewContext from Git data and repository files."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from git_context import GitContextError, collect_context, resolve_repository
from resolve_change_request import ChangeRequestError, resolve


INSTRUCTION_NAMES = {"AGENTS.md", "CONTRIBUTING.md", "README.md", "copilot-instructions.md"}
MANIFEST_NAMES = {"pom.xml", "build.gradle", "pyproject.toml", "requirements.txt", "Pipfile", "package.json", "go.mod", "Cargo.toml"}
TEST_DIRECTORY_NAMES = {"tests", "test", "__tests__"}
TEST_SUFFIXES = ("_test.py", ".spec.ts", ".test.ts", ".spec.js", ".test.js")


def relative_files(repository: Path) -> list[str]:
    ignored = {".git", ".venv", "node_modules", "__pycache__"}
    files = []
    for path in repository.rglob("*"):
        if path.is_file() and not ignored.intersection(path.parts):
            files.append(path.relative_to(repository).as_posix())
    return sorted(files)


def collect_instructions(repository: Path) -> list[dict]:
    instructions = []
    for path in repository.rglob("*"):
        if path.is_file() and path.name in INSTRUCTION_NAMES and ".git" not in path.parts:
            relative = path.relative_to(repository).as_posix()
            scope = "/" + str(path.parent.relative_to(repository)).replace(".", "")
            instructions.append({"path": relative, "scope": scope or "/"})
    for path in repository.glob(".github/instructions/*.instructions.md"):
        instructions.append({"path": path.relative_to(repository).as_posix(), "scope": "/"})
    return sorted({item["path"]: item for item in instructions}.values(), key=lambda item: item["path"])


def collect_tests(repository: Path, changed_files: list[dict]) -> dict:
    all_files = relative_files(repository)
    test_files = [
        path
        for path in all_files
        if any(part in TEST_DIRECTORY_NAMES for part in Path(path).parts)
        or path.endswith(TEST_SUFFIXES)
        or Path(path).name.startswith("test_")
    ]
    manifests = [path for path in all_files if Path(path).name in MANIFEST_NAMES or Path(path).suffix == ".csproj"]
    changed_tests = [item["path"] for item in changed_files if item["path"] in test_files]
    return {"manifests": manifests, "test_files": test_files, "changed_tests": changed_tests}


def collect_full_context(repository: Path, base: str, source: str, change_request: dict | None = None) -> dict:
    context = collect_context(repository, base, source)
    if change_request:
        context["change_request"] = change_request
    files = relative_files(repository)
    context["repository"].update(
        {
            "files": files,
            "manifests": [
                path
                for path in files
                if Path(path).name in MANIFEST_NAMES or Path(path).suffix == ".csproj"
            ],
        }
    )
    context["instructions"] = {"files": collect_instructions(repository)}
    context["tests"] = collect_tests(repository, context["change"]["files"])
    return context


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base")
    parser.add_argument("--source")
    parser.add_argument("--pr-url", "--change-request", "--change-url", "--change_url", dest="change_request")
    parser.add_argument("--provider-input", type=Path, help="Normalized JSON containing base_ref and source_ref for the PR/MR")
    parser.add_argument("--repository", default=".")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        repository = resolve_repository(args.repository)
        change_request = None
        if args.change_request:
            if args.provider_input:
                change_request = json.loads(args.provider_input.read_text(encoding="utf-8"))
            else:
                try:
                    change_request = resolve(args.change_request, subprocess.check_output(["git", "remote", "get-url", "origin"], text=True).strip())
                except ChangeRequestError as error:
                    raise GitContextError(str(error)) from error
            base = args.base or change_request.get("base_ref") or change_request.get("base", "")
            source = args.source or change_request.get("source_ref") or change_request.get("source", "")
            if not base or not source:
                raise GitContextError("provider metadata must include base_ref and source_ref")
            change_request = {**change_request, "url": args.change_request}
        else:
            base = args.base
            source = args.source
        if not base or not source:
            raise GitContextError("provide both --base and --source, or provide --pr-url with --provider-input")
        context = collect_full_context(repository, base, source, change_request)
    except GitContextError as error:
        print(f"Context collection failed.\n\nReason:\n{error}", file=sys.stderr)
        return 1
    rendered = json.dumps(context, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())