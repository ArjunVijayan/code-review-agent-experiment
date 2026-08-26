# Final Review

The final review is a deterministic evaluation over these evidence packages and the inspected source code:

- `review/review-context.md`
- `review/acceptance-criteria.md`
- `review/code-coverage-report.md`
- `pr-insights.json`
- `.github/instructions/insights.instructions.md`
- repository `AGENTS.md` and `.github/instructions/*`

The reviewer first produces `review/review-assessment.json` using the contract below. `scripts/evaluate-review.py` applies `references/review-policy.json` without reinterpretation and writes `review/review-result.json`. `scripts/render-review-report.py` renders that result as `review/review-report.html`.

## Five Gates

1. **Coverage**: evaluate meaningful behavioral scenarios, using measured coverage only when available. Missing coverage evidence is `UNAVAILABLE`, never a pass. The default blocking threshold is 95 and is configurable.
2. **Acceptance criteria**: evaluate every criterion independently as `PASS`, `FAIL`, `UNCERTAIN`, `UNAVAILABLE`, or `NOT_APPLICABLE`. Mandatory or high-confidence criteria must all pass; missing criteria evidence is `UNAVAILABLE`.
3. **Coding guidelines**: check repository, language, framework, dependency, database, security, testing, and shared-module rules.
4. **Historical compliance**: identify whether the current change reintroduces a historical defect pattern, with explicit historical and current evidence.
5. **AI-slop**: report only unnecessary complexity, risk, duplication, maintenance burden, or convention violations. Never flag code merely because it appears AI-generated.

Any gate finding must include `id`, `gate`, `severity`, `issue`, `impact`, `evidence`, `reference`, and `recommendation`. The evidence must identify the exact file, line/range, test, artifact section, or provider record where possible. A finding may be referenced by multiple gates, but duplicate underlying issues must share one `fingerprint` and be consolidated by the evaluator.

The assessment should also include `metrics` (for example, changed files, changed behavioral areas, test scenarios covered/missing, measured coverage when available, and applicable historical rules), `change_summary[]` entries with `requirement`, `files`, `behavior`, and `tests`, and `recommendations[]` entries with priority, description, evidence, and reference. Recommendations must explain what to change, why it matters, and where to change it; generic advice without evidence is not sufficient.

Use the generic review standards reference for scope, false-positive filtering, confidence, and decision vocabulary. A report may contain `WARNING` or `NOT_VERIFIABLE` findings, but only evidence-backed findings with clear impact and a blocking severity may block approval.

## Assessment Input

```json
{
  "pull_request": { "base": "main", "source": "dev/bug_fix" },
  "gates": {
    "coverage": { "status": "PASS", "score": 98, "covered": 20, "required": 20, "findings": [] },
    "acceptance_criteria": { "status": "PASS", "passed": 2, "failed": 0, "uncertain": 0, "criteria": [], "findings": [] },
    "coding_guidelines": { "status": "PASS", "passed": 10, "failed": 0, "findings": [] },
    "historical_review": { "status": "PASS", "passed": 4, "failed": 0, "findings": [] },
    "ai_slop": { "status": "PASS", "blocking_findings": 0, "major_findings": 0, "findings": [] }
  },
  "metrics": {
    "changed_files": 8,
    "behavioral_areas": 4,
    "unit_test_scenarios_covered": 20,
    "unit_test_scenarios_missing": 1,
    "measured_coverage": "not available"
  },
  "change_summary": [],
  "recommendations": []
}
```

Statuses supplied by the reviewer are validated against the policy. `FAIL`, `UNCERTAIN`, and `UNAVAILABLE` never become `PASS`; missing gates are normalized to `UNAVAILABLE`. Overall approval requires every blocking gate to pass and no blocking-severity finding. The evaluator retains backward-compatible `status` values and adds `decision`: `READY_TO_MERGE`, `READY_WITH_WARNINGS`, `NOT_READY_TO_MERGE`, or `CANNOT_DETERMINE`. The final result is structured first; HTML is presentation only and is always generated, including failed or unavailable results.