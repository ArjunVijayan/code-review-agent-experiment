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
  - ArjunVijayan/code-review-agent-experiment/pr-quality-assistant@v1.2.7

safe-outputs:
  add-comment:
    max: 1
  merge:
    max: 1
---

# PR Quality Review

Run the `pr-code-review` skill from the installed `pr-quality-assistant` plugin against the pull request that triggered this workflow.

## Review Request

Use the current pull request as the `change_request`.

The skill must:

1. Resolve the PR's base and source refs.
2. Collect the current PR context and git diff.
3. Build or update historical review intelligence.
4. Extract and evaluate acceptance criteria.
5. Analyze test coverage and test sufficiency.
6. Evaluate the five review gates:
   - Coverage
   - Acceptance criteria
   - Coding guidelines
   - Historical compliance
   - AI-slop
7. Produce the structured review result.
8. Produce the human-readable HTML report.
9. Archive the complete review run.

Follow the `pr-code-review` skill instructions exactly.

## Review Evidence

Treat the following as the authoritative review artifacts:

- `review/review-result.json`
- `review/review-report.html`

Do not make assumptions when evidence is unavailable.

An `UNAVAILABLE`, `UNCERTAIN`, or otherwise non-passing blocking gate must not be treated as a pass.

## PR Comment

After the review is complete, add one concise comment to the pull request summarizing:

- Overall review result
- Acceptance criteria status
- Important findings
- Test and coverage status
- Items requiring human attention
- Link/path to the generated review report when available

Do not include a long reproduction of the full review report in the comment.

## Merge Decision

After `pr-code-review` has completed, use the structured:

`review/review-result.json`

as the input for the merge decision.

Do not independently reinterpret or override the review result.

Only merge the pull request when the structured review result indicates that the configured merge conditions are satisfied.

In particular:

- Do not merge when any blocking gate has failed.
- Do not merge when a required gate is `UNAVAILABLE`.
- Do not merge when there is a blocking-severity finding.
- Do not merge when the review result indicates that human review is required.

If the merge conditions are not satisfied, leave the pull request unmerged and report the reason in the PR comment.

## Restrictions

Do not modify source code.

Do not fix issues found during the review.

Do not approve the pull request.

Do not create additional review logic outside the installed plugin.

Do not fabricate evidence, test results, coverage values, requirements, or review findings.

The only allowed write actions are:

- Add a PR comment
- Merge the PR when the configured merge conditions are satisfied
---