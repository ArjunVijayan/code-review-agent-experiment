# Blast Radius Methodology

## Goal
Provide a repeatable, explainable method for quantifying how far the impact of a change can propagate through a codebase, so risk can be assessed objectively rather than by intuition.

## Step 1 — Classify Changed Files
For each file in the diff, classify the change type:
| Change Type | Examples |
|---|---|
| Logic | function/method body changes |
| Interface | function signature, exported type, API contract changes |
| Schema | DB schema, GraphQL schema, config schema |
| Config | env vars, feature flags, build config |
| Styling | CSS/UI-only changes with no logic impact |
| Test-only | changes confined to test files |

## Step 2 — Dependency Traversal
1. Build (or reuse) a dependency graph from static imports/references.
2. **Direct impact**: modules that directly import/reference a changed file or symbol.
3. **Indirect impact**: modules that depend on a direct-impact module (traverse up to 2 levels by default; deeper only if the change is an `Interface` or `Schema` type).
4. Stop traversal at natural boundaries (e.g., published package boundaries, microservice boundaries) but flag cross-boundary impacts as high-attention items.

## Step 3 — Risk Tier Scoring
Score = weighted sum of:
- Change type weight: Interface/Schema = 3, Logic = 2, Config = 2, Styling = 1, Test-only = 0
- Number of direct-impact modules (capped contribution)
- Number of indirect-impact modules (capped contribution, lower weight than direct)
- Whether changed code sits on a critical path (auth, payments, data integrity) — apply a multiplier if so

| Score Range | Risk Tier |
|---|---|
| 0–3 | low |
| 4–8 | medium |
| 9+ | high |

## Step 4 — Summarize
Produce a human-readable summary, e.g.:
> "3 files changed (2 logic, 1 interface). 4 direct-impact modules, 7 indirect-impact modules across the `billing` domain. Risk tier: **high** due to interface change on a critical payment path."

## Notes for Implementers
- Prefer static analysis tools available in-repo (e.g., `madge`, language-server references) over manual heuristics when possible.
- If no dependency graph tooling is available, fall back to grep-based reference search and clearly flag reduced confidence in the summary.
