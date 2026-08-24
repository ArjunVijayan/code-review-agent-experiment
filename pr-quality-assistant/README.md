# PR Quality Assistant

This package exposes two reusable Agent Skills flows. Start with [AGENTS.md](AGENTS.md); it is the host-neutral entrypoint. The Copilot files provide one optional host adapter; other Agent Skills-compatible agents can discover and invoke the skills directly.

## On-demand persona flow

The developer review and PR quality report personas load repository insights, then share one analysis sequence:

`requirements -> change and blast-radius -> test-analysis -> test-sufficiency`

When tests are insufficient, test generation runs before acceptance-criteria traceability and the final quality report.

## Merge-triggered intelligence flow

On a merged PR event, the host invokes `repo-intelligence`. That agent fetches and cleanses review comments, then calls `insights-generator`, which deduplicates evidence by PR ID and comment hash and updates `data/pr-insights.json` plus `data/insights.instructions.md` when a new reusable rule is found.

For Copilot, the valid session-start hook prompts `repo-intelligence` to check for newly merged PRs because the current Copilot hooks reference has no PR-merged event. Other compatible hosts should connect their native PR webhook or scheduled automation to the same agent. The agent's merge-status check keeps any adapter from recording unmerged PR feedback.

## Compatibility

Any host implementing the Agent Skills specification can use `AGENTS.md` and the directories under `skills/`; see `skills/_shared/agent-skills-compatibility.md` for the host contract. The Markdown persona agents, `plugin.json`, and `hooks.json` are optional adapters, while `data/` is the shared persistence format.

## Documentation consulted

- [GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/plugins) for the requested plugin conventions (the page was unavailable during validation).
- [GitHub Copilot hooks reference](https://docs.github.com/en/copilot/reference/hooks-configuration), especially **Hook configuration format** and **Hook events**.
- [Using hooks with GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-hooks) for the `version: 1` and `sessionStart` configuration examples.