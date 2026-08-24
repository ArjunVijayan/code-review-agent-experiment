---
name: test-sufficiency
description: Decides whether the test-analysis coverage gaps are acceptable, returning a boolean decision and rationale before test generation or final reporting.
---

# Test Sufficiency

## Purpose
Make the workflow's "Tests sufficient?" decision explicit and repeatable. This skill evaluates the gap output from `test-analysis`; it does not generate tests or alter repository files.

## Inputs
- `coverageGaps[]` from `test-analysis`
- `riskTier` and strictness from `change-blast-radius`
- Repository testing conventions and any stated acceptance criteria

## Steps
1. Confirm that every reported gap has a target, reason, and severity.
2. Return `sufficient: true` only when `coverageGaps[]` is empty.
3. When gaps exist, return `sufficient: false` and explain whether they are blocking or warning-level, including the highest-priority gaps.

## Output Contract
```json
{
  "sufficient": true,
  "rationale": "No coverage gaps were reported by test-analysis."
}
```

When gaps exist, `sufficient` must be `false`; the rationale must identify the gaps and state whether `test-generation` should run.