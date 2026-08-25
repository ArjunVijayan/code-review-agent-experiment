#!/usr/bin/env python3
"""Apply merge policy to review-result.json and a model-produced blast-radius assessment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


GATES = ("coverage", "acceptance_criteria", "coding_guidelines", "historical_review", "ai_slop")
LEVELS = {"low", "medium", "high", "critical"}


def decision(review: dict, blast_radius: dict, policy: dict, reference: str, merge_executed: bool) -> dict:
    reasons = list(blast_radius.get("reasons", []))
    missing_gates = [name for name in GATES if name not in review.get("gates", {})]
    failed_gates = [name for name in GATES if review.get("gates", {}).get(name, {}).get("status") != "PASS"]
    blocking = review.get("blocking_findings", [])
    level = str(blast_radius.get("overall_level", "")).lower()
    if level not in LEVELS:
        level = "critical"
        reasons.append("Blast-radius level is missing or invalid.")
    if missing_gates:
        reasons.append(f"Missing review gates: {', '.join(missing_gates)}.")
    if failed_gates:
        reasons.append(f"Review gates are not passing: {', '.join(failed_gates)}.")
    if blocking:
        reasons.append(f"{len(blocking)} blocking review finding(s) remain.")
    review_passes = not missing_gates and not failed_gates and not blocking
    policy_allows = policy.get(level, {}).get("auto_merge", False) and review_passes
    if policy_allows:
        return {
            "decision": "auto_merge",
            "action": "merge" if merge_executed else "merge_not_executed",
            "status": "merged" if merge_executed else "not_merged",
            "blast_radius": {"level": level, "score": blast_radius.get("score")},
            "reasons": reasons or ["Low blast radius and all review gates passed."],
            "review_reference": reference,
        }
    return {
        "decision": "human_review",
        "action": "do_not_merge",
        "status": "not_merged",
        "blast_radius": {"level": level, "score": blast_radius.get("score")},
        "reasons": reasons or [f"{level.title()} blast radius requires human review."],
        "review_reference": reference,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review_result", type=Path)
    parser.add_argument("blast_radius", type=Path)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--reference", default="")
    parser.add_argument("--merge-executed", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("review/merge-result.json"))
    args = parser.parse_args()
    review = json.loads(args.review_result.read_text(encoding="utf-8"))
    blast_radius = json.loads(args.blast_radius.read_text(encoding="utf-8"))
    policy = json.loads(args.policy.read_text(encoding="utf-8"))
    result = decision(review, blast_radius, policy, args.reference, args.merge_executed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())