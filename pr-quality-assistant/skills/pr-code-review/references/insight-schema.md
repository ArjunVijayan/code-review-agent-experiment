# Insight State and Data Schemas

`pr-insights.json` stores distilled knowledge:

```json
{
  "insights": [
    {
      "pattern": "...",
      "category": "security",
      "language": "python",
      "description": "...",
      "module": "...",
      "shared": true,
      "evidence": [{ "change_request_id": "101", "comment_hash": "..." }]
    }
  ]
}
```

`.code-review/insights-state.json` stores processing state only:

```json
{
  "base_ref": "main",
  "last_analyzed_at": "2026-08-26T00:30:00Z",
  "analyzed_change_requests": ["101", "102"]
}
```

State is updated only after insight generation succeeds. Change-request IDs are strings so providers can use numeric PRs, GitLab MRs, or other stable identifiers consistently.