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

1. **Coverage**: evaluate meaningful behavioral scenarios, using measured coverage only when available. A missing score is `UNCERTAIN`, never a pass. The default blocking threshold is 95 and is configurable.
2. **Acceptance criteria**: evaluate every criterion independently as `PASS`, `FAIL`, `UNCERTAIN`, or `NOT_APPLICABLE`. Mandatory or high-confidence criteria must all pass.
3. **Coding guidelines**: check repository, language, framework, dependency, database, security, testing, and shared-module rules.
4. **Historical compliance**: identify whether the current change reintroduces a historical defect pattern, with explicit historical and current evidence.
5. **AI-slop**: report only unnecessary complexity, risk, duplication, maintenance burden, or convention violations. Never flag code merely because it appears AI-generated.

Any gate finding must include `id`, `gate`, `severity`, `issue`, `impact`, `evidence`, `reference`, and `recommendation`. A finding may be referenced by multiple gates, but duplicate underlying issues must share one `fingerprint` and be consolidated by the evaluator.

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
  }
}
```

Statuses supplied by the reviewer are validated against the policy. `FAIL` and `UNCERTAIN` never become `PASS`. Overall approval requires every blocking gate to pass and no blocking-severity finding. The final result is structured first; HTML is presentation only.