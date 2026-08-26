#!/usr/bin/env python3
"""Render a structured blast-radius assessment as Markdown."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def render(assessment: dict) -> str:
    lines = ["# Blast Radius Report", "", "## Overall", "", f"**{str(assessment.get('overall_level', 'UNKNOWN')).upper()}**"]
    if assessment.get("score") is not None:
        lines.append(f"\nScore: {assessment['score']}/100")
    lines.extend(["", "## Dimensions", "", "| Area | Level | Evidence | Justification |", "|---|---|---|---|"])
    for name, item in assessment.get("dimensions", {}).items():
        lines.append(f"| {name.replace('_', ' ').title()} | {item.get('level', 'unknown')} | {item.get('evidence', '')} | {item.get('justification', '')} |")
    lines.extend(["", "## Affected Components", ""])
    lines.extend(f"- {component}" for component in assessment.get("affected_components", []))
    if not assessment.get("affected_components"):
        lines.append("- None supplied")
    lines.extend(["", "## Risk Factors", ""])
    lines.extend(f"- {reason}" for reason in assessment.get("reasons", []))
    lines.extend(["", "## Mitigating Factors", ""])
    lines.extend(f"- {item}" for item in assessment.get("mitigations", []))
    if not assessment.get("mitigations"):
        lines.append("- None supplied")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assessment", type=Path)
    parser.add_argument("--output", type=Path, default=Path("review/blast-radius-report.md"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(json.loads(args.assessment.read_text(encoding="utf-8"))), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())