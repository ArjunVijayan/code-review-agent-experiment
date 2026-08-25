---
name: pr-code-review
description: Builds incremental historical review intelligence, collects Git repository context for a base/source comparison, and produces a traceable review-context.md artifact for later code review. Use with logical base and source refs for pre-PR or pull-request review.
---

# PR Code Review

When invoked with the logical request `{ "base": "main", "source": "dev/bug_fix" }`, execute the phases below in order. Current-change context and historical knowledge are separate artifacts and must not be conflated.

## Phase 1: Historical Intelligence

1. Validate the repository and base ref before attempting discovery.
2. Read `.code-review/insights-state.json`; if absent, treat historical knowledge as empty and bootstrap.
3. Ask the host's change-request provider for merged change requests targeting the base ref. Git alone cannot supply PR/MR IDs, comments, reviewers, or approval history; do not add provider API logic to the scripts.
4. Pass normalized provider JSON to `scripts/discover-historical-prs.py` with the state file and `--limit 100`. It returns only newly discovered, merged requests for the selected base. On a changed base ref, start a fresh analyzed set.
5. For each returned request, provide its description, review comments, threads, and reviews to the model using `references/insight-generation.md`. Extract only generalizable, actionable rules; ignore questions and one-off or PR-specific feedback.
6. Semantically deduplicate the extracted rules against the existing root `pr-insights.json`. Write knowledge to `pr-insights.json` and concise reviewer guidance to `.github/instructions/insights.instructions.md` in the required section order.
7. Only after both outputs are successfully written, run `scripts/manage-insights-state.py --mark-success --base <base> --state .code-review/insights-state.json --successful-ids ...`. Never mark requests before successful generation.

If no new requests are returned, preserve the existing insight files and state. Do not generate a historical raw-comments document.

## Phase 2: Current Change Context

1. Validate the repository, base ref, source ref, distinct commits, and merge base.
2. Collect Git metadata, changed files, numeric diff statistics, complete raw diff, and introduced commit history.
3. Collect repository structure, manifests, applicable instruction files, and test information.
4. Build the canonical `CodeReviewContext` object with `scripts/collect_context.py`.
5. Render `review/review-context.md` with `scripts/generate_context.py`. Keep the raw diff last.

## Phase 3: Evidence Analysis

1. Run `scripts/extract-acceptance-context.py` with the current context and any provider-supplied PR description, comments, threads, reviews, and issue references.
2. Synthesize `review/acceptance-criteria.md` from that evidence using `references/acceptance-criteria.md`. Include source, evidence, confidence, and verification for every criterion. Merge semantic duplicates but preserve distinct observable behaviors. If intent is not supported, write `Unknown / cannot determine`; never invent a criterion from engineering convention or implementation detail alone.
3. Run `scripts/analyze-test-coverage.py` with the current context. It inventories changed behavior candidates, tests, manifests, test commands, and measured coverage files.
4. Synthesize `review/code-coverage-report.md` from those facts using `references/coverage-analysis.md`. Analyze behavioral execution paths and meaningful success, boundary, and error scenarios. Distinguish measured coverage from change-based test sufficiency, and never fabricate a percentage or claim a test passed without evidence.

The two Markdown files are evidence packages for a later reviewer, not generic prose. Preserve links to changed paths, test names, manifests, coverage reports, PR IDs, and comments wherever available.

## Phase 4: Review Handoff

The skill stops after evidence construction. A later review stage may read, in order, `.github/instructions/insights.instructions.md`, `pr-insights.json`, `review/review-context.md`, `review/acceptance-criteria.md`, and `review/code-coverage-report.md`, then inspect source code and produce findings. This skill does not review code, generate findings, approve or reject changes, or call GitHub/GitLab APIs.

Do not perform code review at this stage.

Do not make approval decisions.

## Logical Request and Implementation

The client or launcher maps its command syntax to the logical request; the skill does not depend on a specific CLI. The provider maps its API response to the normalized input expected by `scripts/discover-historical-prs.py`. Run `scripts/collect_context.py` to produce the current-change context JSON, then run `scripts/generate_context.py` with that JSON to render the Markdown artifact. Run `scripts/extract-acceptance-context.py` and `scripts/analyze-test-coverage.py` to produce the evidence inputs for the two additional artifacts.

The scripts require Python 3.9 or newer and a Git repository. They use Git only for repository facts and do not call GitHub, GitLab, or any remote API. Historical extraction and semantic deduplication remain model-driven; Python only validates, selects, and persists state.