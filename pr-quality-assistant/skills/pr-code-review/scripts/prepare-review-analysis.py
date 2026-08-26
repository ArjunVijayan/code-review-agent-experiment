#!/usr/bin/env python3
"""Prepare deterministic evidence for model-driven semantic review analysis."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path, default: object) -> object:
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def read_text(path: Path, limit: int = 20000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""


def prepare(repository: Path, context: dict, acceptance: dict, coverage: dict, discovery: dict) -> dict:
    insight_path = repository / "pr-insights.json"
    if not insight_path.is_file():
        insight_path = repository / "pr-quality-assistant" / "pr-insights.json"
    instruction_path = repository / ".github/instructions/insights.instructions.md"
    if not instruction_path.is_file():
        instruction_path = repository / "pr-quality-assistant/.github/instructions/insights.instructions.md"
    return {
        "purpose": "Provide evidence for semantic PR review. Do not infer facts not present in these inputs.",
        "review_scope": context.get("change", {}),
        "repository": context.get("repository", {}),
        "history": context.get("history", {}),
        "instructions": context.get("instructions", {}),
        "tests": context.get("tests", {}),
        "historical_discovery": discovery,
        "historical_insights": load_json(insight_path, {"insights": []}),
        "insights_instructions": read_text(instruction_path),
        "acceptance_evidence": acceptance,
        "coverage_facts": coverage,
        "analysis_requirements": {
            "review_only_current_change": True,
            "do_not_fabricate_requirements_or_coverage": True,
            "evaluate_acceptance_criteria_independently": True,
            "evaluate_unit_test_scenarios": True,
            "separate_deterministic_facts_from_ai_judgments": True,
            "include_exact_file_line_or_artifact_references": True,
            "consolidate_duplicate_root_causes": True,
            "confidence_values": ["HIGH", "MEDIUM", "LOW"],
            "gate_values": ["PASS", "FAIL", "WARNING", "UNCERTAIN", "UNAVAILABLE", "NOT_APPLICABLE"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path("."))
    parser.add_argument("--context", type=Path, required=True)
    parser.add_argument("--acceptance", type=Path, required=True)
    parser.add_argument("--coverage", type=Path, required=True)
    parser.add_argument("--discovery", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    context = load_json(args.context, {})
    acceptance = load_json(args.acceptance, {})
    coverage = load_json(args.coverage, {})
    discovery = load_json(args.discovery, {"provider_data_available": False}) if args.discovery else {"provider_data_available": False}
    result = prepare(args.repository.resolve(), context, acceptance, coverage, discovery)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())