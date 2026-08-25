---
name: pr-quality-review
description: Reviews a pull request end to end by analyzing requirements, change and blast radius, repository guidelines, coding standards, tests, integration coverage, remediation, and final quality. Use for pre-PR reviews or at-PR quality reports.
---

# PR Quality Review

Run this single workflow for both developer-facing pre-PR review and PR-facing quality reporting. Do not require a custom agent, plugin manifest extension, hook, or orchestration service. Use the host's normal repository, diff, file, and test capabilities.

## Context

Before analysis, load `.github/instructions/insights.instructions.md` when it exists. Read `pr-insights.json` when detailed provenance or rule metadata is needed. Treat historical rules as review guidance, not as proof about the current change.

## Inputs

- Current branch or pull-request diff against the base branch
- PR title, description, linked issue, commits, and acceptance criteria
- Repository dependency manifests and test commands
- Existing tests and integration tests
- Repository-specific guidance in `AGENTS.md` and `.github/instructions/`

## Ordered Workflow

### 1. Requirements

Extract explicit and implicit requirements, acceptance criteria, and open questions from the PR description, linked work, and commits. Surface open questions instead of guessing.

### 2. Change and blast radius

Inspect the diff, classify changed files, trace direct and transitive dependents, identify affected modules, and assign `riskTier` as `low`, `medium`, or `high`.

### 3. Repository guidelines

Apply `pr-insights.json`, `.github/instructions/insights.instructions.md`, `AGENTS.md`, and other existing repository guidance. Prioritize rules marked `shared: true` or affecting common modules.

### 4. Coding standards and security

Check changed code for repository conventions, modularity, secure coding, secret leakage, prompt injection, unsafe configuration, unnecessary duplication, and generated-code anti-patterns.

### 5. Test analysis

Map existing tests to changed code and acceptance criteria. Identify missing unit, contract, edge-case, and regression coverage. In high-risk changes, treat any meaningful gap as blocking unless documented otherwise.

### 6. Integration-test verification

For acceptance criteria requiring cross-component or externally observable behavior, verify an integration-level test exists and run the repository's relevant integration-test command when available. Record command, result, and skipped-test reason.

### 7. Test sufficiency

Return a boolean and rationale. Set `sufficient` to `false` when any material coverage or integration gap remains.

```json
{
  "sufficient": true,
  "rationale": "All changed behavior and acceptance criteria have adequate coverage."
}
```

### 8. Conditional test generation

When `sufficient` is false, suggest or generate tests using the repository's framework and conventions. Do not invent assertions for ambiguous requirements; mark those gaps for clarification.

### 9. Issue remediation

When any blocking or warning finding exists, provide concrete suggested fixes as diffs or focused snippets. Do not apply production changes automatically.

### 10. Final report

Produce a concise checklist-style report containing critical findings, code-quality issues, test sufficiency, integration-test results, regression risk, change impact, acceptance-criteria traceability, quality score, and prioritized recommendations.

## Reporting Rules

- Every finding includes severity, evidence, impact, and actionable remediation.
- Distinguish current-PR evidence from historical repository guidance.
- Check manifest dependencies for known CVEs and approaching end of life.
- Require updated tests, preserved existing coverage, and intact behavior and public contracts.
- Never claim a test passed unless it was inspected or run.

## Output Contract

```json
{
  "qualityScore": 0,
  "riskTier": "low|medium|high",
  "sufficient": true,
  "traceabilityMatrix": [],
  "findings": [],
  "recommendations": []
}
```