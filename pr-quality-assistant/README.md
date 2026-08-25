# PR Quality Assistant

This package is an Agent Plugins v1.0 package containing two portable Agent Skills. Clients discover them from the fixed `skills/` directory; no custom agent or orchestration layer is required.

The `pr-code-review` skill first refreshes incremental historical intelligence, then collects Git-only context for either `{ "base": "main", "source": "dev/bug_fix" }` or a GitHub PR/MR URL. GitHub URLs resolve their refs automatically; other providers can supply normalized `base_ref` and `source_ref` metadata. It creates a structured `CodeReviewContext`, renders evidence packages, evaluates five review gates, and produces `review/review-result.json` plus `review/review-report.html`.

The `pr-code-merger` skill accepts a review-result JSON path, a PR/MR link, and a blast-radius assessment path. It assesses blast radius using deterministic facts plus LLM reasoning, then produces `review/blast-radius-report.md` and `review/merge-result.json`. It does not parse HTML to make decisions and never claims a PR was merged unless the host executed and verified the merge.

See [FLOW.md](FLOW.md) for the complete skill flowchart.

## On-demand review flow

The `pr-code-review` skill provides the context handoff for developer-facing pre-PR review and PR-facing quality reporting:

`historical intelligence -> current context -> acceptance + coverage evidence -> five-gate evaluation -> JSON result + HTML report`

The merger flow is:

`review-result.json + change summary -> blast-radius assessment -> policy gates -> merge-result.json`

Each review run is archived under `.code-review/runs/<run-id>/` with a manifest and hashes for the current context/diff, acceptance criteria, coverage report, historical insights, final result, and HTML report. This archive is the traceability source; `review/` is the working output directory.

When tests are insufficient, test generation runs before acceptance-criteria traceability and the final quality report.

## Merge-triggered intelligence flow

During the historical phase, the host supplies merged change requests and review feedback to the `repo-intelligence` workflow described in `skills/pr-code-review/references/insight-generation.md`. It deduplicates evidence by change-request ID and comment hash, and updates `pr-insights.json` plus `.github/instructions/insights.instructions.md` when a new reusable rule is found.

The host supplies the change-request provider data through its webhook, scheduled job, or native lifecycle event. Hosts without lifecycle events may invoke discovery manually, but the workflow must verify merge status before writing either output.

## Compatibility

Any Agent Plugins-compatible client can load this package. An Agent Skills-compatible client can consume the `pr-code-review/SKILL.md` file directly; the historical workflow is an internal phase, not a second exposed skill. The open standard controls package and skill discovery; each host controls user experience and event delivery.

## Standard

This package follows [Agent Plugins Specification 1.0.0](https://github.com/agentplugins/agent-plugins-spec/blob/main/spec/1.0.0.md) and [Agent Skills Specification](https://agentskills.io/specification). The plugin manifest uses the canonical Agent Plugins schema; skills are discovered from `skills/<name>/SKILL.md`.