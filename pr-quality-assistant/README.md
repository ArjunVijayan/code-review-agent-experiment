# PR Quality Assistant

This plugin has two related flows.

## On-demand persona flow

The developer review and PR quality report agents load repository insights, then share one analysis sequence:

`requirements -> change and blast-radius -> test-analysis -> test-sufficiency`

When tests are insufficient, test generation runs before acceptance-criteria traceability and the final quality report.

## Merge-triggered intelligence flow

At session start, the valid Copilot hook prompts `repo-intelligence` to check for newly merged PRs. That agent fetches and cleanses review comments, then calls `insights-generator`, which deduplicates evidence by PR ID and comment hash and updates `data/pr-insights.json` plus `data/insights.instructions.md` when a new reusable rule is found.

The current Copilot hooks reference has no PR-merged event, so the hook cannot directly subscribe to one. The agent's merge-status check keeps the fallback prompt from recording unmerged PR feedback.

## Documentation consulted

- [GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/plugins) for the requested plugin conventions (the page was unavailable during validation).
- [GitHub Copilot hooks reference](https://docs.github.com/en/copilot/reference/hooks-configuration), especially **Hook configuration format** and **Hook events**.
- [Using hooks with GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-hooks) for the `version: 1` and `sessionStart` configuration examples.