---
name: quality-report
description: Aggregates outputs from requirement-analysis, change-blast-radius, test-analysis, and test-generation into an acceptance-criteria traceability matrix and a final PR quality report with a score and actionable recommendations. Use as the last step in the workflow.
---

# Quality Assessment & Reporting

## Purpose
Synthesize every prior skill's output into a single, decision-ready report: did the PR meet its stated requirements, is the blast radius acceptable, is it adequately tested, and what should happen next.

## Inputs
- `requirements[]`, `acceptanceCriteria[]` from `requirement-analysis`
- `affectedModules[]`, `riskTier`, `blastRadiusSummary` from `change-blast-radius`
- `existingTestsMapped[]`, `acceptanceCriteriaCoverage[]`, `coverageGaps[]` from `test-analysis`
- `generatedTests[]`, `skippedGaps[]` from `test-generation` (if invoked)

## Steps
1. **Build the traceability matrix**: for every `acceptanceCriteria` item, resolve final status as `passed` (test exists and covers it), `generated` (newly created test covers it), or `untested` (still a gap after generation, i.e., in `skippedGaps`).
2. **Compute the quality score** using the rubric in `references/report-format.md` (weights: requirement clarity, blast radius risk, test coverage completeness, unresolved gaps).
3. **Summarize risk**: restate `riskTier` and `blastRadiusSummary` in context of test coverage — e.g., high risk + full coverage is very different from high risk + gaps.
4. **List actionable recommendations**, prioritized by severity (blocking gaps first, then warnings, then informational notes).
5. **Render the final report** using the exact structure defined in `references/report-format.md` so output is consistent across PRs.

## Output Contract
A single markdown report (see `references/report-format.md` for required sections) plus a machine-readable summary:
```json
{
  "qualityScore": 0,
  "riskTier": "low|medium|high",
  "traceabilityMatrix": [
    { "acId": "AC-1", "status": "passed|generated|untested", "tests": ["..."] }
  ],
  "recommendations": [
    { "priority": "blocking|warning|info", "description": "..." }
  ]
}
```

## Handoff
This is the terminal skill in the workflow. The orchestrator returns this report to the user/PR. No further skill is invoked. (Reserved: a future hook could post this report as a PR comment automatically.)
