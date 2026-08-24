---
name: change-blast-radius
description: Analyzes the PR diff to identify changed files, dependent/affected modules, and an overall risk tier (blast radius). Use after requirement-analysis and before test-analysis.
---

# Change & Blast Radius Analysis

## Purpose
Determine the full scope of impact of the code changes in the PR — not just the files touched, but everything that depends on them — and assign a risk tier to guide how strict downstream test analysis should be.

## Inputs
- PR diff (changed files, added/removed/modified lines)
- Repository dependency graph (imports, module references, shared config)
- `requirements[]` from `requirement-analysis`

## Steps
1. List all changed files and classify the type of change (logic, config, schema, styling, test-only).
2. Traverse direct and transitive dependents of changed files/modules.
3. Classify affected modules as `direct` or `indirect` impact.
4. Assign a `riskTier` (`low` | `medium` | `high`) per the methodology in `references/blast-radius-methodology.md`.
5. Summarize the blast radius in plain language for the final report.

See `references/blast-radius-methodology.md` for detailed scoring rules and dependency traversal approach.

## Output Contract
```json
{
  "changedFiles": ["path/to/file.ts"],
  "affectedModules": [
    { "module": "...", "impact": "direct|indirect" }
  ],
  "riskTier": "low|medium|high",
  "blastRadiusSummary": "..."
}
```

## Handoff
Pass `changedFiles[]`, `affectedModules[]`, and `riskTier` to `test-analysis`. A `high` risk tier should cause the orchestrator to run test-analysis in strict mode.
