---
name: pr-code-review
description: Builds incremental historical review intelligence, collects Git repository context for a base/source comparison, and produces a traceable review-context.md artifact for later code review. Use with logical base and source refs for pre-PR or pull-request review.
---

# PR Code Review

When invoked with either `{ "base": "main", "source": "dev/bug_fix" }` or `{ "change_request": "https://host.example/owner/repo/pull/123" }`, execute the phases below in order. Current-change context and historical knowledge are separate artifacts and must not be conflated. CLI adapters may expose the URL as `--pr-url`, `--change-request`, or `--change-url`.

For a GitHub PR URL, the collector resolves `base_ref` and `source_ref` automatically through the GitHub API and preserves the PR metadata. Private or rate-limited repositories require `GITHUB_TOKEN` or `GH_TOKEN`. Other PR/MR providers may still supply normalized metadata with `base_ref` and `source_ref` through `--provider-input`. Direct `base` and `source` values override provider metadata when both are supplied.

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
2. Synthesize `review/acceptance-criteria.md` from that evidence using `references/acceptance-criteria.md`. If PR comments or requirements are unavailable, understand the repository role from README/manifests and derive only clearly observable behavior supported by changed files, tests, or instructions. Include source, evidence, confidence, and verification for every criterion; then evaluate each as `PASS`, `FAIL`, `UNCERTAIN`, or `NOT_APPLICABLE`. Merge semantic duplicates but preserve distinct observable behaviors. If intent is not supported, write `Unknown / cannot determine`; never invent a criterion from engineering convention or implementation detail alone.
3. Run `scripts/analyze-test-coverage.py` with the current context. It inventories changed behavior candidates, tests, manifests, test commands, and measured coverage files.
4. Synthesize `review/code-coverage-report.md` from those facts using `references/coverage-analysis.md`. Determine whether unit tests adequately exercise each changed behavioral path, including meaningful success, boundary, invalid-input, and error scenarios. Distinguish measured coverage from change-based test sufficiency, and never fabricate a percentage or claim a test passed without evidence.

The two Markdown files are evidence packages for a later reviewer, not generic prose. Preserve links to changed paths, test names, manifests, coverage reports, PR IDs, and comments wherever available.

## Phase 4: Final Review Assessment

The final reviewer consumes `.github/instructions/insights.instructions.md`, `pr-insights.json`, `review/review-context.md`, `review/acceptance-criteria.md`, `review/code-coverage-report.md`, and the relevant source code. Evaluate exactly five gates: coverage, acceptance criteria, coding guidelines, historical compliance, and AI-slop. Use `references/final-review.md` to produce `review/review-assessment.json`.

Every gate must be `PASS`, `FAIL`, `UNCERTAIN`, `UNAVAILABLE`, or `NOT_APPLICABLE`. Mark a gate `UNAVAILABLE` when its required evidence or assessment was not supplied; unavailable gates block approval and are never converted into a pass. Findings must include severity from `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, or `INFO`, plus issue, impact, evidence, reference, recommendation, and a stable fingerprint when the same underlying issue appears in multiple gates.

Run `scripts/ensure-review-assessment.py --input review/review-assessment.json --output review/review-assessment.json` when an assessment exists, or omit `--input` to create an unavailable assessment. Then run `scripts/evaluate-review.py review/review-assessment.json --policy references/review-policy.json` to produce the canonical `review/review-result.json`. The evaluator applies the configurable coverage threshold (default 95), mandatory gate rules, unavailable-gate blocking, blocking severities, and AI-slop limits. It consolidates duplicate findings across gates. Approval requires all blocking gates to pass and no blocking-severity finding.

Always run `scripts/render-review-report.py review/review-result.json` to produce the human-facing `review/review-report.html`, including when gates are unavailable. The HTML must show each gate's status and score/evidence, every issue's severity, evidence, and reference link, and the final decision. HTML is presentation only; downstream automation must consume `review/review-result.json`.

The AI-slop gate reports only unnecessary complexity, risk, duplication, maintenance burden, or repository-convention violations. Do not flag code merely because it appears AI-generated.

## Phase 5: Review Handoff

Run `scripts/archive-review-run.py --base <base> --source <source>` after the final artifacts are produced. It snapshots the current diff/context, acceptance criteria, code-coverage report, historical insights, instructions, assessment, result, and HTML report under `.code-review/runs/<run-id>/`, with SHA-256 hashes and base/source commits in `manifest.json`. Missing artifacts are recorded in the manifest so monitoring can distinguish unavailable evidence from an empty file.

The skill stops after archiving the structured result and HTML report. A merger or other downstream agent should consume `review/review-result.json`, not parse HTML or reinterpret an LLM response. This skill does not approve or reject changes on behalf of a host; it records the policy evaluation and decision.

Do not perform code review at this stage.

Do not make approval decisions.

## Logical Request and Implementation

The client or launcher maps its command syntax to the logical request; the skill does not depend on a specific CLI. It may provide direct refs, a GitHub PR URL, or another provider URL plus normalized metadata. Run `scripts/collect_context.py` to produce the current-change context JSON, then run `scripts/generate_context.py` with that JSON to render the Markdown artifact. Run `scripts/extract-acceptance-context.py` and `scripts/analyze-test-coverage.py` to produce the evidence inputs for the two additional artifacts.

The scripts require Python 3.9 or newer and a Git repository. They use Git only for repository facts and do not call GitHub, GitLab, or any remote API. Historical extraction and semantic deduplication remain model-driven; Python only validates, selects, persists, and archives state.