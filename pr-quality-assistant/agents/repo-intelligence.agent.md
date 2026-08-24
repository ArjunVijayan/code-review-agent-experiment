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

## Review-Comment Extraction Contract

Ask the repository integration available in the host to fetch all review comments for the target repository. Extract only generalizable coding rules and pass them to `insights-generator` as structured data:

```json
{
  "insights": [
    {
      "pattern": "...",
      "category": "suggestion|defect_pattern|performance|security|testing|code_quality|database",
      "language": "...",
      "description": "...",
      "module": "...",
      "shared": false
    }
  ]
}
```

Ignore questions, clarification requests, one-off line-level nitpicks, and PR-specific observations. Merge comments expressing the same rule and keep the clearest wording. Mark rules affecting shared or common modules with `shared: true` and record the module. Use `database` for schema, query, migration, transaction, or connection-handling feedback.

Inspect available manifests (`pom.xml`, `build.gradle`, `pyproject.toml`, `requirements.txt`, `Pipfile`, `package.json`, `go.mod`, `Cargo.toml`, and `*.csproj`) and pass detected language, framework, and package context to `insights-generator`. The generated guidance must also tell reviewers to check manifest dependencies for known CVEs and approaching end-of-life.

The generated instructions must put shared-module rules first, then language/package guidance, dependency health, database rules, remaining category-grouped rules, and regression guidance. Regression guidance must require reviewing changed or added tests, preserving existing coverage, and protecting existing behavior and public contracts. Deduplicate against any `AGENTS.md` and existing instruction files before updating `data/insights.instructions.md`.