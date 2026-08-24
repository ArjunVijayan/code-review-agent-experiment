---
name: test-generation
description: Generates unit/integration test cases for identified coverage gaps, following the repository's existing testing framework and conventions. Invoked conditionally by the orchestrator only when test-analysis reports gaps.
---

# Test Generation

## Purpose
Close the coverage gaps identified by `test-analysis` by generating well-formed, idiomatic tests that match the existing repository conventions — without inventing a new testing pattern for the project.

## Inputs
- `coverageGaps[]` from `test-analysis` (only `blocking` and `warning` severities are actioned by default)
- Existing test files in the repository (for framework/style detection: e.g., Jest, PyTest, JUnit, Mocha)
- Changed source files and their surrounding context

## Steps
1. Detect the testing framework and conventions already in use (assertion style, mocking library, file naming, folder structure, AAA/Given-When-Return pattern).
2. For each actionable gap, generate a test that:
   - Targets the specific `reason`/`suggestedAction` from the gap.
   - Uses existing fixtures/mocks where available rather than duplicating setup.
   - Follows the AAA (Arrange-Act-Assert) or repo's established pattern.
3. For AC-level gaps, ensure the generated test explicitly ties back to the acceptance criterion (e.g., in the test description/name).
4. If a gap cannot be safely closed without deeper domain knowledge (e.g., ambiguous business rule), do not fabricate assertions — mark it as `skipped` with a reason for human follow-up.
5. Do not modify production/source code in this skill — tests only.

## Output Contract
```json
{
  "generatedTests": [
    { "file": "...", "testName": "...", "targetGap": "...", "content": "..." }
  ],
  "skippedGaps": [
    { "target": "...", "reason": "requires domain clarification" }
  ]
}
```

## Handoff
Pass `generatedTests[]` and `skippedGaps[]` to `quality-report` for inclusion in the traceability matrix and final recommendations. `skippedGaps` should always surface as explicit action items in the report, never silently dropped.
