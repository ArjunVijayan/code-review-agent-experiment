# PR Quality Assistant

This package is an Agent Plugins v1.0 package containing two portable Agent Skills. Clients discover them from the fixed `skills/` directory; no custom agent or orchestration layer is required.

See [FLOW.md](FLOW.md) for the complete agent and skill flowchart.

## On-demand persona flow

The `pr-quality-review` skill provides both developer-facing pre-PR review and PR-facing quality reporting in one workflow:

`requirements -> change and blast-radius -> test-analysis -> test-sufficiency`

When tests are insufficient, test generation runs before acceptance-criteria traceability and the final quality report.

## Merge-triggered intelligence flow

On a merged PR event, the host invokes `repo-intelligence`. That skill fetches and cleanses review comments, deduplicates evidence by PR ID and comment hash, and updates `pr-insights.json` plus `.github/instructions/insights.instructions.md` when a new reusable rule is found.

The host supplies the merged-PR webhook, scheduled job, or native lifecycle event. Hosts without lifecycle events may invoke the skill manually, but it must verify merge status before writing either output.

## Compatibility

Any Agent Plugins-compatible client can load this package. An Agent Skills-compatible client can also consume the two `SKILL.md` files directly. The open standard controls package and skill discovery; each host controls user experience and event delivery.

## Standard

This package follows [Agent Plugins Specification 1.0.0](https://github.com/agentplugins/agent-plugins-spec/blob/main/spec/1.0.0.md) and [Agent Skills Specification](https://agentskills.io/specification). The plugin manifest uses the canonical Agent Plugins schema; skills are discovered from `skills/<name>/SKILL.md`.