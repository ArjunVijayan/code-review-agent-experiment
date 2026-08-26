#!/usr/bin/env python3
"""Archive review artifacts and provenance for monitoring and traceability."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ARTIFACTS = {
    "review_context": "review/review-context.md",
    "acceptance_criteria": "review/acceptance-criteria.md",
    "code_coverage_report": "review/code-coverage-report.md",
    "review_assessment": "review/review-assessment.json",
    "review_result": "review/review-result.json",
    "review_report": "review/review-report.html",
    "historical_insights": "pr-insights.json",
    "insights_instructions": ".github/instructions/insights.instructions.md",
}
INTERMEDIATE_INPUTS = {
    "historical_discovery": ("/tmp/discovery.json", "review/discovery.json"),
    "current_context_json": ("/tmp/pr-quality-review-context.json", "review/review-context.json"),
    "acceptance_context_json": ("/tmp/acceptance-context.json", "review/acceptance-context.json"),
    "coverage_facts_json": ("/tmp/coverage-facts.json", "review/coverage-facts.json"),
    "review_analysis_input": ("review/review-analysis-input.json", "/tmp/review-analysis-input.json"),
    "change_requests_json": ("review/change-requests.json",),
}


def git_value(repository: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repository), *args], capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else ""


def archive(repository: Path, base: str, source: str, run_id: str | None) -> Path:
    timestamp = datetime.now(timezone.utc).replace(microsecond=0)
    identifier = run_id or timestamp.strftime("%Y%m%dT%H%M%SZ")
    destination = repository / ".code-review" / "runs" / identifier
    destination.mkdir(parents=True, exist_ok=False)
    copied = {}
    copied_inputs = {}
    missing = []
    for name, relative in ARTIFACTS.items():
        source_path = repository / relative
        if not source_path.is_file() and name in {"historical_insights", "insights_instructions"}:
            package_path = repository / "pr-quality-assistant" / relative
            if package_path.is_file():
                source_path = package_path
        if not source_path.is_file():
            missing.append(relative)
            continue
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target)
        copied[name] = {"path": relative, "sha256": hashlib.sha256(source_path.read_bytes()).hexdigest()}
    missing_inputs = []
    for name, candidates in INTERMEDIATE_INPUTS.items():
        source_path = next((repository / candidate for candidate in candidates if (repository / candidate).is_file()), None)
        if source_path is None:
            absolute_candidates = [Path(candidate) for candidate in candidates if candidate.startswith("/")]
            source_path = next((candidate for candidate in absolute_candidates if candidate.is_file()), None)
        if source_path is None:
            missing_inputs.append(list(candidates))
            continue
        relative = source_path.relative_to(repository).as_posix() if source_path.is_relative_to(repository) else f"inputs/{source_path.name}"
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target)
        copied_inputs[name] = {"path": relative, "sha256": hashlib.sha256(source_path.read_bytes()).hexdigest()}
    manifest = {
        "run_id": identifier,
        "created_at": timestamp.isoformat().replace("+00:00", "Z"),
        "repository": str(repository),
        "base": base,
        "source": source,
        "source_commit": git_value(repository, "rev-parse", source),
        "base_commit": git_value(repository, "rev-parse", base),
        "copied_artifacts": copied,
        "missing_artifacts": missing,
        "copied_intermediate_inputs": copied_inputs,
        "missing_intermediate_inputs": missing_inputs,
        "secrets_excluded": [".env", "GITHUB_TOKEN", "GH_TOKEN", "GITLAB_TOKEN", "VCS_TOKEN"],
    }
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path("."))
    parser.add_argument("--base", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--run-id")
    args = parser.parse_args()
    destination = archive(args.repository.resolve(), args.base, args.source, args.run_id)
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())