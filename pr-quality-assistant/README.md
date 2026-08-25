# PR Quality Assistant

This package is an Agent Plugins v1.0 package containing one primary portable Agent Skill. Clients discover it from the fixed `skills/` directory; no custom agent or orchestration layer is required.

The `pr-code-review` skill first refreshes incremental historical intelligence, then collects Git-only context for a logical request such as `{ "base": "main", "source": "dev/bug_fix" }`. It creates a structured `CodeReviewContext`, renders evidence packages, evaluates five review gates, and produces `review/review-result.json` plus `review/review-report.html` without calling a hosting API.

See [FLOW.md](FLOW.md) for the complete skill flowchart.

## On-demand review flow

The `pr-code-review` skill provides the context handoff for developer-facing pre-PR review and PR-facing quality reporting:

`historical intelligence -> current context -> acceptance + coverage evidence -> five-gate evaluation -> JSON result + HTML report`

When tests are insufficient, test generation runs before acceptance-criteria traceability and the final quality report.

## Merge-triggered intelligence flow

During the historical phase, the host supplies merged change requests and review feedback to the `repo-intelligence` workflow described in `skills/pr-code-review/references/insight-generation.md`. It deduplicates evidence by change-request ID and comment hash, and updates `pr-insights.json` plus `.github/instructions/insights.instructions.md` when a new reusable rule is found.

The host supplies the change-request provider data through its webhook, scheduled job, or native lifecycle event. Hosts without lifecycle events may invoke discovery manually, but the workflow must verify merge status before writing either output.

## Compatibility

Any Agent Plugins-compatible client can load this package. An Agent Skills-compatible client can consume the `pr-code-review/SKILL.md` file directly; the historical workflow is an internal phase, not a second exposed skill. The open standard controls package and skill discovery; each host controls user experience and event delivery.

## Standard

This package follows [Agent Plugins Specification 1.0.0](https://github.com/agentplugins/agent-plugins-spec/blob/main/spec/1.0.0.md) and [Agent Skills Specification](https://agentskills.io/specification). The plugin manifest uses the canonical Agent Plugins schema; skills are discovered from `skills/<name>/SKILL.md`.