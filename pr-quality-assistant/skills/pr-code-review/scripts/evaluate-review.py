#!/usr/bin/env python3
"""Apply deterministic approval gates to a structured review assessment."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


GATES = ("coverage", "acceptance_criteria", "coding_guidelines", "historical_review", "ai_slop")
VALID_STATUSES = {"PASS", "FAIL", "UNCERTAIN", "NOT_APPLICABLE"}


def fingerprint(finding: dict) -> str:
    value = finding.get("fingerprint") or "|".join(
        str(finding.get(key, "")).strip().lower()
        for key in ("issue", "impact", "evidence", "reference")
    )
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def consolidate_findings(gates: dict) -> list[dict]:
    merged: dict[str, dict] = {}
    for gate_name in GATES:
        for finding in gates.get(gate_name, {}).get("findings", []):
            item = dict(finding)
            item["gate"] = item.get("gate", gate_name)
            item["fingerprint"] = fingerprint(item)
            if item["fingerprint"] in merged:
                existing = merged[item["fingerprint"]]
                existing["gates"] = sorted(set(existing.get("gates", [existing["gate"]]) + [item["gate"]]))
                existing["references"] = sorted(set(existing.get("references", [existing.get("reference", "")]) + [item.get("reference", "")]))
            else:
                item["gates"] = [item["gate"]]
                item["references"] = [item.get("reference", "")]
                merged[item["fingerprint"]] = item
    return sorted(merged.values(), key=lambda item: (item.get("severity", "INFO"), item["fingerprint"]))


def gate_status(name: str, gate: dict, policy: dict) -> str:
    status = str(gate.get("status", "UNCERTAIN")).upper()
    if status not in VALID_STATUSES:
        return "UNCERTAIN"
    if name == "coverage" and status == "PASS" and gate.get("score") is None:
        return "UNCERTAIN"
    if name == "coverage" and policy[name].get("blocking") and gate.get("score") is not None:
        if float(gate["score"]) < float(policy[name]["threshold"]):
            return "FAIL"
    if name == "acceptance_criteria" and policy[name].get("blocking"):
        total = int(gate.get("passed", 0)) + int(gate.get("failed", 0)) + int(gate.get("uncertain", 0))
        if total and (int(gate.get("failed", 0)) > 0 or int(gate.get("uncertain", 0)) > 0):
            return "FAIL" if int(gate.get("failed", 0)) else "UNCERTAIN"
    if name in {"coding_guidelines", "historical_review"} and policy[name].get("blocking"):
        if int(gate.get("failed", 0)) > 0:
            return "FAIL"
    if name == "ai_slop" and policy[name].get("blocking"):
        if int(gate.get("blocking_findings", 0)) > policy[name]["max_blocking_findings"] or int(gate.get("major_findings", 0)) > policy[name]["max_major_findings"]:
            return "FAIL"
    return status


def evaluate(assessment: dict, policy: dict) -> dict:
    gates = assessment.get("gates", {})
    evaluated_gates = {}
    for name in GATES:
        source = dict(gates.get(name, {}))
        source["status"] = gate_status(name, source, policy)
        evaluated_gates[name] = source
    findings = consolidate_findings(evaluated_gates)
    blocking_severities = set(policy.get("blocking_severities", []))
    blocking_findings = [item for item in findings if str(item.get("severity", "INFO")).upper() in blocking_severities]
    gate_failure = any(gate["status"] in {"FAIL", "UNCERTAIN"} and policy[name].get("blocking", False) for name, gate in evaluated_gates.items())
    return {
        "status": "FAILED" if gate_failure or blocking_findings else "APPROVED",
        "pull_request": assessment.get("pull_request", {}),
        "gates": evaluated_gates,
        "blocking_findings": blocking_findings,
        "findings": findings,
        "approval_policy": policy,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assessment", type=Path)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("review/review-result.json"))
    args = parser.parse_args()
    result = evaluate(json.loads(args.assessment.read_text(encoding="utf-8")), json.loads(args.policy.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())