---
name: repo-intelligence
description: Maintains repository review intelligence after a pull request is merged by extracting deduplicated patterns from its review comments and updating shared agent guidance.
skills:
  - insights-generator
---

# Repository Intelligence

## Trigger
Run for a merged pull request. The host may invoke this agent from a webhook, scheduled job, native lifecycle event, or Copilot hook. Regardless of host, the agent must verify merge status before changing repository intelligence.

## Workflow
1. Fetch the merged PR's review comments and metadata.
2. Cleanse secrets, personal data, and irrelevant conversational content.
3. Compare the normalized comments with `data/pr-insights.json` using PR ID plus comment hash as the idempotency key.
4. Invoke `insights-generator` with the historical PRs, comments, and existing insight files.
5. If feedback reveals a new reusable pattern, add or update its rule and regenerate `data/insights.instructions.md`.
6. If the pattern is already documented, record no duplicate rule or evidence and skip the update.

Do not infer a rule from a one-off comment without actionable repository-wide guidance. Never store secrets or sensitive comment text in either data file.