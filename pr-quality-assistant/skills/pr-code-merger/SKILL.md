---
name: pr-code-merger
description: Evaluates a completed review-result.json, reasons about change blast radius, and decides whether a pull request may be auto-merged or requires human review. Use after pr-code-review has produced its structured result.
---

# PR Code Merger

This is a portable skill, not an orchestration agent. It consumes an explicit `review-result.json` path and a PR/MR link. The JSON is the authoritative review input. `review-report.html` is a human-readable reference only and must never be parsed as the primary decision source.

## Inputs

- PR/MR link supplied by the host, such as `https://host.example/owner/repo/pull/123`
- Path to `review-result.json` from `pr-code-review`
- `review/review-report.html` for human reference when available
- A concise change summary with requirements, affected files, behavior, and tests
- Source and repository facts available to the host
- Optional provider merge capability

## Workflow

1. Accept `--review-result <path>`, `--change-request <PR/MR URL>`, and `--blast-radius <assessment JSON path>`. Validate that the review result exists, is valid JSON, and contains all five gate results and `blocking_findings`.
2. If the review result is failed, uncertain, missing required gates, or contains blocking findings, produce `human_review` and `do_not_merge` without calculating an auto-merge approval.
3. Use deterministic facts for changed files, lines, commits, modified symbols, dependency graph, and contracts where available. Do not ask the LLM to count files or lines.
4. Ask the LLM to assess the six blast-radius dimensions: change size, dependency reach, architectural criticality, data impact, contract impact, and runtime/deployment impact. Each assessment must include evidence and justification.
5. Produce `review/blast-radius-report.md` with the six dimensions, affected components, dependency impact, contract impact, risk factors, mitigating factors, overall level, and optional score.
6. Apply `references/merge-policy.json` to the review result and blast-radius assessment with `scripts/decide-merge.py --review-result <path> --change-request <url> --blast-radius <path>`. Low risk can be auto-merge eligible only when all blocking review gates pass and no blocking finding exists. Medium, high, and critical risk require human review by default.
7. Write `review/merge-result.json`. Distinguish `decision` from `action`: a decision to auto-merge is not proof that a merge occurred.
8. If the host provides a merge tool and policy allows execution, invoke it only after the decision. Verify the resulting PR/MR state before reporting `status: merged`; otherwise use `merge_not_executed`.

## Blast-Radius Assessment Input

The LLM should produce `review/blast-radius-assessment.json` with this shape:

```json
{
  "overall_level": "low|medium|high|critical",
  "score": 18,
  "dimensions": {
    "change_size": { "level": "medium", "evidence": "...", "justification": "..." },
    "dependency_reach": { "level": "low", "evidence": "...", "justification": "..." },
    "architectural_criticality": { "level": "low", "evidence": "...", "justification": "..." },
    "data_impact": { "level": "low", "evidence": "...", "justification": "..." },
    "contract_impact": { "level": "low", "evidence": "...", "justification": "..." },
    "operational_impact": { "level": "low", "evidence": "...", "justification": "..." }
  },
  "affected_components": [],
  "reasons": [],
  "mitigations": []
}
```

Blast radius is not a proxy for file count. Database/schema, PII, financial data, credentials, authentication, public contracts, shared services, infrastructure, and deployment changes require explicit consideration.

## Outputs

```json
{
  "decision": "auto_merge|human_review",
  "action": "merge|merge_not_executed|do_not_merge",
  "status": "pending|merged|not_merged",
  "blast_radius": { "level": "low", "score": 18 },
  "reasons": [],
  "review_reference": "..."
}
```

Never claim a PR/MR was merged when the host merge action was unavailable or unverified.