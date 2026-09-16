---
name: PR Quality Review

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: write
  pull-requests: write

engine: copilot

plugins:
  - ps-health/review-agents@v1.2.7

safe-outputs:
  add-comment:
    max: 1
  merge:
    max: 1
---

# PR Quality Review

Run the PR Quality Assistant against the pull request that triggered this workflow.

Use the `pr-code-review` capability from the installed `ps-health/review-agents` plugin.

## Review Objective

Review the pull request using:

1. PR title and description
2. Stated change intention
3. Explicit acceptance criteria
4. Git diff
5. Relevant repository guidelines
6. Test and coverage evidence
7. Historical review insights, when available

## Acceptance Criteria

First, synthesize simple, human-readable acceptance criteria from the PR description.

Criteria should focus on:

- What the change is intended to achieve
- Why the change is needed
- What observable behavior should be true

Do not turn implementation details or individual code changes into acceptance criteria unless they are explicitly required by the PR.

Evaluate each criterion as:

- PASS
- FAIL
- UNCERTAIN
- NOT_APPLICABLE

Every evaluation must be supported by evidence from the repository, PR context, or git diff.

Do not invent requirements.

## Review Scope

Evaluate:

- Correctness
- Acceptance criteria
- Test coverage
- Repository guidelines
- Historical review compliance
- Obvious AI-generated or low-quality patterns

Do not calculate blast radius during the code-review stage.

The downstream PR Review Agent is responsible for:

- Blast-radius analysis
- Risk assessment
- Merge decision

## Output

Use the plugin's standard review artifacts and reporting format.

Add one concise PR comment containing:

- Acceptance criteria status
- Important findings
- Test and coverage status
- Items requiring human attention

Do not modify source code.

Do not approve the PR.

If evidence is insufficient, report `UNCERTAIN` rather than guessing.

## Merge

After the code review is complete, invoke the downstream PR Review Agent from the installed plugin.

The PR Review Agent should consume the review results and git diff, calculate blast radius and risk, and determine whether the configured merge conditions are satisfied.

Only merge the pull request when all configured merge conditions are satisfied.

If the merge conditions are not satisfied, do not merge the pull request.