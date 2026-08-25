---
name: repo-intelligence
description: Builds repository-specific code-review guidance from merged pull-request review comments, manifests, and existing instructions. Use after a PR merges or when refreshing historical review insights.
---

# Repository Intelligence

Run this skill from a merged-PR webhook, scheduled job, or host-native event. A host without lifecycle events may invoke it manually, but the skill must verify the target PR is merged before writing either output.

## Outputs

1. `pr-insights.json`: raw, deduplicated, generalizable coding rules.
2. `.github/instructions/insights.instructions.md`: short reviewer instructions that summarize and reference `pr-insights.json`.

## Process

1. Fetch all review comments through the host's repository integration. Do not assume a particular tool name or MCP server.
2. Extract only actionable, generalizable rules. Ignore questions, clarification requests, one-off line-level nitpicks, and PR-specific observations.
3. Cleanse secrets, credentials, personal data, and irrelevant conversational text.
4. Detect language, frameworks, and packages from available manifests including `pom.xml`, `build.gradle`, `pyproject.toml`, `requirements.txt`, `Pipfile`, `package.json`, `go.mod`, `Cargo.toml`, and `*.csproj`.
5. Normalize comments and deduplicate by stable PR ID plus comment hash. Merge comments expressing the same rule and retain the clearest wording.
6. Mark shared or common-module rules with `shared: true` and record `module`. Use categories `suggestion`, `defect_pattern`, `performance`, `security`, `testing`, `code_quality`, and `database`.
7. Check `AGENTS.md` and existing `.github/instructions/` files. Do not repeat guidance already covered there.
8. Write only the two output files. Do not generate scripts, modify source code, or embed credentials.

## JSON Contract

```json
{
  "insights": [
    {
      "pattern": "...",
      "category": "suggestion",
      "language": "...",
      "description": "...",
      "module": "...",
      "shared": false,
      "evidence": [{ "prId": 123, "commentHash": "..." }]
    }
  ]
}
```

Re-running the same PR must not duplicate evidence or rules.

## Instructions File

Write `.github/instructions/insights.instructions.md` with `description` and `applyTo: "**"` frontmatter. Keep it short and use these sections in order: Source; Shared / Common Module Rules; Language & Package Guidelines; Dependency Health; Database; General Rules; Regression. Dependency Health must require checking known CVEs and approaching end of life. Regression must require updated tests, preserved coverage, and intact behavior and public contracts.