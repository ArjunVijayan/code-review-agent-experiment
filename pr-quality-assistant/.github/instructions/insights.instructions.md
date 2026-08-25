---
description: >
  Code-review guidelines for this repository, derived from PR review history
  and the detected language/tech stack. Source rules: pr-insights.json.
applyTo: "**"
---

## Source

Detailed rules live in `pr-insights.json`; this file summarizes them for reviewers.

## Dependency Health

Check manifest dependencies for known CVEs and approaching end of life, and flag findings in review.

## Regression

Verify that changes add or update tests, preserve existing test coverage, and do not break existing behavior or public contracts.