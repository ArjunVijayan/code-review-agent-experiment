#!/usr/bin/env python3
"""Ensure a review assessment exists so the final HTML report is always produced."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


GATES = ("coverage", "acceptance_criteria", "coding_guidelines", "historical_review", "ai_slop")
REQUIRED_EVIDENCE = {
    "coverage": "unit-test and coverage assessment",
    "acceptance_criteria": "acceptance criteria evidence",
    "coding_guidelines": "coding standards assessment",
    "historical_review": "historical compliance evidence",
    "ai_slop": "AI-slop assessment",
}
EVIDENCE_REFERENCES = {
    "coverage": "review/code-coverage-report.md",
    "acceptance_criteria": "review/acceptance-criteria.md",
    "coding_guidelines": "review/review-context.md",
    "historical_review": "pr-insights.json",
    "ai_slop": "review/review-context.md",
}


def ensure(assessment: dict) -> dict:
    gates = assessment.setdefault("gates", {})
    recommendations = assessment.setdefault("recommendations", [])
    existing_recommendations = {item.get("description") for item in recommendations if isinstance(item, dict)}
    for name in GATES:
        gate = gates.setdefault(name, {})
        if not gate.get("status"):
            gate["status"] = "UNAVAILABLE"
            gate["unavailable_reason"] = f"{REQUIRED_EVIDENCE[name]} was not supplied."
        if gate.get("status") == "UNAVAILABLE":
            description = f"Supply the {REQUIRED_EVIDENCE[name]} before making a merge decision."
            if description not in existing_recommendations:
                recommendations.append({"priority": "REQUIRED", "description": description, "evidence": gate["unavailable_reason"], "reference": EVIDENCE_REFERENCES[name]})
        gate.setdefault("findings", [])
    return assessment


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("review/review-assessment.json"))
    args = parser.parse_args()
    assessment = json.loads(args.input.read_text(encoding="utf-8")) if args.input else {}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(ensure(assessment), indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())