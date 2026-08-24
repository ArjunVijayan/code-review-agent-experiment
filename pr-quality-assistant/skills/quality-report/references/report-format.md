# Quality Report Format

## Required Report Structure

```markdown
# PR Quality Report — <PR title>

## Summary
<1-2 sentence overview: what the PR does, overall verdict>

## Quality Score: <0-100> (<Tier: Excellent/Good/Needs Work/At Risk>)

## Risk Assessment
- **Blast Radius Risk Tier:** low | medium | high
- **Blast Radius Summary:** <from change-blast-radius>
- **Affected Modules:** <count, direct vs indirect>

## Acceptance Criteria Traceability
| AC ID | Description | Status | Test(s) |
|---|---|---|---|
| AC-1 | ... | ✅ Passed / 🆕 Generated / ⚠️ Untested | ... |

## Test Coverage
- Existing tests mapped: <count>
- Gaps identified: <count> (blocking: <n>, warning: <n>)
- Tests generated: <count>
- Gaps still open (require human follow-up): <list with reasons>

## Recommendations
1. **[Blocking]** <description + suggested action>
2. **[Warning]** <description + suggested action>
3. **[Info]** <description>

## Open Questions (from Requirement Analysis)
- <any ambiguities flagged earlier that still need clarification>
```

## Quality Score Rubric
Score starts at 100 and is reduced by weighted deductions:

| Factor | Deduction |
|---|---|
| Each `blocking` coverage gap left open | -15 (max -45) |
| Each `warning` coverage gap left open | -5 (max -20) |
| Unresolved `openQuestions` from requirement-analysis | -10 each (max -20) |
| `riskTier: high` with any open gap | additional -10 |
| All acceptance criteria traced to passing/generated tests | +0 (baseline expectation, no bonus) |

Floor the score at 0. Map to tiers:
| Score | Tier |
|---|---|
| 90–100 | Excellent |
| 75–89 | Good |
| 50–74 | Needs Work |
| 0–49 | At Risk |

## Formatting Rules
- Always use the exact section headers above so the report is diffable/parseable across PRs.
- Use status emojis consistently (✅ / 🆕 / ⚠️) only in the traceability table, not elsewhere.
- Keep the Summary to 1-2 sentences — details belong in their respective sections.
- Never omit the Open Questions section, even if empty — write "None" explicitly.
