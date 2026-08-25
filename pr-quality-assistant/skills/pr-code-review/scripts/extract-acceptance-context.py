#!/usr/bin/env python3
"""Collect evidence sources for model-driven acceptance-criteria synthesis."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_text(repository: Path, relative_path: str, limit: int = 12000) -> str:
    try:
        return (repository / relative_path).read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""


def extract(context: dict, repository: Path, provider_payload: dict | None) -> dict:
    change = context["change"]
    provider_requests = (provider_payload or {}).get("change_requests", [])
    request_evidence = []
    for request in provider_requests:
        request_evidence.append(
            {
                "id": str(request.get("id", "")),
                "title": request.get("title", ""),
                "description": request.get("description", ""),
                "comments": request.get("comments", []),
                "reviews": request.get("reviews", []),
            }
        )
    instruction_evidence = []
    for item in context.get("instructions", {}).get("files", []):
        content = read_text(repository, item["path"])
        if content:
            instruction_evidence.append({"path": item["path"], "scope": item["scope"], "content": content})
    return {
        "principle": "Do not create an acceptance criterion without evidence; mark insufficiently supported behavior as unknown.",
        "source_priority": [
            "PR description and discussion",
            "linked issue or task",
            "historical reviewer discussion",
            "implementation and diff",
            "existing tests",
            "repository conventions",
        ],
        "change": {
            "base": change["base"],
            "source": change["source"],
            "changed_files": change["files"],
            "diff": change["diff"],
        },
        "provider_evidence": request_evidence,
        "repository_instruction_evidence": instruction_evidence,
        "existing_tests": context.get("tests", {}),
        "synthesis_rules": {
            "merge_semantic_duplicates": True,
            "preserve_distinct_observable_behaviors": True,
            "required_fields": ["requirement", "evidence", "verification", "confidence"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("context", type=Path)
    parser.add_argument("--repository", type=Path, default=Path("."))
    parser.add_argument("--provider-input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    context = json.loads(args.context.read_text(encoding="utf-8"))
    provider = json.loads(args.provider_input.read_text(encoding="utf-8")) if args.provider_input else None
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(extract(context, args.repository.resolve(), provider), indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())