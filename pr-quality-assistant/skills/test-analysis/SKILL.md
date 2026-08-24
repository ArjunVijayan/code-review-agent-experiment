---
name: test-analysis
description: Evaluates existing test coverage against the changed code and acceptance criteria to identify coverage gaps. Use after change-blast-radius and before test-generation.
---

# Test Analysis

## Purpose
Determine whether existing tests adequately cover the changed/affected code and the acceptance criteria established during requirement analysis, and produce a precise list of gaps.

## Inputs
- `changedFiles[]` and `affectedModules[]` from `change-blast-radius`
- `riskTier` (determines strict vs. warn mode)
- `acceptanceCriteria[]` from `requirement-analysis`
- Existing test suite in the repository

## Steps
1. Locate existing tests associated with each changed file/module (by naming convention, imports, or coverage reports if available).
2. Map each `acceptanceCriteria` item to zero or more existing tests.
3. Identify gaps:
   - Changed code with no associated test.
   - Acceptance criteria with no test mapped to it.
   - Edge cases implied by the change type (e.g., interface changes → contract tests) that aren't covered.
4. In **strict mode** (`riskTier: high`), any gap is reported as blocking. In normal mode, gaps are reported as warnings.
5. Do not modify or generate tests in this skill — only analyze and report. See `references/test-coverage-methodology.md` for detailed evaluation criteria.

## Output Contract
```json
{
  "existingTestsMapped": [
    { "file": "...", "tests": ["..."] }
  ],
  "acceptanceCriteriaCoverage": [
    { "acId": "AC-1", "covered": true, "tests": ["..."] }
  ],
  "coverageGaps": [
    { "target": "file|AC-id", "reason": "...", "severity": "blocking|warning" }
  ]
}
```

## Handoff
If `coverageGaps[]` is non-empty, the orchestrator invokes `test-generation`. Regardless, all outputs are passed to `quality-report` for the traceability matrix.
