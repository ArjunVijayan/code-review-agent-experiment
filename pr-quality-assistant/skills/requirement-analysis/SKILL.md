---
name: requirement-analysis
description: Extracts structured requirements and acceptance criteria from a PR description, linked ticket, or user story. Use this skill first, before analyzing code changes, to establish what the PR is supposed to achieve.
---

# Requirement Analysis

## Purpose
Parse the PR description, commit messages, and any linked issue/ticket to produce a structured, unambiguous set of requirements and acceptance criteria that later skills (blast radius, test analysis, quality report) can validate against.

## Inputs
- PR title and description
- Linked ticket/story (if available) — id, description, acceptance criteria
- Commit messages in the PR

## Steps
1. Read the PR description and linked ticket content.
2. Identify explicit and implicit requirements (functional and non-functional).
3. Extract or infer acceptance criteria. If the ticket already lists AC, normalize them into discrete, testable statements.
4. Flag ambiguous or missing requirements as `openQuestions` rather than guessing.
5. Classify each requirement as functional, non-functional (perf/security/a11y), or refactor/chore.

## Output Contract
```json
{
  "requirements": [
    { "id": "REQ-1", "description": "...", "type": "functional|non-functional|chore" }
  ],
  "acceptanceCriteria": [
    { "id": "AC-1", "description": "...", "linkedRequirement": "REQ-1" }
  ],
  "openQuestions": ["..."]
}
```

## Handoff
Pass `requirements[]` and `acceptanceCriteria[]` to `change-blast-radius` and later to `quality-report` for traceability. Surface `openQuestions[]` to the orchestrator immediately — do not proceed with assumptions.
