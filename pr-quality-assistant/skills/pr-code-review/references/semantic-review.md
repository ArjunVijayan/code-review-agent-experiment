# Semantic Review Analysis

Use `review/review-analysis-input.json` as the evidence bundle. This phase is model-driven reasoning over deterministic facts; do not recollect the repository or invent facts.

## Required analysis

1. Establish the repository role and intended observable behavior from explicit PR/MR requirements first, then repository instructions, current diff, commits, and tests.
2. Evaluate acceptance criteria independently. Each criterion must have status, confidence, evidence, implementation location, verification test, and an explanation when it is not `PASS`.
3. Assess unit-test sufficiency by changed behavior and execution scenario: success, boundary, invalid input, error, regression, and critical-path scenarios where applicable. Distinguish measured coverage from inferred sufficiency.
4. Apply coding, architecture, security, dependency, database, historical, regression, and AI-slop standards only when supported by current evidence. Historical insight alone is context, not a current violation.
5. Review only issues introduced or changed by this PR/MR. Do not report pre-existing defects unless the change reintroduces or worsens them.
6. Consolidate findings with the same root cause across gates. Keep all affected gate and requirement references on the consolidated finding.

## Evidence requirement

Every finding must include category, severity, status, blocking, title, summary, evidence objects, expected, actual, impact, recommendation, confidence, and reference. Evidence objects must identify a source file/line, test, coverage result, requirement, historical PR, instruction rule, or build result. If the evidence is unavailable, use `UNAVAILABLE` or `UNCERTAIN`; do not fabricate a location, test result, percentage, or historical reference.

## Output

Write `review/review-assessment.json` with exactly these five gates: `coverage`, `acceptance_criteria`, `coding_guidelines`, `historical_review`, and `ai_slop`. Include `metrics`, `change_summary`, and evidence-backed `recommendations`. The policy evaluator, not this analysis, determines the final readiness decision.